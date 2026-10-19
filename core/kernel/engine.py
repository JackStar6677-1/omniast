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

@dataclass
class OmniASTModule:
    name: str
    version: str
    targets: List[str]
    nodes: List[ASTNode] = field(default_factory=list)

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
        """
        lines = [line.strip() for line in code.splitlines() if line.strip() and not line.strip().startswith("#")]
        
        module_name = "UntitledModule"
        version = "1.0.0"
        targets = ["jvm", "rust"]
        nodes = []

        current_node: Optional[ASTNode] = None

        for line in lines:
            if line.startswith("module "):
                module_name = line.split()[1].replace("{", "").strip()
            elif line.startswith("listener ") or line.startswith("machine ") or line.startswith("sentinel "):
                parts = line.split()
                node_type = parts[0]
                node_name = parts[1]
                current_node = ASTNode(type=node_type, name=node_name)
                nodes.append(current_node)
            elif current_node and line.startswith("guard "):
                current_node.metadata["guard"] = line[6:].strip()
            elif current_node and line.startswith("interval:"):
                current_node.metadata["interval"] = line.split(":")[1].strip()
            elif current_node and line.startswith("capacity:"):
                current_node.metadata["capacity"] = line.split(":")[1].strip()

        return OmniASTModule(name=module_name, version=version, targets=targets, nodes=nodes)

    def transpile(self, module: OmniASTModule, target: str) -> str:
        if target not in self.transpilers:
            raise ValueError(f"Target '{target}' is not registered in OmniAST Kernel.")
        return self.transpilers[target].emit(module)
