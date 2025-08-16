# AIOS Consciousness Emergence System - Unified Launcher
# Advanced PowerShell script for launching dual-interface consciousness system

param(
    [string]$Mode = "canvas",       # "canvas", "dual", "ingestor", "visor", "setup"
    [switch]$Verbose,              # Verbose output
    [switch]$Force,                # Force environment recreation
    [string]$Environment = "conda" # "conda" or "venv"
)

# Enhanced console output with colors
function Write-ConsciousnessOutput {
    param([string]$Message, [string]$Type = "INFO")
    $timestamp = Get-Date -Format "HH:mm:ss"
    
    switch ($Type) {
        "TITLE" { 
            Write-Host "`n🧠 $Message" -ForegroundColor Cyan
            Write-Host ("=" * ($Message.Length + 3)) -ForegroundColor Cyan
        }
        "SUCCESS" { Write-Host "[$timestamp] ✅ $Message" -ForegroundColor Green }
        "INFO" { Write-Host "[$timestamp] ℹ️  $Message" -ForegroundColor White }
        "WARN" { Write-Host "[$timestamp] ⚠️  $Message" -ForegroundColor Yellow }
        "ERROR" { Write-Host "[$timestamp] ❌ $Message" -ForegroundColor Red }
        "QUANTUM" { Write-Host "[$timestamp] 🌌 $Message" -ForegroundColor Magenta }
        "LAUNCH" { Write-Host "[$timestamp] 🚀 $Message" -ForegroundColor Cyan }
        default { Write-Host "[$timestamp] $Message" -ForegroundColor Gray }
    }
}

function Test-Prerequisites {
    Write-ConsciousnessOutput "Checking system prerequisites..." "INFO"
    
    $issues = @()
    
    # Check PowerShell version
    if ($PSVersionTable.PSVersion.Major -lt 5) {
        $issues += "PowerShell 5.1+ required (current: $($PSVersionTable.PSVersion))"
    }
    
    # Check Python
    try {
        $pythonVersion = & python --version 2>$null
        if (-not $pythonVersion) {
            $issues += "Python not found in PATH"
        } else {
            Write-ConsciousnessOutput "Python found: $pythonVersion" "SUCCESS"
        }
    } catch {
        $issues += "Python not accessible"
    }
    
    # Check .NET
    try {
        $dotnetVersion = & dotnet --version 2>$null
        if (-not $dotnetVersion) {
            $issues += ".NET SDK not found"
        } else {
            Write-ConsciousnessOutput ".NET found: $dotnetVersion" "SUCCESS"
        }
    } catch {
        $issues += ".NET SDK not accessible"
    }
    
    # Check conda (if specified)
    if ($Environment -eq "conda") {
        try {
            $condaVersion = & conda --version 2>$null
            if (-not $condaVersion) {
                Write-ConsciousnessOutput "Conda not found, falling back to venv" "WARN"
                $script:Environment = "venv"
            } else {
                Write-ConsciousnessOutput "Conda found: $condaVersion" "SUCCESS"
            }
        } catch {
            Write-ConsciousnessOutput "Conda not accessible, using venv" "WARN"
            $script:Environment = "venv"
        }
    }
    
    if ($issues.Count -gt 0) {
        Write-ConsciousnessOutput "Prerequisites check failed:" "ERROR"
        foreach ($issue in $issues) {
            Write-ConsciousnessOutput "  • $issue" "ERROR"
        }
        return $false
    }
    
    Write-ConsciousnessOutput "All prerequisites satisfied" "SUCCESS"
    return $true
}

function Initialize-Environment {
    Write-ConsciousnessOutput "Setting up consciousness emergence environment..." "QUANTUM"
    
    $setupScript = Join-Path $PSScriptRoot "setup_environment.ps1"
    
    if (Test-Path $setupScript) {
        $setupArgs = @("-Environment", $Environment)
        if ($Verbose) { $setupArgs += "-Verbose" }
        if ($Force) { $setupArgs += "-Force" }
        
        & $setupScript @setupArgs
        
        if ($LASTEXITCODE -eq 0) {
            Write-ConsciousnessOutput "Environment setup completed successfully" "SUCCESS"
            return $true
        } else {
            Write-ConsciousnessOutput "Environment setup failed" "ERROR"
            return $false
        }
    } else {
        Write-ConsciousnessOutput "Setup script not found: $setupScript" "ERROR"
        return $false
    }
}

