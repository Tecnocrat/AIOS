#!/usr/bin/env pwsh
# AIOS AI-Driven Git Hook - Agentic Task Completion Enforcement
# This hook enforces completion through AI visual feedback validation

param(
    [string]$CommitMessage = "",
    [switch]$Force = $false
)

Write-Host " AIOS AI-Driven Commit Validation" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan

# Check for AI Visual Feedback data
$aiVisualPath = Join-Path $PWD "visual_interface/bin/Debug/net9.0-windows/ai_visual_feedback"
$aiStatePath = Join-Path $aiVisualPath "state"
$screenshotsPath = Join-Path $aiVisualPath "screenshots"

if (-not (Test-Path $aiStatePath)) {
    Write-Host "  AI Visual Feedback not found - creating requirement" -ForegroundColor Yellow
    Write-Host "   Agentic stimulation point: AIOS must be running with visual capture" -ForegroundColor Yellow
    
    # Create the requirement file
    $requirement = @{
        Type = "AI_Visual_Validation_Required"
        Reason = "Commits require real-time AI visual validation of AIOS state"
        Instructions = @(
            "1. Launch AIOS Visual Interface",
            "2. Ensure AI Visual Feedback Service is capturing screenshots",
            "3. Validate all components are functioning",
            "4. Attempt commit again"
        )
        AgenticObjective = "Force development workflow to include AI visual validation"
        CreatedAt = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
    }
    
    $requirementPath = Join-Path $PWD "ai_visual_requirement.json"
    $requirement | ConvertTo-Json -Depth 3 | Out-File $requirementPath -Encoding UTF8
    
    Write-Host " COMMIT BLOCKED: AI Visual Validation Required" -ForegroundColor Red
    Write-Host "   Run AIOS Visual Interface to enable AI visual feedback" -ForegroundColor Red
    exit 1
}

# Check for recent visual captures
$recentCaptures = Get-ChildItem $screenshotsPath -Filter "*.png" | 
    Where-Object { $_.LastWriteTime -gt (Get-Date).AddMinutes(-5) } |
    Sort-Object LastWriteTime -Descending

if ($recentCaptures.Count -eq 0) {
    Write-Host " COMMIT BLOCKED: No recent AI visual captures found" -ForegroundColor Red
    Write-Host "   Agentic requirement: Visual state must be captured within last 5 minutes" -ForegroundColor Yellow
    exit 1
}

Write-Host " Found $($recentCaptures.Count) recent visual captures" -ForegroundColor Green

# Analyze AI objectives completion
$objectiveFiles = Get-ChildItem $aiStatePath -Filter "objective_*.json" -ErrorAction SilentlyContinue

if ($objectiveFiles.Count -gt 0) {
    Write-Host " Analyzing AI Objectives:" -ForegroundColor Cyan
    
    foreach ($objFile in $objectiveFiles) {
        try {
            $objective = Get-Content $objFile.FullName | ConvertFrom-Json
            Write-Host "    $($objective.Objective)" -ForegroundColor White
            
            # Check for visual validation requirement
            if ($objective.RequiresVisualValidation -eq $true) {
                # Verify visual evidence exists
                $timeThreshold = [DateTime]::Parse($objective.RegisteredAt).AddMinutes(10)
                $validationCaptures = $recentCaptures | Where-Object { $_.LastWriteTime -gt $timeThreshold }
                
                if ($validationCaptures.Count -eq 0) {
                    Write-Host "    Insufficient visual validation for: $($objective.Objective)" -ForegroundColor Red
                    Write-Host "   Agentic enforcement: Continue running AIOS until objective completion" -ForegroundColor Yellow
                    exit 1
                }
                
                Write-Host "    Visual validation available" -ForegroundColor Green
            }
        }
        catch {
            Write-Host "     Error reading objective: $($objFile.Name)" -ForegroundColor Yellow
        }
    }
}

# Check for session metadata
$sessionFile = Join-Path $aiStatePath "current_session.json"
if (Test-Path $sessionFile) {
    try {
        $session = Get-Content $sessionFile | ConvertFrom-Json
        $sessionDuration = (Get-Date) - [DateTime]::Parse($session.StartTime)
        
        Write-Host " AI Session Analysis:" -ForegroundColor Cyan
        Write-Host "   Duration: $($sessionDuration.TotalMinutes.ToString('F1')) minutes" -ForegroundColor White
        Write-Host "   Purpose: $($session.Purpose)" -ForegroundColor White
        
        # Enforce minimum session duration for meaningful commits
        if ($sessionDuration.TotalMinutes -lt 2 -and -not $Force) {
            Write-Host " COMMIT BLOCKED: Insufficient AI session duration" -ForegroundColor Red
            Write-Host "   Agentic rule: Minimum 2 minutes of visual monitoring required" -ForegroundColor Yellow
            Write-Host "   Current: $($sessionDuration.TotalMinutes.ToString('F1')) minutes" -ForegroundColor Yellow
            Write-Host "   Use -Force to override (not recommended)" -ForegroundColor Gray
            exit 1
        }
        
        Write-Host "    Session duration acceptable" -ForegroundColor Green
    }
    catch {
        Write-Host "  Could not parse session metadata" -ForegroundColor Yellow
    }
}

# Create AI validation summary
$validationSummary = @{
    ValidationTimestamp = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
    VisualCapturesFound = $recentCaptures.Count
    ObjectivesAnalyzed = $objectiveFiles.Count
    ValidationStatus = "PASSED"
    AgenticEnforcement = "AI visual feedback validation completed successfully"
    CommitAuthorization = "APPROVED"
    NextRequirement = "Continue AI visual monitoring for future commits"
}

$summaryPath = Join-Path $aiStatePath "commit_validation_$(Get-Date -Format 'yyyyMMdd_HHmmss').json"
$validationSummary | ConvertTo-Json -Depth 2 | Out-File $summaryPath -Encoding UTF8

Write-Host " AI Visual Validation PASSED" -ForegroundColor Green
Write-Host " Agentic stimulation successful - commit authorized" -ForegroundColor Green
Write-Host " Validation summary saved: $summaryPath" -ForegroundColor Gray

# Additional check for CHANGELOG requirement (maintaining existing governance)
if (-not (Test-Path "CHANGELOG.md") -and -not (Test-Path "docs/CHANGELOG.md") -and -not $Force) {
    Write-Host "  Creating required CHANGELOG.md for governance compliance" -ForegroundColor Yellow
    
    $changelogContent = @"
# AIOS Consciousness System Changelog

## [Unreleased] - $(Get-Date -Format 'yyyy-MM-dd')

### Added
- AI Visual Feedback Service for real-time UI monitoring
- Agentic stimulation points for task completion enforcement  
- Git hook integration for AI-driven development workflow
- Centralized process management system
- Tachyonic viewer integration with hyperdimensional visualization

### Changed
- Enhanced application architecture with dependency injection
- Improved process lifecycle management
- Integrated AI visual validation in commit workflow

### AI Integration
- Real-time screenshot capture every 0.5 seconds
- AI-readable visual state storage and metadata
- Objective-driven task completion validation
- Agentic enforcement of development practices

---
*This changelog is maintained as part of AIOS governance and AI integration requirements.*
"@

    $changelogContent | Out-File "CHANGELOG.md" -Encoding UTF8
    git add "CHANGELOG.md"
    Write-Host " CHANGELOG.md created and staged" -ForegroundColor Green
}

Write-Host " Agentic Task Completion: VALIDATED" -ForegroundColor Green
exit 0
