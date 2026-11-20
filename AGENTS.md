# Engineering Standards for AI Agents & Automated Contributors (AGENTS.md)

This document establishes the binding engineering guidelines for any **Autonomous Agent**, **LLM-assisted developer**, or **Automated CI/CD Workflow** submitting issues, pull requests, or code reviews to the **OmniAST / GraphLang** repository.

---

## 🧭 Core Principles

1. **Human Ownership & Accountability**:
   Automated agents and AI models do not hold legal or technical accountability. The human author whose credentials push the code or open the PR assumes **full responsibility** for the correctness, performance, security, and maintenance of the changes.

2. **Transparent Disclosure**:
   In accordance with open source best practices, contributors must explicitly disclose the involvement of AI agents or LLMs in the PR description:
   ```markdown
   ### 🤖 AI Assistance Disclosure
   - Tools used: [e.g., Claude Code, Cursor, Copilot, Custom Agent]
   - Human verification: Fully reviewed, locally compiled, and all unit tests passed.
   ```

3. **Zero AI Slop & Anti-Hallucination Policy**:
   PRs containing any of the following will be **immediately closed without review, marked as spam, and may result in a contributor block**:
   * Hallucinated Rust crates, non-existent standard library methods, or fabricated AST node types.
   * "Plumbing without water": empty boilerplate files, dummy implementations, or unneeded scaffolding.
   * Unrequested refactoring of working compiler/transpiler code without functional or performance justification.
   * Broken builds, compiler warnings, or failing tests (`cargo test` / `python -m unittest`).
   * Circular, repetitive LLM apologies in issue or review threads.

---

## 🧪 Verification & Evidence Requirement

Every PR submitted to OmniAST with AI assistance **must include verifiable evidence of local execution**:

* **Rust Kernel / Transpiler**:
  - `cargo test --all` must pass with zero failures.
  - `cargo clippy --workspace --all-targets -- -D warnings` must pass cleanly.
  - `cargo fmt --check` must be adhered to.
* **Python Grammar & Ast Test Harness**:
  - `python3 -m unittest discover -s tests` must pass cleanly.
* **Deterministic Reproduction**:
  - Bug fixes must include a minimal `.omni` code snippet reproducing the issue and a regression test.

---

## 🚫 Forbidden AI Behaviors

* **Unsolicited Mass PRs**: Automated bots opening batch PRs without maintainer pre-approval.
* **Automated Grammar Churn**: Changing AST definitions without parity across all transpiler targets (Rust, Python, WebAssembly, TypeScript).
* **Review Spam**: Posting automated LLM code reviews on PRs unless specifically invited by the repository maintainers.

---

## 🏛️ Code of Conduct Compliance

All interactions generated or facilitated by AI tools must strictly adhere to our [Code of Conduct](CODE_OF_CONDUCT.md). Hostile, entitled, or automated spam responses will lead to immediate repository-level and organization-level blocking.
