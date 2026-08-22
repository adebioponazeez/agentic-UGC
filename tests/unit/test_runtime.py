import unittest

from tetrative_os.providers import OpenAICompatibleProvider
from tetrative_os.runtime import ModelBudgetExceeded, ProviderCircuitOpen, ResilientProvider


class FakeProvider:
    name = "fake"

    def __init__(self, outcomes):
        self.outcomes = list(outcomes)
        self.calls = 0

    def generate(self, system, prompt, *, temperature=0.2):
        self.calls += 1
        outcome = self.outcomes.pop(0)
        if isinstance(outcome, Exception):
            raise outcome
        return outcome


class RuntimeTests(unittest.TestCase):
    def test_transient_provider_failure_is_retried_and_measured(self):
        provider = FakeProvider([RuntimeError("temporary"), "recovered"])
        runtime = ResilientProvider(provider, max_calls=1, max_retries=1)
        self.assertEqual(runtime.generate("system", "prompt"), "recovered")
        self.assertEqual(runtime.metrics.model_calls, 1)
        self.assertEqual(runtime.metrics.provider_attempts, 2)
        self.assertEqual(runtime.metrics.retries, 1)

    def test_logical_call_budget_is_hard_limit(self):
        runtime = ResilientProvider(FakeProvider(["one"]), max_calls=1)
        runtime.generate("system", "prompt")
        with self.assertRaises(ModelBudgetExceeded):
            runtime.generate("system", "prompt")

    def test_circuit_opens_after_repeated_failures(self):
        runtime = ResilientProvider(
            FakeProvider([RuntimeError("a"), RuntimeError("b")]),
            max_calls=5,
            max_retries=1,
            failure_threshold=2,
        )
        with self.assertRaises(ProviderCircuitOpen):
            runtime.generate("system", "prompt")
        with self.assertRaises(ProviderCircuitOpen):
            runtime.generate("system", "prompt")

    def test_invalid_provider_url_is_rejected(self):
        with self.assertRaises(ValueError):
            OpenAICompatibleProvider(base_url="file:///etc/passwd")


if __name__ == "__main__":
    unittest.main()
