#!/usr/bin/env python3
"""
OMEGA MEDIA OS v1.0 — MEMORY INTERFACE
Six institutional memory banks with vector + graph + episodic storage.
"""

import json
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Optional, Any, Tuple


class MemoryBank:
    """Memory bank specification — all 6 banks use this interface."""
    BANKS = [
        "WORLD", "STRATEGIC", "CREATIVE",
        "OPERATIONAL", "AUDIENCE", "FAILURE"
    ]

    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or ":memory:"
        # In production: connect to PostgreSQL + pgvector / Weaviate
        # For v1.0: SQLite for portability with JSON fields
        self._init_database()

    def _init_database(self):
        # Simplified schema for v1.0 — full vector/graph would use pgvector + adjacency tables
        conn = sqlite3.connect(str(self.db_path) if self.db_path != ":memory:" else "/tmp/omega_memory.db")
        conn.execute("""
        CREATE TABLE IF NOT EXISTS memory_entries (
            entry_id TEXT PRIMARY KEY,
            bank_id TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            agent_id TEXT,
            task_id TEXT,
            content TEXT,
            vector_embedding TEXT,
            graph_edges TEXT,
            confidence REAL DEFAULT 0.0,
            access_level TEXT DEFAULT 'internal',
            deletion_policy TEXT DEFAULT 'permanent',
            tags TEXT
        )
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_bank ON memory_entries(bank_id)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON memory_entries(timestamp)")
        conn.commit()
        conn.close()

    def write_memory(
        self,
        bank_id: str,
        content: Any,
        agent_id: Optional[str] = None,
        task_id: Optional[str] = None,
        confidence: float = 0.8,
        tags: Optional[List[str]] = None,
        deletion_policy: str = "permanent",
        graph_edges: Optional[List[Dict]] = None,
    ) -> Dict:
        if bank_id not in self.BANKS:
            raise ValueError(f"Invalid bank: {bank_id}. Must be one of {self.BANKS}")

        entry_id = str(uuid.uuid4())
        timestamp = datetime.now(timezone.utc).isoformat()
        content_str = json.dumps(content) if isinstance(content, (dict, list)) else str(content)
        edges_str = json.dumps(graph_edges or [])
        tags_str = json.dumps(tags or [])

        conn = sqlite3.connect(str(self.db_path) if self.db_path != ":memory:" else "/tmp/omega_memory.db")
        conn.execute(
            "INSERT INTO memory_entries (entry_id, bank_id, timestamp, agent_id, task_id, content, graph_edges, confidence, access_level, deletion_policy, tags) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (entry_id, bank_id, timestamp, agent_id, task_id, content_str, edges_str, confidence, "internal", deletion_policy, tags_str)
        )
        conn.commit()
        conn.close()

        return {
            "entry_id": entry_id,
            "bank_id": bank_id,
            "status": "WRITTEN",
            "deletion_policy": deletion_policy,
            "timestamp": timestamp,
            "rollback_ref": f"rollback-{entry_id}",
        }

    def read_memory(
        self,
        bank_id: str,
        query: Optional[str] = None,
        max_results: int = 5,
        min_confidence: float = 0.7,
        mode: str = "vector",  # simplified: for v1.0, basic text search
    ) -> List[Dict]:
        conn = sqlite3.connect(str(self.db_path) if self.db_path != ":memory:" else "/tmp/omega_memory.db")
        if query:
            cursor = conn.execute(
                "SELECT entry_id, bank_id, timestamp, agent_id, task_id, content, confidence FROM memory_entries WHERE bank_id = ? AND content LIKE ? ORDER BY timestamp DESC LIMIT ?",
                (bank_id, f"%{query}%", max_results)
            )
        else:
            cursor = conn.execute(
                "SELECT entry_id, bank_id, timestamp, agent_id, task_id, content, confidence FROM memory_entries WHERE bank_id = ? AND confidence >= ? ORDER BY timestamp DESC LIMIT ?",
                (bank_id, min_confidence, max_results)
            )
        results = []
        for row in cursor.fetchall():
            results.append({
                "entry_id": row[0],
                "bank_id": row[1],
                "timestamp": row[2],
                "agent_id": row[3],
                "task_id": row[4],
                "content": json.loads(row[5]) if row[5].startswith("{") or row[5].startswith("[") else row[5],
                "confidence": row[6],
            })
        conn.close()
        return results

    def get_failure_memory(self, task_id: Optional[str] = None) -> List[Dict]:
        results = self.read_memory("FAILURE", query=f"%{task_id or ''}%", max_results=10)
        return results

    def write_failure_memory(
        self,
        failure_description: str,
        cause: str,
        fix_action: str,
        test_result: str,
        new_guardrail: str,
        agent_id: Optional[str] = None,
        task_id: Optional[str] = None,
    ) -> Dict:
        content = {
            "failure": failure_description,
            "cause": cause,
            "fix": fix_action,
            "test": test_result,
            "new_guardrail": new_guardrail,
            "protocol_followed": True,
        }
        result = self.write_memory(
            bank_id="FAILURE",
            content=content,
            agent_id=agent_id,
            task_id=task_id,
            confidence=1.0,
            tags=["failure_infrastructure", "non_deletable"],
            deletion_policy="permanent",
        )
        return result


if __name__ == "__main__":
    # Demonstration / test harness
    mem = MemoryBank()
    # Initialize failure reference for orchestrator packets
    failure_ref = mem.write_failure_memory(
        failure_description="Initial system activation — no prior failures recorded.",
        cause="First activation — establishing baseline.",
        fix_action="Created memory architecture with permanent failure bank.",
        test_result="Memory read/write verified.",
        new_guardrail="Every packet must include FAILURE memory reference; pollution must not exceed 0.3.",
        agent_id="OMEGA-0",
        task_id="init",
    )
    print(f"Failure memory written: {failure_ref['entry_id']}")

    world_ref = mem.write_memory(
        bank_id="WORLD",
        content={"signal": "OMEGA v1.0 activation", "entity": "Agentic UGC System"},
        agent_id="OMEGA-0",
        task_id="init",
    )
    print(f"World memory written: {world_ref['entry_id']}")

    results = mem.read_memory("FAILURE", max_results=5)
    print(f"Read {len(results)} failure entries.")
    for r in results:
        print(f"  - {r['entry_id']}: {r['content']}")
