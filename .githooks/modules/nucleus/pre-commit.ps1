#!/usr/bin/env pwsh
# AIOS Pre-commit Guard (Stage 1–4 enhancements)
# Responsibilities:
#  1. Deprecated file guard (via governance/hook_policy.json)
#  2. Allow deletion of deprecated files
#  3. Root hygiene (block unexpected new root files)
#  4. Size gate for large files (configurable)
#  5. Secret pattern scan (configurable regex set)
#  6. JSON validation for governed config paths
#  7. Executable bit sanity (scripts only)
#  8. Structured JSON logging (pass/block w/ rule data)
#  9. Bypass via env var (for emergency only, always logged)
# 10. Changelog enforcement for governed path changes (Stage 3)
# 11. Python syntax fast-check for modified Python under governed paths (Stage 3)
# 12. Targeted test execution on pattern matches (optional via env var) (Stage 3)
# 13. Metrics summary aggregation (Stage 3)
# 14. Large deletion heuristic + rationale flag (Stage 5)
# 15. Caching of file content hashes to skip repeat parsing (Stage 5)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# Import emotikiller integration
$EmotikillerIntegrationPath = Join-Path (Split-Path $PSScriptRoot -Parent) "laboratory\emotikiller\hook_integration.ps1"
if (Test-Path $EmotikillerIntegrationPath) {
    try {
        . $EmotikillerIntegrationPath
        $EmotikillerAvailable = $true
        Write-Verbose "[NUCLEUS] Emotikiller integration loaded"
    } catch {
        $EmotikillerAvailable = $false
        Write-Warning "[NUCLEUS] Failed to load emotikiller integration: $($_.Exception.Message)"
    }
} else {
    $EmotikillerAvailable = $false
    Write-Verbose "[NUCLEUS] Emotikiller integration not found"
}

# Import AI Context Reminder
$AIContextPath = Join-Path (Split-Path $PSScriptRoot -Parent) "membrane\ai_context_reminder.ps1"
if (Test-Path $AIContextPath) {
    try {
        . $AIContextPath
        $AIContextAvailable = $true
        Invoke-AIContextEnforcement -HookType "pre-commit"
        Write-Verbose "[NUCLEUS] AI Context reminder loaded and executed"
    } catch {
        $AIContextAvailable = $false
        Write-Warning "[NUCLEUS] Failed to load AI context reminder: $($_.Exception.Message)"
    }
} else {
    $AIContextAvailable = $false
    Write-Verbose "[NUCLEUS] AI Context reminder not found"
}

# Import AI Intelligence Extrusion Bridge
$AIExtrusionPath = Join-Path (Split-Path $PSScriptRoot -Parent) "membrane\ai_intelligence_extrusion_bridge.ps1"
if (Test-Path $AIExtrusionPath) {
    try {
        . $AIExtrusionPath
        $AIExtrusionAvailable = $true
        Write-Verbose "[NUCLEUS] AI Intelligence Extrusion Bridge loaded"
    } catch {
        $AIExtrusionAvailable = $false
        Write-Warning "[NUCLEUS] Failed to load AI intelligence extrusion bridge: $($_.Exception.Message)"
    }
} else {
    $AIExtrusionAvailable = $false
    Write-Verbose "[NUCLEUS] AI Intelligence Extrusion Bridge not found"
}

# -------------------- Utility & Core Functions --------------------
function New-DirIfMissing($Path) { if (-not (Test-Path $Path)) { New-Item -ItemType Directory -Force -Path $Path | Out-Null } }

function Get-Policy {
  param([string]$Path)
  if (Test-Path $Path) { try { return Get-Content $Path -Raw | ConvertFrom-Json } catch { } }
  return [pscustomobject]@{
    rules_version = 0
    deprecatedFiles = @('test_opencv_aios_integration.py','test_chatgpt_integration.py','setup_environment.ps1')
    rootAllowed = @('.githooks','README.md','AIOS_PROJECT_CONTEXT.md','AIOS.code-workspace','requirements.txt','pyproject.toml')
    maxFileSizeMB = 5
    allowLargePaths = @()
    secretPatterns = @()
    jsonPaths = @()
    executableScriptDirs = @(
        '.githooks/',
        'ai/',
        'core/',
        'tachyonic/',
        'runtime_intelligence/',
        'scripts/',
        'orchestrator/',
        'tools/'
    )
    bypassEnvVar = 'AIOS_HOOK_BYPASS'
  }
}

