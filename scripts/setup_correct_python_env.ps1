# AIOS Python Environment Setup Script
# Creates proper Windows-style virtual environment for TensorFlow cellular integration

Write-Host "🧬 Setting up AIOS Python Environment for TensorFlow Cellular Integration" -ForegroundColor Green

# Remove existing problematic venv
if (Test-Path "ai\venv") {
    Write-Host "Removing existing virtual environment..." -ForegroundColor Yellow
    Remove-Item "ai\venv" -Recurse -Force
}

# Create new virtual environment with system Python
Write-Host "Creating new virtual environment..." -ForegroundColor Yellow
python -m venv ai\venv

# Verify Windows-style structure
if (Test-Path "ai\venv\Scripts\python.exe") {
    Write-Host "✅ Virtual environment created successfully!" -ForegroundColor Green

    # Activate and install minimal requirements
    Write-Host "Installing minimal requirements..." -ForegroundColor Yellow
    & ai\venv\Scripts\python.exe -m pip install --upgrade pip
    & ai\venv\Scripts\python.exe -m pip install numpy pandas pathlib tempfile

    Write-Host "✅ Python environment ready for TensorFlow cellular integration tests!" -ForegroundColor Green
    Write-Host "📍 Test file location: tests\integration\test_tensorflow_cellular_integration.py" -ForegroundColor Cyan

} else {
    Write-Host "❌ Failed to create proper Windows virtual environment" -ForegroundColor Red
    Write-Host "Please ensure you're using Windows Python (not MSYS2)" -ForegroundColor Yellow
}
