#!/usr/bin/env pwsh
<#
.SYNOPSIS
    OpenRouter API Key Setup Helper for AIOS

.DESCRIPTION
    Guides user through OpenRouter API key configuration and validates setup.
    Handles both temporary (session) and persistent (user profile) setup.

.EXAMPLE
    .\setup_openrouter_key.ps1
#>

Write-Host ""
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 68) -ForegroundColor Cyan
Write-Host "  OpenRouter API Key Setup for AIOS" -ForegroundColor Cyan
Write-Host ("=" * 70) -ForegroundColor Cyan
Write-Host ""

# Check current key status
Write-Host "📋 Step 1: Checking current configuration..." -ForegroundColor Yellow
Write-Host ""

$currentKey = $env:OPENROUTER_API_KEY

if ($currentKey) {
    Write-Host "  Current key found:" -ForegroundColor Green
    Write-Host "    Length: $($currentKey.Length) chars"
    Write-Host "    Prefix: $($currentKey.Substring(0, [Math]::Min(15, $currentKey.Length)))..."
    Write-Host ""
    
    # Test current key
    Write-Host "  Testing current key..." -ForegroundColor Yellow
    $testResult = python test_openrouter_key.py 2>&1
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✅ Current key is VALID - no action needed!" -ForegroundColor Green
        Write-Host ""
        exit 0
    } else {
        Write-Host "  ❌ Current key is INVALID" -ForegroundColor Red
        Write-Host ""
    }
} else {
    Write-Host "  ⚠️  No key found in environment" -ForegroundColor Yellow
    Write-Host ""
}

# Guide to get new key
Write-Host "🔑 Step 2: Get your OpenRouter API key" -ForegroundColor Yellow
Write-Host ""
Write-Host "  1. Open browser to: " -NoNewline
Write-Host "https://openrouter.ai/settings/keys" -ForegroundColor Cyan
Write-Host "  2. Sign in (or create free account)"
Write-Host "  3. Click " -NoNewline
Write-Host "'Create Key'" -ForegroundColor Green -NoNewline
Write-Host " button"
Write-Host "  4. Give it a name (e.g., 'AIOS E501 Fixer')"
Write-Host "  5. Set credit limit (optional, $5 default is fine)"
Write-Host "  6. Copy the generated key (starts with 'sk-or-v1-...')"
Write-Host ""

