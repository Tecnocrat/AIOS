#!/usr/bin/env pwsh
# AIOS Agentic Git Integration Setup
# Configures git hooks for AI-driven task completion enforcement

Write-Host " Setting up AIOS Agentic Git Integration" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

# Ensure we're in the AIOS repository
if (-not (Test-Path ".git")) {
    Write-Host " Error: Not in a git repository" -ForegroundColor Red
    exit 1
}

# Setup git hook for AI-driven commits
$hookPath = ".git/hooks/pre-commit"
$aiHookScript = ".githooks/aios_ai_driven_commit.ps1"

# Create the pre-commit hook that calls our AI validation
$hookContent = @"
#!/bin/sh
# AIOS AI-Driven Pre-Commit Hook
# Enforces agentic task completion through visual validation

echo " AIOS Agentic Validation Starting..."

# Call PowerShell AI validation script
if command -v pwsh >/dev/null 2>&1; then
    pwsh -ExecutionPolicy Bypass -File "$aiHookScript"
    exit_code=$?
elif command -v powershell >/dev/null 2>&1; then
    powershell -ExecutionPolicy Bypass -File "$aiHookScript"
    exit_code=$?
else
    echo " PowerShell not found - AI validation cannot run"
    echo "   Please install PowerShell Core for agentic enforcement"
    exit 1
fi

if [ $exit_code -ne 0 ]; then
    echo " AI Validation Failed - Commit blocked by agentic enforcement"
    exit 1
fi

echo " AI Validation Passed - Agentic objectives satisfied"
exit 0
"@

# Write the hook
$hookContent | Out-File $hookPath -Encoding ASCII
if ($IsLinux -or $IsMacOS) {
    chmod +x $hookPath
}

Write-Host " Pre-commit hook configured" -ForegroundColor Green

# Setup commit-msg hook for enhanced validation
$commitMsgHookPath = ".git/hooks/commit-msg"
$commitMsgContent = @"
#!/bin/sh
# AIOS AI-Enhanced Commit Message Hook

echo " AIOS AI-Enhanced Commit Processing..."

# Call AI validation with commit message
if command -v pwsh >/dev/null 2>&1; then
    pwsh -ExecutionPolicy Bypass -File "$aiHookScript" -CommitMessage "$1"
elif command -v powershell >/dev/null 2>&1; then
    powershell -ExecutionPolicy Bypass -File "$aiHookScript" -CommitMessage "$1"
fi

echo " AI-Enhanced Commit Message Processed"
exit 0
"@

$commitMsgContent | Out-File $commitMsgHookPath -Encoding ASCII
if ($IsLinux -or $IsMacOS) {
    chmod +x $commitMsgHookPath
}

Write-Host " Commit-msg hook configured" -ForegroundColor Green

# Create configuration file for AI integration
$aiConfig = @{
    AIOSAgenticIntegration = @{
        Enabled = $true
        VisualValidationRequired = $true
        ScreenshotInterval = 500
        MinimumSessionDuration = 120
        ObjectiveValidation = $true
        AgenticEnforcement = $true
    }
    Stimulation = @{
        Type = "TaskCompletionEnforcement"
        Mechanism = "VisualFeedbackLoop"
        Objective = "ForceAIEngineIntegration"
        CompletionCriteria = @(
            "UI running and captured",
            "Visual state validated", 
            "AI objectives satisfied",
            "Development workflow integrated"
        )
    }
    Integration = @{
        GitHooks = $true
        RealTimeCapture = $true
        MetadataGeneration = $true
        AIReadableFormat = $true
    }
    CreatedAt = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
    Purpose = "Enable AI engine to 'see' and validate AIOS application state in real-time"
}

$configPath = ".aios_agentic_config.json"
$aiConfig | ConvertTo-Json -Depth 4 | Out-File $configPath -Encoding UTF8

Write-Host " Agentic configuration created: $configPath" -ForegroundColor Green

Write-Host ""
Write-Host " AIOS Agentic Integration Setup Complete!" -ForegroundColor Green
Write-Host ""
Write-Host " What this enables:" -ForegroundColor Cyan
Write-Host "   • AI visual validation required for all commits" -ForegroundColor White
Write-Host "   • Real-time screenshot capture (0.5s intervals)" -ForegroundColor White  
Write-Host "   • Task completion enforcement through visual feedback" -ForegroundColor White
Write-Host "   • AI-readable state metadata generation" -ForegroundColor White
Write-Host "   • Agentic stimulation points for development workflow" -ForegroundColor White
Write-Host ""
Write-Host " To activate:" -ForegroundColor Yellow
Write-Host "   1. Launch AIOS Visual Interface" -ForegroundColor White
Write-Host "   2. AI Visual Feedback Service will start capturing" -ForegroundColor White
Write-Host "   3. Commits will require active visual validation" -ForegroundColor White
Write-Host "   4. AI engine can now 'see' the application state!" -ForegroundColor White
Write-Host ""
Write-Host " Agentic enforcement: Active!" -ForegroundColor Green
