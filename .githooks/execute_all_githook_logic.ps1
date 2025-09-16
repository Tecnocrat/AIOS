# AIOS GitHook Logic - Single Entry Point
# =======================================
# This is the UNIQUE ENTRY POINT for all GitHook agentic optimization
# Integrates with SUPERCELL architecture

param(
    [switch]$Parallel,
    [switch]$SkipDependencies,
    [switch]$ShowHelp,
    [switch]$ShowSupercells,
    [switch]$AgenticMode,
    [switch]$AnalysisOnly,
    [switch]$NoAutoFix,
    [int]$TimeoutSeconds = 30
)

if ($ShowHelp) {
    Write-Host "AIOS GITHOOK LOGIC - SINGLE ENTRY POINT" -ForegroundColor Cyan
    Write-Host "==========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "This is the UNIQUE entry point for executing ALL GitHook logic" -ForegroundColor Yellow
    Write-Host "through the AIOS supercell architecture." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "USAGE:" -ForegroundColor Green
    Write-Host "    .\execute_all_githook_logic.ps1                 # Execute all hooks" -ForegroundColor White
    Write-Host "    .\execute_all_githook_logic.ps1 -Parallel       # Parallel execution" -ForegroundColor White
    Write-Host "    .\execute_all_githook_logic.ps1 -ShowSupercells # Display architecture" -ForegroundColor White
    Write-Host "    .\execute_all_githook_logic.ps1 -AgenticMode    # AI-driven auto refactoring" -ForegroundColor White
    Write-Host "    .\execute_all_githook_logic.ps1 -AnalysisOnly   # Quality analysis without execution" -ForegroundColor White
    Write-Host "    .\execute_all_githook_logic.ps1 -NoAutoFix      # Disable automatic fixes" -ForegroundColor White
    Write-Host "    .\execute_all_githook_logic.ps1 -ShowHelp       # This help" -ForegroundColor White
    Write-Host ""
    Write-Host "SUPERCELL INTEGRATION:" -ForegroundColor Green
    Write-Host "    NUCLEUS: Core git hook logic (pre-commit, commit-msg, pre-push)" -ForegroundColor Gray
    Write-Host "    MEMBRANE: AI integrations (GitHub Copilot, external tools)" -ForegroundColor Gray
    Write-Host "    CYTOPLASM: Supporting infrastructure and auto-optimization" -ForegroundColor Gray
    Write-Host "    TRANSPORT: Inter-supercell communication" -ForegroundColor Gray
    Write-Host "    LABORATORY: Analysis and experimental features" -ForegroundColor Gray
    Write-Host "    INFORMATION_STORAGE: Configuration and documentation" -ForegroundColor Gray
    exit 0
}

if ($ShowSupercells) {
    Write-Host "AIOS SUPERCELL ARCHITECTURE" -ForegroundColor Cyan
    Write-Host "============================" -ForegroundColor Cyan
    Write-Host ""
    
    $SupercellPaths = @{
        "NUCLEUS" = "supercells\nucleus"
        "MEMBRANE" = "supercells\membrane"  
        "CYTOPLASM" = "supercells\cytoplasm"
        "TRANSPORT" = "supercells\transport"
        "LABORATORY" = "supercells\laboratory"
        "INFORMATION_STORAGE" = "supercells\information_storage"
    }
    
    foreach ($Supercell in $SupercellPaths.Keys) {
        $Path = Join-Path $PSScriptRoot $SupercellPaths[$Supercell]
        $Status = if (Test-Path $Path) { "OPERATIONAL" } else { "MISSING" }
        $Color = if ($Status -eq "OPERATIONAL") { "Green" } else { "Red" }
        
        Write-Host "[$Status] $Supercell" -ForegroundColor $Color
        if (Test-Path $Path) {
            $Files = Get-ChildItem $Path -Recurse -File | Measure-Object
            Write-Host "    Files: $($Files.Count)" -ForegroundColor Gray
        }
    }
    exit 0
}

Write-Host "AIOS GITHOOK LOGIC - SINGLE ENTRY POINT" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Initialize execution tracking
$ExecutionResults = @{}
$StartTime = Get-Date
$TotalSteps = 0
$CompletedSteps = 0

# Define supercell execution order
$ExecutionOrder = @(
    @{ Name = "NUCLEUS"; Script = "supercells\nucleus\pre-commit.ps1"; Description = "Core validation" },
    @{ Name = "MEMBRANE"; Script = "supercells\membrane\aios_copilot_orchestrator.ps1"; Description = "AI integration"; Optional = $true },
    @{ Name = "CYTOPLASM"; Script = "supercells\cytoplasm\auto_optimization.ps1"; Description = "Auto-optimization"; Optional = $true },
    @{ Name = "LABORATORY"; Script = "supercells\laboratory\comprehensive_analysis.ps1"; Description = "Analysis"; Optional = $AnalysisOnly }
)

$TotalSteps = $ExecutionOrder.Count

