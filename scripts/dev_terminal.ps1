<#
 AIOS Development Terminal (Harmonized)
 Relocated from repository root (terminal.ps1 -> scripts/dev_terminal.ps1)
 AINLP Harmonization Enhancements:
  - Path hygiene: removed root-level script
  - Non-interactive mode via -Action parameter (canvas|visor|orchestrator|all|env|workspace|menu)
  - Environment bootstrap delegation to scripts/setup_env.ps1
  - Core path corrected (uses 'core')
  - Structured exit codes: 0 success; 2 partial (warnings); 3 error
  - LFC/GPC coherence metrics (root sentinel removed)
  - Root hygiene governed by ROOT_HYGIENE_POLICY.md
#>
param(
  [ValidateSet('menu','canvas','visor','orchestrator','all','env','workspace')]
  [string]$Action = 'menu',
  [ValidateSet('check','bootstrap','skip')]
  [string]$Environment = 'check',
  [switch]$Quiet,
  [switch]$ReportCoherence,
  [string]$CoherenceFormat = 'text',  # text|json
  [switch]$FinalizeHygiene
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$Root = Split-Path -Parent $MyInvocation.MyCommand.Definition | Split-Path -Parent
$CorePath = Join-Path $Root 'core'
$ScriptsPath = Join-Path $Root 'scripts'
$WorkspaceFile = Join-Path $Root 'AIOS.code-workspace'
$EnvScript = Join-Path $ScriptsPath 'setup_env.ps1'

function Write-Log {
  param([string]$Msg,[string]$Level='INFO')
  if ($Quiet -and $Level -notin @('ERROR')) { return }
  $color = switch ($Level){ 'INFO'{'Green'} 'WARN'{'Yellow'} 'ERROR'{'Red'} 'LFC'{'Cyan'} 'GPC'{'Magenta'} default{'White'} }
  Write-Host "[$Level] $Msg" -ForegroundColor $color
}

function Invoke-EnvironmentCheck {
  if ($Environment -eq 'skip'){ return 0 }
  Write-Log 'Environment check starting' 'INFO'
  $warn = 0
  try { python --version | Out-Null } catch { Write-Log 'Python not found' 'WARN'; $warn++ }
  try { conda --version | Out-Null } catch { Write-Log 'Conda not found (OK if using venv)' 'WARN' }
  if (-not (Test-Path $WorkspaceFile)) { Write-Log 'Workspace file missing' 'WARN'; $warn++ }
  if (-not (Test-Path $CorePath)) { Write-Log "Core path missing: $CorePath" 'WARN'; $warn++ }
  if ($Environment -eq 'bootstrap' -and (Test-Path $EnvScript)) {
    Write-Log 'Bootstrapping environment (setup_env.ps1)' 'INFO'
    pwsh -File $EnvScript | Out-Null
  }
  return $warn
}

function Invoke-Canvas { Write-Log 'Launching Quantum Consciousness Canvas' 'INFO'; python (Join-Path $ScriptsPath 'quantum_consciousness_canvas.py') }
function Invoke-Visor { Write-Log 'Launching Visual Interface (open manually if needed)' 'INFO' }
function Invoke-Orchestrator {
  if (-not (Test-Path (Join-Path $CorePath 'build'))) {
    Write-Log 'Configuring C++ core (cmake configure)' 'INFO'
    cmake -B (Join-Path $CorePath 'build') -S $CorePath -DCMAKE_BUILD_TYPE=Debug | Out-Null
  }
  Write-Log 'Building C++ core' 'INFO'
  cmake --build (Join-Path $CorePath 'build') --config Debug
}
function Invoke-All { Invoke-Canvas; Invoke-Orchestrator; Invoke-Visor }
function Invoke-Workspace { if (Test-Path $WorkspaceFile) { code $WorkspaceFile } else { Write-Log 'Workspace file not found' 'ERROR' } }
function Invoke-EnvSetup { if (Test-Path $EnvScript) { pwsh -File $EnvScript } else { Write-Log 'Environment script missing' 'ERROR' } }

# --- Coherence Metrics (LFC/GPC) ---
function Get-CoherenceMetrics {
  # Deprecated root files (must not exist)
  $GovDir = Join-Path $Root 'governance'
  if (Test-Path (Join-Path $GovDir 'deprecated_files.ps1')) { . (Join-Path $GovDir 'deprecated_files.ps1'); $deprecated = $Global:AIOS_DeprecatedRootFiles } else { $deprecated = @('test_opencv_aios_integration.py','test_chatgpt_integration.py','setup_environment.ps1','terminal.ps1') }
  # Expose for callers needing the full set (e.g., finalize hygiene purge)
  $script:DeprecatedList = $deprecated
  $present = @()
  foreach($d in $deprecated){ if (Test-Path (Join-Path $Root $d)) { $present += $d } }
  $deprecatedScore = if($deprecated.Count -eq 0){1}else{ 1 - ($present.Count / $deprecated.Count) }
  # Resurrection penalty: if any deprecated present, subtract adaptive penalty scaled by count
  $resurrectionPenalty = if($present.Count -gt 0){ [math]::Min(0.3, 0.1 * $present.Count) } else { 0 }

  # Governance layer checks
  $guardOk = Test-Path (Join-Path $ScriptsPath 'root_clutter_guard.ps1')
  $ciOk = Test-Path (Join-Path $Root '.github/workflows/root-clutter-guard.yml')
  $hookOk = Test-Path (Join-Path $Root '.githooks/pre-commit')
  # Inventory filter: folder_structure.json should not list deprecated filenames
  $inventoryFile = Join-Path $Root 'docs/AIOS/folder_structure.json'
  $inventoryOk = $true
  if (Test-Path $inventoryFile){
    $invText = Get-Content -Raw $inventoryFile
    foreach($d in $deprecated){ if ($invText -match [regex]::Escape($d)) { $inventoryOk = $false; break } }
  }
  $govTotal = 4
  $govPass = @($guardOk,$ciOk,$hookOk,$inventoryOk) | Where-Object { $_ } | Measure-Object | Select-Object -ExpandProperty Count
  $governanceFailures = @()
  if (-not $guardOk) { $governanceFailures += 'guard_script_missing' }
  if (-not $ciOk) { $governanceFailures += 'ci_workflow_missing' }
  if (-not $hookOk) { $governanceFailures += 'pre_commit_hook_missing' }
  if (-not $inventoryOk) { $governanceFailures += 'inventory_filter_failure' }
  $gpc = if($govTotal -eq 0){1}else{ $govPass / $govTotal }

  # Local File Coherence (LFC) blends deprecated absence + workspace presence
  $workspaceExists = Test-Path $WorkspaceFile
  # Mutation distance placeholder (future): currently neutral = 1.0 (would integrate structural diff signal)
  $mutationDistance = 1.0
  $lfcRaw = (($deprecatedScore - $resurrectionPenalty) * 0.6) + (($workspaceExists)?0.25:0) + ($mutationDistance * 0.15)
  if ($lfcRaw -lt 0) { $lfcRaw = 0 }
  $lfc = [math]::Round($lfcRaw,4)
  $gpc = [math]::Round($gpc,4)
  return [pscustomobject]@{ LFC=$lfc; GPC=$gpc; DeprecatedPresent=$present; GovernancePass=$govPass; GovernanceTotal=$govTotal; GovernanceFailures=$governanceFailures; ResurrectionPenalty=$resurrectionPenalty; MutationDistance=$mutationDistance }
}

function Invoke-CoherenceReport {
  $m = Get-CoherenceMetrics
  if ($CoherenceFormat -eq 'json') {
    # Do not emit here; caller decides when to output JSON to avoid duplication
  } else {
    Write-Log ("LFC: " + $m.LFC) 'LFC'
    Write-Log ("GPC: " + $m.GPC) 'GPC'
    if ($m.ResurrectionPenalty -gt 0) { Write-Log ("Resurrection penalty applied: " + $m.ResurrectionPenalty) 'WARN' }
    if ($m.DeprecatedPresent.Count -gt 0){ Write-Log ('Deprecated present: ' + ($m.DeprecatedPresent -join ', ')) 'WARN' }
  }
  return $m
}

function Show-Menu {
  Write-Host "`n🧠 AIOS Dev Terminal" -ForegroundColor Cyan
  Write-Host '1. Canvas (Python)'
  Write-Host '2. Visual Interface (C#)'
  Write-Host '3. Core Build (C++)'
  Write-Host '4. All'
  Write-Host '5. Environment Bootstrap'
  Write-Host '6. Open Workspace'
  $c = Read-Host 'Select (1-6)'
  switch ($c) {
  '1' { Invoke-Canvas }
  '2' { Invoke-Visor }
  '3' { Invoke-Orchestrator }
  '4' { Invoke-All }
  '5' { Invoke-EnvSetup }
  '6' { Invoke-Workspace }
    default { Write-Log 'Invalid selection' 'ERROR' }
  }
}

$metrics = Invoke-CoherenceReport

$warns = Invoke-EnvironmentCheck

try {
  switch ($Action) {
    'menu' { Show-Menu }
  'canvas' { Invoke-Canvas }
  'visor' { Invoke-Visor }
  'orchestrator' { Invoke-Orchestrator }
  'all' { Invoke-All }
  'env' { Invoke-EnvSetup }
  'workspace' { Invoke-Workspace }
  }
  if ($FinalizeHygiene) {
    # Purge deprecated sentinel files (terminal.ps1 etc.) after metrics initially collected
  if (-not $script:DeprecatedList) { $null = Get-CoherenceMetrics } # ensure population
  foreach($f in $script:DeprecatedList){
      $p = Join-Path $Root $f
      if (Test-Path $p) {
        try { Remove-Item $p -Force -ErrorAction Stop }
        catch { Write-Log ("Failed to remove deprecated file ${f}: $($_.Exception.Message)") 'WARN' }
      }
    }
    # Recompute metrics post-purge
    $metrics = Invoke-CoherenceReport
  }
  if ($ReportCoherence -and $CoherenceFormat -eq 'json') { $metrics | ConvertTo-Json -Depth 4 | Write-Output }
  if ($warns -gt 0 -or $metrics.DeprecatedPresent.Count -gt 0) { exit 2 } else { exit 0 }
}
catch {
  Write-Log "Terminal error: $($_.Exception.Message)" 'ERROR'
  exit 3
}

if (-not $Quiet) {
  Write-Host "`nExamples:" -ForegroundColor Cyan
  Write-Host ' pwsh -File scripts/dev_terminal.ps1 -Action menu'
  Write-Host ' pwsh -File scripts/dev_terminal.ps1 -Action all -Environment bootstrap'
  Write-Host ' pwsh -File scripts/dev_terminal.ps1 -Action orchestrator -Quiet'
}
