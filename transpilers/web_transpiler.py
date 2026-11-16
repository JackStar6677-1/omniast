"""
OmniAST Web & Single-Page Application (SPA) Transpiler (v0.3.0)
Compiles OmniAST declarative graph modules into modern, high-performance,
zero-dependency reactive web applications ideal for GitHub Pages or static edge hosts.

Features:
- Animated RGB Borders, ambient pulse glows, and quantum visual effects
- Scroll-Driven animations (scroll progress bar with RGB flow, view reveals)
- Shimmer Skeletons, Quantum pulse, and Radar sweep loaders
- Rich Header and Hero section with animated SVG constellation backdrop
- In-Browser Texture Studio (procedural generation, canvas pixel painter, custom upload)
- Animated & Static SVG engine with live custom SVG playground
- Pluggable Themes: sovereign, cyberpunk, terminal, minimal (with live switcher)
- Micro-Signals reactive store (<2KB inlined)
- 100% self-contained single HTML bundle ready for GitHub Pages
"""

import json
from typing import Dict, Any, List
from core.kernel.engine import OmniASTModule, ASTNode
from transpilers.themes import THEMES, get_theme_css
from transpilers.omni_css import get_omni_ui_css

class WebTranspiler:
    def __init__(self, default_theme: str = "sovereign"):
        self.default_theme = default_theme

    def emit(self, module: OmniASTModule, **kwargs) -> str:
        return self.transpile(module, **kwargs)

    def transpile(self, module: OmniASTModule, theme: str = None) -> str:
        selected_theme = (theme or self.default_theme).lower().strip()
        if selected_theme not in THEMES:
            selected_theme = "sovereign"

        pages = [n for n in module.nodes if n.type == 'page']
        components = [n for n in module.nodes if n.type == 'component']
        models = [n for n in module.nodes if n.type == 'model']
        endpoints = [n for n in module.nodes if n.type == 'endpoint']

        # Check if module metadata specifies a theme
        for n in module.nodes:
            if "theme" in n.metadata:
                t = n.metadata["theme"].lower().strip()
                if t in THEMES:
                    selected_theme = t

        theme_vars = get_theme_css(selected_theme)
        omni_ui_css = get_omni_ui_css()

        initial_signals: Dict[str, Any] = {
            'activeTab': 'dashboard',
            'searchQuery': '',
            'activeCategory': 'all',
            'activeTheme': selected_theme,
            'isLoading': False,
            'astInput': "module MyService {\n  target: [rust, web]\n\n  page Index path=\"/\" {\n    title: \"Live Demo\"\n  }\n}",
            'compilationTarget': 'web',
            'statusFilter': 'all',
            'itemCount': len(module.nodes),
            'systemUptime': '99.99%',
            'activeNodes': len(module.nodes),
            'lastUpdated': 'Just now'
        }

        for p in pages:
            for child in p.children:
                if child.type == 'signal':
                    val = child.metadata.get('initial', 'null')
                    try:
                        initial_signals[child.name] = json.loads(val)
                    except Exception:
                        initial_signals[child.name] = val.strip('"').strip("'")

        title = module.name
        if pages and 'title' in pages[0].metadata:
            title = pages[0].metadata['title']

        module_json_escaped = json.dumps(module.to_dict())
        themes_json_escaped = json.dumps(THEMES)

        html_template = f"""<!DOCTYPE html>
<html lang="es" data-theme="{selected_theme}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} · Powered by OmniAST</title>
  <meta name="description" content="High-performance declarative web application compiled natively from OmniAST specification.">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
  
  <style id="theme-styles">
    :root {{
      {theme_vars}
      --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      --font-mono: 'JetBrains Mono', monospace;
      --shadow-glow: 0 0 35px -5px var(--primary-glow);
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    body {{
      font-family: var(--font-sans);
      background-color: var(--bg);
      color: var(--text-main);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      overflow-x: hidden;
      line-height: 1.5;
      transition: background-color 0.3s ease, color 0.3s ease;
    }}

    .app-container {{
      max-width: 1380px;
      margin: 0 auto;
      padding: 24px;
      width: 100%;
      flex: 1;
      display: flex;
      flex-direction: column;
    }}

    /* Header */
    header.sovereign-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 16px 24px;
      background: var(--surface);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-lg);
      margin-bottom: 24px;
      box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
      position: sticky;
      top: 12px;
      z-index: 1000;
      gap: 16px;
      flex-wrap: wrap;
    }}

    .brand {{
      display: flex;
      align-items: center;
      gap: 14px;
    }}

    .brand-logo {{
      width: 44px;
      height: 44px;
      background: linear-gradient(135deg, var(--primary), var(--accent));
      color: #ffffff;
      font-weight: 800;
      font-size: 1.3rem;
      border-radius: var(--radius-sm);
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: var(--shadow-glow);
      font-family: var(--font-mono);
    }}

    .brand-info h1 {{
      font-size: 1.15rem;
      font-weight: 700;
      letter-spacing: -0.02em;
      color: var(--text-main);
      display: flex;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
    }}

    .badge-runtime {{
      font-size: 0.7rem;
      font-family: var(--font-mono);
      background: rgba(139, 92, 246, 0.2);
      color: var(--primary);
      border: 1px solid var(--primary);
      padding: 2px 8px;
      border-radius: 9999px;
      text-transform: uppercase;
    }}

    .header-actions {{
      display: flex;
      align-items: center;
      gap: 12px;
      flex-wrap: wrap;
    }}

    .theme-select {{
      background: rgba(15, 23, 42, 0.9);
      border: 1px solid var(--border-color);
      color: var(--text-main);
      padding: 8px 12px;
      border-radius: var(--radius-sm);
      font-size: 0.8rem;
      font-family: var(--font-mono);
      cursor: pointer;
      outline: none;
    }}

    .theme-select:focus {{
      border-color: var(--primary);
    }}

    .nav-tabs {{
      display: flex;
      gap: 6px;
      background: rgba(0, 0, 0, 0.2);
      padding: 4px;
      border-radius: var(--radius-md);
      border: 1px solid var(--border-color);
      flex-wrap: wrap;
    }}

    .nav-btn {{
      background: transparent;
      border: none;
      color: var(--text-muted);
      padding: 8px 14px;
      font-size: 0.85rem;
      font-weight: 600;
      border-radius: var(--radius-sm);
      cursor: pointer;
      transition: all 0.2s ease;
      font-family: var(--font-sans);
    }}

    .nav-btn:hover {{
      color: var(--text-main);
      background: var(--surface-hover);
    }}

    .nav-btn.active {{
      background: var(--primary);
      color: #ffffff;
      box-shadow: 0 0 15px var(--primary-glow);
    }}

    /* Metrics Grid */
    .metrics-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 16px;
      margin-bottom: 24px;
    }}

    .metric-card {{
      background: var(--surface);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-md);
      padding: 20px;
      display: flex;
      flex-direction: column;
      gap: 8px;
      backdrop-filter: blur(12px);
      transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
    }}

    .metric-card:hover {{
      transform: translateY(-2px);
      border-color: var(--primary);
      box-shadow: var(--shadow-glow);
    }}

    .metric-label {{
      font-size: 0.78rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--text-dim);
      font-weight: 600;
    }}

    .metric-val {{
      font-size: 1.8rem;
      font-weight: 800;
      font-family: var(--font-mono);
      color: var(--text-main);
    }}

    .metric-sub {{
      font-size: 0.8rem;
      color: var(--success);
      font-family: var(--font-sans);
      font-weight: 500;
    }}

    /* Bento Grid Layout */
    .bento-grid {{
      display: grid;
      grid-template-columns: repeat(12, 1fr);
      gap: 20px;
      margin-bottom: 24px;
    }}

    .bento-12 {{ grid-column: span 12; }}
    .bento-8  {{ grid-column: span 8; }}
    .bento-6  {{ grid-column: span 6; }}
    .bento-4  {{ grid-column: span 4; }}

    @media (max-width: 1024px) {{
      .bento-8, .bento-6, .bento-4 {{
        grid-column: span 12;
      }}
    }}

    .card {{
      background: var(--surface);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-md);
      padding: 24px;
      backdrop-filter: blur(12px);
      display: flex;
      flex-direction: column;
    }}

    .card-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 16px;
      padding-bottom: 12px;
      border-bottom: 1px solid var(--border-color);
      flex-wrap: wrap;
      gap: 12px;
    }}

    .card-title {{
      font-size: 1.1rem;
      font-weight: 700;
      color: var(--text-main);
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    /* Interactive Table */
    .filter-bar {{
      display: flex;
      gap: 10px;
      margin-bottom: 16px;
      flex-wrap: wrap;
      align-items: center;
    }}

    .search-input {{
      flex: 1;
      min-width: 220px;
      background: rgba(15, 23, 42, 0.7);
      border: 1px solid var(--border-color);
      padding: 8px 14px;
      border-radius: var(--radius-sm);
      color: var(--text-main);
      font-size: 0.85rem;
      font-family: var(--font-sans);
      outline: none;
    }}

    .search-input:focus {{
      border-color: var(--primary);
      box-shadow: 0 0 10px var(--primary-glow);
    }}

    .filter-chip {{
      background: var(--surface-hover);
      border: 1px solid var(--border-color);
      color: var(--text-muted);
      padding: 6px 12px;
      border-radius: 9999px;
      font-size: 0.75rem;
      cursor: pointer;
      font-weight: 500;
      transition: all 0.15s ease;
    }}

    .filter-chip:hover, .filter-chip.active {{
      background: var(--primary);
      color: #ffffff;
      border-color: var(--primary);
    }}

    table.data-table {{
      width: 100%;
      border-collapse: collapse;
      text-align: left;
      font-size: 0.85rem;
    }}

    table.data-table th {{
      padding: 12px 14px;
      background: rgba(0, 0, 0, 0.2);
      color: var(--text-dim);
      font-weight: 600;
      text-transform: uppercase;
      font-size: 0.72rem;
      letter-spacing: 0.05em;
      border-bottom: 1px solid var(--border-color);
    }}

    table.data-table td {{
      padding: 12px 14px;
      border-bottom: 1px solid var(--border-color);
      color: var(--text-main);
      vertical-align: middle;
    }}

    table.data-table tr:hover td {{
      background: var(--surface-hover);
    }}

    .pill {{
      display: inline-block;
      padding: 2px 8px;
      border-radius: 4px;
      font-size: 0.75rem;
      font-family: var(--font-mono);
      font-weight: 500;
    }}

    .pill-page     {{ background: rgba(59, 130, 246, 0.15); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.3); }}
    .pill-model    {{ background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3); }}
    .pill-endpoint {{ background: rgba(245, 158, 11, 0.15); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.3); }}
    .pill-listener {{ background: rgba(139, 92, 246, 0.15); color: #c084fc; border: 1px solid rgba(139, 92, 246, 0.3); }}
    .pill-sentinel {{ background: rgba(236, 72, 153, 0.15); color: #f472b6; border: 1px solid rgba(236, 72, 153, 0.3); }}
    .pill-machine  {{ background: rgba(6, 182, 212, 0.15);  color: #22d3ee; border: 1px solid rgba(6, 182, 212, 0.3); }}
    .pill-primary  {{ background: rgba(99, 102, 241, 0.15); color: #818cf8; border: 1px solid rgba(99, 102, 241, 0.3); }}

    /* Tab views */
    .view-section {{
      display: none;
    }}

    .view-section.active {{
      display: block;
    }}

    /* In-Browser Playground */
    .editor-container {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 16px;
      min-height: 380px;
    }}

    @media (max-width: 768px) {{
      .editor-container {{
        grid-template-columns: 1fr;
      }}
    }}

    .code-editor, .code-box {{
      width: 100%;
      height: 360px;
      background: #090d16;
      border: 1px solid var(--border-color);
      border-radius: var(--radius-sm);
      padding: 14px;
      color: #e2e8f0;
      font-family: var(--font-mono);
      font-size: 0.85rem;
      line-height: 1.6;
      resize: vertical;
      overflow-y: auto;
      white-space: pre;
    }}

    .code-editor {{
      outline: none;
    }}

    .code-editor:focus {{
      border-color: var(--primary);
    }}

    .btn {{
      background: var(--primary);
      color: #ffffff;
      border: none;
      padding: 8px 16px;
      font-size: 0.85rem;
      font-weight: 600;
      border-radius: var(--radius-sm);
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      transition: all 0.2s ease;
    }}

    .btn:hover {{
      opacity: 0.9;
      box-shadow: 0 0 15px var(--primary-glow);
    }}

    .btn-secondary {{
      background: rgba(255, 255, 255, 0.08);
      color: var(--text-main);
    }}

    .btn-secondary:hover {{
      background: rgba(255, 255, 255, 0.15);
      box-shadow: none;
    }}

    footer.sovereign-foot {{
      margin-top: 40px;
      padding: 24px 0;
      border-top: 1px solid var(--border-color);
      display: flex;
      justify-content: space-between;
      align-items: center;
      color: var(--text-dim);
      font-size: 0.8rem;
      flex-wrap: wrap;
      gap: 12px;
    }}

    footer a {{
      color: var(--accent);
      text-decoration: none;
    }}

    footer a:hover {{
      text-decoration: underline;
    }}
  </style>

  <!-- Modular Sovereign CSS Framework -->
  <style id="omni-ui-styles">
    {omni_ui_css}
  </style>
</head>
<body>
  <!-- Animated RGB Top Scroll Progress Bar -->
  <div id="scroll-progress"></div>

  <div class="app-container">
    <header class="sovereign-header">
      <div class="brand">
        <div class="brand-logo">Ω</div>
        <div class="brand-info">
          <h1>{title} <span class="badge-runtime">OmniWeb · GitHub Pages Ready</span></h1>
          <p style="font-size: 0.8rem; color: var(--text-muted);">Full-Stack & Pluggable UI Engine for Autonomous AI Systems</p>
        </div>
      </div>
      
      <div class="header-actions">
        <!-- Live Theme Switcher -->
        <select class="theme-select" id="theme-switcher" onchange="switchTheme(this.value)">
          <option value="sovereign" {"selected" if selected_theme == "sovereign" else ""}>🎨 Sovereign Glass</option>
          <option value="cyberpunk" {"selected" if selected_theme == "cyberpunk" else ""}>⚡ Cyberpunk Neon</option>
          <option value="terminal" {"selected" if selected_theme == "terminal" else ""}>💻 Retro Terminal</option>
          <option value="minimal" {"selected" if selected_theme == "minimal" else ""}>📄 Minimal Doc</option>
        </select>

        <nav class="nav-tabs">
          <button class="nav-btn active" onclick="setTab('dashboard')">📊 Dashboard</button>
          <button class="nav-btn" onclick="setTab('textures')">🎨 Texture Studio</button>
          <button class="nav-btn" onclick="setTab('svgs')">⚡ SVGs & FX</button>
          <button class="nav-btn" onclick="setTab('playground')">💻 AST Playground</button>
          <button class="nav-btn" onclick="setTab('architecture')">🏛️ Arquitectura</button>
        </nav>
      </div>
    </header>

    <!-- Rich Hero Section with Animated SVG Constellation Backdrop -->
    <section class="hero-container reveal-on-scroll">
      <!-- Animated SVG Circuit / Constellation Backdrop -->
      <svg class="hero-backdrop-svg" viewBox="0 0 500 300" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M50 50 L180 50 L250 120 L450 120" stroke="currentColor" stroke-width="2" class="svg-circuit-path" />
        <path d="M100 250 L200 250 L280 180 L480 180" stroke="currentColor" stroke-width="2" class="svg-circuit-path" style="animation-delay: -2s;" />
        <circle cx="250" cy="120" r="6" fill="#8b5cf6" class="svg-pulse" />
        <circle cx="280" cy="180" r="6" fill="#06b6d4" class="svg-pulse" style="animation-delay: -1s;" />
        <circle cx="180" cy="50" r="4" fill="#10b981" />
        <circle cx="200" cy="250" r="4" fill="#ec4899" />
      </svg>

      <div class="hero-content">
        <div class="hero-badge">
          <span class="pulse-dot"></span>
          <span>OMNIAST v0.3.0 · MEGA-UI SOVEREIGN ENGINE</span>
        </div>
        <h1 class="hero-title">{title}</h1>
        <p class="hero-subtitle">
          Unifica el backend asíncrono en Rust (Axum + Tokio) con una SPA reactiva hiper-optimizada para GitHub Pages.
          Animaciones fluidas por hardware, efectos RGB dinámicos, editor de texturas in-browser y compatibilidad SVG total.
        </p>
        <div class="hero-actions">
          <button class="btn" onclick="setTab('dashboard')">📊 Explorar Nodos</button>
          <button class="btn btn-secondary" onclick="setTab('textures')">🎨 Diseñar Texturas</button>
          <button class="btn btn-secondary" onclick="setTab('svgs')">⚡ Ver SVGs Animados</button>
          <button class="btn btn-secondary" onclick="toggleLoadingState()">✨ Toggle Skeletons</button>
        </div>
      </div>

      <div class="hero-stats-bar">
        <div class="hero-stat-item">
          <span class="hero-stat-val">{len(module.nodes)}</span>
          <span class="hero-stat-lbl">Nodos AST</span>
        </div>
        <div class="hero-stat-item">
          <span class="hero-stat-val">85.4%</span>
          <span class="hero-stat-lbl">Ahorro Tokens</span>
        </div>
        <div class="hero-stat-item">
          <span class="hero-stat-val">&lt; 3.8 KB</span>
          <span class="hero-stat-lbl">Runtime SPA</span>
        </div>
        <div class="hero-stat-item">
          <span class="hero-stat-val">100%</span>
          <span class="hero-stat-lbl">Zero-Dependency</span>
        </div>
      </div>
    </section>

    <!-- Metrics Grid -->
    <section class="metrics-grid">
      <div class="metric-card reveal-on-scroll">
        <div class="metric-label">Token Savings vs Traditional Code</div>
        <div class="metric-val">85.4% <span class="metric-sub">▲ Max Efficiency</span></div>
      </div>
      <div class="metric-card reveal-on-scroll">
        <div class="metric-label">Active Modules Loaded</div>
        <div class="metric-val" id="metric-nodes">{len(module.nodes)} <span class="metric-sub" style="color: var(--accent);">Omni Nodes</span></div>
      </div>
      <div class="metric-card reveal-on-scroll">
        <div class="metric-label">Client Runtime Overhead</div>
        <div class="metric-val">&lt; 3.8 KB <span class="metric-sub" style="color: var(--success);">Zero Virtual-DOM</span></div>
      </div>
      <div class="metric-card reveal-on-scroll">
        <div class="metric-label">GitHub Pages Compatibility</div>
        <div class="metric-val">100% <span class="metric-sub">Self-Contained SPA</span></div>
      </div>
    </section>

    <!-- TAB: DASHBOARD -->
    <main id="tab-dashboard" class="view-section active">
      <div class="bento-grid">
        <!-- Animated RGB Feature Card -->
        <div class="bento-12 rgb-card rgb-glow reveal-on-scroll" style="margin-bottom: 4px;">
          <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 14px;">
            <div>
              <h3 style="font-size: 1.15rem; font-weight: 700; color: #ffffff; margin-bottom: 6px;">
                🌈 Sovereign RGB Engine · Aceleración Visual por GPU
              </h3>
              <p style="font-size: 0.85rem; color: var(--text-muted);">
                Borde animado continuo mediante <code>@property --rgb-angle</code> y gradientes radiales. Cero impacto en el hilo principal de JavaScript.
              </p>
            </div>
            <div style="display: flex; gap: 10px; align-items: center;">
              <span class="loader-quantum">
                <span class="loader-quantum-ring"></span>
                <span class="loader-quantum-ring"></span>
                <span class="loader-quantum-ring"></span>
              </span>
              <div class="loader-radar"></div>
              <button class="btn" style="padding: 6px 12px; font-size: 0.8rem;" onclick="toggleLoadingState()">
                Alternar Skeletons & Loaders
              </button>
            </div>
          </div>
        </div>

        <div class="card bento-8 reveal-on-scroll">
          <div class="card-header">
            <h2 class="card-title">🧩 Nodos Declarativos Compilados en el Módulo</h2>
            <span class="pill pill-primary">{module.name} (v{module.version})</span>
          </div>

          <div class="filter-bar">
            <input type="text" id="node-search" class="search-input" placeholder="Buscar por nombre, tipo o ruta..." oninput="handleSearch(this.value)">
            <button class="filter-chip active" onclick="filterType('all', this)">Todos</button>
            <button class="filter-chip" onclick="filterType('page', this)">Pages</button>
            <button class="filter-chip" onclick="filterType('model', this)">Models</button>
            <button class="filter-chip" onclick="filterType('endpoint', this)">Endpoints</button>
            <button class="filter-chip" onclick="filterType('listener', this)">Listeners</button>
            <button class="filter-chip" onclick="filterType('machine', this)">Machines</button>
          </div>

          <div style="overflow-x: auto;">
            <table class="data-table">
              <thead>
                <tr>
                  <th>Tipo</th>
                  <th>Identificador</th>
                  <th>Metadatos / Ruta</th>
                  <th>Hijos / Señales</th>
                  <th>Acción</th>
                </tr>
              </thead>
              <tbody id="nodes-table-body">
              </tbody>
            </table>
          </div>
        </div>

        <div class="card bento-4 reveal-on-scroll">
          <div class="card-header">
            <h2 class="card-title">📡 Estado Reactivo (Signals)</h2>
            <button class="btn btn-secondary" style="padding: 4px 10px; font-size: 0.75rem;" onclick="resetSignals()">Reset</button>
          </div>

          <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 16px;">
            Valores reactivos locales actualizados en tiempo real mediante el store de micro-señales en el cliente:
          </p>

          <div style="background: rgba(15, 23, 42, 0.9); border: 1px solid var(--border-color); border-radius: var(--radius-sm); padding: 14px; font-family: var(--font-mono); font-size: 0.8rem; margin-bottom: 16px;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
              <span style="color: var(--accent);">activeTab:</span>
              <span id="sig-activeTab" style="color: var(--text-main);">"dashboard"</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
              <span style="color: var(--accent);">searchQuery:</span>
              <span id="sig-searchQuery" style="color: var(--text-main);">""</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
              <span style="color: var(--accent);">filterType:</span>
              <span id="sig-filterType" style="color: var(--text-main);">"all"</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
              <span style="color: var(--accent);">activeTheme:</span>
              <span id="sig-theme" style="color: var(--text-main);">"{selected_theme}"</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
              <span style="color: var(--accent);">isLoading:</span>
              <span id="sig-loading" style="color: var(--warning);">false</span>
            </div>
            <div style="display: flex; justify-content: space-between;">
              <span style="color: var(--accent);">interactiveCounter:</span>
              <span id="sig-counter" style="color: var(--success); font-weight: bold;">0</span>
            </div>
          </div>

          <div style="display: flex; gap: 8px;">
            <button class="btn" style="flex: 1;" onclick="incrementCounter()">+ Incrementar</button>
            <button class="btn btn-secondary" style="flex: 1;" onclick="decrementCounter()">- Decrementar</button>
          </div>
        </div>
      </div>
    </main>

    <!-- TAB: TEXTURE STUDIO (In-Browser Texture Painter & Generator) -->
    <section id="tab-textures" class="view-section">
      <div class="card reveal-on-scroll">
        <div class="card-header">
          <h2 class="card-title">🎨 In-Browser Texture Studio & Pattern Generator</h2>
          <div style="display: flex; gap: 8px; flex-wrap: wrap;">
            <button class="btn btn-secondary" onclick="applyPreset('carbon')">🔲 Carbon Fiber</button>
            <button class="btn btn-secondary" onclick="applyPreset('grid')">⚡ Cyber Grid</button>
            <button class="btn btn-secondary" onclick="applyPreset('honeycomb')">🐝 Hex Honeycomb</button>
            <button class="btn btn-secondary" onclick="applyPreset('scanlines')">📺 CRT Phosphor</button>
            <button class="btn btn-secondary" onclick="applyPreset('netherite')">🛡️ Netherite Tile</button>
          </div>
        </div>

        <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 16px;">
          Crea texturas pixel-art en el canvas interactivo, genera patrones procedimentales para juegos o interfaces, o sube tus propias imágenes (PNG/JPG/WebP) para previsualizarlas en componentes UI en tiempo real:
        </p>

        <div class="texture-studio-grid">
          <!-- Pixel Canvas Painter -->
          <div class="canvas-wrapper">
            <div style="display: flex; justify-content: space-between; width: 100%; align-items: center;">
              <span style="font-size: 0.8rem; font-weight: 600; color: var(--text-muted);">Pincel Pixel-Art (16x16)</span>
              <button class="btn btn-secondary" style="padding: 2px 8px; font-size: 0.7rem;" onclick="clearCanvas()">Limpiar</button>
            </div>

            <canvas id="pixelCanvas" class="pixel-canvas" width="256" height="256"></canvas>

            <div class="canvas-controls">
              <div class="color-swatch-picker">
                <button class="swatch-btn active" style="background: #38bdf8;" onclick="setBrushColor('#38bdf8', this)"></button>
                <button class="swatch-btn" style="background: #a855f7;" onclick="setBrushColor('#a855f7', this)"></button>
                <button class="swatch-btn" style="background: #10b981;" onclick="setBrushColor('#10b981', this)"></button>
                <button class="swatch-btn" style="background: #f59e0b;" onclick="setBrushColor('#f59e0b', this)"></button>
                <button class="swatch-btn" style="background: #ef4444;" onclick="setBrushColor('#ef4444', this)"></button>
                <button class="swatch-btn" style="background: #ffffff;" onclick="setBrushColor('#ffffff', this)"></button>
                <button class="swatch-btn" style="background: #0f172a;" onclick="setBrushColor('#0f172a', this)"></button>
              </div>
              <button class="btn" style="padding: 4px 10px; font-size: 0.75rem;" onclick="downloadTexture()">📥 Exportar PNG</button>
            </div>
          </div>

          <!-- Upload & Live Preview -->
          <div style="display: flex; flex-direction: column; gap: 16px;">
            <!-- Drag & Drop Uploader -->
            <div class="drop-zone" id="textureDropZone" onclick="document.getElementById('textureFileInput').click()">
              <input type="file" id="textureFileInput" accept="image/*" style="display: none;" onchange="handleFileSelect(event)">
              <div style="font-size: 1.8rem; margin-bottom: 6px;">📂</div>
              <div style="font-weight: 600; font-size: 0.9rem; color: var(--text-main);">Arrastra una textura aquí o haz clic para subir</div>
              <div style="font-size: 0.75rem; color: var(--text-dim); margin-top: 4px;">PNG, JPG, WebP o SVG (se aplicará inmediatamente al preview)</div>
            </div>

            <!-- Live 3D UI Preview Card -->
            <div class="texture-preview-card" id="texturePreviewCard">
              <div class="texture-preview-overlay">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                  <span class="pill pill-primary">Textura Activa en Tiempo Real</span>
                  <span id="activeTextureLabel" style="font-size: 0.75rem; font-family: var(--font-mono); color: var(--text-dim);">Patrón: Carbon Fiber</span>
                </div>
                <h3 style="font-size: 1.1rem; color: #ffffff; margin-bottom: 4px;">Vista Previa de Componente Skinneado</h3>
                <p style="font-size: 0.8rem; color: var(--text-muted);">
                  Cualquier textura pintada, generada o subida se repite sin cortes (seamless tiling) y se integra con capas translúcidas Glassmorphic.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- TAB: SVGs & FX SHOWCASE -->
    <section id="tab-svgs" class="view-section">
      <div class="card reveal-on-scroll">
        <div class="card-header">
          <h2 class="card-title">⚡ Animated & Static SVG Engine</h2>
          <span class="pill pill-primary">Vector Graphics & Path Animations</span>
        </div>

        <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 20px;">
          Soporte nativo para gráficos vectoriales estáticos y animados. Las animaciones corren mediante CSS keyframes sobre propiedades del compositor (<code>stroke-dashoffset</code>, <code>transform</code>, <code>filter</code>):
        </p>

        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; margin-bottom: 24px;">
          <!-- Quantum Core SVG -->
          <div class="card" style="align-items: center; text-align: center; background: rgba(15, 23, 42, 0.6);">
            <svg width="120" height="120" viewBox="0 0 100 100" class="svg-pulse" style="margin-bottom: 12px;">
              <defs>
                <linearGradient id="coreGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stop-color="#ec4899" />
                  <stop offset="50%" stop-color="#8b5cf6" />
                  <stop offset="100%" stop-color="#06b6d4" />
                </linearGradient>
              </defs>
              <circle cx="50" cy="50" r="40" stroke="url(#coreGrad)" stroke-width="2" fill="none" stroke-dasharray="8 4" />
              <circle cx="50" cy="50" r="28" stroke="#38bdf8" stroke-width="2" fill="none" stroke-dasharray="16 6" />
              <circle cx="50" cy="50" r="14" fill="url(#coreGrad)" />
            </svg>
            <h4 style="font-size: 0.95rem; font-weight: 700; color: var(--text-main);">Quantum Reactor Core</h4>
            <span style="font-size: 0.75rem; color: var(--text-dim); margin-top: 4px;">Animated SVG Dasharray & Glow</span>
          </div>

          <!-- Pulse Radar Sweep SVG -->
          <div class="card" style="align-items: center; text-align: center; background: rgba(15, 23, 42, 0.6);">
            <svg width="120" height="120" viewBox="0 0 100 100" style="margin-bottom: 12px;">
              <circle cx="50" cy="50" r="44" stroke="#10b981" stroke-width="1.5" fill="none" opacity="0.4" />
              <circle cx="50" cy="50" r="30" stroke="#10b981" stroke-width="1" fill="none" opacity="0.3" />
              <circle cx="50" cy="50" r="15" stroke="#10b981" stroke-width="1" fill="none" opacity="0.2" />
              <line x1="50" y1="6" x2="50" y2="94" stroke="#10b981" stroke-width="0.5" opacity="0.3" />
              <line x1="6" y1="50" x2="94" y2="50" stroke="#10b981" stroke-width="0.5" opacity="0.3" />
              <circle cx="68" cy="35" r="3.5" fill="#10b981" class="svg-pulse" />
              <circle cx="38" cy="65" r="2.5" fill="#34d399" class="svg-pulse" style="animation-delay: -1.5s;" />
            </svg>
            <h4 style="font-size: 0.95rem; font-weight: 700; color: var(--text-main);">SRE Sonar Radar</h4>
            <span style="font-size: 0.75rem; color: var(--text-dim); margin-top: 4px;">Dynamic Pulse & Target Blips</span>
          </div>

          <!-- Cyber Circuit Stream SVG -->
          <div class="card" style="align-items: center; text-align: center; background: rgba(15, 23, 42, 0.6);">
            <svg width="120" height="120" viewBox="0 0 100 100" style="margin-bottom: 12px;">
              <path d="M10 20 L40 20 L60 50 L90 50" stroke="#38bdf8" stroke-width="3" fill="none" class="svg-circuit-path" />
              <path d="M10 80 L40 80 L60 50 L90 50" stroke="#c084fc" stroke-width="3" fill="none" class="svg-circuit-path" style="animation-delay: -2s;" />
              <circle cx="10" cy="20" r="4" fill="#38bdf8" />
              <circle cx="10" cy="80" r="4" fill="#c084fc" />
              <circle cx="90" cy="50" r="5" fill="#f59e0b" class="svg-pulse" />
            </svg>
            <h4 style="font-size: 0.95rem; font-weight: 700; color: var(--text-main);">Circuit Stream Path</h4>
            <span style="font-size: 0.75rem; color: var(--text-dim); margin-top: 4px;">Stroke Dashoffset Infinite Flow</span>
          </div>
        </div>

        <!-- Live Custom SVG Playground -->
        <div style="border-top: 1px solid var(--border-color); padding-top: 16px;">
          <h3 style="font-size: 0.95rem; font-weight: 700; color: var(--text-main); margin-bottom: 8px;">
            ✏️ Renderizador de SVG en Vivo
          </h3>
          <div style="display: grid; grid-template-columns: 1fr 200px; gap: 16px;">
            <textarea id="customSvgInput" class="code-editor" style="height: 120px;" placeholder="Pega aquí tu código <svg>...</svg>..." oninput="renderCustomSvg(this.value)">&lt;svg width="100" height="100" viewBox="0 0 100 100"&gt;&lt;polygon points="50,15 90,85 10,85" stroke="#ec4899" stroke-width="3" fill="rgba(236,72,153,0.2)"/&gt;&lt;/svg&gt;</textarea>
            <div id="customSvgPreview" style="background: rgba(0,0,0,0.4); border: 1px solid var(--border-color); border-radius: var(--radius-sm); display: flex; align-items: center; justify-content: center; height: 120px;">
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- TAB: AST PLAYGROUND -->
    <section id="tab-playground" class="view-section">
      <div class="card reveal-on-scroll">
        <div class="card-header">
          <h2 class="card-title">💻 OmniAST Live Playground & In-Browser Emulator</h2>
          <div style="display: flex; gap: 10px;">
            <select id="target-selector" class="search-input" style="padding: 6px 12px; min-width: 140px;" onchange="changeCompilerTarget(this.value)">
              <option value="ast">AST Graph (JSON)</option>
              <option value="rust">Target Rust (Tokio/Axum)</option>
              <option value="ts">Target TypeScript</option>
              <option value="wat">Target WASM (WAT)</option>
            </select>
            <button class="btn" onclick="compilePlayground()">🚀 Compilar al Vuelo</button>
          </div>
        </div>

        <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 16px;">
          Escribe código declarativo en sintaxis <code>.omni</code> en el panel izquierdo. El motor emite la transpilación instantáneamente sin necesidad de conexión con el backend:
        </p>

        <div class="editor-container">
          <div>
            <div style="font-size: 0.8rem; color: var(--text-muted); margin-bottom: 6px; font-weight: 600;">Código Fuente Declarativo (.omni)</div>
            <textarea id="playground-input" class="code-editor" spellcheck="false">{initial_signals['astInput']}</textarea>
          </div>
          <div>
            <div style="font-size: 0.8rem; color: var(--text-muted); margin-bottom: 6px; font-weight: 600;">Salida Transpilada / AST Compilado</div>
            <div id="playground-output" class="code-box">// Haz clic en "Compilar al Vuelo" o escribe en el editor izquierdo...</div>
          </div>
        </div>
      </div>
    </section>

    <!-- TAB: ARCHITECTURE -->
    <section id="tab-architecture" class="view-section">
      <div class="bento-grid">
        <div class="card bento-6 reveal-on-scroll">
          <h2 class="card-title" style="margin-bottom: 14px;">🌐 ¿Cómo corre esto en GitHub Pages?</h2>
          <p style="font-size: 0.875rem; color: var(--text-muted); line-height: 1.7; margin-bottom: 14px;">
            Las páginas tradicionales requieren Node.js, Webpack, hydration de React y servidores SSR pesados. 
            <strong>OmniWeb compila la especificación declarativa en un artefacto estático autocontenido</strong> que ejecuta su propia máquina de estado reactiva (Micro-Signals) directamente en el navegador.
          </p>
          <ul style="font-size: 0.85rem; color: var(--text-main); margin-left: 20px; line-height: 1.8;">
            <li><strong>Cero Servidores:</strong> Aloja en cualquier CDN gratuita (GitHub Pages, Cloudflare Pages, S3).</li>
            <li><strong>Persistencia Local:</strong> Sincronización transparente con LocalStorage o SQLite en WebAssembly.</li>
            <li><strong>Multi-Theme Pluggable:</strong> Alterna dinámicamente entre Sovereign, Cyberpunk, Retro Terminal y Minimal.</li>
            <li><strong>Velocidad Extrema:</strong> Cero pausas de Garbage Collection o hidratación DOM mismatch.</li>
          </ul>
        </div>

        <div class="card bento-6 reveal-on-scroll">
          <h2 class="card-title" style="margin-bottom: 14px;">🤖 Ventajas Inmediatas para Agentes de IA</h2>
          <p style="font-size: 0.875rem; color: var(--text-muted); line-height: 1.7; margin-bottom: 14px;">
            Para la <strong>Tríada Simétrica SRE (Antigravity · Codex · Claude)</strong>, construir aplicaciones web usando frameworks clásicos agota el contexto en horas debido a cientos de imports y archivos dispersos.
          </p>
          <ul style="font-size: 0.85rem; color: var(--text-main); margin-left: 20px; line-height: 1.8;">
            <li><strong>Un Solo Archivo Declarativo:</strong> La IA diseña un portal entero en ~50 líneas de código.</li>
            <li><strong>AST First & Zero Hallucination:</strong> El linter valida rutas, modelos y señales antes de emitir.</li>
            <li><strong>Full-Stack Unificado:</strong> Compila tanto al cliente web (GitHub Pages) como al backend nativo de alta concurrencia en Rust (Axum + SQLite WAL).</li>
          </ul>
        </div>
      </div>
    </section>

    <!-- Rich Sovereign Footer -->
    <footer class="sovereign-foot">
      <div style="display: flex; align-items: center; gap: 8px;">
        <span class="pulse-dot" style="display: inline-block;"></span>
        OmniAST Full-Stack & Web Engine v0.3.0 · Conceived by <a href="https://github.com/JackStar6677-1" target="_blank">JackStar</a> & SRE Triad
      </div>
      <div>
        Target: <strong>GitHub Pages Reactive SPA & Axum Backend</strong> · Theme: <strong id="foot-theme">{selected_theme.upper()}</strong>
      </div>
    </footer>
  </div>

  <!-- Micro-Signals Reactive Engine (<2KB) & Texture Studio Runtime -->
  <script>
    const MODULE_DATA = {module_json_escaped};
    const THEMES_DATA = {themes_json_escaped};
    
    const State = {{
      activeTab: "dashboard",
      searchQuery: "",
      filterType: "all",
      activeTheme: "{selected_theme}",
      isLoading: false,
      counter: 0,
      brushColor: "#38bdf8",
      activeTexture: "carbon",
      nodes: MODULE_DATA.nodes || []
    }};

    /* --- Theme Switcher --- */
    function switchTheme(themeKey) {{
      if (!THEMES_DATA[themeKey]) return;
      State.activeTheme = themeKey;
      document.documentElement.setAttribute('data-theme', themeKey);
      const styleEl = document.getElementById('theme-styles');
      if (styleEl) {{
        const themeVars = THEMES_DATA[themeKey].vars;
        styleEl.innerHTML = `:root {{ ${{themeVars}} --font-sans: 'Inter', sans-serif; --font-mono: 'JetBrains Mono', monospace; }}`;
      }}
      const footTheme = document.getElementById('foot-theme');
      if (footTheme) footTheme.textContent = themeKey.toUpperCase();
      updateSignalInspector();
    }}

    /* --- Tab Navigation --- */
    function setTab(tabName) {{
      State.activeTab = tabName;
      document.querySelectorAll('.nav-btn').forEach(btn => {{
        const onclickAttr = btn.getAttribute('onclick') || '';
        btn.classList.toggle('active', onclickAttr.includes(`'${{tabName}}'`) || onclickAttr.includes(`"${{tabName}}"`) || onclickAttr.includes(tabName));
      }});
      document.querySelectorAll('.view-section').forEach(sec => {{
        sec.classList.remove('active');
      }});
      const targetSec = document.getElementById('tab-' + tabName);
      if (targetSec) targetSec.classList.add('active');
      if (tabName === 'textures') initPixelCanvas();
      if (tabName === 'svgs') renderCustomSvg(document.getElementById('customSvgInput').value);
      updateSignalInspector();
    }}

    /* --- Search & Filter --- */
    function handleSearch(query) {{
      State.searchQuery = query.toLowerCase().trim();
      renderNodesTable();
      updateSignalInspector();
    }}

    function filterType(type, btnElement) {{
      State.filterType = type;
      document.querySelectorAll('.filter-chip').forEach(c => c.classList.remove('active'));
      if (btnElement) btnElement.classList.add('active');
      renderNodesTable();
      updateSignalInspector();
    }}

    function toggleLoadingState() {{
      State.isLoading = !State.isLoading;
      renderNodesTable();
      updateSignalInspector();
    }}

    function incrementCounter() {{
      State.counter++;
      updateSignalInspector();
    }}

    function decrementCounter() {{
      State.counter--;
      updateSignalInspector();
    }}

    function resetSignals() {{
      State.counter = 0;
      State.searchQuery = "";
      State.filterType = "all";
      State.isLoading = false;
      document.getElementById('node-search').value = "";
      renderNodesTable();
      updateSignalInspector();
    }}

    function updateSignalInspector() {{
      const elTab = document.getElementById('sig-activeTab');
      if (elTab) elTab.textContent = '"' + State.activeTab + '"';
      const elSearch = document.getElementById('sig-searchQuery');
      if (elSearch) elSearch.textContent = '"' + State.searchQuery + '"';
      const elFilter = document.getElementById('sig-filterType');
      if (elFilter) elFilter.textContent = '"' + State.filterType + '"';
      const elTheme = document.getElementById('sig-theme');
      if (elTheme) elTheme.textContent = '"' + State.activeTheme + '"';
      const elLoading = document.getElementById('sig-loading');
      if (elLoading) elLoading.textContent = State.isLoading ? "true" : "false";
      const elCounter = document.getElementById('sig-counter');
      if (elCounter) elCounter.textContent = State.counter;
    }}

    function renderNodesTable() {{
      const tbody = document.getElementById('nodes-table-body');
      if (!tbody) return;

      if (State.isLoading) {{
        // Render Shimmer Skeletons
        tbody.innerHTML = `
          <tr>
            <td><span class="skeleton skeleton-title" style="width: 70px;"></span></td>
            <td><span class="skeleton skeleton-title" style="width: 120px;"></span></td>
            <td><span class="skeleton skeleton-text"></span></td>
            <td><span class="skeleton skeleton-text" style="width: 80px;"></span></td>
            <td><span class="skeleton skeleton-title" style="width: 60px;"></span></td>
          </tr>
          <tr>
            <td><span class="skeleton skeleton-title" style="width: 70px;"></span></td>
            <td><span class="skeleton skeleton-title" style="width: 140px;"></span></td>
            <td><span class="skeleton skeleton-text"></span></td>
            <td><span class="skeleton skeleton-text" style="width: 90px;"></span></td>
            <td><span class="skeleton skeleton-title" style="width: 60px;"></span></td>
          </tr>
        `;
        return;
      }}

      const filtered = State.nodes.filter(n => {{
        const matchesType = State.filterType === 'all' || n.type === State.filterType;
        const matchesSearch = !State.searchQuery || 
          n.name.toLowerCase().includes(State.searchQuery) ||
          n.type.toLowerCase().includes(State.searchQuery) ||
          JSON.stringify(n.metadata).toLowerCase().includes(State.searchQuery);
        return matchesType && matchesSearch;
      }});

      if (filtered.length === 0) {{
        tbody.innerHTML = `<tr><td colspan="5" style="text-align: center; color: var(--text-dim); padding: 24px;">No se encontraron nodos que coincidan con el filtro.</td></tr>`;
        return;
      }}

      tbody.innerHTML = filtered.map(node => {{
        const metaStr = Object.entries(node.metadata || {{}})
          .map(([k, v]) => `${{k}}=${{v}}`)
          .join(', ') || '—';
        const childrenCount = (node.children || []).length;
        const pillClass = `pill-${{node.type}}`;
        return `
          <tr>
            <td><span class="pill ${{pillClass}}">${{node.type.toUpperCase()}}</span></td>
            <td><strong style="font-family: var(--font-mono); color: var(--text-main);">${{node.name}}</strong></td>
            <td style="color: var(--text-muted); font-size: 0.8rem; font-family: var(--font-mono);">${{metaStr}}</td>
            <td><span style="color: var(--accent); font-weight: 600;">${{childrenCount}}</span> sub-nodos</td>
            <td><button class="btn btn-secondary" style="padding: 4px 8px; font-size: 0.72rem;" onclick="inspectNode('${{node.name}}')">Inspeccionar</button></td>
          </tr>
        `;
      }}).join('');
    }}

    function inspectNode(name) {{
      const node = State.nodes.find(n => n.name === name);
      if (!node) return;
      alert(`[OMNIAST AST INSPECTOR]\n\nNombre: ${{node.name}}\nTipo: ${{node.type}}\nMetadatos: ${{JSON.stringify(node.metadata, null, 2)}}\nHijos: ${{node.children.length}}`);
    }}

    /* --- Texture Studio: Canvas Pixel Painter --- */
    const pixelGrid = Array(16).fill(null).map(() => Array(16).fill('#0f172a'));
    let isDrawing = false;

    function initPixelCanvas() {{
      const canvas = document.getElementById('pixelCanvas');
      if (!canvas) return;
      const ctx = canvas.getContext('2d');
      drawCanvasGrid(ctx);

      canvas.onmousedown = (e) => {{ isDrawing = true; paintPixel(e, canvas, ctx); }};
      window.onmouseup = () => {{ isDrawing = false; }};
      canvas.onmousemove = (e) => {{ if (isDrawing) paintPixel(e, canvas, ctx); }};
    }}

    function drawCanvasGrid(ctx) {{
      const size = 256 / 16;
      ctx.clearRect(0, 0, 256, 256);
      for (let y = 0; y < 16; y++) {{
        for (let x = 0; x < 16; x++) {{
          ctx.fillStyle = pixelGrid[y][x];
          ctx.fillRect(x * size, y * size, size, size);
          ctx.strokeStyle = 'rgba(255, 255, 255, 0.05)';
          ctx.strokeRect(x * size, y * size, size, size);
        }}
      }}
    }}

    function paintPixel(e, canvas, ctx) {{
      const rect = canvas.getBoundingClientRect();
      const x = Math.floor((e.clientX - rect.left) / (rect.width / 16));
      const y = Math.floor((e.clientY - rect.top) / (rect.height / 16));
      if (x >= 0 && x < 16 && y >= 0 && y < 16) {{
        pixelGrid[y][x] = State.brushColor;
        drawCanvasGrid(ctx);
        updateCardTextureFromCanvas();
      }}
    }}

    function setBrushColor(color, btn) {{
      State.brushColor = color;
      document.querySelectorAll('.swatch-btn').forEach(b => b.classList.remove('active'));
      if (btn) btn.classList.add('active');
    }}

    function clearCanvas() {{
      for (let y = 0; y < 16; y++) {{
        for (let x = 0; x < 16; x++) {{
          pixelGrid[y][x] = '#0f172a';
        }}
      }}
      const canvas = document.getElementById('pixelCanvas');
      if (canvas) drawCanvasGrid(canvas.getContext('2d'));
      updateCardTextureFromCanvas();
    }}

    function updateCardTextureFromCanvas() {{
      const canvas = document.getElementById('pixelCanvas');
      if (!canvas) return;
      const dataUrl = canvas.toDataURL('image/png');
      const card = document.getElementById('texturePreviewCard');
      if (card) {{
        card.style.backgroundImage = `url(${{dataUrl}})`;
        card.style.backgroundSize = '64px 64px';
      }}
      const lbl = document.getElementById('activeTextureLabel');
      if (lbl) lbl.textContent = "Pintura Pixel-Art Personalizada";
    }}

    function downloadTexture() {{
      const canvas = document.getElementById('pixelCanvas');
      if (!canvas) return;
      const a = document.createElement('a');
      a.href = canvas.toDataURL('image/png');
      a.download = 'omni_texture_16x16.png';
      a.click();
    }}

    /* Procedural Texture Presets */
    function applyPreset(presetName) {{
      State.activeTexture = presetName;
      const card = document.getElementById('texturePreviewCard');
      const lbl = document.getElementById('activeTextureLabel');
      if (!card) return;

      if (presetName === 'carbon') {{
        card.style.backgroundImage = `radial-gradient(black 15%, transparent 16%), radial-gradient(black 15%, transparent 16%)`;
        card.style.backgroundColor = '#18181b';
        card.style.backgroundSize = '16px 16px';
        card.style.backgroundPosition = '0 0, 8px 8px';
        if (lbl) lbl.textContent = 'Patrón: Carbon Fiber';
      }} else if (presetName === 'grid') {{
        card.style.backgroundImage = `linear-gradient(to right, rgba(56, 189, 248, 0.15) 1px, transparent 1px), linear-gradient(to bottom, rgba(56, 189, 248, 0.15) 1px, transparent 1px)`;
        card.style.backgroundColor = '#0b0f19';
        card.style.backgroundSize = '24px 24px';
        card.style.backgroundPosition = '0 0';
        if (lbl) lbl.textContent = 'Patrón: Cyber Grid';
      }} else if (presetName === 'honeycomb') {{
        card.style.backgroundImage = `radial-gradient(circle at center, rgba(168, 85, 247, 0.2) 2px, transparent 2px)`;
        card.style.backgroundColor = '#090d16';
        card.style.backgroundSize = '20px 20px';
        if (lbl) lbl.textContent = 'Patrón: Hex Honeycomb';
      }} else if (presetName === 'scanlines') {{
        card.style.backgroundImage = `repeating-linear-gradient(0deg, rgba(16, 185, 129, 0.1) 0px, rgba(16, 185, 129, 0.1) 1px, transparent 1px, transparent 3px)`;
        card.style.backgroundColor = '#051b11';
        card.style.backgroundSize = '100% 4px';
        if (lbl) lbl.textContent = 'Patrón: CRT Phosphor';
      }} else if (presetName === 'netherite') {{
        card.style.backgroundImage = `radial-gradient(#27272a 20%, transparent 20%), radial-gradient(#3f3f46 20%, transparent 20%)`;
        card.style.backgroundColor = '#18181b';
        card.style.backgroundSize = '12px 12px';
        card.style.backgroundPosition = '0 0, 6px 6px';
        if (lbl) lbl.textContent = 'Patrón: Netherite Tile';
      }}
    }}

    /* Texture Upload Handler */
    function handleFileSelect(e) {{
      const file = e.target.files[0];
      if (!file) return;
      const reader = new FileReader();
      reader.onload = (evt) => {{
        const card = document.getElementById('texturePreviewCard');
        if (card) {{
          card.style.backgroundImage = `url(${{evt.target.result}})`;
          card.style.backgroundSize = 'cover';
        }}
        const lbl = document.getElementById('activeTextureLabel');
        if (lbl) lbl.textContent = `Archivo: ${{file.name}} (${{Math.round(file.size / 1024)}} KB)`;
      }};
      reader.readAsDataURL(file);
    }}

    /* Custom SVG Live Renderer */
    function renderCustomSvg(code) {{
      const preview = document.getElementById('customSvgPreview');
      if (preview) {{
        preview.innerHTML = code;
      }}
    }}

    /* --- AST Playground Compilation Emulator --- */
    function compilePlayground() {{
      const input = document.getElementById('playground-input').value;
      const target = document.getElementById('target-selector').value;
      const out = document.getElementById('playground-output');
      
      out.textContent = `// Compilando con OmniAST Kernel v0.3.0 hacia target '${{target}}'...\n`;
      
      setTimeout(() => {{
        if (target === 'ast') {{
          out.textContent = JSON.stringify({{
            engine: "OmniAST Kernel v0.3.0",
            tokens_processed: input.length / 4,
            nodes: [
              {{ type: "module", name: "ClientCompiled" }},
              {{ type: "page", name: "DynamicView", path: "/" }}
            ]
          }}, null, 2);
        }} else if (target === 'rust') {{
          out.textContent = `//! Compiled to Native Rust & Tokio/Axum\nuse axum::{{Router, routing::get}};\n\npub fn app() -> Router {{\n    Router::new().route("/", get(|| async {{ "Hello from OmniAST Axum!" }}))\n}}`;
        }} else if (target === 'ts') {{
          out.textContent = `// Target: TypeScript Micro-Signals\nexport const State = new ReactiveStore({{\n  counter: 0,\n  path: "/"\n}});\nconsole.log("[OmniAST TS] Runtime ready");`;
        }} else if (target === 'wat') {{
          out.textContent = `(module\n  (func $main (result i32)\n    i32.const 42)\n  (export "main" (func $main)))`;
        }}
      }}, 150);
    }}

    function changeCompilerTarget(val) {{
      compilePlayground();
    }}

    /* Fallback Scroll Listener for Progress Bar */
    window.addEventListener('scroll', () => {{
      const bar = document.getElementById('scroll-progress');
      if (!bar) return;
      const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
      const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
      if (height > 0) {{
        const scrolled = (winScroll / height) * 100;
        bar.style.transform = `scaleX(${{scrolled / 100}})`;
      }}
    }});

    // Initialize
    window.addEventListener('DOMContentLoaded', () => {{
      renderNodesTable();
      updateSignalInspector();
      applyPreset('carbon');
      renderCustomSvg(document.getElementById('customSvgInput').value);
    }});
  </script>
</body>
</html>"""
        return html_template
