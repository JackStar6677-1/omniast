"""
OmniAST Hermes & OpenClaw Skill Framework (v0.1.0)
Standardizes tool-calling schemas, multi-channel gateways, and autonomous skill packs
compatible with Nous Hermes (JSON Schema function calling) and OpenClaw agent architectures.
"""

from typing import Dict, Any, List
import json

class HermesSkillRegistry:
    """
    Central registry for Hermes and OpenClaw agent skills.
    Translates OmniAST Graph operations into JSON Schema function calling specifications.
    """

    def __init__(self):
        self.skills: Dict[str, Dict[str, Any]] = {}
        self._register_default_skills()

    def register(self, name: str, description: str, parameters: Dict[str, Any], handler_meta: Dict[str, Any]):
        self.skills[name] = {
            "type": "function",
            "function": {
                "name": name,
                "description": description,
                "parameters": parameters,
            },
            "openclaw_meta": handler_meta
        }

    def _register_default_skills(self):
        # 1. OmniAST Graph Query Skill
        self.register(
            name="omniast_query_graph",
            description="Query the AST dependency graph by node type, name, or connected edge relationships.",
            parameters={
                "type": "object",
                "properties": {
                    "node_type": {
                        "type": "string",
                        "enum": ["module", "entity", "listener", "sentinel", "machine", "all"],
                        "description": "Category of AST node to filter."
                    },
                    "target_name": {
                        "type": "string",
                        "description": "Optional name or regex pattern of the node."
                    },
                    "depth": {
                        "type": "integer",
                        "description": "Graph traversal depth from the target node (default: 1)."
                    }
                },
                "required": ["node_type"]
            },
            handler_meta={
                "category": "ast_kernel",
                "requires_sandbox": False,
                "permission": "read"
            }
        )

        # 2. Atomic Graph Mutation Skill
        self.register(
            name="omniast_mutate_node",
            description="Perform an atomic graph mutation on an OmniAST node (add, update property, prune edge).",
            parameters={
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "enum": ["add_node", "update_property", "remove_node", "add_edge"],
                        "description": "Type of graph mutation."
                    },
                    "node_id": {
                        "type": "string",
                        "description": "Identifier of the target node."
                    },
                    "payload": {
                        "type": "object",
                        "description": "Key-value attributes or properties to apply."
                    }
                },
                "required": ["action", "node_id"]
            },
            handler_meta={
                "category": "ast_kernel",
                "requires_sandbox": False,
                "permission": "write"
            }
        )

        # 3. Omnichannel Dispatcher (OpenClaw Multi-Gateway)
        self.register(
            name="openclaw_dispatch_message",
            description="Send a formatted notification, alert, or interactive prompt to Discord, WhatsApp, or Web Console.",
            parameters={
                "type": "object",
                "properties": {
                    "channel": {
                        "type": "string",
                        "enum": ["discord", "whatsapp", "web_console", "broadcast"],
                        "description": "Target communication channel."
                    },
                    "recipient": {
                        "type": "string",
                        "description": "User ID, phone number, channel ID, or 'default'."
                    },
                    "content": {
                        "type": "string",
                        "description": "Message body or markdown content."
                    },
                    "urgency": {
                        "type": "string",
                        "enum": ["info", "warning", "critical", "silent_digest"],
                        "description": "Urgency tier. Silent digests are throttled to prevent spam."
                    }
                },
                "required": ["channel", "content"]
            },
            handler_meta={
                "category": "gateway",
                "requires_sandbox": False,
                "permission": "network"
            }
        )

        # 4. Sandboxed Shell & SRE Execution (OpenClaw Docker/Host Sandbox)
        self.register(
            name="openclaw_exec_sandboxed",
            description="Execute an audited shell command inside the isolated SRE container or host runner.",
            parameters={
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "Command line string to execute."
                    },
                    "working_dir": {
                        "type": "string",
                        "description": "Directory where command executes."
                    },
                    "timeout_seconds": {
                        "type": "integer",
                        "description": "Maximum execution duration before auto-kill."
                    }
                },
                "required": ["command"]
            },
            handler_meta={
                "category": "sre_runner",
                "requires_sandbox": True,
                "permission": "system_exec"
            }
        )

        # 5. Shared Memory (Vector & SQLite WAL)
        self.register(
            name="shared_memory_recall",
            description="Recall persistent knowledge, prior incident resolutions, or architectural facts from shared memory.",
            parameters={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search topic, keyword, or semantic question."
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of memory events to return (default: 5)."
                    }
                },
                "required": ["query"]
            },
            handler_meta={
                "category": "memory",
                "requires_sandbox": False,
                "permission": "read"
            }
        )

    def export_hermes_tools_json(self) -> List[Dict[str, Any]]:
        """Exports standard Hermes / OpenAI-compatible tool specifications."""
        return [
            {
                "type": s["type"],
                "function": s["function"]
            }
            for s in self.skills.values()
        ]

    def export_openclaw_skills_manifest(self) -> Dict[str, Any]:
        """Exports an OpenClaw-compatible plugin manifest with permission boundaries."""
        return {
            "name": "omniast-agent-skills",
            "version": "0.1.0",
            "engine": "openclaw-hermes-hybrid",
            "skills": [
                {
                    "name": name,
                    "description": s["function"]["description"],
                    "parameters": s["function"]["parameters"],
                    "meta": s["openclaw_meta"]
                }
                for name, s in self.skills.items()
            ]
        }
