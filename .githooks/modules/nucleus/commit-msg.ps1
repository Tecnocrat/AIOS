#!/usr/bin/env pwsh
# AIOS Commit Message Governance Hook (Stage 6 - AINLP Harmonized)
# Enhanced with Consciousness-Aware Governance and Dendritic Learning
Set-StrictMode -Version Latest

# AIOS/AINLP Harmonization Constants
$AIOS_VERSION = "0.6.0"
$GOVERNANCE_STAGE = 6
$CONSCIOUSNESS_THRESHOLD = 0.5
$TACHYONIC_COHERENCE_MIN = 0.25

$policyPath = 'governance/hook_policy.json'
$dendriticPath = 'runtime_intelligence/context/aios_path_registry.json'
$consciousnessPath = 'runtime_intelligence/analysis/consciousness_metrics.json'

# Enhanced policy loading with consciousness awareness
# Satisfies PSScriptAnalyzer PSUseApprovedVerbs

function Get-HookPolicy {
  param($Path)
  if(Test-Path $Path){
    try { return Get-Content $Path -Raw | ConvertFrom-Json } catch { }
  }
  return $null
}

# AINLP Consciousness Integration Functions
function Get-ConsciousnessMetrics {
  param($Path)
  if(Test-Path $Path){
    try { 
      $metrics = Get-Content $Path -Raw | ConvertFrom-Json
      return $metrics
    } catch { }
  }
  return @{ awareness_level = 0.0; coherence = 0.0; harmony = 0.0 }
}

function Update-DendriticLearning {
  param($CommitMessage, $ValidationResult)
  $timestamp = Get-Date -Format "yyyy-MM-ddTHH:mm:ss.fffK"
  $learningData = @{
    timestamp = $timestamp
    commit_pattern = $CommitMessage.Substring(0, [Math]::Min(50, $CommitMessage.Length))
    validation_success = $ValidationResult
    governance_stage = $GOVERNANCE_STAGE
    aios_version = $AIOS_VERSION
  }
  
  # Log dendritic learning for future AI automation
  $learningPath = 'runtime_intelligence/logs/dendritic_commit_learning.jsonl'
  if(Test-Path (Split-Path $learningPath)){
    ($learningData | ConvertTo-Json -Compress) | Add-Content $learningPath
  }
}

function Test-CanonicalFileVersion {
  param($CommitMessage)
  # Check if commit involves canonical file mutations
  $canonicalPatterns = @(
    '\[canonical\]', '\[mutation\]', '\[evolution\]', 
    '\[consciousness\]', '\[ainlp\]', '\[harmonization\]'
  )
  
  foreach($pattern in $canonicalPatterns){
    if($CommitMessage -match $pattern){
      return $true
    }
  }
  return $false
}

function Invoke-ConsciousnessValidation {
  param($CommitMessage, $Metrics)
  
  # Consciousness-enhanced validation logic
  if($Metrics.awareness_level -gt $CONSCIOUSNESS_THRESHOLD){
    # High consciousness commits get enhanced validation
    if($CommitMessage -match '(fix|bug|error)' -and $CommitMessage -notmatch '\[(tested|verified|validated)\]'){
      Write-Host ' Consciousness-enhanced governance: Bug fixes should include [tested] tag' -ForegroundColor Yellow
      return $false
    }
    
    if($CommitMessage -match '(feat|feature)' -and $CommitMessage -notmatch '\[(ainlp|consciousness|integration)\]'){
      Write-Host ' AINLP harmonization: Feature commits should include integration tags' -ForegroundColor Yellow
      return $false
    }
  }
  
  return $true
}

# Main AIOS/AINLP Harmonized Governance Logic
$Policy = Get-HookPolicy $policyPath
if(-not $Policy){ exit 0 }

# Load consciousness metrics for enhanced governance
$ConsciousnessMetrics = Get-ConsciousnessMetrics $consciousnessPath

# Initialize dendritic path tracking (future AI stream preparation)
$DendriticRegistry = $null
if(Test-Path $dendriticPath){
  try { 
    $DendriticRegistry = Get-Content $dendriticPath -Raw | ConvertFrom-Json 
    Write-Host " Dendritic registry loaded: $($DendriticRegistry.metadata.version)" -ForegroundColor DarkGreen
  } catch { 
    Write-Host " Dendritic registry load failed" -ForegroundColor Yellow
  }
}