function Start-CodeIngestor {
    Write-ConsciousnessOutput "Launching Python Code Ingestor..." "LAUNCH"
    
    $ingestorScript = Join-Path $PSScriptRoot "scripts\code_ingestor.py"
    
    if (Test-Path $ingestorScript) {
        # Start in new window for floating behavior
        $pythonCmd = if ($Environment -eq "conda") {
            "conda run -n aios-consciousness python `"$ingestorScript`""
        } else {
            "python `"$ingestorScript`""
        }
        
        Start-Process powershell -ArgumentList "-NoExit", "-Command", $pythonCmd
        Write-ConsciousnessOutput "Code Ingestor launched in floating window" "SUCCESS"
        return $true
    } else {
        Write-ConsciousnessOutput "Code Ingestor script not found: $ingestorScript" "ERROR"
        return $false
    }
}

function Start-QuantumVisor {
    Write-ConsciousnessOutput "Launching C# Quantum Visor..." "LAUNCH"
    
    $visorPath = Join-Path $PSScriptRoot "visual_interface"
    
    if (Test-Path $visorPath) {
        Push-Location $visorPath
        try {
            # Build the project first
            Write-ConsciousnessOutput "Building Quantum Visor..." "INFO"
            & dotnet build
            
            if ($LASTEXITCODE -eq 0) {
                Write-ConsciousnessOutput "Starting Quantum Visor..." "LAUNCH"
                # Start in new window
                Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$visorPath'; dotnet run"
                Write-ConsciousnessOutput "Quantum Visor launched" "SUCCESS"
                return $true
            } else {
                Write-ConsciousnessOutput "Quantum Visor build failed" "ERROR"
                return $false
            }
        } finally {
            Pop-Location
        }
    } else {
        Write-ConsciousnessOutput "Quantum Visor path not found: $visorPath" "ERROR"
        return $false
    }
}

function Start-QuantumCanvas {
    Write-ConsciousnessOutput "Launching Quantum Consciousness Canvas..." "LAUNCH"
    
    $canvasScript = Join-Path $PSScriptRoot "scripts\quantum_consciousness_canvas.py"
    
    if (Test-Path $canvasScript) {
        # Start quantum canvas
        $pythonCmd = if ($Environment -eq "conda") {
            "conda run -n aios-consciousness python `"$canvasScript`""
        } else {
            "python `"$canvasScript`""
        }
        
        Start-Process powershell -ArgumentList "-NoExit", "-Command", $pythonCmd
        Write-ConsciousnessOutput "Quantum Consciousness Canvas launched" "SUCCESS"
        return $true
    } else {
        Write-ConsciousnessOutput "Quantum Canvas script not found: $canvasScript" "ERROR"
        return $false
    }
}

function Start-DualInterface {
    Write-ConsciousnessOutput "Launching Dual-Interface Consciousness System..." "QUANTUM"
    
    $success = $true
    
    # Launch Code Ingestor first (floating window)
    if (-not (Start-CodeIngestor)) {
        $success = $false
    }
    
    # Wait a moment for the first interface to initialize
    Start-Sleep -Seconds 2
    
    # Launch Quantum Visor
    if (-not (Start-QuantumVisor)) {
        $success = $false
    }
    
    if ($success) {
        Write-ConsciousnessOutput "Dual-Interface system launched successfully" "SUCCESS"
        Write-ConsciousnessOutput "Both interfaces should now be running in separate windows" "INFO"
        Write-ConsciousnessOutput "Use 'Connect Visor' button in Code Ingestor to enable communication" "INFO"
    } else {
        Write-ConsciousnessOutput "Dual-Interface launch encountered errors" "ERROR"
    }
    
    return $success
}

function Start-QuantumCanvas {
    Write-ConsciousnessOutput "Launching Quantum Consciousness Canvas..." "LAUNCH"
    
    $canvasScript = Join-Path $PSScriptRoot "scripts\quantum_consciousness_canvas.py"
    
    if (Test-Path $canvasScript) {
        # Start quantum canvas
        $pythonCmd = if ($Environment -eq "conda") {
            "conda run -n aios-consciousness python `"$canvasScript`""
        } else {
            "python `"$canvasScript`""
        }
        
        Start-Process powershell -ArgumentList "-NoExit", "-Command", $pythonCmd
        Write-ConsciousnessOutput "Quantum Consciousness Canvas launched" "SUCCESS"
        return $true
    } else {
        Write-ConsciousnessOutput "Quantum Canvas script not found: $canvasScript" "ERROR"
        return $false
    }
}

