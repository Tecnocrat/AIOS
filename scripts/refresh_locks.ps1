<#
pip-tools lock refresh script
Generates consolidated lock file(s) from requirements.in using pip-compile.
Appends hash summary for governance; non-destructive (writes into locks/).
#>

param(
  [switch]$Quiet
)
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Definition)
$reqIn = Join-Path $Root 'requirements.in'
if (-not (Test-Path $reqIn)) { Write-Host '[ERROR] requirements.in missing' -ForegroundColor Red; exit 3 }
$locksDir = Join-Path $Root 'locks'
if (-not (Test-Path $locksDir)) { New-Item -ItemType Directory -Path $locksDir | Out-Null }
# Ensure pip-tools present
pip show pip-tools 1>$null 2>$null; if ($LASTEXITCODE -ne 0) { Write-Host '[INFO] Installing pip-tools' -ForegroundColor Yellow; pip install pip-tools | Out-Null }
$timestamp = Get-Date -Format 'yyyyMMdd_HHmmss'
$lockFile = Join-Path $locksDir "requirements.lock.txt"
$cmd = "pip-compile --quiet --generate-hashes --output-file $lockFile $reqIn"
if (-not $Quiet){ Write-Host "[INFO] Executing: $cmd" -ForegroundColor Cyan }
$env:PIP_TOOLS_CACHE_DIR = Join-Path $locksDir '.cache'
# Execute compile
pip-compile --generate-hashes --output-file "$lockFile" "$reqIn"
if ($LASTEXITCODE -ne 0) { Write-Host '[ERROR] pip-compile failed' -ForegroundColor Red; exit 2 }
# Copy timestamped snapshot
Copy-Item $lockFile (Join-Path $locksDir "requirements.lock_$timestamp.txt") -Force
$hash = (Get-FileHash -Algorithm SHA256 -Path $lockFile).Hash
$meta = [pscustomobject]@{ type='lock_refresh'; file='requirements.lock.txt'; sha256=$hash; ts=$timestamp }
$metaFile = Join-Path $locksDir 'lock_events.jsonl'
$meta | ConvertTo-Json -Compress | Add-Content -Path $metaFile -Encoding UTF8
if (-not $Quiet){ Write-Host "[INFO] Lock refreshed sha256=$hash" -ForegroundColor Green }
