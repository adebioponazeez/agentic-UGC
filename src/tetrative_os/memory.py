from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any


DATABASE_SCHEMA_VERSION = 1
CHECKPOINT_STATUSES = {"running", "awaiting_human_approval", "failed", "completed"}


class DatabaseVersionError(RuntimeError):
    """Raised when storage is newer than this binary can safely interpret."""


class MemoryStore:
    """Append-oriented episodic memory and durable run state, backed by SQLite."""

    def __init__(self, path: str | Path = ".tetrative/memory.db") -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(self.path, timeout=5.0)
        self.db.row_factory = sqlite3.Row
        self.db.execute("PRAGMA foreign_keys=ON")
        self.db.execute("PRAGMA busy_timeout=5000")
        self.db.execute("PRAGMA journal_mode=WAL")
        self._migrate()

    def _migrate(self) -> None:
        current = int(self.db.execute("PRAGMA user_version").fetchone()[0])
        if current > DATABASE_SCHEMA_VERSION:
            self.db.close()
            raise DatabaseVersionError(
                f"Database schema {current} is newer than supported {DATABASE_SCHEMA_VERSION}"
            )
        if current < 1:
            self.db.executescript(
                """
                BEGIN;
                CREATE TABLE IF NOT EXISTS events (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  run_id TEXT NOT NULL, stage TEXT NOT NULL, kind TEXT NOT NULL,
                  payload TEXT NOT NULL, created_at TEXT DEFAULT CURRENT_TIMESTAMP
                );
                CREATE TABLE IF NOT EXISTS lessons (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  domain TEXT NOT NULL, lesson TEXT NOT NULL, score REAL NOT NULL,
                  evidence TEXT NOT NULL, created_at TEXT DEFAULT CURRENT_TIMESTAMP
                );
                CREATE TABLE IF NOT EXISTS checkpoints (
                  run_id TEXT PRIMARY KEY, status TEXT NOT NULL, payload TEXT NOT NULL,
                  artifact_hash TEXT, updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                );
                CREATE TABLE IF NOT EXISTS approvals (
                  id INTEGER PRIMARY KEY AUTOINCREMENT, run_id TEXT NOT NULL,
                  artifact_hash TEXT NOT NULL, approver TEXT NOT NULL,
                  created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                  UNIQUE(run_id, artifact_hash)
                );
                PRAGMA user_version=1;
                COMMIT;
                """
            )

    @property
    def schema_version(self) -> int:
        return int(self.db.execute("PRAGMA user_version").fetchone()[0])

    def record(self, run_id: str, stage: str, kind: str, payload: dict[str, Any]) -> None:
        self.db.execute(
            "INSERT INTO events(run_id, stage, kind, payload) VALUES (?, ?, ?, ?)",
            (run_id, stage, kind, json.dumps(payload, sort_keys=True)),
        )
        self.db.commit()

    def learn(self, domain: str, lesson: str, score: float, evidence: str) -> None:
        if not 0.0 <= score <= 1.0:
            raise ValueError("Lesson score must be between zero and one")
        self.db.execute(
            "INSERT INTO lessons(domain, lesson, score, evidence) VALUES (?, ?, ?, ?)",
            (domain, lesson, score, evidence),
        )
        self.db.commit()

    def recall(self, domain: str, limit: int = 5) -> list[dict[str, Any]]:
        if limit < 0 or limit > 100:
            raise ValueError("Recall limit must be between zero and 100")
        rows = self.db.execute(
            "SELECT lesson, score, evidence FROM lessons WHERE domain IN (?, 'meta') "
            "ORDER BY score DESC, id DESC LIMIT ?",
            (domain, limit),
        ).fetchall()
        return [dict(row) for row in rows]

    def events(self, run_id: str) -> list[dict[str, Any]]:
        rows = self.db.execute(
            "SELECT stage, kind, payload, created_at FROM events WHERE run_id=? ORDER BY id",
            (run_id,),
        ).fetchall()
        return [{**dict(row), "payload": json.loads(row["payload"])} for row in rows]

    def save_checkpoint(
        self,
        run_id: str,
        status: str,
        payload: dict[str, Any],
        artifact_hash: str | None = None,
    ) -> None:
        if status not in CHECKPOINT_STATUSES:
            raise ValueError(f"Invalid checkpoint status {status!r}")
        encoded = json.dumps(payload, sort_keys=True)
        self.db.execute(
            """INSERT INTO checkpoints(run_id, status, payload, artifact_hash)
               VALUES (?, ?, ?, ?)
               ON CONFLICT(run_id) DO UPDATE SET status=excluded.status,
                 payload=excluded.payload, artifact_hash=excluded.artifact_hash,
                 updated_at=CURRENT_TIMESTAMP""",
            (run_id, status, encoded, artifact_hash),
        )
        self.db.commit()

    def load_checkpoint(self, run_id: str) -> dict[str, Any] | None:
        row = self.db.execute(
            "SELECT status, payload, artifact_hash, updated_at FROM checkpoints WHERE run_id=?",
            (run_id,),
        ).fetchone()
        if row is None:
            return None
        try:
            payload = json.loads(row["payload"])
        except (json.JSONDecodeError, TypeError) as exc:
            raise RuntimeError(f"Checkpoint {run_id} contains invalid JSON") from exc
        if not isinstance(payload, dict):
            raise RuntimeError(f"Checkpoint {run_id} payload must be an object")
        return {
            "status": row["status"],
            "payload": payload,
            "artifact_hash": row["artifact_hash"],
            "updated_at": row["updated_at"],
        }

    def approve(self, run_id: str, artifact_hash: str, approver: str) -> None:
        if not approver.strip():
            raise ValueError("Approver identity cannot be empty")
        self.db.execute(
            "INSERT OR IGNORE INTO approvals(run_id, artifact_hash, approver) VALUES (?, ?, ?)",
            (run_id, artifact_hash, approver.strip()),
        )
        self.db.commit()

    def close(self) -> None:
        self.db.close()
