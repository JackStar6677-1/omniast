# SAORI v3: Estudio Arquitectónico y Blueprint de Unificación
## Integrando OpenClaw (TypeScript Daemon), Hermes (Function Calling) y OmniAST (Graph IR)

**Fecha:** 19 de Octubre de 2026  
**Autor:** JackStar6677-1 / Antigravity SRE Team  
**Estado:** Blueprint Aprobado para Ejecución Progresiva  
**Ubicación:** `omniast/docs/architecture/SAORI_OPENCLAW_HERMES_UNIFICATION.md` & `ai-hub/docs/`

---

## 1. Resumen Ejecutivo y Diagnóstico

### La Pregunta Central
> *"¿Sería prudente organizar a SAORI como lo hace OpenClaw con Node/TypeScript y meterle las skills de OpenClaw/Hermes a OmniAST? ¿Sería el culmine mover SAORI a Node con la tecnología de OpenClaw y Hermes juntos más OmniAST?"*

### La Respuesta de Ingeniería
**Sí, rotundamente sí, pero aplicando un modelo híbrido por capas (Gateway en TypeScript 90% + Kernel en Rust/Python + Core Cognitivo en Hermes/OmniAST).**

Hoy en día, la infraestructura de SAORI en Star VPS tiene una división accidental:
- `saori-discord`: Escrito en **Node.js** (discord.js v14 en Docker).
- `saori-whatsapp`: Escrito en **Node.js** (@whiskeysockets/baileys en Docker).
- `saori-knowledge-engine`: Escrito en **Python** (FastAPI en Docker).
- Supervisores SRE y Staging: Escritos en **Python standalone** bajo systemd.
- Memoria compartida: **SQLite WAL** (puerto 8077).

**El problema actual:** Los bots de Discord y WhatsApp ya usan Node.js, pero están en silos desconectados, con código duplicado, buffers separados y prompts no estandarizados. Mientras tanto, los supervisores SRE en Python operan por su cuenta sin un bus de eventos unificado.

Adoptar la arquitectura de **OpenClaw (TypeScript 90.2%)** combinada con **Hermes (JSON Schema Function Calling)** y el kernel de grafos de **OmniAST** unifica el ecosistema en una plataforma industrial definitiva.

---

## 2. Los Tres Pilares de la Nueva Arquitectura

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       CAPA 1: OMNICHANNEL GATEWAY                           │
│                 (OpenClaw Style - TypeScript 90.2% / Node 20+)              │
│                                                                             │
│  ┌────────────────┐ ┌────────────────┐ ┌────────────────┐ ┌──────────────┐  │
│  │ Discord Bridge │ │WhatsApp Baileys│ │  In-Game RCON  │ │ Web / Mobile │  │
│  │ (discord.js 14)│ │  (WebSockets)  │ │  (Minecraft)   │ │  Dashboard   │  │
│  └───────┬────────┘ └───────┬────────┘ └───────┬────────┘ └──────┬───────┘  │
│          │                  │                  │                 │          │
│          └──────────────────┼──────────────────┼─────────────────┘          │
│                             ▼                                               │
│                 [ Unified Event Bus / Dispatcher ]                          │
└─────────────────────────────┬───────────────────────────────────────────────┘
                              │
┌─────────────────────────────▼───────────────────────────────────────────────┐
│                    CAPA 2: COGNITIVE AGENT PROTOCOL                         │
│                    (Hermes Function Calling & Skills)                       │
│                                                                             │
│  * Esquema Unificado de Herramientas (JSON Schema)                          │
│  * Modelos Compatibles: Claude 3.5, OpenAI Codex, Antigravity, Hermes 3     │
│  * Skills Estándar: Shell Sandbox, Filesystem, Memory Recall, Alert Throttler│
└─────────────────────────────┬───────────────────────────────────────────────┘
                              │
┌─────────────────────────────▼───────────────────────────────────────────────┐
│                   CAPA 3: GRAPH KERNEL & MEMORY IR                          │
│                       (OmniAST / GraphLang)                                 │
│                                                                             │
│  * 85% Reducción de Tokens: Código y Estado modelados como Grafo AST        │
│  * Transpilador Multi-Target: TypeScript (Gateway), Rust (SIMD), Java (JVM) │
│  * Memoria Compartida: SQLite WAL + Graphify Knowledge Memory               │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. ¿Por qué OpenClaw como Referencia para SAORI?

