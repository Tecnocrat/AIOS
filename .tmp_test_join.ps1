$a = Join-Path 'C:\dev\AIOS' 'runtime/tools/scripts/dev_terminal.ps1'
$b = Join-Path 'C:\dev\AIOS' 'runtime/tools/consolidated/dev_terminal.ps1'
$arr=@($a,$b)
foreach ($item in $arr) { Write-Host "ITEM: $item"; Write-Host "TYPE: $($item.GetType().FullName)" }
