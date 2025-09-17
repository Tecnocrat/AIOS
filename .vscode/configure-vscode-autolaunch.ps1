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
    Write-Host "[CONFIG] VS Code settings configured for workspace only (no global modifications)"
    
    # AIOS operates entirely within its workspace - no global VSCode settings modified
    # All configuration is contained within the workspace .vscode/settings.json
    
    $workspaceVscodeDir = "$aiosRoot\.vscode"
    $workspaceSettingsPath = "$workspaceVscodeDir\settings.json"
    
    # Ensure workspace .vscode directory exists
    if (-not (Test-Path $workspaceVscodeDir)) {
        New-Item -ItemType Directory -Path $workspaceVscodeDir -Force | Out-Null
    }
    
    # Verify workspace settings exist (they should already be committed)
    if (Test-Path $workspaceSettingsPath) {
        Write-Host "[SUCCESS] Workspace settings configured - no global modifications needed" -ForegroundColor Green
        return $true
    }
    else {
        Write-Host "[WARNING] Workspace settings not found at $workspaceSettingsPath" -ForegroundColor Yellow
        return $false
    }
}


function New-AIOSWorkspaceLauncher {
    Write-Host "[CONFIG] Creating workspace-contained launcher (no desktop shortcuts)"
    
    # SECURITY: AIOS creates NO files outside C:\dev\AIOS workspace
    # No desktop shortcuts, no user directory modifications
    
    $workspaceLauncher = "$aiosRoot\launch-aios.bat"
    $launcherContent = @"
@echo off
REM AIOS Workspace Launcher - Contained within C:\dev\AIOS only
echo [AIOS] Launching workspace from C:\dev\AIOS
code "%~dp0AIOS.code-workspace"
"@
    
    Set-Content -Path $workspaceLauncher -Value $launcherContent
    Write-Host "[SUCCESS] Workspace launcher created: $workspaceLauncher" -ForegroundColor Green
    Write-Host "[SECURITY] No external files created - workspace contained" -ForegroundColor Green
    return $true
}

function Set-PowerShellStartupLocation {
    Write-Host "[CONFIG] AIOS workspace-only configuration (no external profile modification)"
    
    # SECURITY: AIOS NEVER modifies user PowerShell profiles or personal directories
    # All configuration is contained within C:\dev\AIOS workspace only
    
    Write-Host "[SECURITY] AIOS respects user privacy - no profile modifications" -ForegroundColor Green
    Write-Host "[INFO] Use 'cd C:\dev\AIOS' manually or workspace shortcuts" -ForegroundColor Yellow
    
    # Create workspace-local startup script instead
    $workspaceStartup = "$aiosRoot\.vscode\workspace-startup.ps1"
    $startupConfig = @"
# AIOS Workspace-Local Startup Script
# This script runs only when explicitly called from within AIOS workspace

Write-Host '[AIOS] Workspace startup script executed' -ForegroundColor Green
Write-Host '[LOCATION] Current directory: C:\dev\AIOS' -ForegroundColor Cyan

# Verify we're in the correct workspace
if ((Get-Location).Path -ne 'C:\dev\AIOS') {
    Write-Warning '[AIOS] Not in AIOS workspace directory'
    Write-Host '[SUGGESTION] Navigate to C:\dev\AIOS manually' -ForegroundColor Yellow
}
"@

    Set-Content -Path $workspaceStartup -Value $startupConfig
    Write-Host "[SUCCESS] Workspace-local startup script created: $workspaceStartup" -ForegroundColor Green
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
        New-AIOSWorkspaceLauncher
    }
    
    Write-Host "`n[SUCCESS] AIOS VS Code auto-launch configuration completed" -ForegroundColor Green
    Write-Host "[INFO] Restart VS Code to apply changes" -ForegroundColor Cyan
    Write-Host "[INFO] Use 'launch-aios-workspace.bat' for direct workspace launch" -ForegroundColor Cyan
    Write-Host "[SECURITY] All configuration contained within C:\dev\AIOS workspace" -ForegroundColor Green
}
elseif ($CreateShortcut) {
    New-AIOSWorkspaceLauncher
}
else {
    Write-Host "Usage: .\configure-vscode-autolaunch.ps1 [-Install] [-Configure] [-CreateShortcut]"
    Write-Host ""
    Write-Host "Options:"
    Write-Host "  -Install        Configure VS Code workspace (no global modifications)"
    Write-Host "  -Configure      Same as -Install (alias)"
    Write-Host "  -CreateShortcut Create workspace launcher (no desktop shortcuts)"
    Write-Host ""
    Write-Host "Examples:"
    Write-Host "  .\configure-vscode-autolaunch.ps1 -Install -CreateShortcut"
    Write-Host "  .\configure-vscode-autolaunch.ps1 -Configure"
    Write-Host ""
    Write-Host "SECURITY: AIOS creates NO files outside C:\dev\AIOS workspace"
}