Analizando la composición técnica de OpenClaw:
- **TypeScript (90.2%):** Lenguaje ideal para manejar I/O asíncrono masivo, WebSockets de Discord y WhatsApp, reconexiones automáticas, validación de schemas con Zod y tipado estricto.
- **Arquitectura de Gateway Único:** En lugar de mantener contenedores aislados que no se hablan entre sí, un único demonio Node/TS (`saori-core-gateway`) orquesta todos los canales de entrada. Si un usuario habla en WhatsApp o Discord, el contexto fluye por el mismo pipeline.
- **Skills Directory Desacoplado:** Cada herramienta (shell, docker, git, tickets, servidor) es un plugin modular con permisos granulares.

---

## 4. ¿Por qué Hermes para el Protocolo de Herramientas?

**Nous Hermes** introdujo el estándar abierto más limpio y eficiente de Function Calling:
- Define herramientas mediante JSON Schema estándar:
  ```json
  {
    "type": "function",
    "function": {
      "name": "omniast_mutate_node",
      "description": "Mutación atómica de grafo de código",
      "parameters": { ... }
    }
  }
  ```
- **Agnóstico al proveedor:** Funciona de forma idéntica si el cerebro detrás de SAORI es Claude Haiku/Sonnet, OpenAI Codex, Google Antigravity, o un modelo local Hermes-3 corriendo en vLLM/Ollama.
- **Razonamiento estructurado:** El modelo emite `<tool_call>` directo sin desperdiciar tokens en saludos o texto intermedio cuando se requiere ejecución de acciones.

---

## 5. El Rol de OmniAST en este Ecosistema

**OmniAST es el pegamento estructural:**
1. **Representación de Código y Estado:** Mientras OpenClaw y Hermes suelen trabajar con texto plano o llamadas JSON simples, OmniAST aporta la **persistencia en grafos de dependencias**.
2. **Generación Directa de TypeScript:** El nuevo transpilador `transpilers/typescript_transpiler.py` permite que los agentes escriban o editen módulos `.omni` y se compilen inmediatamente a TypeScript compatible con el runtime de OpenClaw.
3. **Erradicación del Context Window Exhaustion:** En sistemas con más de 190 repositorios (como Slimefun New Horizons), cargar archivos de código colapsa el context window. Con OmniAST, el agente solo consulta el nodo exacto del grafo vía `omniast_query_graph`.

---

## 6. Plan de Transición por Fases (Cero Downtime)

Para no interrumpir la operación 24/7 de Star VPS ni de DrakesCraft:

### Fase A: Adopción Inmediata (Ya Completada en OmniAST)
- [x] Transpilador TypeScript (`ts`) integrado en OmniAST.
- [x] Registro formal de herramientas Hermes y manifiesto OpenClaw en `core/skills/hermes_openclaw.py`.
- [x] Verificación de pruebas (9/9 tests pasando en 0.001s).

### Fase B: Fusión del Gateway SAORI (Node/TypeScript)
- Unificar `saori-discord` y `saori-whatsapp` en un solo monorepo TypeScript (`saori-gateway`).
- Adoptar el bus de eventos centralizado con tipado común para Discord, WhatsApp y Web Console.
- Conectar el gateway al servidor MCP de OmniAST y a la memoria compartida SQLite WAL.

### Fase C: Integración Total SRE
- Migrar los supervisores periódicos en Python para que emitan eventos al bus de SAORI mediante sockets locales o gRPC.
- Las alertas se consolidan bajo el throttler de OmniAST (evitando alertas duplicadas en Discord).

---

## 7. Conclusión

Mover la capa de interacción y coordinación de SAORI a **TypeScript/Node (estilo OpenClaw)**, gobernada por el protocolo de **Function Calling de Hermes** y anclada en el **Kernel de Grafos de OmniAST**, es la cúspide técnica natural de nuestro ecosistema. Elimina silos, optimiza el consumo de RAM en Star VPS y deja a SAORI preparada para interactuar fluidamente con cualquier modelo de IA del mundo.
