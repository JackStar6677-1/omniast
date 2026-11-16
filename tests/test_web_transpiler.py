"""
Unit Tests for OmniAST Web & GitHub Pages Transpiler (OmniWeb)
"""

import unittest
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.kernel.engine import OmniASTKernel
from transpilers.web_transpiler import WebTranspiler
from transpilers.rust_transpiler import RustTranspiler

class TestWebTranspiler(unittest.TestCase):
    def setUp(self):
        self.kernel = OmniASTKernel()
        self.kernel.register_transpiler("web", WebTranspiler())
        self.kernel.register_transpiler("rust", RustTranspiler())

    def test_parse_web_module(self):
        code = """
        module WebApp {
            version: "1.0.0"
            target: [web, rust]

            page Dashboard path="/dashboard" {
                title: "Live SRE Dashboard"
                signal status = "online"
            }

            model UserSession {
                id: uuid
                token: string
            }

            endpoint GET "/api/v1/status" {
                guard session.is_valid()
            }
        }
        """
        mod = self.kernel.parse_source(code)
        self.assertEqual(mod.name, "WebApp")
        self.assertEqual(len(mod.nodes), 3)

        page_node = next(n for n in mod.nodes if n.type == "page")
        self.assertEqual(page_node.name, "Dashboard")
        self.assertEqual(page_node.metadata.get("path"), "/dashboard")
        self.assertEqual(page_node.metadata.get("title"), "Live SRE Dashboard")

        signals = [c for c in page_node.children if c.type == "signal"]
        self.assertEqual(len(signals), 1)
        self.assertEqual(signals[0].name, "status")

        endpoint_node = next(n for n in mod.nodes if n.type == "endpoint")
        self.assertEqual(endpoint_node.metadata.get("method"), "GET")
        self.assertEqual(endpoint_node.metadata.get("path"), "/api/v1/status")

    def test_transpile_web_spa(self):
        code = """
        module TestPortal {
            target: [web]

            page Home path="/" {
                title: "Test Portal"
            }

            model Metric {
                name: string
                value: float
            }
        }
        """
        mod = self.kernel.parse_source(code)
        html = self.kernel.transpile(mod, "web")
        self.assertIn("<!DOCTYPE html>", html)
        self.assertIn("Test Portal", html)
        self.assertIn("OmniWeb · GitHub Pages Ready", html)
        self.assertIn("MODULE_DATA", html)
        self.assertIn("Micro-Signals Reactive Engine", html)

    def test_transpile_rust_endpoints(self):
        code = """
        module ApiService {
            endpoint GET "/api/health" {
            }
            model Item {
            }
        }
        """
        mod = self.kernel.parse_source(code)
        rust = self.kernel.transpile(mod, "rust")
        self.assertIn("handle_endpoint_get_api_health", rust)
        self.assertIn("get_model_item_schema", rust)
        self.assertIn("build_router", rust)
        self.assertIn("pub struct Item", rust)

    def test_themes_transpilation(self):
        code = """
        module ThemeApp {
            page Home path="/" {
                title: "Theme Test"
            }
        }
        """
        mod = self.kernel.parse_source(code)
        themes = ["sovereign", "cyberpunk", "terminal", "minimal"]
        for th in themes:
            html = self.kernel.transpile(mod, "web", theme=th)
            self.assertIn(f'data-theme="{th}"', html)
            self.assertIn(f'id="foot-theme">{th.upper()}<', html)
            self.assertIn("THEMES_DATA", html)

    def test_theme_invalid_fallback(self):
        code = """
        module FallbackApp {
            page Home path="/" {
                title: "Fallback Test"
            }
        }
        """
        mod = self.kernel.parse_source(code)
        html = self.kernel.transpile(mod, "web", theme="non_existent_theme_xyz")
        self.assertIn('data-theme="sovereign"', html)
        self.assertIn('id="foot-theme">SOVEREIGN<', html)

    def test_omni_ui_css_export(self):
        from transpilers.omni_css import get_omni_ui_css
        css = get_omni_ui_css()
        self.assertIn("#scroll-progress", css)
        self.assertIn(".rgb-card", css)
        self.assertIn(".skeleton", css)
        self.assertIn(".loader-quantum", css)
        self.assertIn("grow-scroll-progress", css)

    def test_mega_ui_elements_in_spa(self):
        code = """
        module MegaUIApp {
            page Main path="/" {
                title: "Mega UI Test"
            }
        }
        """
        mod = self.kernel.parse_source(code)
        html = self.kernel.transpile(mod, "web")
        self.assertIn('id="scroll-progress"', html)
        self.assertIn('class="hero-container', html)
        self.assertIn('id="pixelCanvas"', html)
        self.assertIn('Quantum Reactor Core', html)
        self.assertIn('rgb-card', html)

if __name__ == "__main__":
    unittest.main()
