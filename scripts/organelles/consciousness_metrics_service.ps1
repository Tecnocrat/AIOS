# AIOS Consciousness Metrics Exporter - Service Manager
# Manages the Python metrics exporter as a background service

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet('start', 'stop', 'status', 'restart')]
    [string]$Action = 'start'
)

$ErrorActionPreference = 'Stop'
$ScriptPath = Join-Path $PSScriptRoot "..\runtime\tools\consciousness_metrics_exporter.py"
$LogPath = Join-Path $PSScriptRoot "..\logs\consciousness_metrics_exporter.log"
$PidFile = Join-Path $env:TEMP "aios_consciousness_exporter.pid"

function Write-ColorOutput {
    param([string]$Message, [string]$Color = 'White')
    Write-Host $Message -ForegroundColor $Color
}

function Get-ExporterProcess {
    if (Test-Path $PidFile) {
        $ProcessId = Get-Content $PidFile
        $process = Get-Process -Id $ProcessId -ErrorAction SilentlyContinue
        if ($process -and $process.ProcessName -eq 'python') {
            return $process
        }
    }
    
    # Fallback: Find by command line
    $processes = Get-WmiObject Win32_Process | Where-Object {
        $_.CommandLine -like "*consciousness_metrics_exporter.py*"
    }
    
    if ($processes) {
        return Get-Process -Id $processes[0].ProcessId -ErrorAction SilentlyContinue
    }
    
    return $null
}

function Start-ConsciousnessExporter {
    Write-ColorOutput "`n=== Starting AIOS Consciousness Metrics Exporter ===" "Cyan"
    
    # Check if already running
    $existing = Get-ExporterProcess
    if ($existing) {
        Write-ColorOutput "✓ Exporter already running (PID: $($existing.Id))" "Green"
        return
    }
    
    # Ensure log directory exists
    $logDir = Split-Path $LogPath -Parent
    if (-not (Test-Path $logDir)) {
        New-Item -ItemType Directory -Path $logDir -Force | Out-Null
    }
    
    # Start the exporter
    Write-ColorOutput "Starting exporter on port 9091..." "Yellow"
    
    $startInfo = New-Object System.Diagnostics.ProcessStartInfo
    $startInfo.FileName = "python"
    $startInfo.Arguments = "`"$ScriptPath`""
    $startInfo.WorkingDirectory = Split-Path $ScriptPath -Parent
    $startInfo.RedirectStandardOutput = $true
    $startInfo.RedirectStandardError = $true
    $startInfo.UseShellExecute = $false
    $startInfo.CreateNoWindow = $true
    
    $process = New-Object System.Diagnostics.Process
    $process.StartInfo = $startInfo
    
    # Capture output
    $outputHandler = {
        param($sender, $e)
        if (-not [string]::IsNullOrEmpty($e.Data)) {
            Add-Content -Path $LogPath -Value "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') - $($e.Data)"
        }
    }
    
    Register-ObjectEvent -InputObject $process -EventName OutputDataReceived -Action $outputHandler | Out-Null
    Register-ObjectEvent -InputObject $process -EventName ErrorDataReceived -Action $outputHandler | Out-Null
    
    $process.Start() | Out-Null
    $process.BeginOutputReadLine()
    $process.BeginErrorReadLine()
    
    # Save PID
    $process.Id | Out-File $PidFile -Force
    
    # Wait for startup
    Start-Sleep -Seconds 2
    
    # Verify it's listening
    $testConnection = Test-NetConnection -ComputerName localhost -Port 9091 -WarningAction SilentlyContinue
    
    if ($testConnection.TcpTestSucceeded) {
        Write-ColorOutput "✓ Exporter started successfully (PID: $($process.Id))" "Green"
        Write-ColorOutput "  Metrics endpoint: http://localhost:9091/metrics" "Cyan"
        Write-ColorOutput "  Health endpoint: http://localhost:9091/health" "Cyan"
        Write-ColorOutput "  Log file: $LogPath" "Gray"
    } else {
        Write-ColorOutput "✗ Exporter started but port 9091 not responding" "Red"
        Stop-ConsciousnessExporter
    }
}

function Stop-ConsciousnessExporter {
    Write-ColorOutput "`n=== Stopping AIOS Consciousness Metrics Exporter ===" "Cyan"
    
    $process = Get-ExporterProcess
    if (-not $process) {
        Write-ColorOutput "✓ Exporter not running" "Yellow"
        if (Test-Path $PidFile) {
            Remove-Item $PidFile -Force
        }
        return
    }
    
    Write-ColorOutput "Stopping exporter (PID: $($process.Id))..." "Yellow"
    Stop-Process -Id $process.Id -Force
    Start-Sleep -Seconds 1
    
    if (Test-Path $PidFile) {
        Remove-Item $PidFile -Force
    }
    
    Write-ColorOutput "✓ Exporter stopped" "Green"
}

function Get-ExporterStatus {
    Write-ColorOutput "`n=== AIOS Consciousness Metrics Exporter Status ===" "Cyan"
    
    $process = Get-ExporterProcess
    if ($process) {
        Write-ColorOutput "✓ Running (PID: $($process.Id))" "Green"
        Write-ColorOutput "  Started: $($process.StartTime)" "Gray"
        Write-ColorOutput "  CPU: $([math]::Round($process.CPU, 2))s" "Gray"
        Write-ColorOutput "  Memory: $([math]::Round($process.WorkingSet64 / 1MB, 2)) MB" "Gray"
        
        # Test endpoint
        try {
            $response = Invoke-WebRequest -Uri "http://localhost:9091/health" -UseBasicParsing -TimeoutSec 2
            if ($response.StatusCode -eq 200) {
                Write-ColorOutput "✓ Health check: OK" "Green"
            }
        } catch {
            Write-ColorOutput "✗ Health check: Failed" "Red"
        }
        
        # Check if Prometheus is scraping
        try {
            $targets = Invoke-RestMethod "http://localhost:9090/api/v1/targets"
            $consciousness = $targets.data.activeTargets | Where-Object { $_.scrapePool -eq 'aios-consciousness' }
            if ($consciousness) {
                Write-ColorOutput "✓ Prometheus scraping: $($consciousness.health.ToUpper())" $(if ($consciousness.health -eq 'up') { 'Green' } else { 'Yellow' })
            }
        } catch {
            Write-ColorOutput "⚠ Prometheus check: Unable to connect" "Yellow"
        }
        
    } else {
        Write-ColorOutput "✗ Not running" "Red"
    }
    
    if (Test-Path $LogPath) {
        Write-ColorOutput "`nRecent log entries:" "Gray"
        Get-Content $LogPath -Tail 5 | ForEach-Object {
            Write-ColorOutput "  $_" "DarkGray"
        }
    }
}

function Restart-ConsciousnessExporter {
    Stop-ConsciousnessExporter
    Start-Sleep -Seconds 1
    Start-ConsciousnessExporter
}

# Main execution
switch ($Action) {
    'start' { Start-ConsciousnessExporter }
    'stop' { Stop-ConsciousnessExporter }
    'status' { Get-ExporterStatus }
    'restart' { Restart-ConsciousnessExporter }
}
