#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Wrapper for root_clutter_guard.ps1 - forwards to canonical implementation.
.DESCRIPTION
    This wrapper script forwards execution to the canonical root_clutter_guard.ps1
    located in runtime/tools/scripts/ or runtime/tools/consolidated/.
#>
param(
    [Parameter(ValueFromRemainingArguments=$true)]
    [string[]]$RemainingArgs
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repoRoot = Split-Path $PSScriptRoot -Parent
$candidate1 = "$repoRoot/runtime/tools/scripts/root_clutter_guard.ps1"
$candidate2 = "$repoRoot/runtime/tools/consolidated/root_clutter_guard.ps1"

$target = $null
if (Test-Path $candidate1) { $target = $candidate1 }
elseif (Test-Path $candidate2) { $target = $candidate2 }

if (-not $target) {
    [Console]::Error.WriteLine("No canonical root_clutter_guard.ps1 found. Checked: $candidate1, $candidate2")
    exit 1
}

try {
    if ($RemainingArgs -and $RemainingArgs.Count -gt 0) {
        & $target @RemainingArgs
    } else {
        & $target
    }
    exit $LASTEXITCODE
} catch {
    [Console]::Error.WriteLine("Wrapper error: $_")
    exit 1
}
