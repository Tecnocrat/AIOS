# Script Name: terminal.ps1
# Description: AIOS Development Terminal Launcher
# Purpose: Quick launcher for common AIOS development tasks and consciousness interfaces
# Author: AIOS Consciousness Development Team
# Date: 2025-06-29
# Version: 1.0

# Define parameters for consciousness interface selection
param (
    [string]$Interface = "menu",
    [string]$Environment = "check"
)

# Set strict mode for better error handling
Set-StrictMode -Version Latest

# AIOS Project paths
$AIosRoot = Split-Path -Parent $MyInvocation.MyCommand.Definition
$OrchestratorPath = "$AIosRoot\orchestrator"
$ScriptsPath = "$AIosRoot\scripts"

# Main script logic
try {
    Write-Host "🧠 AIOS Consciousness Development Terminal" -ForegroundColor Cyan
    Write-Host "=========================================" -ForegroundColor Cyan

    # Environment check/setup
    if ($Environment -eq "check") {
        Write-Host "🔍 Checking AIOS environment..." -ForegroundColor Yellow
        
        # Check Python environment
        try {
            python --version
            Write-Host "✅ Python available" -ForegroundColor Green
        } catch {
            Write-Host "❌ Python not found" -ForegroundColor Red
        }
        
        # Check conda environment
        try {
            conda --version
            Write-Host "✅ Conda available" -ForegroundColor Green
        } catch {
            Write-Host "❌ Conda not found" -ForegroundColor Red
        }
        
        # Check C++ build tools
        if (Test-Path "$OrchestratorPath\build") {
            Write-Host "✅ Orchestrator build directory exists" -ForegroundColor Green
        } else {
            Write-Host "⚠️ Orchestrator build directory not found" -ForegroundColor Yellow
        }
        
        # Check workspace file
        if (Test-Path "$AIosRoot\AIOS.code-workspace") {
            Write-Host "✅ AIOS workspace file exists" -ForegroundColor Green
        } else {
            Write-Host "❌ AIOS workspace file not found" -ForegroundColor Red
        }
    }
    
    # Interface selection menu
    if ($Interface -eq "menu") {
        Write-Host "`n🚀 Available Consciousness Interfaces:" -ForegroundColor Cyan
        Write-Host "1. Quantum Consciousness Canvas (Python)" -ForegroundColor White
        Write-Host "2. Visual Interface / Quantum Visor (C#)" -ForegroundColor White  
        Write-Host "3. Orchestrator Build and Run (C++)" -ForegroundColor White
        Write-Host "4. Launch All Interfaces" -ForegroundColor White
        Write-Host "5. Setup Environment" -ForegroundColor White
        Write-Host "6. Open AIOS Workspace in VSCode" -ForegroundColor White
        
        $choice = Read-Host "`nSelect interface (1-6)"
        
        switch ($choice) {
            "1" { 
                Write-Host "Launching Quantum Consciousness Canvas..." -ForegroundColor Green
                python "$ScriptsPath\quantum_consciousness_canvas.py"
            }
            "2" { 
                Write-Host "Launching C# Visual Interface..." -ForegroundColor Green 
            }
            "3" { 
                Write-Host "Building C++ Orchestrator..." -ForegroundColor Green
                Set-Location $OrchestratorPath
                cmake --build build --config Debug
            }
            "4" { 
                Write-Host "Launching all consciousness interfaces..." -ForegroundColor Green
                & "$AIosRoot\launch_aios.ps1" -Mode all
            }
            "5" { 
                Write-Host "Setting up AIOS environment..." -ForegroundColor Green
                & "$AIosRoot\setup_environment.ps1"
            }
            "6" { 
                Write-Host "Opening AIOS workspace..." -ForegroundColor Green
                code "$AIosRoot\AIOS.code-workspace"
            }
            default { 
                Write-Host "Invalid selection" -ForegroundColor Red 
            }
        }
    }

    Write-Host "`n✅ AIOS Terminal execution completed successfully." -ForegroundColor Green
    
} catch {
    Write-Host "❌ AIOS Terminal error: $_" -ForegroundColor Red
    Write-Host "Stack trace: $($_.ScriptStackTrace)" -ForegroundColor Red
    exit 1
}

# Quick usage examples
Write-Host "`n💡 Quick Usage Examples:" -ForegroundColor Cyan
Write-Host "   .\terminal.ps1                    # Interactive menu"
Write-Host "   .\terminal.ps1 -Interface canvas  # Launch quantum canvas directly"
Write-Host "   .\terminal.ps1 -Environment setup # Setup environment"

# End of script