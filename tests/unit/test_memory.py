import sqlite3
import tempfile
import unittest
from pathlib import Path

from tetrative_os.memory import DATABASE_SCHEMA_VERSION, DatabaseVersionError, MemoryStore


class MemoryStoreTests(unittest.TestCase):
    def test_empty_database_migrates_to_current_version(self):
        with tempfile.TemporaryDirectory() as directory:
            store = MemoryStore(Path(directory) / "memory.db")
            try:
                self.assertEqual(store.schema_version, DATABASE_SCHEMA_VERSION)
                tables = {
                    row[0]
                    for row in store.db.execute(
                        "SELECT name FROM sqlite_master WHERE type='table'"
                    ).fetchall()
                }
                self.assertTrue({"events", "lessons", "checkpoints", "approvals"} <= tables)
            finally:
                store.close()

    def test_v1_database_migrates_to_v2_without_losing_events(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "v1.db"
            db = sqlite3.connect(path)
            db.executescript(
                """
                CREATE TABLE events (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  run_id TEXT NOT NULL, stage TEXT NOT NULL, kind TEXT NOT NULL,
                  payload TEXT NOT NULL, created_at TEXT DEFAULT CURRENT_TIMESTAMP
                );
                CREATE TABLE lessons (
                  id INTEGER PRIMARY KEY AUTOINCREMENT, domain TEXT NOT NULL,
                  lesson TEXT NOT NULL, score REAL NOT NULL, evidence TEXT NOT NULL,
                  created_at TEXT DEFAULT CURRENT_TIMESTAMP
                );
                CREATE TABLE checkpoints (
                  run_id TEXT PRIMARY KEY, status TEXT NOT NULL, payload TEXT NOT NULL,
                  artifact_hash TEXT, updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                );
                CREATE TABLE approvals (
                  id INTEGER PRIMARY KEY AUTOINCREMENT, run_id TEXT NOT NULL,
                  artifact_hash TEXT NOT NULL, approver TEXT NOT NULL,
                  created_at TEXT DEFAULT CURRENT_TIMESTAMP, UNIQUE(run_id, artifact_hash)
                );
                INSERT INTO events(run_id, stage, kind, payload)
                  VALUES ('legacy', 'stage', 'kept', '{"value": 1}');
                PRAGMA user_version=1;
                """
            )
            db.close()
            store = MemoryStore(path)
            try:
                self.assertEqual(store.schema_version, DATABASE_SCHEMA_VERSION)
                self.assertEqual(store.events("legacy")[0]["payload"], {"value": 1})
                tables = {
                    row[0]
                    for row in store.db.execute(
                        "SELECT name FROM sqlite_master WHERE type='table'"
                    ).fetchall()
                }
                self.assertIn("outcomes", tables)
                self.assertIn("action_ledger", tables)
            finally:
                store.close()

    def test_newer_database_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "future.db"
            db = sqlite3.connect(path)
            db.execute(f"PRAGMA user_version={DATABASE_SCHEMA_VERSION + 1}")
            db.close()
            with self.assertRaises(DatabaseVersionError):
                MemoryStore(path)

    def test_invalid_checkpoint_status_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            store = MemoryStore(Path(directory) / "memory.db")
            try:
                with self.assertRaises(ValueError):
                    store.save_checkpoint("run", "invented", {})
            finally:
                store.close()


if __name__ == "__main__":
    unittest.main()
