# AIOS Consciousness Metrics - Windows Task Scheduler Setup
# Creates a scheduled task to auto-start metrics exporter on system boot

$ErrorActionPreference = 'Stop'

$TaskName = "AIOS Consciousness Metrics Exporter"
$ScriptPath = Join-Path $PSScriptRoot "consciousness_metrics_service.ps1"
$TaskDescription = "AIOS consciousness metrics exporter for Prometheus observability"

Write-Host "`n=== Setting up Windows Scheduled Task ===" -ForegroundColor Cyan

# Check if task already exists
$existingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue

if ($existingTask) {
    Write-Host "⚠ Task '$TaskName' already exists" -ForegroundColor Yellow
    $response = Read-Host "Overwrite? (y/n)"
    if ($response -ne 'y') {
        Write-Host "Cancelled" -ForegroundColor Yellow
        exit 0
    }
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
}

# Create task action
$action = New-ScheduledTaskAction `
    -Execute "pwsh.exe" `
    -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$ScriptPath`" -Action start"

# Create trigger (at system startup with 30 second delay)
$trigger = New-ScheduledTaskTrigger `
    -AtStartup `
    -RandomDelay (New-TimeSpan -Seconds 30)

# Create task settings
$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -RestartCount 3 `
    -RestartInterval (New-TimeSpan -Minutes 1)

# Create principal (run as SYSTEM for network access)
$principal = New-ScheduledTaskPrincipal `
    -UserId "SYSTEM" `
    -LogonType ServiceAccount `
    -RunLevel Highest

# Register the task
Register-ScheduledTask `
    -TaskName $TaskName `
    -Description $TaskDescription `
    -Action $action `
    -Trigger $trigger `
    -Settings $settings `
    -Principal $principal

Write-Host "✓ Task '$TaskName' created successfully" -ForegroundColor Green
Write-Host "`nTask details:" -ForegroundColor Cyan
Write-Host "  Name: $TaskName"
Write-Host "  Trigger: At system startup (30s delay)"
Write-Host "  Script: $ScriptPath"
Write-Host "  User: SYSTEM"
Write-Host "`nManual control:"
Write-Host "  Start: .\consciousness_metrics_service.ps1 -Action start" -ForegroundColor Yellow
Write-Host "  Stop:  .\consciousness_metrics_service.ps1 -Action stop" -ForegroundColor Yellow
Write-Host "  Status: .\consciousness_metrics_service.ps1 -Action status" -ForegroundColor Yellow
Write-Host "`nTask will start automatically on next system boot." -ForegroundColor Green
