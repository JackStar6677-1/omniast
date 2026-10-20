import unittest
import json
import os
import shutil

from core.kernel.compression import ContextCompressor
from core.kernel.session_memory import SessionMemoryStore
from core.skills.meta_observer import MetaSkillObserver

class TestOmniASTInnovations(unittest.TestCase):

    def test_context_compression_ast(self):
        sample_ast = {
            "name": "TestModule",
            "version": "1.0.0",
            "targets": ["jvm", "rust"],
            "children": [
                {
                    "type": "listener",
                    "name": "OnJoin",
                    "metadata": {"priority": "high"},
                    "children": []
                }
            ]
        }
        compressed = ContextCompressor.compress_ast_json(sample_ast)
        self.assertIn("n", compressed)
        self.assertIn("ch", compressed)
        self.assertEqual(compressed["n"], "TestModule")
        # Children metadata should be preserved
        self.assertEqual(compressed["ch"][0]["t"], "listener")

    def test_context_compression_logs(self):
        raw_logs = """
2026-10-20T08:00:01Z [pid 1234] [INFO] Starting engine...
2026-10-20T08:00:02Z [pid 1234] [WARN] Connection retry in 5s
2026-10-20T08:00:03Z [pid 1234] [WARN] Connection retry in 5s
2026-10-20T08:00:04Z [pid 1234] [ERROR] Failed to bind port 8080
"""
        compressed = ContextCompressor.compress_logs(raw_logs)
        self.assertIn("Failed to bind port 8080", compressed)
        self.assertIn("Connection retry in 5s", compressed)
        # Should deduplicate repeated WARN
        lines = [l for l in compressed.splitlines() if "Connection retry" in l]
        self.assertEqual(len(lines), 1)

    def test_session_memory_store(self):
        test_db = "/tmp/test_omniast_mem.db"
        if os.path.exists(test_db):
            os.remove(test_db)

        store = SessionMemoryStore(db_path=test_db)
        store.record_decision("session_abc", "architecture", "Use Panama FFI for Rust backend")
        store.record_decision("session_abc", "fix", "Resolve null pointer in AST parser")

        decisions = store.get_recent_decisions(limit=5)
        self.assertEqual(len(decisions), 2)
        self.assertEqual(decisions[0]["summary"], "Resolve null pointer in AST parser")

        digest = store.format_memory_digest_for_llm(limit=2)
        self.assertIn("Panama FFI", digest)
        self.assertIn("null pointer", digest)

    def test_meta_skill_observer(self):
        observer = MetaSkillObserver(skills_dir="/tmp")
        obs = observer.observe_friction_event("omniast transpile", "Error: Unknown target xyz")
        self.assertIn("valid targets", obs["proposed_remedy"])

        manifest = observer.generate_skill_manifest(
            skill_name="custom-transpile",
            description="Automates custom transpilations",
            steps=["Run omniast parse", "Apply optimizations", "Transpile"]
        )
        self.assertIn("name: custom-transpile", manifest)
        self.assertIn("Step 1", manifest)

if __name__ == "__main__":
    unittest.main()
