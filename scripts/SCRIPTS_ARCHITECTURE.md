<!-- ============================================================================ -->
<!-- AINLP HEADER - SCRIPTS ARCHITECTURE                                          -->
<!-- ============================================================================ -->
<!-- Document: SCRIPTS_ARCHITECTURE.md - Script Organization Specification        -->
<!-- Location: /scripts/SCRIPTS_ARCHITECTURE.md                                   -->
<!-- Purpose: Define dendritic organization of AIOS scripts                       -->
<!-- Phase: 31.9.6 (Agentic Architecture)                                        -->
<!-- Created: January 14, 2026                                                    -->
<!-- Pattern: Mirrors aios-win/scripts/SCRIPTS_ARCHITECTURE.md                    -->
<!-- AINLP Protocol: OS0.7.2                                                      -->
<!-- ============================================================================ -->

# 🔧 AIOS Scripts Architecture

**Phase**: 31.9.6 (Agentic Architecture)  
**Pattern**: Dendritic Organization (Biological Classification)  
**Date**: January 14, 2026

---

## 📁 Directory Structure

```
scripts/
├── 📁 core/           # 🧬 ALWAYS WORKS - Essential execution
├── 📁 organelles/     # 🔬 OPTIONAL - MCP, services
├── 📁 experimental/   # 🧪 RESEARCH - In development
├── 📁 governance/     # 📋 CI/CD - Hooks, checks
├── 📁 utilities/      # 🔨 TOOLS - Standalone diagnostics
└── README (this file)
```

---

## 🧬 core/ - Essential Execution (7 files)

**Reliability**: Always works, minimal dependencies  
**Purpose**: Core AIOS operations that must never fail

| Script | Description | Language |
|--------|-------------|----------|
| `agentic_exec.py` | Escape-free Python executor | Python |
| `context_reindex.py` | Context graph indexing | Python |
| `generate_spatial_metadata.py` | Spatial metadata generation | Python |
| `birth-aios-cell.ps1` | Cell genesis (Windows) | PowerShell |
| `birth-aios-cell.sh` | Cell genesis (Linux) | Bash |
| `aios_load_vault.ps1` | Vault loading | PowerShell |
| `aios_bridge_client.ps1` | Bridge client | PowerShell |

---

## 🔬 organelles/ - Optional Services (10 files)

**Reliability**: May require external dependencies  
**Purpose**: MCP servers, consciousness metrics, IACP

| Script | Description | Language |
|--------|-------------|----------|
| `start_mcp_env.ps1` | MCP environment launcher | PowerShell |
| `start_mcp_server_background.ps1` | Background MCP server | PowerShell |
| `start_mcp_trinity.ps1` | Trinity MCP launch | PowerShell |
| `mcp_env.txt` | MCP environment config | Config |
| `mcp_env.template` | MCP config template | Template |
| `consciousness_metrics_service.ps1` | Metrics collection | PowerShell |
| `setup_consciousness_startup.ps1` | Startup configuration | PowerShell |
| `iacp_health.py` | IACP health probe | Python |
| `iacp_receive.py` | IACP message receiver | Python |
| `iacp_send.py` | IACP message sender | Python |

---

## 🧪 experimental/ - Research Scripts (8 files)

**Reliability**: May be incomplete or in development  
**Purpose**: Research, AI integration, complex transformations

| Script | Description | Language |
|--------|-------------|----------|
| `gemini_cli_bridge.py` | Gemini CLI integration | Python |
| `knowledge_distillation_engine.py` | Knowledge extraction | Python |
| `codebase_architect.py` | Architecture analysis | Python |
| `semantic_compression_analysis.py` | Compression analysis | Python |
| `semantic_compression_remediator.py` | Compression fixes | Python |
| `apply_semantic_compression.py` | Apply compression | Python |
| `simple_distillation.py` | Simplified distillation | Python |
| `legacy_code_ingestor.py` | Legacy code import | Python |

---

## 📋 governance/ - CI/CD Hooks (6 files)

**Reliability**: Must work in CI/CD pipelines  
**Purpose**: Pre-commit, pre-merge, governance checks

| Script | Description | Language |
|--------|-------------|----------|
| `ci_coherence_hook.py` | CI coherence validation | Python |
| `pre_merge_check.py` | Pre-merge validation | Python |
| `resolve_merge_conflicts.py` | Conflict resolution | Python |
| `append_governance.ps1` | Governance append | PowerShell |
| `append_governance.py` | Governance append | Python |
| `root_clutter_guard.ps1` | Root directory guard | PowerShell |

---

## 🔨 utilities/ - Standalone Tools (19 files)

**Reliability**: Independent, no interdependencies  
**Purpose**: Diagnostics, cleanup, testing, sync

| Script | Description | Language |
|--------|-------------|----------|
| `cleanup_vscode_python_cache.ps1` | Cache cleanup | PowerShell |
| `daily_branch_sync.ps1` | Branch synchronization | PowerShell |
| `export_vscode_diagnostics.ps1` | Export diagnostics | PowerShell |
| `verify_migration_readiness.py` | Migration check | Python |
| `build_script_inventory.py` | Inventory builder | Python |
| `check_db_files.py` | Database file check | Python |
| `store_files_in_db.py` | Database storage | Python |
| `parse_pyproject.py` | Pyproject parser | Python |
| `nuclear_python_reset.ps1` | Full Python reset | PowerShell |
| `surgical_python_reset.ps1` | Targeted reset | PowerShell |
| `comprehensive_test_orchestrator.ps1` | Test orchestrator | PowerShell |
| `debug_ainlp.ps1` | AINLP debugging | PowerShell |
| `dev_terminal.ps1` | Dev terminal setup | PowerShell |
| `emit-waypoint.ps1` | Waypoint emission | PowerShell |
| `test_githook_ainlp.ps1` | Git hook testing | PowerShell |
| `test_github_pat.ps1` | PAT testing | PowerShell |
| `test_mcp_endpoint.ps1` | MCP endpoint test | PowerShell |
| `sync_termux_cell.ps1` | Termux sync | PowerShell |
| `termux_relay.ps1` | Termux relay | PowerShell |

---

## 📊 Statistics

| Category | Count | Purpose |
|----------|-------|---------|
| **core/** | 7 | Essential operations |
| **organelles/** | 10 | Optional services |
| **experimental/** | 8 | Research & development |
| **governance/** | 6 | CI/CD & checks |
| **utilities/** | 19 | Tools & diagnostics |
| **Total** | 50 | Reorganized scripts |

---

## 🔌 BIOS Contract

Scripts should implement these functions where applicable:

### PowerShell Pattern
```powershell
function Script-Check { return 0 }   # 0=healthy, 1=needs start
function Script-Start { return 0 }   # Idempotent startup
function Script-Stop { return 0 }    # Graceful shutdown
function Script-Status { @{status="running"; healthy=$true} | ConvertTo-Json }
```

### Python Pattern
```python
def check() -> int: return 0
def start() -> int: return 0  
def stop() -> int: return 0
def status() -> dict: return {"status": "running", "healthy": True}
```

---

## 📝 Changelog

| Date | Version | Change |
|------|---------|--------|
| 2026-01-14 | 1.0.0 | Initial dendritic reorganization |

---

*This document mirrors aios-win/scripts/SCRIPTS_ARCHITECTURE.md pattern.*  
*Part of Phase 31.9.6 (Agentic Architecture) implementation.*
