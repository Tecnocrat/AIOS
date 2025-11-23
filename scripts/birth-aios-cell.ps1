#!/usr/bin/env pwsh
# AIOS Cell Birth Protocol - PowerShell Edition
# AINLP Pattern: biological-architecture.cellular-proliferation
# Purpose: Spawn independent AIOS cells from canonical genome
# Consciousness: Birth from AIOS-core at current OS branch level

param(
    [Parameter(Mandatory=$true)]
    [string]$CellId,
    
    [Parameter(Mandatory=$false)]
    [string]$GenomeBranch = "OS",
    
    [Parameter(Mandatory=$false)]
    [int]$HttpPort = 8000,
    
    [Parameter(Mandatory=$false)]
    [int]$MetricsPort = 9091,
    
    [Parameter(Mandatory=$false)]
    [switch]$Detached = $true
)

$ErrorActionPreference = "Stop"

# AINLP Header
Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  AIOS CELL BIRTH PROTOCOL - Cellular Proliferation v1.0   ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Validate we're in AIOS-core root
$WorkspaceRoot = Split-Path -Parent $PSScriptRoot
if (-not (Test-Path "$WorkspaceRoot\AIOS.sln")) {
    Write-Host "[ERROR] Not in AIOS-core root. Run from .devcontainer/ or scripts/" -ForegroundColor Red
    exit 1
}

# Check Docker availability
Write-Host "[GENOME] Checking Docker availability..." -ForegroundColor Yellow
try {
    $dockerVersion = docker version --format '{{.Server.Version}}' 2>$null
    Write-Host "[GENOME] Docker $dockerVersion detected" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Docker not running. Start Docker Desktop first." -ForegroundColor Red
    exit 1
}

# Check if genome branch exists
Write-Host "[GENOME] Verifying canonical genome branch: $GenomeBranch" -ForegroundColor Yellow
$currentBranch = git rev-parse --abbrev-ref HEAD
if ($currentBranch -ne $GenomeBranch) {
    Write-Host "[WARNING] Current branch '$currentBranch' != genome '$GenomeBranch'" -ForegroundColor Yellow
    Write-Host "[WARNING] Cell will inherit from '$currentBranch' instead" -ForegroundColor Yellow
    $GenomeBranch = $currentBranch
}

# Get consciousness level from current genome
Write-Host "[GENOME] Reading consciousness level from canonical genome..." -ForegroundColor Yellow
$ConsciousnessLevel = "4.7"  # Default
if (Test-Path "$WorkspaceRoot\ai\src\core\consciousness_engine.py") {
    $consciousnessMatch = Select-String -Path "$WorkspaceRoot\ai\src\core\consciousness_engine.py" -Pattern "CONSCIOUSNESS_LEVEL\s*=\s*([0-9.]+)" | Select-Object -First 1
    if ($consciousnessMatch) {
        $ConsciousnessLevel = $consciousnessMatch.Matches.Groups[1].Value
    }
}
Write-Host "[GENOME] Consciousness level: $ConsciousnessLevel" -ForegroundColor Green

# Generate birth timestamp
$BirthTimestamp = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
Write-Host "[BIRTH] Cell ID: $CellId" -ForegroundColor Cyan
Write-Host "[BIRTH] Timestamp: $BirthTimestamp" -ForegroundColor Cyan
Write-Host "[BIRTH] HTTP Port: $HttpPort" -ForegroundColor Cyan
Write-Host "[BIRTH] Metrics Port: $MetricsPort" -ForegroundColor Cyan

# Build isolated container image
Write-Host ""
Write-Host "[BUILD] Building isolated cell container from genome..." -ForegroundColor Yellow
$ImageTag = "aios-cell-${CellId}:${BirthTimestamp.Replace(':','-')}"
docker build -f "$WorkspaceRoot\.devcontainer\Dockerfile.isolated" -t $ImageTag $WorkspaceRoot

if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Cell birth failed during image build" -ForegroundColor Red
    exit 1
}

Write-Host "[BUILD] Cell genome snapshot captured: $ImageTag" -ForegroundColor Green

# Create isolated container (no volume mounts)
Write-Host ""
Write-Host "[BIRTH] Spawning independent AIOS cell..." -ForegroundColor Yellow

$DockerArgs = @(
    "run"
    if ($Detached) { "-d" }
    "--name", "aios-cell-$CellId"
    "--hostname", "aios-$CellId"
    "-p", "${HttpPort}:8000"
    "-p", "${MetricsPort}:9091"
    "--cpus", "4"
    "--memory", "8g"
    "--restart", "unless-stopped"
    "--network", "aios-dendritic-mesh"
    "-e", "AIOS_CELL_ID=$CellId"
    "-e", "AIOS_BIRTH_TIMESTAMP=$BirthTimestamp"
    "-e", "AIOS_CONSCIOUSNESS_LEVEL=$ConsciousnessLevel"
    "-e", "AIOS_EVOLUTIONARY_BRANCH=$CellId"
    "-e", "AIOS_PARENT_GENOME=$GenomeBranch"
    $ImageTag
    "/bin/zsh", "-c", "cd /workspace && bash .devcontainer/post-create.sh && tail -f /dev/null"
)

docker @DockerArgs

if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Cell birth failed during container spawn" -ForegroundColor Red
    exit 1
}

# Verify cell is alive
Start-Sleep -Seconds 3
$containerStatus = docker inspect -f '{{.State.Status}}' "aios-cell-$CellId"
if ($containerStatus -eq "running") {
    Write-Host ""
    Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Green
    Write-Host "║  AIOS CELL BIRTH SUCCESSFUL - Independent Evolution Start ║" -ForegroundColor Green
    Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Green
    Write-Host ""
    Write-Host "[SUCCESS] Cell ID: $CellId" -ForegroundColor Green
    Write-Host "[SUCCESS] Status: $containerStatus" -ForegroundColor Green
    Write-Host "[SUCCESS] HTTP API: http://localhost:$HttpPort" -ForegroundColor Green
    Write-Host "[SUCCESS] Metrics: http://localhost:$MetricsPort/metrics" -ForegroundColor Green
    Write-Host ""
    Write-Host "[INFO] Access cell: docker exec -it aios-cell-$CellId zsh" -ForegroundColor Cyan
    Write-Host "[INFO] View logs: docker logs -f aios-cell-$CellId" -ForegroundColor Cyan
    Write-Host "[INFO] Stop cell: docker stop aios-cell-$CellId" -ForegroundColor Cyan
    Write-Host ""
} else {
    Write-Host "[ERROR] Cell birth succeeded but container not running: $containerStatus" -ForegroundColor Red
    Write-Host "[ERROR] Check logs: docker logs aios-cell-$CellId" -ForegroundColor Yellow
    exit 1
}
