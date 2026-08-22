from __future__ import annotations

import time
from dataclasses import dataclass

from .providers import ModelProvider


class ModelBudgetExceeded(RuntimeError):
    """Raised before a model call would exceed the configured run budget."""


class ProviderCircuitOpen(RuntimeError):
    """Raised when repeated provider failures trip the circuit breaker."""


@dataclass(slots=True)
class RuntimeMetrics:
    model_calls: int = 0
    provider_attempts: int = 0
    provider_failures: int = 0
    retries: int = 0
    input_characters: int = 0
    output_characters: int = 0


class ResilientProvider:
    """Budget, retry, and circuit-breaker boundary around any model provider.

    One logical ``generate`` counts as one model call; transport retries are tracked separately.
    The wrapper deliberately retries only RuntimeError because programmer and schema errors should
    fail immediately rather than be hidden by retries.
    """

    def __init__(
        self,
        provider: ModelProvider,
        *,
        max_calls: int = 100,
        max_retries: int = 1,
        failure_threshold: int = 3,
        retry_delay_seconds: float = 0.05,
    ) -> None:
        if max_calls < 0 or max_retries < 0 or failure_threshold < 1:
            raise ValueError("Invalid provider runtime limits")
        self.provider = provider
        self.name = f"resilient:{provider.name}"
        self.max_calls = max_calls
        self.max_retries = max_retries
        self.failure_threshold = failure_threshold
        self.retry_delay_seconds = retry_delay_seconds
        self.metrics = RuntimeMetrics()
        self._consecutive_failures = 0
        self._circuit_open = False

    def generate(self, system: str, prompt: str, *, temperature: float = 0.2) -> str:
        if self._circuit_open:
            raise ProviderCircuitOpen("Model provider circuit is open after repeated failures")
        if self.metrics.model_calls >= self.max_calls:
            raise ModelBudgetExceeded(f"Model-call budget exhausted ({self.max_calls})")

        self.metrics.model_calls += 1
        self.metrics.input_characters += len(system) + len(prompt)
        last_error: RuntimeError | None = None
        for attempt in range(self.max_retries + 1):
            self.metrics.provider_attempts += 1
            try:
                output = self.provider.generate(system, prompt, temperature=temperature)
                if not isinstance(output, str) or not output.strip():
                    raise RuntimeError("Model returned empty or non-text output")
                self._consecutive_failures = 0
                self.metrics.output_characters += len(output)
                return output.strip()
            except RuntimeError as exc:
                last_error = exc
                self.metrics.provider_failures += 1
                self._consecutive_failures += 1
                if self._consecutive_failures >= self.failure_threshold:
                    self._circuit_open = True
                    raise ProviderCircuitOpen(
                        f"Provider circuit opened after {self._consecutive_failures} failures"
                    ) from exc
                if attempt < self.max_retries:
                    self.metrics.retries += 1
                    time.sleep(self.retry_delay_seconds * (2**attempt))
        assert last_error is not None
        raise last_error
