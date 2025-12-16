# VSCode Python Interpreter Cache Cleanup
# This script cleans VSCode's Python interpreter discovery cache

Write-Host "🧹 Cleaning VSCode Python Interpreter Cache..." -ForegroundColor Yellow

# VSCode cache locations
$vscodeExtensionsPath = "$env:USERPROFILE\.vscode\extensions"
$pythonExtensionCache = "$vscodeExtensionsPath\ms-python.*\pythonFiles\lib\python\*\*\*cache*"

# Clean Python extension cache
Write-Host "📂 Cleaning Python extension cache..." -ForegroundColor Cyan
if (Test-Path $vscodeExtensionsPath) {
    Get-ChildItem -Path $vscodeExtensionsPath -Filter "ms-python*" -Directory | ForEach-Object {
        $cachePath = Join-Path $_.FullName "pythonFiles\lib\python"
        if (Test-Path $cachePath) {
            Write-Host "  🗑️ Clearing cache in $($_.Name)" -ForegroundColor Gray
            Get-ChildItem -Path $cachePath -Recurse -Directory -Name "*cache*" -ErrorAction SilentlyContinue | 
                ForEach-Object { Remove-Item -Path (Join-Path $cachePath $_) -Recurse -Force -ErrorAction SilentlyContinue }
        }
    }
}

# Clean VSCode workspace state
$workspaceStatePath = "$env:APPDATA\Code\User\workspaceStorage"
Write-Host "📂 Cleaning workspace storage..." -ForegroundColor Cyan
if (Test-Path $workspaceStatePath) {
    Get-ChildItem -Path $workspaceStatePath -Directory | ForEach-Object {
        $workspaceJsonPath = Join-Path $_.FullName "workspace.json"
        if (Test-Path $workspaceJsonPath) {
            $content = Get-Content $workspaceJsonPath -Raw -ErrorAction SilentlyContinue
            if ($content -and $content.Contains("AIOS")) {
                Write-Host "  🗑️ Clearing AIOS workspace cache: $($_.Name)" -ForegroundColor Gray
                Remove-Item -Path $_.FullName -Recurse -Force -ErrorAction SilentlyContinue
            }
        }
    }
}

Write-Host "✅ VSCode cache cleanup complete!" -ForegroundColor Green
Write-Host "🔄 Please reload VSCode window (Ctrl+Shift+P -> 'Developer: Reload Window')" -ForegroundColor Yellow
