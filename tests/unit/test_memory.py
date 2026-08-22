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
