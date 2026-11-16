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

### 3.6 Web Single-Page Applications & Reactive Pages
Declares reactive, client-side views and state signals without JSX, Virtual DOM, or npm build steps:

```omniast
page ClusterMonitor path="/" {
    title: "StarMesh · Sovereign Autonomous Cluster"
    layout: "SovereignShell"
    theme: "sovereign"
    signal clusterHealth = "OPTIMAL"
    signal activeNodes = 12
    signal averageTPS = 20.0
}
```

### 3.7 Data Models & REST Endpoints (Full-Stack)
Declares strongly typed data schemas and HTTP REST endpoints for Axum and web consumers:

```omniast
model ServerNode {
    id: uuid primary_key
    hostname: string index
    region: string
    memory_rss: long
    cpu_cores: int
    status: string
}

endpoint GET "/api/v1/cluster/status" {
    guard actor.has_role("sre_lead") or actor.has_role("architect")
    cache ttl=5s
}

endpoint POST "/api/v1/cluster/drain" {
    guard actor.has_role("root_operator")
    rate_limit max=3 window=60s
}
```

---

## 4. Transpiler Backends

1. **JVM Backend (`emit-jvm`):** Generates compliant Java 21+ code targeting Paper/Purpur APIs, avoiding reflection and compiling direct calls.
2. **Rust Backend (`emit-rust`):** Emits zero-cost abstractions, safe multithreading via Tokio, Axum REST routing (`build_router()`), Serde model serialization, and Panama FFI bindings for Java.
3. **Python Backend (`emit-py`):** Generates asynchronous `asyncio` services for system management, monitoring, and Discord/Telegram bots.
4. **OmniWeb Backend (`emit-web` / `emit-spa` / `emit-gh-pages`):** Generates single-file reactive SPAs embedding the Micro-Signals reactive store (<2KB), in-browser theme switcher, metrics bento grid, dynamic data table with filtering, and AST playground. 100% zero-dependency, static CDN and GitHub Pages ready.
5. **WASM / WAT Backend (`emit-wasm` / `emit-wat`):** Compiles high-speed execution routines into WebAssembly text and binary formats for edge runtimes and browsers.

---

## 5. Pluggable UI Design Themes

OmniAST features 4 built-in, production-grade visual themes:
* **`sovereign`:** Glassmorphism, Bento Grid layout, deep dark background, amethyst purple and cyan accents.
* **`cyberpunk`:** High-contrast tactical dark slate, neon cyan and electric magenta glows, angular borders.
* **`terminal`:** Classic retro CRT monitor, phosphor green monochrome palette, monospace typography.
* **`minimal`:** Stripe and VitePress inspired clean documentation theme with high-contrast neutral slate.
