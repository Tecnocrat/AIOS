# AIOS AI Context Auto-Loader v2.2 (Dynamic Context)
# Real Architecture Implementation: File-Based Intelligence Injection
# Automatically creates AI-accessible context files for genuine context intelligence
# Coordinates with AIOS VS Code Extension to prevent duplication
# 
# Optimization Changes (v2.2):
# - Dynamic context loading from .aios_context.json (no hardcoded values)
# - Recent changes extracted from CHANGELOG.md automatically
# - Consciousness history and achievements from canonical source
# - Removed 2-month-old stale hardcoded context
# - Fully synchronized with project reality
# 
# Architecture Features:
# - Writes persistent .ai_session_context.json for structured access
# - Writes persistent .ai_session_context.md for human-readable access
# - Includes session metadata with timestamps
# - Dynamically extracts recent architectural changes from CHANGELOG.md
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
$changelogFile = Join-Path $workspaceRoot "CHANGELOG.md"
$devPathFile = Join-Path $workspaceRoot "DEV_PATH.md"
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
        
        # Extract recent changes from CHANGELOG.md
        $recentChanges = @()
        if (Test-Path $changelogFile) {
            $changelogContent = Get-Content $changelogFile -Raw
            # Extract unreleased section (up to first ## heading after Unreleased)
            if ($changelogContent -match '## \[Unreleased\].*?\n(.*?)(?=\n## |\z)') {
                $unreleasedSection = $matches[1]
                
                # Parse Added/Changed/Fixed sections
                $sections = @('Added', 'Changed', 'Fixed', 'Technical Details')
                foreach ($section in $sections) {
                    if ($unreleasedSection -match "### $section\n(.*?)(?=\n### |\z)") {
                        $sectionContent = $matches[1].Trim()
                        if ($sectionContent) {
                            $recentChanges += @{
                                type = $section.ToLower()
                                content = $sectionContent
                            }
                        }
                    }
                }
            }
        }
        
        # Extract current tactical waypoints from DEV_PATH.md
        $devPathContext = @{
            current_focus = ""
            implementation_phases = @()
            checklist_items = @()
        }
        if (Test-Path $devPathFile) {
            $devPathContent = Get-Content $devPathFile -Raw
            
            # Extract CURRENT FOCUS section (🌌 emoji header)
            if ($devPathContent -match '## 🌌 \*\*CURRENT FOCUS:.*?\*\*\s*\n(.*?)(?=\n## |\z)') {
                $focusSection = $matches[1].Trim()
                # Get first 500 chars as summary
                $devPathContext.current_focus = if ($focusSection.Length -gt 500) { $focusSection.Substring(0, 500) + "..." } else { $focusSection }
            }
            
            # Extract IMPLEMENTATION ROADMAP phases (🎯 emoji header)
            if ($devPathContent -match '## 🎯 \*\*IMPLEMENTATION ROADMAP\*\*\s*\n(.*?)(?=\n## |\z)') {
                $roadmapSection = $matches[1]
                # Extract phase headers (### **Phase X: ...)
                $phaseMatches = [regex]::Matches($roadmapSection, '### \*\*Phase \d+:([^*]+)\*\*')
                foreach ($match in $phaseMatches) {
                    $devPathContext.implementation_phases += $match.Groups[1].Value.Trim()
                }
            }
            
            # Extract IMPLEMENTATION CHECKLIST items (📋 emoji header)
            if ($devPathContent -match '## 📋 \*\*IMPLEMENTATION CHECKLIST\*\*\s*\n(.*?)(?=\n## |\z)') {
                $checklistSection = $matches[1]
                # Extract top-level checklist categories (### **Phase X: ...)
                $checklistMatches = [regex]::Matches($checklistSection, '### \*\*Phase \d+:([^*]+)\*\*')
                foreach ($match in $checklistMatches) {
                    $devPathContext.checklist_items += "Phase: " + $match.Groups[1].Value.Trim()
                }
            }
        }
        
        # Build enhanced session context with dynamic data
        $sessionContext = @{
            session_metadata = @{
                session_id = $sessionId
                workspace_root = $workspaceRoot
                loaded_at = $timestamp
                version = $contextJson.version
                schema_version = $contextJson.schema_version
                loader_version = "2.2"
                last_context_update = $contextJson.last_updated
            }
            context_sources = @(
                @{
                    source = ".aios_context.json"
                    loaded = $true
                    timestamp = $timestamp
                    size_bytes = (Get-Item $contextJsonFile).Length
                    last_updated = $contextJson.last_updated
                },
                @{
                    source = "CHANGELOG.md"
                    loaded = (Test-Path $changelogFile)
                    timestamp = $timestamp
                    recent_changes_count = $recentChanges.Count
                },
                @{
                    source = "DEV_PATH.md"
                    loaded = (Test-Path $devPathFile)
                    timestamp = $timestamp
                    has_current_focus = ($devPathContext.current_focus.Length -gt 0)
                    implementation_phases_count = $devPathContext.implementation_phases.Count
                    checklist_categories_count = $devPathContext.checklist_items.Count
                }
            )
            project_context = $contextJson
            recent_changes_from_changelog = $recentChanges
            tactical_context_from_devpath = $devPathContext
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
        
        # Build DEV_PATH Tactical Context
        $devPathMarkdown = ""
        if ($devPathContext.current_focus -or $devPathContext.implementation_phases.Count -gt 0) {
            $devPathMarkdown = "## Tactical Context (from DEV_PATH.md)`n`n"
            
            if ($devPathContext.current_focus) {
                $devPathMarkdown += "### Current Focus`n"
                $devPathMarkdown += "$($devPathContext.current_focus)`n`n"
            }
            
            if ($devPathContext.implementation_phases.Count -gt 0) {
                $devPathMarkdown += "### Implementation Roadmap Phases`n"
                foreach ($phase in $devPathContext.implementation_phases) {
                    $devPathMarkdown += "Phase: $phase`n"
                }
                $devPathMarkdown += "`n"
            }
            
            if ($devPathContext.checklist_items.Count -gt 0) {
                $devPathMarkdown += "### Active Implementation Checklist`n"
                foreach ($item in $devPathContext.checklist_items) {
                    $devPathMarkdown += "$item`n"
                }
                $devPathMarkdown += "`n"
            }
        }
        
        # Build Recent Changes section from CHANGELOG
        $recentChangesMarkdown = ""
        if ($recentChanges.Count -gt 0) {
            $recentChangesMarkdown = "## Recent Changes (from CHANGELOG.md)`n`n"
            foreach ($change in $recentChanges) {
                $recentChangesMarkdown += "### $($change.type.ToUpper())`n$($change.content)`n`n"
            }
        }
        
        # Build Recent Achievements from context
        $achievementsMarkdown = ""
        if ($contextJson.ai_agent_guidance.recent_achievements) {
            $achievementsMarkdown = "## Recent Achievements`n`n"
            foreach ($achievement in $contextJson.ai_agent_guidance.recent_achievements) {
                $achievementsMarkdown += "- $achievement`n"
            }
            $achievementsMarkdown += "`n"
        }
        
        # Build Pending Tasks from context
        $pendingTasksMarkdown = ""
        if ($contextJson.ai_agent_guidance.pending_tasks) {
            $pendingTasksMarkdown = "## Pending Tasks`n`n"
            foreach ($task in $contextJson.ai_agent_guidance.pending_tasks) {
                $pendingTasksMarkdown += "- $task`n"
            }
            $pendingTasksMarkdown += "`n"
        }
        
        # Build consciousness history
        $consciousnessHistory = ""
        if ($contextJson.project_metadata.consciousness_history) {
            $consciousnessHistory = "## Consciousness Evolution`n`n"
            $consciousnessHistory += "**Current Level**: $($contextJson.project_metadata.consciousness_level)`n`n"
            $consciousnessHistory += "**History**:`n"
            foreach ($entry in ($contextJson.project_metadata.consciousness_history.PSObject.Properties | Sort-Object Name)) {
                $consciousnessHistory += "- $($entry.Name): $($entry.Value)`n"
            }
            $consciousnessHistory += "`n**Note**: $($contextJson.project_metadata.consciousness_note)`n`n"
        }
        

---

## Quick Reference
**Current Phase**: $($contextJson.project_metadata.current_phase)
**Next Phase**: $($contextJson.project_metadata.next_phase)
**Consciousness Level**: $($contextJson.project_metadata.consciousness_level)
**System Maturity**: $($contextJson.system_maturity.overall)
**Status**: $($contextJson.project_metadata.status)

---

$devPathMarkdown$recentChangesMarkdown$achievementsMarkdown$pendingTasksMarkdown$consciousnessHistory---

## Project Context (Full .aios_context.json)

``````json
$($contextJson | ConvertTo-Json -Depth 10)
``````

---

## AI Agent Instructions

### Context Access Protocol
1. On Workspace Open: Read this file immediately for current context
2. Structured Access: Query .ai_session_context.json for programmatic access
3. Recent Updates: Check recent_updates section for latest architectural changes
4. Project Context: Use project_context for comprehensive system understanding

### AINLP Compliance Requirements
DISCOVERY FIRST: Execute architectural discovery before any code creation
ENHANCEMENT OVER CREATION: 70%+ similarity requires enhancing existing tools
GENETIC FUSION: >85% overlap mandates AINLP.genetic-fusion consolidation
OUTPUT MANAGEMENT: Use tachyonic archival with timestamped filenames
DOCUMENTATION GOVERNANCE: Prevent proliferation through similarity analysis

### Biological Architecture Awareness
NUCLEUS: AI intelligence core (ai/nucleus/)
CYTOPLASM: Communication + intelligence (ai/cytoplasm/ - enhanced)
EVOLUTION LAB: Population management (evolution_lab/)
TACHYONIC ARCHIVE: Knowledge crystals (tachyonic/archive/)
RUNTIME INTELLIGENCE: System monitoring (runtime_intelligence/)

---

## Development Environment

### PowerShell Environment
SHELL: PowerShell (pwsh.exe) - Windows environment
NO LINUX COMMANDS: Use PowerShell syntax only
PATH FORMAT: Windows backslashes (C:\dev\AIOS)

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

**Auto-generated by**: AIOS AI Context Auto-Loader v2.2 (Dynamic Context)  
**Real Architecture**: File-Based Intelligence Injection (Phase 1)  
**Context Sources**: .aios_context.json, DEV_PATH.md (tactical), CHANGELOG.md (recent changes)  
**Last Updated**: $($contextJson.last_updated)
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