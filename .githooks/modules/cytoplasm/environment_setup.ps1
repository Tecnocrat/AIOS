# AIOS GitHook Integration - Single Entry Point Creator
# ====================================================
# Creates the unified entry point for all GitHook logic execution
# Integrates with CYTOPLASM supercell architecture

param(
    [switch]$CreateSymlinks,
    [switch]$UpdateExistingHooks,
    [switch]$ShowIntegration
)

Write-Host " AIOS GITHOOK INTEGRATION SETUP" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# Find AIOS root
$AIOSRoot = $PSScriptRoot
while ($AIOSRoot -and $AIOSRoot -ne [System.IO.Path]::GetPathRoot($AIOSRoot)) {
    if (Test-Path (Join-Path $AIOSRoot "AIOS.sln")) {
        break
    }
    $AIOSRoot = Split-Path $AIOSRoot -Parent
}

if (-not $AIOSRoot) {
    Write-Host " AIOS root not found!" -ForegroundColor Red
    exit 1
}

Write-Host " AIOS Root: $AIOSRoot" -ForegroundColor Gray

$GitHooksPath = Join-Path $AIOSRoot ".githooks"
$CytoplasmOrchestrator = Join-Path $AIOSRoot "ai\cytoplasm\scripts\githook_orchestrator.ps1"

Write-Host " GitHooks Path: $GitHooksPath" -ForegroundColor Gray
Write-Host " CYTOPLASM Orchestrator: $CytoplasmOrchestrator" -ForegroundColor Gray
Write-Host ""

if (-not (Test-Path $CytoplasmOrchestrator)) {
    Write-Host " CYTOPLASM orchestrator not found!" -ForegroundColor Red
    exit 1
}

# Create the master entry point in .githooks
$MasterEntryPoint = Join-Path $GitHooksPath "execute_all_githook_logic.ps1"

Write-Host " Creating master entry point: execute_all_githook_logic.ps1" -ForegroundColor Yellow

$MasterScript = @"
# AIOS GitHook Logic - Single Entry Point
# =======================================
# This is the UNIQUE ENTRY POINT for all GitHook agentic optimization
# Integrates with CYTOPLASM supercell architecture

param(
    [switch]`$Parallel,
    [switch]`$SkipDependencies,
    [switch]`$ShowHelp
)

if (`$ShowHelp) {
    Write-Host " AIOS GITHOOK LOGIC - SINGLE ENTRY POINT" -ForegroundColor Cyan
    Write-Host "==========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "This is the UNIQUE entry point for executing ALL GitHook logic" -ForegroundColor Yellow
    Write-Host "through the AIOS supercell architecture." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "USAGE:" -ForegroundColor Green
    Write-Host "    .\execute_all_githook_logic.ps1           # Execute all hooks" -ForegroundColor White
    Write-Host "    .\execute_all_githook_logic.ps1 -Parallel # Parallel execution" -ForegroundColor White
    Write-Host "    .\execute_all_githook_logic.ps1 -ShowHelp # This help" -ForegroundColor White
    Write-Host ""
    Write-Host "SUPERCELL INTEGRATION:" -ForegroundColor Green
    Write-Host "     Delegates to CYTOPLASM supercell orchestrator" -ForegroundColor Gray
    Write-Host "     Coordinates with all AIOS supercells" -ForegroundColor Gray
    Write-Host "     Provides unified logging and reporting" -ForegroundColor Gray
    exit 0
}

Write-Host " AIOS GITHOOK LOGIC - SINGLE ENTRY POINT" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Delegate to CYTOPLASM supercell orchestrator
`$CytoplasmScript = "`$PSScriptRoot\..\ai\cytoplasm\scripts\githook_orchestrator.ps1"

if (Test-Path `$CytoplasmScript) {
    Write-Host " Delegating to CYTOPLASM supercell orchestrator..." -ForegroundColor Yellow
    
    `$Args = @()
    if (`$Parallel) { `$Args += "-Parallel" }
    if (`$SkipDependencies) { `$Args += "-SkipDependencies" }
    
    & `$CytoplasmScript @Args
    exit `$LASTEXITCODE
} else {
    Write-Host " CYTOPLASM orchestrator not found at: `$CytoplasmScript" -ForegroundColor Red
    Write-Host " Please ensure supercell architecture is properly initialized." -ForegroundColor Yellow
    exit 1
}
"@

$MasterScript | Out-File -FilePath $MasterEntryPoint -Encoding UTF8

Write-Host " Master entry point created: $MasterEntryPoint" -ForegroundColor Green

