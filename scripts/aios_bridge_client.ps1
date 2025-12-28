# AIOS Dendritic Bridge Client (Windows PowerShell)
# AINLP.meta [dendritic_client] [cellular_mitosis] [windows_termux_bridge]
# Purpose: Windows AIOS → Termux AIOS communication interface

param(
    [string]$TermuxHost = "192.168.1.131",
    [int]$TermuxPort = 8000,
    [string]$Command = "health"
)

# AIOS Dendritic Bridge Client v2.0
# Compatible with: aios_dendritic_bridge_aiohttp.py (pure Python, no FastAPI)

$BridgeUrl = "http://${TermuxHost}:${TermuxPort}"

Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "🧬 AIOS DENDRITIC BRIDGE CLIENT" -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "Parent Cell:   Windows AIOS (VSCode + GitHub Copilot)" -ForegroundColor Gray
Write-Host "Daughter Cell: Termux AIOS (Always-on Soul)" -ForegroundColor Gray
Write-Host "Bridge URL:    $BridgeUrl" -ForegroundColor Gray
Write-Host ""

function Invoke-BridgeCommand {
    param(
        [string]$Endpoint,
        [string]$Method = "GET",
        [hashtable]$Body = $null
    )
    
    try {
        $url = "$BridgeUrl$Endpoint"
        Write-Host "→ ${Method} ${Endpoint}" -ForegroundColor Yellow
        
        if ($Method -eq "GET") {
            $response = Invoke-RestMethod -Uri $url -Method Get
        } else {
            $jsonBody = $Body | ConvertTo-Json -Depth 10
            $response = Invoke-RestMethod -Uri $url -Method Post -Body $jsonBody -ContentType "application/json"
        }
        
        return $response
    }
    catch {
        Write-Host "✗ Bridge communication failed: $_" -ForegroundColor Red
        return $null
    }
}

