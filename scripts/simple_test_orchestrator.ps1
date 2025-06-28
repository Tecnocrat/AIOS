# Simple AIOS Test Script
# PowerShell script for basic AIOS testing without Unicode characters

param(
    [string]$Phase = "all",
    [switch]$Verbose
)

$AIosRoot = "c:\dev\AIOS"
$BuildPath = "$AIosRoot\orchestrator\build"

function Write-TestStatus {
    param([string]$Message, [string]$Status = "INFO")
    
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $statusChar = switch ($Status) {
        "SUCCESS" { "[OK]" }
        "ERROR" { "[ERROR]" }
        "WARN" { "[WARN]" }
        default { "[INFO]" }
    }
    
    Write-Host "$timestamp $statusChar $Message"
}

function Test-BuildValidation {
    Write-TestStatus "Starting build validation..." "INFO"
    
    # Navigate to build directory
    if (!(Test-Path $BuildPath)) {
        New-Item -ItemType Directory -Path $BuildPath -Force
    }
    
    Push-Location $BuildPath
    
    try {
        # Clean previous build
        Get-ChildItem . -Include "*.exe", "*.pdb", "CMakeCache.txt" | Remove-Item -Force -ErrorAction SilentlyContinue
        Write-TestStatus "Build artifacts cleaned" "SUCCESS"
        
        # Configure with CMake
        Write-TestStatus "Running CMake configuration..." "INFO"
        $cmakeOutput = cmake .. -DCMAKE_BUILD_TYPE=Debug 2>&1
        
        if ($LASTEXITCODE -eq 0) {
            Write-TestStatus "CMake configuration successful" "SUCCESS"
            
            # Build the project
            Write-TestStatus "Building AIOS kernel..." "INFO"
            $buildOutput = cmake --build . --target aios_kernel --config Debug 2>&1
            
            if ($LASTEXITCODE -eq 0) {
                Write-TestStatus "Build successful" "SUCCESS"
                
                # Check for executable
                $debugExe = "Debug\aios_kernel.exe"
                $releaseExe = "Release\aios_kernel.exe"
                
                if ((Test-Path $debugExe) -or (Test-Path $releaseExe)) {
                    $exePath = if (Test-Path $debugExe) { $debugExe } else { $releaseExe }
                    Write-TestStatus "Executable found: $exePath" "SUCCESS"
                    return @{ "status" = "success"; "executable" = $exePath }
                } else {
                    Write-TestStatus "No executable found after build" "ERROR"
                    return @{ "status" = "failed"; "error" = "No executable found" }
                }
            } else {
                Write-TestStatus "Build failed" "ERROR"
                Write-Host "Build output:" $buildOutput
                return @{ "status" = "failed"; "error" = "Build failed" }
            }
        } else {
            Write-TestStatus "CMake configuration failed" "ERROR"
            Write-Host "CMake output:" $cmakeOutput
            return @{ "status" = "failed"; "error" = "CMake failed" }
        }
    }
    finally {
        Pop-Location
    }
}

function Test-ExecutionBasic {
    param([string]$ExecutablePath)
    
    Write-TestStatus "Starting basic execution test..." "INFO"
    
    if (!(Test-Path $ExecutablePath)) {
        Write-TestStatus "Executable not found: $ExecutablePath" "ERROR"
        return @{ "status" = "failed"; "error" = "Executable not found" }
    }
    
    Push-Location (Split-Path $ExecutablePath -Parent)
    
    try {
        Write-TestStatus "Running AIOS kernel..." "INFO"
        
        # Run with timeout
        $job = Start-Job -ScriptBlock {
            param($exe)
            & $exe
        } -ArgumentList (Split-Path $ExecutablePath -Leaf)
        
        if (Wait-Job $job -Timeout 30) {
            $output = Receive-Job $job
            Write-TestStatus "Execution completed" "SUCCESS"
            
            # Check for consciousness indicators
            $indicators = @(
                "consciousness",
                "quantum coherence", 
                "recursive",
                "universal"
            )
            
            $foundCount = 0
            foreach ($indicator in $indicators) {
                if ($output -match $indicator) {
                    $foundCount++
                }
            }
            
            Write-TestStatus "Found $foundCount/$($indicators.Count) consciousness indicators" "INFO"
            
            return @{ 
                "status" = "success"; 
                "indicators_found" = $foundCount;
                "total_indicators" = $indicators.Count
            }
        } else {
            Stop-Job $job
            Write-TestStatus "Execution timed out" "WARN"
            return @{ "status" = "timeout"; "error" = "Execution timed out" }
        }
        
        Remove-Job $job -Force
    }
    catch {
        Write-TestStatus "Execution error: $($_.Exception.Message)" "ERROR"
        return @{ "status" = "error"; "error" = $_.Exception.Message }
    }
    finally {
        Pop-Location
    }
}

