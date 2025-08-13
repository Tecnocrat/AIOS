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
    $Removed | ConvertTo-Json -Depth 3 | Out-File -Append -FilePath $log -Encoding UTF8
    Write-Host "Removed deprecated root files:" ($Removed.file -join ', ')
    exit 1  # Non-zero exit to signal hygiene enforcement failure in CI
} else {
    Write-Host 'No deprecated root files found.'
}
