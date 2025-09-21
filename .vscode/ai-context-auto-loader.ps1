# AIOS AI Context Auto-Loader
# Automatically outputs critical context to terminal for AI engine consumption
# Consolidates both context loading and environment enforcement
# Coordinates with AIOS VS Code Extension to prevent duplication

param(
    [switch]$Silent = $false,
    [switch]$ContextOnly = $false,
    [switch]$ForceLoad = $false
)

# Context files to auto-load
$contextFiles = @{
    "AI_CONTEXT_AUTO_LOAD" = ".vscode/AI_CONTEXT_AUTO_LOAD.md"
    "AIOS_CONTEXT" = ".aios_context.json"
}

# Check for extension coordination to prevent duplication
$extensionActive = $env:AIOS_EXTENSION_ACTIVE -eq "true"
$extensionContextLoaded = $env:AIOS_EXTENSION_CONTEXT_LOADED -eq "true"

if ($extensionActive -and $extensionContextLoaded -and -not $ForceLoad) {
    if (-not $Silent) {
        Write-Host ""
        Write-Host "[COORDINATION] AIOS Extension has already loaded context" -ForegroundColor Green
        Write-Host "[TASK-SYSTEM] Skipping duplicate context loading" -ForegroundColor Yellow
        Write-Host "Use -ForceLoad to override extension coordination" -ForegroundColor DarkGray
        Write-Host ""
    }
    return
}

if (-not $Silent -and -not $ContextOnly) {
    Write-Host ""
    Write-Host "AI ENGINE CONTEXT LOADED" -ForegroundColor Cyan
    Write-Host "=================================" -ForegroundColor Cyan
    Write-Host "Environment: Windows PowerShell" -ForegroundColor Green
    Write-Host "Workspace: AIOS Development" -ForegroundColor Green
    Write-Host "Shell: PowerShell (pwsh.exe)" -ForegroundColor Green
    Write-Host ""
    Write-Host "CRITICAL REMINDERS:" -ForegroundColor Yellow
    Write-Host "   • Use PowerShell syntax only" -ForegroundColor Yellow
    Write-Host "   • NO Linux bash commands" -ForegroundColor Red
    Write-Host "   • Context auto-loaded below" -ForegroundColor Cyan
    Write-Host ""
}

if (-not $Silent) {
    Write-Host ""
    Write-Host "AIOS AI CONTEXT AUTO-LOADER" -ForegroundColor Cyan
    Write-Host "============================" -ForegroundColor Cyan
}

foreach ($name in $contextFiles.Keys) {
    $file = $contextFiles[$name]
    if (Test-Path $file) {
        if (-not $Silent) {
            Write-Host ""
            Write-Host "Loading $name..." -ForegroundColor Green
            Write-Host "Source: $file" -ForegroundColor DarkGray
            Write-Host "----------------------------------------" -ForegroundColor DarkGray
        }
        
        # Output content with AI-readable markers
        Write-Host "# AI_CONTEXT_START: $name"
        Get-Content $file | ForEach-Object {
            Write-Host $_
        }
        Write-Host "# AI_CONTEXT_END: $name"
        Write-Host ""
    } else {
        if (-not $Silent) {
            Write-Host "Warning: Context file not found: $file" -ForegroundColor Yellow
        }
    }
}

if (-not $Silent) {
    Write-Host "AI Context loading complete!" -ForegroundColor Green
    
    if (-not $ContextOnly) {
        # Set window title to remind about PowerShell context
        $Host.UI.RawUI.WindowTitle = "AIOS Development - PowerShell Only"
        
        # Display current location and environment
        Write-Host ""
        Write-Host "Current Location: $(Get-Location)" -ForegroundColor Magenta
        Write-Host "PowerShell Version: $($PSVersionTable.PSVersion)" -ForegroundColor Magenta
    }
    
    Write-Host ""
}