# OmniAST / GraphLang Specification (v0.1.0-draft)

## 1. Abstract
**OmniAST** (also referred to as **GraphLang**) is an intermediate, graph-native programming language and execution kernel designed specifically for modern autonomous AI coding agents (such as Google Antigravity, OpenAI Codex, Anthropic Claude, DeepSeek, and Grok) and high-concurrency event-driven engines.

Traditional programming languages (Java, C++, Rust, Python) were engineered for humans typing characters in linear ASCII files. They carry extensive syntactic overhead—excess imports, verbose type declarations, package definitions, access modifiers, and ceremonial boilerplate. 

OmniAST represents code directly as an **Executable Abstract Syntax Tree (AST) & Dependency Graph**:
* **Zero Boilerplate:** Omits boilerplate imports, classes, and repetitive annotations.
* **80%+ Token Reduction:** Large Language Models (LLMs) reason and generate intent-dense graphs rather than thousands of lines of linear syntax.
* **Universal Transpilation:** A single OmniAST module compiles down to JVM Bytecode (Java 21/25), native Rust/LLVM, or standalone Python/TypeScript modules.

---

## 2. Core Architectural Pillars

```
                     ┌─────────────────────────────────────────┐
                     │          OmniAST Intent & Graph         │
                     │       (Direct AST / Token-Efficient)    │
                     └────────────────────┬────────────────────┘
                                          │
                               ┌──────────┴──────────┐
                               ▼                     ▼
                     ┌──────────────────┐   ┌──────────────────┐
                     │  Agent Reasoning │   │  Graphify Memory │
                     │   (Claude/Codex/ │   │ (AST & Community │
                     │   Antigravity)   │   │    Knowledge)    │
                     └─────────┬────────┘   └────────┬─────────┘
                               │                     │
                     ┌─────────▼─────────────────────▼─────────┐
                     │             OmniAST Kernel              │
                     │      Parser · Validator · Optimizer     │
                     └────────────────────┬────────────────────┘
                                          │
         ┌────────────────────────────────┼────────────────────────────────┐
         ▼                                ▼                                ▼
┌──────────────────┐             ┌──────────────────┐             ┌──────────────────┐
│  Target: JVM     │             │  Target: Rust    │             │  Target: Python  │
│  Paper / Spigot  │             │  Native LLVM     │             │  SRE Watchers    │
│  Slimefun / FFI  │             │  High Performance│             │  Automation Bots │
└──────────────────┘             └──────────────────┘             └──────────────────┘
```

---

## 3. Language Syntax & Primitives

OmniAST syntax uses clean, declarative constructs tailored for state machines, reactors, distributed systems, and microservices.

### 3.1 Entities & Modules
Modules define autonomous units of execution (e.g., a plugin, a daemon, or an SRE watcher).

```omniast
module OdysseiaCore {
    version: "2.0.0"
    target: [jvm, rust]
}
```

### 3.2 State & Storage
Declarative storage handles persistent NBT/PDC, SQLite, or Redis without manual SQL/IO code:

```omniast
entity PlayerVault {
    id: uuid primary
    owner: string
    items: list<item> max(54)
    balance: decimal default(0.0)

    persist: pdc("odysseia:vault_data")
}
```

### 3.3 Event Listeners & Reactive Hooks
Events specify triggers, conditions (`guard`), and atomic effects:

```omniast
listener AntiSpamGuard on player.chat priority(lowest) {
    guard event.message.matches(HATE_SPEECH_PATTERN)
    
    cancel
    actor.ban(reason="Zero tolerance hate speech", ip=true)
    strike_lightning(actor.location)
    notify discord.mod_channel, "Blocked & banned attacker: " + actor.name
}
```

### 3.4 SRE Sentinel & Distributed Automation
Replaces fragile multi-file Python scripts with declarative watchers:

```omniast
sentinel StagingFleetSupervisor {
    interval: 30m
    target: systemd("saori-staging-s2")

    on failure {
        quarantine_faulty_jars()
        alert(operator="jack", channel="discord", throttle=12h)
    }

    on progress(port_ok) {
        log "Fleet progress: " + port_ok.addon_name
        # Note: Suppresses notification when no human intervention is needed!
    }
}
```

### 3.5 Industrial Mechanics & Slimefun Machine Networks
Expresses complex multi-block energy routing and item sorting in 10 lines:

```omniast
machine QuantumCapacitor : EnergyStorage {
    capacity: 250000 J
    rate: 2000 J/s

    on tick(delta) {
        if network.has_deficit {
            route self.stored -> network.bus, max=rate
        }
    }
}
```

---

## 4. Transpiler Backends

1. **JVM Backend (`emit-jvm`):** Generates compliant Java 21+ code targeting Paper/Purpur APIs, avoiding reflection and compiling direct calls.
2. **Rust Backend (`emit-rust`):** Emits zero-cost abstractions, safe multithreading via Tokio, and Foreign Function Interface (FFI) bindings for Java via Project Panama.
3. **Python Backend (`emit-py`):** Generates asynchronous `asyncio` services for system management, monitoring, and Discord/Telegram bots.
