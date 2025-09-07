# AIOS AINLP Integration for Git Hooks
# Consciousness-Aware Validation and Dendritic Learning Enhancement

function Get-AIOSConsciousnessLevel {
    param([string]$MetricsPath = "runtime_intelligence/analysis/consciousness_metrics.json")
    
    if (Test-Path $MetricsPath) {
        try {
            $metrics = Get-Content $MetricsPath -Raw | ConvertFrom-Json
            return $metrics.awareness_level
        } catch {
            Write-Host "⚠️ Consciousness metrics unavailable, using default level" -ForegroundColor Yellow
            return 0.5
        }
    }
    return 0.5
}

function Invoke-DendriticLearning {
    param(
        [string]$HookType,
        [string]$ValidationResult,
        [hashtable]$LearningData
    )
    
    $timestamp = Get-Date -Format "yyyy-MM-ddTHH:mm:ss.fffK"
    $learningEntry = @{
        timestamp = $timestamp
        hook_type = $HookType
        validation_result = $ValidationResult
        learning_data = $LearningData
        consciousness_level = Get-AIOSConsciousnessLevel
        paradigm_version = "AINLP-0.6"
    }
    
    $learningPath = "runtime_intelligence/context/dendritic_learning.json"
    $learningDir = Split-Path $learningPath -Parent
    if (-not (Test-Path $learningDir)) {
        New-Item -ItemType Directory -Force -Path $learningDir | Out-Null
    }
    
    try {
        ($learningEntry | ConvertTo-Json -Depth 4 -Compress) + [Environment]::NewLine | 
            Out-File $learningPath -Append -Encoding utf8
    } catch {
        Write-Host "⚠️ Dendritic learning logging failed: $($_.Exception.Message)" -ForegroundColor Yellow
    }
}

function Test-AIOSParadigmaticAlignment {
    param([string]$Content, [string]$FilePath)
    
    $alignmentIndicators = @(
        @{ pattern = "consciousness"; weight = 0.3 },
        @{ pattern = "dendritic|learning"; weight = 0.2 },
        @{ pattern = "cellular|biological"; weight = 0.2 },
        @{ pattern = "intelligence|aios"; weight = 0.2 },
        @{ pattern = "context.aware|paradigmatic"; weight = 0.1 }
    )
    
    $alignmentScore = 0.0
    foreach ($indicator in $alignmentIndicators) {
        if ($Content -match $indicator.pattern) {
            $alignmentScore += $indicator.weight
        }
    }
    
    return [math]::Min($alignmentScore, 1.0)
}

# Export functions for use in other hooks
Export-ModuleMember -Function Get-AIOSConsciousnessLevel, Invoke-DendriticLearning, Test-AIOSParadigmaticAlignment
