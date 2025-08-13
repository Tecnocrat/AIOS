<#
 AIOS Environment Bootstrap (Enhanced)
 Relocated from repository root to scripts/ per Agentic File Creation Policy.
 Features:
  - Conda or venv creation (-Environment conda|venv)
  - Force recreation (-Force)
  - Report-only audit without changes (-ReportOnly)
  - Integrity hash of requirements to detect drift
  - Optional lightweight import test (-SkipImportTest)
  - Idempotent re-entry (no duplicate creation)
    - Structured JSON report archived under docs/unified_backups/tachyonic_operations/environment_state
        * Timestamped: environment_report_yyyyMMdd_HHmmss.json
        * Rolling pointer: environment_report_latest.json
        * Legacy root environment_report.json removed automatically
  - Exit codes: 0 success, 2 drift detected, 3 setup error
#>
param(
    [ValidateSet('conda','venv')][string]$Environment = 'conda',
    [switch]$Force,
    [switch]$Verbose,
    [switch]$ReportOnly,
    [switch]$SkipImportTest
)

$ErrorActionPreference = 'Stop'

Write-Host "🧠 AIOS Environment Bootstrap" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$ProjectRoot = Split-Path -Parent $ScriptDir
$EnvName = 'aios-consciousness'
$PythonVersion = '3.12'
$LogFile = Join-Path $ProjectRoot 'setup.log'

function Write-AIOSLog {
    param([string]$Message,[ValidateSet('INFO','WARN','ERROR','DEBUG')]$Level='INFO')
    $timestamp = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
    $color = switch ($Level) { 'INFO'{'Green'} 'WARN'{'Yellow'} 'ERROR'{'Red'} 'DEBUG'{'Cyan'} default{'White'} }
    Write-Host "[$timestamp] [$Level] $Message" -ForegroundColor $color
    "$timestamp [$Level] $Message" | Out-File -Append -FilePath $LogFile -Encoding UTF8
}

function Get-FileHashOrNull { param([string]$Path) if (Test-Path $Path) { (Get-FileHash -Algorithm SHA256 -Path $Path).Hash } else { $null } }
function Test-CondaInstall { try { & conda info --json 2>$null | Out-Null; return $true } catch { return $false } }

# Backward compatibility aliases (legacy function names)
Set-Alias -Name Setup-CondaEnvironment -Value Initialize-CondaEnvironment -ErrorAction SilentlyContinue
Set-Alias -Name Setup-VenvEnvironment -Value Initialize-VenvEnvironment -ErrorAction SilentlyContinue
Set-Alias -Name Generate-EnvironmentReport -Value Get-EnvironmentReport -ErrorAction SilentlyContinue

function Initialize-CondaEnvironment {
    Write-AIOSLog "[Conda] Target env: $EnvName" 'INFO'
    if ($Force) { Write-AIOSLog '[Conda] Force removal of existing env (if any)' 'WARN'; & conda env remove -n $EnvName -y 2>$null }
    $exists = & conda env list | Select-String -SimpleMatch " $EnvName "
    if (-not $exists) {
        Write-AIOSLog '[Conda] Creating environment (environment.yml or fallback)' 'INFO'
        $envYml = Join-Path $ProjectRoot 'environment.yml'
        if (Test-Path $envYml) { & conda env create -f $envYml } else { & conda create -n $EnvName python=$PythonVersion -y }
        if ($LASTEXITCODE -ne 0) { throw 'Conda environment creation failed' }
    } else { Write-AIOSLog '[Conda] Environment already exists (reuse)' 'INFO' }
    & conda activate $EnvName
    Write-AIOSLog '[Conda] Environment activated' 'INFO'
}

function Initialize-VenvEnvironment {
    $venvPath = Join-Path $ProjectRoot 'venv'
    Write-AIOSLog "[Venv] Path: $venvPath" 'INFO'
    if ($Force -and (Test-Path $venvPath)) { Write-AIOSLog '[Venv] Force removal of existing venv' 'WARN'; Remove-Item -Recurse -Force $venvPath }
    if (-not (Test-Path $venvPath)) { Write-AIOSLog '[Venv] Creating virtual environment' 'INFO'; & python -m venv $venvPath; if ($LASTEXITCODE -ne 0) { throw 'Venv creation failed' } } else { Write-AIOSLog '[Venv] Existing venv reused' 'INFO' }
    & (Join-Path $venvPath 'Scripts/Activate.ps1')
    Write-AIOSLog '[Venv] Activated' 'INFO'
}

function Install-PipRequirements {  # Verb Install is approved
    $req = Join-Path $ProjectRoot 'ai/requirements.txt'
    Write-AIOSLog 'Upgrading pip' 'INFO'; & python -m pip install --upgrade pip | Out-Null
    if (Test-Path $req) { Write-AIOSLog "Installing requirements: $req" 'INFO'; & pip install -r $req --upgrade } else { Write-AIOSLog 'requirements.txt missing (ai/requirements.txt)' 'WARN' }
}

