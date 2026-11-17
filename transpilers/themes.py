"""
OmniAST Pluggable UI Design Themes (v0.1.0)
Provides modular, modern, high-contrast design themes for OmniWeb apps:
- sovereign: Glassmorphism, Bento Grid, amethyst & cyan accents (Star / Nova signature)
- cyberpunk: High-tech neon cyan / matrix green, dark terminal aesthetics
- terminal: Retro phosphor amber / green CRT terminal UI
- minimal: Crisp, clean, enterprise documentation layout (Stripe / VitePress style)
"""

from typing import Dict, Any

THEMES: Dict[str, Dict[str, Any]] = {
    "sovereign": {
        "name": "Sovereign Glass",
        "description": "Star & Nova signature Glassmorphism with Bento Grid, radial glows, and amethyst accents.",
        "vars": """
      --bg-base: #070913;
      --bg: #070913;
      --surface: rgba(15, 23, 42, 0.85);
      --surface-hover: rgba(30, 41, 59, 0.92);
      --bg-surface: #0f172a;
      --bg-card: rgba(15, 23, 42, 0.82);
      --bg-card-hover: rgba(30, 41, 59, 0.92);
      --card: rgba(15, 23, 42, 0.82);
      --card-hover: rgba(30, 41, 59, 0.92);
      --border-color: rgba(255, 255, 255, 0.12);
      --border-accent: rgba(99, 102, 241, 0.45);
      --primary: #6366f1;
      --primary-glow: rgba(99, 102, 241, 0.35);
      --accent: #38bdf8;
      --accent-purple: #a855f7;
      --success: #10b981;
      --warning: #f59e0b;
      --danger: #ef4444;
      --text-main: #f8fafc;
      --text-muted: #cbd5e1;
      --text-dim: #94a3b8;
      --radius-sm: 8px;
      --radius-md: 14px;
      --radius-lg: 20px;
      --body-bg: #070913;
        """
    },
    "cyberpunk": {
        "name": "Cyberpunk Neon",
        "description": "High-contrast tactical hacker interface with electric cyan, neon magenta, and dark slate.",
        "vars": """
      --bg-base: #04060c;
      --bg: #04060c;
      --surface: rgba(10, 18, 38, 0.9);
      --surface-hover: rgba(18, 32, 68, 0.96);
      --bg-surface: #0a0f1d;
      --bg-card: rgba(10, 18, 38, 0.88);
      --bg-card-hover: rgba(18, 32, 68, 0.96);
      --card: rgba(10, 18, 38, 0.88);
      --card-hover: rgba(18, 32, 68, 0.96);
      --border-color: rgba(0, 240, 255, 0.25);
      --border-accent: #00f0ff;
      --primary: #00f0ff;
      --primary-glow: rgba(0, 240, 255, 0.45);
      --accent: #ff007f;
      --accent-purple: #9d00ff;
      --success: #00ff66;
      --warning: #ffe600;
      --danger: #ff003c;
      --text-main: #f0fdff;
      --text-muted: #93c5fd;
      --text-dim: #60a5fa;
      --radius-sm: 4px;
      --radius-md: 6px;
      --radius-lg: 10px;
      --body-bg: #04060c;
        """
    },
    "terminal": {
        "name": "Retro Terminal",
        "description": "Phosphor green CRT terminal with scanline accents and strict monospace typography.",
        "vars": """
      --bg-base: #060906;
      --bg: #060906;
      --surface: rgba(16, 26, 16, 0.9);
      --surface-hover: rgba(24, 38, 24, 0.96);
      --bg-surface: #101610;
      --bg-card: rgba(16, 26, 16, 0.88);
      --bg-card-hover: rgba(24, 38, 24, 0.96);
      --card: rgba(16, 26, 16, 0.88);
      --card-hover: rgba(24, 38, 24, 0.96);
      --border-color: rgba(34, 197, 94, 0.3);
      --border-accent: #22c55e;
      --primary: #22c55e;
      --primary-glow: rgba(34, 197, 94, 0.4);
      --accent: #4ade80;
      --accent-purple: #86efac;
      --success: #22c55e;
      --warning: #facc15;
      --danger: #f87171;
      --text-main: #f0fdf4;
      --text-muted: #86efac;
      --text-dim: #4ade80;
      --radius-sm: 0px;
      --radius-md: 2px;
      --radius-lg: 4px;
      --body-bg: #060906;
        """
    },
    "minimal": {
        "name": "Minimal Clean Doc",
        "description": "Crisp enterprise layout with soft borders, high legibility, and refined slate accents.",
        "vars": """
      --bg-base: #0b1120;
      --bg: #0b1120;
      --surface: rgba(30, 41, 59, 0.9);
      --surface-hover: rgba(51, 65, 85, 0.96);
      --bg-surface: #1e293b;
      --bg-card: rgba(30, 41, 59, 0.88);
      --bg-card-hover: rgba(51, 65, 85, 0.96);
      --card: rgba(30, 41, 59, 0.88);
      --card-hover: rgba(51, 65, 85, 0.96);
      --border-color: rgba(255, 255, 255, 0.15);
      --border-accent: #3b82f6;
      --primary: #3b82f6;
      --primary-glow: rgba(59, 130, 246, 0.3);
      --accent: #60a5fa;
      --accent-purple: #a855f7;
      --success: #10b981;
      --warning: #f59e0b;
      --danger: #ef4444;
      --text-main: #f8fafc;
      --text-muted: #e2e8f0;
      --text-dim: #94a3b8;
      --radius-sm: 6px;
      --radius-md: 10px;
      --radius-lg: 14px;
      --body-bg: #0b1120;
        """
    }
}

def get_theme_css(theme_name: str = "sovereign") -> str:
    key = theme_name.lower().strip()
    theme = THEMES.get(key, THEMES["sovereign"])
    return theme["vars"]
