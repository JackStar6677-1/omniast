"""
SAORI Core & OmniAST Integration Bridge
Connects OmniAST Graph Kernel with SAORI SRE Engine, Multi-Account Model Broker,
and Shared Memory (ai_hub_memory on port 8077).
"""

import json
import urllib.request
import os
import sys
import time
from typing import Dict, Any, List, Optional

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from core.kernel.engine import OmniASTKernel
from sre.models.multi_account_broker import MultiAccountBroker

class SAORIOmniASTBridge:
    def __init__(self, memory_endpoint: str = "http://100.114.161.74:8077/mcp"):
        self.memory_endpoint = memory_endpoint
        self.kernel = OmniASTKernel()
        self.broker = MultiAccountBroker()

    def query_shared_memory(self, tema: str) -> Dict[str, Any]:
        """Queries ai_hub_memory for persisted knowledge or incident context."""
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "recuperar",
                "arguments": {"tema": tema}
            }
        }
        try:
            req = urllib.request.Request(
                self.memory_endpoint,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=3.0) as resp:
                res = json.loads(resp.read().decode("utf-8"))
                return res.get("result", {})
        except Exception as e:
            return {"error": f"Memory connection offline: {e}"}

    def record_shared_memory(self, tema: str, contenido: str) -> bool:
        """Records an incident resolution or architectural milestone into ai_hub_memory."""
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "recordar",
                "arguments": {"tema": tema, "contenido": contenido}
            }
        }
        try:
            req = urllib.request.Request(
                self.memory_endpoint,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=3.0) as resp:
                res = json.loads(resp.read().decode("utf-8"))
                return not res.get("isError", False)
        except Exception:
            return False

    def triage_incident_with_failover(self, incident_desc: str, provider: str = "codex") -> Dict[str, Any]:
        """
        Executes autonomous SRE triage selecting active account with automatic failover.
        """
        acc = self.broker.acquire_account(provider)
        if not acc:
            return {"status": "degraded", "message": "All accounts in pool currently sleeping."}

        # Simulated verified triage with account attribution
        return {
            "status": "triaged",
            "assigned_account": acc.id,
            "account_name": acc.account_name,
            "provider": acc.provider,
            "timestamp": time.time()
        }
