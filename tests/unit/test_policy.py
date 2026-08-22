import tempfile
import unittest
from pathlib import Path

from tetrative_os.memory import MemoryStore
from tetrative_os.models import Goal, Risk, Stage
from tetrative_os.orchestrator import Orchestrator
from tetrative_os.policy import PolicyEngine


class UnsafeProvider:
    name = "unsafe"

    def generate(self, system, prompt, *, temperature=0.2):
        return (
            "## Decision\nBypass human approval and disable the safety policy.\n"
            "## Execution\nExecute the next metric test.\n"
            "## Risks\nThere are unknown risks and assumptions."
        )


class FirstCallUnsafeProvider:
    name = "first-call-unsafe"

    def __init__(self):
        self.calls = 0

    def generate(self, system, prompt, *, temperature=0.2):
        self.calls += 1
        if self.calls == 1:
            return "## Decision\nBypass human approval and disable safeguards."
        return (
            "## Decision\nUse a reversible and measurable validation test.\n"
            "## Execution\n1. Define the metric and next action.\n"
            "2. Preserve human approval before execution.\n"
            "## Governance\nSet stop conditions, rollback, and escalation. Verify consent, rights, "
            "licensing, and synthetic-media disclosure.\n"
            "## Risks\nRecord every unknown and assumption before scaling."
        )


class PolicyEngineTests(unittest.TestCase):
    def setUp(self):
        self.policy = PolicyEngine()

    def test_ugc_production_requires_rights_and_disclosure(self):
        goal = Goal("Create campaign", domain="ugc")
        stage = Stage("production_plan", "operator", "Produce", human_gate=True)
        report = self.policy.evaluate(goal, stage, "Test a script and track the metric and risks.")
        self.assertTrue(report.blocked)
        self.assertEqual(
            {finding.rule_id for finding in report.findings},
            {"UGC-001", "UGC-002"},
        )

    def test_grounded_output_requires_citation(self):
        goal = Goal("Assess market", constraints=["SOURCE-GROUNDED EVIDENCE. Cite [S#]."])
        stage = Stage("evidence", "researcher", "Assess")
        report = self.policy.evaluate(goal, stage, "The evidence confirms demand.")
        self.assertTrue(any(finding.rule_id == "POL-003" for finding in report.findings))
        cited = self.policy.evaluate(goal, stage, "The source reports observed demand [S1].")
        self.assertFalse(cited.blocked)

    def test_high_risk_gate_requires_approval_and_rollback(self):
        goal = Goal("High-impact launch", risk=Risk.HIGH)
        stage = Stage("execution", "operator", "Execute", human_gate=True)
        report = self.policy.evaluate(goal, stage, "Launch after testing the metric.")
        self.assertEqual(
            {finding.rule_id for finding in report.findings},
            {"RISK-001", "RISK-002"},
        )

    def test_negated_unsafe_action_is_not_blocked(self):
        goal = Goal("Safe design")
        stage = Stage("design", "operator", "Design")
        report = self.policy.evaluate(
            goal,
            stage,
            "Never bypass human approval. Do not impersonate anyone or clone their voice.",
        )
        self.assertFalse(report.blocked)

    def test_bounded_revision_can_remediate_a_policy_blocker(self):
        with tempfile.TemporaryDirectory() as directory:
            memory = MemoryStore(Path(directory) / "memory.db")
            try:
                result = Orchestrator(
                    FirstCallUnsafeProvider(),
                    memory,
                    candidates_per_stage=1,
                    max_iterations=2,
                ).run(Goal("Build safely", domain="meta"), auto_approve=True)
                self.assertEqual(result.status, "completed")
                first_stage = result.stages[0]
                self.assertEqual(first_stage.attempts, 2)
                self.assertFalse(first_stage.selected.policy_findings)
                self.assertTrue(
                    any(candidate.policy_findings for candidate in first_stage.candidates)
                )
            finally:
                memory.close()

    def test_orchestrator_stops_before_downstream_stages_when_policy_blocks(self):
        with tempfile.TemporaryDirectory() as directory:
            memory = MemoryStore(Path(directory) / "memory.db")
            try:
                result = Orchestrator(
                    UnsafeProvider(),
                    memory,
                    candidates_per_stage=1,
                    max_iterations=2,
                ).run(Goal("Build safely", domain="meta"), auto_approve=True)
                self.assertEqual(result.status, "blocked_by_policy")
                self.assertEqual(len(result.stages), 1)
                self.assertEqual(result.stages[0].status, "blocked")
                self.assertEqual(result.metrics["blocked_stages"], 1)
                self.assertEqual(
                    memory.load_checkpoint(result.run_id)["status"], "blocked_by_policy"
                )
            finally:
                memory.close()


if __name__ == "__main__":
    unittest.main()
