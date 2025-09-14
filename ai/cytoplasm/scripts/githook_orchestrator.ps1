# AIOS GitHook Master Orchestrator - PowerShell Entry Point
# ==========================================================
# Integrated with CYTOPLASM supercell architecture
# Purpose: Windows-native entry point for complete GitHook execution

param(
    [switch]$Parallel,
    [switch]$SkipDependencies,
    [string]$AIOSRoot = "",
    [switch]$ShowHelp
)

if ($ShowHelp) {
    Write-Host "🧬 AIOS GitHook Master Orchestrator" -ForegroundColor Cyan
    Write-Host "=====================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "SYNOPSIS:" -ForegroundColor Yellow
    Write-Host "    Executes all GitHook logic through the CYTOPLASM supercell architecture" -ForegroundColor White
    Write-Host ""
    Write-Host "PARAMETERS:" -ForegroundColor Yellow
    Write-Host "    -Parallel         Execute independent hooks in parallel" -ForegroundColor White
    Write-Host "    -SkipDependencies Skip dependency checks (use with caution)" -ForegroundColor White
    Write-Host "    -AIOSRoot         Specify AIOS root directory" -ForegroundColor White
    Write-Host "    -ShowHelp         Show this help message" -ForegroundColor White
    Write-Host ""
    Write-Host "EXAMPLES:" -ForegroundColor Yellow
    Write-Host "    .\githook_orchestrator.ps1" -ForegroundColor Gray
    Write-Host "    .\githook_orchestrator.ps1 -Parallel" -ForegroundColor Gray
    Write-Host "    .\githook_orchestrator.ps1 -SkipDependencies" -ForegroundColor Gray
    Write-Host ""
    Write-Host "SUPERCELL INTEGRATION:" -ForegroundColor Yellow
    Write-Host "    🧬 CYTOPLASM: Orchestration and logging" -ForegroundColor Green
    Write-Host "    🧬 NUCLEUS: Core runtime notification" -ForegroundColor Green
    Write-Host "    🧬 TRANSPORT: Intercellular communication" -ForegroundColor Green
    Write-Host "    🧬 MEMBRANE: External interface coordination" -ForegroundColor Green
    exit 0
}

Write-Host "🧬 AIOS GITHOOK MASTER ORCHESTRATOR" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "🎯 EXECUTING ALL GITHOOK LOGIC VIA SUPERCELL ARCHITECTURE" -ForegroundColor Yellow
Write-Host ""

# Find AIOS root if not provided
if (-not $AIOSRoot) {
    $CurrentPath = $PSScriptRoot
    while ($CurrentPath -and $CurrentPath -ne [System.IO.Path]::GetPathRoot($CurrentPath)) {
        if (Test-Path (Join-Path $CurrentPath "AIOS.sln")) {
            $AIOSRoot = $CurrentPath
            break
        }
        $CurrentPath = Split-Path $CurrentPath -Parent
    }
    
    if (-not $AIOSRoot) {
        Write-Host "❌ AIOS root not found. Please specify -AIOSRoot parameter." -ForegroundColor Red
        exit 1
    }
}

Write-Host "📂 AIOS Root: $AIOSRoot" -ForegroundColor Gray

# Path to CYTOPLASM orchestrator
$CytoplasmOrchestrator = Join-Path $AIOSRoot "ai\cytoplasm\scripts\githook_orchestrator.py"