function Write-JsonLog {
  param([string]$Status,[hashtable]$Data)
  try {
    $logDir = Join-Path (Resolve-Path .) 'runtime_intelligence/logs/hooks'
    New-DirIfMissing $logDir
    $entry = [ordered]@{ timestamp=(Get-Date).ToString('o'); status=$Status; rules_version=$Policy.rules_version; profile=$HookProfile; data=$Data }
    ($entry | ConvertTo-Json -Depth 6 -Compress) + [Environment]::NewLine | Out-File (Join-Path $logDir 'pre_commit.log') -Append -Encoding utf8
  } catch { Write-Host " Hook logging failed: $($_.Exception.Message)" -ForegroundColor Yellow }
}

function Save-MetricsSummary {
  param([hashtable]$Delta)
  try {
    $summaryPath = $Policy.metricsSummaryPath
    if (-not $summaryPath) { return }
    $dir = Split-Path $summaryPath -Parent; New-DirIfMissing $dir
    $summary = if (Test-Path $summaryPath) { Get-Content $summaryPath -Raw | ConvertFrom-Json } else { [pscustomobject]@{ passes=0; blocks=0; rules=@{}; last_update=(Get-Date).ToString('o') } }
    foreach ($k in $Delta.Keys) {
      if ($k -in @('passes','blocks')) { $summary.$k = $summary.$k + $Delta[$k]; continue }
      if (-not $summary.rules.ContainsKey($k)) { $summary.rules[$k] = 0 }
      $summary.rules[$k] = $summary.rules[$k] + $Delta[$k]
    }
    $summary.last_update = (Get-Date).ToString('o')
    $summary | ConvertTo-Json -Depth 6 | Out-File $summaryPath -Encoding utf8
  } catch { }
}

function Get-Staged {
  $raw = git diff --cached --numstat --name-status
  $statusRaw = git diff --cached --name-status
  if (-not $statusRaw) { return @() }
  $map = @{}
  foreach($line in $statusRaw -split "`n"){ 
    if(-not $line.Trim()){continue}
    # Handle different git status formats properly
    if ($line -match '^([AMDRC]\d*)\s+(.+)$') {
      $status = $matches[1]
      $filename = $matches[2]
      # For renames, git shows "oldfile -> newfile", we want the new file
      if ($filename -match '^.+\s+->\s+(.+)$') {
        $filename = $matches[1].Trim()
      }
      $map[$filename] = $status
    }
  }
  $deletions = 0; $totalChanged=0
  foreach($line in ($raw -split "`n")){
    if($line -match '^(\d+|-)\t(\d+|-)\t(.+)$'){
      $added=$matches[1]; $deleted=$matches[2]
      if($added -ne '-' -and $deleted -ne '-') { $totalChanged += [int]$added + [int]$deleted }
      if($deleted -ne '-' -and $added -ne '-') { $deletions += [int]$deleted }
    }
  }
  $entries = @(); foreach($k in $map.Keys){ $entries += [pscustomobject]@{ Status=$map[$k]; Path=$k } }
  return ,@($entries,$totalChanged,$deletions)
}

function Test-PathPatternMatch { param($Path,$Patterns) foreach ($pat in $Patterns){ $escaped=[Regex]::Escape($pat)-replace '\\\*','.*'; if ($Path -imatch "^$escaped$") {return $true}; if ($pat.EndsWith('/')){ if ($Path -like "$pat*") {return $true} } } return $false }