function Get-EnvironmentReport {  # Verb Get is approved; still performs generation side-effect
    Write-AIOSLog 'Generating environment report (tachyonic archival mode)' 'INFO'
    $reqHash = Get-FileHashOrNull (Join-Path $ProjectRoot 'ai/requirements.txt')
    $pipPackages = @()
    try { $pipPackages = & pip list --format=json | ConvertFrom-Json } catch { Write-AIOSLog 'pip list retrieval failed (continuing with empty list)' 'WARN' }
    $report = [ordered]@{
        timestamp         = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
        environment_type  = $Environment
        project_root      = $ProjectRoot
        env_name          = $EnvName
        requirements_hash = $reqHash
        python_version    = (& python --version 2>$null)
        pip_packages      = $pipPackages
        system            = [ordered]@{
            os          = [System.Environment]::OSVersion.ToString()
            machine     = [System.Environment]::MachineName
            user        = [System.Environment]::UserName
            processors  = [System.Environment]::ProcessorCount
        }
        aios              = [ordered]@{
            setup_method        = 'scripts/setup_env.ps1'
            consciousness_stage = 'bootstrap'
            report_only         = [bool]$ReportOnly
            force               = [bool]$Force
        }
    }
    # Tachyonic archival destination (harmonized): docs/unified_backups/tachyonic_operations/environment_state
    $tachyonicBase = Join-Path $ProjectRoot 'docs/unified_backups/tachyonic_operations/environment_state'
    if (-not (Test-Path $tachyonicBase)) { New-Item -ItemType Directory -Path $tachyonicBase -Force | Out-Null }
    $tsCompact = Get-Date -Format 'yyyyMMdd_HHmmss'
    $archivedReportPath = Join-Path $tachyonicBase ("environment_report_" + $tsCompact + '.json')
    $latestLinkPath = Join-Path $tachyonicBase 'environment_report_latest.json'
    $json = $report | ConvertTo-Json -Depth 6
    $json | Out-File -FilePath $archivedReportPath -Encoding UTF8
    # Maintain/update latest pointer copy
    $json | Out-File -FilePath $latestLinkPath -Encoding UTF8
    Write-AIOSLog "Report archived: $archivedReportPath" 'INFO'
    Write-AIOSLog "Latest pointer updated: $latestLinkPath" 'INFO'
    # Remove legacy root report if present to avoid drift
    $legacy = Join-Path $ProjectRoot 'environment_report.json'
    if (Test-Path $legacy) { try { Remove-Item $legacy -Force } catch { Write-AIOSLog "Legacy root report cleanup failed: $($_.Exception.Message)" 'WARN' } }
}

function Test-CoreImports {  # Test is approved
    if ($SkipImportTest) { Write-AIOSLog 'Skipping import tests per flag' 'WARN'; return }
    Write-AIOSLog 'Validating core imports' 'INFO'
    $tmpPy = New-TemporaryFile
@'
import importlib, sys
mods = ['torch','numpy','pandas','transformers']
missing = []
for m in mods:
    try:
        importlib.import_module(m)
    except Exception as e:
        missing.append((m,str(e)))
if missing:
    print('Missing/failed imports:', missing)
    sys.exit(2)
print('Core AI dependencies loaded successfully')
'@ | Out-File -FilePath $tmpPy -Encoding UTF8
    & python $tmpPy
    Remove-Item $tmpPy -Force -ErrorAction SilentlyContinue
    $status = $LASTEXITCODE
    if ($status -eq 2) { Write-AIOSLog 'Core import validation: DRIFT (some packages missing)' 'WARN'; return 2 }
    if ($status -ne 0) { throw 'Import validation error' }
    Write-AIOSLog 'Core imports OK' 'INFO'
    return 0
}

try {
    Write-AIOSLog "Mode: $(if($ReportOnly){'REPORT-ONLY'}else{'APPLY'})" 'INFO'
    if (-not $ReportOnly) {
        if ($Environment -eq 'conda') { if (Test-CondaInstall) { Initialize-CondaEnvironment } else { Write-AIOSLog 'Conda not found; falling back to venv' 'WARN'; $Environment = 'venv'; Initialize-VenvEnvironment } } else { Initialize-VenvEnvironment }
        Install-PipRequirements
    } else { Write-AIOSLog 'Report-only mode: no environment changes will be made' 'INFO' }
    Get-EnvironmentReport
    $importResult = Test-CoreImports
    if ($importResult -eq 2) { exit 2 }
    Write-AIOSLog '🎉 Environment bootstrap complete' 'INFO'
    exit 0
}
catch {
    Write-AIOSLog "Setup failed: $($_.Exception.Message)" 'ERROR'
    exit 3
}
