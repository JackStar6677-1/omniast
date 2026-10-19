"""
OmniAST / GraphLang Command Line Interface (CLI)
Allows parsing, transpiling, and inspecting OmniAST modules directly from the terminal.
Supports JVM (Java 21+), Native Rust/Tokio, Python Asyncio, TypeScript/Node.js, and WebAssembly (WASM/WAT).
Integrates Hermes Function Calling schemas and OpenClaw Skills.
"""

import sys
import argparse
import json
import os

from core.kernel.engine import OmniASTKernel
from transpilers.java_transpiler import JavaTranspiler
from transpilers.python_transpiler import PythonTranspiler
from transpilers.rust_transpiler import RustTranspiler
from transpilers.typescript_transpiler import TypeScriptTranspiler
from transpilers.wasm_transpiler import WasmTranspiler
from core.skills.hermes_openclaw import HermesSkillRegistry

def build_kernel() -> OmniASTKernel:
    k = OmniASTKernel()
    k.register_transpiler("jvm", JavaTranspiler())
    k.register_transpiler("py", PythonTranspiler())
    k.register_transpiler("rust", RustTranspiler())
    k.register_transpiler("ts", TypeScriptTranspiler())
    k.register_transpiler("wat", WasmTranspiler())
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

    # Command: skills
    skill_cmd = subparsers.add_parser("skills", help="Export Hermes & OpenClaw skill schemas for AI agent tool calling")
    skill_cmd.add_argument("--format", "-f", choices=["hermes", "openclaw"], default="hermes", help="Output format")

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
        graph_json = module.export_graph_json()
        if args.output:
            with open(args.output, "w", encoding="utf-8") as out:
                out.write(graph_json)
            print(f"[OK] AST Graph saved to {args.output}")
        else:
            print(graph_json)

    elif args.command == "transpile":
        if not os.path.exists(args.input):
            print(f"[ERROR] Input file '{args.input}' does not exist.", file=sys.stderr)
            sys.exit(1)
        with open(args.input, "r", encoding="utf-8") as f:
            code = f.read()
        module = kernel.parse_source(code)

        if args.target == "wasm":
            wasm_trans = WasmTranspiler()
            binary_wasm = wasm_trans.transpile_to_wasm_binary(module.to_dict())
            out_path = args.output or "out.wasm"
            if os.path.dirname(out_path):
                os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
            with open(out_path, "wb") as out:
                out.write(binary_wasm)
            print(f"[OK] Compiled standalone WebAssembly binary ({len(binary_wasm)} bytes) saved to {out_path}")
        elif args.target == "wat":
            wasm_trans = WasmTranspiler()
            result = wasm_trans.transpile_to_wat(module.to_dict())
            if args.output:
                os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
                with open(args.output, "w", encoding="utf-8") as out:
                    out.write(result)
                print(f"[OK] Transpiled WebAssembly Text (WAT) saved to {args.output}")
            else:
                print(result)
        else:
            result = kernel.transpile(module, args.target)
            if args.output:
                os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
                with open(args.output, "w", encoding="utf-8") as out:
                    out.write(result)
                print(f"[OK] Transpiled {args.target.upper()} code saved to {args.output}")
            else:
                print(result)

    elif args.command == "skills":
        reg = HermesSkillRegistry()
        if args.format == "openclaw":
            manifest = reg.export_openclaw_skills_manifest()
            print(json.dumps(manifest, indent=2))
        else:
            tools = reg.export_hermes_tools_json()
            print(json.dumps(tools, indent=2))

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
