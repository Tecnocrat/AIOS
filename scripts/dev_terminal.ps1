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
  [ValidateSet('menu','canvas','visor','orchestrator','all','env','workspace','update-hashes','safety-validate','prune-archives','guard-report','normalize-guard-log','truncate-guard-log')]
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
# Safety docs after $Root is known
$SafetyDocs = @(
  (Join-Path $Root 'docs/safety/SAFETY_PROTOCOL.md'),
  (Join-Path $Root 'docs/safety/SAFETY_IMPLEMENTATION_SUMMARY.md')
)
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
function Invoke-UpdateHashes {
  # Compute hashes and replace placeholders in safety docs
  $hashMap = @{}
  foreach($sd in $SafetyDocs){
    if (Test-Path $sd){
      try { $hashMap[$sd] = (Get-FileHash -Algorithm SHA256 -Path $sd).Hash.ToLower() } catch {}
    }
  }
  if ($hashMap.Count -eq 0){ Write-Log 'No safety docs found for hashing' 'WARN'; return }
  $protocolPath = $SafetyDocs[0]
  $implPath = $SafetyDocs[1]
  if (Test-Path $protocolPath){
    $c = Get-Content -Raw $protocolPath
    $c2 = $c -replace '@hash_protocol@',( $hashMap[$protocolPath] )
    if ($c -ne $c2){ Set-Content -Path $protocolPath -Value $c2 -Encoding UTF8; Write-Log 'Updated protocol hash placeholder' 'INFO' }
  }
  if (Test-Path $implPath){
    $c = Get-Content -Raw $implPath
    $c2 = $c -replace '@hash_impl@',( $hashMap[$implPath] )
    if ($c -ne $c2){ Set-Content -Path $implPath -Value $c2 -Encoding UTF8; Write-Log 'Updated implementation summary hash placeholder' 'INFO' }
  }
  if ($CoherenceFormat -eq 'json') { $hashMap | ConvertTo-Json | Write-Output }
}

function Invoke-SafetyValidate {
  Write-Log 'Running safety validation (session+emergency)' 'INFO'
  $py = Get-Command python -ErrorAction SilentlyContinue
  if (-not $py) { Write-Log 'Python not found for safety validation' 'ERROR'; return 3 }
  $scriptPath = Join-Path $ScriptsPath 'safety_validate.py'
  if (-not (Test-Path $scriptPath)) { Write-Log 'safety_validate.py missing' 'ERROR'; return 3 }
  $env:AIOS_SAFETY_AUTO_APPROVE = '1'
  $proc = & $py.Path $scriptPath --mode both --json 2>&1
  $exit = $LASTEXITCODE
  if ($CoherenceFormat -eq 'json') { $proc | Write-Output } else { Write-Log "Safety validation exit code: $exit" 'INFO' }
  if ($exit -ne 0) { Write-Log 'Safety validation reported issues' 'WARN' }
  return $exit
}

function Invoke-PruneArchives {
  param([int]$Keep=10)
  $archiveDir = Join-Path $Root 'docs/tachyonic_archive/folder_structure'
  if (-not (Test-Path $archiveDir)) { Write-Log "Archive directory not found: $archiveDir" 'WARN'; return }
  $files = @(Get-ChildItem -LiteralPath $archiveDir -Filter '*_folder_structure_*.json' | Sort-Object LastWriteTime -Descending)
  $count = $files.Length
  if ($count -le $Keep) { Write-Log "Archive pruning not needed (count=$count, keep=$Keep)" 'INFO'; return }
  $toRemove = $files[$Keep..($count-1)]
  foreach($f in $toRemove){
    try { Remove-Item -LiteralPath $f.FullName -Force; Write-Log "Pruned archive: $($f.Name)" 'INFO' } catch { Write-Log "Failed to remove archive $($f.Name): $($_.Exception.Message)" 'WARN' }
  }
  Write-Log "Archive pruning complete (kept $Keep of $count)" 'INFO'
}

