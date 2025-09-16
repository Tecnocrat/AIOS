# AIOS GitHook Entry Point - Pre-Commit (PowerShell)
# Optimized for Windows PowerShell environment with profile isolation
# Delegates to NUCLEUS module for actual hook logic

param(
    [Parameter(ValueFromRemainingArguments=$true)]
    [string[]]$PassThrough
)

# Ensure isolated execution environment
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

try {
    # Ensure we're in the repository root
    $GitRoot = git rev-parse --show-toplevel 2>$null
    if (-not $GitRoot) {
        Write-Error "Not in a Git repository"
        exit 1
    }
    
    # Convert to Windows path format
    $GitRoot = $GitRoot -replace '/', '\'
    
    # Path to the actual pre-commit logic
    $PreCommitScript = Join-Path $GitRoot ".githooks\modules\nucleus\pre-commit.ps1"
    $RefactoringScript = Join-Path $GitRoot ".githooks\modules\nucleus\ai_guided_refactoring_engine.ps1"
    $AIReminderScript = Join-Path $GitRoot ".githooks\modules\membrane\ai_context_reminder.ps1"
    
    if (-not (Test-Path $PreCommitScript)) {
        Write-Error "GitHook nucleus pre-commit script not found: $PreCommitScript"
        exit 1
    }
    
    # Execute the actual pre-commit logic
    Write-Host "`n🔍 [AIOS-GITHOOK] Running standard pre-commit checks..." -ForegroundColor Green
    & $PreCommitScript @PassThrough
    $PreCommitResult = $LASTEXITCODE
    
    # Execute AI-guided refactoring analysis
    if (Test-Path $RefactoringScript) {
        Write-Host "`n🧠 [AI-INTEGRATION] Running intelligent refactoring analysis..." -ForegroundColor Cyan
        & $RefactoringScript
        $RefactoringResult = $LASTEXITCODE
    } else {
        $RefactoringResult = 0
    }
    
    # Display AI context reminder
    if (Test-Path $AIReminderScript) {
        & $AIReminderScript
    }
    
    # If refactoring opportunities detected, recommend AI intervention
    if ($RefactoringResult -eq 1) {
        Write-Host "`n💡 [AI-AGENT-ACTIVATION] Enhancement opportunities detected!" -ForegroundColor Yellow
        Write-Host "🎯 [RECOMMENDATION] Open VS Code and let the AI agent review suggestions in .vscode\ai_refactoring_context.md" -ForegroundColor Magenta
        Write-Host "🤖 [AUTONOMOUS-MODE] The AI agent will intelligently decide the best refactoring approach" -ForegroundColor Cyan
    }
    
    # Return the most restrictive result (prioritize pre-commit over refactoring)
    if ($PreCommitResult -ne 0) {
        exit $PreCommitResult
    } else {
        exit $RefactoringResult
    }
    
} catch {
    Write-Error "GitHook pre-commit failed: $($_.Exception.Message)"
    exit 1
}