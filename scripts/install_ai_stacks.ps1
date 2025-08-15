<#!
AIOS Composite Stack Installer
Usage examples:
  pwsh -File scripts/install_ai_stacks.ps1 -Stacks extras,dev
  pwsh -File scripts/install_ai_stacks.ps1 -Stacks all
#>
param(
  [Parameter(Mandatory=$true)][string]$Stacks,
  [string]$Pip='pip'
)
$ErrorActionPreference='Stop'
$Root = Split-Path -Parent $MyInvocation.MyCommand.Definition | Split-Path -Parent
$Map = @{
  'extras' = 'ai/deps/requirements_extras.txt'
  'quantum' = 'ai/deps/requirements_quantum.txt'
  'dev' = 'ai/deps/requirements_dev.txt'
  'graph' = 'ai/deps/requirements_future_graph.txt'
  'perf' = 'ai/deps/requirements_perf_serial.txt'
}
if ($Stacks -eq 'all') { $selected = $Map.Keys } else { $selected = $Stacks.Split(',') | ForEach-Object { $_.Trim().ToLower() } }
$files = @()
foreach($s in $selected){
  if (-not $Map.ContainsKey($s)) { Write-Host "Unknown stack: $s" -ForegroundColor Red; exit 2 }
  $p = Join-Path $Root $Map[$s]
  if (-not (Test-Path $p)) { Write-Host "Missing file for stack $s ($p)" -ForegroundColor Red; exit 3 }
  $files += $p
}
Write-Host "Installing stacks: $($selected -join ', ')" -ForegroundColor Cyan
foreach($f in $files){
  Write-Host "-> $f" -ForegroundColor Yellow
  & $Pip install -r $f
  if ($LASTEXITCODE -ne 0) { Write-Host "Install failed for $f" -ForegroundColor Red; exit 4 }
}
Write-Host 'Stack installation complete.' -ForegroundColor Green
