# AIOS GitHooks Comprehensive Test Suite
# =======================================
# Tests all supercell functions systematically

param(
    [switch]$TestNucleus,
    [switch]$TestMembrane,
    [switch]$TestCytoplasm,
    [switch]$TestTransport,
    [switch]$TestLaboratory,
    [switch]$TestInformationStorage,
    [switch]$TestAll,
    [switch]$DetailedOutput
)

if ($TestAll) {
    $TestNucleus = $true
    $TestMembrane = $true
    $TestCytoplasm = $true
    $TestTransport = $true
    $TestLaboratory = $true
    $TestInformationStorage = $true
}

Write-Host "🧪 AIOS GITHOOKS COMPREHENSIVE TEST SUITE" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Testing all supercell functions systematically" -ForegroundColor Gray
Write-Host ""

$GitHooksPath = $PSScriptRoot
$TestResults = @{}
$TotalTests = 0
$PassedTests = 0
$FailedTests = 0

function Test-Script {
    param(
        [string]$ScriptPath,
        [string]$TestName,
        [string[]]$Arguments = @(),
        [int]$TimeoutSeconds = 30
    )
    
    $global:TotalTests++
    
    Write-Host " Testing: $TestName" -ForegroundColor Yellow
    
    if (-not (Test-Path $ScriptPath)) {
        Write-Host " FAIL: Script not found - $ScriptPath" -ForegroundColor Red
        $global:FailedTests++
        return $false
    }
    
    try {
        $StartTime = Get-Date
        
        # Test if script can be loaded (syntax check)
        $ParseErrors = $null
        $ParsedScript = [System.Management.Automation.PSParser]::Tokenize((Get-Content $ScriptPath -Raw), [ref]$ParseErrors)
        
        if ($ParseErrors.Count -gt 0) {
            Write-Host " FAIL: Syntax errors found" -ForegroundColor Red
            if ($DetailedOutput) {
                foreach ($Error in $ParseErrors) {
                    Write-Host "    Error: $($Error.Content) at line $($Error.StartLine)" -ForegroundColor Red
                }
            }
            $global:FailedTests++
            return $false
        }
        
        # Test script execution with timeout
        $Job = Start-Job -ScriptBlock {
            param($Script, $Args)
            & $Script @Args
        } -ArgumentList $ScriptPath, $Arguments
        
        $JobResult = Wait-Job $Job -Timeout $TimeoutSeconds
        
        if ($JobResult) {
            $Output = Receive-Job $Job
            $ExitCode = $Job.State
            Stop-Job $Job -PassThru | Remove-Job
            
            $ExecutionTime = ((Get-Date) - $StartTime).TotalSeconds
            
            if ($ExitCode -eq "Completed") {
                Write-Host " PASS: $TestName ($([math]::Round($ExecutionTime, 2))s)" -ForegroundColor Green
                $global:PassedTests++
                return $true
            } else {
                Write-Host " FAIL: Script execution failed - $ExitCode" -ForegroundColor Red
                if ($DetailedOutput -and $Output) {
                    Write-Host "    Output: $($Output | Out-String)" -ForegroundColor Gray
                }
                $global:FailedTests++
                return $false
            }
        } else {
            Stop-Job $Job -PassThru | Remove-Job
            Write-Host " FAIL: Script timed out (${TimeoutSeconds}s)" -ForegroundColor Red
            $global:FailedTests++
            return $false
        }
        
    } catch {
        Write-Host " FAIL: Exception - $($_.Exception.Message)" -ForegroundColor Red
        $global:FailedTests++
        return $false
    }
}

function Test-FileExists {
    param(
        [string]$FilePath,
        [string]$TestName
    )
    
    $global:TotalTests++
    
    if (Test-Path $FilePath) {
        Write-Host " PASS: $TestName exists" -ForegroundColor Green
        $global:PassedTests++
        return $true
    } else {
        Write-Host " FAIL: $TestName not found - $FilePath" -ForegroundColor Red
        $global:FailedTests++
        return $false
    }
}

