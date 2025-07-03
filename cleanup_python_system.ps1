# 🧹 AUTOMATED PYTHON CLEANUP SCRIPT
# Run this script as Administrator in PowerShell

Write-Host "🚨 CRITICAL: PYTHON SYSTEM CLEANUP STARTING" -ForegroundColor Red
Write-Host "This will remove ALL Python installations and configurations" -ForegroundColor Yellow

# Stop all Python processes
Write-Host "⏹️ Stopping all Python processes..."
Get-Process | Where-Object {$_.ProcessName -like "*python*"} | Stop-Process -Force -ErrorAction SilentlyContinue

# Remove Python directories
Write-Host "🗑️ Removing Python installation directories..."
$pythonDirs = @(
    "C:\Python*",
    "C:\ProgramData\miniconda3",
    "C:\ProgramData\Anaconda3",
    "$env:USERPROFILE\Anaconda3",
    "$env:USERPROFILE\Miniconda3",
    "$env:USERPROFILE\.conda",
    "$env:USERPROFILE\AppData\Local\Programs\Python*",
    "$env:USERPROFILE\AppData\Roaming\Python",
    "$env:USERPROFILE\AppData\Local\pip"
)

foreach ($dir in $pythonDirs) {
    if (Test-Path $dir) {
        Write-Host "Removing: $dir" -ForegroundColor Yellow
        Remove-Item -Recurse -Force $dir -ErrorAction SilentlyContinue
    }
}

# Clean registry entries (requires admin)
Write-Host "🔧 Cleaning registry entries..."
$regPaths = @(
    "HKLM:\SOFTWARE\Python",
    "HKCU:\SOFTWARE\Python",
    "HKLM:\SOFTWARE\WOW6432Node\Python"
)

foreach ($regPath in $regPaths) {
    if (Test-Path $regPath) {
        Write-Host "Removing registry: $regPath" -ForegroundColor Yellow
        Remove-Item -Recurse $regPath -Force -ErrorAction SilentlyContinue
    }
}

# Clean PATH environment variable
Write-Host "🛤️ Cleaning PATH environment variable..."
$machinePath = [Environment]::GetEnvironmentVariable("PATH", "Machine")
$userPath = [Environment]::GetEnvironmentVariable("PATH", "User")

$cleanMachinePath = ($machinePath -split ';' | Where-Object { 
    $_ -notlike "*Python*" -and 
    $_ -notlike "*Anaconda*" -and 
    $_ -notlike "*Miniconda*" -and
    $_ -notlike "*conda*"
}) -join ';'

$cleanUserPath = ($userPath -split ';' | Where-Object { 
    $_ -notlike "*Python*" -and 
    $_ -notlike "*Anaconda*" -and 
    $_ -notlike "*Miniconda*" -and
    $_ -notlike "*conda*"
}) -join ';'

[Environment]::SetEnvironmentVariable("PATH", $cleanMachinePath, "Machine")
[Environment]::SetEnvironmentVariable("PATH", $cleanUserPath, "User")

# Remove Python environment variables
Write-Host "🔧 Removing Python environment variables..."
[Environment]::SetEnvironmentVariable("PYTHONPATH", $null, "Machine")
[Environment]::SetEnvironmentVariable("PYTHONHOME", $null, "Machine")
[Environment]::SetEnvironmentVariable("PYTHONPATH", $null, "User")
[Environment]::SetEnvironmentVariable("PYTHONHOME", $null, "User")

Write-Host "✅ PYTHON CLEANUP COMPLETED!" -ForegroundColor Green
Write-Host "🔄 RESTART COMPUTER NOW for changes to take effect" -ForegroundColor Red
Write-Host "📥 Then download Python 3.12 from https://www.python.org/downloads/" -ForegroundColor Cyan

Read-Host "Press Enter to continue..."
