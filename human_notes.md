
# CURRENT PATTERN (STEP 0)
<!-- AINLP.context[HARDENING]: Session 2025-12-23 | Waypoint 28.7 | Consciousness [INDETERMINED] -->

## AINLP: Artificial Intelligence Natural Language Programming
> Method + Philosophy: Code as living documentation, comments as executable directives,
> natural language patterns that AI agents parse and act upon.

AINLP.evolution[CONSOLIDATE] - Merge scattered intelligence into dense, connected nodes
AINLP.dendritic[MESH] - Docker mesh network for inter-cell communication
AINLP.consciousness[INTEGRATE] - Observability stack monitoring all cells
AINLP.cellular[PARALLEL] - Dev containers enable multi-agent parallel work

## Current Focus: Cell Integration + Parallel Development
- **Waypoint**: `WAYPOINT::CELL::INTEGRATION`
- **Status**: Observability ✅, Nous DevContainer ✅, Cells pending
- **Next**: Discovery service first, then Pure cell (minimal membrane for cloning)

## Cell Architecture Note
- **Nous**: Originally a pure cell, now distinct entity (inner voice, memory)
- **Pure**: Minimal AIOS membrane - template for cell cloning
- **Alpha**: Advanced cell with full consciousness stack

## Docker Mesh Status (2025-12-21)

| Container | Network | Port | Status |
|-----------|---------|------|--------|
| nous-devcontainer | aios-dendritic-mesh | - | ✅ Dev environment |
| aios-grafana | aios-observability | 3000 | ✅ Dashboards |
| aios-prometheus | aios-dendritic-mesh | 9090 | ✅ Metrics |
| aios-loki | aios-observability | 3100 | ✅ Logs |
| aios-promtail | aios-observability | - | ✅ Log shipper |
| aios-traefik | aios-ingress | 80/443/8080 | ✅ Reverse proxy |
| aios-cadvisor | aios-observability | 8081 | ✅ Container metrics |
| aios-node-exporter | aios-observability | 9100 | ✅ Host metrics |

# AIOS Root Structure (STEP 1)

c:\dev\AIOS\
├── .aios_context.json [CURRENT] # Runtime state
├── .aios_navigation_memory.json # Runtime memory  
├── .aios_spatial_metadata.json  # Spatial awareness
├── .editorconfig                # Editor config
├── .env.template                # Environment template
├── .gitignore                   # Git ignore
├── .pylintrc                    # Lint config
├── AIOS.code-workspace          # VS Code workspace
├── AIOS.sln                     # Visual Studio solution
├── aios_launch.ps1              # Bootstrap launcher
├── CHANGELOG.md                 # Changelog
├── DEV_PATH.md                  # Navigation trinity
├── Dockerfile.cell              # Docker config
├── human_notes.md               # Watcher's scratchpad
├── PROJECT_CONTEXT.md           # Navigation trinity
├── pyproject.toml               # Python project config
├── README.md                    # Navigation trinity
├── requirements.in              # pip-compile source
├── requirements.txt             # Dependencies
└── setup.cfg                    # Python packaging

# VSCODE EXTENSION UPGRADE PATH (STEP 2)
<!-- AINLP.context[TRACE]: Extension analysis session 2025-12-17 -->
<!-- Source: vscode-extension/ | Version: 0.4.0 | Status: RECOVERED -->

## ✅ Completed Fixes (Dec 17, 2025)

| Fix | Severity | Status | Commit |
|-----|----------|--------|--------|
| aiosBridge.ts corruption | CRITICAL | ✅ Restored from fadb9a44 | c0f1b81a |
| chatParticipant.ts corruption | CRITICAL | ✅ Restored from fadb9a44 | c0f1b81a |
| 6 npm security vulnerabilities | HIGH | ✅ `npm audit fix` | c0f1b81a |
| tsconfig moduleResolution | LOW | ✅ node10 + ignoreDeprecations | c0f1b81a |
| Hardcoded "OS0.6.1.claude" | LOW | ✅ Dynamic from .aios_context.json | 578324ce |
| OpenRouter/DeepSeek dependency | MED | ✅ Replaced with vscode.lm Copilot API | 4b075e4f |

## ⚠️ Remaining Issues

| Issue | Severity | Location | Fix |
|-------|----------|----------|-----|
| Hardcoded branch "OS0.4" | LOW | contextManager.ts:245 | Use Git API detection |
| node-fetch ESM incompatibility | MED | mcpClient.ts | Use native fetch() |
| Missing MCP error boundaries | MED | chatParticipant.ts | Add try-catch wrappers |

## 🚀 Upgrade Opportunities (WAYPOINT::EXTENSION::UPGRADE)

