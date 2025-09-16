# AIOS GitHook Entry Point - Pre-Push (PowerShell)
# Optimized for Windows PowerShell environment
# Delegates to NUCLEUS module for actual hook logic

param(
    [Parameter(ValueFromRemainingArguments=$true)]
    [string[]]$PassThrough
)

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
    
    # Path to the actual pre-push logic
    $PrePushScript = Join-Path $GitRoot ".githooks\modules\nucleus\pre-push.ps1"
    
    if (-not (Test-Path $PrePushScript)) {
        Write-Error "GitHook nucleus pre-push script not found: $PrePushScript"
        exit 1
    }
    
    # Execute the actual pre-push logic
    & $PrePushScript @PassThrough
    exit $LASTEXITCODE
    
} catch {
    Write-Error "GitHook pre-push failed: $($_.Exception.Message)"
    exit 1
}