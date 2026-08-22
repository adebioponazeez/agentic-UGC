from __future__ import annotations

import hashlib
import io
import json
import zipfile
from datetime import UTC, datetime
from typing import Any

from .artifacts import Artifact, ArtifactStore


class UgcPackageExporter:
    """Export an approved/completed UGC run as an integrity-verifiable production package."""

    def __init__(self, artifacts: ArtifactStore) -> None:
        self.artifacts = artifacts

    def export(self, run_id: str, checkpoint: dict[str, Any]) -> Artifact:
        payload = checkpoint["payload"]
        goal = payload.get("goal", {})
        if goal.get("domain") not in {"ugc", "ecosystem"}:
            raise ValueError("UGC package export requires a UGC or ecosystem run")
        if checkpoint["status"] not in {"awaiting_human_approval", "completed"}:
            raise ValueError("Only reviewed checkpoints or completed runs can be exported")

        files: dict[str, bytes] = {}
        for result in payload.get("results", []):
            stage = self._safe_name(result["stage"])
            files[f"stages/{stage}.md"] = result["selected"]["content"].encode()
        files["README.md"] = self._readme(run_id, checkpoint).encode()

        manifest = {
            "schema_version": 1,
            "run_id": run_id,
            "domain": goal.get("domain"),
            "status": checkpoint["status"],
            "workflow_version": payload.get("workflow_version"),
            "checkpoint_schema_version": payload.get("checkpoint_schema_version"),
            "approval_artifact_hash": checkpoint.get("artifact_hash"),
            "exported_at": datetime.now(UTC).isoformat(),
            "files": {
                path: {"sha256": hashlib.sha256(content).hexdigest(), "size": len(content)}
                for path, content in sorted(files.items())
            },
        }
        files["manifest.json"] = json.dumps(manifest, indent=2, sort_keys=True).encode()
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for path, content in sorted(files.items()):
                archive.writestr(path, content)
        return self.artifacts.put(
            buffer.getvalue(),
            kind="ugc.production-package.v1",
            content_type="application/zip",
            metadata={"run_id": run_id, "status": checkpoint["status"]},
        )

    @staticmethod
    def _safe_name(value: str) -> str:
        cleaned = "".join(character if character.isalnum() or character in "-_" else "-" for character in value)
        return cleaned.strip("-") or "stage"

    @staticmethod
    def _readme(run_id: str, checkpoint: dict[str, Any]) -> str:
        goal = checkpoint["payload"].get("goal", {})
        return (
            "# Tetrative UGC production package\n\n"
            f"- Run: `{run_id}`\n"
            f"- Status: `{checkpoint['status']}`\n"
            f"- Objective: {goal.get('objective', '')}\n"
            f"- Audience: {goal.get('audience', '')}\n\n"
            "Every stage is a proposal. Verify factual claims, rights, consent, disclosures, platform "
            "requirements, and final human approval before publication. File hashes are in manifest.json.\n"
        )
