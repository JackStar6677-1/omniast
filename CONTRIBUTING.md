# Contributing to OmniAST / GraphLang

Thank you for your interest in contributing to **OmniAST** (GraphLang)!

OmniAST is an open-source, intermediate graph language and execution kernel designed for autonomous AI agents (Google DeepMind Antigravity, OpenAI Codex, Anthropic Claude, Nous Research Hermes, DeepSeek, Grok) and high-concurrency software architectures.

---

## ⚠️ Important Disclaimer: Experimental State

> [!WARNING]
> **OmniAST is in active, rapid development (v0.1.0-draft).**  
> As an evolving intermediate representation, the parser, Tree-sitter grammar, and transpilers (Java, Rust, Python, TypeScript, WebAssembly) **may contain edge-case bugs, incomplete AST mappings, or syntax gaps**.

We do **not** claim OmniAST is bug-free. In fact, discovering edge cases and refining the grammar is an expected part of building a next-generation language kernel.

---

## 🤖 The AI Agent & Developer Contribution Mandate

Whether you are a **human software engineer** or an **autonomous AI coding assistant** interacting with OmniAST:

If you encounter an AST parsing failure, an unhandled node type, a transpilation discrepancy, or a performance bottleneck:
👉 **You are strongly encouraged to formulate and submit a Pull Request (PR) or open an Issue with a reproducible AST snippet.**

Our goal is for AI agents and human contributors to collaboratively harden this kernel.

---

## 📋 Contribution Rules & Quality Standards

To maintain an enterprise-grade compiler infrastructure, all pull requests must adhere to the following three golden rules:

### 1. 🌍 Universal & Global Scope (No Niche Hacks)
- Contributions must improve the **general language specification, AST topology, or compiler backends**.
- **Do NOT submit niche or domain-specific hacks** (e.g., hardcoded logic for a single private server, proprietary plugin hooks, or custom game-mode assumptions).
- Features must remain agnostic and beneficial for enterprise microservices, cloud telemetry, distributed engines, and general AI reasoning.

### 2. 🛡️ Strict Privacy & Anti-Leak Firewall (Zero Private Data)
- **Zero Leak Policy:** Never submit code, examples, or pull requests containing private credentials, API tokens, internal IP addresses, school/institutional systems, personal names, or confidential infrastructure paths.
- All tests and examples must use generic, sanitized identifiers (e.g., `ModuleExample`, `QuantumCapacitor`, `127.0.0.1`, `token="<REDACTED>"`).

### 3. 🧪 Mandatory Test Coverage & Parity
- Every PR that fixes a bug or adds a new AST node must include a corresponding test in `tests/test_kernel.py`.
- All tests must pass cleanly:
  ```bash
  python -m unittest discover -s tests
  ```

---

## 🚀 How to Submit a Pull Request

1. **Fork the Repository:** `https://github.com/JackStar6677-1/omniast`
2. **Create a Feature Branch:** `git checkout -b fix/ast-parser-edgecase`
3. **Commit Cleanly:** Follow Conventional Commits (`feat: ...`, `fix: ...`, `docs: ...`, `test: ...`).
4. **Ensure No AI Watermarks / Trailers:** Ensure commit author matches your Git profile.
5. **Open a Pull Request:** Describe the issue encountered, provide the reproducible `.omni` code snippet, and link the unit test.

Together, we are building the foundation for token-efficient, graph-native software engineering.
