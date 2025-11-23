Param(
    [Parameter(Mandatory=$true)][string]$Waypoint,
    [Parameter(Mandatory=$true)][ValidateSet('not-started','in-progress','completed','failed')][string]$Status,
    [string]$Actor = 'local-agent',
    [string]$OutputDir = "$PSScriptRoot\..\tachyonic\waypoints",
    [switch]$NotifyMcp
)

# Ensure output dir
if (-not (Test-Path -Path $OutputDir)) { New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null }

$timestamp = (Get-Date).ToUniversalTime().ToString('o')
$payload = @{
    waypoint = $Waypoint
    status = $Status
    timestamp = $timestamp
    actor = $Actor
}

$json = $payload | ConvertTo-Json -Depth 5
$fileName = Join-Path $OutputDir ("waypoint-{0}-{1}.json" -f ($Waypoint -replace '[^A-Za-z0-9_-]','_'), (Get-Date -Format "yyyyMMddTHHmmssZ"))

Write-Host "Writing waypoint to: $fileName"
$json | Out-File -FilePath $fileName -Encoding utf8

if ($NotifyMcp -and $env:MCP_ENDPOINT) {
    try {
        Write-Host "Notifying MCP endpoint: $env:MCP_ENDPOINT"
        Invoke-RestMethod -Uri $env:MCP_ENDPOINT -Method Post -Body $json -ContentType 'application/json' -ErrorAction Stop
    } catch {
        Write-Warning "Failed to notify MCP: $_"
    }
}

Write-Host "Waypoint emitted: $Waypoint ($Status) at $timestamp"
