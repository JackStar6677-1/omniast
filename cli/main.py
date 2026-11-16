"""
OmniAST / GraphLang Command Line Interface (CLI)
Allows parsing, transpiling, inspecting OmniAST modules, managing multi-account AI pools,
compressing context, accessing cross-session memory, and exporting native integrations.
"""

import sys
import argparse
import json
import os

# Ensure repository root is on sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.kernel.engine import OmniASTKernel
from core.kernel.compression import ContextCompressor
from core.kernel.session_memory import SessionMemoryStore
from transpilers.java_transpiler import JavaTranspiler
from transpilers.python_transpiler import PythonTranspiler
from transpilers.rust_transpiler import RustTranspiler
from transpilers.typescript_transpiler import TypeScriptTranspiler
from transpilers.wasm_transpiler import WasmTranspiler
from transpilers.web_transpiler import WebTranspiler
from core.skills.hermes_openclaw import HermesSkillRegistry
from sre.models.multi_account_broker import MultiAccountBroker
from integrations.universal_agent_adapter import UniversalAgentAdapter

def build_kernel() -> OmniASTKernel:
    k = OmniASTKernel()
    k.register_transpiler("jvm", JavaTranspiler())
    k.register_transpiler("py", PythonTranspiler())
    k.register_transpiler("rust", RustTranspiler())
    k.register_transpiler("ts", TypeScriptTranspiler())
    wasm_t = WasmTranspiler()
    k.register_transpiler("wat", wasm_t)
    k.register_transpiler("wasm", wasm_t)
    web_t = WebTranspiler()
    k.register_transpiler("web", web_t)
    k.register_transpiler("spa", web_t)
    k.register_transpiler("gh-pages", web_t)
    return k

