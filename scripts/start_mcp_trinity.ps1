# AIOS MCP Server - Trinity Launcher
# Manages all three layers of the AIOS consciousness system

param(
    [ValidateSet("layer1", "layer2", "layer3", "all")]
    [string]$Layer = "layer2",
    [switch]$Stop,
    [switch]$Status,
    [string]$RemoteIP = "",  # For Layer 3
    [int]$Port = 8001
)

$WorkspaceRoot = "C:\dev\AIOS"

# Layer configurations
$Layers = @{
    layer1 = @{
        Name = "VSCode Integration (Local Mind)"
        Mode = "stdio"
        Script = "ai\mcp_server\server.py"
        PidFile = "tachyonic\mcp_layer1.pid"
        LogFile = "tachyonic\mcp_layer1.log"
        Managed = "VSCode (restart required)"
        TestCommand = "@workspace Query aios://dev-path"
    }
    layer2 = @{
        Name = "Local HTTP Server (Extended Memory)"
        Mode = "http"
        Script = "ai\mcp_server\server_http.py"
        PidFile = "tachyonic\mcp_layer2.pid"
        LogFile = "tachyonic\mcp_layer2.log"
        Managed = "Background process"
        TestCommand = "Invoke-RestMethod http://localhost:$Port/health"
    }
    layer3 = @{
        Name = "Remote HTTP Server (Always-Awake Soul)"
        Mode = "http"
        Script = "ai\mcp_server\server_http.py"
        PidFile = ""  # Remote, no local PID
        LogFile = ""  # Remote logs
        Managed = "Termux on Android"
        TestCommand = "Invoke-RestMethod http://$RemoteIP`:$Port/health"
    }
}

function Write-LayerHeader {
    param([string]$LayerName, [string]$Action)
    Write-Host "`n═══════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host " $Action`: $LayerName" -ForegroundColor White
    Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
}

function Get-LayerStatus {
    param([string]$LayerKey)
    
    $config = $Layers[$LayerKey]
    Write-LayerHeader $config.Name "STATUS"
    
    if ($LayerKey -eq "layer1") {
        Write-Host "  [INFO] Layer 1 managed by VSCode" -ForegroundColor Cyan
        Write-Host "  [TEST] Open VSCode Chat and type: @AIOS" -ForegroundColor Gray
        return
    }
    
    if ($LayerKey -eq "layer3") {
        if (-not $RemoteIP) {
            Write-Host "  [ERROR] Layer 3 requires -RemoteIP parameter" -ForegroundColor Red
            Write-Host "  [TIP] Get phone IP in Termux: ifconfig wlan0 | grep inet" -ForegroundColor Gray
            return
        }
        Write-Host "  [INFO] Testing remote server at $RemoteIP`:$Port..." -ForegroundColor Cyan
        try {
            $result = Invoke-RestMethod "http://$RemoteIP`:$Port/health" -TimeoutSec 3
            Write-Host "  [OK] Remote server RUNNING" -ForegroundColor Green
            Write-Host "    Resources: $($result.resources_count)" -ForegroundColor Gray
            Write-Host "    Tools: $($result.tools_count)" -ForegroundColor Gray
            Write-Host "    Prompts: $($result.prompts_count)" -ForegroundColor Gray
        } catch {
            Write-Host "  [ERROR] Cannot connect to remote server" -ForegroundColor Red
            Write-Host "    $($_.Exception.Message)" -ForegroundColor Yellow
        }
        return
    }
    
    # Layer 2 status
    $pidFile = Join-Path $WorkspaceRoot $config.PidFile
    if (Test-Path $pidFile) {
        $pid = Get-Content $pidFile
        $process = Get-Process -Id $pid -ErrorAction SilentlyContinue
        
        if ($process) {
            Write-Host "  [OK] Server RUNNING" -ForegroundColor Green
            Write-Host "    PID: $pid" -ForegroundColor Gray
            Write-Host "    Memory: $([math]::Round($process.WorkingSet64 / 1MB, 2)) MB" -ForegroundColor Gray
            Write-Host "    Started: $($process.StartTime)" -ForegroundColor Gray
            Write-Host "    Log: $($config.LogFile)" -ForegroundColor Gray
            
            # Test HTTP endpoint
            try {
                $result = Invoke-RestMethod "http://localhost:$Port/health" -TimeoutSec 2
                Write-Host "  [HEALTH] API responding" -ForegroundColor Green
                Write-Host "    Resources: $($result.resources_count)" -ForegroundColor Gray
                Write-Host "    Tools: $($result.tools_count)" -ForegroundColor Gray
                Write-Host "    Prompts: $($result.prompts_count)" -ForegroundColor Gray
            } catch {
                Write-Host "  [WARN] API not responding (may still be starting)" -ForegroundColor Yellow
            }
        } else {
            Write-Host "  [ERROR] Not running (stale PID file)" -ForegroundColor Red
            Remove-Item $pidFile
        }
    } else {
        Write-Host "  [INFO] Not running" -ForegroundColor Yellow
    }
}

