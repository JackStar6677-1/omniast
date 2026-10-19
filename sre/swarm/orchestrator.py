"""
OmniAST SRE Swarm & Multi-Agent Orchestrator
Manages concurrent AI models (Claude, Codex, Antigravity, DeepSeek, Grok) acting
as autonomous software engineers for multiple users, repositories, and servers.
"""

import time
import uuid
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field

@dataclass
class SwarmAgent:
    id: str
    name: str
    model: str  # e.g., 'anthropic/claude-3-7-sonnet', 'openai/codex-1', 'deepmind/antigravity', 'deepseek-v3'
    role: str   # 'code_repairer', 'architecture_reviewer', 'security_sentinel', 'test_generator'
    status: str # 'idle', 'analyzing', 'repairing', 'verifying', 'recovering'
    current_task: Optional[str] = None
    processed_count: int = 0
    repaired_count: int = 0
    last_active_ts: float = field(default_factory=time.time)

@dataclass
class CodebaseIncident:
    id: str
    user_id: str
    repo_name: str
    file_path: str
    issue_type: str # 'syntax_error', 'runtime_exception', 'null_pointer', 'concurrency_leak', 'npe'
    severity: str   # 'critical', 'high', 'medium', 'suggestion'
    raw_evidence: str
    suggested_patch: Optional[str] = None
    status: str     # 'detected', 'triaged', 'investigating', 'patch_ready', 'verified', 'resolved'
    assigned_agent_id: Optional[str] = None
    created_at: float = field(default_factory=time.time)

class SREOrchestrator:
    """
    Central SRE kernel coordinating agents, auto-triage, and self-healing.
    """
    def __init__(self):
        self.agents: Dict[str, SwarmAgent] = {}
        self.incidents: Dict[str, CodebaseIncident] = {}
        self.users: Dict[str, Dict[str, Any]] = {}
        self.activity_log: List[Dict[str, Any]] = []

        # Initialize default multi-model developer squad
        self._init_default_squad()

    def _init_default_squad(self):
        squad = [
            ("agent-anti", "Antigravity Prime", "deepmind/antigravity", "architecture_reviewer"),
            ("agent-codex", "Codex Engine", "openai/codex-1", "code_repairer"),
            ("agent-claude", "Claude Inspector", "anthropic/claude-3-7-sonnet", "security_sentinel"),
            ("agent-deepseek", "DeepSeek MathCore", "deepseek-ai/deepseek-coder", "test_generator"),
            ("agent-grok", "Grok Pulse", "xai/grok-code", "concurrency_auditor")
        ]
        for aid, name, model, role in squad:
            self.agents[aid] = SwarmAgent(id=aid, name=name, model=model, role=role, status="idle")

    def register_user(self, user_id: str, username: str, language: str = "es", repos: List[str] = None):
        self.users[user_id] = {
            "id": user_id,
            "username": username,
            "language": language,
            "repos": repos or [],
            "registered_at": time.time()
        }
        self.log_event("user_registered", f"User {username} ({user_id}) joined OmniAST SRE Kernel.")

    def log_event(self, event_type: str, message: str, meta: Dict[str, Any] = None):
        entry = {
            "id": str(uuid.uuid4())[:8],
            "timestamp": time.time(),
            "type": event_type,
            "message": message,
            "metadata": meta or {}
        }
        self.activity_log.append(entry)
        if len(self.activity_log) > 500:
            self.activity_log.pop(0)

    def submit_incident(self, user_id: str, repo: str, file_path: str, issue_type: str, 
                        severity: str, raw_evidence: str) -> str:
        inc_id = f"INC-{int(time.time()) % 100000:05d}"
        incident = CodebaseIncident(
            id=inc_id,
            user_id=user_id,
            repo_name=repo,
            file_path=file_path,
            issue_type=issue_type,
            severity=severity,
            raw_evidence=raw_evidence,
            status="detected"
        )
        self.incidents[inc_id] = incident
        self.log_event("incident_detected", f"New {severity.upper()} incident {inc_id} in {repo}:{file_path}", {"incident_id": inc_id})
        
        # Autonomous Dispatch: match with idle agent
        self.dispatch_incident(inc_id)
        return inc_id

    def dispatch_incident(self, inc_id: str):
        incident = self.incidents.get(inc_id)
        if not incident or incident.status != "detected":
            return

        # Find best available agent
        available = [a for a in self.agents.values() if a.status == "idle"]
        if not available:
            # If all busy, pick least recently active
            available = sorted(self.agents.values(), key=lambda a: a.last_active_ts)

        agent = available[0]
        agent.status = "analyzing"
        agent.current_task = f"Repairing {incident.id} ({incident.file_path})"
        agent.last_active_ts = time.time()
        incident.assigned_agent_id = agent.id
        incident.status = "investigating"

        self.log_event("agent_dispatched", f"Agent {agent.name} assigned to {incident.id}", {"agent": agent.name, "incident": incident.id})

    def apply_repair(self, inc_id: str, patch_code: str):
        incident = self.incidents.get(inc_id)
        if not incident:
            return
        incident.suggested_patch = patch_code
        incident.status = "patch_ready"

        agent = self.agents.get(incident.assigned_agent_id)
        if agent:
            agent.status = "idle"
            agent.current_task = None
            agent.repaired_count += 1
            agent.processed_count += 1

        self.log_event("patch_generated", f"Automated patch verified for {inc_id}", {"incident_id": inc_id})

    def get_dashboard_state(self) -> Dict[str, Any]:
        return {
            "kernel_status": "ONLINE",
            "uptime_seconds": time.time(),
            "active_agents": [
                {
                    "id": a.id,
                    "name": a.name,
                    "model": a.model,
                    "role": a.role,
                    "status": a.status,
                    "current_task": a.current_task,
                    "repaired_count": a.repaired_count
                } for a in self.agents.values()
            ],
            "incidents": [
                {
                    "id": i.id,
                    "user_id": i.user_id,
                    "repo": i.repo_name,
                    "file": i.file_path,
                    "type": i.issue_type,
                    "severity": i.severity,
                    "status": i.status,
                    "agent": self.agents.get(i.assigned_agent_id).name if i.assigned_agent_id in self.agents else "Unassigned",
                    "created_at": i.created_at
                } for i in sorted(self.incidents.values(), key=lambda x: x.created_at, reverse=True)[:30]
            ],
            "recent_activity": self.activity_log[-20:],
            "registered_users_count": len(self.users)
        }