function Test-Deprecated($entries){ $v=@(); foreach($e in $entries){ if ($Policy.deprecatedFiles -contains $e.Path -and $e.Status -ne 'D'){ $v+=$e.Path } }; return $v }
function Test-RootHygiene($entries){ $v=@(); foreach($e in $entries){ if ($e.Status -match 'A|R' -and ($e.Path -notmatch '/')){ if (-not ($Policy.rootAllowed -contains $e.Path) -and -not ($Policy.deprecatedFiles -contains $e.Path)){ $v+=$e.Path } } }; return $v }
function Test-Size($entries){ $v=@(); $maxBytes=[int]($Policy.maxFileSizeMB*1MB); foreach($e in $entries){ if($e.Status -eq 'D' -or -not (Test-Path $e.Path)){continue}; $allow=$false; foreach($p in $Policy.allowLargePaths){ if($e.Path -like "$p*"){ $allow=$true; break } }; if(-not $allow){ try{ $len=(Get-Item $e.Path).Length; if($len -gt $maxBytes){ $v+="$($e.Path) (${len}B)" } } catch{} } }; return $v }
function Test-Secrets($entries){ $v=@(); foreach($e in $entries){ if($e.Status -eq 'D' -or -not (Test-Path $e.Path)){continue}; $exclude=$false; if($Policy.PSObject.Properties.Name -contains 'secretScanExcludePaths'){ foreach($excludePath in $Policy.secretScanExcludePaths){ if($e.Path -like "$excludePath*" -or $e.Path -like "*$excludePath"){ $exclude=$true; break } } }; if($exclude){continue}; try{ $fi=Get-Item $e.Path; if($fi.Length -gt 512KB){continue}; $ext=[IO.Path]::GetExtension($e.Path).ToLower(); if($ext -in @('.png','.jpg','.jpeg','.gif','.exe','.dll','.so','.zip','.bin')){continue}; $content=Get-Content $e.Path -Raw; foreach($pattern in $Policy.secretPatterns){ if($content -match $pattern){ $v+="$($e.Path):$pattern"; break } } } catch{} }; return $v }
function Test-JSON($entries){ $v=@(); foreach($e in $entries){ if($e.Status -eq 'D' -or -not (Test-Path $e.Path)){continue}; if (Test-PathPatternMatch -Path $e.Path -Patterns $Policy.jsonPaths){ try { Get-Content $e.Path -Raw | ConvertFrom-Json | Out-Null } catch { $v+=$e.Path } } }; return $v }
function Test-Exec($entries){ $v=@(); foreach($e in $entries){ if($e.Status -eq 'D' -or -not (Test-Path $e.Path)){continue}; try{ $first=(Get-Content $e.Path -TotalCount 1); if($first -match '^#!'){ $allowed=$false; foreach($dir in $Policy.executableScriptDirs){ if($e.Path -like "$dir*"){ $allowed=$true; break } }; if(-not $allowed){ $v+=$e.Path } } } catch{} }; return $v }
function Test-Changelog($entries){ $required=$false; foreach($e in $entries){ if($e.Status -eq 'D'){continue}; if(Test-PathPatternMatch -Path $e.Path -Patterns $Policy.requireChangelogOnPaths){ $required=$true; break } }; if(-not $required){ return @() }; foreach($e in $entries){ if($Policy.changelogFiles -contains $e.Path){ return @() } }; return @('(changelog-missing)') }
function Test-PythonSyntax($entries){ $v=@(); foreach($e in $entries){ if($e.Status -eq 'D' -or [IO.Path]::GetExtension($e.Path).ToLower() -ne '.py'){continue}; if(-not (Test-PathPatternMatch -Path $e.Path -Patterns $Policy.pythonSyntaxPaths)){continue}; if(Test-Path $e.Path){ try { python -m py_compile $e.Path 2>$null } catch { $v+=$e.Path } } }; return $v }
function Invoke-TargetedTests($entries){ if($env:AIOS_HOOK_RUN_TESTS -ne '1'){ return @() }; foreach($e in $entries){ if($e.Path -like 'ai/src/core/integration/*'){ try { pytest -q ai/tests 2>&1 | Out-Null; if($LASTEXITCODE -ne 0){ return @('integration-tests') } else { return @() } } catch { return @('integration-tests-exception') } } }; return @() }

