#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Configure DeepSeek API key for hierarchical E501 pipeline
    
.DESCRIPTION
    Helps configure DEEPSEEK_API_KEY environment variable for three-tier
    hierarchical intelligence pipeline. Supports session and permanent config.
    
.PARAMETER ApiKey
    Your DeepSeek API key (starts with sk-)
    
.PARAMETER Permanent
    Set as permanent user environment variable (recommended)
    
.PARAMETER Verify
    Verify configuration and test agent readiness
    
.EXAMPLE
    .\configure_deepseek_key.ps1 -ApiKey "sk-your-key" -Permanent
    
.EXAMPLE
    .\configure_deepseek_key.ps1 -Verify
#>

param(
    [Parameter(Mandatory=$false)]
    [string]$ApiKey,
    
    [Parameter(Mandatory=$false)]
    [switch]$Permanent,
    
    [Parameter(Mandatory=$false)]
    [switch]$Verify
)

Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "DEEPSEEK API KEY CONFIGURATION" -ForegroundColor Cyan
Write-Host "Hierarchical Three-Tier Pipeline (OLLAMA→GEMINI→DEEPSEEK)" -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Cyan

# Verify mode: Check current configuration
if ($Verify) {
    Write-Host "`n🔍 Verifying DeepSeek Configuration..." -ForegroundColor Yellow
    
    # Check environment variable
    $currentKey = $env:DEEPSEEK_API_KEY
    if ($currentKey) {
        $masked = $currentKey.Substring(0, 8) + "*" * ($currentKey.Length - 8)
        Write-Host "✅ Session variable set: $masked" -ForegroundColor Green
    } else {
        Write-Host "❌ Session variable not set" -ForegroundColor Red
    }
    
    # Check permanent variable (user scope)
    $permanentKey = [System.Environment]::GetEnvironmentVariable(
        'DEEPSEEK_API_KEY',
        [System.EnvironmentVariableTarget]::User
    )
    if ($permanentKey) {
        $masked = $permanentKey.Substring(0, 8) + "*" * ($permanentKey.Length - 8)
        Write-Host "✅ Permanent variable set: $masked" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Permanent variable not set (optional)" -ForegroundColor Yellow
    }
    
    # Test agent readiness
    Write-Host "`n🧪 Testing Agent Readiness..." -ForegroundColor Yellow
    $scriptDir = Split-Path -Parent $PSCommandPath
    $validatorPath = Join-Path (Split-Path -Parent $scriptDir) "tools\dendritic_config_agent.py"
    
    if (Test-Path $validatorPath) {
        try {
            $result = python $validatorPath --validate-multiagent 2>&1 | ConvertFrom-Json
            
            Write-Host "`n📊 Agent Status:" -ForegroundColor Cyan
            Write-Host "   Readiness Level: $($result.readiness_level)" -ForegroundColor $(
                if ($result.readiness_level -eq 1.0) { "Green" } else { "Yellow" }
            )
            
            foreach ($agent in $result.agents_available.PSObject.Properties) {
                $status = if ($agent.Value) { "✅" } else { "❌" }
                $color = if ($agent.Value) { "Green" } else { "Red" }
                Write-Host "   $status $($agent.Name): $($agent.Value)" -ForegroundColor $color
            }
            
            if ($result.readiness_level -eq 1.0) {
                Write-Host "`n🌟 All agents operational! Ready for hierarchical pipeline." -ForegroundColor Green
            } else {
                Write-Host "`n⚠️  Some agents unavailable. Check configuration." -ForegroundColor Yellow
            }
        } catch {
            Write-Host "❌ Failed to validate agents: $_" -ForegroundColor Red
        }
    } else {
        Write-Host "⚠️  Validator not found: $validatorPath" -ForegroundColor Yellow
    }
    
    exit
}

# Configuration mode: Set API key
if (-not $ApiKey) {
    Write-Host "`n❌ No API key provided!" -ForegroundColor Red
    Write-Host "`nUsage:" -ForegroundColor Yellow
    Write-Host "  .\configure_deepseek_key.ps1 -ApiKey 'sk-your-key' -Permanent"
    Write-Host "`nOr verify current configuration:"
    Write-Host "  .\configure_deepseek_key.ps1 -Verify"
    exit 1
}

# Validate API key format
if (-not $ApiKey.StartsWith("sk-")) {
    Write-Host "`n⚠️  Warning: API key doesn't start with 'sk-'" -ForegroundColor Yellow
    Write-Host "DeepSeek API keys typically start with 'sk-'" -ForegroundColor Yellow
    $continue = Read-Host "Continue anyway? (y/n)"
    if ($continue -ne "y") {
        Write-Host "❌ Configuration cancelled" -ForegroundColor Red
        exit 1
    }
}

Write-Host "`n📝 Configuration Details:" -ForegroundColor Cyan
$masked = $ApiKey.Substring(0, 8) + "*" * ($ApiKey.Length - 8)
Write-Host "   API Key: $masked"
Write-Host "   Scope: $(if ($Permanent) { 'Permanent (User)' } else { 'Session Only' })"

# Set session variable
$env:DEEPSEEK_API_KEY = $ApiKey
Write-Host "`n✅ Session variable set" -ForegroundColor Green

# Set permanent variable if requested
if ($Permanent) {
    try {
        [System.Environment]::SetEnvironmentVariable(
            'DEEPSEEK_API_KEY',
            $ApiKey,
            [System.EnvironmentVariableTarget]::User
        )
        Write-Host "✅ Permanent variable set (User scope)" -ForegroundColor Green
        Write-Host "   Variable will persist after reboot" -ForegroundColor Gray
    } catch {
        Write-Host "❌ Failed to set permanent variable: $_" -ForegroundColor Red
        Write-Host "   Session variable is still active for current shell" -ForegroundColor Yellow
    }
}

# Test configuration
Write-Host "`n🧪 Testing Configuration..." -ForegroundColor Yellow

try {
    $testUrl = "https://api.deepseek.com/v1/models"
    $headers = @{
        "Authorization" = "Bearer $ApiKey"
    }
    
    $response = Invoke-RestMethod -Uri $testUrl -Headers $headers -Method Get -TimeoutSec 10
    Write-Host "✅ DeepSeek API connection successful!" -ForegroundColor Green
    Write-Host "   Available models: $($response.data.Count)" -ForegroundColor Gray
} catch {
    Write-Host "⚠️  API connection test failed: $($_.Exception.Message)" -ForegroundColor Yellow
    Write-Host "   Key is set, but verify it's valid at https://platform.deepseek.com" -ForegroundColor Gray
}

Write-Host "`n🎯 Next Steps:" -ForegroundColor Cyan
Write-Host "   1. Verify configuration: .\configure_deepseek_key.ps1 -Verify"
Write-Host "   2. Test hierarchical pipeline: python tools\test_hierarchical_pipeline.py"
Write-Host "   3. Run E501 fixer: python tools\agentic_e501_fixer.py <file> --fix"

Write-Host "`n🌟 Hierarchical pipeline ready!" -ForegroundColor Green
Write-Host "   Tier 1: OLLAMA (Context Manager)" -ForegroundColor Gray
Write-Host "   Tier 2: GEMINI (Code Generator)" -ForegroundColor Gray
Write-Host "   Tier 3: DEEPSEEK (Quality Validator) ✅" -ForegroundColor Green
