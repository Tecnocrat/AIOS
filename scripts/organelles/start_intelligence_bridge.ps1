<#
.SYNOPSIS
    Start AIOS Intelligence Bridge Service
.DESCRIPTION
    Launches the Intelligence Bridge that exposes AIOS main tools to the Docker ecosystem.
    Port: 8950 (configurable via INTELLIGENCE_BRIDGE_PORT)
.NOTES
    AINLP: start_intelligence_bridge.ps1 | /scripts/organelles:launcher | C:6.0 | →mesh,bridge | P:deploy
#>

param(
    [switch]$Check,
    [switch]$Start,
    [switch]$Stop,
    [switch]$Status
)

$BRIDGE_PORT = if ($env:INTELLIGENCE_BRIDGE_PORT) { $env:INTELLIGENCE_BRIDGE_PORT } else { 8950 }
$AIOS_MAIN = if ($env:AIOS_MAIN) { $env:AIOS_MAIN } else { "C:\dev\AIOS" }
$BRIDGE_PATH = Join-Path $AIOS_MAIN "ai\tools\mesh"

function Test-BridgeRunning {
    try {
        $response = Invoke-RestMethod -Uri "http://localhost:$BRIDGE_PORT/health" -TimeoutSec 2 -ErrorAction Stop
        return $true
    } catch {
        return $false
    }
}

function Get-BridgeProcess {
    Get-Process python -ErrorAction SilentlyContinue | 
        Where-Object { $_.CommandLine -like "*intelligence_bridge*" }
}

if ($Check) {
    if (Test-BridgeRunning) {
        Write-Host "[CHECK] Intelligence Bridge running on port $BRIDGE_PORT" -ForegroundColor Green
        exit 0
    } else {
        Write-Host "[CHECK] Intelligence Bridge not running" -ForegroundColor Yellow
        exit 1
    }
}

if ($Stop) {
    $proc = Get-BridgeProcess
    if ($proc) {
        Stop-Process -Id $proc.Id -Force
        Write-Host "[STOP] Intelligence Bridge stopped" -ForegroundColor Green
        exit 0
    } else {
        Write-Host "[STOP] No bridge process found" -ForegroundColor Yellow
        exit 0
    }
}

if ($Status) {
    if (Test-BridgeRunning) {
        $health = Invoke-RestMethod -Uri "http://localhost:$BRIDGE_PORT/health"
        Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
        Write-Host "  INTELLIGENCE BRIDGE STATUS" -ForegroundColor Cyan
        Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
        Write-Host "  Status: $($health.status)" -ForegroundColor Green
        Write-Host "  Cell ID: $($health.cell_id)"
        Write-Host "  Tools: $($health.tools_available)"
        Write-Host "  Uptime: $([math]::Round($health.uptime_seconds / 60, 2)) minutes"
        Write-Host "  Port: $BRIDGE_PORT"
        Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
        exit 0
    } else {
        Write-Host "[STATUS] Intelligence Bridge not running" -ForegroundColor Red
        exit 1
    }
}

if ($Start) {
    if (Test-BridgeRunning) {
        Write-Host "[START] Intelligence Bridge already running" -ForegroundColor Green
        exit 0
    }
    
    Write-Host "[START] Starting Intelligence Bridge on port $BRIDGE_PORT..." -ForegroundColor Cyan
    
    Push-Location $BRIDGE_PATH
    
    $startInfo = New-Object System.Diagnostics.ProcessStartInfo
    $startInfo.FileName = "python"
    $startInfo.Arguments = "-c `"import uvicorn; uvicorn.run('intelligence_bridge:app', host='0.0.0.0', port=$BRIDGE_PORT)`""
    $startInfo.WorkingDirectory = $BRIDGE_PATH
    $startInfo.UseShellExecute = $false
    $startInfo.CreateNoWindow = $true
    $startInfo.RedirectStandardOutput = $true
    $startInfo.RedirectStandardError = $true
    
    $process = [System.Diagnostics.Process]::Start($startInfo)
    
    Pop-Location
    
    # Wait for startup
    $maxWait = 10
    $waited = 0
    while ($waited -lt $maxWait) {
        Start-Sleep -Seconds 1
        $waited++
        if (Test-BridgeRunning) {
            Write-Host "[START] Intelligence Bridge started successfully" -ForegroundColor Green
            Write-Host "  URL: http://localhost:$BRIDGE_PORT" -ForegroundColor DarkGray
            Write-Host "  Health: http://localhost:$BRIDGE_PORT/health" -ForegroundColor DarkGray
            Write-Host "  Tools: http://localhost:$BRIDGE_PORT/tools" -ForegroundColor DarkGray
            exit 0
        }
    }
    
    Write-Host "[START] Failed to start Intelligence Bridge" -ForegroundColor Red
    exit 1
}

# Default: show help
Write-Host "AIOS Intelligence Bridge Launcher"
Write-Host ""
Write-Host "Usage:"
Write-Host "  .\start_intelligence_bridge.ps1 -Check   # Check if running"
Write-Host "  .\start_intelligence_bridge.ps1 -Start   # Start service"
Write-Host "  .\start_intelligence_bridge.ps1 -Stop    # Stop service"
Write-Host "  .\start_intelligence_bridge.ps1 -Status  # Show status"