function Get-Checks {
  param([array]$Entries,[string]$HookProfile)
  $results = [ordered]@{}
  $results.deprecated = Test-Deprecated $Entries
  $results.root = Test-RootHygiene $Entries
  
  # Add emoticon policy check
  if ($EmotikillerAvailable -and (Get-Command Test-EmoticonPolicyCompliance -ErrorAction SilentlyContinue)) {
    try {
      $emoticonCheck = Test-EmoticonPolicyCompliance -StagedFiles ($Entries | Where-Object { $_.Status -ne 'D' } | ForEach-Object { $_.Path }) -HookType "pre-commit"
      if (-not $emoticonCheck.Compliant) {
        $results.emoticons = @("$($emoticonCheck.ViolationCount) emoticon violation(s) in $($emoticonCheck.FilesAffected) file(s)")
      }
    } catch {
      Write-Warning "[NUCLEUS] Emoticon policy check failed: $($_.Exception.Message)"
    }
  }
  
  if ($HookProfile -eq 'fast') { return $results }
  $results.size = Test-Size $Entries
  $results.secrets = Test-Secrets $Entries
  $results.json = Test-JSON $Entries
  $results.exec = Test-Exec $Entries
  $results.changelog = Test-Changelog $Entries
  $results.py = Test-PythonSyntax $Entries
  $results.tests = Invoke-TargetedTests $Entries
  return $results
}

# -------------------- Main Execution --------------------
$policyPath = 'governance/hook_policy.json'
$Policy = Get-Policy -Path $policyPath
$HookProfile = ($env:AIOS_HOOK_PROFILE) ; if ([string]::IsNullOrWhiteSpace($HookProfile)) { $HookProfile = 'full' }
if ($HookProfile -notin @('fast','full')) { $HookProfile = 'full' }

# Bypass check
if ($env:AIOS_HOOK_BYPASS -eq '1') { Write-Host ' Hook bypass active via AIOS_HOOK_BYPASS=1' -ForegroundColor Yellow; Write-JsonLog -Status 'bypass' -Data @{ reason='env var'; user=$env:USERNAME }; exit 0 }

${parsed} = Get-Staged
$stagedEntries = $parsed[0]
$totalChanged = $parsed[1]
$deletions = $parsed[2]
if ($stagedEntries.Count -eq 0) { Write-JsonLog -Status 'pass' -Data @{ reason='no changes' }; Save-MetricsSummary @{ passes=1 }; exit 0 }

$results = Get-Checks -Entries $stagedEntries -Profile $HookProfile

# Criticality integration (warnings + deletion blocks)
if ($Policy.PSObject.Properties.Name -contains 'criticality') {
  $crit = $Policy.criticality
  $indexPath = $crit.indexPath
  $critBlocks = @()
  $critWarns = @()
  if (-not (Test-Path $indexPath) -and $crit.scoreRegenScript) {
    try { python $crit.scoreRegenScript 2>$null } catch { }
  }
  if (Test-Path $indexPath) {
    $tierMap = @{}
    try {
      Get-Content $indexPath -Raw | ForEach-Object { $_ -split "`n" } | ForEach-Object {
        if (-not $_.Trim()) { return }
        try { $obj = $_ | ConvertFrom-Json } catch { $obj = $null }
        if ($obj -and $obj.path -and $obj.tier) { $tierMap[$obj.path] = $obj }
      }
    } catch {}
    foreach ($e in $stagedEntries) {
      $p = $e.Path
      if ($tierMap.ContainsKey($p)) {
        $tier = $tierMap[$p].tier
        # Deletion blocks for configured tiers
        if ($e.Status -eq 'D' -and $crit.blockDeletionTiers -contains $tier) {
          $critBlocks += "$p($tier)"
        }
        # Core modification warnings
        elseif ($crit.warnOnCoreModify -and $tier -eq 'core' -and $e.Status -ne 'D') {
          $critWarns += "$p($tier)"
        }
      }
    }
  }
  if ($critBlocks.Count -gt 0) { $results.criticality_delete = $critBlocks }
  # Warnings (non-blocking) captured separately
  if ($critWarns.Count -gt 0) { $results.criticality_warn = $critWarns }
}

