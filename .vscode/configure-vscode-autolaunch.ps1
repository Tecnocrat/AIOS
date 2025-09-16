# AIOS VS Code Auto-Launch Configuration Script
# STRICT NO EMOTICON POLICY ENFORCED
# This script configures VS Code to automatically open the AIOS workspace

param(
    [switch]$Install,
    [switch]$Configure,
    [switch]$CreateShortcut
)

Write-Host "[AIOS] VS Code Auto-Launch Configuration" -ForegroundColor Cyan
Write-Host "[POLICY] Professional workspace optimization" -ForegroundColor Green

# AIOS workspace path
$workspacePath = "C:\dev\AIOS\AIOS.code-workspace"
$aiosRoot = "C:\dev\AIOS"

# Verify AIOS workspace exists
if (-not (Test-Path $workspacePath)) {
    Write-Host "[ERROR] AIOS workspace not found: $workspacePath" -ForegroundColor Red
    exit 1
}

function Set-VSCodeDefaultWorkspace {
    Write-Host "[CONFIG] Setting VS Code default workspace to AIOS"
    
    # VS Code user settings directory
    $vscodeUserDir = "$env:APPDATA\Code\User"
    $userSettingsPath = "$vscodeUserDir\settings.json"
    
    # Create user settings directory if it doesn't exist
    if (-not (Test-Path $vscodeUserDir)) {
        New-Item -ItemType Directory -Path $vscodeUserDir -Force | Out-Null
    }
    
    # Default user settings for AIOS
    $userSettings = @{
        "window.restoreWindows" = "one"
        "workbench.startupEditor" = "none"
        "window.reopenFolders" = "all"
        "window.openFilesInNewWindow" = "off"
        "window.openFoldersInNewWindow" = "on"
        "window.newWindowDimensions" = "maximized"
        "workbench.welcomePage.walkthroughs.openOnInstall" = $false
        "workbench.welcome.enabled" = $false
        "powershell.cwd" = $aiosRoot
        "terminal.integrated.defaultLocation" = "editor"
        "terminal.integrated.cwd" = $aiosRoot
    }
    
    # Read existing settings if they exist
    $existingSettings = @{}
    if (Test-Path $userSettingsPath) {
        try {
            $existingContent = Get-Content $userSettingsPath -Raw
            $existingSettings = $existingContent | ConvertFrom-Json -AsHashtable
        }
        catch {
            Write-Host "[WARNING] Could not parse existing user settings, creating new file" -ForegroundColor Yellow
        }
    }
    
    # Merge settings
    foreach ($key in $userSettings.Keys) {
        $existingSettings[$key] = $userSettings[$key]
    }
    
    # Write updated settings
    $existingSettings | ConvertTo-Json -Depth 10 | Set-Content $userSettingsPath -Encoding UTF8
    Write-Host "[SUCCESS] VS Code user settings updated" -ForegroundColor Green
}

