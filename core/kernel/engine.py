"""
OmniAST / GraphLang Core Kernel & AST Parser
(c) 2026 JackStar6677-1 & OmniAST Contributors
Licensed under MIT or Apache-2.0
"""

import json
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class ASTNode:
    type: str
    name: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    children: List['ASTNode'] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type,
            "name": self.name,
            "metadata": self.metadata,
            "children": [c.to_dict() for c in self.children]
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ASTNode':
        children = [cls.from_dict(c) for c in data.get("children", [])]
        return cls(
            type=data.get("type", "unknown"),
            name=data.get("name", "unnamed"),
            metadata=dict(data.get("metadata", {})),
            children=children
        )

@dataclass
class OmniASTModule:
    name: str
    version: str = "1.0.0"
    targets: List[str] = field(default_factory=lambda: ["jvm", "rust"])
    nodes: List[ASTNode] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "targets": self.targets,
            "nodes": [n.to_dict() for n in self.nodes]
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'OmniASTModule':
        nodes = [ASTNode.from_dict(n) for n in data.get("nodes", data.get("ast_nodes", []))]
        return cls(
            name=data.get("name", data.get("module", "UntitledModule")),
            version=data.get("version", "1.0.0"),
            targets=list(data.get("targets", ["jvm", "rust"])),
            nodes=nodes
        )

    @classmethod
    def from_json(cls, json_str: str) -> 'OmniASTModule':
        return cls.from_dict(json.loads(json_str))

    def export_graph_json(self) -> str:
        return json.dumps({
            "module": self.name,
            "version": self.version,
            "targets": self.targets,
            "ast_nodes": [n.to_dict() for n in self.nodes]
        }, indent=2)

class OmniASTKernel:
    """
    Kernel orchestrator for OmniAST parsing, semantic validation, 
    and target emission.
    """
    def __init__(self):
        self.registry: Dict[str, ASTNode] = {}
        self.transpilers: Dict[str, Any] = {}

    def register_transpiler(self, target: str, transpiler_instance):
        self.transpilers[target] = transpiler_instance

    def parse_source(self, code: str) -> OmniASTModule:
        """
        Parses high-level OmniAST syntax into normalized AST representation.
        Supports modules, listeners, machines, sentinels, properties, guards, and events.
        """
        raw_lines = code.splitlines()
        clean_lines = []
        for line in raw_lines:
            s = line.strip()
            # Strip comments
            if not s or s.startswith("#") or s.startswith("//"):
                continue
            # Remove inline comments
            for marker in ("//", "#"):
                if marker in s:
                    s = s.split(marker)[0].strip()
            if s:
                clean_lines.append(s)

        module_name = "UntitledModule"
        version = "1.0.0"
        targets = ["jvm", "rust"]
        nodes: List[ASTNode] = []
        current_node: Optional[ASTNode] = None

        for line in clean_lines:
            if line.startswith("module "):
                module_name = line.split()[1].replace("{", "").strip()
            elif line.startswith("version:") or line.startswith("version ="):
                val = line.split(":", 1)[1] if ":" in line else line.split("=", 1)[1]
                version = val.strip().strip('"').strip("'").strip()
            elif line.startswith("target:") or line.startswith("targets:"):
                val = line.split(":", 1)[1].strip()
                val = val.strip("[]").replace('"', "").replace("'", "")
                targets = [t.strip() for t in val.split(",") if t.strip()]
            elif line.startswith("listener ") or line.startswith("machine ") or line.startswith("sentinel "):
                # Support: listener Name on event.name {
                parts = line.split()
                node_type = parts[0]
                node_name = parts[1].replace("{", "").strip()
                current_node = ASTNode(type=node_type, name=node_name)
                
                # Check for 'on <event>' syntax in listener declaration
                if " on " in line:
                    after_on = line.split(" on ", 1)[1]
                    event_hook = after_on.split()[0].replace("{", "").strip()
                    current_node.metadata["event"] = event_hook

                nodes.append(current_node)
            elif line == "}":
                current_node = None
            elif current_node is not None:
                if line.startswith("guard "):
                    current_node.metadata["guard"] = line[6:].strip()
                elif ":" in line:
                    key, val = line.split(":", 1)
                    key = key.strip()
                    val = val.strip().strip('"').strip("'")
                    current_node.metadata[key] = val

        return OmniASTModule(name=module_name, version=version, targets=targets, nodes=nodes)

    def transpile(self, module: OmniASTModule, target: str) -> str:
        target = target.lower().strip()
        if target not in self.transpilers:
            # Check target aliases (e.g. wasm -> wat if wat is registered)
            if target == "wasm" and "wat" in self.transpilers:
                target = "wat"
            elif target == "wat" and "wasm" in self.transpilers:
                target = "wasm"
            else:
                raise ValueError(f"Target '{target}' is not registered in OmniAST Kernel.")
        return self.transpilers[target].emit(module)