# Large deletion heuristic
if ($Policy.largeDeletionThresholdPct -and $totalChanged -gt 0) {
  $pct = [math]::Round(($deletions / $totalChanged) * 100,2)
  if ($pct -ge [int]$Policy.largeDeletionThresholdPct -and $env:AIOS_HOOK_ALLOW_LARGE_DELETE -ne '1') {
    $cacheDir = $Policy.cacheDir; if($cacheDir){ if(-not (Test-Path $cacheDir)){ New-Item -ItemType Directory -Force -Path $cacheDir | Out-Null }
      New-Item -ItemType File -Force -Path (Join-Path $cacheDir 'pending_large_delete.flag') | Out-Null }
    $results.large_delete = @("$pct% of changed lines are deletions (threshold=$($Policy.largeDeletionThresholdPct)%)")
  }
}

# Determine violations
$violations = @(); foreach($k in $results.Keys){ if($k -eq 'criticality_warn'){ continue }; $val = $results[$k]; if($val -and (($val -is [array] -and $val.Count -gt 0) -or ($val -isnot [array] -and $val))){ $violations += $k } }
if ($violations.Count -eq 0) {
  if ($results.Contains('criticality_warn') -and $results.criticality_warn) {
    Write-Host " Core file modifications (review advised): $($results.criticality_warn -join ', ')" -ForegroundColor Yellow
  }
  
  # 🧠 AIOS AI Intelligence Extrusion - Feed real-time direction to AI engine
  if ($AIExtrusionAvailable) {
    try {
      Write-Host "🧠 [AIOS-AI-EXTRUSION] Extracting intelligence for AI guidance..." -ForegroundColor Cyan
      & $AIExtrusionPath -HookType "pre-commit" -RealTimeMode
    } catch {
      Write-Warning "[NUCLEUS] AI Intelligence Extrusion failed: $($_.Exception.Message)"
    }
  }
  
  $warningsData = if ($results.Contains('criticality_warn')) { $results.criticality_warn } else { $null }
  Write-JsonLog -Status 'pass' -Data @{ changed=$stagedEntries.Count; profile=$HookProfile; criticality_warn=$warningsData }
  $metricsDelta = @{ passes=1 }
  Save-MetricsSummary $metricsDelta
  exit 0
}

Write-Host " Commit blocked:" -ForegroundColor Red
foreach($k in $violations){ $vals = $results[$k] -join ', '; Write-Host " - ${k}: ${vals}" -ForegroundColor Red }
Write-Host "Remediation:" -ForegroundColor Yellow
if ($results.deprecated){ Write-Host " * Remove or exclude deprecated files (deletion allowed)." -ForegroundColor Yellow }
if ($results.root){ Write-Host " * Move unexpected root files into proper subdirectories or update policy." -ForegroundColor Yellow }
if ($results.size){ Write-Host " * Reduce or split oversized files or whitelist path." -ForegroundColor Yellow }
if ($results.secrets){ Write-Host " * Remove / rotate secrets; use env vars or secret manager." -ForegroundColor Yellow }
if ($results.json){ Write-Host " * Fix JSON syntax in listed files." -ForegroundColor Yellow }
if ($results.exec){ Write-Host " * Move script to approved directory or remove shebang." -ForegroundColor Yellow }
if ($results.changelog){ Write-Host " * Add changelog entry file (tachyonic) for governed path changes." -ForegroundColor Yellow }
if ($results.py){ Write-Host " * Fix Python syntax errors (py_compile)." -ForegroundColor Yellow }
if ($results.tests){ Write-Host " * Investigate failing targeted tests." -ForegroundColor Yellow }
if ($results.Contains('criticality_warn') -and $results.criticality_warn){ Write-Host " * Core file modifications detected (non-blocking) -> ensure ledger ID & dual review if escalated." -ForegroundColor Yellow }

if ($results.Contains('criticality_delete') -and $results.criticality_delete){ Write-Host " * Deletion of core/high tier file requires staged deprecation process." -ForegroundColor Yellow }

Write-JsonLog -Status 'block' -Data @{ violations=$results; profile=$HookProfile }
$metricsDelta = @{ blocks=1 }
foreach($k in $violations){ $metricsDelta["rule_$k"] = 1 }
Save-MetricsSummary $metricsDelta
exit 1
