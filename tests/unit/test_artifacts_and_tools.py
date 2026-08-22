import json
import tempfile
import unittest
from pathlib import Path

from tetrative_os.artifacts import ArtifactStore
from tetrative_os.tools import (
    SideEffect,
    ToolInvocation,
    ToolPolicy,
    ToolPolicyError,
    ToolRegistry,
)


class ArtifactAndToolTests(unittest.TestCase):
    def test_artifact_round_trip_and_tamper_detection(self):
        with tempfile.TemporaryDirectory() as directory:
            store = ArtifactStore(directory)
            artifact = store.put_json({"evidence": "value"}, kind="test.v1")
            loaded, content = store.get(artifact.id)
            self.assertEqual(loaded.sha256, artifact.sha256)
            self.assertEqual(json.loads(content), {"evidence": "value"})
            (Path(directory) / loaded.path).write_bytes(b"tampered")
            with self.assertRaises(RuntimeError):
                store.get(artifact.id)

    def test_artifact_record_cannot_redirect_blob_path(self):
        with tempfile.TemporaryDirectory() as directory:
            store = ArtifactStore(directory)
            artifact = store.put(b"safe", kind="test.v1", content_type="text/plain")
            record = Path(directory) / "records" / f"{artifact.id}.json"
            data = json.loads(record.read_text())
            data["path"] = "../../outside"
            record.write_text(json.dumps(data))
            with self.assertRaises(RuntimeError):
                store.get(artifact.id)

    def test_tool_registry_fails_closed_and_is_idempotent(self):
        registry = ToolRegistry()
        calls = []
        registry.register(
            ToolPolicy(
                name="publisher.preview.v1",
                description="Build a non-publishing preview",
                side_effect=SideEffect.REVERSIBLE,
                required_capability="preview",
                allowed_input_keys=frozenset({"caption"}),
            ),
            lambda value: calls.append(value) or {"preview": value["caption"]},
        )
        invocation = ToolInvocation(
            tool="publisher.preview.v1",
            input={"caption": "hello"},
            capability="preview",
            approval_artifact_hash="a" * 64,
            idempotency_key="run:stage:preview",
            dry_run=True,
        )
        first = registry.invoke(invocation)
        second = registry.invoke(invocation)
        self.assertEqual(first, second)
        self.assertEqual(len(calls), 1)

    def test_tool_rejects_unknown_input_and_real_side_effect(self):
        registry = ToolRegistry()
        registry.register(
            ToolPolicy(
                "message.send.v1",
                "Send message",
                SideEffect.IRREVERSIBLE,
                "message",
                allowed_input_keys=frozenset({"text"}),
            ),
            lambda value: value,
        )
        with self.assertRaises(ToolPolicyError):
            registry.invoke(
                ToolInvocation(
                    "message.send.v1",
                    {"text": "x", "secret": "leak"},
                    capability="message",
                    approval_artifact_hash="a" * 64,
                    idempotency_key="1",
                )
            )
        with self.assertRaises(ToolPolicyError):
            registry.invoke(
                ToolInvocation(
                    "message.send.v1",
                    {"text": "x"},
                    capability="message",
                    approval_artifact_hash="a" * 64,
                    idempotency_key="2",
                    dry_run=False,
                )
            )


if __name__ == "__main__":
    unittest.main()
