import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class CliCheckpointIntegrationTests(unittest.TestCase):
    def test_cli_pause_and_resume_uses_same_run(self):
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            database = directory / "memory.db"
            paused_file = directory / "paused.json"
            resumed_file = directory / "resumed.json"
            env = {**os.environ, "PYTHONPATH": str(ROOT / "src")}

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "tetrative_os.cli",
                    "Launch reviewed UGC",
                    "--domain",
                    "ugc",
                    "--mock",
                    "--memory",
                    str(database),
                    "--output",
                    str(paused_file),
                ],
                cwd=ROOT,
                env=env,
                check=True,
                capture_output=True,
                text=True,
            )
            paused = json.loads(paused_file.read_text())
            self.assertEqual(paused["status"], "awaiting_human_approval")

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "tetrative_os.cli",
                    "--resume",
                    paused["run_id"],
                    "--approve",
                    paused["approval_required"]["artifact_hash"],
                    "--approver",
                    "integration-reviewer",
                    "--mock",
                    "--memory",
                    str(database),
                    "--output",
                    str(resumed_file),
                ],
                cwd=ROOT,
                env=env,
                check=True,
                capture_output=True,
                text=True,
            )
            resumed = json.loads(resumed_file.read_text())
            self.assertEqual(resumed["status"], "completed")
            self.assertEqual(resumed["run_id"], paused["run_id"])
            self.assertEqual(len(resumed["stages"]), 5)


if __name__ == "__main__":
    unittest.main()
