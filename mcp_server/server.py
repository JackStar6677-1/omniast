#!/usr/bin/env python3
"""
OmniAST / GraphLang Model Context Protocol (MCP) Server
Allows any AI agent (Claude, Codex, Antigravity, DeepSeek, Grok) to natively
query code graphs, transpile modules, and reason with 80%+ fewer tokens.
"""

import sys
import json
import os
from typing import Any, Dict

# Import core kernel
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.kernel.engine import OmniASTKernel
from transpilers.java_transpiler import JavaTranspiler
from transpilers.python_transpiler import PythonTranspiler

kernel = OmniASTKernel()
kernel.register_transpiler("jvm", JavaTranspiler())
kernel.register_transpiler("py", PythonTranspiler())

TOOLS = [
    {
        "name": "omniast_parse",
        "description": "Parses high-level OmniAST syntax into normalized AST and dependency graph JSON.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "source_code": {
                    "type": "string",
                    "description": "The OmniAST / GraphLang code snippet."
                }
            },
            "required": ["source_code"]
        }
    },
    {
        "name": "omniast_transpile",
        "description": "Transpiles an OmniAST module directly to the target runtime (jvm or py).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "source_code": {
                    "type": "string",
                    "description": "The OmniAST code."
                },
                "target": {
                    "type": "string",
                    "enum": ["jvm", "py"],
                    "description": "Target language or runtime platform."
                }
            },
            "required": ["source_code", "target"]
        }
    },
    {
        "name": "omniast_get_prompt",
        "description": "Returns the universal token-saver prompt for AI agents to adopt OmniAST methodology.",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    }
]

def handle_call(name: str, args: Dict[str, Any]) -> Dict[str, Any]:
    if name == "omniast_parse":
        code = args.get("source_code", "")
        module = kernel.parse_source(code)
        return {
            "ok": True,
            "module": module.name,
            "version": module.version,
            "ast_nodes": [n.to_dict() for n in module.nodes]
        }
    elif name == "omniast_transpile":
        code = args.get("source_code", "")
        target = args.get("target", "jvm")
        module = kernel.parse_source(code)
        emitted = kernel.transpile(module, target)
        return {
            "ok": True,
            "target": target,
            "emitted_code": emitted
        }
    elif name == "omniast_get_prompt":
        prompt_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "prompts", "universal_agent_prompt.md")
        if os.path.exists(prompt_path):
            with open(prompt_path, "r", encoding="utf-8") as f:
                return {"ok": True, "prompt": f.read()}
        return {"ok": False, "error": "Prompt file not found"}
    else:
        return {"ok": False, "error": f"Unknown tool: {name}"}

def main():
    """
    Standard JSON-RPC 2.0 loop over stdin/stdout for MCP clients.
    """
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            method = req.get("method")
            msg_id = req.get("id")

            if method == "initialize":
                res = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {"tools": {}},
                        "serverInfo": {"name": "omniast-mcp-kernel", "version": "0.1.0"}
                    }
                }
            elif method == "tools/list":
                res = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {"tools": TOOLS}
                }
            elif method == "tools/call":
                params = req.get("params", {})
                tool_name = params.get("name")
                tool_args = params.get("arguments", {})
                result = handle_call(tool_name, tool_args)
                res = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "content": [{"type": "text", "text": json.dumps(result, indent=2)}],
                        "isError": not result.get("ok", True)
                    }
                }
            else:
                res = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "error": {"code": -32601, "message": f"Method {method} not supported"}
                }
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err_res = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32603, "message": str(e)}
            }
            sys.stdout.write(json.dumps(err_res) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
