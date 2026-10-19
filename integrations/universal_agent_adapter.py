"""
Universal Agent Adapter for OmniAST
Allows any external AI framework (Nous Hermes, OpenClaw, SAORI, LangChain, CrewAI,
AutoGen, OpenDevin, Claude Code, or Antigravity) to adopt OmniAST as a native capability.
"""

from typing import Dict, Any, List, Optional
import json

from core.kernel.engine import OmniASTKernel
from transpilers.java_transpiler import JavaTranspiler
from transpilers.python_transpiler import PythonTranspiler
from transpilers.rust_transpiler import RustTranspiler
from transpilers.typescript_transpiler import TypeScriptTranspiler
from transpilers.wasm_transpiler import WasmTranspiler
from core.skills.hermes_openclaw import HermesSkillRegistry

class UniversalAgentAdapter:
    """
    Standard interface exposing OmniAST tools, schemas, and execution targets
    across all mainstream AI agent ecosystems.
    """
    def __init__(self):
        self.kernel = OmniASTKernel()
        self.kernel.register_transpiler("jvm", JavaTranspiler())
        self.kernel.register_transpiler("py", PythonTranspiler())
        self.kernel.register_transpiler("rust", RustTranspiler())
        self.kernel.register_transpiler("ts", TypeScriptTranspiler())
        self.kernel.register_transpiler("wat", WasmTranspiler())
        self.skills = HermesSkillRegistry()

    def get_supported_frameworks(self) -> List[str]:
        return [
            "hermes-agent (NousResearch)",
            "openclaw (Multi-Channel Daemon)",
            "saori (Star SRE Swarm)",
            "model-context-protocol (Anthropic/Claude/Antigravity MCP)",
            "openai-function-calling (Codex/GPT-4o)",
            "langchain / langgraph",
            "crewai / autogen"
        ]

    def export_tools_for_framework(self, framework: str) -> Any:
        fw = framework.lower().strip()
        if "hermes" in fw:
            return self.skills.export_hermes_tools_json()
        elif "openclaw" in fw:
            return self.skills.export_openclaw_skills_manifest()
        elif "mcp" in fw:
            return {
                "server": "omniast",
                "capabilities": ["tools", "resources"],
                "tools": self.skills.export_hermes_tools_json()
            }
        else:
            return self.skills.export_hermes_tools_json()

    def execute_agent_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Unified tool execution dispatcher."""
        if tool_name in ["omniast_parse", "omni_parse"]:
            code = arguments.get("code", "")
            mod = self.kernel.parse_source(code)
            return {"status": "ok", "module": mod.name, "nodes": [n.to_dict() for n in mod.nodes]}
        elif tool_name in ["omniast_transpile", "omni_transpile"]:
            code = arguments.get("code", "")
            target = arguments.get("target", "jvm")
            mod = self.kernel.parse_source(code)
            if target == "wasm":
                binary = WasmTranspiler().transpile_to_wasm_binary(mod.to_dict())
                return {"status": "ok", "target": "wasm", "length": len(binary)}
            elif target == "wat":
                return {"status": "ok", "code": WasmTranspiler().transpile_to_wat(mod.to_dict())}
            else:
                return {"status": "ok", "code": self.kernel.transpile(mod, target)}
        elif tool_name == "shared_memory_recall":
            return {"status": "ok", "recall": f"Knowledge query simulated for: {arguments.get('query')}"}
        else:
            return {"error": f"Tool '{tool_name}' not implemented in adapter"}
