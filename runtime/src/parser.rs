use crate::ast::{GraphModule, NodeType, OmniNode};
use std::collections::HashMap;

pub struct NativeParser;

impl NativeParser {
    pub fn parse(source: &str) -> Result<GraphModule, String> {
        let lines: Vec<&str> = source.lines().collect();
        let mut module = GraphModule::new("AnonymousModule", "1.0.0");
        let mut current_node: Option<OmniNode> = None;

        for line in lines {
            let trimmed = line.trim();
            if trimmed.is_empty() || trimmed.starts_with('#') || trimmed.starts_with("//") {
                continue;
            }

            if trimmed.starts_with("module ") {
                let parts: Vec<&str> = trimmed.split_whitespace().collect();
                if parts.len() >= 2 {
                    let mod_name = parts[1].trim_matches('{').trim();
                    module.name = mod_name.to_string();
                }
            } else if trimmed.starts_with("listener ") {
                let parts: Vec<&str> = trimmed.split_whitespace().collect();
                if parts.len() >= 2 {
                    let name = parts[1];
                    let mut props = HashMap::new();
                    if trimmed.contains(" on ") {
                        let after_on = trimmed.split(" on ").nth(1).unwrap_or("");
                        let event = after_on.split_whitespace().next().unwrap_or("");
                        props.insert("event".to_string(), event.to_string());
                    }
                    current_node = Some(OmniNode {
                        id: format!("node:{}", name),
                        node_type: NodeType::Listener,
                        name: name.to_string(),
                        properties: props,
                        metadata: HashMap::new(),
                    });
                }
            } else if trimmed.starts_with("sentinel ") {
                let parts: Vec<&str> = trimmed.split_whitespace().collect();
                if parts.len() >= 2 {
                    let name = parts[1].trim_matches('{').trim();
                    current_node = Some(OmniNode {
                        id: format!("node:{}", name),
                        node_type: NodeType::Sentinel,
                        name: name.to_string(),
                        properties: HashMap::new(),
                        metadata: HashMap::new(),
                    });
                }
            } else if trimmed.starts_with("machine ") {
                let parts: Vec<&str> = trimmed.split_whitespace().collect();
                if parts.len() >= 2 {
                    let name = parts[1].trim_matches('{').trim();
                    current_node = Some(OmniNode {
                        id: format!("node:{}", name),
                        node_type: NodeType::Machine,
                        name: name.to_string(),
                        properties: HashMap::new(),
                        metadata: HashMap::new(),
                    });
                }
            } else if trimmed.starts_with("entity ") {
                let parts: Vec<&str> = trimmed.split_whitespace().collect();
                if parts.len() >= 2 {
                    let name = parts[1].trim_matches('{').trim();
                    current_node = Some(OmniNode {
                        id: format!("node:{}", name),
                        node_type: NodeType::Entity,
                        name: name.to_string(),
                        properties: HashMap::new(),
                        metadata: HashMap::new(),
                    });
                }
            } else if trimmed == "}" {
                if let Some(node) = current_node.take() {
                    module.add_edge(&module.name, &node.id, "contains");
                    module.add_node(node);
                }
            } else if let Some(ref mut node) = current_node {
                if trimmed.contains(':') {
                    let parts: Vec<&str> = trimmed.splitn(2, ':').collect();
                    if parts.len() == 2 {
                        let key = parts[0].trim().to_string();
                        let val = parts[1].trim().trim_matches(',').to_string();
                        node.properties.insert(key, val);
                    }
                }
            }
        }

        if let Some(node) = current_node.take() {
            module.add_edge(&module.name, &node.id, "contains");
            module.add_node(node);
        }

        Ok(module)
    }
}
