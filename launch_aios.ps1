<#
Deprecated Root Stub (2025-08-17)
The launcher has moved to scripts/launch_aios.ps1 for root hygiene.
Keep this stub minimal; update any shortcuts or docs still pointing here.
#>
Write-Host "[AIOS] launcher relocated -> use scripts/launch_aios.ps1" -ForegroundColor Cyan
& "$PSScriptRoot\scripts\launch_aios.ps1" @args
