use crate::engine::ExecutionEngine;
use crate::parser::NativeParser;

#[cfg(feature = "wasm")]
use wasm_bindgen::prelude::*;

#[cfg_attr(feature = "wasm", wasm_bindgen)]
pub fn omniast_parse_to_json(source: &str) -> String {
    match NativeParser::parse(source) {
        Ok(module) => serde_json::to_string_pretty(&module).unwrap_or_else(|e| format!("{{\"error\": \"{}\"}}", e)),
        Err(err) => format!("{{\"error\": \"{}\"}}", err),
    }
}

#[cfg_attr(feature = "wasm", wasm_bindgen)]
pub fn omniast_optimize(source: &str) -> String {
    match NativeParser::parse(source) {
        Ok(mut module) => match ExecutionEngine::validate_and_optimize(&mut module) {
            Ok(report) => report,
            Err(e) => format!("Optimization error: {}", e),
        },
        Err(e) => format!("Parse error: {}", e),
    }
}

#[cfg_attr(feature = "wasm", wasm_bindgen)]
pub fn omniast_compile_target(source: &str, target: &str) -> String {
    match NativeParser::parse(source) {
        Ok(module) => {
            format!(
                "// [OmniAST WASM Transpiled Target: {}]\n// Module: {} (v{})\n// Status: Ready for runtime execution",
                target, module.name, module.version
            )
        }
        Err(e) => format!("Compilation error: {}", e),
    }
}
