# AI Context Enforcement for AIOS Workspace
# Auto-executed when workspace opens to remind AI engines of PowerShell context

Write-Host ""
Write-Host "🤖 AI ENGINE CONTEXT LOADED 🤖" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host "Environment: Windows PowerShell" -ForegroundColor Green
Write-Host "Workspace: AIOS Development" -ForegroundColor Green
Write-Host "Shell: PowerShell (pwsh.exe)" -ForegroundColor Green
Write-Host ""
Write-Host "⚠️  CRITICAL REMINDERS:" -ForegroundColor Yellow
Write-Host "   • Use PowerShell syntax only" -ForegroundColor Yellow
Write-Host "   • NO Linux bash commands" -ForegroundColor Red
Write-Host "   • Check .vscode/AI_CONTEXT_POWERSHELL_ONLY.md for reference" -ForegroundColor Cyan
Write-Host ""
Write-Host "✅ Ready for AIOS development!" -ForegroundColor Green
Write-Host ""

# Set window title to remind about PowerShell context
$Host.UI.RawUI.WindowTitle = "AIOS Development - PowerShell Only"

# Display current location
Write-Host "Current Location: $(Get-Location)" -ForegroundColor Magenta
Write-Host "PowerShell Version: $($PSVersionTable.PSVersion)" -ForegroundColor Magenta
Write-Host ""