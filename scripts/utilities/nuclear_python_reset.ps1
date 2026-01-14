# AIOS Python Interpreter Nuclear Reset
# This script completely resets VSCode's Python interpreter configuration

Write-Host "🚀 AIOS Python Interpreter Nuclear Reset" -ForegroundColor Red
Write-Host "=" * 50 -ForegroundColor Red

# Kill all Python processes that might be interfering
Write-Host "🔪 Terminating all Python processes..." -ForegroundColor Yellow
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Write-Host "✅ Python processes terminated" -ForegroundColor Green

# Clean VSCode workspace cache completely
Write-Host "🧹 Nuclear cleaning VSCode workspace cache..." -ForegroundColor Yellow
$workspaceStatePath = "$env:APPDATA\Code\User\workspaceStorage"
if (Test-Path $workspaceStatePath) {
    Remove-Item -Path $workspaceStatePath -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "✅ Workspace storage nuked" -ForegroundColor Green
}

# Clean Python extension cache
Write-Host "🧹 Nuclear cleaning Python extension cache..." -ForegroundColor Yellow
$pythonExtCache = "$env:USERPROFILE\.vscode\extensions\ms-python*"
Get-Item $pythonExtCache -ErrorAction SilentlyContinue | ForEach-Object {
    $cachePath = Join-Path $_.FullName "pythonFiles"
    if (Test-Path $cachePath) {
        Remove-Item -Path $cachePath -Recurse -Force -ErrorAction SilentlyContinue
    }
}
Write-Host "✅ Python extension cache nuked" -ForegroundColor Green

# Clean global VSCode settings cache
Write-Host "🧹 Cleaning global VSCode settings..." -ForegroundColor Yellow
$globalSettingsPath = "$env:APPDATA\Code\User\settings.json"
if (Test-Path $globalSettingsPath) {
    $settings = Get-Content $globalSettingsPath -Raw | ConvertFrom-Json -ErrorAction SilentlyContinue
    if ($settings) {
        # Remove any Python interpreter settings from global config
        $settings.PSObject.Properties | Where-Object { $_.Name -like "python.*" } | ForEach-Object {
            $settings.PSObject.Properties.Remove($_.Name)
        }
        $settings | ConvertTo-Json -Depth 10 | Set-Content $globalSettingsPath -ErrorAction SilentlyContinue
    }
}
Write-Host "✅ Global settings cleaned" -ForegroundColor Green

# Force VSCode to reload
Write-Host "🔄 Configuration complete!" -ForegroundColor Green
Write-Host ""
Write-Host "🎯 NEXT STEPS:" -ForegroundColor Cyan
Write-Host "1. Close ALL VSCode windows" -ForegroundColor White
Write-Host "2. Reopen VSCode with: code c:\dev\AIOS\AIOS.code-workspace" -ForegroundColor White
Write-Host "3. Python interpreter should be automatically detected" -ForegroundColor White
Write-Host ""
Write-Host "🧪 TEST: Open chatgpt.py - no interpreter selection should appear!" -ForegroundColor Yellow
