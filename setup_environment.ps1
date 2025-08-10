# AIOS Consciousness Emergence System - Environment Setup
# Advanced PowerShell script for optimal conda/venv environment configuration
# Ensures robust, fractal context retention and meta-analytics

param(
    [string]$Environment = "conda",  # "conda" or "venv"
    [switch]$Force,                  # Force recreate environment
    [switch]$Verbose                 # Verbose output
)

Write-Host "🧠 AIOS Consciousness Emergence Environment Setup" -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Definition
$EnvName = "aios-consciousness"
$PythonVersion = "3.12"

# Function for enhanced logging
function Write-AIOSLog {
    param([string]$Message, [string]$Level = "INFO")
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $color = switch ($Level) {
        "INFO" { "Green" }
        "WARN" { "Yellow" } 
        "ERROR" { "Red" }
        "DEBUG" { "Cyan" }
        default { "White" }
    }
    Write-Host "[$timestamp] [$Level] $Message" -ForegroundColor $color
    
    # Log to file for recursive ingestion
    "$timestamp [$Level] $Message" | Out-File -Append -FilePath "$ProjectRoot\setup.log"
}

# Detect conda installation
function Test-CondaInstall {
    try {
        $condaInfo = & conda info --json 2>$null | ConvertFrom-Json
        return $true
    }
    catch {
        return $false
    }
}

# Setup conda environment
function Setup-CondaEnvironment {
    Write-AIOSLog "Setting up conda environment: $EnvName" "INFO"
    
    if ($Force) {
        Write-AIOSLog "Force flag detected - removing existing environment" "WARN"
        & conda env remove -n $EnvName -y 2>$null
    }
    
    # Check if environment exists
    $envExists = & conda env list | Select-String $EnvName
    
    if ($envExists -and -not $Force) {
        Write-AIOSLog "Environment '$EnvName' already exists. Use -Force to recreate." "WARN"
        Write-AIOSLog "Activating existing environment..." "INFO"
        & conda activate $EnvName
    }
    else {
        Write-AIOSLog "Creating new conda environment from environment.yml" "INFO"
        & conda env create -f "$ProjectRoot\environment.yml"
        
        if ($LASTEXITCODE -eq 0) {
            Write-AIOSLog "Conda environment created successfully" "INFO"
        }
        else {
            Write-AIOSLog "Failed to create conda environment" "ERROR"
            exit 1
        }
    }
    
    # Activate environment and install additional packages
    Write-AIOSLog "Activating conda environment..." "INFO"
    & conda activate $EnvName
    
    # Install additional pip packages that might not be in conda
    Write-AIOSLog "Installing additional packages via pip..." "INFO"
    & pip install --upgrade pip
    $aiReq = Join-Path $ProjectRoot "ai\requirements.txt"
    if (Test-Path $aiReq) {
        & pip install -r $aiReq --upgrade
    } else {
        Write-AIOSLog "ai/requirements.txt not found; skipping pip install" "WARN"
    }
    
    Write-AIOSLog "Conda environment setup complete!" "INFO"
}

# Setup virtual environment
function Setup-VenvEnvironment {
    Write-AIOSLog "Setting up Python virtual environment: $EnvName" "INFO"
    
    $venvPath = "$ProjectRoot\venv"
    
    if ($Force -and (Test-Path $venvPath)) {
        Write-AIOSLog "Force flag detected - removing existing venv" "WARN"
        Remove-Item -Recurse -Force $venvPath
    }
    
    if (-not (Test-Path $venvPath)) {
        Write-AIOSLog "Creating new virtual environment..." "INFO"
        & python -m venv $venvPath
        
        if ($LASTEXITCODE -eq 0) {
            Write-AIOSLog "Virtual environment created successfully" "INFO"
        }
        else {
            Write-AIOSLog "Failed to create virtual environment" "ERROR"
            exit 1
        }
    }
    
    # Activate virtual environment
    Write-AIOSLog "Activating virtual environment..." "INFO"
    & "$venvPath\Scripts\Activate.ps1"
    
    # Install packages
    Write-AIOSLog "Installing packages from requirements.txt..." "INFO"
    & pip install --upgrade pip
    $aiReq = Join-Path $ProjectRoot "ai\requirements.txt"
    if (Test-Path $aiReq) {
        & pip install -r $aiReq
    } else {
        Write-AIOSLog "ai/requirements.txt not found; skipping pip install" "WARN"
    }
    
    Write-AIOSLog "Virtual environment setup complete!" "INFO"
}

# Generate environment report for meta-analytics
function Generate-EnvironmentReport {
    Write-AIOSLog "Generating environment analytics report..." "INFO"
    
    $report = @{
        timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        environment_type = $Environment
        python_version = & python --version
        pip_packages = & pip list --format=json | ConvertFrom-Json
        system_info = @{
            os = [System.Environment]::OSVersion.ToString()
            machine = [System.Environment]::MachineName
            user = [System.Environment]::UserName
            processors = [System.Environment]::ProcessorCount
        }
        aios_metadata = @{
            project_root = $ProjectRoot
            setup_method = "PowerShell Automation"
            consciousness_level = "Environment Bootstrap"
            recursive_ingestion = $true
        }
    }
    
    $reportPath = "$ProjectRoot\environment_report.json"
    $report | ConvertTo-Json -Depth 4 | Out-File -FilePath $reportPath -Encoding UTF8
    
    Write-AIOSLog "Environment report saved to: $reportPath" "INFO"
}

# Main execution flow
try {
    Write-AIOSLog "Starting AIOS environment setup..." "INFO"
    Write-AIOSLog "Project root: $ProjectRoot" "DEBUG"
    Write-AIOSLog "Target environment: $Environment" "DEBUG"
    
    if ($Environment -eq "conda") {
        if (Test-CondaInstall) {
            Setup-CondaEnvironment
        }
        else {
            Write-AIOSLog "Conda not found. Falling back to virtual environment." "WARN"
            $Environment = "venv"
            Setup-VenvEnvironment
        }
    }
    elseif ($Environment -eq "venv") {
        Setup-VenvEnvironment
    }
    else {
        Write-AIOSLog "Invalid environment type: $Environment. Use 'conda' or 'venv'." "ERROR"
        exit 1
    }
    
    # Generate analytics
    Generate-EnvironmentReport
    
    Write-AIOSLog "🎉 AIOS environment setup completed successfully!" "INFO"
    Write-AIOSLog "Environment is ready for consciousness emergence..." "INFO"
    
    # Test basic imports
    Write-AIOSLog "Testing core dependencies..." "INFO"
    & python -c "import torch, numpy, pandas, transformers; print('✅ Core AI dependencies loaded successfully')"
    & python -c "import tkinter; print('✅ GUI dependencies loaded successfully')" 2>$null
    
}
catch {
    Write-AIOSLog "Setup failed: $($_.Exception.Message)" "ERROR"
    exit 1
}