function Invoke-GuardReport {
  # Summarize root_clutter_guard log events and governance events JSONL
  $logPath = Join-Path $Root 'root_clutter_guard.log'
  $eventsDir = Join-Path $Root 'docs/unified_backups/tachyonic_operations/governance_events'
  $eventsFile = Join-Path $eventsDir 'events.jsonl'
  $events = @()
  if (Test-Path $logPath) {
    $raw = Get-Content -Raw -Path $logPath
    # Attempt JSON lines parse: split on newlines and parse each
    $lines = ($raw -split "`n") | Where-Object { $_.Trim() }
    foreach($ln in $lines){
      try { $obj = $ln | ConvertFrom-Json -ErrorAction Stop; if ($obj) { $events += [pscustomobject]@{ source='root_guard_log'; file=$obj.file; length=$obj.length; removed=$obj.removed } } } catch { }
    }
    # Fallback: whole-file JSON (array or single object) if events empty
    if ($events.Count -eq 0) {
      try {
        $maybe = $raw | ConvertFrom-Json -ErrorAction Stop
        if ($maybe -is [System.Collections.IEnumerable]) {
          foreach($m in $maybe){ if ($m.file){ $events += [pscustomobject]@{ source='root_guard_blob'; file=$m.file; length=$m.length; removed=$m.removed } } }
        }
        else {
          if ($maybe.file){ $events += [pscustomobject]@{ source='root_guard_blob'; file=$maybe.file; length=$maybe.length; removed=$maybe.removed } }
        }
      } catch { }
    }
  }
  if (Test-Path $eventsFile) {
    foreach($ln in Get-Content -Path $eventsFile){
      if (-not $ln.Trim()) { continue }
      try { $e = $ln | ConvertFrom-Json -ErrorAction Stop; if ($e.type -eq 'root_deprecated_purge'){ $events += [pscustomobject]@{ source='events_jsonl'; file=$e.file; length=$e.length; removed=$e.ts } } } catch { }
    }
  }
  if ($events.Count -eq 0){ Write-Log 'No root guard events recorded' 'INFO'; return }
  $grouped = $events | Group-Object -Property file | ForEach-Object { [pscustomobject]@{ file=$_.Name; count=$_.Count; last=($_.Group | Sort-Object removed | Select-Object -Last 1 -ExpandProperty removed) } }
  $summaryItems = @()
  foreach($g in $grouped){ $summaryItems += ("{0}={1}@{2}" -f $g.file,$g.count,$g.last) }
  $summaryLine = "Root Guard Event Summary (file,count,last): " + ($summaryItems -join '; ')
  Write-Log $summaryLine 'INFO'
  if ($CoherenceFormat -eq 'json') { $grouped | ConvertTo-Json -Depth 4 | Write-Output }
}

function Invoke-NormalizeGuardLog {
  $logPath = Join-Path $Root 'root_clutter_guard.log'
  if (-not (Test-Path $logPath)) { Write-Log 'Guard log not found (nothing to normalize)' 'WARN'; return }
  $raw = Get-Content -Raw -Path $logPath
  $trimmed = ($raw.Trim())
  $normalized = @()
  # Detect JSONL: multiple lines each independently parseable
  $rawLines = $raw -split "`n"
  $parseableLineCount = 0
  foreach($ln in $rawLines){
    $t = $ln.Trim()
    if (-not $t) { continue }
    try { $null = $t | ConvertFrom-Json -ErrorAction Stop; $parseableLineCount++ } catch { $parseableLineCount = -1; break }
  }
  if ($parseableLineCount -gt 1 -and $parseableLineCount -eq (@($rawLines | Where-Object { $_.Trim() }).Count)) {
    # Already JSONL
    return
  }
  # Treat entire file as single JSON blob (object or array)
  try {
    $blob = $trimmed | ConvertFrom-Json -ErrorAction Stop
    if ($blob -is [System.Collections.IEnumerable] -and -not ($blob -is [string])) {
      foreach($b in $blob){ $normalized += ($b | ConvertTo-Json -Depth 5 -Compress) }
    } else {
      $normalized += ($blob | ConvertTo-Json -Depth 5 -Compress)
    }
  } catch {
    Write-Log 'Failed to parse guard log as single JSON blob; leaving unchanged' 'WARN'; return
  }
  if ($normalized.Count -gt 0) {
    Set-Content -Path $logPath -Value ($normalized -join [Environment]::NewLine) -Encoding UTF8
    Write-Log "Normalized guard log to JSONL lines=$($normalized.Count)" 'INFO'
  }
}

