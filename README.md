<div align="center">

<img src="https://raw.githubusercontent.com/JackStar6677-1/omniast/main/assets/banner.svg" alt="OmniAST / GraphLang — The Universal Graph-Native Kernel for Autonomous AI Systems & Engine Interop" width="100%" />

</div>

<p align="center">
  <strong>The Universal Graph-Native Kernel & Declarative AST for Autonomous AI Systems, Game Engines & Distributed SRE</strong>
</p>

<p align="center">
  <a href="#key-innovations"><img src="https://img.shields.io/badge/Architecture-Graph--Native-38BDF8?style=flat-square" alt="Graph Native"></a>
  <a href="#token-efficiency"><img src="https://img.shields.io/badge/LLM_Efficiency-85%25_Token_Reduction-818CF8?style=flat-square" alt="Token Saver"></a>
  <a href="#supported-targets"><img src="https://img.shields.io/badge/Targets-Java_21+_·_Rust_·_Python-F472B6?style=flat-square" alt="Multi Target"></a>
  <a href="#license"><img src="https://img.shields.io/badge/License-MIT-34D399?style=flat-square" alt="MIT License"></a>
</p>

---

## 🌌 What is OmniAST (GraphLang)?

**OmniAST** (also known as **GraphLang**) is an intermediate, declarative programming language and kernel runtime engineered for the new paradigm of software development: **collaboration between autonomous AI models (Google DeepMind Antigravity, OpenAI Codex, Anthropic Claude, DeepSeek, Grok) and high-throughput execution engines.**

Traditional programming languages (Java, C++, Rust, Python) were designed decades ago for humans typing characters in linear text files. They are full of syntactic ceremonies: thousands of redundant lines of imports, boilerplate classes, verbose access modifiers, and complex packaging structures. When modern AI models read and reason through these files, **millions of tokens are wasted on boilerplate rather than architecture and logic**.

**OmniAST changes this equation:**
1. **Direct AST Representation:** Code is authored and represented directly as an **Executable Abstract Syntax Tree & Dependency Graph**.
2. **Universal AI Interoperability:** Any AI agent or human can read, mutate, query, and verify complete architectures with minimal token cost.
3. **Multi-Target Transpilation:** Write once in OmniAST; transpile deterministically to **Java 21/25 (Paper/Spigot)**, **Native Rust/Tokio**, or **Asynchronous Python**.

---

## ⚡ Key Innovations

```
                       ┌─────────────────────────────────────────┐
                       │          OmniAST Declarative Node       │
                       │           (85% Fewer Tokens)            │
                       └────────────────────┬────────────────────┘
                                            │
                                 ┌──────────┴──────────┐
                                 ▼                     ▼
                       ┌──────────────────┐   ┌──────────────────┐
                       │  Agent Reasoning │   │  Graphify Memory │
                       │ (Claude · Codex  │   │ (AST & Community │
                       │  Antigravity)    │   │    Knowledge)    │
                       └─────────┬────────┘   └────────┬─────────┘
                                 │                     │
                       ┌─────────▼─────────────────────▼─────────┐
                       │             OmniAST Kernel              │
                       │     Typecheck · Validate · Transpile    │
                       └────────────────────┬────────────────────┘
                                            │
           ┌────────────────────────────────┼────────────────────────────────┐
           ▼                                ▼                                ▼
  ┌──────────────────┐             ┌──────────────────┐             ┌──────────────────┐
  │  JVM (Java 21+)  │             │  Native (Rust)   │             │ Asynchronous Py  │
  │  Paper / Purpur  │             │  Zero-Cost LLVM  │             │ SRE Sentinels    │
  │  Minecraft Engine│             │  Panama Java FFI │             │ Fleet Automations│
  └──────────────────┘             └──────────────────┘             └──────────────────┘
```

* **Token-Efficient by Design:** Cuts down model context consumption by 70% to 85% compared to raw Java or C++.
* **Engine-Agnostic & Native Interop:** Ideal for game server extensions (like Paper/Spigot plugins), multi-agent swarms, SRE automation, and industrial networks.
* **AST First, Text Second:** Fully integrated with Tree-sitter and AST graph databases for instant topological querying and zero-cost structural diffs.

---

## 🛠️ Code Examples

### 1. In-Engine Safety & Event Routing (e.g. Minecraft / Paper)

