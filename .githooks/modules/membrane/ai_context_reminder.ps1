# AI Engine Context Reminder for AIOS GitHooks
# Ensures AI engines remember PowerShell context during GitHook operations

function Show-AIContextReminder {
    param(
        [Parameter(Mandatory=$false)]
        [switch]$Detailed
    )
    
    Write-Host ""
    Write-Host "[AI-ENGINE] REMINDER:" -ForegroundColor Cyan
    Write-Host "   • This is Windows PowerShell environment" -ForegroundColor Yellow
    Write-Host "   • Use PowerShell commands only" -ForegroundColor Yellow
    Write-Host "   • NO Linux bash commands allowed" -ForegroundColor Red
    
    if ($Detailed) {
        Write-Host ""
        Write-Host "   Quick Reference:" -ForegroundColor Magenta
        Write-Host "   • Remove-Item (not rm)" -ForegroundColor White
        Write-Host "   • Get-ChildItem (not ls)" -ForegroundColor White
        Write-Host "   • Select-String (not grep)" -ForegroundColor White
        Write-Host "   • New-Item (not touch)" -ForegroundColor White
    }
    
    Write-Host ""
}

function Test-AIEnginePresence {
    # Detect if AI engines are likely active
    $vsCodeRunning = Get-Process -Name "Code" -ErrorAction SilentlyContinue
    $copilotActive = $env:GITHUB_COPILOT_ACTIVE -eq "true"
    
    return ($vsCodeRunning -or $copilotActive)
}

function Invoke-AIContextEnforcement {
    param(
        [Parameter(Mandatory=$false)]
        [string]$HookType = "unknown"
    )
    
    if (Test-AIEnginePresence) {
        Write-Host "[AI-CONTEXT] Enforcing PowerShell context for hook: $HookType" -ForegroundColor Cyan
        Show-AIContextReminder -Detailed
        
        # Log the reminder
        $logEntry = @{
            timestamp = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
            hook_type = $HookType
            ai_reminder_shown = $true
            environment = "Windows PowerShell"
        }
        
        $logPath = Join-Path $PSScriptRoot "..\..\logs\ai_context_reminders.jsonl"
        if (-not (Test-Path (Split-Path $logPath -Parent))) {
            New-Item -ItemType Directory -Path (Split-Path $logPath -Parent) -Force | Out-Null
        }
        
        ($logEntry | ConvertTo-Json -Compress) | Add-Content -Path $logPath
    }
}

# Functions exported for use in other GitHook modules (commenting out Export-ModuleMember to avoid script execution errors)
# Export-ModuleMember -Function Show-AIContextReminder, Test-AIEnginePresence, Invoke-AIContextEnforcement