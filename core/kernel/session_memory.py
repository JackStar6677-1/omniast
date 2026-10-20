"""
OmniAST Persistent Session Memory
(c) 2026 JackStar6677-1 & OmniAST Contributors.
Inspired by claude-mem (thedotmack/claude-mem).

Maintains cross-session architectural continuity, recording AST mutations,
active files, user preferences, and transpilation decisions in local SQLite.
Allows AI models (Claude, Codex, Antigravity) to instantly resume tasks without
re-explaining project topology.
"""

import sqlite3
import os
import json
import time
from typing import Dict, Any, List, Optional

class SessionMemoryStore:
    """
    Lightweight, embedded cross-session memory ledger.
    """
    def __init__(self, db_path: Optional[str] = None):
        if not db_path:
            # Default to local cache in workspace or user home
            cache_dir = os.path.expanduser("~/.cache/omniast")
            os.makedirs(cache_dir, exist_ok=True)
            db_path = os.path.join(cache_dir, "session_memory.db")
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS session_decisions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    timestamp REAL NOT NULL,
                    category TEXT NOT NULL, -- 'ast_edit', 'architecture', 'user_preference', 'fix'
                    summary TEXT NOT NULL,
                    context_json TEXT
                )
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_session_time 
                ON session_decisions(session_id, timestamp)
            """)
            conn.commit()

    def record_decision(self, session_id: str, category: str, summary: str, context: Optional[Dict[str, Any]] = None):
        """Records an architectural or coding decision."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO session_decisions (session_id, timestamp, category, summary, context_json)
                VALUES (?, ?, ?, ?, ?)
            """, (session_id, time.time(), category, summary, json.dumps(context or {})))
            conn.commit()

    def get_recent_decisions(self, limit: int = 15, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retrieves recent decisions across sessions."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            query = "SELECT * FROM session_decisions"
            params = []
            if category:
                query += " WHERE category = ?"
                params.append(category)
            query += " ORDER BY timestamp DESC LIMIT ?"
            params.append(limit)

            cursor = conn.execute(query, params)
            rows = cursor.fetchall()

            return [
                {
                    "id": r["id"],
                    "session_id": r["session_id"],
                    "timestamp": r["timestamp"],
                    "category": r["category"],
                    "summary": r["summary"],
                    "context": json.loads(r["context_json"])
                }
                for r in rows
            ]

    def format_memory_digest_for_llm(self, limit: int = 10) -> str:
        """Formats session history into a dense, token-efficient prompt snippet."""
        decisions = self.get_recent_decisions(limit=limit)
        if not decisions:
            return ""

        lines = ["## 🧠 OmniAST Cross-Session Memory (claude-mem compatible)"]
        for d in reversed(decisions):
            date_str = time.strftime('%Y-%m-%d %H:%M', time.localtime(d['timestamp']))
            lines.append(f"- **[{date_str}] ({d['category']})**: {d['summary']}")
        return "\n".join(lines)