if ($TestNucleus) {
    Write-Host " TESTING NUCLEUS SUPERCELL" -ForegroundColor Magenta
    Write-Host "============================" -ForegroundColor Magenta
    Write-Host "Core git hook logic validation" -ForegroundColor Gray
    Write-Host ""
    
    $NucleusPath = Join-Path $GitHooksPath "supercells\nucleus"
    
    # Test core PowerShell hooks
    Test-Script (Join-Path $NucleusPath "pre-commit.ps1") "NUCLEUS: Pre-commit validation"
    Test-Script (Join-Path $NucleusPath "commit-msg.ps1") "NUCLEUS: Commit message validation" @("Test commit message")
    Test-Script (Join-Path $NucleusPath "pre-push.ps1") "NUCLEUS: Pre-push validation"
    
    # Test shell hook bridges
    Test-FileExists (Join-Path $NucleusPath "pre-commit") "NUCLEUS: Shell pre-commit bridge"
    Test-FileExists (Join-Path $NucleusPath "commit-msg") "NUCLEUS: Shell commit-msg bridge"
    Test-FileExists (Join-Path $NucleusPath "pre-push") "NUCLEUS: Shell pre-push bridge"
    
    Write-Host ""
}

if ($TestMembrane) {
    Write-Host " TESTING MEMBRANE SUPERCELL" -ForegroundColor Magenta
    Write-Host "=============================" -ForegroundColor Magenta
    Write-Host "External AI integrations validation" -ForegroundColor Gray
    Write-Host ""
    
    $MembranePath = Join-Path $GitHooksPath "supercells\membrane"
    
    # Test AI integration scripts
    Test-Script (Join-Path $MembranePath "aios_copilot_orchestrator.ps1") "MEMBRANE: GitHub Copilot integration"
    Test-Script (Join-Path $MembranePath "ai_integration_bridge.ps1") "MEMBRANE: AI integration bridge"
    Test-Script (Join-Path $MembranePath "external_tools.ps1") "MEMBRANE: External tools integration"
    Test-Script (Join-Path $MembranePath "aios_ainlp_integration.ps1") "MEMBRANE: AINLP integration"
    Test-Script (Join-Path $MembranePath "aios_consciousness_bridge.ps1") "MEMBRANE: Consciousness bridge"
    
    Write-Host ""
}

if ($TestCytoplasm) {
    Write-Host " TESTING CYTOPLASM SUPERCELL" -ForegroundColor Magenta
    Write-Host "==============================" -ForegroundColor Magenta
    Write-Host "Supporting infrastructure validation" -ForegroundColor Gray
    Write-Host ""
    
    $CytoplasmPath = Join-Path $GitHooksPath "supercells\cytoplasm"
    
    # Test infrastructure scripts
    Test-Script (Join-Path $CytoplasmPath "orchestration.ps1") "CYTOPLASM: Orchestration logic"
    Test-Script (Join-Path $CytoplasmPath "environment_setup.ps1") "CYTOPLASM: Environment setup"
    Test-Script (Join-Path $CytoplasmPath "auto_optimization.ps1") "CYTOPLASM: Auto-optimization" @() 60  # Longer timeout
    
    Write-Host ""
}

if ($TestTransport) {
    Write-Host " TESTING TRANSPORT SUPERCELL" -ForegroundColor Magenta
    Write-Host "==============================" -ForegroundColor Magenta
    Write-Host "Communication & coordination validation" -ForegroundColor Gray
    Write-Host ""
    
    $TransportPath = Join-Path $GitHooksPath "supercells\transport"
    
    # Test communication scripts
    Test-Script (Join-Path $TransportPath "supercell_bridge.ps1") "TRANSPORT: Supercell bridge"
    
    Write-Host ""
}

if ($TestLaboratory) {
    Write-Host " TESTING LABORATORY SUPERCELL" -ForegroundColor Magenta
    Write-Host "===============================" -ForegroundColor Magenta
    Write-Host "Analysis & experimentation validation" -ForegroundColor Gray
    Write-Host ""
    
    $LaboratoryPath = Join-Path $GitHooksPath "supercells\laboratory"
    
    # Test analysis scripts
    Test-Script (Join-Path $LaboratoryPath "comprehensive_analysis.ps1") "LABORATORY: Comprehensive analysis"
    Test-Script (Join-Path $LaboratoryPath "intelligence_reports.ps1") "LABORATORY: Intelligence reports"
    Test-Script (Join-Path $LaboratoryPath "optimization_analysis.ps1") "LABORATORY: Optimization analysis"
    Test-Script (Join-Path $LaboratoryPath "experimental_features.ps1") "LABORATORY: Experimental features"
    Test-Script (Join-Path $LaboratoryPath "real_ai_githook.ps1") "LABORATORY: Real AI GitHook"
    Test-Script (Join-Path $LaboratoryPath "real_vs_fake_ai_demo.ps1") "LABORATORY: Real vs Fake AI demo"
    Test-Script (Join-Path $LaboratoryPath "architecture_revolution_summary.ps1") "LABORATORY: Architecture summary"
    Test-Script (Join-Path $LaboratoryPath "hybrid_architecture_summary.ps1") "LABORATORY: Hybrid architecture"
    
    Write-Host ""
}

