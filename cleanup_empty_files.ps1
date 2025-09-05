# Script to clean up empty files that reappeared after VSCode restart
# Focus on user files, exclude venv and node_modules

$emptyFiles = @()

# Get all empty files
Get-ChildItem -Path "C:\dev\AIOS" -Recurse -File | Where-Object { 
    $_.Length -eq 0 -and 
    $_.FullName -notlike "*\venv\*" -and 
    $_.FullName -notlike "*\node_modules\*" -and
    $_.FullName -notlike "*\__pycache__\*" -and
    $_.FullName -notlike "*\.git\*"
} | ForEach-Object {
    $emptyFiles += $_.FullName
    Write-Host "Found empty file: $($_.FullName)" -ForegroundColor Yellow
}

Write-Host "`nFound $($emptyFiles.Count) empty user files" -ForegroundColor Cyan

if ($emptyFiles.Count -gt 0) {
    Write-Host "`nDeleting empty files..." -ForegroundColor Red
    foreach ($file in $emptyFiles) {
        try {
            Remove-Item -Path $file -Force
            Write-Host "Deleted: $file" -ForegroundColor Green
        } catch {
            Write-Host "Failed to delete: $file - $_" -ForegroundColor Red
        }
    }
    Write-Host "`nCleanup completed!" -ForegroundColor Green
} else {
    Write-Host "No empty files to clean up." -ForegroundColor Green
}
