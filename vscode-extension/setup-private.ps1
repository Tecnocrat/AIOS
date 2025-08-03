# AIOS VSCode Extension - Private Use Setup Script
# This script configures the AIOS extension for private/local use only

param(
    [switch]$Install,
    [switch]$Configure,
    [switch]$Test,
    [switch]$All
)

# Colors for output
$Red = [System.ConsoleColor]::Red
$Green = [System.ConsoleColor]::Green
$Yellow = [System.ConsoleColor]::Yellow
$Blue = [System.ConsoleColor]::Blue

function Write-ColorOutput($Message, $Color) {
    $originalColor = $Host.UI.RawUI.ForegroundColor
    $Host.UI.RawUI.ForegroundColor = $Color
    Write-Host $Message
    $Host.UI.RawUI.ForegroundColor = $originalColor
}

function Test-VSCodeInstalled {
    try {
        $null = Get-Command code -ErrorAction Stop
        return $true
    } catch {
        return $false
    }
}

function Install-AIOSExtension {
    Write-ColorOutput "🔧 Installing AIOS VSCode Extension..." $Blue

    if (-not (Test-VSCodeInstalled)) {
        Write-ColorOutput "❌ VSCode not found in PATH. Please install VSCode first." $Red
        return $false
    }

    $vsixPath = "c:\dev\AIOS\vscode-extension\aios-vscode-0.4.0.vsix"

    if (-not (Test-Path $vsixPath)) {
        Write-ColorOutput "❌ VSIX file not found at: $vsixPath" $Red
        return $false
    }

    Write-ColorOutput "📦 Installing from VSIX: $vsixPath" $Yellow

    try {
        # Uninstall existing version if present
        & code --uninstall-extension tecnocrat.aios-vscode 2>$null

        # Install new version
        & code --install-extension $vsixPath

        Write-ColorOutput "✅ Extension installed successfully!" $Green
        return $true
    } catch {
        Write-ColorOutput "❌ Failed to install extension: $($_.Exception.Message)" $Red
        return $false
    }
}

function Set-PrivateSettings {
    Write-ColorOutput "🔧 Configuring private use settings..." $Blue

    # Get VSCode settings file path
    $settingsPath = "$env:APPDATA\Code\User\settings.json"

    if (-not (Test-Path $settingsPath)) {
        Write-ColorOutput "📝 Creating new settings file..." $Yellow
        New-Item -Path $settingsPath -ItemType File -Force | Out-Null
        Set-Content -Path $settingsPath -Value "{}"
    }

    # Read current settings
    $currentSettings = Get-Content -Path $settingsPath -Raw | ConvertFrom-Json -AsHashtable

    # Add AIOS private settings
    $aiosSettings = @{
        "aios.core.enabled"                              = $true
        "aios.context.persistAcrossRestarts"             = $true
        "aios.context.maxHistorySize"                    = 1000
        "aios.ai.pythonPath"                             = "c:/dev/AIOS/ai/src"
        "aios.ai.corePath"                               = "c:/dev/AIOS/core"
        "aios.debug.enabled"                             = $false
        "aios.privacy.mode"                              = "strict"
        "aios.network.enabled"                           = $false
        "aios.telemetry.enabled"                         = $false
        "aios.autoUpdate.enabled"                        = $false
        "aios.marketplace.checkUpdates"                  = $false
        "aios.logs.retention"                            = "session-only"
        "aios.context.encryption"                        = $true
        "aios.debug.traceLevel"                          = "error-only"
        "telemetry.telemetryLevel"                       = "off"
        "workbench.settings.enableNaturalLanguageSearch" = $false
    }

    # Merge settings
    foreach ($key in $aiosSettings.Keys) {
        $currentSettings[$key] = $aiosSettings[$key]
    }

    # Save settings
    try {
        $currentSettings | ConvertTo-Json -Depth 10 | Set-Content -Path $settingsPath
        Write-ColorOutput "✅ Private settings configured successfully!" $Green
        return $true
    } catch {
        Write-ColorOutput "❌ Failed to configure settings: $($_.Exception.Message)" $Red
        return $false
    }
}

function Test-PrivateConfiguration {
    Write-ColorOutput "🧪 Testing private configuration..." $Blue

    # Test VSCode can find extension
    Write-ColorOutput "📋 Checking installed extensions..." $Yellow
    $extensions = & code --list-extensions

    if ($extensions -like "*aios-vscode*") {
        Write-ColorOutput "✅ AIOS extension found in installed extensions" $Green
    } else {
        Write-ColorOutput "❌ AIOS extension not found in installed extensions" $Red
        return $false
    }

    # Test settings file
    $settingsPath = "$env:APPDATA\Code\User\settings.json"

    if (Test-Path $settingsPath) {
        $settings = Get-Content -Path $settingsPath -Raw | ConvertFrom-Json

        if ($settings."aios.core.enabled" -eq $true) {
            Write-ColorOutput "✅ AIOS core enabled in settings" $Green
        } else {
            Write-ColorOutput "❌ AIOS core not enabled in settings" $Red
            return $false
        }

        if ($settings."aios.privacy.mode" -eq "strict") {
            Write-ColorOutput "✅ Privacy mode set to strict" $Green
        } else {
            Write-ColorOutput "❌ Privacy mode not configured" $Red
            return $false
        }

        if ($settings."telemetry.telemetryLevel" -eq "off") {
            Write-ColorOutput "✅ Telemetry disabled" $Green
        } else {
            Write-ColorOutput "❌ Telemetry not disabled" $Red
            return $false
        }
    } else {
        Write-ColorOutput "❌ Settings file not found" $Red
        return $false
    }

    Write-ColorOutput "✅ All private configuration tests passed!" $Green
    return $true
}

function Show-Usage {
    Write-ColorOutput @"
🔒 AIOS VSCode Extension - Private Use Setup

Usage:
  .\setup-private.ps1 -Install      # Install extension from VSIX
  .\setup-private.ps1 -Configure    # Configure private settings
  .\setup-private.ps1 -Test         # Test private configuration
  .\setup-private.ps1 -All          # Do all steps

Examples:
  .\setup-private.ps1 -All          # Complete private setup
  .\setup-private.ps1 -Install      # Just install extension
  .\setup-private.ps1 -Configure    # Just configure settings

"@ $Blue
}

# Main execution
if ($All) {
    Write-ColorOutput "🚀 Starting complete private setup..." $Blue

    $success = $true
    $success = $success -and (Install-AIOSExtension)
    $success = $success -and (Set-PrivateSettings)
    $success = $success -and (Test-PrivateConfiguration)

    if ($success) {
        Write-ColorOutput @"

🎉 AIOS VSCode Extension - Private Setup Complete!

✅ Extension installed locally
✅ Private settings configured
✅ All tests passed

🔒 Your extension is now configured for private use only:
   - No external connections
   - Local data storage only
   - Privacy mode enabled
   - Telemetry disabled

🚀 Next steps:
   1. Restart VSCode
   2. Open any project
   3. Press F1 and type 'AIOS'
   4. Start using @aios in chat

"@ $Green
    } else {
        Write-ColorOutput "❌ Setup incomplete. Please check errors above." $Red
    }
} elseif ($Install) {
    Install-AIOSExtension
} elseif ($Configure) {
    Set-PrivateSettings
} elseif ($Test) {
    Test-PrivateConfiguration
} else {
    Show-Usage
}
