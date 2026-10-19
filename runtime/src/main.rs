use omniast_runtime::engine::ExecutionEngine;
use omniast_runtime::parser::NativeParser;
use std::env;
use std::fs;

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        println!("OmniAST Native Runtime (v0.1.0)");
        println!("Usage: omniast-runtime <file.omni> [--json | --optimize]");
        return;
    }

    let filepath = &args[1];
    let content = match fs::read_to_string(filepath) {
        Ok(c) => c,
        Err(err) => {
            eprintln!("Error reading file {}: {}", filepath, err);
            std::process::exit(1);
        }
    };

    match NativeParser::parse(&content) {
        Ok(mut module) => {
            if args.iter().any(|a| a == "--json") {
                let json = serde_json::to_string_pretty(&module).unwrap();
                println!("{}", json);
            } else {
                let report = ExecutionEngine::validate_and_optimize(&mut module).unwrap();
                println!("Module '{}' parsed successfully.", module.name);
                println!("{}", report);
            }
        }
        Err(err) => {
            eprintln!("Parse error: {}", err);
            std::process::exit(1);
        }
    }
}