def main():
    parser = argparse.ArgumentParser(
        prog="omniast",
        description="OmniAST / GraphLang — The Universal Graph-Native Kernel for Autonomous AI Systems & Engine Interop"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # Command: parse
    parse_cmd = subparsers.add_parser("parse", help="Parse an .omni source file into normalized AST JSON")
    parse_cmd.add_argument("--input", "-i", required=True, help="Path to .omni source file")
    parse_cmd.add_argument("--output", "-o", help="Optional output path for JSON")
    parse_cmd.add_argument("--compress", "-c", action="store_true", help="Compress AST tokens (Headroom mode)")

    # Command: transpile
    trans_cmd = subparsers.add_parser("transpile", help="Transpile an .omni source file to target runtime")
    trans_cmd.add_argument("--input", "-i", required=True, help="Path to .omni source file")
    trans_cmd.add_argument(
        "--target", "-t",
        choices=["jvm", "py", "rust", "ts", "wasm", "wat", "web", "spa", "gh-pages"],
        required=True,
        help="Target platform (jvm, py, rust, ts, wasm, wat, web, spa, gh-pages)"
    )
    trans_cmd.add_argument("--output", "-o", help="Optional output file path")

    # Command: web (OmniWeb & GitHub Pages)
    web_cmd = subparsers.add_parser("web", help="OmniWeb engine: build or preview reactive SPA for GitHub Pages")
    web_sub = web_cmd.add_subparsers(dest="web_action", help="Web actions")
    
    web_build = web_sub.add_parser("build", help="Compile .omni module to static reactive bundle (HTML/JS/CSS)")
    web_build.add_argument("--input", "-i", required=True, help="Path to .omni file")
    web_build.add_argument("--output", "-o", default="dist/index.html", help="Destination path (default: dist/index.html)")
    web_build.add_argument("--theme", choices=["sovereign", "cyberpunk", "terminal", "minimal"], default="sovereign", help="Theme (default: sovereign)")
    
    web_serve = web_sub.add_parser("serve", help="Preview compiled reactive web app on local HTTP server")
    web_serve.add_argument("--input", "-i", required=True, help="Path to .omni file")
    web_serve.add_argument("--port", "-p", type=int, default=8080, help="Port to serve on (default: 8080)")
    web_serve.add_argument("--theme", choices=["sovereign", "cyberpunk", "terminal", "minimal"], default="sovereign", help="Theme (default: sovereign)")

    web_css = web_sub.add_parser("css", help="Export standalone Sovereign CSS design system (omni-ui.css)")
    web_css.add_argument("--output", "-o", default="dist/omni-ui.css", help="Destination path (default: dist/omni-ui.css)")

    # Command: fullstack (Rust Axum + Reactive Web SPA)
    fs_cmd = subparsers.add_parser("fullstack", help="Full-stack engine: generate Rust Axum backend + Reactive Web frontend")
    fs_sub = fs_cmd.add_subparsers(dest="fullstack_action", help="Fullstack actions")
    fs_gen = fs_sub.add_parser("generate", help="Generate full-stack application (Axum REST API + Reactive Web SPA)")
    fs_gen.add_argument("--input", "-i", required=True, help="Path to .omni file")
    fs_gen.add_argument("--output", "-o", default="out_fullstack", help="Destination directory (default: out_fullstack)")
    fs_gen.add_argument("--theme", choices=["sovereign", "cyberpunk", "terminal", "minimal"], default="sovereign", help="Theme for frontend SPA")

    # Command: compress (Headroom integration)
    comp_cmd = subparsers.add_parser("compress", help="Compress JSON payloads or logs by 60-90%% (Headroom mode)")
    comp_cmd.add_argument("--file", "-f", required=True, help="Path to file (JSON or logs)")
    comp_cmd.add_argument("--type", choices=["ast", "logs"], default="ast", help="Type of content")

    # Command: memory (claude-mem integration)
    mem_cmd = subparsers.add_parser("memory", help="Inspect or record cross-session decisions (claude-mem compatible)")
    mem_cmd.add_argument("--digest", "-d", action="store_true", help="Print condensed memory digest for LLM")
    mem_cmd.add_argument("--record", "-r", help="Record a new architectural decision or lesson")
    mem_cmd.add_argument("--category", "-c", default="architecture", help="Category for decision")

    # Command: skills
    skill_cmd = subparsers.add_parser("skills", help="Export Hermes & OpenClaw skill schemas for AI agent tool calling")
    skill_cmd.add_argument("--format", "-f", choices=["hermes", "openclaw"], default="hermes", help="Output format")

    # Command: accounts (Multi-account broker)
    acc_cmd = subparsers.add_parser("accounts", help="Manage and inspect multi-account AI pools (Antigravity, Codex, Claude, etc.)")
    acc_cmd.add_argument("--provider", "-p", help="Filter by provider (antigravity, codex, claude, deepseek, grok)")
    acc_cmd.add_argument("--json", action="store_true", help="Output raw telemetry JSON")

    # Command: export-agent (Universal Agent Integration)
    exp_cmd = subparsers.add_parser("export-agent", help="Export native configuration for NousResearch/hermes-agent, OpenClaw, SAORI, or MCP")
    exp_cmd.add_argument(
        "--framework", "-f",
        choices=["hermes", "openclaw", "saori", "mcp"],
        required=True,
        help="Target agentic framework"
    )

    # Command: prompt
    subparsers.add_parser("prompt", help="Display the Universal Token-Saver prompt for AI models")

    args = parser.parse_args()
    kernel = build_kernel()

    if args.command == "parse":
        if not os.path.exists(args.input):
            print(f"[ERROR] Input file '{args.input}' does not exist.", file=sys.stderr)
            sys.exit(1)
        with open(args.input, "r", encoding="utf-8") as f:
            code = f.read()
        module = kernel.parse_source(code)
        if args.compress:
            compressed = ContextCompressor.compress_ast_json(module.to_dict())
            out_str = json.dumps(compressed, indent=2)
        else:
            out_str = module.export_graph_json()

        if args.output:
            with open(args.output, "w", encoding="utf-8") as out:
                out.write(out_str)
            print(f"[OK] AST Graph saved to {args.output}")
        else:
            print(out_str)

    elif args.command == "transpile":
        if not os.path.exists(args.input):
            print(f"[ERROR] Input file '{args.input}' does not exist.", file=sys.stderr)
            sys.exit(1)
        with open(args.input, "r", encoding="utf-8") as f:
            code = f.read()
        module = kernel.parse_source(code)
        emitted = kernel.transpile(module, args.target)
        if args.output:
            with open(args.output, "w", encoding="utf-8") as out:
                out.write(emitted)
            print(f"[OK] Transpiled ({args.target}) code saved to {args.output}")
        else:
            print(emitted)

    elif args.command == "web":
        if not hasattr(args, "web_action") or not args.web_action:
            print("[ERROR] Please specify 'omniast web build', 'omniast web serve', or 'omniast web css'.", file=sys.stderr)
            sys.exit(1)

        if args.web_action == "css":
            from transpilers.omni_css import get_omni_ui_css
            css_content = get_omni_ui_css()
            out_path = args.output
            os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
            with open(out_path, "w", encoding="utf-8") as out:
                out.write(css_content)
            print(f"[OK] Sovereign CSS framework exported successfully: {out_path}")
            return

        if not os.path.exists(args.input):
            print(f"[ERROR] Input file '{args.input}' does not exist.", file=sys.stderr)
            sys.exit(1)

        with open(args.input, "r", encoding="utf-8") as f:
            code = f.read()
        module = kernel.parse_source(code)
        theme = getattr(args, "theme", "sovereign")
        bundle_html = kernel.transpile(module, "web", theme=theme)

        if args.web_action == "build":
            out_path = args.output
            os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
            with open(out_path, "w", encoding="utf-8") as out:
                out.write(bundle_html)
            print(f"[OK] OmniWeb static reactive application compiled successfully:")
            print(f"     -> {out_path} (Theme: {theme} · Ready for GitHub Pages deployment)")

        elif args.web_action == "serve":
            import http.server
            import socketserver
            import tempfile

            with tempfile.TemporaryDirectory() as tmpdir:
                index_path = os.path.join(tmpdir, "index.html")
                with open(index_path, "w", encoding="utf-8") as out:
                    out.write(bundle_html)

                class OmniHandler(http.server.SimpleHTTPRequestHandler):
                    def __init__(self, *a, **kw):
                        super().__init__(*a, directory=tmpdir, **kw)
                    def log_message(self, format, *args):
                        pass

                port = args.port
                print(f"[OMNIWEB DEV SERVER] Serving live app on http://localhost:{port} (Theme: {theme})")
                print(f"[OMNIWEB DEV SERVER] Press Ctrl+C to stop.")
                with socketserver.TCPServer(("", port), OmniHandler) as httpd:
                    try:
                        httpd.serve_forever()
                    except KeyboardInterrupt:
                        print("\n[OMNIWEB DEV SERVER] Server stopped.")

    elif args.command == "fullstack":
        if not hasattr(args, "fullstack_action") or not args.fullstack_action:
            print("[ERROR] Please specify 'omniast fullstack generate'.", file=sys.stderr)
            sys.exit(1)

        if not os.path.exists(args.input):
            print(f"[ERROR] Input file '{args.input}' does not exist.", file=sys.stderr)
            sys.exit(1)

        with open(args.input, "r", encoding="utf-8") as f:
            code = f.read()
        module = kernel.parse_source(code)

        out_dir = os.path.abspath(args.output)
        backend_dir = os.path.join(out_dir, "backend", "src")
        frontend_dir = os.path.join(out_dir, "frontend")
        os.makedirs(backend_dir, exist_ok=True)
        os.makedirs(frontend_dir, exist_ok=True)

        # Generate Rust Axum backend
        rust_code = kernel.transpile(module, "rust")
        rust_main_path = os.path.join(backend_dir, "main.rs")
        with open(rust_main_path, "w", encoding="utf-8") as f:
            f.write(rust_code)

        cargo_path = os.path.join(out_dir, "backend", "Cargo.toml")
        clean_mod_name = module.name.lower().replace("-", "_")
        cargo_toml = f"""[package]
name = "{clean_mod_name}_backend"
version = "{module.version}"
edition = "2021"

[dependencies]
tokio = {{ version = "1.0", features = ["full"] }}
axum = "0.7"
serde = {{ version = "1.0", features = ["derive"] }}
serde_json = "1.0"
tracing = "0.1"
tracing-subscriber = "0.3"
"""
        with open(cargo_path, "w", encoding="utf-8") as f:
            f.write(cargo_toml)

        # Generate Reactive Web frontend
        theme = getattr(args, "theme", "sovereign")
        web_html = kernel.transpile(module, "web", theme=theme)
        index_path = os.path.join(frontend_dir, "index.html")
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(web_html)

        # Generate Root README
        readme_path = os.path.join(out_dir, "README.md")
        readme_content = f"""# {module.name} — Full-Stack Sovereign Application
Generated by **OmniAST v0.2.0** (The Universal Graph-Native Kernel).

## 🏛️ Architecture Overview
- **Backend:** High-performance asynchronous Rust server using [Axum](https://github.com/tokio-rs/axum) and Tokio.
- **Frontend:** Zero-dependency, client-side reactive SPA with Micro-Signals (<2KB) ready for **GitHub Pages**.
- **Theme:** `{theme}` (with dynamic in-browser theme switcher enabled).

## 🚀 Quickstart

### 1. Run the Backend API
```bash
cd backend
cargo run
```
Server listens on `http://0.0.0.0:8080`.

### 2. Run / Deploy the Frontend
- **Local preview:** Open `frontend/index.html` directly in any web browser or serve with `omniast web serve -i <spec.omni>`.
- **Deploy to GitHub Pages:** Push the contents of `frontend/` to your `gh-pages` branch or configure your repository to deploy from `/docs`.
"""
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(readme_content)

        print(f"[OK] Full-stack application '{module.name}' generated successfully at: {out_dir}")
        print(f"     ├── backend/src/main.rs  (Axum REST API & models)")
        print(f"     ├── backend/Cargo.toml   (Tokio / Axum / Serde toolchain)")
        print(f"     ├── frontend/index.html  (Micro-Signals SPA · GitHub Pages ready · Theme: {theme})")
        print(f"     └── README.md            (Full-stack quickstart guide)")

    elif args.command == "compress":
        if not os.path.exists(args.file):
            print(f"[ERROR] File '{args.file}' not found.", file=sys.stderr)
            sys.exit(1)
        with open(args.file, "r", encoding="utf-8") as f:
            raw = f.read()
        if args.type == "ast":
            try:
                data = json.loads(raw)
                res = ContextCompressor.compress_ast_json(data)
                res_str = json.dumps(res, indent=2)
                savings = ContextCompressor.estimate_token_savings(raw, res_str)
                print(f"[COMPRESSED AST] Saved: {savings['reduction_percent']}% tokens ({savings['saved_tokens']} tokens)")
                print(res_str)
            except Exception as e:
                print(f"[ERROR] Invalid JSON: {e}", file=sys.stderr)
        else:
            res_str = ContextCompressor.compress_logs(raw)
            savings = ContextCompressor.estimate_token_savings(raw, res_str)
            print(f"[COMPRESSED LOGS] Saved: {savings['reduction_percent']}% tokens ({savings['saved_tokens']} tokens)")
            print(res_str)

    elif args.command == "memory":
        mem = SessionMemoryStore()
        if args.record:
            mem.record_decision("cli_user", args.category, args.record)
            print(f"[OK] Recorded memory decision: {args.record}")
        elif args.digest:
            print(mem.format_memory_digest_for_llm())
        else:
            decisions = mem.get_recent_decisions(limit=10)
            print(json.dumps(decisions, indent=2))

    elif args.command == "skills":
        HermesSkillRegistry.export_cli(args.format)

    elif args.command == "accounts":
        broker = MultiAccountBroker()
        if args.json:
            print(json.dumps(broker.export_telemetry(), indent=2))
        else:
            broker.print_dashboard(provider_filter=args.provider)

    elif args.command == "export-agent":
        adapter = UniversalAgentAdapter()
        config = adapter.export(args.framework)
        print(json.dumps(config, indent=2))

    elif args.command == "prompt":
        prompt_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "prompts", "universal_agent_prompt.md")
        if os.path.exists(prompt_path):
            with open(prompt_path, "r", encoding="utf-8") as f:
                print(f.read())
        else:
            print("[ERROR] Prompt file not found.", file=sys.stderr)
            sys.exit(1)

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
