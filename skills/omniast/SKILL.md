---
name: omniast
description: Operates and transpiles graph-native OmniAST/GraphLang modules, executes graph-based queries, and generates high-efficiency code for AI agents with 80%+ token reduction.
---

# OmniAST / GraphLang Skill

Use this skill whenever you need to:
1. Generate new backend services, listeners, machines, or sentinels without generating thousands of lines of boilerplate.
2. Query codebase relationships, call-graphs, and AST topologies instead of reading files linearly.
3. Transpile `.omni` modules into Java 21+ (Paper/Purpur), Python daemons, or Rust modules.
4. Enforce the **Zero-Noise Alert Throttling** rule to avoid spamming operators.

## Workflow

### Step 1: Query Before Reading
Before opening files, ask the graph kernel:
```bash
omniast query --graph ./graph.json --symbol <TargetSymbol>
```

### Step 2: Formulate Intent in OmniAST
Write a `.omni` specification file rather than hundreds of lines of boilerplate. Example:
```omniast
module RateLimiter {
    target: [jvm, py]

    listener AntiFlood on player.chat {
        guard actor.message_count_in(3s) > 4
        cancel
        actor.mute(duration=5m, reason="Excessive message flood")
    }
}
```

### Step 3: Transpile to Target
```bash
omniast transpile --input RateLimiter.omni --target jvm --output ./src/main/java
```
