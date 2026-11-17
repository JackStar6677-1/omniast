"""
OmniAST 3D Sovereign Cyber-Universe & Language Constellation Engine (v0.3.0)
Conceived by JackStar6677-1 (Creator & Chief Architect) & Antigravity (SRE Triad).
Provides a real-time, hardware-accelerated 3D background with:
- Nested Sovereign geometric wireframe cores (Icosahedron, Dodecahedron, Octahedron)
- 4D Gyroscopic Torus Gimbal Rings rotating on independent axes
- Plexus Graph Constellation with dynamic line connection segments
- Cosmic Starfield with depth and subtle shimmer
- Orbiting 3D AST Syntax Badges rendering our native language (GraphLang / OmniAST / JackStar)
- Full mouse parallax with inertial damping (lerp)
- Resilient 2D canvas fallback for reduced motion or offline environments
"""

def get_3d_background_html() -> str:
    return """
  <!-- 3D Cyber-Universe Background Engine (Three.js & WebGL) -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
  <script>
  (function () {
    'use strict';

    function initSovereign3DBackground() {
      const canvas = document.getElementById('bg-canvas-3d');
      if (!canvas) return;

      // Respetar preferencias de accesibilidad de movimiento reducido
      if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        init2DFallback(canvas);
        return;
      }

      // Verificar Three.js
      if (typeof THREE === 'undefined') {
        console.warn('[OmniAST 3D] Three.js no está disponible. Activando fallback 2D.');
        init2DFallback(canvas);
        return;
      }

      let scene, camera, renderer;
      let mainGroup;
      let coreMesh, innerCoreMesh, centerCoreMesh;
      let rings = [];
      let satellites = [];
      let starfieldMesh;
      let particlesMesh, linesMesh;
      let particlePositions, particleData = [];
      let tokenSprites = [];
      const MAX_PARTICLES = 190;
      const MAX_DISTANCE = 48;

      let mouseX = 0, mouseY = 0;
      let targetX = 0, targetY = 0;
      let isPaused = false;
      let clock = 0;

      try {
        let width = window.innerWidth;
        let height = window.innerHeight;

        // 1. Escena y Cámara con perspectiva cinematográfica
        scene = new THREE.Scene();
        camera = new THREE.PerspectiveCamera(50, width / height, 0.1, 1600);
        camera.position.z = 210;

        // 2. Renderer WebGL de alto rendimiento con transparencia
        renderer = new THREE.WebGLRenderer({
          canvas: canvas,
          alpha: true,
          antialias: true,
          powerPreference: 'high-performance'
        });
        renderer.setSize(width, height);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));

        mainGroup = new THREE.Group();
        scene.add(mainGroup);

        // 3. Campo de Estrellas Cósmicas (Deep Starfield)
        const starCount = 420;
        const starGeo = new THREE.BufferGeometry();
        const starPos = new Float32Array(starCount * 3);
        for (let s = 0; s < starCount; s++) {
          const rad = 180 + Math.random() * 450;
          const th = Math.random() * Math.PI * 2;
          const ph = Math.acos((Math.random() * 2) - 1);
          starPos[s * 3] = rad * Math.sin(ph) * Math.cos(th);
          starPos[s * 3 + 1] = rad * Math.sin(ph) * Math.sin(th);
          starPos[s * 3 + 2] = rad * Math.cos(ph);
        }
        starGeo.setAttribute('position', new THREE.BufferAttribute(starPos, 3));
        const starMat = new THREE.PointsMaterial({
          color: 0xc4b5fd,
          size: 1.8,
          transparent: true,
          opacity: 0.65
        });
        starfieldMesh = new THREE.Points(starGeo, starMat);
        scene.add(starfieldMesh);

        // 4. Núcleos Geométricos Soberanos (Sovereign Multi-Cores)
        // Núcleo Exterior: Icosaedro Amatista
        const coreGeo = new THREE.IcosahedronGeometry(48, 1);
        const coreMat = new THREE.MeshBasicMaterial({
          color: 0xa855f7,
          wireframe: true,
          transparent: true,
          opacity: 0.38
        });
        coreMesh = new THREE.Mesh(coreGeo, coreMat);
        mainGroup.add(coreMesh);

        // Núcleo Medio: Dodecaedro Índigo Eléctrico
        const innerGeo = new THREE.DodecahedronGeometry(30, 0);
        const innerMat = new THREE.MeshBasicMaterial({
          color: 0x6366f1,
          wireframe: true,
          transparent: true,
          opacity: 0.48
        });
        innerCoreMesh = new THREE.Mesh(innerGeo, innerMat);
        mainGroup.add(innerCoreMesh);

        // Núcleo Central: Octaedro Cian Cuántico
        const centerGeo = new THREE.OctahedronGeometry(15, 0);
        const centerMat = new THREE.MeshBasicMaterial({
          color: 0x22d3ee,
          wireframe: true,
          transparent: true,
          opacity: 0.75
        });
        centerCoreMesh = new THREE.Mesh(centerGeo, centerMat);
        mainGroup.add(centerCoreMesh);

        // 5. Cuádruple Anillo Orbital Giroscópico (Gimbal 4D)
        const ringConfigs = [
          { r: 72, tube: 0.45, color: 0x9333ea, rotX: Math.PI / 3, rotY: 0, rotZ: 0 },
          { r: 92, tube: 0.40, color: 0x06b6d4, rotX: 0, rotY: Math.PI / 4, rotZ: 0 },
          { r: 112, tube: 0.35, color: 0xec4899, rotX: -Math.PI / 5, rotY: 0, rotZ: Math.PI / 6 },
          { r: 132, tube: 0.35, color: 0x38bdf8, rotX: 0, rotY: -Math.PI / 3, rotZ: 0 }
        ];
        ringConfigs.forEach(rc => {
          const rGeo = new THREE.TorusGeometry(rc.r, rc.tube, 16, 120);
          const rMat = new THREE.MeshBasicMaterial({
            color: rc.color,
            transparent: true,
            opacity: 0.42
          });
          const rMesh = new THREE.Mesh(rGeo, rMat);
          rMesh.rotation.set(rc.rotX, rc.rotY, rc.rotZ);
          mainGroup.add(rMesh);
          rings.push(rMesh);
        });

        // 6. Satélites Orbitantes
        const satColors = [0x22d3ee, 0xa855f7, 0xec4899, 0x10b981, 0xfbbf24, 0x60a5fa];
        for (let s = 0; s < 6; s++) {
          const satGeo = new THREE.BoxGeometry(3, 3, 3);
          const satMat = new THREE.MeshBasicMaterial({
            color: satColors[s % satColors.length],
            transparent: true,
            opacity: 0.85
          });
          const satMesh = new THREE.Mesh(satGeo, satMat);
          mainGroup.add(satMesh);
          satellites.push({
            mesh: satMesh,
            radius: 65 + s * 14,
            speed: 0.015 + (s * 0.005),
            angle: (s * Math.PI) / 3
          });
        }

        // 7. Red Plexus / Constelación AST
        const pCount = Math.min(MAX_PARTICLES, Math.max(100, Math.floor(width / 7)));
        particlePositions = new Float32Array(pCount * 3);
        const particleColors = new Float32Array(pCount * 3);
        const pal = [
          new THREE.Color(0xa855f7),
          new THREE.Color(0x38bdf8),
          new THREE.Color(0x10b981),
          new THREE.Color(0xfbbf24),
          new THREE.Color(0xec4899)
        ];

        for (let i = 0; i < pCount; i++) {
          const radius = 55 + Math.random() * 115;
          const theta = Math.random() * Math.PI * 2;
          const phi = Math.acos((Math.random() * 2) - 1);
          particlePositions[i * 3] = radius * Math.sin(phi) * Math.cos(theta);
          particlePositions[i * 3 + 1] = radius * Math.sin(phi) * Math.sin(theta);
          particlePositions[i * 3 + 2] = radius * Math.cos(phi);

          particleData.push({
            vx: (Math.random() - 0.5) * 0.2,
            vy: (Math.random() - 0.5) * 0.2,
            vz: (Math.random() - 0.5) * 0.2
          });

          const c = pal[i % pal.length];
          particleColors[i * 3] = c.r;
          particleColors[i * 3 + 1] = c.g;
          particleColors[i * 3 + 2] = c.b;
        }

        const pGeo = new THREE.BufferGeometry();
        pGeo.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3).setUsage(THREE.DynamicDrawUsage));
        pGeo.setAttribute('color', new THREE.BufferAttribute(particleColors, 3));
        const pMat = new THREE.PointsMaterial({
          size: 3.6,
          vertexColors: true,
          transparent: true,
          opacity: 0.85
        });
        particlesMesh = new THREE.Points(pGeo, pMat);
        mainGroup.add(particlesMesh);

        // Líneas dinámicas de conexión
        const maxLines = (pCount * (pCount - 1)) / 2;
        const linePositions = new Float32Array(maxLines * 6);
        const lineColors = new Float32Array(maxLines * 6);
        const lineGeo = new THREE.BufferGeometry();
        lineGeo.setAttribute('position', new THREE.BufferAttribute(linePositions, 3).setUsage(THREE.DynamicDrawUsage));
        lineGeo.setAttribute('color', new THREE.BufferAttribute(lineColors, 3).setUsage(THREE.DynamicDrawUsage));
        const lineMat = new THREE.LineBasicMaterial({
          vertexColors: true,
          transparent: true,
          opacity: 0.45
        });
        linesMesh = new THREE.LineSegments(lineGeo, lineMat);
        mainGroup.add(linesMesh);

        // 8. "LENGUAJE DE NOSOTROS" — 16 Sprites 3D Orbitantes con Badges de Sintaxis AST
        function createTextBadgeSprite(text, borderColor, textColor) {
          const c = document.createElement('canvas');
          c.width = 440;
          c.height = 92;
          const ctx = c.getContext('2d');

          // Fondo Glassmorphic Oscuro
          ctx.fillStyle = 'rgba(7, 11, 24, 0.92)';
          ctx.strokeStyle = borderColor || '#38bdf8';
          ctx.lineWidth = 4;

          const r = 24;
          const x = 6, y = 6, w = c.width - 12, h = c.height - 12;
          ctx.beginPath();
          ctx.moveTo(x + r, y);
          ctx.arcTo(x + w, y, x + w, y + h, r);
          ctx.arcTo(x + w, y + h, x, y + h, r);
          ctx.arcTo(x, y + h, x, y, r);
          ctx.arcTo(x, y, x + w, y, r);
          ctx.closePath();
          ctx.fill();
          ctx.stroke();

          // Punto de estado brillante
          ctx.beginPath();
          ctx.arc(38, c.height / 2, 8, 0, Math.PI * 2);
          ctx.fillStyle = borderColor || '#38bdf8';
          ctx.shadowColor = borderColor || '#38bdf8';
          ctx.shadowBlur = 10;
          ctx.fill();
          ctx.shadowBlur = 0;

          // Texto en JetBrains Mono
          ctx.fillStyle = textColor || '#ffffff';
          ctx.font = 'bold 25px "JetBrains Mono", monospace';
          ctx.textBaseline = 'middle';
          ctx.fillText(text, 62, c.height / 2);

          const tex = new THREE.CanvasTexture(c);
          tex.minFilter = THREE.LinearFilter;
          const sMat = new THREE.SpriteMaterial({
            map: tex,
            transparent: true,
            opacity: 0.90
          });
          const sp = new THREE.Sprite(sMat);
          sp.scale.set(36, 7.5, 1);
          return sp;
        }

        const ourLanguageTokens = [
          { text: "◈ OmniAST v0.3.0", border: "#38bdf8", color: "#e0f2fe" },
          { text: "⚡ GraphLang · AST", border: "#a855f7", color: "#f3e8ff" },
          { text: "👑 JackStar Sovereign", border: "#fbbf24", color: "#fef3c7" },
          { text: "📄 page SovereignPortal", border: "#3b82f6", color: "#dbeafe" },
          { text: "📡 signal kernelStatus", border: "#10b981", color: "#d1fae5" },
          { text: "📦 model ASTGraphNode", border: "#6366f1", color: "#e0e7ff" },
          { text: "🔌 endpoint /api/v1/ast", border: "#f59e0b", color: "#fef3c7" },
          { text: "🛡️ sentinel FleetSupervisor", border: "#ec4899", color: "#fce7f3" },
          { text: "⚙️ machine QuantumAST", border: "#06b6d4", color: "#cffafe" },
          { text: "🦀 Axum 0.7 + Tokio 1.0", border: "#f97316", color: "#ffedd5" },
          { text: "⚡ Micro-Signals <3.8KB", border: "#10b981", color: "#d1fae5" },
          { text: "📉 Token Savings -85.4%", border: "#22c55e", color: "#dcfce7" },
          { text: "💎 Zero-Virtual-DOM", border: "#38bdf8", color: "#e0f2fe" },
          { text: "🌸 Saori AI · Athena SRE", border: "#c084fc", color: "#f3e8ff" },
          { text: "⭐ Star Cloud 24/7/365", border: "#fbbf24", color: "#fef3c7" },
          { text: "🛡️ SRE Swarm Sentinel", border: "#ec4899", color: "#fce7f3" }
        ];

        ourLanguageTokens.forEach((tok, idx) => {
          const sp = createTextBadgeSprite(tok.text, tok.border, tok.color);
          mainGroup.add(sp);
          const rad = 88 + (idx % 4) * 22;
          const initialAngle = (idx * (Math.PI * 2)) / ourLanguageTokens.length;
          const yOffset = ((idx % 5) - 2) * 19;
          tokenSprites.push({
            sprite: sp,
            radius: rad,
            angle: initialAngle,
            speed: 0.0032 + (idx % 3) * 0.0018,
            yOffset: yOffset
          });
        });

        // 9. Interacción con Mouse / Tacto y Bucle de Animación
        function onPointerMove(e) {
          const clientX = e.clientX || (e.touches && e.touches[0] ? e.touches[0].clientX : 0);
          const clientY = e.clientY || (e.touches && e.touches[0] ? e.touches[0].clientY : 0);
          mouseX = (clientX / window.innerWidth) * 2 - 1;
          mouseY = -(clientY / window.innerHeight) * 2 + 1;
        }

        window.addEventListener('pointermove', onPointerMove, { passive: true });
        window.addEventListener('touchmove', onPointerMove, { passive: true });

        window.addEventListener('resize', () => {
          width = window.innerWidth;
          height = window.innerHeight;
          camera.aspect = width / height;
          camera.updateProjectionMatrix();
          renderer.setSize(width, height);
          renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
        }, { passive: true });

        document.addEventListener('visibilitychange', () => {
          isPaused = document.hidden;
        });

        function animate() {
          requestAnimationFrame(animate);
          if (isPaused) return;

          clock += 0.016;

          targetX += (mouseX - targetX) * 0.05;
          targetY += (mouseY - targetY) * 0.05;

          mainGroup.rotation.y += 0.0028;
          mainGroup.rotation.x = targetY * 0.22;
          mainGroup.rotation.y += targetX * 0.004;

          starfieldMesh.rotation.y -= 0.0005;

          coreMesh.rotation.y += 0.005;
          coreMesh.rotation.x += 0.0025;

          innerCoreMesh.rotation.y -= 0.0065;
          innerCoreMesh.rotation.z += 0.0035;

          centerCoreMesh.rotation.x += 0.012;
          centerCoreMesh.rotation.y += 0.014;
          const pulse = 1.0 + Math.sin(clock * 3) * 0.2;
          centerCoreMesh.scale.set(pulse, pulse, pulse);

          rings[0].rotation.z += 0.0055;
          rings[1].rotation.x -= 0.0045;
          rings[2].rotation.y += 0.0065;
          rings[3].rotation.z -= 0.004;

          satellites.forEach(sat => {
            sat.angle += sat.speed;
            sat.mesh.position.x = Math.cos(sat.angle) * sat.radius;
            sat.mesh.position.z = Math.sin(sat.angle) * sat.radius;
            sat.mesh.position.y = Math.sin(sat.angle * 1.5) * (sat.radius * 0.35);
            sat.mesh.rotation.x += 0.02;
            sat.mesh.rotation.y += 0.02;
          });

          // Orbitar Sprites de Sintaxis ("lenguaje de nosotros")
          tokenSprites.forEach(tok => {
            tok.angle += tok.speed;
            tok.sprite.position.x = Math.cos(tok.angle) * tok.radius;
            tok.sprite.position.z = Math.sin(tok.angle) * tok.radius;
            tok.sprite.position.y = tok.yOffset + Math.sin(tok.angle * 1.8 + clock) * 9;
          });

          // Enlaces Plexus Dinámicos
          let connectedLines = 0;
          let lineVertexPos = 0;
          let lineColorsPos = 0;

          for (let i = 0; i < pCount; i++) {
            const i3 = i * 3;
            particlePositions[i3] += particleData[i].vx;
            particlePositions[i3 + 1] += particleData[i].vy;
            particlePositions[i3 + 2] += particleData[i].vz;

            const dist = Math.sqrt(
              particlePositions[i3] * particlePositions[i3] +
              particlePositions[i3 + 1] * particlePositions[i3 + 1] +
              particlePositions[i3 + 2] * particlePositions[i3 + 2]
            );

            if (dist > 165 || dist < 42) {
              particleData[i].vx *= -1;
              particleData[i].vy *= -1;
              particleData[i].vz *= -1;
            }

            for (let j = i + 1; j < pCount; j++) {
              const j3 = j * 3;
              const dx = particlePositions[i3] - particlePositions[j3];
              const dy = particlePositions[i3 + 1] - particlePositions[j3 + 1];
              const dz = particlePositions[i3 + 2] - particlePositions[j3 + 2];
              const d = Math.sqrt(dx * dx + dy * dy + dz * dz);

              if (d < MAX_DISTANCE) {
                const alpha = (1.0 - d / MAX_DISTANCE) * 0.55;

                linePositions[lineVertexPos++] = particlePositions[i3];
                linePositions[lineVertexPos++] = particlePositions[i3 + 1];
                linePositions[lineVertexPos++] = particlePositions[i3 + 2];

                linePositions[lineVertexPos++] = particlePositions[j3];
                linePositions[lineVertexPos++] = particlePositions[j3 + 1];
                linePositions[lineVertexPos++] = particlePositions[j3 + 2];

                const cR = 0.58 * alpha, cG = 0.32 * alpha, cB = 0.95 * alpha;
                lineColors[lineColorsPos++] = cR;
                lineColors[lineColorsPos++] = cG;
                lineColors[lineColorsPos++] = cB;

                const cR2 = 0.12 * alpha, cG2 = 0.75 * alpha, cB2 = 0.95 * alpha;
                lineColors[lineColorsPos++] = cR2;
                lineColors[lineColorsPos++] = cG2;
                lineColors[lineColorsPos++] = cB2;

                connectedLines++;
              }
            }
          }

          pGeo.attributes.position.needsUpdate = true;
          lineGeo.setDrawRange(0, connectedLines * 2);
          lineGeo.attributes.position.needsUpdate = true;
          lineGeo.attributes.color.needsUpdate = true;

          renderer.render(scene, camera);
        }

        animate();
      } catch (err) {
        console.warn('[OmniAST 3D] Error WebGL, ejecutando fallback 2D:', err);
        init2DFallback(canvas);
      }
    }

    // Fallback Canvas 2D
    function init2DFallback(canvas) {
      const ctx = canvas.getContext('2d');
      if (!ctx) return;
      let w = window.innerWidth, h = window.innerHeight;
      canvas.width = w; canvas.height = h;

      const pts = Array.from({ length: 48 }, () => ({
        x: Math.random() * w,
        y: Math.random() * h,
        vx: (Math.random() - 0.5) * 0.6,
        vy: (Math.random() - 0.5) * 0.6
      }));

      function step() {
        ctx.clearRect(0, 0, w, h);
        ctx.fillStyle = '#070913';
        ctx.fillRect(0, 0, w, h);

        pts.forEach(p => {
          p.x += p.vx; p.y += p.vy;
          if (p.x < 0 || p.x > w) p.vx *= -1;
          if (p.y < 0 || p.y > h) p.vy *= -1;
          ctx.beginPath();
          ctx.arc(p.x, p.y, 2, 0, Math.PI * 2);
          ctx.fillStyle = 'rgba(56, 189, 248, 0.7)';
          ctx.fill();
        });

        requestAnimationFrame(step);
      }
      step();
    }

    window.initSovereign3DBackground = initSovereign3DBackground;
  })();
  </script>
"""
