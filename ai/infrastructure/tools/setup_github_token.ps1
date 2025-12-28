#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Setup GitHub token for AIOS persistent use
.DESCRIPTION
    Stores GitHub token securely in user config directory and sets environment variable
    Token persists across sessions via PowerShell profile integration
#>

param(
    [Parameter(Mandatory=$false)]
    [string]$Token
)

$ErrorActionPreference = "Stop"

# AIOS config directory
$configDir = "$env:USERPROFILE\.aios"
$tokenFile = Join-Path $configDir "github_token.txt"
$profilePath = $PROFILE

Write-Host "=================================" -ForegroundColor Cyan
Write-Host "AIOS GitHub Token Setup" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""

# Create config directory
if (-not (Test-Path $configDir)) {
    New-Item -ItemType Directory -Path $configDir -Force | Out-Null
    Write-Host "✓ Created config directory: $configDir" -ForegroundColor Green
}

# Get token from parameter or prompt
if (-not $Token) {
    Write-Host "Please paste your GitHub token (40 chars, starts with ghp_):" -ForegroundColor Yellow
    Write-Host "Get it from: https://github.com/settings/tokens" -ForegroundColor Gray
    Write-Host "Required scope: 'repo' for GitHub Models API access" -ForegroundColor Gray
    Write-Host ""
    $Token = Read-Host "Token"
}

# Validate token format
if ($Token -notmatch '^ghp_[a-zA-Z0-9]{36}$') {
    Write-Host "✗ Invalid token format. Expected: ghp_XXXX... (40 chars total)" -ForegroundColor Red
    exit 1
}

# Save token to file
$Token | Out-File -FilePath $tokenFile -Encoding utf8 -NoNewline
Write-Host "✓ Token saved to: $tokenFile" -ForegroundColor Green

# Set environment variable for current session
$env:GITHUB_TOKEN = $Token
Write-Host "✓ Environment variable set for current session" -ForegroundColor Green

# Add to PowerShell profile for persistence
$profileInit = @"

# AIOS GitHub Token Auto-Load
if (Test-Path "$tokenFile") {
    `$env:GITHUB_TOKEN = Get-Content "$tokenFile" -Raw
}
"@

if (Test-Path $profilePath) {
    $profileContent = Get-Content $profilePath -Raw
    if ($profileContent -notlike "*AIOS GitHub Token Auto-Load*") {
        Add-Content -Path $profilePath -Value $profileInit
        Write-Host "✓ Added token auto-load to PowerShell profile" -ForegroundColor Green
    } else {
        Write-Host "✓ Token auto-load already in PowerShell profile" -ForegroundColor Green
    }
} else {
    New-Item -Path $profilePath -ItemType File -Force | Out-Null
    Set-Content -Path $profilePath -Value $profileInit
    Write-Host "✓ Created PowerShell profile with token auto-load" -ForegroundColor Green
}

# Test token
Write-Host ""
Write-Host "Testing token..." -ForegroundColor Yellow

try {
    $response = Invoke-RestMethod -Uri "https://models.inference.ai.azure.com/models" `
        -Headers @{
            "Authorization" = "Bearer $Token"
            "Content-Type" = "application/json"
        } `
        -Method Get
    
    $modelCount = $response.data.Count
    Write-Host "✓ Token valid! Access to $modelCount GitHub Models (GPT-4o, GPT-4o-mini, etc.)" -ForegroundColor Green
} catch {
    Write-Host "✗ Token test failed: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "  Check token scopes at: https://github.com/settings/tokens" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "=================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Token location: $tokenFile"
Write-Host "Profile updated: $profilePath"
Write-Host "Current session: GITHUB_TOKEN set"
Write-Host "Future sessions: Auto-loaded from profile"
Write-Host ""
Write-Host "Ready to use GitHub Models API with AIOS!" -ForegroundColor Green
