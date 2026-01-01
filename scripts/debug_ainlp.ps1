# Debug AINLP validation
$file = 'test_consciousness_validation.py'
$content = Get-Content $file -Raw

Write-Host "File: $file"
Write-Host "Matches extension: $($file -match '\.(py|cs|ps1)$')"
Write-Host "Matches intelligence: $($file -match 'intelligence|consciousness')"
Write-Host "Content length: $($content.Length)"
Write-Host "Content contains AINLP/dendritic: $($content -match 'AINLP|dendritic')"
Write-Host "Should trigger validation: $(($file -match '\.(py|cs|ps1)$') -and ($file -match 'intelligence|consciousness') -and ($content -notmatch 'AINLP|dendritic'))"