function New-AIOSShortcut {
    Write-Host "[CONFIG] Creating AIOS workspace shortcut"
    
    $shortcutPath = "$env:USERPROFILE\Desktop\AIOS Workspace.lnk"
    $vscodeExe = Get-Command code -ErrorAction SilentlyContinue
    
    if (-not $vscodeExe) {
        Write-Host "[ERROR] VS Code not found in PATH" -ForegroundColor Red
        return $false
    }
    
    # Create shortcut using WScript.Shell
    $shell = New-Object -ComObject WScript.Shell
    $shortcut = $shell.CreateShortcut($shortcutPath)
    $shortcut.TargetPath = $vscodeExe.Source
    $shortcut.Arguments = "`"$workspacePath`""
    $shortcut.WorkingDirectory = $aiosRoot
    $shortcut.Description = "AIOS Development Workspace"
    $shortcut.IconLocation = $vscodeExe.Source
    $shortcut.Save()
    
    Write-Host "[SUCCESS] Desktop shortcut created: $shortcutPath" -ForegroundColor Green
    return $true
}

function Set-PowerShellStartupLocation {
    Write-Host "[CONFIG] Configuring PowerShell startup location"
    
    # PowerShell profile path
    $profilePath = $PROFILE.CurrentUserAllHosts
    $profileDir = Split-Path $profilePath -Parent
    
    # Create profile directory if it doesn't exist
    if (-not (Test-Path $profileDir)) {
        New-Item -ItemType Directory -Path $profileDir -Force | Out-Null
    }
    
    # AIOS startup configuration
    $startupConfig = @"

# AIOS Development Environment Auto-Configuration
if (Test-Path 'C:\dev\AIOS') {
    if ((Get-Location).Path -eq $env:USERPROFILE -or (Get-Location).Path -eq 'C:\Windows\System32') {
        Set-Location 'C:\dev\AIOS'
        Write-Host '[AIOS] Workspace ready: C:\dev\AIOS' -ForegroundColor Green
    }
}

"@

    # Add to profile if not already present
    $profileContent = ""
    if (Test-Path $profilePath) {
        $profileContent = Get-Content $profilePath -Raw
    }
    
    if ($profileContent -notlike "*AIOS Development Environment Auto-Configuration*") {
        Add-Content -Path $profilePath -Value $startupConfig
        Write-Host "[SUCCESS] PowerShell profile updated" -ForegroundColor Green
    } else {
        Write-Host "[INFO] PowerShell profile already configured" -ForegroundColor Yellow
    }
}

function New-BatchLauncher {
    Write-Host "[CONFIG] Creating AIOS batch launcher"
    
    $batchPath = "$aiosRoot\launch-aios-workspace.bat"
    $batchContent = @"
@echo off
REM AIOS Workspace Launcher
REM STRICT NO EMOTICON POLICY ENFORCED

echo [AIOS] Launching development workspace
echo [POLICY] Professional development environment

REM Change to AIOS directory
cd /d "C:\dev\AIOS"

REM Launch VS Code with AIOS workspace
code "C:\dev\AIOS\AIOS.code-workspace"

echo [SUCCESS] AIOS workspace launched
pause
"@

    Set-Content -Path $batchPath -Value $batchContent -Encoding ASCII
    Write-Host "[SUCCESS] Batch launcher created: $batchPath" -ForegroundColor Green
}

function Test-AIOSConfiguration {
    Write-Host "[TEST] Verifying AIOS configuration"
    
    $tests = @(
        @{ Name = "AIOS Directory"; Path = $aiosRoot; Type = "Directory" },
        @{ Name = "AIOS Workspace"; Path = $workspacePath; Type = "File" },
        @{ Name = "VS Code Executable"; Command = "code"; Type = "Command" }
    )
    
    $allPassed = $true
    
    foreach ($test in $tests) {
        Write-Host "  Testing $($test.Name)..." -NoNewline
        
        $passed = $false
        switch ($test.Type) {
            "Directory" { $passed = Test-Path $test.Path -PathType Container }
            "File" { $passed = Test-Path $test.Path -PathType Leaf }
            "Command" { $passed = $null -ne (Get-Command $test.Command -ErrorAction SilentlyContinue) }
        }
        
        if ($passed) {
            Write-Host " PASS" -ForegroundColor Green
        } else {
            Write-Host " FAIL" -ForegroundColor Red
            $allPassed = $false
        }
    }
    
    return $allPassed
}

# Main execution
if ($Install -or $Configure) {
    if (-not (Test-AIOSConfiguration)) {
        Write-Host "[ERROR] AIOS configuration test failed" -ForegroundColor Red
        exit 1
    }
    
    Set-VSCodeDefaultWorkspace
    Set-PowerShellStartupLocation
    New-BatchLauncher
    
    if ($CreateShortcut) {
        New-AIOSShortcut
    }
    
    Write-Host "`n[SUCCESS] AIOS VS Code auto-launch configuration completed" -ForegroundColor Green
    Write-Host "[INFO] Restart VS Code to apply changes" -ForegroundColor Cyan
    Write-Host "[INFO] Use 'launch-aios-workspace.bat' for direct workspace launch" -ForegroundColor Cyan
}
elseif ($CreateShortcut) {
    New-AIOSShortcut
}
else {
    Write-Host "Usage: .\configure-vscode-autolaunch.ps1 [-Install] [-Configure] [-CreateShortcut]"
    Write-Host ""
    Write-Host "Options:"
    Write-Host "  -Install        Configure VS Code and PowerShell for AIOS auto-launch"
    Write-Host "  -Configure      Same as -Install (alias)"
    Write-Host "  -CreateShortcut Create desktop shortcut for AIOS workspace"
    Write-Host ""
    Write-Host "Examples:"
    Write-Host "  .\configure-vscode-autolaunch.ps1 -Install -CreateShortcut"
    Write-Host "  .\configure-vscode-autolaunch.ps1 -Configure"
}