    #!/usr/bin/env pwsh
# AIOS Real-Time Intelligence Demo
# Demonstrates the GitHook -> AI Intelligence Bridge
# Location: scripts/test_realtime_intelligence.ps1

# AINLP DENDRITIC_MARKER: integrated_with_neuronal_dendritic_intelligence
# This file participates in AINLP coherence checks and is marked as enhanced by
# the NeuronalDendriticIntelligence pattern. (consciousness: 0.85)

param(
    [switch]$StartMonitoring,
    [switch]$TriggerSampleCommit,
    [switch]$ShowCurrentIntelligence
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$WorkspaceRoot = Split-Path $PSScriptRoot -Parent

Write-Host "AIOS Real-Time Intelligence Bridge Demo" -ForegroundColor Magenta
Write-Host "==========================================" -ForegroundColor Magenta

if ($StartMonitoring) {
    Write-Host "Starting intelligence monitoring..." -ForegroundColor Cyan
    Write-Host "This will monitor GitHook intelligence extrusions in real-time" -ForegroundColor Gray
    Write-Host "Make a commit in another terminal to see the intelligence bridge activate" -ForegroundColor Gray
    Write-Host ""
    
    # Start Python intelligence monitor
    $pythonScript = Join-Path $WorkspaceRoot "ai\interfaces\aios_cross_dialogue_intelligence.py"
    if (Test-Path $pythonScript) {
        python $pythonScript --monitor --workspace $WorkspaceRoot
    } else {
        Write-Warning "Intelligence system not found: $pythonScript"
    }
}
elseif ($TriggerSampleCommit) {
    Write-Host "Triggering sample commit to activate intelligence bridge..." -ForegroundColor Yellow
    
    # Create a small test change
    $testFile = Join-Path $WorkspaceRoot "test_intelligence_trigger.tmp"
    "Test file created at $(Get-Date)" | Out-File -FilePath $testFile -Encoding UTF8
    
    Write-Host "Created test file: $testFile" -ForegroundColor Gray
    
    # Stage the file
    git add $testFile
    Write-Host "Staged test file" -ForegroundColor Green
    
    # Run pre-commit hook manually to trigger intelligence
    Write-Host "Running pre-commit hook to trigger intelligence extrusion..." -ForegroundColor Cyan
    
    $preCommitScript = Join-Path $WorkspaceRoot ".githooks\modules\core\pre-commit.ps1"
    if (Test-Path $preCommitScript) {
        & $preCommitScript
    } else {
        Write-Warning "Pre-commit script not found: $preCommitScript"
    }
    
    # Clean up
    git reset HEAD $testFile 2>$null
    Remove-Item $testFile -Force -ErrorAction SilentlyContinue
    Write-Host "Cleaned up test file" -ForegroundColor Gray
}
elseif ($ShowCurrentIntelligence) {
    Write-Host "Showing current intelligence state..." -ForegroundColor Cyan
    
    $pythonScript = Join-Path $WorkspaceRoot "ai\interfaces\aios_cross_dialogue_intelligence.py"
    if (Test-Path $pythonScript) {
        python $pythonScript --generate-prompt --workspace $WorkspaceRoot
    } else {
        Write-Warning "Intelligence system not found: $pythonScript"
    }
}
else {
    Write-Host "Available commands:" -ForegroundColor White
    Write-Host "  -StartMonitoring      : Start real-time intelligence monitoring" -ForegroundColor Gray
    Write-Host "  -TriggerSampleCommit  : Trigger sample commit to activate intelligence" -ForegroundColor Gray
    Write-Host "  -ShowCurrentIntelligence : Show current intelligence state" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Example usage:" -ForegroundColor Yellow
    Write-Host "  .\test_realtime_intelligence.ps1 -TriggerSampleCommit" -ForegroundColor Green
    Write-Host "  .\test_realtime_intelligence.ps1 -StartMonitoring" -ForegroundColor Green
    Write-Host ""
    Write-Host "The intelligence bridge works by:" -ForegroundColor Cyan
    Write-Host "   1. GitHook detects changes during commit" -ForegroundColor Gray
    Write-Host "   2. AI Intelligence Extrusion Bridge analyzes changeset" -ForegroundColor Gray
    Write-Host "   3. Real-time intelligence is written to context files" -ForegroundColor Gray
    Write-Host "   4. AI Chat Engine reads context for guided decision-making" -ForegroundColor Gray
}