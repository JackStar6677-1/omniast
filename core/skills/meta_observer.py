"""
OmniAST Meta Skill Observer & Evolver
(c) 2026 JackStar6677-1 & OmniAST Contributors.
Inspired by one-skill-to-rule-them-all (rebelytics/one-skill-to-rule-them-all).

Monitors agent tool usage, CLI commands, transpilation errors, and human feedback.
Dynamically proposes and registers improved or new OmniAST skills, making the agent
ecosystem self-improving and adaptive over time.
"""

import os
import json
import time
from typing import Dict, Any, List

class MetaSkillObserver:
    """
    Self-improving skill observer for OmniAST agent tasks.
    """
    def __init__(self, skills_dir: str):
        self.skills_dir = skills_dir

    def observe_friction_event(self, tool_name: str, error_message: str, user_correction: str = "") -> Dict[str, Any]:
        """
        Analyzes a failure or correction event and drafts an updated rule/skill.
        """
        observation = {
            "timestamp": time.time(),
            "tool": tool_name,
            "error": error_message,
            "correction": user_correction,
            "proposed_remedy": None
        }

        # Heuristic detection for common grammar or transpilation gaps
        if "unknown target" in error_message.lower():
            observation["proposed_remedy"] = "Update skill manifest to specify valid targets: [jvm, py, rust, ts, wasm, wat]."
        elif "syntax error" in error_message.lower():
            observation["proposed_remedy"] = "Add linting guard before invoking omniast transpile."
        elif "token limit" in error_message.lower() or "context" in error_message.lower():
            observation["proposed_remedy"] = "Enable ContextCompressor to compress AST prior to LLM reasoning."
        else:
            observation["proposed_remedy"] = f"Record edge case pattern for {tool_name} to prevent recurrence."

        return observation

    def generate_skill_manifest(self, skill_name: str, description: str, steps: List[str]) -> str:
        """
        Generates standard SKILL.md content formatted for Antigravity, Claude Code, and OpenClaw.
        """
        formatted_steps = "\n".join([f"### Step {i+1}\n{step}\n" for i, step in enumerate(steps)])
        return f"""---
name: {skill_name}
description: {description}
---

# {skill_name.capitalize()} Skill

{description}

## Workflow

{formatted_steps}
"""