if (Test-Path $CytoplasmOrchestrator) {
    Write-Host "✅ Found CYTOPLASM orchestrator: $CytoplasmOrchestrator" -ForegroundColor Green
    Write-Host ""
    
    # Build Python command arguments
    $PythonArgs = @($CytoplasmOrchestrator)
    
    if ($Parallel) {
        $PythonArgs += "--parallel"
        Write-Host "⚡ Parallel execution ENABLED" -ForegroundColor Yellow
    }
    
    if ($SkipDependencies) {
        $PythonArgs += "--skip-deps"
        Write-Host "⚠️ Dependency checks DISABLED" -ForegroundColor Yellow
    }
    
    $PythonArgs += "--aios-root"
    $PythonArgs += $AIOSRoot
    
    Write-Host ""
    Write-Host "🚀 Executing complete GitHook logic via supercell architecture..." -ForegroundColor Cyan
    Write-Host ""
    
    # Execute with proper environment
    $env:AIOS_ROOT = $AIOSRoot
    $env:AIOS_HOOK_ORCHESTRATED = "true"
    $env:PYTHONPATH = "$AIOSRoot\ai"
    
    try {
        # Change to AIOS root for execution
        Push-Location $AIOSRoot
        
        # Execute Python orchestrator
        $Process = Start-Process -FilePath "python" -ArgumentList $PythonArgs -Wait -PassThru -NoNewWindow
        
        $ExitCode = $Process.ExitCode
        
        Pop-Location
        
        Write-Host ""
        if ($ExitCode -eq 0) {
            Write-Host "✅ GitHook orchestration completed successfully!" -ForegroundColor Green
        } else {
            Write-Host "❌ GitHook orchestration completed with errors (Exit Code: $ExitCode)" -ForegroundColor Red
        }
        
        Write-Host ""
        Write-Host "📊 Check logs in: ai\cytoplasm\runtime\logs\githooks\" -ForegroundColor Gray
        
        exit $ExitCode
        
    } catch {
        Write-Host ""
        Write-Host "❌ Failed to execute CYTOPLASM orchestrator: $($_.Exception.Message)" -ForegroundColor Red
        exit 1
    }
    
} else {
    Write-Host "❌ CYTOPLASM orchestrator not found at: $CytoplasmOrchestrator" -ForegroundColor Red
    Write-Host ""
    Write-Host "🔧 ATTEMPTING LEGACY EXECUTION..." -ForegroundColor Yellow
    
    # Fallback to individual PowerShell script execution
    $GitHooksPath = Join-Path $AIOSRoot ".githooks"
    
    if (Test-Path $GitHooksPath) {
        Write-Host "📂 Found .githooks directory: $GitHooksPath" -ForegroundColor Gray
        
        $LegacyHooks = @(
            "pre-commit.ps1",
            "commit-msg.ps1",
            "pre-push.ps1",
            "aios_copilot_orchestrator.ps1",
            "aios_auto_optimization.ps1"
        )
        
        $SuccessfulHooks = 0
        $FailedHooks = 0
        
        foreach ($Hook in $LegacyHooks) {
            $HookPath = Join-Path $GitHooksPath $Hook
            if (Test-Path $HookPath) {
                Write-Host ""
                Write-Host "🔧 Executing legacy hook: $Hook" -ForegroundColor Yellow
                
                try {
                    $HookProcess = Start-Process -FilePath "pwsh" -ArgumentList @("-ExecutionPolicy", "Bypass", "-File", $HookPath) -Wait -PassThru -NoNewWindow -WorkingDirectory $AIOSRoot
                    
                    if ($HookProcess.ExitCode -eq 0) {
                        Write-Host "✅ $Hook completed successfully" -ForegroundColor Green
                        $SuccessfulHooks++
                    } else {
                        Write-Host "❌ $Hook failed (Exit Code: $($HookProcess.ExitCode))" -ForegroundColor Red
                        $FailedHooks++
                    }
                } catch {
                    Write-Host "❌ $Hook execution error: $($_.Exception.Message)" -ForegroundColor Red
                    $FailedHooks++
                }
            } else {
                Write-Host "⚠️ Hook not found: $Hook" -ForegroundColor Yellow
            }
        }
        
        Write-Host ""
        Write-Host "📊 Legacy Execution Summary:" -ForegroundColor Cyan
        Write-Host "    Successful: $SuccessfulHooks" -ForegroundColor Green
        Write-Host "    Failed: $FailedHooks" -ForegroundColor Red
        
        exit $(if ($FailedHooks -gt 0) { 1 } else { 0 })
        
    } else {
        Write-Host "❌ .githooks directory not found at: $GitHooksPath" -ForegroundColor Red
        Write-Host ""
        Write-Host "🏗️ RECOMMENDATION: Initialize supercell architecture!" -ForegroundColor Yellow
        exit 1
    }
}

Write-Host ""
Write-Host "🧬 Supercell Architecture Information:" -ForegroundColor Cyan
Write-Host "    CYTOPLASM: Supporting infrastructure and orchestration" -ForegroundColor Gray
Write-Host "    NUCLEUS: Central control and core processing" -ForegroundColor Gray  
Write-Host "    TRANSPORT: Intercellular communication and data flow" -ForegroundColor Gray
Write-Host "    MEMBRANE: External interfaces and integration" -ForegroundColor Gray
Write-Host "    LABORATORY: Research, testing, and experimental features" -ForegroundColor Gray
Write-Host "    INFORMATION_STORAGE: Documentation and persistent data" -ForegroundColor Gray