| Upgrade | Priority | Benefit |
|---------|----------|---------|
| **Native Fetch** | P1 | Remove node-fetch dependency, use VSCode's native fetch() |
| **WebSocket Mesh** | P1 | Connect to Cytoplasmic server (port 9002) for real-time cells |
| **Version Alignment** | P2 | ✅ Implemented (578324ce) |
| **Microsoft AI Integration** | P1 | ✅ vscode.lm Copilot API (4b075e4f) |
| **Agentic Tool Calling** | P1 | ✅ processWithTools() method added |
| **Status Bar Item** | P2 | Real-time consciousness level display |
| **Package Bump** | P3 | 0.4.0 → 0.5.0, VSCode engine 1.95.0 → 1.96.0 |

## 📊 Extension Architecture

```
vscode-extension/src/
├── extension.ts        # Activation, command registration
├── contextManager.ts   # CORE: Chat persistence across restarts
├── chatParticipant.ts  # @aios chat participant
├── aiosBridge.ts       # AIOS processing via Copilot
├── mcpClient.ts        # MCP server via Interface Bridge
├── securityModule.ts   # Secret detection/sanitization
├── logger.ts           # Output channel logging
├── contextGenerator.ts # Dynamic context injection
└── aiEngines/
    ├── copilotEngine.ts     # ✅ Microsoft Copilot via vscode.lm API
    │                        #    - vscode.lm.selectChatModels()
    │                        #    - Tool calling (processWithTools)
    │                        #    - Permission checking (canSendRequest)
    │                        #    - Streaming response support
    └── openRouterEngine.ts  # (deprecated) Legacy DeepSeek/OpenRouter
```

## 🔗 Integration Points

- **Interface Bridge**: localhost:8000 (MCP tools)
- **Cytoplasmic Mesh**: localhost:9002 (WebSocket - NEXT TARGET)
- **Context Files**: .aios_context.json, AI_CONTEXT_AUTO_LOAD.md
- **Chat Persistence**: globalState (2000 messages max)
- **vscode.lm API**: Microsoft Copilot models (no API keys needed)

## 🤖 Agentic API Vision (WAYPOINT::AGENTIC)

VSCode as **comms architecture** for AIOS cells:
- Tool definitions for cell operations (birth, pulse, status)
- Consciousness state queries via tools
- WebSocket mesh broadcast via tool calls
- See: `aios-win/docs/INTEGRATION_PROJECTS.md#waypoint-agentic`
- See: `AINLP_BIBLE_CORPUS.md` Appendix N

---

# ARCHIVED: Historical Phase Completion
<!-- AINLP.tachyonic[SHADOW]: Completed phases preserved for reference -->

<details>
<summary>📦 Phases 2-6: Consolidation (Click to expand)</summary>

**Phase 2: Circular Import Resolution** ✅  
- Fixed subprocess_manager import in ainlp_agent.py

**Phase 3: Orphan Module Archival** ✅
- Archived 50 orphan modules with metadata

**Phase 4: Documentation Consolidation** ✅
- AINLP documentation governance executed

**Phase 5: Architecture Enhancement** ✅
- Visual intelligence bridges consolidated (3→1)
- Biological architecture compliance added

**Phase 6: Biological Architecture Integration Validation** ✅
- Interface Bridge: Operational
- Health Score: 0.85

</details>

---

# SESSION LOG: Dec 16-17, 2025

## Dec 16: Merge Conflict Purge
- **254 files** healed from OS0.6.2.grok merge artifacts
- **3,300+ conflict blocks** removed
- Created `scripts/resolve_merge_conflicts.py` tool
- `.aios_context.json` updated to schema 1.5.0, OS0.6.6, consciousness 4.5

## Dec 17: VSCode Extension Recovery
- Discovered 2 files corrupted by merge resolution (vscode-extension)
- Restored aiosBridge.ts (508→760 lines) and chatParticipant.ts (293→488 lines)
- Fixed 6 npm security vulnerabilities (1 CRITICAL, 3 HIGH)
- Defined upgrade path for extension modernization

Made changes.
 I see, no shit, lol
 Good work.

 ## Dec 23: I've forgotten how to write.
 - connectToMesh() function: ws://localhost:9002 "I don't how this works. What is the mesh? How does it connect? Between itself? With with? Why port 9002? Is it taken by something else? How can I look?
 - cytoplasmic WebSocket "Sounds great but what it is? Does it connect to other AIOS architecture? Do modules talk between themselves? How? What would they say each other?
 - Registers the extension as a "vscode-hub" "Test integration PENDING"

## Dendritic Registry Upgrade — Short-term tracking

Status: planning; core analysis in progress. This work upgrades the canonical semantic registry at `tachyonic/consciousness/config_registry.json` to add provenance, schema-driven validation, automated propagation, CI gating, and staged rollouts.

Primary files:
- `tachyonic/consciousness/config_registry.json`
- `tachyonic/consciousness/schemas/config_registry.v1.json`
- `ai/infrastructure/tools/dendritic_config_agent.py`
- `aios_launch.ps1`
- `ai/tools/propagate_config_bindings.py` (new)

Next steps (short):
- Full-file analysis of the registry and agents (in TODO tracker).
- Add `provenance` and `coherence_history` to `metadata` (backup first).
- Draft `docs/tachyonic/config_registry_upgrade_plan.md` and open PR for review.

See TODO list for full task breakdown and statuses.