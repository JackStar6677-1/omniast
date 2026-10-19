"""
OmniAST Multi-Account Model Broker & Swarm Pool
Enables concurrent multi-account management, circuit breakers, and automatic failovers
for Google Antigravity, OpenAI Codex, Anthropic Claude, DeepSeek, and Grok.
Modeled after SAORI's 24/7 production broker on Star VPS.
"""

import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field

@dataclass
class ModelAccount:
    id: str                   # e.g., 'antigravity-1', 'codex-2', 'claude-haiku'
    provider: str             # 'antigravity', 'codex', 'claude', 'deepseek', 'grok'
    account_name: str         # Human-friendly label
    auth_profile: str         # Config path or CLI binary (e.g., '~/.codex2', 'agy2')
    priority: int = 1         # 1 = primary, 2 = secondary/backup, 3 = tertiary
    status: str = "ONLINE"    # 'ONLINE', 'DEGRADED', 'SLEEPING', 'OFFLINE'
    failure_count: int = 0
    max_failures: int = 3
    sleep_until: float = 0.0
    cooldown_seconds: float = 60.0
    total_invocations: int = 0
    successful_invocations: int = 0
    rolling_latency_ms: float = 250.0
    tokens_consumed: int = 0
    last_error: Optional[str] = None

    def is_available(self) -> bool:
        now = time.time()
        if self.status == "OFFLINE":
            return False
        if self.status == "SLEEPING":
            if now >= self.sleep_until:
                # Half-open probe: permit retry
                self.status = "ONLINE"
                self.failure_count = 0
                return True
            return False
        return True

class MultiAccountBroker:
    """
    Coordinates multi-account pools per AI provider with circuit breakers and failovers.
    """
    def __init__(self):
        self.accounts: Dict[str, ModelAccount] = {}
        self.activity_log: List[Dict[str, Any]] = []
        self._init_default_saori_pools()

    def _init_default_saori_pools(self):
        """Initializes default multi-account topology matching SAORI production configuration."""
        defaults = [
            # Google Antigravity Pool
            ModelAccount(
                id="antigravity-1",
                provider="antigravity",
                account_name="Antigravity Prime (Main)",
                auth_profile="agy",
                priority=1,
                rolling_latency_ms=320.0
            ),
            ModelAccount(
                id="antigravity-2",
                provider="antigravity",
                account_name="Antigravity Backup (Secondary)",
                auth_profile="agy2",
                priority=2,
                rolling_latency_ms=380.0
            ),

            # OpenAI Codex Pool
            ModelAccount(
                id="codex-1",
                provider="codex",
                account_name="Codex Terra (Primary)",
                auth_profile="~/.codex",
                priority=1,
                rolling_latency_ms=550.0
            ),
            ModelAccount(
                id="codex-2",
                provider="codex",
                account_name="Codex Luna (Backup / Fallback)",
                auth_profile="~/.codex2",
                priority=2,
                rolling_latency_ms=620.0
            ),

            # Anthropic Claude Pool
            ModelAccount(
                id="claude-1",
                provider="claude",
                account_name="Claude Sonnet/Opus (Deep Arch)",
                auth_profile="~/.claude",
                priority=1,
                rolling_latency_ms=850.0
            ),
            ModelAccount(
                id="claude-2",
                provider="claude",
                account_name="Claude Haiku (Fast SRE / Triage)",
                auth_profile="claude-haiku",
                priority=2,
                rolling_latency_ms=280.0
            ),

            # Specialized Models
            ModelAccount(
                id="deepseek-1",
                provider="deepseek",
                account_name="DeepSeek Coder (Math/AST)",
                auth_profile="deepseek-coder",
                priority=1,
                rolling_latency_ms=410.0
            ),
            ModelAccount(
                id="grok-1",
                provider="grok",
                account_name="Grok Code Sentinel",
                auth_profile="grok-beta",
                priority=1,
                rolling_latency_ms=450.0
            ),
        ]
        for acc in defaults:
            self.accounts[acc.id] = acc

    def register_account(self, account: ModelAccount):
        self.accounts[account.id] = account

    def acquire_account(self, provider: str) -> Optional[ModelAccount]:
        """
        Retrieves the best available account for a given provider.
        If primary is SLEEPING or OFFLINE, automatically fails over to secondary/backup.
        """
        candidates = [
            acc for acc in self.accounts.values()
            if acc.provider == provider and acc.is_available()
        ]
        if not candidates:
            # Check if any candidate exists in sleeping state to log circuit trip
            return None

        # Sort by priority (1 is best), then least failure_count, then latency
        candidates.sort(key=lambda a: (a.priority, a.failure_count, a.rolling_latency_ms))
        selected = candidates[0]
        selected.total_invocations += 1
        return selected

    def report_result(self, account_id: str, success: bool, latency_ms: float = 0.0,
                      tokens: int = 0, error: str = None) -> Dict[str, Any]:
        """
        Reports invocation outcome. Trips circuit breaker if failure threshold is reached.
        """
        account = self.accounts.get(account_id)
        if not account:
            return {"error": f"Account {account_id} not found"}

        now = time.time()
        if success:
            account.successful_invocations += 1
            account.failure_count = 0
            account.status = "ONLINE"
            account.tokens_consumed += tokens
            if latency_ms > 0:
                account.rolling_latency_ms = (account.rolling_latency_ms * 0.8) + (latency_ms * 0.2)
            return {"status": "ok", "account": account.id}
        else:
            account.failure_count += 1
            account.last_error = error or "Execution timeout or quota error"

            # Check if circuit breaker should trip
            if account.failure_count >= account.max_failures:
                account.status = "SLEEPING"
                account.sleep_until = now + account.cooldown_seconds
                failover_msg = (
                    f"[CIRCUIT BREAKER] Account {account.id} ({account.account_name}) reached "
                    f"{account.failure_count} failures. Sleeping until {account.cooldown_seconds}s. "
                    f"Failing over to secondary account."
                )
                self.activity_log.append({
                    "timestamp": now,
                    "event": "circuit_tripped",
                    "account_id": account.id,
                    "provider": account.provider,
                    "message": failover_msg
                })
                return {
                    "status": "circuit_tripped",
                    "account": account.id,
                    "sleep_seconds": account.cooldown_seconds,
                    "message": failover_msg
                }

            return {"status": "failure_recorded", "failures": account.failure_count}

    def get_pool_status(self) -> Dict[str, Any]:
        """Returns comprehensive status across all provider pools."""
        pools: Dict[str, List[Dict[str, Any]]] = {}
        now = time.time()

        for acc in self.accounts.values():
            if acc.provider not in pools:
                pools[acc.provider] = []

            sleeping_left = max(0.0, acc.sleep_until - now) if acc.status == "SLEEPING" else 0.0
            pools[acc.provider].append({
                "id": acc.id,
                "name": acc.account_name,
                "auth_profile": acc.auth_profile,
                "priority": acc.priority,
                "status": acc.status,
                "available": acc.is_available(),
                "sleeping_seconds_left": round(sleeping_left, 1),
                "failures": acc.failure_count,
                "invocations": acc.total_invocations,
                "success_rate": round(
                    (acc.successful_invocations / acc.total_invocations * 100)
                    if acc.total_invocations > 0 else 100.0, 1
                ),
                "latency_ms": round(acc.rolling_latency_ms, 1),
                "tokens_consumed": acc.tokens_consumed,
                "last_error": acc.last_error
            })

        return {
            "total_accounts": len(self.accounts),
            "providers": list(pools.keys()),
            "pools": pools,
            "recent_events": self.activity_log[-10:]
        }