# Prompt for key
Write-Host "📝 Step 3: Enter your new API key" -ForegroundColor Yellow
Write-Host ""
Write-Host "  Paste your key here (it won't be displayed): " -NoNewline -ForegroundColor Cyan
$newKey = Read-Host -AsSecureString
$newKeyPlain = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto(
    [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($newKey)
)

if ([string]::IsNullOrWhiteSpace($newKeyPlain)) {
    Write-Host ""
    Write-Host "❌ No key provided. Exiting." -ForegroundColor Red
    exit 1
}

# Validate format
Write-Host ""
Write-Host "🔍 Step 4: Validating key format..." -ForegroundColor Yellow
Write-Host ""

if (-not $newKeyPlain.StartsWith("sk-or-v1-")) {
    Write-Host "  ❌ Invalid key format" -ForegroundColor Red
    Write-Host "     OpenRouter keys should start with 'sk-or-v1-'" -ForegroundColor Red
    Write-Host "     Your key starts with: $($newKeyPlain.Substring(0, [Math]::Min(10, $newKeyPlain.Length)))..." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  Double-check you copied the full key from OpenRouter." -ForegroundColor Yellow
    exit 1
}

Write-Host "  ✅ Key format looks correct" -ForegroundColor Green
Write-Host "     Length: $($newKeyPlain.Length) characters"
Write-Host "     Prefix: $($newKeyPlain.Substring(0, 15))..."
Write-Host ""

# Set environment variable (session-level)
Write-Host "⚙️  Step 5: Setting environment variable..." -ForegroundColor Yellow
Write-Host ""

$env:OPENROUTER_API_KEY = $newKeyPlain
Write-Host "  ✅ Set for current PowerShell session" -ForegroundColor Green
Write-Host ""

# Test the new key
Write-Host "🧪 Step 6: Testing API key..." -ForegroundColor Yellow
Write-Host ""

$testResult = python test_openrouter_key.py 2>&1
$testExitCode = $LASTEXITCODE

if ($testExitCode -eq 0) {
    Write-Host ""
    Write-Host "🎉 SUCCESS! OpenRouter API key is configured and working!" -ForegroundColor Green
    Write-Host ""
    
    # Offer to make it persistent
    Write-Host "💾 Step 7: Make key persistent (optional)" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  Current setup is SESSION-ONLY (lost when you close PowerShell)" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  Would you like to save it to your PowerShell profile?" -ForegroundColor Cyan
    Write-Host "  (This will automatically load it in future sessions)" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  Save to profile? [Y/n]: " -NoNewline -ForegroundColor Cyan
    $response = Read-Host
    
    if ($response -eq "" -or $response -eq "Y" -or $response -eq "y") {
        # Add to PowerShell profile
        $profilePath = $PROFILE.CurrentUserAllHosts
        $profileDir = Split-Path $profilePath
        
        # Create profile directory if it doesn't exist
        if (-not (Test-Path $profileDir)) {
            New-Item -ItemType Directory -Path $profileDir -Force | Out-Null
        }
        
        # Check if key already in profile
        $keyLine = "`$env:OPENROUTER_API_KEY = '$newKeyPlain'"
        
        if (Test-Path $profilePath) {
            $profileContent = Get-Content $profilePath -Raw
            if ($profileContent -match "OPENROUTER_API_KEY") {
                Write-Host ""
                Write-Host "  ⚠️  Profile already contains OPENROUTER_API_KEY" -ForegroundColor Yellow
                Write-Host "     Profile: $profilePath" -ForegroundColor Yellow
                Write-Host ""
                Write-Host "  Please manually update the key in your profile file." -ForegroundColor Yellow
            } else {
                Add-Content -Path $profilePath -Value "`n# OpenRouter API Key for AIOS"
                Add-Content -Path $profilePath -Value $keyLine
                Write-Host ""
                Write-Host "  ✅ Added to profile: $profilePath" -ForegroundColor Green
                Write-Host "     Key will load automatically in new PowerShell sessions" -ForegroundColor Green
            }
        } else {
            Set-Content -Path $profilePath -Value "# PowerShell Profile"
            Add-Content -Path $profilePath -Value "`n# OpenRouter API Key for AIOS"
            Add-Content -Path $profilePath -Value $keyLine
            Write-Host ""
            Write-Host "  ✅ Created profile: $profilePath" -ForegroundColor Green
            Write-Host "     Key will load automatically in new PowerShell sessions" -ForegroundColor Green
        }
    } else {
        Write-Host ""
        Write-Host "  Skipped profile update. Remember to set the key each session:" -ForegroundColor Yellow
        Write-Host "    `$env:OPENROUTER_API_KEY = 'your-key-here'" -ForegroundColor Cyan
    }
    
    Write-Host ""
    Write-Host "=" -NoNewline -ForegroundColor Green
    Write-Host ("=" * 68) -ForegroundColor Green
    Write-Host "  Setup Complete! You can now use OpenRouter-powered tools." -ForegroundColor Green
    Write-Host ("=" * 70) -ForegroundColor Green
    Write-Host ""
    
    exit 0
} else {
    Write-Host ""
    Write-Host "❌ API key validation FAILED" -ForegroundColor Red
    Write-Host ""
    Write-Host "  The key you entered appears invalid or the OpenRouter service" -ForegroundColor Red
    Write-Host "  is having issues. Please:" -ForegroundColor Red
    Write-Host ""
    Write-Host "  1. Double-check you copied the FULL key from OpenRouter" -ForegroundColor Yellow
    Write-Host "  2. Ensure your OpenRouter account is active" -ForegroundColor Yellow
    Write-Host "  3. Try generating a new key at:" -ForegroundColor Yellow
    Write-Host "     https://openrouter.ai/settings/keys" -ForegroundColor Cyan
    Write-Host "  4. Run this script again" -ForegroundColor Yellow
    Write-Host ""
    
    exit 1
}
