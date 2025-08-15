<#
 Generates a JSON snapshot of the repository folder structure similar to the existing
 docs/AIOS/folder_structure.json format.
 - Includes every directory as a key whose value has 'folders' and 'files' arrays.
 - Root directory key is an empty string "" (matching prior convention).
 - Excludes deprecated root files from the root file list (governance list) to avoid
   reintroducing them into the inventory snapshot.
 Usage:
   pwsh -File scripts/generate_folder_structure.ps1
   pwsh -File scripts/generate_folder_structure.ps1 -Output docs/AIOS/folder_structure.json
#>
param(
  [string]$Output = 'docs/AIOS/folder_structure.json'
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$Root = Split-Path -Parent $MyInvocation.MyCommand.Definition | Split-Path -Parent

# Load deprecated list (root only relevance)
$GovernanceDir = Join-Path $Root 'governance'
$DeprecatedRoot = @()
if (Test-Path (Join-Path $GovernanceDir 'deprecated_files.ps1')) {
  . (Join-Path $GovernanceDir 'deprecated_files.ps1')
  if ($Global:AIOS_DeprecatedRootFiles) { $DeprecatedRoot = $Global:AIOS_DeprecatedRootFiles }
}

function Get-RelativePath([string]$full){
  $rel = $full.Substring($Root.Length)
  # Normalize leading separators via regex
  return ($rel -replace '^[\\/]+','')
}

$map = @{}

function Ensure-Entry([string]$rel){
  if (-not $map.ContainsKey($rel)) { $map[$rel] = [ordered]@{ folders = @(); files = @() } }
}

# Walk directories
Get-ChildItem -LiteralPath $Root -Recurse -Force | ForEach-Object {
  $rel = Get-RelativePath $_.FullName
  if (-not $rel) { return }
  $parent = Split-Path $rel
  if ($_.PSIsContainer) {
    if ($parent -eq '.') { $parent = '' }
    Ensure-Entry $parent
    Ensure-Entry $rel
    $name = Split-Path $rel -Leaf
    if ($name -ne '' -and $map[$parent].folders -notcontains $name) { $map[$parent].folders += $name }
  } else {
    if ($parent -eq '.') { $parent = '' }
    Ensure-Entry $parent
    $name = Split-Path $rel -Leaf
    if ($parent -eq '' -and $DeprecatedRoot -contains $name) { return } # exclude deprecated root files
    if ($map[$parent].files -notcontains $name) { $map[$parent].files += $name }
  }
}

# Sort for determinism
foreach($k in $map.Keys){
  $map[$k].folders = @($map[$k].folders | Sort-Object)
  $map[$k].files   = @($map[$k].files   | Sort-Object)
}

# Root key required
Ensure-Entry ''

# Ensure output directory
$outPath = Join-Path $Root $Output
$outDir  = Split-Path $outPath -Parent
if (-not (Test-Path $outDir)) { New-Item -ItemType Directory -Path $outDir -Force | Out-Null }

# Ordered PSCustomObject for stable JSON (root first)
$ordered = New-Object System.Collections.Specialized.OrderedDictionary
if ($map.ContainsKey('')) { $ordered[''] = $map[''] }
foreach($k in ($map.Keys | Where-Object { $_ -ne '' } | Sort-Object)) { $ordered[$k] = $map[$k] }

$json = $ordered | ConvertTo-Json -Depth 100
Set-Content -Path $outPath -Value $json -Encoding UTF8
Write-Host "Folder structure snapshot written: $outPath"
