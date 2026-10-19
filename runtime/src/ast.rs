use serde::{Deserialize, Serialize};
use std::collections::HashMap;

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub enum NodeType {
    Module,
    Entity,
    Listener,
    Sentinel,
    Machine,
    Pipeline,
    Service,
    Field,
    Block,
    Statement,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct OmniNode {
    pub id: String,
    pub node_type: NodeType,
    pub name: String,
    pub properties: HashMap<String, String>,
    pub metadata: HashMap<String, String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct OmniEdge {
    pub source: String,
    pub target: String,
    pub relationship: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GraphModule {
    pub name: String,
    pub version: String,
    pub targets: Vec<String>,
    pub nodes: Vec<OmniNode>,
    pub edges: Vec<OmniEdge>,
}

impl GraphModule {
    pub fn new(name: &str, version: &str) -> Self {
        Self {
            name: name.to_string(),
            version: version.to_string(),
            targets: vec!["jvm".to_string(), "rust".to_string(), "py".to_string(), "wasm".to_string()],
            nodes: Vec::new(),
            edges: Vec::new(),
        }
    }

    pub fn add_node(&mut self, node: OmniNode) {
        self.nodes.push(node);
    }

    pub fn add_edge(&mut self, source: &str, target: &str, relationship: &str) {
        self.edges.push(OmniEdge {
            source: source.to_string(),
            target: target.to_string(),
            relationship: relationship.to_string(),
        });
    }
}
