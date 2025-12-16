# Surgical VSCode Python Interpreter Reset
# This forces VSCode to re-evaluate Python interpreters without affecting context

Write-Host "🎯 Surgical VSCode Python Interpreter Reset..." -ForegroundColor Yellow

# Force Python extension to reload interpreter settings
Write-Host "📋 Forcing Python extension to reload..." -ForegroundColor Cyan

# Create a temporary trigger file that forces re-evaluation
$triggerFile = "c:\dev\AIOS\.vscode\python_interpreter_reset_trigger"
$timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
"Reset triggered at: $timestamp" | Out-File -FilePath $triggerFile -Encoding UTF8

# Update the workspace file modification time to force VSCode to re-read it
$workspaceFile = "c:\dev\AIOS\AIOS.code-workspace"
if (Test-Path $workspaceFile) {
    Write-Host "📝 Updating workspace file timestamp..." -ForegroundColor Gray
    (Get-Item $workspaceFile).LastWriteTime = Get-Date
}

# Touch all settings.json files to force re-evaluation
$settingsFiles = @(
    "c:\dev\AIOS\.vscode\settings.json",
    "c:\dev\AIOS\chatgpt_integration\.vscode\settings.json",
    "c:\dev\AIOS\visual_interface\.vscode\settings.json",
    "c:\dev\AIOS\scripts\.vscode\settings.json",
    "c:\dev\AIOS\gemini_cli_bridge\.vscode\settings.json"
)

foreach ($file in $settingsFiles) {
    if (Test-Path $file) {
        Write-Host "  📄 Updating $file timestamp..." -ForegroundColor Gray
        (Get-Item $file).LastWriteTime = Get-Date
    }
}

Write-Host "✅ Surgical reset complete!" -ForegroundColor Green
Write-Host "🔄 Please run 'Python: Refresh Interpreters' command in VSCode" -ForegroundColor Yellow
Write-Host "   (Ctrl+Shift+P -> 'Python: Refresh Interpreters')" -ForegroundColor Yellow