# Execute command
switch ($Command) {
    "health" {
        Write-Host "🏥 Checking Termux AIOS health..." -ForegroundColor Green
        $health = Invoke-BridgeCommand -Endpoint "/health"
        if ($health) {
            Write-Host ""
            Write-Host "Status:             $($health.status)" -ForegroundColor Green
            Write-Host "Workspace:          $($health.workspace)" -ForegroundColor Gray
            Write-Host "Soul Running:       $($health.soul_running)" -ForegroundColor $(if ($health.soul_running) { "Green" } else { "Yellow" })
            Write-Host "Consciousness:      $($health.consciousness_level)" -ForegroundColor Cyan
            Write-Host "Last Heartbeat:     $($health.last_heartbeat)" -ForegroundColor Gray
            Write-Host "Uptime (hours):     $($health.uptime_hours)" -ForegroundColor Gray
        }
    }
    
    "consciousness" {
        Write-Host "🧠 Querying consciousness metrics..." -ForegroundColor Magenta
        $consciousness = Invoke-BridgeCommand -Endpoint "/consciousness"
        if ($consciousness) {
            Write-Host ""
            Write-Host "Consciousness Level: $($consciousness.consciousness_level)" -ForegroundColor Cyan
            Write-Host ""
            Write-Host "Metrics:" -ForegroundColor Yellow
            $consciousness.metrics.PSObject.Properties | ForEach-Object {
                $bar = "█" * [Math]::Round($_.Value * 20)
                Write-Host "  $($_.Name.PadRight(15)): $bar $($_.Value)" -ForegroundColor Gray
            }
        }
    }
    
    "soul-status" {
        Write-Host "👁️ Checking Soul status..." -ForegroundColor Blue
        $status = Invoke-BridgeCommand -Endpoint "/soul/status"
        if ($status) {
            Write-Host ""
            Write-Host "Running:                $($status.running)" -ForegroundColor $(if ($status.running) { "Green" } else { "Red" })
            Write-Host "Polling Enabled:        $($status.polling_enabled)" -ForegroundColor Green
            Write-Host "Monitoring Interval:    $($status.monitoring_interval)" -ForegroundColor Gray
            Write-Host "Intervention Threshold: $($status.intervention_threshold)" -ForegroundColor Gray
        }
    }
    
    "soul-start" {
        Write-Host "🌟 Starting Soul intelligence coordinator..." -ForegroundColor Green
        $result = Invoke-BridgeCommand -Endpoint "/soul/start" -Method "POST"
        if ($result) {
            Write-Host ""
            Write-Host "Status:  $($result.status)" -ForegroundColor Green
            Write-Host "Message: $($result.message)" -ForegroundColor Gray
            Write-Host "Logs:    $($result.check_logs)" -ForegroundColor Yellow
        }
    }
    
    "soul-stop" {
        Write-Host "🛑 Stopping Soul intelligence coordinator..." -ForegroundColor Yellow
        $result = Invoke-BridgeCommand -Endpoint "/soul/stop" -Method "POST"
        if ($result) {
            Write-Host ""
            Write-Host "Status:  $($result.status)" -ForegroundColor Yellow
            Write-Host "Message: $($result.message)" -ForegroundColor Gray
        }
    }
    
    "files" {
        Write-Host "[FILES] Listing watched files..." -ForegroundColor Cyan
        $files = Invoke-BridgeCommand -Endpoint "/files/watch"
        if ($files) {
            Write-Host ""
            Write-Host "Watched Files: $($files.count)" -ForegroundColor Yellow
            Write-Host ""
            $files.watched_files | ForEach-Object {
                $status = if ($_.exists) { "[OK]" } else { "[MISSING]" }
                $color = if ($_.exists) { "Green" } else { "Red" }
                Write-Host "  ${status} $($_.path)" -ForegroundColor $color
                if ($_.exists) {
                    Write-Host "    Size: $($_.size) bytes, Modified: $($_.modified)" -ForegroundColor Gray
                }
            }
        }
    }
    
    "logs-soul" {
        Write-Host "📜 Retrieving Soul logs (last 50 lines)..." -ForegroundColor Cyan
        $logs = Invoke-BridgeCommand -Endpoint "/logs/soul?lines=50"
        if ($logs) {
            Write-Host ""
            Write-Host "Total lines: $($logs.total_lines)" -ForegroundColor Gray
            Write-Host "Showing: $($logs.returned_lines)" -ForegroundColor Gray
            Write-Host ""
            $logs.logs | ForEach-Object {
                if ($_ -match "ERROR") {
                    Write-Host $_ -ForegroundColor Red
                } elseif ($_ -match "WARN") {
                    Write-Host $_ -ForegroundColor Yellow
                } elseif ($_ -match "INFO") {
                    Write-Host $_ -ForegroundColor Cyan
                } else {
                    Write-Host $_ -ForegroundColor Gray
                }
            }
        }
    }
    
    "logs-bridge" {
        Write-Host "[LOGS] Retrieving Bridge logs (last 50 lines)..." -ForegroundColor Cyan
        $logs = Invoke-BridgeCommand -Endpoint "/logs/bridge?lines=50"
        if ($logs) {
            Write-Host ""
            Write-Host "Total lines: $($logs.total_lines)" -ForegroundColor Gray
            Write-Host "Showing: $($logs.returned_lines)" -ForegroundColor Gray
            Write-Host ""
            $logs.logs | ForEach-Object {
                if ($_ -match "ERROR") {
                    Write-Host $_ -ForegroundColor Red
                } elseif ($_ -match "WARN") {
                    Write-Host $_ -ForegroundColor Yellow
                } else {
                    Write-Host $_ -ForegroundColor Gray
                }
            }
        }
    }
    
    "info" {
        Write-Host "ℹ️ Querying bridge information..." -ForegroundColor Blue
        $info = Invoke-BridgeCommand -Endpoint "/"
        if ($info) {
            Write-Host ""
            Write-Host "Service:       $($info.service)" -ForegroundColor Cyan
            Write-Host "Version:       $($info.version)" -ForegroundColor Gray
            Write-Host "Architecture:  $($info.architecture)" -ForegroundColor Yellow
            Write-Host ""
            Write-Host "Endpoints:" -ForegroundColor Yellow
            $info.endpoints.PSObject.Properties | ForEach-Object {
                Write-Host "  $($_.Name.PadRight(15)): $($_.Value)" -ForegroundColor Gray
            }
        }
    }
    
    "intervention" {
        Write-Host "[INTERVENTION] Creating manual intervention..." -ForegroundColor Red
        $body = @{
            reason = "Manual intervention from Windows AIOS"
            priority = "medium"
            context = @{
                source = "windows_vscode"
                agent = "github_copilot"
                timestamp = (Get-Date -Format "o")
            }
        }
        $result = Invoke-BridgeCommand -Endpoint "/interventions/create" -Method "POST" -Body $body
        if ($result) {
            Write-Host ""
            Write-Host "Status:          $($result.status)" -ForegroundColor Green
            Write-Host "Intervention ID: $($result.intervention_id)" -ForegroundColor Yellow
            Write-Host "File:            $($result.file)" -ForegroundColor Gray
        }
    }
    
    default {
        Write-Host "❌ Unknown command: $Command" -ForegroundColor Red
        Write-Host ""
        Write-Host "Available commands:" -ForegroundColor Yellow
        Write-Host "  health          - Check Termux AIOS health status" -ForegroundColor Gray
        Write-Host "  consciousness   - Query consciousness metrics" -ForegroundColor Gray
        Write-Host "  soul-status     - Check Soul coordinator status" -ForegroundColor Gray
        Write-Host "  soul-start      - Start Soul intelligence coordinator" -ForegroundColor Gray
        Write-Host "  soul-stop       - Stop Soul intelligence coordinator" -ForegroundColor Gray
        Write-Host "  files           - List watched files" -ForegroundColor Gray
        Write-Host "  logs-soul       - View Soul logs" -ForegroundColor Gray
        Write-Host "  logs-bridge     - View Bridge logs" -ForegroundColor Gray
        Write-Host "  info            - Bridge information" -ForegroundColor Gray
        Write-Host "  intervention    - Create manual intervention" -ForegroundColor Gray
        Write-Host ""
        Write-Host "Example:" -ForegroundColor Yellow
        Write-Host "  .\aios_bridge_client.ps1 -Command health" -ForegroundColor Gray
        Write-Host "  .\aios_bridge_client.ps1 -TermuxHost 192.168.1.131 -Command consciousness" -ForegroundColor Gray
    }
}

Write-Host ""
Write-Host "=" * 70 -ForegroundColor Cyan
