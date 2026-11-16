"""
Omni-UI Sovereign CSS Design System (v0.3.0)
A modular, high-performance CSS framework engineered for OmniAST,
supporting animated RGB borders, scroll-driven animations, loaders/skeletons,
modern headers, hero sections, texture rendering, and SVG animation utilities.
"""

def get_omni_ui_css() -> str:
    return """
/* ==========================================================================
   OMNI-UI SOVEREIGN DESIGN SYSTEM (v0.3.0)
   Zero-dependency, Compositor-accelerated, High-contrast Cyberpunk & Sovereign CSS
   ========================================================================== */

/* --- Scroll Progress Bar (Scroll-driven animation with RGB flow) --- */
#scroll-progress {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 3px;
  background: linear-gradient(90deg, #ec4899, #8b5cf6, #3b82f6, #06b6d4, #10b981, #ec4899);
  background-size: 300% 100%;
  transform-origin: 0 50%;
  z-index: 10000;
  pointer-events: none;
  animation: rgb-flow 4s linear infinite;
}

@supports (animation-timeline: scroll()) {
  @keyframes grow-scroll-progress {
    from { transform: scaleX(0); }
    to { transform: scaleX(1); }
  }
  #scroll-progress {
    animation: grow-scroll-progress auto linear, rgb-flow 4s linear infinite;
    animation-timeline: scroll(root block), auto;
  }
}

/* --- Animated RGB Border & Ambient Glow --- */
@keyframes rgb-flow {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

@keyframes rgb-glow-pulse {
  0%, 100% {
    box-shadow: 0 0 15px rgba(139, 92, 246, 0.4), 0 0 30px rgba(6, 182, 212, 0.2);
  }
  50% {
    box-shadow: 0 0 25px rgba(236, 72, 153, 0.5), 0 0 45px rgba(16, 185, 129, 0.3);
  }
}

@keyframes rgb-spin-border {
  0% { --rgb-angle: 0deg; }
  100% { --rgb-angle: 360deg; }
}

@property --rgb-angle {
  syntax: '<angle>';
  initial-value: 0deg;
  inherits: false;
}

.rgb-card {
  position: relative;
  background: var(--surface);
  border-radius: var(--radius-md);
  padding: 24px;
  overflow: hidden;
  border: 1px solid transparent;
  background-clip: padding-box;
}

.rgb-card::before {
  content: '';
  position: absolute;
  inset: -2px;
  z-index: -1;
  background: linear-gradient(var(--rgb-angle, 0deg), #ec4899, #8b5cf6, #06b6d4, #10b981, #f59e0b, #ec4899);
  border-radius: calc(var(--radius-md) + 2px);
  animation: rgb-spin-border 6s linear infinite;
}

.rgb-glow {
  animation: rgb-glow-pulse 4s ease-in-out infinite;
}

/* --- Scroll-Driven Content Reveals --- */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(24px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.reveal-on-scroll {
  animation: fadeInUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) both;
}

@supports (animation-timeline: view()) {
  @keyframes view-reveal {
    from {
      opacity: 0;
      transform: translateY(30px) scale(0.98);
    }
    to {
      opacity: 1;
      transform: translateY(0) scale(1);
    }
  }
  .scroll-view-reveal {
    animation: view-reveal 0.6s linear both;
    animation-timeline: view();
    animation-range: entry 10% cover 30%;
  }
}

/* --- Loaders & Shimmer Skeletons --- */
@keyframes shimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}

.skeleton {
  background: linear-gradient(90deg, 
    var(--surface-hover) 25%, 
    rgba(255, 255, 255, 0.08) 37%, 
    var(--surface-hover) 63%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s cubic-bezier(0.4, 0, 0.6, 1) infinite;
  border-radius: var(--radius-sm);
  display: inline-block;
}

.skeleton-text {
  height: 14px;
  width: 100%;
  margin-bottom: 8px;
}

.skeleton-title {
  height: 22px;
  width: 60%;
  margin-bottom: 14px;
}

.skeleton-circle {
  width: 44px;
  height: 44px;
  border-radius: 50%;
}

.skeleton-card {
  height: 140px;
  width: 100%;
  border-radius: var(--radius-md);
}

/* Quantum Pulse Loader */
.loader-quantum {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  position: relative;
  width: 48px;
  height: 48px;
}

.loader-quantum-ring {
  position: absolute;
  width: 100%;
  height: 100%;
  border: 2px solid transparent;
  border-top-color: var(--primary);
  border-radius: 50%;
  animation: spin 1s cubic-bezier(0.5, 0, 0.5, 1) infinite;
}

.loader-quantum-ring:nth-child(2) {
  width: 75%;
  height: 75%;
  border-top-color: var(--accent);
  animation-duration: 1.5s;
  animation-direction: reverse;
}

.loader-quantum-ring:nth-child(3) {
  width: 50%;
  height: 50%;
  border-top-color: var(--success);
  animation-duration: 0.8s;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Radar Sweep Loader */
.loader-radar {
  position: relative;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  border: 1px solid rgba(16, 185, 129, 0.3);
  background: radial-gradient(circle, rgba(16, 185, 129, 0.05) 0%, transparent 70%);
  overflow: hidden;
}

.loader-radar::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 50%;
  height: 50%;
  background: linear-gradient(45deg, rgba(16, 185, 129, 0.8), transparent);
  transform-origin: 0% 0%;
  animation: radar-sweep 2s linear infinite;
}

@keyframes radar-sweep {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* --- Hero Section & Banner --- */
.hero-container {
  position: relative;
  padding: 60px 32px 48px;
  margin-bottom: 32px;
  border-radius: var(--radius-lg);
  background: radial-gradient(circle at 80% 20%, rgba(139, 92, 246, 0.15), transparent 60%),
              radial-gradient(circle at 20% 80%, rgba(6, 182, 212, 0.12), transparent 50%),
              var(--surface);
  border: 1px solid var(--border-color);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.hero-backdrop-svg {
  position: absolute;
  top: 0;
  right: 0;
  width: 50%;
  height: 100%;
  opacity: 0.12;
  pointer-events: none;
  z-index: 0;
}

.hero-content {
  position: relative;
  z-index: 1;
  max-width: 780px;
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 6px 14px;
  border-radius: 9999px;
  background: rgba(139, 92, 246, 0.15);
  border: 1px solid rgba(139, 92, 246, 0.3);
  font-size: 0.78rem;
  font-family: var(--font-mono);
  color: #c084fc;
  margin-bottom: 16px;
  box-shadow: 0 0 12px rgba(139, 92, 246, 0.2);
}

.hero-badge .pulse-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #10b981;
  box-shadow: 0 0 8px #10b981;
  animation: pulse-dot-glow 2s infinite;
}

@keyframes pulse-dot-glow {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.4; transform: scale(0.85); }
}

.hero-title {
  font-size: clamp(2rem, 4vw, 3.2rem);
  font-weight: 800;
  letter-spacing: -0.03em;
  line-height: 1.15;
  margin-bottom: 14px;
  background: linear-gradient(135deg, var(--text-main) 30%, var(--primary) 70%, var(--accent) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.hero-subtitle {
  font-size: 1.05rem;
  color: var(--text-muted);
  line-height: 1.6;
  margin-bottom: 24px;
}

.hero-actions {
  display: flex;
  gap: 14px;
  flex-wrap: wrap;
  align-items: center;
}

.hero-stats-bar {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
  gap: 16px;
  margin-top: 24px;
  padding-top: 20px;
  border-top: 1px solid var(--border-color);
}

.hero-stat-item {
  display: flex;
  flex-direction: column;
}

.hero-stat-val {
  font-size: 1.5rem;
  font-weight: 700;
  font-family: var(--font-mono);
  color: var(--text-main);
}

.hero-stat-lbl {
  font-size: 0.75rem;
  color: var(--text-dim);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

/* --- SVG Animation Utilities --- */
.svg-pulse {
  animation: svg-pulse-anim 3s ease-in-out infinite;
}

@keyframes svg-pulse-anim {
  0%, 100% { transform: scale(1); filter: drop-shadow(0 0 4px var(--primary-glow)); }
  50% { transform: scale(1.05); filter: drop-shadow(0 0 12px var(--accent)); }
}

.svg-circuit-path {
  stroke-dasharray: 100;
  stroke-dashoffset: 100;
  animation: circuit-draw 4s linear infinite;
}

@keyframes circuit-draw {
  0% { stroke-dashoffset: 100; }
  50% { stroke-dashoffset: 0; }
  100% { stroke-dashoffset: -100; }
}

/* --- In-Browser Texture Studio --- */
.texture-studio-grid {
  display: grid;
  grid-template-columns: 320px 1fr;
  gap: 24px;
  margin-top: 16px;
}

@media (max-width: 900px) {
  .texture-studio-grid {
    grid-template-columns: 1fr;
  }
}

.canvas-wrapper {
  background: #0f172a;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  padding: 16px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.pixel-canvas {
  image-rendering: pixelated;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  background-color: #1e293b;
  cursor: crosshair;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
}

.canvas-controls {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
  width: 100%;
  justify-content: center;
}

.color-swatch-picker {
  display: flex;
  gap: 6px;
}

.swatch-btn {
  width: 24px;
  height: 24px;
  border-radius: 4px;
  border: 2px solid transparent;
  cursor: pointer;
  transition: transform 0.15s ease;
}

.swatch-btn:hover {
  transform: scale(1.2);
}

.swatch-btn.active {
  border-color: #ffffff;
  box-shadow: 0 0 8px rgba(255, 255, 255, 0.6);
}

.drop-zone {
  border: 2px dashed var(--border-color);
  border-radius: var(--radius-md);
  padding: 24px;
  text-align: center;
  cursor: pointer;
  background: var(--surface);
  transition: all 0.2s ease;
}

.drop-zone:hover, .drop-zone.dragover {
  border-color: var(--primary);
  background: var(--surface-hover);
}

.texture-preview-card {
  min-height: 200px;
  border-radius: var(--radius-md);
  padding: 24px;
  background-size: repeat;
  border: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  box-shadow: inset 0 0 40px rgba(0, 0, 0, 0.8), 0 10px 30px rgba(0, 0, 0, 0.5);
  position: relative;
  overflow: hidden;
}

.texture-preview-overlay {
  background: rgba(15, 23, 42, 0.85);
  backdrop-filter: blur(8px);
  padding: 16px;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border-color);
}
"""
