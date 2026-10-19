"""
Unit and Integration Tests for OmniAST Kernel, Transpilers, WASM, Grammars, Hermes Skills, and Multi-Account Broker
"""

import unittest
import os
import sys

# Ensure root is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.kernel.engine import OmniASTKernel
from transpilers.java_transpiler import JavaTranspiler
from transpilers.python_transpiler import PythonTranspiler
from transpilers.rust_transpiler import RustTranspiler
from transpilers.typescript_transpiler import TypeScriptTranspiler
from transpilers.wasm_transpiler import WasmTranspiler
from core.skills.hermes_openclaw import HermesSkillRegistry
from sre.models.multi_account_broker import MultiAccountBroker, ModelAccount

class TestOmniASTKernel(unittest.TestCase):
    def setUp(self):
        self.kernel = OmniASTKernel()
        self.kernel.register_transpiler("jvm", JavaTranspiler())
        self.kernel.register_transpiler("py", PythonTranspiler())
        self.kernel.register_transpiler("rust", RustTranspiler())
        self.kernel.register_transpiler("ts", TypeScriptTranspiler())

    def test_parse_simple_module(self):
        code = """
        module TestMod {
            version: "1.0.0"
            target: [jvm, py, rust, ts]

            machine Battery {
                capacity: 50000J
            }
        }
        """
        mod = self.kernel.parse_source(code)
        self.assertEqual(mod.name, "TestMod")
        self.assertEqual(len(mod.nodes), 1)
        self.assertEqual(mod.nodes[0].name, "Battery")
        self.assertEqual(mod.nodes[0].metadata.get("capacity"), "50000J")

    def test_transpile_jvm(self):
        code = """
        module SafetyGuard {
            listener AntiSpam on player.chat {
                guard message.is_spam()
            }
        }
        """
        mod = self.kernel.parse_source(code)
        java_code = self.kernel.transpile(mod, "jvm")
        self.assertIn("package org.omniast.generated.safetyguard;", java_code)
        self.assertIn("class SafetyGuardPlugin", java_code)
        self.assertIn("onAntiSpam", java_code)

    def test_transpile_python(self):
        code = """
        module Supervisor {
            sentinel Watcher {
                interval: 15m
            }
        }
        """
        mod = self.kernel.parse_source(code)
        py_code = self.kernel.transpile(mod, "py")
        self.assertIn("class SupervisorDaemon:", py_code)
        self.assertIn("run_watcher", py_code)
        self.assertIn("asyncio.sleep(15*60)", py_code)

    def test_transpile_rust(self):
        code = """
        module IndustrialGrid {
            machine FusionCore {
                capacity: 500000J
            }
        }
        """
        mod = self.kernel.parse_source(code)
        rust_code = self.kernel.transpile(mod, "rust")
        self.assertIn("pub struct IndustrialGridKernel", rust_code)
        self.assertIn("run_machine_fusioncore", rust_code)
        self.assertIn("omniast_industrialgrid_create", rust_code)

    def test_transpile_typescript(self):
        code = """
        module BotSecurity {
            listener FloodGuard on chat.message {
                guard event.isSpam
            }
        }
        """
        mod = self.kernel.parse_source(code)
        ts_code = self.kernel.transpile(mod, "ts")
        self.assertIn("export class BotSecurityModule extends EventEmitter", ts_code)
        self.assertIn("export class FloodGuardListener", ts_code)
        self.assertIn("dispatchHermesTool", ts_code)

    def test_transpile_wasm_wat(self):
        code = """
        module EdgeReactor {
            machine Core {
                capacity: 10000J
            }
        }
        """
        mod = self.kernel.parse_source(code)
        wasm_trans = WasmTranspiler()
        wat_code = wasm_trans.transpile_to_wat(mod.to_dict())
        self.assertIn("(module", wat_code)
        self.assertIn("Core_run", wat_code)
        self.assertIn("omni_init", wat_code)

    def test_transpile_wasm_binary(self):
        code = """
        module NativeWasmModule {
            machine NodeA {
                rate: 100J/s
            }
        }
        """
        mod = self.kernel.parse_source(code)
        wasm_trans = WasmTranspiler()
        wasm_bytes = wasm_trans.transpile_to_wasm_binary(mod.to_dict())
        self.assertTrue(wasm_bytes.startswith(b"\x00asm\x01\x00\x00\x00"))
        self.assertGreaterEqual(len(wasm_bytes), 32)

    def test_hermes_and_openclaw_skills(self):
        registry = HermesSkillRegistry()
        tools = registry.export_hermes_tools_json()
        self.assertGreaterEqual(len(tools), 5)
        tool_names = [t["function"]["name"] for t in tools]
        self.assertIn("omniast_query_graph", tool_names)
        self.assertIn("openclaw_dispatch_message", tool_names)
        self.assertIn("openclaw_exec_sandboxed", tool_names)

        manifest = registry.export_openclaw_skills_manifest()
        self.assertEqual(manifest["engine"], "openclaw-hermes-hybrid")

    def test_tree_sitter_and_editor_artifacts(self):
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        grammar_js = os.path.join(root, "tree-sitter-omniast", "grammar.js")
        highlights_scm = os.path.join(root, "tree-sitter-omniast", "queries", "highlights.scm")
        vscode_pkg = os.path.join(root, "editors", "vscode", "package.json")
        runtime_cargo = os.path.join(root, "runtime", "Cargo.toml")

        self.assertTrue(os.path.exists(grammar_js), "grammar.js exists")
        self.assertTrue(os.path.exists(highlights_scm), "highlights.scm exists")
        self.assertTrue(os.path.exists(vscode_pkg), "vscode package.json exists")
        self.assertTrue(os.path.exists(runtime_cargo), "runtime Cargo.toml exists")

    def test_multi_account_pools_and_failover(self):
        broker = MultiAccountBroker()
        
        # 1. Primary account acquisition
        acc1 = broker.acquire_account("codex")
        self.assertIsNotNone(acc1)
        self.assertEqual(acc1.id, "codex-1")

        # 2. Simulate 3 consecutive failures to trip circuit breaker on codex-1
        broker.report_result("codex-1", success=False, error="Rate limit 429 quota exhausted")
        broker.report_result("codex-1", success=False, error="Rate limit 429 quota exhausted")
        trip_res = broker.report_result("codex-1", success=False, error="Rate limit 429 quota exhausted")
        
        self.assertEqual(trip_res["status"], "circuit_tripped")
        self.assertEqual(acc1.status, "SLEEPING")

        # 3. Transparent failover to secondary backup (codex-2)
        acc2 = broker.acquire_account("codex")
        self.assertIsNotNone(acc2)
        self.assertEqual(acc2.id, "codex-2")
        self.assertEqual(acc2.status, "ONLINE")

        # 4. Same verified for antigravity pool
        anti1 = broker.acquire_account("antigravity")
        self.assertEqual(anti1.id, "antigravity-1")
        broker.report_result("antigravity-1", success=False)
        broker.report_result("antigravity-1", success=False)
        broker.report_result("antigravity-1", success=False)
        self.assertEqual(anti1.status, "SLEEPING")
        anti2 = broker.acquire_account("antigravity")
        self.assertEqual(anti2.id, "antigravity-2")

    def test_hermes_agent_and_universal_adapter(self):
        from integrations.hermes_agent.omniast_hermes_skill import HermesAgentOmniASTSkill, HERMES_AGENT_TOOLS
        from integrations.universal_agent_adapter import UniversalAgentAdapter

        # 1. Verify Hermes-Agent Skill
        skill = HermesAgentOmniASTSkill()
        code = """
        module HermesTestMod {
            sentinel Watcher {
                interval: 10m
            }
        }
        """
        parse_res = skill.parse_graph(code)
        self.assertEqual(parse_res["status"], "success")
        self.assertEqual(parse_res["module"], "HermesTestMod")

        trans_res = skill.transpile_code(code, "ts")
        self.assertEqual(trans_res["status"], "success")
        self.assertIn("HermesTestModModule", trans_res["code"])

        # 2. Verify ShareGPT Trajectory Recording for Nous Research Fine-tuning
        traj = skill.record_learning_trajectory("Create a sentinel that runs every 10m", code, reward=1.0)
        self.assertEqual(traj["status"], "recorded")
        self.assertEqual(len(skill.export_sharegpt_dataset()), 1)

        # 3. Verify Universal Agent Adapter
        adapter = UniversalAgentAdapter()
        fws = adapter.get_supported_frameworks()
        self.assertTrue(any("hermes" in f for f in fws))
        self.assertTrue(any("openclaw" in f for f in fws))
        self.assertTrue(any("saori" in f for f in fws))

        exec_res = adapter.execute_agent_tool("omni_parse", {"code": code})
        self.assertEqual(exec_res["status"], "ok")

if __name__ == "__main__":
    unittest.main()
