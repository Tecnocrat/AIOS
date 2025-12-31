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
Write-Host "DEBUG: PSScriptRoot=[$PSScriptRoot] (Type: $($PSScriptRoot.GetType().FullName))"
Write-Host "DEBUG: repoRoot=[$repoRoot] (Type: $($repoRoot.GetType().FullName))"
$candidate1 = "$repoRoot\runtime\tools\scripts\dev_terminal.ps1"
$candidate2 = "$repoRoot\runtime\tools\consolidated\dev_terminal.ps1"

Write-Host "DEBUG: candidate1=[$candidate1]"
Write-Host "DEBUG: candidate2=[$candidate2]"

$target = $null
if (Test-Path $candidate1) { $target = $candidate1 }
elseif (Test-Path $candidate2) { $target = $candidate2 }

if (-not $target) {
    Write-Error "No canonical dev_terminal.ps1 found. Checked: $($candidates -join ', ')"
    exit 1
}

# Forward parameters to the canonical script
try {
    $argList = @('-File', $target, '-Action', $Action)
    if ($ReportCoherence) { $argList += '-ReportCoherence' }
    if ($CoherenceFormat) { $argList += @('-CoherenceFormat', $CoherenceFormat) }
    if ($Quiet) { $argList += '-Quiet' }

    $proc = Start-Process pwsh -ArgumentList $argList -NoNewWindow -PassThru -Wait
    $exit = $proc.ExitCode
    if ($exit -ne 0) {
        Write-Error "Canonical dev_terminal exited with code $exit"
    }
    exit $exit
} catch {
    Write-Host "Wrapper error: $($_ | Out-String)"
    if ($_.Exception) { $_.Exception | Format-List * -Force }
    exit 1
}