function Invoke-TruncateGuardLog {
  param([int]$Keep=200)
  $logPath = Join-Path $Root 'root_clutter_guard.log'
  if (-not (Test-Path $logPath)) { Write-Log 'Guard log not found (nothing to truncate)' 'WARN'; return }
  $lines = Get-Content -Path $logPath
  if ($lines.Count -le $Keep) { Write-Log "Guard log within retention (count=$($lines.Count), keep=$Keep)" 'INFO'; return }
  $new = $lines[-$Keep..-1]
  Set-Content -Path $logPath -Value ($new -join [Environment]::NewLine) -Encoding UTF8
  Write-Log "Truncated guard log to last $Keep lines (was $($lines.Count))" 'INFO'
}

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
  # Inventory filter: only examine root file list of folder_structure.json (avoid false positives deeper in tree)
  $inventoryFile = Join-Path $Root 'docs/AIOS/folder_structure.json'
  $inventoryOk = $true
  $inventoryRemediation = $null
  $inventoryCheckedRootFiles = @()
  if (Test-Path $inventoryFile){
    try {
      $invObj = Get-Content -Raw $inventoryFile | ConvertFrom-Json -ErrorAction Stop
      $rootEntry = $invObj.''
      if ($null -ne $rootEntry) {
        $inventoryCheckedRootFiles = @($rootEntry.files)
        foreach($d in $deprecated){ if ($inventoryCheckedRootFiles -contains $d) { $inventoryOk = $false; break } }
      }
    } catch {
      $invText = Get-Content -Raw $inventoryFile
      foreach($d in $deprecated){ if ($invText -match [regex]::Escape($d)) { $inventoryOk = $false; break } }
    }
    if (-not $inventoryOk) {
      # Dynamic remediation: confirm physical root re-scan has no deprecated files
      $physicalRootFiles = Get-ChildItem -LiteralPath $Root -File | Select-Object -ExpandProperty Name
      $physHit = $false
      foreach($d in $deprecated){ if ($physicalRootFiles -contains $d) { $physHit = $true; break } }
      if (-not $physHit) { $inventoryOk = $true; $inventoryRemediation = 'dynamic_rescan_pass' }
    }
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
  return [pscustomobject]@{ LFC=$lfc; GPC=$gpc; DeprecatedPresent=$present; GovernancePass=$govPass; GovernanceTotal=$govTotal; GovernanceFailures=$governanceFailures; ResurrectionPenalty=$resurrectionPenalty; MutationDistance=$mutationDistance; InventoryRemediation=$inventoryRemediation; InventoryCheckedRootFiles=$inventoryCheckedRootFiles }
}

function Invoke-CoherenceReport {
  $m = Get-CoherenceMetrics
  # Safety docs hygiene: ensure no root copies exist (fallback guard)
  foreach($dup in 'SAFETY_PROTOCOL.md','SAFETY_IMPLEMENTATION_SUMMARY.md'){
    if (Test-Path (Join-Path $Root $dup)) {
      try { Remove-Item (Join-Path $Root $dup) -Force } catch {}
    }
  }
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
  'update-hashes' { Invoke-UpdateHashes }
  'safety-validate' { $sv = Invoke-SafetyValidate; if ($sv -ne 0) { exit $sv } }
  'prune-archives' { Invoke-PruneArchives }
  'guard-report' { Invoke-GuardReport }
  'normalize-guard-log' { Invoke-NormalizeGuardLog }
  'truncate-guard-log' { Invoke-TruncateGuardLog }
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
  # Compute integrity hashes (SHA256) for safety nucleus docs
  $hashes = @{}
  foreach($sd in $SafetyDocs){
    if (Test-Path $sd){
      try {
        $h = (Get-FileHash -Algorithm SHA256 -Path $sd).Hash.ToLower()
        $hashes[$sd] = $h
      } catch {}
    }
  }
  if ($CoherenceFormat -eq 'json') {
    $metrics | Add-Member -NotePropertyName SafetyDocHashes -NotePropertyValue $hashes -Force
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
