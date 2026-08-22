import tempfile
import unittest
from pathlib import Path

from tetrative_os.memory import MemoryStore
from tetrative_os.models import Goal
from tetrative_os.orchestrator import Orchestrator
from tetrative_os.providers import DeterministicMockProvider
from tetrative_os.topology import WORKFLOWS


class EcosystemJourneyTests(unittest.TestCase):
    def test_integrated_ecosystem_completes_declared_workflow(self):
        with tempfile.TemporaryDirectory() as directory:
            memory = MemoryStore(Path(directory) / "memory.db")
            try:
                result = Orchestrator(DeterministicMockProvider(), memory).run(
                    Goal(
                        "Build an evidence-led creator venture ecosystem",
                        domain="ecosystem",
                        audience="African founders",
                        success_metrics=["ten design partners"],
                    ),
                    auto_approve=True,
                )
                self.assertEqual(result.status, "completed")
                self.assertEqual(
                    [stage.stage for stage in result.stages],
                    [stage.name for stage in WORKFLOWS["ecosystem"]],
                )
                self.assertEqual(
                    memory.load_checkpoint(result.run_id)["payload"]["next_stage"],
                    len(WORKFLOWS["ecosystem"]),
                )
            finally:
                memory.close()


if __name__ == "__main__":
    unittest.main()