if ($TestInformationStorage) {
    Write-Host " TESTING INFORMATION_STORAGE SUPERCELL" -ForegroundColor Magenta
    Write-Host "========================================" -ForegroundColor Magenta
    Write-Host "Configuration & documentation validation" -ForegroundColor Gray
    Write-Host ""
    
    $InfoStoragePath = Join-Path $GitHooksPath "supercells\information_storage"
    
    # Test configuration files
    Test-FileExists (Join-Path $InfoStoragePath "config\consciousness_metrics.json") "INFO_STORAGE: Consciousness metrics config"
    Test-FileExists (Join-Path $InfoStoragePath "config\ai_visual_requirement.json") "INFO_STORAGE: AI visual requirements config"
    
    # Test documentation files
    Test-FileExists (Join-Path $InfoStoragePath "docs\ARCHITECTURE_REFERENCE.md") "INFO_STORAGE: Architecture reference"
    Test-FileExists (Join-Path $InfoStoragePath "docs\CHANGELOG.md") "INFO_STORAGE: Changelog"
    Test-FileExists (Join-Path $InfoStoragePath "docs\ENHANCEMENT_SUMMARY.md") "INFO_STORAGE: Enhancement summary"
    
    # Test legacy archive
    Test-FileExists (Join-Path $InfoStoragePath "legacy\archive") "INFO_STORAGE: Legacy archive directory"
    
    Write-Host ""
}

# Test main entry point functionality
Write-Host " TESTING MAIN ENTRY POINT" -ForegroundColor Magenta
Write-Host "============================" -ForegroundColor Magenta
Write-Host ""

Test-Script (Join-Path $GitHooksPath "execute_all_githook_logic.ps1") "MAIN: Help display" @("-ShowHelp")
Test-Script (Join-Path $GitHooksPath "execute_all_githook_logic.ps1") "MAIN: Supercell display" @("-ShowSupercells")

# Summary
Write-Host ""
Write-Host " TEST RESULTS SUMMARY" -ForegroundColor Cyan
Write-Host "=======================" -ForegroundColor Cyan
Write-Host "Total Tests: $TotalTests" -ForegroundColor White
Write-Host "Passed: $PassedTests" -ForegroundColor Green
Write-Host "Failed: $FailedTests" -ForegroundColor Red
Write-Host "Success Rate: $([math]::Round(($PassedTests / $TotalTests) * 100, 1))%" -ForegroundColor $(if ($FailedTests -eq 0) { "Green" } else { "Yellow" })
Write-Host ""

if ($FailedTests -eq 0) {
    Write-Host " ALL TESTS PASSED!" -ForegroundColor Green
    Write-Host "GitHooks supercell architecture is fully functional" -ForegroundColor Green
} else {
    Write-Host " SOME TESTS FAILED" -ForegroundColor Yellow
    Write-Host "Review failed tests and fix issues before deployment" -ForegroundColor Yellow
}

Write-Host ""
Write-Host " NEXT STEPS:" -ForegroundColor Yellow
if ($FailedTests -gt 0) {
    Write-Host "    1. Review failed tests with -DetailedOutput" -ForegroundColor Gray
    Write-Host "    2. Fix syntax errors and missing files" -ForegroundColor Gray
    Write-Host "    3. Re-run tests until all pass" -ForegroundColor Gray
} else {
    Write-Host "    1. Deploy GitHooks system to production" -ForegroundColor Gray
    Write-Host "    2. Monitor execution in real workflows" -ForegroundColor Gray
    Write-Host "    3. Collect performance metrics" -ForegroundColor Gray
}

exit $(if ($FailedTests -eq 0) { 0 } else { 1 })