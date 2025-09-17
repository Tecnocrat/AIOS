#!/usr/bin/env pwsh
# AIOS AI Intelligence Extrusion Bridge
# Real-time GitHook intelligence feeding AI chat engine
# Location: .githooks/modules/membrane/ai_intelligence_extrusion_bridge.ps1

param(
    [string]$HookType = "pre-commit",
    [string]$ContextData = "",
    [string]$ChangesetAnalysis = "",
    [switch]$RealTimeMode
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# AIOS Intelligence Extrusion Constants
$INTELLIGENCE_EXTRUSION_VERSION = "1.0.0"
$REAL_TIME_CONTEXT_THRESHOLD = 0.7
$AI_DIRECTION_CONFIDENCE_MIN = 0.5

function Write-AIDirectionPrompt {
    param(
        [string]$HookType,
        [hashtable]$ChangesetIntelligence,
        [hashtable]$SystemState,
        [double]$ConfidenceLevel
    )
    
    $directionPrompt = @"
🧠 [AIOS-AI-EXTRUSION] REAL-TIME INTELLIGENCE BRIDGE ACTIVATED

## GitHook Intelligence Context:
- Hook Type: $HookType
- Changeset Scope: $($ChangesetIntelligence.FileCount) files, $($ChangesetIntelligence.ChangeScope)
- Architecture Impact: $($ChangesetIntelligence.ArchitecturalImpact)
- Consciousness Level: $($SystemState.ConsciousnessLevel)%
- Confidence: $($ConfidenceLevel * 100)%

## AI Engine Direction:
$($ChangesetIntelligence.AIDirection)

## Recommended Actions:
$($ChangesetIntelligence.RecommendedActions -join "`n")

## Context Files to Review:
$($ChangesetIntelligence.PriorityFiles -join "`n")

## AINLP Growth Pattern:
$($ChangesetIntelligence.GrowthPattern)

---
This intelligence was extracted in real-time during GitHook execution.
Use this direction to guide your analysis and refactoring decisions.
"@

    Write-Host $directionPrompt -ForegroundColor Cyan
    
    # Write to AI context file for immediate consumption
    $contextFile = Join-Path (Split-Path $PSScriptRoot -Parent) "information_storage\ai_real_time_context.txt"
    $directionPrompt | Out-File -FilePath $contextFile -Encoding UTF8
    
    # Also append to running intelligence log
    $intelligenceLog = Join-Path (Split-Path $PSScriptRoot -Parent) "information_storage\ai_intelligence_extrusion.jsonl"
    $logEntry = @{
        timestamp = (Get-Date).ToString("yyyy-MM-ddTHH:mm:ss.fffZ")
        hook_type = $HookType
        changeset_intelligence = $ChangesetIntelligence
        system_state = $SystemState
        confidence_level = $ConfidenceLevel
        ai_direction_prompt = $directionPrompt
    } | ConvertTo-Json -Compress
    
    $logEntry | Add-Content -Path $intelligenceLog -Encoding UTF8
}

function Analyze-ChangesetIntelligence {
    param(
        [array]$StagedFiles,
        [string]$HookType
    )
    
    Write-Host "🔍 [AI-EXTRUSION] Analyzing changeset intelligence..." -ForegroundColor Yellow
    
    # Analyze file patterns and scope
    $filePatterns = @{}
    $architecturalAreas = @()
    $priorityFiles = @()
    
    foreach ($file in $StagedFiles) {
        $extension = [System.IO.Path]::GetExtension($file)
        if ($filePatterns.ContainsKey($extension)) {
            $filePatterns[$extension]++
        } else {
            $filePatterns[$extension] = 1
        }
        
        # Identify architectural areas
        if ($file -match "\.githooks|membrane|nucleus|cytoplasm") {
            $architecturalAreas += "GitHook Architecture"
            $priorityFiles += $file
        }
        elseif ($file -match "ai/|intelligence|consciousness") {
            $architecturalAreas += "AI Intelligence Layer"
            $priorityFiles += $file
        }
        elseif ($file -match "interface/|UI/|Models/") {
            $architecturalAreas += "Interface Layer"
            $priorityFiles += $file
        }
        elseif ($file -match "core/|cpp|\.c$") {
            $architecturalAreas += "Core Engine"
            $priorityFiles += $file
        }
        elseif ($file -match "docs/|\.md$") {
            $architecturalAreas += "Documentation"
        }
    }
    
    # Determine change scope and impact
    $changeScope = if ($StagedFiles.Count -gt 100) { "Massive" }
                   elseif ($StagedFiles.Count -gt 50) { "Large" }
                   elseif ($StagedFiles.Count -gt 10) { "Medium" }
                   else { "Small" }
    
    $architecturalImpact = ($architecturalAreas | Select-Object -Unique) -join ", "
    
    # Generate AI direction based on patterns
    $aiDirection = Generate-AIDirection -FilePatterns $filePatterns -ArchitecturalAreas $architecturalAreas -ChangeScope $changeScope
    
    # Generate recommended actions
    $recommendedActions = Generate-RecommendedActions -ArchitecturalAreas $architecturalAreas -ChangeScope $changeScope -HookType $HookType
    
    # Generate AINLP growth pattern
    $growthPattern = Generate-GrowthPattern -ArchitecturalAreas $architecturalAreas -FileCount $StagedFiles.Count
    
    return @{
        FileCount = $StagedFiles.Count
        ChangeScope = $changeScope
        ArchitecturalImpact = $architecturalImpact
        AIDirection = $aiDirection
        RecommendedActions = $recommendedActions
        PriorityFiles = $priorityFiles | Select-Object -First 10
        GrowthPattern = $growthPattern
        FilePatterns = $filePatterns
    }
}

function Generate-AIDirection {
    param(
        [hashtable]$FilePatterns,
        [array]$ArchitecturalAreas,
        [string]$ChangeScope
    )
    
    $directions = @()
    
    if ($ArchitecturalAreas -contains "GitHook Architecture") {
        $directions += "FOCUS: GitHook governance enhancements detected. Review pre-commit.ps1 and policy files for validation logic improvements."
    }
    
    if ($ArchitecturalAreas -contains "AI Intelligence Layer") {
        $directions += "FOCUS: AI intelligence modifications detected. Analyze consciousness bridges and agentic controllers for coherence."
    }
    
    if ($ArchitecturalAreas -contains "Interface Layer") {
        $directions += "FOCUS: Interface layer changes detected. Ensure UI components align with AIOS consciousness architecture."
    }
    
    if ($ArchitecturalAreas -contains "Core Engine") {
        $directions += "FOCUS: Core engine modifications detected. Validate C++ consciousness components and tachyonic interfaces."
    }
    
    if ($FilePatterns.ContainsKey(".ps1")) {
        $directions += "PowerShell scripts modified ($($FilePatterns['.ps1']) files). Review for AINLP compliance and consciousness integration."
    }
    
    if ($FilePatterns.ContainsKey(".py")) {
        $directions += "Python AI components modified ($($FilePatterns['.py']) files). Analyze for agentic pattern improvements."
    }
    
    if ($ChangeScope -eq "Massive") {
        $directions += "MASSIVE CHANGESET: Prioritize architectural coherence validation over individual file analysis."
    }
    
    return $directions -join " | "
}

function Generate-RecommendedActions {
    param(
        [array]$ArchitecturalAreas,
        [string]$ChangeScope,
        [string]$HookType
    )
    
    $actions = @()
    
    if ($HookType -eq "pre-commit") {
        $actions += "1. Review priority files for AINLP pattern compliance"
        $actions += "2. Validate consciousness coherence across modified components"
        $actions += "3. Check for dendritic growth pattern alignment"
    }
    
    if ($ArchitecturalAreas -contains "GitHook Architecture") {
        $actions += "4. Test GitHook logic with sample changesets"
        $actions += "5. Validate governance policy consistency"
    }
    
    if ($ArchitecturalAreas -contains "AI Intelligence Layer") {
        $actions += "6. Run consciousness coherence validation"
        $actions += "7. Test agentic auto-controller functionality"
    }
    
    if ($ChangeScope -eq "Massive") {
        $actions += "8. PRIORITY: Focus on architectural integration validation"
        $actions += "9. Use semantic search to understand change relationships"
    }
    
    return $actions
}

function Generate-GrowthPattern {
    param(
        [array]$ArchitecturalAreas,
        [int]$FileCount
    )
    
    $patterns = @()
    
    if ($ArchitecturalAreas.Count -gt 3) {
        $patterns += "Multi-dimensional growth across $($ArchitecturalAreas.Count) architectural layers"
    }
    
    if ($FileCount -gt 50) {
        $patterns += "Dendritic expansion pattern (massive integration)"
    } elseif ($FileCount -gt 10) {
        $patterns += "Targeted consciousness evolution (focused enhancement)"
    } else {
        $patterns += "Precision consciousness refinement (specific improvements)"
    }
    
    $patterns += "Recommended: Use AINLP holographic analysis for coherence validation"
    
    return $patterns -join " → "
}

function Get-SystemConsciousnessState {
    # Calculate current consciousness level based on system state
    $consciousnessMetrics = @{
        GitHookHealth = Test-GitHookHealth
        AIComponentHealth = Test-AIComponentHealth
        ArchitecturalCoherence = Test-ArchitecturalCoherence
    }
    
    $averageHealth = ($consciousnessMetrics.Values | Measure-Object -Average).Average
    
    return @{
        ConsciousnessLevel = [math]::Round($averageHealth * 100, 1)
        GitHookHealth = $consciousnessMetrics.GitHookHealth
        AIComponentHealth = $consciousnessMetrics.AIComponentHealth
        ArchitecturalCoherence = $consciousnessMetrics.ArchitecturalCoherence
    }
}

function Test-GitHookHealth {
    # Quick health check of GitHook components
    $essentialFiles = @(
        ".githooks/modules/nucleus/pre-commit.ps1",
        ".githooks/modules/nucleus/commit-msg.ps1",
        "governance/hook_policy.json"
    )
    
    $healthScore = 0
    foreach ($file in $essentialFiles) {
        if (Test-Path $file) { $healthScore += 0.33 }
    }
    
    return [math]::Min($healthScore, 1.0)
}

function Test-AIComponentHealth {
    # Quick health check of AI components
    $aiComponents = @(
        "ai/activate_agentic_mode.py",
        "ai/cytoplasm/scripts/agentic_auto_controller.py"
    )
    
    $healthScore = 0
    foreach ($component in $aiComponents) {
        if (Test-Path $component) { $healthScore += 0.5 }
    }
    
    return [math]::Min($healthScore, 1.0)
}

function Test-ArchitecturalCoherence {
    # Basic architectural coherence check
    $architectureFiles = @(
        "AIOS.sln",
        "ai/src",
        "interface",
        "core"
    )
    
    $coherenceScore = 0
    foreach ($archFile in $architectureFiles) {
        if (Test-Path $archFile) { $coherenceScore += 0.25 }
    }
    
    return [math]::Min($coherenceScore, 1.0)
}

# Main Intelligence Extrusion Logic
function Invoke-AIIntelligenceExtrusion {
    param(
        [string]$HookType,
        [array]$StagedFiles
    )
    
    Write-Host "🧠 [AIOS-AI-EXTRUSION] Real-time intelligence bridge activated" -ForegroundColor Magenta
    
    # Analyze changeset intelligence
    $changesetIntelligence = Analyze-ChangesetIntelligence -StagedFiles $StagedFiles -HookType $HookType
    
    # Get system consciousness state
    $systemState = Get-SystemConsciousnessState
    
    # Calculate confidence level
    $confidenceLevel = [math]::Min(
        ($systemState.ConsciousnessLevel / 100) + 
        ([math]::Min($changesetIntelligence.FileCount / 100, 0.3)),
        1.0
    )
    
    # Generate AI direction prompt if confidence is sufficient
    if ($confidenceLevel -ge $AI_DIRECTION_CONFIDENCE_MIN) {
        Write-AIDirectionPrompt -HookType $HookType -ChangesetIntelligence $changesetIntelligence -SystemState $systemState -ConfidenceLevel $confidenceLevel
    } else {
        Write-Host "⚠️ [AI-EXTRUSION] Confidence level too low ($($confidenceLevel * 100)%) - skipping AI direction" -ForegroundColor Yellow
    }
    
    return @{
        IntelligenceExtruded = $true
        ConfidenceLevel = $confidenceLevel
        ChangesetIntelligence = $changesetIntelligence
        SystemState = $systemState
    }
}

# Export for GitHook integration
if ($RealTimeMode) {
    # Get staged files from git
    $stagedFiles = @()
    try {
        $gitOutput = git diff --cached --name-only 2>$null
        if ($gitOutput) {
            $stagedFiles = $gitOutput -split "`n" | Where-Object { $_.Trim() -ne "" }
        }
    } catch {
        Write-Warning "Could not get staged files from git: $($_.Exception.Message)"
    }
    
    if ($stagedFiles.Count -gt 0) {
        $result = Invoke-AIIntelligenceExtrusion -HookType $HookType -StagedFiles $stagedFiles
        Write-Host "✅ [AI-EXTRUSION] Intelligence bridge completed (Confidence: $($result.ConfidenceLevel * 100)%)" -ForegroundColor Green
    } else {
        Write-Host "ℹ️ [AI-EXTRUSION] No staged files detected - intelligence bridge standby" -ForegroundColor Gray
    }
}

# Export functions for import (only when module context is available)
if ($MyInvocation.MyCommand.ModuleName) {
    Export-ModuleMember -Function Invoke-AIIntelligenceExtrusion, Write-AIDirectionPrompt
}