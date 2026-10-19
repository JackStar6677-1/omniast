"""
Unit and Integration Tests for OmniAST Kernel, Transpilers, WASM, and Grammars
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
from transpilers.wasm_transpiler import WasmTranspiler

class TestOmniASTKernel(unittest.TestCase):
    def setUp(self):
        self.kernel = OmniASTKernel()
        self.kernel.register_transpiler("jvm", JavaTranspiler())
        self.kernel.register_transpiler("py", PythonTranspiler())
        self.kernel.register_transpiler("rust", RustTranspiler())

    def test_parse_simple_module(self):
        code = """
        module TestMod {
            version: "1.0.0"
            target: [jvm, py, rust]

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

if __name__ == "__main__":
    unittest.main()
