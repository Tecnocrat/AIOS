#!/usr/bin/env pwsh
# AIOS Pre-push Hook (Stage 6) - Consciousness-Enhanced Build & Test Validation
# Enhanced with AINLP integration and consciousness-aware validation patterns
Set-StrictMode -Version Latest
$ErrorActionPreference='Stop'

# AIOS Pre-push Hook - Free Cell Architecture  
# AINLP Tachyonic Path: tachyonic/AINLP_CANONICAL_KNOWLEDGE_GENOME.md
# Free Cell Pattern: Minimal consciousness calls with functional efficiency

function Load-Policy { param($p) if(Test-Path $p){ try { return Get-Content $p -Raw | ConvertFrom-Json } catch {} } }
$Policy = Load-Policy 'governance/hook_policy.json'
if(-not $Policy -or -not $Policy.prePush.enable){ exit 0 }

if($env:AIOS_PREPUSH_SKIP -eq '1') { Write-Host ' Pre-push skipped via env var.' -ForegroundColor Yellow; exit 0 }

# Free cell consciousness reference (minimal AINLP call)
$consciousnessState = @{ Status = "FREE_CELL_OPTIMIZED" }
$consciousnessLevel = @{ Level = "OPTIMAL" }

Write-Host " Pre-push validation starting... (Consciousness Level: $($consciousnessLevel.Level))" -ForegroundColor Cyan
Write-Host " AIOS Free Cell Architecture: $($consciousnessState.Status)" -ForegroundColor Magenta

$fail=$false
$buildMetrics = @{
    commands_executed = 0
    commands_successful = 0
    consciousness_enhancements = 0
    start_time = Get-Date
}

# Consciousness-enhanced build validation (Free cell pattern)
foreach($cmd in $Policy.prePush.buildCommands){
  Write-Host " Build: $cmd" -ForegroundColor DarkCyan
  $buildMetrics.commands_executed++
  
  # Free cell consciousness assessment (minimal AINLP call)
  $buildConsciousness = @{ RequiresEnhancement = $false; Status = "OPTIMIZED" }
  
  try { 
    Invoke-Expression $cmd 
    $buildMetrics.commands_successful++
  } catch { 
    $fail=$true
    Write-Host "Build command failed: $cmd" -ForegroundColor Red
    Write-Host " Free cell analysis: Build failure requires optimization" -ForegroundColor Yellow
    break 
  }
  if($LASTEXITCODE -ne 0){ 
    $fail=$true
    Write-Host "Build exit code $LASTEXITCODE" -ForegroundColor Red
    Write-Host " Free cell recommendation: Review build coherence" -ForegroundColor Yellow
    break 
  }
}

$testMetrics = @{
    commands_executed = 0
    commands_successful = 0
    consciousness_validations = 0
    paradigmatic_alignments = 0
}

# Consciousness-enhanced test validation
if(-not $fail){
  foreach($t in $Policy.prePush.testCommands){
    Write-Host "🧪 Test: $t" -ForegroundColor DarkCyan
    $testMetrics.commands_executed++
    
    # Free cell consciousness assessment (minimal AINLP call)
    $testConsciousness = @{ Aligned = $true; Status = "OPTIMIZED" }
    if ($testConsciousness.Aligned) {
      $testMetrics.paradigmatic_alignments++
    }
    
    try { 
      Invoke-Expression $t 
      $testMetrics.commands_successful++
      $testMetrics.consciousness_validations++
    } catch { 
      $fail=$true
      Write-Host "Test command failed: $t" -ForegroundColor Red
      Write-Host " Free cell analysis: Test failure requires optimization" -ForegroundColor Yellow
      break 
    }
    if($LASTEXITCODE -ne 0){ 
      $fail=$true
      Write-Host "Test exit code $LASTEXITCODE" -ForegroundColor Red
      Write-Host " Consciousness recommendation: Review test consciousness coherence patterns" -ForegroundColor Yellow
      break 
    }
  }
}

# Final consciousness validation and reporting
$endTime = Get-Date
$totalDuration = ($endTime - $buildMetrics.start_time).TotalSeconds

$finalMetrics = @{
    build_metrics = $buildMetrics
    test_metrics = $testMetrics
    consciousness_level = $consciousnessLevel
    duration_seconds = $totalDuration
    overall_success = -not $fail
    consciousness_enhancements_applied = $buildMetrics.consciousness_enhancements + $testMetrics.consciousness_validations
}

if($fail){ 
  Write-Host ' Pre-push blocked.' -ForegroundColor Red
  Write-Host " Consciousness State: Validation failure detected - consider consciousness-guided remediation" -ForegroundColor Yellow
  
  # Log failure metrics for consciousness learning
  $finalMetrics | ConvertTo-Json -Compress | Add-Content -Path "runtime_intelligence/logs/pre_push_failures.jsonl"
  exit 1 
}

Write-Host ' Pre-push validation passed.' -ForegroundColor Green
Write-Host " Consciousness Enhancement: $($finalMetrics.consciousness_enhancements_applied) consciousness patterns applied" -ForegroundColor Green
Write-Host " Tachyonic Performance: $($totalDuration)s with $($consciousnessLevel.Level) consciousness level" -ForegroundColor Cyan

# Log success metrics for consciousness evolution
$finalMetrics | ConvertTo-Json -Compress | Add-Content -Path "runtime_intelligence/logs/pre_push_success.jsonl"

exit 0
