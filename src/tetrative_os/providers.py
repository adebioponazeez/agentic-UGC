from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Protocol


class ModelProvider(Protocol):
    name: str

    def generate(self, system: str, prompt: str, *, temperature: float = 0.2) -> str: ...


@dataclass(slots=True)
class OpenAICompatibleProvider:
    """Works with Ollama, vLLM, llama.cpp servers, and compatible cloud APIs."""

    base_url: str = "http://localhost:11434/v1"
    model: str = "qwen3:8b"
    api_key: str = "local"
    timeout: int = 120
    max_response_bytes: int = 10_000_000
    name: str = "openai-compatible"

    def __post_init__(self) -> None:
        parsed = urllib.parse.urlparse(self.base_url)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError("Model base_url must be an absolute HTTP(S) URL")
        if not self.model.strip():
            raise ValueError("Model name cannot be empty")
        if self.timeout < 1 or self.max_response_bytes < 1:
            raise ValueError("Provider limits must be positive")

    @classmethod
    def from_env(cls) -> OpenAICompatibleProvider:
        return cls(
            base_url=os.getenv("TETRATIVE_BASE_URL", "http://localhost:11434/v1"),
            model=os.getenv("TETRATIVE_MODEL", "qwen3:8b"),
            api_key=os.getenv("TETRATIVE_API_KEY", "local"),
        )

    def generate(self, system: str, prompt: str, *, temperature: float = 0.2) -> str:
        payload = json.dumps(
            {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": prompt},
                ],
                "temperature": temperature,
            }
        ).encode()
        request = urllib.request.Request(
            f"{self.base_url.rstrip('/')}/chat/completions",
            data=payload,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                raw = response.read(self.max_response_bytes + 1)
                if len(raw) > self.max_response_bytes:
                    raise RuntimeError("Model response exceeded configured size limit")
                body = json.loads(raw)
            content = body["choices"][0]["message"]["content"]
            if not isinstance(content, str) or not content.strip():
                raise RuntimeError("Model response contained no text content")
            return content.strip()
        except (urllib.error.URLError, TimeoutError) as exc:
            raise RuntimeError(
                f"Model endpoint unavailable at {self.base_url}. Start Ollama/vLLM or use --mock."
            ) from exc
        except (json.JSONDecodeError, KeyError, IndexError, TypeError) as exc:
            raise RuntimeError("Model endpoint returned an invalid chat-completions response") from exc


@dataclass(slots=True)
class DeterministicMockProvider:
    """Offline provider for demos and tests. It proves orchestration, not content quality."""

    name: str = "deterministic-mock"
    calls: int = 0

    def generate(self, system: str, prompt: str, *, temperature: float = 0.2) -> str:
        self.calls += 1
        role = system.splitlines()[0].replace("You are ", "").strip(". ")
        focus = " ".join(prompt.split())[:500]
        return (
            f"## {role} output\n"
            f"Call {self.calls}. Objective interpreted from: {focus}\n\n"
            "### Decision\nPrioritize a falsifiable, audience-specific vertical slice.\n\n"
            "### Execution\n1. Validate the highest-risk assumption.\n"
            "2. Produce one measurable artifact.\n"
            "3. Instrument outcomes and feed evidence into the next iteration.\n\n"
            "### Risks\nUnverified demand, weak evidence, model hallucination, and premature scaling.\n"
        )
