import tempfile
import unittest
from pathlib import Path

from tetrative_os.memory import MemoryStore
from tetrative_os.models import Goal
from tetrative_os.orchestrator import ApprovalError, Orchestrator
from tetrative_os.providers import DeterministicMockProvider
from tetrative_os.runtime import ModelBudgetExceeded
from tetrative_os.topology import WORKFLOWS


class OrchestratorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.memory = MemoryStore(Path(self.temp.name) / "memory.db")
        self.provider = DeterministicMockProvider()

    def tearDown(self):
        self.memory.close()
        self.temp.cleanup()

    def test_all_domains_complete_with_auto_approval(self):
        for domain, stages in WORKFLOWS.items():
            result = Orchestrator(self.provider, self.memory).run(
                Goal("Build a measurable vertical slice", domain=domain), auto_approve=True
            )
            self.assertEqual(result.status, "completed")
            self.assertEqual(len(result.stages), len(stages))
            self.assertGreater(result.metrics["total_candidates"], len(stages))
            self.assertTrue(self.memory.events(result.run_id))

    def test_human_gate_stops_consequential_flow(self):
        result = Orchestrator(self.provider, self.memory).run(
            Goal("Launch a campaign", domain="ugc"), auto_approve=False
        )
        self.assertEqual(result.status, "awaiting_human_approval")
        self.assertTrue(result.stages[-1].human_gate)
        self.assertEqual(result.stages[-1].stage, "production_plan")

    def test_unknown_domain_is_rejected(self):
        with self.assertRaises(ValueError):
            Orchestrator(self.provider, self.memory).run(Goal("x", domain="unknown"))

    def test_empty_goal_is_rejected(self):
        with self.assertRaises(ValueError):
            Goal("   ")

    def test_human_gate_can_resume_without_repeating_approved_stage(self):
        orchestrator = Orchestrator(self.provider, self.memory)
        paused = orchestrator.run(Goal("Launch safely", domain="ugc"))
        digest = paused.approval_required["artifact_hash"]
        stage_events_before = len(
            [event for event in self.memory.events(paused.run_id) if event["kind"] == "stage_completed"]
        )

        completed = orchestrator.resume(paused.run_id, digest, approver="human@example.test")

        self.assertEqual(completed.status, "completed")
        self.assertEqual(completed.run_id, paused.run_id)
        self.assertGreater(completed.metrics["model_calls"], paused.metrics["model_calls"])
        self.assertEqual(stage_events_before + 1, len(completed.stages))
        approval_events = [
            event for event in self.memory.events(paused.run_id) if event["kind"] == "human_approved"
        ]
        self.assertEqual(len(approval_events), 1)

    def test_resume_rejects_wrong_artifact_hash(self):
        orchestrator = Orchestrator(self.provider, self.memory)
        paused = orchestrator.run(Goal("Launch safely", domain="ugc"))
        with self.assertRaises(ApprovalError):
            orchestrator.resume(paused.run_id, "0" * 64, approver="reviewer")

    def test_resume_rejects_unsupported_checkpoint_version(self):
        orchestrator = Orchestrator(self.provider, self.memory)
        paused = orchestrator.run(Goal("Launch safely", domain="ugc"))
        checkpoint = self.memory.load_checkpoint(paused.run_id)
        checkpoint["payload"]["checkpoint_schema_version"] = 999
        self.memory.save_checkpoint(
            paused.run_id,
            "awaiting_human_approval",
            checkpoint["payload"],
            checkpoint["artifact_hash"],
        )
        with self.assertRaises(ApprovalError):
            orchestrator.resume(
                paused.run_id,
                checkpoint["artifact_hash"],
                approver="reviewer",
            )

    def test_model_call_budget_fails_closed_and_checkpoints(self):
        orchestrator = Orchestrator(
            self.provider, self.memory, max_model_calls=1, provider_retries=0
        )
        with self.assertRaises(ModelBudgetExceeded):
            orchestrator.run(Goal("Bound this run", domain="meta"), auto_approve=True)
        row = self.memory.db.execute(
            "SELECT status FROM checkpoints ORDER BY updated_at DESC LIMIT 1"
        ).fetchone()
        self.assertEqual(row["status"], "failed")

    def test_run_serializes(self):
        result = Orchestrator(self.provider, self.memory, candidates_per_stage=1).run(
            Goal("Diagnose cognition", domain="meta"), auto_approve=True
        )
        payload = result.to_dict()
        self.assertEqual(payload["goal"]["objective"], "Diagnose cognition")
        self.assertIn("average_quality", payload["metrics"])


if __name__ == "__main__":
    unittest.main()
