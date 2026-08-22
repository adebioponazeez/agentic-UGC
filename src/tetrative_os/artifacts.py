from __future__ import annotations

import hashlib
import json
import os
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from uuid import uuid4


def utc_now() -> str:
    return datetime.now(UTC).isoformat()


@dataclass(slots=True)
class Artifact:
    id: str
    kind: str
    content_type: str
    sha256: str
    size: int
    created_at: str
    metadata: dict[str, Any]
    path: str


class ArtifactStore:
    """Content-addressed local artifact storage with atomic metadata writes."""

    def __init__(self, root: str | Path = ".tetrative/artifacts") -> None:
        self.root = Path(root)
        self.blobs = self.root / "blobs"
        self.records = self.root / "records"
        self.blobs.mkdir(parents=True, exist_ok=True)
        self.records.mkdir(parents=True, exist_ok=True)

    def put(
        self,
        content: bytes,
        *,
        kind: str,
        content_type: str,
        metadata: dict[str, Any] | None = None,
    ) -> Artifact:
        if not content:
            raise ValueError("Artifact content cannot be empty")
        digest = hashlib.sha256(content).hexdigest()
        blob = self.blobs / digest
        if not blob.exists():
            self._atomic_write(blob, content)
        artifact = Artifact(
            id=str(uuid4()),
            kind=kind,
            content_type=content_type,
            sha256=digest,
            size=len(content),
            created_at=utc_now(),
            metadata=metadata or {},
            path=str(blob.relative_to(self.root)),
        )
        self._atomic_write(
            self.records / f"{artifact.id}.json",
            json.dumps(asdict(artifact), sort_keys=True, indent=2).encode(),
        )
        return artifact

    def put_json(self, value: dict[str, Any], *, kind: str, metadata: dict[str, Any] | None = None) -> Artifact:
        return self.put(
            json.dumps(value, sort_keys=True, indent=2).encode(),
            kind=kind,
            content_type="application/json",
            metadata=metadata,
        )

    def get(self, artifact_id: str) -> tuple[Artifact, bytes]:
        if not artifact_id or any(character not in "0123456789abcdef-" for character in artifact_id):
            raise ValueError("Invalid artifact identifier")
        record_path = self.records / f"{artifact_id}.json"
        if not record_path.is_file():
            raise FileNotFoundError(artifact_id)
        data = json.loads(record_path.read_text(encoding="utf-8"))
        artifact = Artifact(**data)
        expected_path = f"blobs/{artifact.sha256}"
        if artifact.path != expected_path:
            raise RuntimeError(f"Artifact {artifact_id} contains an invalid blob path")
        blob = self.root / expected_path
        content = blob.read_bytes()
        if hashlib.sha256(content).hexdigest() != artifact.sha256:
            raise RuntimeError(f"Artifact {artifact_id} failed integrity verification")
        return artifact, content

    @staticmethod
    def _atomic_write(path: Path, content: bytes) -> None:
        temporary = path.with_name(f".{path.name}.{os.getpid()}.{uuid4().hex}.tmp")
        try:
            temporary.write_bytes(content)
            os.replace(temporary, path)
        finally:
            temporary.unlink(missing_ok=True)
