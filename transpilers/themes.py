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
      --bg-base: #090d16;
      --bg-surface: #0f172a;
      --bg-card: rgba(30, 41, 59, 0.7);
      --bg-card-hover: rgba(51, 65, 85, 0.8);
      --border-color: rgba(255, 255, 255, 0.08);
      --border-accent: rgba(99, 102, 241, 0.35);
      --primary: #6366f1;
      --primary-glow: rgba(99, 102, 241, 0.25);
      --accent: #38bdf8;
      --accent-purple: #a855f7;
      --success: #10b981;
      --warning: #f59e0b;
      --danger: #ef4444;
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --text-dim: #64748b;
      --radius-sm: 8px;
      --radius-md: 14px;
      --radius-lg: 20px;
      --body-bg: radial-gradient(circle at 15% 15%, rgba(99, 102, 241, 0.12) 0%, transparent 40%), radial-gradient(circle at 85% 85%, rgba(56, 189, 248, 0.08) 0%, transparent 45%), #090d16;
        """
    },
    "cyberpunk": {
        "name": "Cyberpunk Neon",
        "description": "High-contrast tactical hacker interface with electric cyan, neon magenta, and dark slate.",
        "vars": """
      --bg-base: #05070e;
      --bg-surface: #0a0f1d;
      --bg-card: rgba(10, 18, 38, 0.85);
      --bg-card-hover: rgba(16, 28, 60, 0.95);
      --border-color: rgba(0, 240, 255, 0.2);
      --border-accent: #00f0ff;
      --primary: #00f0ff;
      --primary-glow: rgba(0, 240, 255, 0.4);
      --accent: #ff007f;
      --accent-purple: #9d00ff;
      --success: #00ff66;
      --warning: #ffe600;
      --danger: #ff003c;
      --text-main: #e0faff;
      --text-muted: #7ca5b8;
      --text-dim: #446577;
      --radius-sm: 4px;
      --radius-md: 6px;
      --radius-lg: 10px;
      --body-bg: linear-gradient(180deg, #05070e 0%, #080d1a 100%);
        """
    },
    "terminal": {
        "name": "Retro Terminal",
        "description": "Phosphor green CRT terminal with scanline accents and strict monospace typography.",
        "vars": """
      --bg-base: #0a0d0a;
      --bg-surface: #101610;
      --bg-card: #131a13;
      --bg-card-hover: #192419;
      --border-color: #1e331e;
      --border-accent: #22c55e;
      --primary: #22c55e;
      --primary-glow: rgba(34, 197, 94, 0.3);
      --accent: #4ade80;
      --accent-purple: #86efac;
      --success: #22c55e;
      --warning: #facc15;
      --danger: #f87171;
      --text-main: #f0fdf4;
      --text-muted: #86efac;
      --text-dim: #3f6248;
      --radius-sm: 0px;
      --radius-md: 2px;
      --radius-lg: 4px;
      --body-bg: #0a0d0a;
        """
    },
    "minimal": {
        "name": "Minimal Clean Doc",
        "description": "Crisp enterprise layout with soft borders, high legibility, and refined slate accents.",
        "vars": """
      --bg-base: #0f172a;
      --bg-surface: #1e293b;
      --bg-card: #1e293b;
      --bg-card-hover: #334155;
      --border-color: rgba(255, 255, 255, 0.12);
      --border-accent: #3b82f6;
      --primary: #3b82f6;
      --primary-glow: rgba(59, 130, 246, 0.2);
      --accent: #60a5fa;
      --accent-purple: #a855f7;
      --success: #10b981;
      --warning: #f59e0b;
      --danger: #ef4444;
      --text-main: #f8fafc;
      --text-muted: #cbd5e1;
      --text-dim: #64748b;
      --radius-sm: 6px;
      --radius-md: 10px;
      --radius-lg: 14px;
      --body-bg: #0f172a;
        """
    }
}

def get_theme_css(theme_name: str = "sovereign") -> str:
    key = theme_name.lower().strip()
    theme = THEMES.get(key, THEMES["sovereign"])
    return theme["vars"]
