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
        choices=["jvm", "py", "rust", "ts", "wasm", "wat"],
        required=True,
        help="Target platform (jvm, py, rust, ts, wasm, wat)"
    )
    trans_cmd.add_argument("--output", "-o", help="Optional output file path")

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
