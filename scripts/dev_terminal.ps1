#!/usr/bin/env pwsh
param(
    [Parameter(Mandatory=$false)]
    [string]$Action = "workspace",

    [Parameter(Mandatory=$false)]
    [switch]$ReportCoherence,

    [Parameter(Mandatory=$false)]
    [string]$CoherenceFormat = "json",

    [Parameter(Mandatory=$false)]
    [switch]$Quiet
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# Resolve canonical script locations and prefer runtime/tools/scripts first
$repoRoot = Split-Path $PSScriptRoot -Parent
$candidates = @(
    Join-Path $repoRoot "runtime/tools/scripts/dev_terminal.ps1",
    Join-Path $repoRoot "runtime/tools/consolidated/dev_terminal.ps1"
)

$target = $null
foreach ($path in $candidates) {
    if (Test-Path $path) { $target = $path; break }
}

if (-not $target) {
    Write-Error "No canonical dev_terminal.ps1 found. Checked: $($candidates -join ', ')"
    exit 1
}

# Forward parameters to the canonical script
& $target -Action $Action -ReportCoherence:$ReportCoherence -CoherenceFormat $CoherenceFormat -Quiet:$Quiet

exit $LASTEXITCODE
