# AIOS Quick Setup Script for Windows
Write-Host "AIOS - Artificial Intelligence Operating System" -ForegroundColor Cyan
Write-Host "Quick Setup Script" -ForegroundColor Green
Write-Host "="*60 -ForegroundColor Cyan

# Check if we're in the correct directory
if (!(Test-Path "AIOS_PROJECT_CONTEXT.md")) {
    Write-Error "Please run this script from the AIOS project root directory"
    exit 1
}

Write-Host "Setting up AIOS development environment..." -ForegroundColor Yellow

# Create Python virtual environment
Write-Host "`nCreating Python virtual environment..." -ForegroundColor Yellow
if (!(Test-Path "ai/venv")) {
    python -m venv ai/venv
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Python virtual environment created successfully!" -ForegroundColor Green
    } else {
        Write-Warning "Failed to create Python virtual environment. Please ensure Python is installed."
    }
}

# Install Python dependencies
Write-Host "`nInstalling Python dependencies..." -ForegroundColor Yellow
if (Test-Path "ai/venv/Scripts/activate.ps1") {
    & ai/venv/Scripts/activate.ps1
    pip install -r ai/requirements.txt
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Python dependencies installed successfully!" -ForegroundColor Green
    } else {
        Write-Warning "Some Python dependencies may have failed to install"
    }
}

# Setup C++ build directory
Write-Host "`nSetting up C++ build directory..." -ForegroundColor Yellow
if (!(Test-Path "build")) {
    New-Item -ItemType Directory -Path "build" | Out-Null
    Write-Host "Build directory created!" -ForegroundColor Green
}

# Configure CMake (if available)
Write-Host "`nConfiguring CMake..." -ForegroundColor Yellow
Set-Location "build"
cmake ../core -DCMAKE_BUILD_TYPE=Debug
if ($LASTEXITCODE -eq 0) {
    Write-Host "CMake configured successfully!" -ForegroundColor Green
} else {
    Write-Warning "CMake configuration failed. Please install CMake and required dependencies."
}
Set-Location ".."

# Setup C# projects (if .NET is available)
Write-Host "`nSetting up C# projects..." -ForegroundColor Yellow
Set-Location "interface"
dotnet new sln -n AIOS --force
dotnet new classlib -n AIOS.Models --force
dotnet new classlib -n AIOS.Services --force
dotnet new wpf -n AIOS.UI --force

dotnet sln add AIOS.Models/AIOS.Models.csproj
dotnet sln add AIOS.Services/AIOS.Services.csproj
dotnet sln add AIOS.UI/AIOS.UI.csproj

dotnet add AIOS.Services/AIOS.Services.csproj reference AIOS.Models/AIOS.Models.csproj
dotnet add AIOS.UI/AIOS.UI.csproj reference AIOS.Services/AIOS.Services.csproj

if ($LASTEXITCODE -eq 0) {
    Write-Host "C# projects created successfully!" -ForegroundColor Green
} else {
    Write-Warning "C# project creation failed. Please install .NET SDK."
}
Set-Location ".."

# Summary
Write-Host "`n" + "="*60 -ForegroundColor Cyan
Write-Host "AIOS Setup Complete!" -ForegroundColor Green
Write-Host "="*60 -ForegroundColor Cyan

Write-Host "`nProject structure created:" -ForegroundColor Yellow
Write-Host "  - C++ Core (core/)" -ForegroundColor Green
Write-Host "  - C# Interface (interface/)" -ForegroundColor Green
Write-Host "  - Python AI (ai/)" -ForegroundColor Green
Write-Host "  - Configuration (config/)" -ForegroundColor Green
Write-Host "  - Documentation (docs/)" -ForegroundColor Green

Write-Host "`nNext steps:" -ForegroundColor Yellow
Write-Host "1. Open the project in Visual Studio Code" -ForegroundColor White
Write-Host "2. Use Ctrl+Shift+P and run 'AIOS: Test AI Core' to test the system" -ForegroundColor White
Write-Host "3. Review the documentation in docs/ folder" -ForegroundColor White
Write-Host "4. Start developing your AI operating system!" -ForegroundColor White

Write-Host "`nFor detailed information, see AIOS_PROJECT_CONTEXT.md" -ForegroundColor Cyan
Write-Host "Happy coding!" -ForegroundColor Green