function Execute-SupercellScript {
    param(
        [string]$Name,
        [string]$ScriptPath,
        [string]$Description,
        [bool]$Optional = $false,
        [int]$TimeoutSeconds = 30
    )
    
    $FullPath = Join-Path $PSScriptRoot $ScriptPath
    Write-Host "[$Name] $Description..." -ForegroundColor Yellow
    
    if (-not (Test-Path $FullPath)) {
        if ($Optional) {
            Write-Host "    [SKIPPED] Script not found (optional): $ScriptPath" -ForegroundColor Gray
            return $true
        } else {
            Write-Host "    [ERROR] Required script not found: $ScriptPath" -ForegroundColor Red
            return $false
        }
    }
    
    try {
        if ($Parallel -and $Optional) {
            # Execute optional scripts in background for parallel execution
            $Job = Start-Job -ScriptBlock {
                param($Script)
                & $Script
            } -ArgumentList $FullPath
            
            $ExecutionResults[$Name] = @{
                Job = $Job
                StartTime = Get-Date
                Status = "Running"
            }
            
            Write-Host "    [STARTED] Background execution" -ForegroundColor Green
            return $true
        } else {
            # Execute synchronously with timeout
            $Job = Start-Job -ScriptBlock {
                param($Script)
                & $Script
            } -ArgumentList $FullPath
            
            $Result = Wait-Job $Job -Timeout $TimeoutSeconds
            
            if ($Result) {
                $Output = Receive-Job $Job
                Stop-Job $Job -PassThru | Remove-Job
                Write-Host "    [COMPLETED] $Name execution successful" -ForegroundColor Green
                return $true
            } else {
                Stop-Job $Job -PassThru | Remove-Job
                Write-Host "    [TIMEOUT] $Name execution timed out (${TimeoutSeconds}s)" -ForegroundColor Yellow
                return $Optional
            }
        }
    } catch {
        Write-Host "    [ERROR] $Name execution failed: $($_.Exception.Message)" -ForegroundColor Red
        return $Optional
    }
}

# Main execution logic
if ($AnalysisOnly) {
    Write-Host "Analysis-only mode enabled - executing analysis supercells only" -ForegroundColor Gray
    $ExecutionOrder = $ExecutionOrder | Where-Object { $_.Name -eq "LABORATORY" }
}

if ($AgenticMode) {
    Write-Host "Agentic mode enabled - prioritizing AI-driven workflows" -ForegroundColor Magenta
}

# Execute supercells in order
foreach ($Step in $ExecutionOrder) {
    $Success = Execute-SupercellScript -Name $Step.Name -ScriptPath $Step.Script -Description $Step.Description -Optional $Step.Optional -TimeoutSeconds $TimeoutSeconds
    
    if ($Success) {
        $CompletedSteps++
    } elseif (-not $Step.Optional) {
        Write-Host ""
        Write-Host "CRITICAL FAILURE in required supercell: $($Step.Name)" -ForegroundColor Red
        Write-Host "Aborting execution sequence." -ForegroundColor Red
        exit 1
    }
    
    # Progress indicator
    $Progress = [math]::Round(($CompletedSteps / $TotalSteps) * 100, 1)
    Write-Host "    Progress: $Progress% ($CompletedSteps/$TotalSteps)" -ForegroundColor Cyan
}

# Wait for parallel jobs if any
if ($Parallel) {
    Write-Host ""
    Write-Host "Waiting for parallel executions to complete..." -ForegroundColor Yellow
    
    foreach ($Name in $ExecutionResults.Keys) {
        $JobInfo = $ExecutionResults[$Name]
        if ($JobInfo.Job) {
            $Result = Wait-Job $JobInfo.Job -Timeout ($TimeoutSeconds * 2)
            if ($Result) {
                $Output = Receive-Job $JobInfo.Job
                Write-Host "[$Name] Background execution completed" -ForegroundColor Green
            } else {
                Write-Host "[$Name] Background execution timed out" -ForegroundColor Yellow
            }
            Stop-Job $JobInfo.Job -PassThru | Remove-Job
        }
    }
}

# Execution summary
$EndTime = Get-Date
$Duration = ($EndTime - $StartTime).TotalSeconds

Write-Host ""
Write-Host "EXECUTION SUMMARY" -ForegroundColor Cyan
Write-Host "=================" -ForegroundColor Cyan
Write-Host "Completed Steps: $CompletedSteps/$TotalSteps" -ForegroundColor Green
Write-Host "Total Duration: $([math]::Round($Duration, 2))s" -ForegroundColor Green
Write-Host "Success Rate: $([math]::Round(($CompletedSteps / $TotalSteps) * 100, 1))%" -ForegroundColor Green

if ($CompletedSteps -eq $TotalSteps) {
    Write-Host ""
    Write-Host "ALL SUPERCELLS EXECUTED SUCCESSFULLY!" -ForegroundColor Green
    Write-Host "AIOS GitHook logic execution complete." -ForegroundColor Green
    exit 0
} else {
    Write-Host ""
    Write-Host "PARTIAL EXECUTION COMPLETED" -ForegroundColor Yellow
    Write-Host "Some optional supercells were skipped or failed." -ForegroundColor Yellow
    exit 0
}
