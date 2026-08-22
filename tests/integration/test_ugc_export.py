import io
import json
import tempfile
import unittest
import zipfile
from pathlib import Path

from tetrative_os.artifacts import ArtifactStore
from tetrative_os.exporter import UgcPackageExporter
from tetrative_os.memory import MemoryStore
from tetrative_os.models import Goal
from tetrative_os.orchestrator import Orchestrator
from tetrative_os.providers import DeterministicMockProvider


class UgcExportIntegrationTests(unittest.TestCase):
    def test_reviewed_run_exports_verifiable_zip(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            memory = MemoryStore(root / "memory.db")
            artifacts = ArtifactStore(root / "artifacts")
            try:
                paused = Orchestrator(DeterministicMockProvider(), memory).run(
                    Goal("Create reviewed campaign", domain="ugc")
                )
                artifact = UgcPackageExporter(artifacts).export(
                    paused.run_id, memory.load_checkpoint(paused.run_id)
                )
                _, content = artifacts.get(artifact.id)
                with zipfile.ZipFile(io.BytesIO(content)) as package:
                    names = package.namelist()
                    self.assertIn("manifest.json", names)
                    self.assertIn("stages/production_plan.md", names)
                    manifest = json.loads(package.read("manifest.json"))
                    self.assertEqual(manifest["run_id"], paused.run_id)
                    self.assertEqual(manifest["status"], "awaiting_human_approval")
            finally:
                memory.close()


if __name__ == "__main__":
    unittest.main()
