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
$candidate1 = "$repoRoot/runtime/tools/scripts/dev_terminal.ps1"
$candidate2 = "$repoRoot/runtime/tools/consolidated/dev_terminal.ps1"

$target = $null
if (Test-Path $candidate1) { $target = $candidate1 }
elseif (Test-Path $candidate2) { $target = $candidate2 }

if (-not $target) {
    [Console]::Error.WriteLine("No canonical dev_terminal.ps1 found. Checked: $candidate1, $candidate2")
    exit 1
}

# Forward parameters to the canonical script - use dot-sourcing or direct invocation
# This ensures stdout flows through without corruption
try {
    $argList = @()
    $argList += '-Action'; $argList += $Action
    if ($ReportCoherence) { $argList += '-ReportCoherence' }
    if ($CoherenceFormat) { $argList += '-CoherenceFormat'; $argList += $CoherenceFormat }
    if ($Quiet) { $argList += '-Quiet' }

    & $target @argList
    exit $LASTEXITCODE
} catch {
    [Console]::Error.WriteLine("Wrapper error: $_")
    exit 1
}
