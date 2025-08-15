<#!
 Purge legacy root safety documents that have canonical copies under docs/safety.
#>
$Root = Split-Path -Parent $MyInvocation.MyCommand.Definition | Split-Path -Parent
$Targets = @('SAFETY_PROTOCOL.md','SAFETY_IMPLEMENTATION_SUMMARY.md')
$Removed = @()
foreach($t in $Targets){
  $p = Join-Path $Root $t
  if (Test-Path $p){
    Remove-Item $p -Force
    $Removed += $t
  }
}
if($Removed.Count -gt 0){
  Write-Host "[SAFETY_DOC_HYGIENE] Removed: $($Removed -join ', ')" -ForegroundColor Yellow
}else{
  Write-Host "[SAFETY_DOC_HYGIENE] Clean (no root safety docs)" -ForegroundColor Green
}