function Test-ArchiveValidation {
    Write-TestStatus "Validating archive generation..." "INFO"
    
    $archivePath = "$AIosRoot\orchestrator\archive"
    
    if (Test-Path $archivePath) {
        $logFiles = Get-ChildItem $archivePath -Filter "*.log"
        $jsonFiles = Get-ChildItem $archivePath -Filter "*.json"
        
        Write-TestStatus "Found $($logFiles.Count) log files and $($jsonFiles.Count) diagnostic files" "INFO"
        
        return @{
            "status" = "success";
            "log_files" = $logFiles.Count;
            "diagnostic_files" = $jsonFiles.Count
        }
    } else {
        Write-TestStatus "Archive directory not found" "WARN"
        return @{ "status" = "not_found"; "error" = "Archive directory missing" }
    }
}

# Main execution
Write-Host ""
Write-Host "==============================================="
Write-Host "AIOS Simple Test Orchestrator"
Write-Host "==============================================="
Write-Host ""

$results = @{}

# Phase 1: Build Validation
if ($Phase -eq "all" -or $Phase -eq "1") {
    Write-Host "--- PHASE 1: Build Validation ---"
    $buildResult = Test-BuildValidation
    $results["build"] = $buildResult
    
    if ($buildResult.status -eq "success") {
        # Phase 2: Basic Execution Test
        if ($Phase -eq "all" -or $Phase -eq "2") {
            Write-Host ""
            Write-Host "--- PHASE 2: Basic Execution Test ---"
            $exePath = "$BuildPath\$($buildResult.executable)"
            $execResult = Test-ExecutionBasic $exePath
            $results["execution"] = $execResult
        }
    } else {
        Write-TestStatus "Skipping execution test due to build failure" "WARN"
        $results["execution"] = @{ "status" = "skipped"; "reason" = "build_failed" }
    }
}

# Phase 3: Archive Validation
if ($Phase -eq "all" -or $Phase -eq "3") {
    Write-Host ""
    Write-Host "--- PHASE 3: Archive Validation ---"
    $archiveResult = Test-ArchiveValidation
    $results["archive"] = $archiveResult
}

# Summary
Write-Host ""
Write-Host "==============================================="
Write-Host "TEST SUMMARY"
Write-Host "==============================================="

$successCount = 0
$totalTests = $results.Count

foreach ($testName in $results.Keys) {
    $result = $results[$testName]
    $status = $result.status
    $statusText = switch ($status) {
        "success" { "SUCCESS"; $successCount++ }
        "failed" { "FAILED" }
        "error" { "ERROR" }
        "timeout" { "TIMEOUT" }
        "skipped" { "SKIPPED" }
        default { "UNKNOWN" }
    }
    
    Write-Host "$($testName.ToUpper()): $statusText"
    
    if ($result.error) {
        Write-Host "  Error: $($result.error)"
    }
}

$successRate = if ($totalTests -gt 0) { $successCount / $totalTests } else { 0 }
Write-Host ""
Write-Host "Overall Success Rate: $($successCount)/$totalTests ($($successRate.ToString("P0")))"

if ($successRate -ge 0.7) {
    Write-TestStatus "Test execution PASSED" "SUCCESS"
} elseif ($successRate -ge 0.4) {
    Write-TestStatus "Test execution PARTIAL - needs attention" "WARN"
} else {
    Write-TestStatus "Test execution FAILED - critical issues" "ERROR"
}

Write-Host ""
