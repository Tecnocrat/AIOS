# AIOS GitHook Logic - Single Entry Point
# =======================================
# This is the UNIQUE ENTRY POINT for all GitHook agentic optimization
# Integrates with CYTOPLASM supercell architecture

param(
    [switch]$Parallel,
    [switch]$SkipDependencies,
    [switch]$ShowHelp
)

if ($ShowHelp) {
    Write-Host "🎯 AIOS GITHOOK LOGIC - SINGLE ENTRY POINT" -ForegroundColor Cyan
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
    Write-Host "    🧬 Delegates to CYTOPLASM supercell orchestrator" -ForegroundColor Gray
    Write-Host "    🧬 Coordinates with all AIOS supercells" -ForegroundColor Gray
    Write-Host "    🧬 Provides unified logging and reporting" -ForegroundColor Gray
    exit 0
}

Write-Host "🎯 AIOS GITHOOK LOGIC - SINGLE ENTRY POINT" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Delegate to CYTOPLASM supercell orchestrator
$CytoplasmScript = "$PSScriptRoot\..\ai\cytoplasm\scripts\githook_orchestrator.ps1"

if (Test-Path $CytoplasmScript) {
    Write-Host "🧬 Delegating to CYTOPLASM supercell orchestrator..." -ForegroundColor Yellow
    
    $Args = @()
    if ($Parallel) { $Args += "-Parallel" }
    if ($SkipDependencies) { $Args += "-SkipDependencies" }
    
    & $CytoplasmScript @Args
    exit $LASTEXITCODE
} else {
    Write-Host "❌ CYTOPLASM orchestrator not found at: $CytoplasmScript" -ForegroundColor Red
    Write-Host "🔧 Please ensure supercell architecture is properly initialized." -ForegroundColor Yellow
    exit 1
}
