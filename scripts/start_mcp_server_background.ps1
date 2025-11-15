# AIOS MCP Server - Background Launcher
# Starts MCP server as background process for testing/development

param(
    [string]$WorkspaceRoot = "C:\dev\AIOS",
    [switch]$Stop,
    [switch]$Status
)

$ServerScript = Join-Path $WorkspaceRoot "ai\mcp_server\server.py"
$LogFile = Join-Path $WorkspaceRoot "tachyonic\mcp_server.log"
$PidFile = Join-Path $WorkspaceRoot "tachyonic\mcp_server.pid"

function Stop-MCPServer {
    if (Test-Path $PidFile) {
        $pid = Get-Content $PidFile
        try {
            $process = Get-Process -Id $pid -ErrorAction Stop
            Write-Host "[STOP] Stopping MCP server (PID: $pid)..." -ForegroundColor Yellow
            Stop-Process -Id $pid -Force
            Remove-Item $PidFile
            Write-Host "[OK] MCP server stopped" -ForegroundColor Green
        } catch {
            Write-Host "[WARN] Process not found (PID: $pid)" -ForegroundColor Yellow
            Remove-Item $PidFile -ErrorAction SilentlyContinue
        }
    } else {
        Write-Host "[INFO] MCP server not running (no PID file)" -ForegroundColor Cyan
    }
}

function Get-MCPServerStatus {
    if (Test-Path $PidFile) {
        $pid = Get-Content $PidFile
        try {
            $process = Get-Process -Id $pid -ErrorAction Stop
            Write-Host "[STATUS] MCP server RUNNING" -ForegroundColor Green
            Write-Host "  PID: $pid" -ForegroundColor Cyan
            Write-Host "  Memory: $([math]::Round($process.WorkingSet64 / 1MB, 2)) MB" -ForegroundColor Cyan
            Write-Host "  Started: $($process.StartTime)" -ForegroundColor Cyan
            Write-Host "  Log: $LogFile" -ForegroundColor Cyan
            return $true
        } catch {
            Write-Host "[STATUS] MCP server NOT RUNNING (stale PID file)" -ForegroundColor Red
            Remove-Item $PidFile -ErrorAction SilentlyContinue
            return $false
        }
    } else {
        Write-Host "[STATUS] MCP server NOT RUNNING" -ForegroundColor Yellow
        return $false
    }
}

function Start-MCPServer {
    # Check if already running
    if (Test-Path $PidFile) {
        $running = Get-MCPServerStatus
        if ($running) {
            Write-Host "[ERROR] MCP server already running" -ForegroundColor Red
            Write-Host "[TIP] Use -Stop flag to stop existing server" -ForegroundColor Cyan
            return
        }
    }

    Write-Host "[AIOS] Starting MCP Server in background..." -ForegroundColor Cyan
    Write-Host "[INFO] Workspace: $WorkspaceRoot" -ForegroundColor Cyan
    Write-Host "[INFO] Log: $LogFile" -ForegroundColor Cyan

    # Set environment variables
    $env:AIOS_WORKSPACE = $WorkspaceRoot
    $env:PYTHONPATH = Join-Path $WorkspaceRoot "ai\src"

    # Start server as background job
    $job = Start-Job -ScriptBlock {
        param($ServerScript, $WorkspaceRoot, $LogFile)
        $env:AIOS_WORKSPACE = $WorkspaceRoot
        $env:PYTHONPATH = Join-Path $WorkspaceRoot "ai\src"
        
        # Redirect output to log
        python $ServerScript 2>&1 | Out-File -FilePath $LogFile -Append
    } -ArgumentList $ServerScript, $WorkspaceRoot, $LogFile

    # Wait a moment for process to start
    Start-Sleep -Milliseconds 500

    # Get the actual Python process PID (job creates wrapper)
    $pythonProcesses = Get-Process python -ErrorAction SilentlyContinue | 
                       Where-Object { $_.CommandLine -like "*mcp_server*" }
    
    if ($pythonProcesses) {
        $pid = $pythonProcesses[0].Id
        $pid | Out-File $PidFile
        Write-Host "[OK] MCP server started (PID: $pid)" -ForegroundColor Green
        Write-Host "[INFO] Server running in background" -ForegroundColor Cyan
        Write-Host "[TIP] Use -Status to check status, -Stop to stop" -ForegroundColor Cyan
    } else {
        Write-Host "[ERROR] Failed to start MCP server" -ForegroundColor Red
        Write-Host "[DEBUG] Check log: $LogFile" -ForegroundColor Yellow
    }
}

# Main execution
if ($Stop) {
    Stop-MCPServer
} elseif ($Status) {
    Get-MCPServerStatus
} else {
    Start-MCPServer
}