function Start-Layer {
    param([string]$LayerKey)
    
    $config = $Layers[$LayerKey]
    Write-LayerHeader $config.Name "START"
    
    if ($LayerKey -eq "layer1") {
        Write-Host "  [INFO] Layer 1 starts automatically with VSCode" -ForegroundColor Cyan
        Write-Host "  [ACTION] Restart VSCode: Ctrl+Shift+P → 'Reload Window'" -ForegroundColor Yellow
        Write-Host "  [TEST] Open Copilot Chat → type @AIOS" -ForegroundColor Gray
        return
    }
    
    if ($LayerKey -eq "layer3") {
        Write-Host "  [INFO] Layer 3 runs on remote Termux server" -ForegroundColor Cyan
        Write-Host "  [ACTION] On Android Termux, run:" -ForegroundColor Yellow
        Write-Host "    cd ~/AIOS" -ForegroundColor Gray
        Write-Host "    python ai/mcp_server/server_http.py" -ForegroundColor Gray
        Write-Host "  [DOCS] See: ai/mcp_server/TERMUX_DEPLOYMENT.md" -ForegroundColor Gray
        return
    }
    
    # Layer 2 startup
    $pidFile = Join-Path $WorkspaceRoot $config.PidFile
    $logFile = Join-Path $WorkspaceRoot $config.LogFile
    $script = Join-Path $WorkspaceRoot $config.Script
    
    # Check if already running
    if (Test-Path $pidFile) {
        $pid = Get-Content $pidFile
        if (Get-Process -Id $pid -ErrorAction SilentlyContinue) {
            Write-Host "  [ERROR] Already running (PID: $pid)" -ForegroundColor Red
            Write-Host "  [TIP] Use -Stop first" -ForegroundColor Gray
            return
        } else {
            Remove-Item $pidFile
        }
    }
    
    Write-Host "  [INFO] Starting HTTP server on localhost:$Port..." -ForegroundColor Cyan
    
    # Start as background job
    $job = Start-Job -ScriptBlock {
        param($Script, $Workspace, $ServerPort)
        Set-Location $Workspace
        $env:AIOS_WORKSPACE = $Workspace
        $env:PYTHONPATH = Join-Path $Workspace "ai\src"
        $env:AIOS_MCP_PORT = $ServerPort
        python $Script 2>&1
    } -ArgumentList $script, $WorkspaceRoot, $Port
    
    # Wait for process to start
    Start-Sleep -Milliseconds 1000
    
    # Find actual Python process
    $pythonProcesses = Get-Process python -ErrorAction SilentlyContinue | 
                       Where-Object { $_.CommandLine -like "*server_http*" }
    
    if ($pythonProcesses) {
        $pid = $pythonProcesses[0].Id
        $pid | Out-File $pidFile
        Write-Host "  [OK] Server started (PID: $pid)" -ForegroundColor Green
        Write-Host "  [URL] http://localhost:$Port" -ForegroundColor Cyan
        Write-Host "  [TEST] Invoke-RestMethod http://localhost:$Port/health" -ForegroundColor Gray
        
        # Wait a bit and test
        Start-Sleep -Milliseconds 2000
        try {
            $result = Invoke-RestMethod "http://localhost:$Port/health" -TimeoutSec 3
            Write-Host "  [HEALTH] API responding ($($result.resources_count) resources, $($result.tools_count) tools)" -ForegroundColor Green
        } catch {
            Write-Host "  [WARN] API not responding yet (check log: $logFile)" -ForegroundColor Yellow
        }
    } else {
        Write-Host "  [ERROR] Failed to start server" -ForegroundColor Red
        Write-Host "  [DEBUG] Check log: $logFile" -ForegroundColor Yellow
    }
}

