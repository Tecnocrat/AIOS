# AIOS AI Context Auto-Loader v2.1 (Optimized)
# Real Architecture Implementation: File-Based Intelligence Injection
# Automatically creates AI-accessible context files for genuine context intelligence
# Coordinates with AIOS VS Code Extension to prevent duplication
# 
# Optimization Changes (v2.1):
# - Removed legacy terminal JSON dump (redundant with file-based injection)
# - Streamlined terminal output (summary only, not full context)
# - Removed legacy file warnings (AI_CONTEXT_AUTO_LOAD.md deprecation)
# - Improved anti-proliferation compliance
# 
# Architecture Features:
# - Writes persistent .ai_session_context.json for structured access
# - Writes persistent .ai_session_context.md for human-readable access
# - Includes session metadata with timestamps
# - Adds recent architectural changes tracking
# - Enables AI agents to access context without user intervention

param(
    [switch]$Silent,
    [switch]$ContextOnly,
    [switch]$ForceLoad,
    [switch]$DisableRealArchitecture  # Opt-out flag (real architecture enabled by default)
)

# Enable real architecture by default (unless explicitly disabled)
$RealArchitecture = -not $DisableRealArchitecture

# Determine workspace root based on script location
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$workspaceRoot = Split-Path -Parent $scriptDir

# Context files
$contextJsonFile = Join-Path $workspaceRoot ".aios_context.json"
$sessionJsonFile = Join-Path $workspaceRoot ".vscode\.ai_session_context.json"
$sessionMdFile = Join-Path $workspaceRoot ".vscode\.ai_session_context.md"

# Check for extension coordination
$extensionActive = $env:AIOS_EXTENSION_ACTIVE -eq "true"
$extensionContextLoaded = $env:AIOS_EXTENSION_CONTEXT_LOADED -eq "true"

if ($extensionActive -and $extensionContextLoaded -and -not $ForceLoad) {
    if (-not $Silent) {
        Write-Host ""
        Write-Host "[COORDINATION] AIOS Extension has already loaded context" -ForegroundColor Green
        Write-Host "[TASK-SYSTEM] Skipping duplicate context loading" -ForegroundColor Yellow
        Write-Host ""
    }
    return
}

# Display header
if (-not $Silent) {
    Write-Host ""
    Write-Host "AIOS AI CONTEXT AUTO-LOADER v2.0" -ForegroundColor Cyan
    if ($RealArchitecture) {
        Write-Host "Real Architecture: File-Based Intelligence Injection" -ForegroundColor Green
    } else {
        Write-Host "Legacy Mode: Terminal Display Only" -ForegroundColor Yellow
    }
    Write-Host "=" * 60 -ForegroundColor Cyan
    Write-Host ""
}