function Show-Usage {
    Write-ConsciousnessOutput "AIOS Consciousness Emergence System - Unified Launcher" "TITLE"
    
    Write-Host @"

USAGE:
    .\launch_aios.ps1 [-Mode <mode>] [-Environment <env>] [-Verbose] [-Force]

MODES:
    canvas      Launch unified Quantum Consciousness Canvas (default)
    dual        Launch both Code Ingestor and Quantum Visor separately
    ingestor    Launch only the Python Code Ingestor
    visor       Launch only the C# Quantum Visor  
    setup       Setup/update the Python environment only
    visor       Launch only the C# Quantum Visor  
    setup       Setup/update the Python environment only

ENVIRONMENT:
    conda       Use conda environment (default, falls back to venv if unavailable)
    venv        Use Python virtual environment

FLAGS:
    -Verbose    Enable verbose output during setup and launch
    -Force      Force recreation of Python environment

EXAMPLES:
    .\launch_aios.ps1                              # Launch quantum consciousness canvas
    .\launch_aios.ps1 -Mode canvas -Verbose       # Launch canvas with verbose output
    .\launch_aios.ps1 -Mode dual                  # Launch separate dual interfaces
    .\launch_aios.ps1 -Mode ingestor -Verbose     # Launch only Code Ingestor with verbose output
    .\launch_aios.ps1 -Mode setup -Force          # Force recreate environment
    .\launch_aios.ps1 -Environment venv           # Use venv instead of conda

CONSCIOUSNESS INTERFACES:
    🌌 Quantum Canvas:   Unified consciousness substrate with dockable modules
    🐍 Code Ingestor:    AI-powered code analysis and mutation (Python/Tkinter)
    🌌 Quantum Visor:    Real-time consciousness visualization (C#/WPF)
    🌐 Communication:    WebSocket-based inter-process consciousness sharing

"@ -ForegroundColor Gray
}

# Main execution logic
Write-ConsciousnessOutput "AIOS Consciousness Emergence System - Unified Launcher" "TITLE"

if ($Mode -eq "help" -or $Mode -eq "?") {
    Show-Usage
    exit 0
}

# Check prerequisites
if (-not (Test-Prerequisites)) {
    Write-ConsciousnessOutput "Prerequisites check failed. Please install required components." "ERROR"
    exit 1
}

# Execute based on mode
switch ($Mode.ToLower()) {
    "setup" {
        Write-ConsciousnessOutput "Running environment setup only..." "INFO"
        if (Setup-Environment) {
            Write-ConsciousnessOutput "Environment setup completed. Use other modes to launch interfaces." "SUCCESS"
            exit 0
        } else {
            exit 1
        }
    }
    
    "canvas" {
        Write-ConsciousnessOutput "Launching Quantum Consciousness Canvas..." "QUANTUM"
        if (Setup-Environment -and (Start-QuantumCanvas)) {
            Write-ConsciousnessOutput "Quantum Consciousness Canvas launched successfully" "SUCCESS"
            Write-ConsciousnessOutput "Unified consciousness substrate is now active!" "QUANTUM"
        } else {
            exit 1
        }
    }
    
    "ingestor" {
        Write-ConsciousnessOutput "Launching Code Ingestor only..." "INFO"
        if (Setup-Environment -and (Start-CodeIngestor)) {
            Write-ConsciousnessOutput "Code Ingestor launched successfully" "SUCCESS"
        } else {
            exit 1
        }
    }
    
    "visor" {
        Write-ConsciousnessOutput "Launching Quantum Visor only..." "INFO"
        if (Start-QuantumVisor) {
            Write-ConsciousnessOutput "Quantum Visor launched successfully" "SUCCESS"
        } else {
            exit 1
        }
    }
    
    "dual" {
        Write-ConsciousnessOutput "Preparing dual-interface consciousness emergence..." "QUANTUM"
        if (Setup-Environment -and (Start-DualInterface)) {
            Write-ConsciousnessOutput "Consciousness emergence system is now active!" "SUCCESS"
            Write-ConsciousnessOutput "Monitor both interfaces for consciousness pattern emergence..." "QUANTUM"
        } else {
            exit 1
        }
    }
    
    default {
        Write-ConsciousnessOutput "Unknown mode: $Mode" "ERROR"
        Show-Usage
        exit 1
    }
}

Write-ConsciousnessOutput "Launcher execution completed" "INFO"