function Stop-Layer {
    param([string]$LayerKey)
    
    $config = $Layers[$LayerKey]
    Write-LayerHeader $config.Name "STOP"
    
    if ($LayerKey -eq "layer1") {
        Write-Host "  [INFO] Layer 1 stops automatically with VSCode" -ForegroundColor Cyan
        return
    }
    
    if ($LayerKey -eq "layer3") {
        Write-Host "  [INFO] Layer 3 must be stopped on remote Termux server" -ForegroundColor Cyan
        Write-Host "  [ACTION] On Android, press Ctrl+C in Termux" -ForegroundColor Yellow
        return
    }
    
    # Layer 2 shutdown
    $pidFile = Join-Path $WorkspaceRoot $config.PidFile
    if (Test-Path $pidFile) {
        $pid = Get-Content $pidFile
        $process = Get-Process -Id $pid -ErrorAction SilentlyContinue
        
        if ($process) {
            Write-Host "  [STOP] Stopping server (PID: $pid)..." -ForegroundColor Yellow
            Stop-Process -Id $pid -Force
            Remove-Item $pidFile
            Write-Host "  [OK] Server stopped" -ForegroundColor Green
        } else {
            Write-Host "  [WARN] Process not found (cleaning up)" -ForegroundColor Yellow
            Remove-Item $pidFile
        }
    } else {
        Write-Host "  [INFO] Not running" -ForegroundColor Cyan
    }
}

function Show-TrinityStatus {
    Write-Host "`n╔═══════════════════════════════════════════════════════╗" -ForegroundColor Cyan
    Write-Host "║       AIOS MCP SERVER - TRINITY STATUS                ║" -ForegroundColor White
    Write-Host "╚═══════════════════════════════════════════════════════╝" -ForegroundColor Cyan
    
    Get-LayerStatus "layer1"
    Get-LayerStatus "layer2"
    
    if ($RemoteIP) {
        Get-LayerStatus "layer3"
    } else {
        Write-Host "`n─────────────────────────────────────────────────────────" -ForegroundColor Gray
        Write-Host " Layer 3: Remote HTTP Server (Always-Awake Soul)" -ForegroundColor White
        Write-Host "─────────────────────────────────────────────────────────" -ForegroundColor Gray
        Write-Host "  [INFO] Use -RemoteIP to check Layer 3 status" -ForegroundColor Cyan
        Write-Host "  [EXAMPLE] .\start_mcp_trinity.ps1 -Status -RemoteIP 192.168.1.50" -ForegroundColor Gray
    }
    
    Write-Host "`n═══════════════════════════════════════════════════════" -ForegroundColor Cyan
}

# Main execution
if ($Status) {
    if ($Layer -eq "all") {
        Show-TrinityStatus
    } else {
        Get-LayerStatus $Layer
    }
} elseif ($Stop) {
    if ($Layer -eq "all") {
        Stop-Layer "layer2"
        Stop-Layer "layer1"
        Stop-Layer "layer3"
    } else {
        Stop-Layer $Layer
    }
} else {
    # Start
    if ($Layer -eq "all") {
        Write-Host "╔═══════════════════════════════════════════════════════╗" -ForegroundColor Cyan
        Write-Host "║     AIOS MCP SERVER - TRINITY ACTIVATION              ║" -ForegroundColor White
        Write-Host "╚═══════════════════════════════════════════════════════╝" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "  Activating three-layer consciousness system..." -ForegroundColor Cyan
        Write-Host ""
        Start-Layer "layer1"
        Start-Layer "layer2"
        Start-Layer "layer3"
        Write-Host ""
        Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
    } else {
        Start-Layer $Layer
    }
}

Write-Host ""