if ($CreateSymlinks) {
    Write-Host ""
    Write-Host " Creating symbolic links for easy access..." -ForegroundColor Yellow
    
    # Create shortcuts in common locations
    $RootShortcut = Join-Path $AIOSRoot "execute_all_githook_logic.ps1"
    
    try {
        New-Item -ItemType SymbolicLink -Path $RootShortcut -Target $MasterEntryPoint -Force -ErrorAction Stop
        Write-Host " Root shortcut created: $RootShortcut" -ForegroundColor Green
    } catch {
        Write-Host " Could not create root shortcut (may require admin privileges)" -ForegroundColor Yellow
    }
}

if ($UpdateExistingHooks) {
    Write-Host ""
    Write-Host " Updating existing git hooks to use supercell orchestrator..." -ForegroundColor Yellow
    
    $GitHookFiles = @("pre-commit", "commit-msg", "pre-push")
    
    foreach ($HookFile in $GitHookFiles) {
        $HookPath = Join-Path $GitHooksPath $HookFile
        if (Test-Path $HookPath) {
            # Backup original
            $BackupPath = "$HookPath.backup"
            Copy-Item $HookPath $BackupPath -Force
            
            # Create new hook that delegates to orchestrator
            $NewHookContent = @"
#!/bin/sh
# AIOS Git Hook - Supercell Integration
# Delegates to CYTOPLASM orchestrator

echo " AIOS Git Hook: Delegating to supercell orchestrator..."
exec "$PSScriptRoot/../ai/cytoplasm/scripts/githook_orchestrator.py" --hook-name="$HookFile" "`$@"
"@
            $NewHookContent | Out-File -FilePath $HookPath -Encoding UTF8
            Write-Host " Updated $HookFile (backup: $BackupPath)" -ForegroundColor Green
        }
    }
}

Write-Host ""
Write-Host " INTEGRATION COMPLETE!" -ForegroundColor Green
Write-Host "========================" -ForegroundColor Green
Write-Host ""
Write-Host "SINGLE ENTRY POINT CREATED:" -ForegroundColor Yellow
Write-Host "    File: execute_all_githook_logic.ps1" -ForegroundColor White
Write-Host "    Location: .githooks/" -ForegroundColor White
Write-Host "    Purpose: Execute ALL GitHook logic via supercell architecture" -ForegroundColor White
Write-Host ""
Write-Host "USAGE EXAMPLES:" -ForegroundColor Yellow
Write-Host "    cd .githooks && .\execute_all_githook_logic.ps1" -ForegroundColor Gray
Write-Host "    cd .githooks && .\execute_all_githook_logic.ps1 -Parallel" -ForegroundColor Gray
Write-Host "    cd .githooks && .\execute_all_githook_logic.ps1 -ShowHelp" -ForegroundColor Gray
Write-Host ""
Write-Host "SUPERCELL ARCHITECTURE:" -ForegroundColor Yellow
Write-Host "     CYTOPLASM: Orchestration and infrastructure" -ForegroundColor Green
Write-Host "     NUCLEUS: Core processing and runtime" -ForegroundColor Green
Write-Host "     TRANSPORT: Intercellular communication" -ForegroundColor Green
Write-Host "     MEMBRANE: External interfaces" -ForegroundColor Green
Write-Host ""

if ($ShowIntegration) {
    Write-Host " INTEGRATION ARCHITECTURE:" -ForegroundColor Cyan
    Write-Host "============================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "USER REQUEST: 'Execute all githook logic'" -ForegroundColor White
    Write-Host "    ↓" -ForegroundColor Gray
    Write-Host ".githooks/execute_all_githook_logic.ps1 (ENTRY POINT)" -ForegroundColor Yellow
    Write-Host "    ↓" -ForegroundColor Gray
    Write-Host "ai/cytoplasm/scripts/githook_orchestrator.ps1 (SUPERCELL)" -ForegroundColor Green
    Write-Host "    ↓" -ForegroundColor Gray
    Write-Host "ai/cytoplasm/scripts/githook_orchestrator.py (ORCHESTRATOR)" -ForegroundColor Green
    Write-Host "    ↓" -ForegroundColor Gray
    Write-Host "Individual .githooks/*.ps1 scripts (EXECUTION)" -ForegroundColor Blue
    Write-Host "    ↓" -ForegroundColor Gray
    Write-Host "Supercell synchronization and logging (INTEGRATION)" -ForegroundColor Magenta
    Write-Host ""
    Write-Host " No more script proliferation outside supercells!" -ForegroundColor Green
    Write-Host " Proper architecture compliance!" -ForegroundColor Green
    Write-Host " Single entry point for all GitHook logic!" -ForegroundColor Green
}

Write-Host ""
Write-Host " ARCHITECTURAL COMPLIANCE ACHIEVED!" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Green
Write-Host " GitHook orchestration moved to CYTOPLASM supercell" -ForegroundColor White
Write-Host " No more script proliferation in ROOT\scripts" -ForegroundColor White
Write-Host " Proper supercell integration and communication" -ForegroundColor White
Write-Host " Single entry point for agentic optimization" -ForegroundColor White