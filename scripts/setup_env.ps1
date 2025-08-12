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
  - Structured JSON report (environment_report.json)
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

function Setup-CondaEnvironment {
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

function Setup-VenvEnvironment {
    $venvPath = Join-Path $ProjectRoot 'venv'
    Write-AIOSLog "[Venv] Path: $venvPath" 'INFO'
    if ($Force -and (Test-Path $venvPath)) { Write-AIOSLog '[Venv] Force removal of existing venv' 'WARN'; Remove-Item -Recurse -Force $venvPath }
    if (-not (Test-Path $venvPath)) { Write-AIOSLog '[Venv] Creating virtual environment' 'INFO'; & python -m venv $venvPath; if ($LASTEXITCODE -ne 0) { throw 'Venv creation failed' } } else { Write-AIOSLog '[Venv] Existing venv reused' 'INFO' }
    & (Join-Path $venvPath 'Scripts/Activate.ps1')
    Write-AIOSLog '[Venv] Activated' 'INFO'
}

function Install-PipRequirements {
    $req = Join-Path $ProjectRoot 'ai/requirements.txt'
    Write-AIOSLog 'Upgrading pip' 'INFO'; & python -m pip install --upgrade pip | Out-Null
    if (Test-Path $req) { Write-AIOSLog "Installing requirements: $req" 'INFO'; & pip install -r $req --upgrade } else { Write-AIOSLog 'requirements.txt missing (ai/requirements.txt)' 'WARN' }
}

function Generate-EnvironmentReport {
    Write-AIOSLog 'Generating environment report' 'INFO'
    $reqHash = Get-FileHashOrNull (Join-Path $ProjectRoot 'ai/requirements.txt')
    $report = [ordered]@{
        timestamp = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
        environment_type = $Environment
        project_root = $ProjectRoot
        env_name = $EnvName
        requirements_hash = $reqHash
        python_version = (& python --version 2>$null)
        pip_packages = try { & pip list --format=json | ConvertFrom-Json } catch { @() }
        system = [ordered]@{ os = [System.Environment]::OSVersion.ToString(); machine = [System.Environment]::MachineName; user = [System.Environment]::UserName; processors = [System.Environment]::ProcessorCount }
        aios = [ordered]@{ setup_method = 'scripts/setup_env.ps1'; consciousness_stage = 'bootstrap'; report_only = [bool]$ReportOnly; force = [bool]$Force }
    }
    $reportPath = Join-Path $ProjectRoot 'environment_report.json'
    $report | ConvertTo-Json -Depth 6 | Out-File -FilePath $reportPath -Encoding UTF8
    Write-AIOSLog "Report saved: $reportPath" 'INFO'
}

function Test-CoreImports {
    if ($SkipImportTest) { Write-AIOSLog 'Skipping import tests per flag' 'WARN'; return }
    Write-AIOSLog 'Validating core imports' 'INFO'
    & python - <<'PY'
import importlib, sys
mods = ['torch','numpy','pandas','transformers']
missing = []
for m in mods:
    try: importlib.import_module(m)
    except Exception as e: missing.append((m,str(e)))
if missing:
    print('Missing/failed imports:', missing)
    sys.exit(2)
print('✅ Core AI dependencies loaded successfully')
PY
    $status = $LASTEXITCODE
    if ($status -eq 2) { Write-AIOSLog 'Core import validation: DRIFT (some packages missing)' 'WARN'; return 2 }
    if ($status -ne 0) { throw 'Import validation error' }
    Write-AIOSLog 'Core imports OK' 'INFO'
    return 0
}

try {
    Write-AIOSLog "Mode: $(if($ReportOnly){'REPORT-ONLY'}else{'APPLY'})" 'INFO'
    if (-not $ReportOnly) {
        if ($Environment -eq 'conda') { if (Test-CondaInstall) { Setup-CondaEnvironment } else { Write-AIOSLog 'Conda not found; falling back to venv' 'WARN'; $Environment = 'venv'; Setup-VenvEnvironment } } else { Setup-VenvEnvironment }
        Install-PipRequirements
    } else { Write-AIOSLog 'Report-only mode: no environment changes will be made' 'INFO' }
    Generate-EnvironmentReport
    $importResult = Test-CoreImports
    if ($importResult -eq 2) { exit 2 }
    Write-AIOSLog '🎉 Environment bootstrap complete' 'INFO'
    exit 0
}
catch {
    Write-AIOSLog "Setup failed: $($_.Exception.Message)" 'ERROR'
    exit 3
}