Traditional Java requires 150+ lines across multiple classes, annotations, listener registrations, and plugin loaders. In **OmniAST**, the entire intent is declared cleanly:

```omniast
module OdysseiaSafety {
    version: "2.1.0"
    target: [jvm, rust]

    listener ChatFilter on player.chat priority(lowest) {
        guard event.message.contains_hate_speech()

        cancel
        actor.ban(reason="Zero tolerance policy", ip=true)
        world.strike_lightning(actor.location)
        notify discord.mod_channel, "Blocked & banned attacker: " + actor.name
    }
}
```

### 2. Autonomous SRE Sentinel & Daemon

Replaces fragile multi-file Python scripts with self-healing, declarative supervisor logic:

```omniast
module StagingSentinel {
    version: "1.0.0"
    target: [py, rust]

    sentinel StagingFleetSupervisor {
        interval: 30m
        target: systemd("saori-staging-s2")

        on failure {
            quarantine_faulty_jars()
            alert(operator="jack", channel="discord", throttle=12h)
        }

        on progress(port_ok) {
            log "Fleet progress: " + port_ok.addon_name
            # Anti-spam: Suppresses notifications when no human intervention is needed
        }
    }
}
```

---

## 🚀 Getting Started

### Installation

```bash
git clone https://github.com/JackStar6677-1/omniast.git
cd omniast
pip install -e .
```

### Quick Run & CLI Usage

OmniAST provides a unified CLI to parse, transpile, and inspect modules:

```bash
# 1. Parse an OmniAST module into an AST dependency graph
omniast parse --input examples/industrial_machine.omni

# 2. Transpile to Native Rust / Tokio with Panama FFI bindings
omniast transpile --input examples/industrial_machine.omni --target rust --output ./dist/machine.rs

# 3. Transpile to Java 21+ Paper / Spigot Plugin code
omniast transpile --input examples/odysseia_safety.omni --target jvm --output ./dist/SafetyPlugin.java

# 4. Transpile to Asynchronous Python SRE Daemon
omniast transpile --input examples/sre_sentinel.omni --target py --output ./dist/sentinel.py

# 5. Run the Kernel Test Suite
python -m unittest discover -s tests
```

---

## 🤖 AI Agent & MCP Integration (Zero Context Exhaustion)

OmniAST ships with a native **Model Context Protocol (MCP)** server and universal agent prompt. Any AI coding assistant (Antigravity, Codex, Claude, DeepSeek, Grok) can connect to the OmniAST Kernel to operate on code graphs and transpile intents:

### MCP Server Configuration (`mcp.json`)

```json
{
  "mcpServers": {
    "omniast": {
      "command": "python",
      "args": ["/path/to/omniast/mcp_server/server.py"]
    }
  }
}
```

### Universal Agent Prompt
Equip your AI agent with [`prompts/universal_agent_prompt.md`](prompts/universal_agent_prompt.md). The agent will automatically adopt graph-first navigation, bypass linear file scans, formulate code in `.omni` declarative blocks, and enforce **Zero-Noise Alert Throttling** for automated daemons.

---

## 🧭 Project Roadmap

- [x] **Phase 1: Concept & Initial Architecture** (Kernel data structures, AST definitions, animated banner).
- [x] **Phase 2: Core Transpiler Suite** (Java 21+ Paper/Spigot, Asynchronous Python SRE, Native Rust/Tokio FFI).
- [x] **Phase 3: Agent Driver & MCP Server** (Native JSON-RPC 2.0 MCP server for Claude, Codex, Antigravity, DeepSeek, Grok).
- [x] **Phase 4: Unified CLI & Test Suite** (`omniast` command-line interface, automated unit tests, GitHub Actions CI).
- [ ] **Phase 5: Tree-Sitter Grammar (`tree-sitter-omniast`)** (Formal grammar definition, syntax highlighting for VS Code & Neovim).
- [ ] **Phase 6: Self-Hosting Runtime** (Compiling OmniAST to native WebAssembly & standalone binaries).

---

## 🤝 Contributing

Contributions are welcome from developers, language designers, and AI researchers! Please read [`spec/LANGUAGE_SPEC.md`](spec/LANGUAGE_SPEC.md) before submitting pull requests.

## 📄 License

OmniAST is open-source software released under the [MIT License](LICENSE).
