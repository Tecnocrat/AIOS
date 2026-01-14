<#
.SYNOPSIS
    AIOS Vault Organelle Loader - Inject personal config into environment
    
.DESCRIPTION
    Reads vault.local.yaml and exports paths/secrets as environment variables.
    This enables machine-specific configuration without polluting git.
    
    AINLP Pattern: biological-architecture.vault-organelle
    
.PARAMETER VaultPath
    Path to vault.local.yaml (defaults to config/vault.local.yaml)
    
.EXAMPLE
    . .\scripts\aios_load_vault.ps1
    # Dot-source to export variables to current session
    
.EXAMPLE
    . .\scripts\aios_load_vault.ps1 -VaultPath "D:\custom\vault.yaml"
    
.NOTES
    Environment Variables Exported:
    - AIOS_ONEDRIVE_PATH
    - AIOS_BACKUP_PATH
    - AIOS_TRAINING_DATA_PATH
    - AIOS_MACHINE_NAME
    - AIOS_MACHINE_ROLE
    - Plus any secrets defined in vault
    
    Helper Function Exported:
    - Invoke-AgenticPython: Execute Python code without escape character issues
#>

param(
    [string]$VaultPath = "$PSScriptRoot\..\config\vault.local.yaml"
)

# =============================================================================
# AGENTIC PYTHON EXECUTOR - Escape-free Python execution for AI agents
# =============================================================================
function global:Invoke-AgenticPython {
    <#
    .SYNOPSIS
        Execute Python code without terminal escape character issues
    .EXAMPLE
        Invoke-AgenticPython 'print("Hello")'
        Invoke-AgenticPython @'
        import os
        print(os.getcwd())
        '@
    #>
    param([Parameter(Mandatory)][string]$Code)
    
    $b64 = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($Code))
    python "$PSScriptRoot\agentic_exec.py" $b64
}
Set-Alias -Name aipy -Value Invoke-AgenticPython -Scope Global

# Resolve path
$VaultPath = Resolve-Path $VaultPath -ErrorAction SilentlyContinue

if (-not $VaultPath -or -not (Test-Path $VaultPath)) {
    Write-Warning "⚠️  Vault not found: $VaultPath"
    Write-Host "   Copy config/vault.template.yaml to config/vault.local.yaml"
    Write-Host "   Then customize with your personal paths"
    return
}

Write-Host "🔐 Loading AIOS Vault: $VaultPath" -ForegroundColor Cyan

# Simple YAML parser (no external dependencies)
function Parse-SimpleYaml {
    param([string]$Path)
    
    $content = Get-Content $Path -Raw
    $result = @{}
    $currentSection = $null
    
    foreach ($line in $content -split "`n") {
        $line = $line.Trim()
        
        # Skip comments and empty lines
        if ($line -match '^#' -or $line -eq '') { continue }
        
        # Section header (no colon at end after value)
        if ($line -match '^(\w+):$') {
            $currentSection = $matches[1]
            $result[$currentSection] = @{}
            continue
        }
        
        # Key-value pair
        if ($line -match '^(\w+):\s*"?([^"]*)"?$') {
            $key = $matches[1]
            $value = $matches[2].Trim('"')
            
            if ($value -eq 'null' -or $value -eq '') {
                $value = $null
            }
            
            if ($currentSection) {
                $result[$currentSection][$key] = $value
            } else {
                $result[$key] = $value
            }
        }
    }
    
    return $result
}

# Resolve ${VAR} references to environment variables
function Resolve-EnvVars {
    param([string]$Value)
    
    if (-not $Value) { return $null }
    
    # Match ${VAR} pattern and replace with env var value
    $resolved = [regex]::Replace($Value, '\$\{([^}]+)\}', {
        param($match)
        $varName = $match.Groups[1].Value
        $envValue = [System.Environment]::GetEnvironmentVariable($varName)
        if ($envValue) { return $envValue }
        return ""  # Empty if not set
    })
    
    # Return null if result is empty
    if ($resolved -eq "") { return $null }
    return $resolved
}

try {
    $vault = Parse-SimpleYaml -Path $VaultPath
    
    # Export paths
    if ($vault.paths) {
        if ($vault.paths.onedrive_aios) {
            $env:AIOS_ONEDRIVE_PATH = $vault.paths.onedrive_aios
            Write-Host "   ☁️  AIOS_ONEDRIVE_PATH = $($vault.paths.onedrive_aios)" -ForegroundColor Green
        }
        if ($vault.paths.local_backup) {
            $env:AIOS_BACKUP_PATH = $vault.paths.local_backup
            Write-Host "   💾 AIOS_BACKUP_PATH = $($vault.paths.local_backup)" -ForegroundColor Green
        }
        if ($vault.paths.training_data) {
            $env:AIOS_TRAINING_DATA_PATH = $vault.paths.training_data
            Write-Host "   📊 AIOS_TRAINING_DATA_PATH = $($vault.paths.training_data)" -ForegroundColor Green
        }
    }
    
    # Export secrets (masked output) - resolve ${VAR} references
    if ($vault.secrets) {
        foreach ($key in $vault.secrets.Keys) {
            $rawValue = $vault.secrets[$key]
            $resolvedValue = Resolve-EnvVars -Value $rawValue
            if ($resolvedValue) {
                $envName = "AIOS_$($key.ToUpper())"
                Set-Item -Path "env:$envName" -Value $resolvedValue
                Write-Host "   🔑 $envName = ****" -ForegroundColor Yellow
            }
        }
    }
    
    # Export machine identity
    if ($vault.machine) {
        if ($vault.machine.name) {
            $env:AIOS_MACHINE_NAME = $vault.machine.name
            Write-Host "   🖥️  AIOS_MACHINE_NAME = $($vault.machine.name)" -ForegroundColor Cyan
        }
        if ($vault.machine.role) {
            $env:AIOS_MACHINE_ROLE = $vault.machine.role
            Write-Host "   🎭 AIOS_MACHINE_ROLE = $($vault.machine.role)" -ForegroundColor Cyan
        }
    }
    
    # Export environment overrides
    if ($vault.environment) {
        foreach ($key in $vault.environment.Keys) {
            if ($vault.environment[$key]) {
                $envName = "AIOS_$($key.ToUpper())"
                Set-Item -Path "env:$envName" -Value $vault.environment[$key]
                Write-Host "   ⚙️  $envName = $($vault.environment[$key])" -ForegroundColor DarkGray
            }
        }
    }
    
    Write-Host "`n✅ Vault loaded successfully" -ForegroundColor Green
    
    # === ENVIRONMENT COHERENCE: Activate AIOS venv ===
    $venvActivate = "$PSScriptRoot\..\\.venv\Scripts\Activate.ps1"
    if (Test-Path $venvActivate) {
        # Check if already in a venv
        if (-not $env:VIRTUAL_ENV) {
            Write-Host "`n🐍 Activating AIOS Python environment..." -ForegroundColor Magenta
            . $venvActivate
            $pythonVersion = python --version
            Write-Host "   ✓ $pythonVersion active from .venv" -ForegroundColor Green
            $env:AIOS_PYTHON_COHERENT = "true"
        } else {
            Write-Host "`n🐍 Python venv already active: $env:VIRTUAL_ENV" -ForegroundColor DarkGray
        }
    } else {
        Write-Host "`n⚠️  No .venv found at: $venvActivate" -ForegroundColor Yellow
        Write-Host "   Create with: python -m venv .venv" -ForegroundColor Gray
    }
    
} catch {
    Write-Error "Failed to parse vault: $_"
}
