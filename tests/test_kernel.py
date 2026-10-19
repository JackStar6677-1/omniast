"""
Unit and Integration Tests for OmniAST Kernel and Transpilers
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

if __name__ == "__main__":
    unittest.main()
