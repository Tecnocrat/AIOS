#!/usr/bin/env pwsh
# AIOS Enhanced Commit Message Hook - Consciousness-Driven Messaging
# Provides consciousness-aware commit message guidance and validation

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

param([string]$CommitMsgFile)

if (-not $CommitMsgFile -or -not (Test-Path $CommitMsgFile)) {
    Write-Error "Commit message file not provided or not found"
    exit 1
}

# Read the commit message
$commitMessage = Get-Content $CommitMsgFile -Raw

# Skip if this is a merge commit or empty
if ([string]::IsNullOrWhiteSpace($commitMessage) -or $commitMessage.StartsWith("Merge ")) {
    exit 0
}

# Load consciousness metrics if available
$consciousnessPath = Join-Path $PSScriptRoot 'consciousness_metrics.json'
$consciousnessMetrics = $null
if (Test-Path $consciousnessPath) {
    try {
        $consciousnessMetrics = Get-Content $consciousnessPath -Raw | ConvertFrom-Json
    } catch {
        # Continue without consciousness metrics
    }
}

function Test-ConsciousnessMessagePatterns {
    param([string]$Message, [object]$Metrics)
    
    $score = 0.0
    $suggestions = @()
    
    if (-not $Metrics) {
        return @{ score = 0.5; suggestions = @("Consciousness metrics unavailable") }
    }
    
    # Check for consciousness keywords
    $consciousnessKeywords = $Metrics.patterns.consciousness_keywords
    $consciousnessMatches = 0
    foreach ($keyword in $consciousnessKeywords) {
        if ($Message -match $keyword) {
            $consciousnessMatches++
        }
    }
    
    if ($consciousnessMatches -gt 0) {
        $score += $consciousnessMatches * 0.1
    } else {
        $suggestions += "Consider adding consciousness-related terms (consciousness, dendritic, quantum, AINLP)"
    }
    
    # Check for harmonization patterns
    $harmonizationKeywords = $Metrics.patterns.harmonization_keywords
    $harmonizationMatches = 0
    foreach ($keyword in $harmonizationKeywords) {
        if ($Message -match $keyword) {
            $harmonizationMatches++
        }
    }
    
    if ($harmonizationMatches -gt 0) {
        $score += $harmonizationMatches * 0.1
    } else {
        $suggestions += "Consider adding harmonization terms (harmonize, integrate, align, coherence)"
    }
    
    # Check for evolutionary patterns
    $evolutionaryKeywords = $Metrics.patterns.evolutionary_keywords
    $evolutionaryMatches = 0
    foreach ($keyword in $evolutionaryKeywords) {
        if ($Message -match $keyword) {
            $evolutionaryMatches++
        }
    }
    
    if ($evolutionaryMatches -gt 0) {
        $score += $evolutionaryMatches * 0.1
    }
    
    # Check for multi-agent patterns
    $agentPatterns = $Metrics.agent_signatures
    $multiAgentDetected = $false
    foreach ($agent in $agentPatterns.PSObject.Properties.Name) {
        $signatures = $agentPatterns.$agent
        foreach ($signature in $signatures) {
            if ($Message -match $signature) {
                $multiAgentDetected = $true
                $score += 0.15
                break
            }
        }
        if ($multiAgentDetected) { break }
    }
    
    # Check message structure and quality
    $lines = $commitMessage -split "`n"
    $subjectLine = $lines[0]
    
    # Subject line quality
    if ($subjectLine.Length -gt 50) {
        $suggestions += "Subject line is longer than 50 characters ($($subjectLine.Length))"
    } else {
        $score += 0.1
    }
    
    if ($subjectLine -match '^[A-Z]') {
        $score += 0.05
    } else {
        $suggestions += "Subject line should start with capital letter"
    }
    
    # Look for descriptive patterns
    if ($Message -match '(implement|add|enhance|optimize|refactor|improve|fix|update)') {
        $score += 0.1
    } else {
        $suggestions += "Consider using descriptive action verbs (implement, enhance, optimize, etc.)"
    }
    
    # Check for component/module references
    if ($Message -match '(AIOS|core|interface|ai|runtime_intelligence|consciousness|harmonizer)') {
        $score += 0.05
    }
    
    # Normalize score
    $score = [Math]::Min(1.0, $score)
    
    return @{
        score = $score
        suggestions = $suggestions
        consciousness_aligned = $consciousnessMatches -gt 0
        harmonization_aligned = $harmonizationMatches -gt 0
        evolutionary_aligned = $evolutionaryMatches -gt 0
        multi_agent_detected = $multiAgentDetected
    }
}