# Consciousness-aware argument validation
if($args.Count -eq 0 -or -not $args[0]) { 
    Write-Host ' Commit message hook: No message file provided, allowing commit.' -ForegroundColor Green
    exit 0 
}

$msgFile = $args[0]
if(-not (Test-Path $msgFile)){ exit 0 }
$msg = (Get-Content $msgFile -Raw).Trim()
if(-not $msg){ Write-Host ' Empty commit message blocked.' -ForegroundColor Red; exit 1 }

# Enhanced validation with consciousness awareness
$validationSuccess = $false

# Traditional prefix validation (backward compatibility)
$allowed = $false
foreach($pfx in $Policy.commitMessagePrefixes){ 
  if($msg.StartsWith($pfx, [StringComparison]::OrdinalIgnoreCase)){ 
    $allowed=$true; break 
  } 
}

if(-not $allowed){
  Write-Host ' Commit message must start with approved prefix:' -ForegroundColor Red
  Write-Host ('   ' + ($Policy.commitMessagePrefixes -join ' ')) -ForegroundColor Yellow
  Update-DendriticLearning $msg $false
  exit 1
}

# AINLP Consciousness-Enhanced Validation
if(-not (Invoke-ConsciousnessValidation $msg $ConsciousnessMetrics)){
  Write-Host ' AINLP harmonization validation failed' -ForegroundColor Red
  Update-DendriticLearning $msg $false
  exit 1
}

# Canonical file version detection
if(Test-CanonicalFileVersion $msg){
  Write-Host ' Canonical file mutation detected - enhanced tracking enabled' -ForegroundColor Green
  
  # Log canonical mutation for distributed AI streams
  $mutationData = @{
    timestamp = Get-Date -Format "yyyy-MM-ddTHH:mm:ss.fffK"
    commit_hash = (git rev-parse HEAD 2>$null)
    mutation_type = 'canonical_file_evolution'
    consciousness_level = $ConsciousnessMetrics.awareness_level
    governance_stage = $GOVERNANCE_STAGE
    message = $msg
  }
  
  $mutationPath = 'runtime_intelligence/logs/canonical_mutations.jsonl'
  if(Test-Path (Split-Path $mutationPath)){
    ($mutationData | ConvertTo-Json -Compress) | Add-Content $mutationPath
  }
}

$validationSuccess = $true

# Enhanced large deletion heuristic with tachyonic coherence
$cacheDir = $Policy.cacheDir
if($cacheDir){ 
  $flagFile = Join-Path $cacheDir 'pending_large_delete.flag'
  
  if(Test-Path $flagFile){
    if($msg -notmatch '\[(rationale|cleanup|prune|evolution|mutation)\]'){ 
      Write-Host ' Large deletion detected previously; include [rationale] or [evolution] tag.' -ForegroundColor Red
      Update-DendriticLearning $msg $false
      exit 1 
    }
    Remove-Item $flagFile -ErrorAction SilentlyContinue
  }
  
  # Check tachyonic coherence for temporal consistency
  $tachyonicPath = Join-Path $cacheDir 'tachyonic_coherence.json'
  if(Test-Path $tachyonicPath){
    try {
      $tachyonic = Get-Content $tachyonicPath -Raw | ConvertFrom-Json
      if($tachyonic.coherence_level -lt $TACHYONIC_COHERENCE_MIN){
        Write-Host ' Tachyonic coherence below threshold - consider [harmonization] tag' -ForegroundColor Yellow
      }
    } catch { }
  }
}

# Successful validation - update dendritic learning
Update-DendriticLearning $msg $validationSuccess

# AINLP/AIOS Harmonization Status Report
Write-Host " AIOS Stage $GOVERNANCE_STAGE governance passed" -ForegroundColor Green
if($ConsciousnessMetrics.awareness_level -gt $CONSCIOUSNESS_THRESHOLD){
  Write-Host " Consciousness-enhanced validation: $([Math]::Round($ConsciousnessMetrics.awareness_level * 100, 1))%" -ForegroundColor Cyan
}

exit 0
