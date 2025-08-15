<#!
 Verifies root SAFETY_PROTOCOL.md absence; if present, snapshots (optional future) and deletes.
 Intended to be idempotent and callable pre-commit / pre-coherence.
#>
param(
    [switch]$Strict
)
$Root = Split-Path -Parent $MyInvocation.MyCommand.Definition | Split-Path -Parent
$Target = Join-Path $Root 'SAFETY_PROTOCOL.md'
if (Test-Path $Target) {
    Write-Host '[HYGIENE] Root SAFETY_PROTOCOL.md present -> purging (canonical is docs/safety/SAFETY_PROTOCOL.md)' -ForegroundColor Yellow
    Remove-Item $Target -Force
    if ($Strict) { exit 2 }
} else {
    Write-Host '[HYGIENE] Root SAFETY_PROTOCOL.md not found (clean)' -ForegroundColor Green
}