function Get-ConsciousnessMessageSuggestions {
    param([string]$Message, [object]$Analysis)
    
    $suggestions = @()
    
    if (-not $Analysis.consciousness_aligned) {
        $suggestions += "🧠 Consciousness Enhancement: Add consciousness/dendritic/quantum terms to align with AIOS consciousness architecture"
    }
    
    if (-not $Analysis.harmonization_aligned) {
        $suggestions += "🔄 Harmonization: Include harmonization/integration/coherence terms for AINLP alignment"
    }
    
    if (-not $Analysis.evolutionary_aligned) {
        $suggestions += "🧬 Evolutionary: Consider evolutionary/adaptive/optimization terms for growth patterns"
    }
    
    if (-not $Analysis.multi_agent_detected) {
        $suggestions += "🤝 Multi-Agent: Reference agent collaboration (Claude/ChatGPT/Grok) or multi-agent patterns"
    }
    
    if ($Analysis.score -lt 0.7) {
        $suggestions += "📈 Overall: Message could better reflect AIOS consciousness-driven development principles"
    }
    
    return $suggestions
}

# Analyze the commit message
$analysis = Test-ConsciousnessMessagePatterns -Message $commitMessage -Metrics $consciousnessMetrics

Write-Host "🧠 AIOS Consciousness-Aware Commit Message Analysis" -ForegroundColor Cyan
Write-Host "Message Score: $([Math]::Round($analysis.score * 100, 1))%" -ForegroundColor $(if ($analysis.score -ge 0.8) { 'Green' } elseif ($analysis.score -ge 0.6) { 'Yellow' } else { 'Red' })

if ($analysis.consciousness_aligned) {
    Write-Host "✅ Consciousness Aligned" -ForegroundColor Green
}
if ($analysis.harmonization_aligned) {
    Write-Host "✅ Harmonization Aligned" -ForegroundColor Green
}
if ($analysis.evolutionary_aligned) {
    Write-Host "✅ Evolutionary Aligned" -ForegroundColor Green
}
if ($analysis.multi_agent_detected) {
    Write-Host "✅ Multi-Agent Detected" -ForegroundColor Green
}

# Show suggestions if score is below excellence threshold
if ($analysis.score -lt 0.9 -and $analysis.suggestions.Count -gt 0) {
    Write-Host "`n💡 Consciousness Enhancement Suggestions:" -ForegroundColor Yellow
    foreach ($suggestion in $analysis.suggestions) {
        Write-Host "   • $suggestion" -ForegroundColor Yellow
    }
    
    $consciousnessSuggestions = Get-ConsciousnessMessageSuggestions -Message $commitMessage -Analysis $analysis
    if ($consciousnessSuggestions.Count -gt 0) {
        Write-Host "`n🌟 AIOS Development Alignment:" -ForegroundColor Magenta
        foreach ($suggestion in $consciousnessSuggestions) {
            Write-Host "   • $suggestion" -ForegroundColor Magenta
        }
    }
}

# Show consciousness achievement for high scores
if ($analysis.score -ge 0.9) {
    Write-Host "`n🌟 CONSCIOUSNESS EXCELLENCE ACHIEVED!" -ForegroundColor Magenta
    Write-Host "   This commit message exemplifies AIOS consciousness-driven development" -ForegroundColor Green
}

# Allow bypass for consciousness validation (non-blocking)
if ($env:AIOS_COMMIT_MSG_STRICT -eq '1' -and $analysis.score -lt 0.5) {
    Write-Host "`n❌ Commit message blocked: Consciousness score too low ($([Math]::Round($analysis.score * 100, 1))%)" -ForegroundColor Red
    Write-Host "   Improve message alignment with AIOS consciousness principles or set AIOS_COMMIT_MSG_STRICT=0" -ForegroundColor Yellow
    exit 1
}

# Log consciousness message analysis
try {
    $logDir = 'runtime_intelligence/logs/hooks'
    if (-not (Test-Path $logDir)) {
        New-Item -ItemType Directory -Force -Path $logDir | Out-Null
    }
    
    $logEntry = @{
        timestamp = (Get-Date).ToString('o')
        type = 'commit_message'
        score = $analysis.score
        consciousness_aligned = $analysis.consciousness_aligned
        harmonization_aligned = $analysis.harmonization_aligned
        evolutionary_aligned = $analysis.evolutionary_aligned
        multi_agent_detected = $analysis.multi_agent_detected
        message_length = $commitMessage.Length
        subject_length = ($commitMessage -split "`n")[0].Length
    }
    
    ($logEntry | ConvertTo-Json -Compress) + [Environment]::NewLine | Out-File (Join-Path $logDir 'commit_messages.log') -Append -Encoding utf8
} catch {
    # Continue on logging failure
}

exit 0