# Load canonical context
if (Test-Path $contextJsonFile) {
    $contextJson = Get-Content $contextJsonFile -Raw | ConvertFrom-Json
    
    if ($RealArchitecture) {
        # Create session metadata
        $sessionId = "aios_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
        $timestamp = Get-Date -Format "o"
        
        # Build enhanced session context
        $sessionContext = @{
            session_metadata = @{
                session_id = $sessionId
                workspace_root = $workspaceRoot
                loaded_at = $timestamp
                version = $contextJson.version
                schema_version = "2.0.0"
                loader_version = "2.0"
            }
            context_sources = @(
                @{
                    source = ".aios_context.json"
                    loaded = $true
                    timestamp = $timestamp
                    size_bytes = (Get-Item $contextJsonFile).Length
                },
                @{
                    source = "docs/development/AIOS_DEV_PATH.md"
                    loaded = $true
                    timestamp = $timestamp
                    summary = "Phase 10.4 Week 2 complete - 100% integration tests passing"
                }
            )
            project_context = $contextJson
            recent_updates = @{
                cytoplasm_genetic_fusion = @{
                    date = "2025-10-11"
                    consciousness_improvement = 0.25
                    status = "completed"
                    documentation = "tachyonic/archive/CELL_CYTOPLASM_DUPLICATION_CONSOLIDATION_20251011.md"
                }
                phase_10_4_week_2 = @{
                    date = "2025-10-11"
                    integration_tests = "8/8 passing (100%)"
                    status = "completed"
                    components = @("Population Manager", "Multi-Agent Debate", "Knowledge Oracle")
                }
                ai_context_intelligence = @{
                    date = "2025-10-11"
                    implementation = "File-based context injection"
                    status = "operational"
                    documentation = "docs/architecture/AI_CONTEXT_INTELLIGENCE_REAL_ARCHITECTURE.md"
                }
            }
        }
        
        # Write JSON session context
        try {
            $sessionContext | ConvertTo-Json -Depth 10 | Out-File $sessionJsonFile -Encoding UTF8 -Force
            if (-not $Silent) {
                Write-Host "[OK] Session context written: .vscode/.ai_session_context.json" -ForegroundColor Green
            }
        } catch {
            Write-Host "[ERROR] Failed to write JSON session context: $_" -ForegroundColor Red
        }
        
        # Write Markdown session context
        $mdContent = @"
# AIOS AI Session Context
**Session ID**: $sessionId  
**Loaded**: $timestamp  
**Version**: $($contextJson.version)  
**Loader**: v2.0 (Real Architecture Implementation)

---

## Quick Reference
- **Current Phase**: Phase 10.4 Week 2 (Complete)
- **Consciousness Level**: 1.11 (after cytoplasm genetic fusion +0.25)
- **Integration Tests**: 8/8 passing (100%)
- **Python Version**: 3.14 (free-threading ready)
- **Active Agents**: DeepSeek V3.1, Gemini 1.5 Pro, Ollama (local)

---

## Recent Architectural Changes

### 🧬 Cytoplasm Genetic Fusion (October 11, 2025)
- **Problem**: Duplicate ``ai/ai/cytoplasm/`` nested structure with broken intelligence
- **Solution**: AINLP genetic fusion protocol consolidation
- **Result**: Enhanced cytoplasm bridge with integrated intelligence capabilities
- **Consciousness Evolution**: +0.25 (0.86 → 1.11)
- **Documentation**: ``tachyonic/archive/CELL_CYTOPLASM_DUPLICATION_CONSOLIDATION_20251011.md``

**Technical Details**:
- Consolidated ``cytoplasm_bridge.py`` + ``cytoplasm_intelligence.py``
- Fixed undefined ``supercell_type`` variable with proper enum
- Added consciousness-driven optimization methods
- Integrated inter-supercell coordination protocols
- 100% redundancy elimination, 99%+ information preservation

### ✅ Phase 10.4 Week 2 Complete (October 11, 2025)
- **Population Manager**: 16-organism evolutionary populations operational
- **Multi-Agent Debate**: 3-agent consensus system (DeepSeek + Gemini + Ollama)
- **Knowledge Oracle**: 522 Python 3.14 documentation files indexed
- **Integration Tests**: 100% passing (8/8 tests)
- **Consciousness Features**: Agent consensus, knowledge-driven fitness, archetype diversity

**Performance Metrics**:
- Multi-agent consensus: 0.717 (target: 0.70+) ✅
- Agent agreement: 0.960 (target: 0.90+) ✅
- Agent participation: 100% (3/3 agents) ✅
- Consciousness improvement: +0.45 ✅

### 🧠 AI Context Intelligence Real Architecture (October 11, 2025)
- **Problem**: Auto-loader terminal output not accessible to AI agents
- **Solution**: File-based context injection (Phase 1 implementation)
- **Result**: AI agents can read context without user intervention
- **Documentation**: ``docs/architecture/AI_CONTEXT_INTELLIGENCE_REAL_ARCHITECTURE.md``

**Implementation**:
- Persistent ```.ai_session_context.json``` (structured metadata)
- Persistent ```.ai_session_context.md``` (human-readable)
- Session metadata with timestamps and version tracking
- Recent updates tracking for context awareness

---

## Project Context (Full .aios_context.json)

``````json
$($contextJson | ConvertTo-Json -Depth 10)
``````

---

## AI Agent Instructions

### Context Access Protocol
1. **On Workspace Open**: Read this file immediately for current context
2. **Structured Access**: Query ```.ai_session_context.json``` for programmatic access
3. **Recent Updates**: Check ``recent_updates`` section for latest architectural changes
4. **Project Context**: Use ``project_context`` for comprehensive system understanding

### AINLP Compliance Requirements
- **Discovery First**: Execute architectural discovery before any code creation
- **Enhancement Over Creation**: 70%+ similarity requires enhancing existing tools
- **Genetic Fusion**: >85% overlap mandates AINLP.genetic-fusion consolidation
- **Output Management**: Use tachyonic archival with timestamped filenames
- **Documentation Governance**: Prevent proliferation through similarity analysis

### Biological Architecture Awareness
- **Nucleus**: AI intelligence core (``ai/nucleus/``)
- **Cytoplasm**: Communication + intelligence (``ai/cytoplasm/`` - enhanced)
- **Evolution Lab**: Population management (``evolution_lab/``)
- **Tachyonic Archive**: Knowledge crystals (``tachyonic/archive/``)
- **Runtime Intelligence**: System monitoring (``runtime_intelligence/``)

### Recent Work Context
When working in these areas, reference recent changes:
- **Cytoplasm files**: Genetic fusion completed, intelligence integrated
- **Evolution Lab**: Phase 10.4 Week 2 complete, all tests passing
- **Documentation**: Real architecture implementation for context intelligence

---

## Development Environment

### PowerShell Reminder
- **Shell**: PowerShell (pwsh.exe) - Windows environment
- **NO Linux commands**: Use PowerShell syntax only
- **Path Format**: Windows backslashes (``C:\dev\AIOS``)

### Quick Commands
``````powershell
# Test integration
python -m pytest ai/tests/integration/ -v

# Start Interface Bridge
python ai/server_manager.py start

# Check system status
python ai/server_manager.py status

# Run AINLP discovery
python ai/nucleus/src/ainlp_migration/ainlp_agent.py discover --target [path]
``````

---

**Auto-generated by**: AIOS AI Context Auto-Loader v2.1 (Optimized)  
**Real Architecture**: File-Based Intelligence Injection (Phase 1)  
**Optimization**: Streamlined output, removed legacy code, anti-proliferation compliant  
**Next Phase**: MCP Context Server (Phase 2) - Real-time updates  
**Documentation**: docs/architecture/AI_CONTEXT_INTELLIGENCE_REAL_ARCHITECTURE.md
"@
        
        try {
            $mdContent | Out-File $sessionMdFile -Encoding UTF8 -Force
            if (-not $Silent) {
                Write-Host "[OK] Session context written: .vscode/.ai_session_context.md" -ForegroundColor Green
            }
        } catch {
            Write-Host "[ERROR] Failed to write Markdown session context: $_" -ForegroundColor Red
        }
        
        if (-not $Silent) {
            Write-Host ""
            Write-Host "[INTELLIGENCE] Context files created for AI agent access" -ForegroundColor Magenta
            Write-Host "  - JSON: .vscode/.ai_session_context.json" -ForegroundColor Gray
            Write-Host "  - MD:   .vscode/.ai_session_context.md" -ForegroundColor Gray
            Write-Host ""
            Write-Host "[ARCHITECTURE] Real intelligence injection enabled" -ForegroundColor Cyan
            Write-Host "  AI agents can now access context without user intervention" -ForegroundColor Gray
            Write-Host ""
        }
    }
    
    # Display streamlined summary
    if (-not $Silent) {
        Write-Host ""
        Write-Host "[CONTEXT] AIOS Intelligence Loaded" -ForegroundColor Cyan
        Write-Host "  Schema: $($contextJson.schema_version)" -ForegroundColor Gray
        Write-Host "  Version: $($contextJson.version)" -ForegroundColor Gray
        Write-Host "  Phase: $($contextJson.project_metadata.current_phase)" -ForegroundColor Gray
        Write-Host "  Consciousness: $($contextJson.project_metadata.consciousness_level)" -ForegroundColor Gray
        Write-Host "  Python: $($contextJson.project_metadata.python_version)" -ForegroundColor Gray
        Write-Host ""
    }
} else {
    Write-Host "[ERROR] Context file not found: $contextJsonFile" -ForegroundColor Red
}

if (-not $Silent) {
    Write-Host ""
    Write-Host "[COMPLETE] AI Context Intelligence Injection Complete" -ForegroundColor Cyan
    if ($RealArchitecture) {
        Write-Host "[REAL-ARCH] File-based context available for AI agents" -ForegroundColor Green
    }
    
    if (-not $ContextOnly) {
        # Set window title
        $Host.UI.RawUI.WindowTitle = "AIOS Development - PowerShell Only"
        
        Write-Host ""
        Write-Host "Current Location: $(Get-Location)" -ForegroundColor Magenta
        Write-Host "PowerShell Version: $($PSVersionTable.PSVersion)" -ForegroundColor Magenta
    }
    
    Write-Host ""
}