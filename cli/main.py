"""
OmniAST / GraphLang Command Line Interface (CLI)
Allows parsing, transpiling, and inspecting OmniAST modules directly from the terminal.
"""

import sys
import argparse
import json
import os

from core.kernel.engine import OmniASTKernel
from transpilers.java_transpiler import JavaTranspiler
from transpilers.python_transpiler import PythonTranspiler
from transpilers.rust_transpiler import RustTranspiler

def build_kernel() -> OmniASTKernel:
    k = OmniASTKernel()
    k.register_transpiler("jvm", JavaTranspiler())
    k.register_transpiler("py", PythonTranspiler())
    k.register_transpiler("rust", RustTranspiler())
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
    trans_cmd.add_argument("--target", "-t", choices=["jvm", "py", "rust"], required=True, help="Target platform (jvm, py, rust)")
    trans_cmd.add_argument("--output", "-o", help="Optional output file path")

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
        result = kernel.transpile(module, args.target)
        if args.output:
            os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
            with open(args.output, "w", encoding="utf-8") as out:
                out.write(result)
            print(f"[OK] Transpiled {args.target.upper()} code saved to {args.output}")
        else:
            print(result)

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
