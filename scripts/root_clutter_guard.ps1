<#
 Root Clutter Guard
 Scans for deprecated root-level files that must not reappear and removes them.
 Currently guards: test_opencv_aios_integration.py (moved to scripts/legacy/)
 Extend list as needed.
#>
$GovernanceDir = Join-Path (Split-Path -Parent $MyInvocation.MyCommand.Definition | Split-Path -Parent) 'governance'
if (Test-Path (Join-Path $GovernanceDir 'deprecated_files.ps1')) {
    . (Join-Path $GovernanceDir 'deprecated_files.ps1')
    $DeprecatedRootFiles = $Global:AIOS_DeprecatedRootFiles
} else {
    $DeprecatedRootFiles = @(
        'test_opencv_aios_integration.py',
        'test_chatgpt_integration.py',
        'setup_environment.ps1',
        'terminal.ps1'
    )
}
$Root = Split-Path -Parent $MyInvocation.MyCommand.Definition | Split-Path -Parent
$Removed = @()
foreach ($f in $DeprecatedRootFiles){
    $path = Join-Path $Root $f
    if (Test-Path $path){
        $len = (Get-Item $path).Length
        Remove-Item $path -Force
        $Removed += [pscustomobject]@{ file=$f; length=$len; removed=(Get-Date).ToString('s') }
    }
}
if ($Removed.Count -gt 0){
    $log = Join-Path $Root 'root_clutter_guard.log'
    # Write each removal as a single JSON line (JSONL format) for easier ingestion
    foreach($r in $Removed){ $r | ConvertTo-Json -Depth 4 -Compress | Out-File -Append -FilePath $log -Encoding UTF8 }
    # Governance event logging (tachyonic archival)
    $eventsDir = Join-Path $Root 'docs/unified_backups/tachyonic_operations/governance_events'
    if (-not (Test-Path $eventsDir)) { New-Item -ItemType Directory -Path $eventsDir -Force | Out-Null }
    $eventFile = Join-Path $eventsDir 'events.jsonl'
    foreach($r in $Removed){
        $evRecord = [pscustomobject]@{
            type = 'root_deprecated_purge'
            file = $r.file
            length = $r.length
            ts = (Get-Date).ToString('o')
            actor = 'root_clutter_guard'
            policy = 'ROOT_HYGIENE_POLICY'
        }
        $evRecord | ConvertTo-Json -Depth 4 | Out-File -Append -FilePath $eventFile -Encoding UTF8
    }
    Write-Host "Removed deprecated root files:" ($Removed.file -join ', ')
    exit 1  # Non-zero exit to signal hygiene enforcement failure in CI
} else {
    Write-Host 'No deprecated root files found.'
}
