#!/usr/bin/env python3
"""
OmniAST SRE Live Web Console & HTTP Server
Built with standard Python HTTP server (zero heavy dependencies) for maximum reliability.
Exposes real-time agent telemetry, incident triage, and interactive web dashboard.
"""

import sys
import os
import json
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

# Add parent path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from sre.swarm.orchestrator import SREOrchestrator

orchestrator = SREOrchestrator()

# Initialize demo user and seed incident
orchestrator.register_user("usr-jack", "JackStar", language="es", repos=["Odysseia", "Slimefun4-Drake", "ai-hub"])
orchestrator.submit_incident(
    user_id="usr-jack",
    repo="Odysseia",
    file_path="src/main/java/listeners/VoidSafety.java",
    issue_type="null_pointer_exception",
    severity="critical",
    raw_evidence="PlayerTeleportEvent triggered with null target world on chunk unload."
)

class SREWebHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Suppress noisy standard HTTP logs
        pass

    def do_GET(self):
        url = urlparse(self.path)
        path = url.path.rstrip("/") or "/"

        if path == "/" or path == "/dashboard":
            template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "dashboard.html")
            if os.path.exists(template_path):
                with open(template_path, "r", encoding="utf-8") as f:
                    content = f.read().encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
                return

        elif path == "/api/state":
            state = orchestrator.get_dashboard_state()
            data = json.dumps(state).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            return

        self.send_response(404)
        self.end_headers()

    def do_POST(self):
        url = urlparse(self.path)
        path = url.path.rstrip("/") or "/"

        if path == "/api/incidents/simulate":
            # Simulate real-time codebase triage and auto-repair
            inc_id = orchestrator.submit_incident(
                user_id="usr-jack",
                repo="Slimefun4-Drake",
                file_path="implementation/tasks/TickerTask.java",
                issue_type="concurrency_leak",
                severity="high",
                raw_evidence="Async energy balance task attempted synchronous inventory access."
            )
            # Instantly simulate auto-patching
            patch = "guard thread.is_async() -> schedule_sync_task()"
            orchestrator.apply_repair(inc_id, patch)

            resp = json.dumps({"ok": True, "incident_id": inc_id}).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(resp)))
            self.end_headers()
            self.wfile.write(resp)
            return

        self.send_response(404)
        self.end_headers()

def run_server(host="0.0.0.0", port=8089):
    server = ThreadingHTTPServer((host, port), SREWebHandler)
    print(f"[OMNIAST SRE] Live Web Console active on http://{host}:{port}/dashboard")
    server.serve_forever()

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8089
    run_server(port=port)
