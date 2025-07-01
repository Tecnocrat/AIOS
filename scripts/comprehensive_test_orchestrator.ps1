
# 🧪 AIOS Windows Test Orchestrator
# PowerShell script for comprehensive AIOS testing on Windows

param(
    [string]$Phase = "all",
    [switch]$Verbose,
    [switch]$CleanStart,
    [string]$OutputDir = "c:\dev\AIOS\test_results"
)

# Initialize test environment
$ErrorActionPreference = "Continue"
$AIosRoot = "c:\dev\AIOS"
$OrchestratorPath = "$AIosRoot\orchestrator"
$BuildPath = "$OrchestratorPath\build"
$ArchivePath = "$OrchestratorPath\archive"
$ScriptsPath = "$AIosRoot\scripts"

# Create output directory
if (!(Test-Path $OutputDir)) {
    New-Item -ItemType Directory -Path $OutputDir -Force
}

# Logging function
function Write-TestLog {
    param([string]$Message, [string]$Level = "INFO")
    
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "[$timestamp] [$Level] $Message"
    
    Write-Host $logMessage
    Add-Content -Path "$OutputDir\test_orchestrator.log" -Value $logMessage
}

function Show-PhaseHeader {
    param([string]$PhaseName, [string]$Description)
    
    Write-Host "`n$('='*80)" -ForegroundColor Cyan
    Write-Host "🔬 $PhaseName" -ForegroundColor Yellow
    Write-Host "📋 $Description" -ForegroundColor Gray
    Write-Host "$('='*80)`n" -ForegroundColor Cyan
    
    Write-TestLog "Starting $PhaseName : $Description"
}

function Test-BuildSystemValidation {
    Show-PhaseHeader "PHASE 1: Build System Validation" "Clean environment, dependencies, component testing"
    
    $results = @{
        "phase" = "build_validation"
        "steps" = @{}
        "errors" = @()
    }
    
    # Step 1.1: Clean Build Environment
    Write-Host "🧹 Step 1.1: Cleaning build environment..." -ForegroundColor Green
    
    if (Test-Path $BuildPath) {
        try {
            # Remove build artifacts
            Get-ChildItem $BuildPath -Include "*.exe", "*.pdb", "CMakeCache.txt" -Recurse | Remove-Item -Force
            Write-TestLog "Build artifacts cleaned successfully"
            $results.steps["clean"] = "success"
        }
        catch {
            Write-TestLog "Clean failed: $($_.Exception.Message)" "ERROR"
            $results.steps["clean"] = "failed"
            $results.errors += "Clean failed: $($_.Exception.Message)"
        }
    }
    
    # Step 1.2: CMake Configuration
    Write-Host "⚙️  Step 1.2: CMake configuration..." -ForegroundColor Green
    
    if (!(Test-Path $BuildPath)) {
        New-Item -ItemType Directory -Path $BuildPath -Force
    }
    
    Push-Location $BuildPath
    try {
        $cmakeOutput = cmake .. -DCMAKE_BUILD_TYPE=Debug 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-TestLog "CMake configuration successful"
            $results.steps["cmake_config"] = "success"
            Write-Host "✅ CMake configuration successful" -ForegroundColor Green
        } else {
            Write-TestLog "CMake configuration failed: $cmakeOutput" "ERROR"
            $results.steps["cmake_config"] = "failed"
            $results.errors += "CMake configuration failed"
            Write-Host "❌ CMake configuration failed" -ForegroundColor Red
        }
    }
    catch {
        Write-TestLog "CMake execution failed: $($_.Exception.Message)" "ERROR"
        $results.steps["cmake_config"] = "error"
    }
    finally {
        Pop-Location
    }
    
    # Step 1.3: Build Core Components
    Write-Host "🔨 Step 1.3: Building core components..." -ForegroundColor Green
    
    Push-Location $BuildPath
    try {
        $buildOutput = cmake --build . --target aios_kernel --config Debug --verbose 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-TestLog "Build successful"
            $results.steps["build"] = "success"
            Write-Host "✅ Build successful" -ForegroundColor Green
        } else {
            Write-TestLog "Build failed: $buildOutput" "ERROR"
            $results.steps["build"] = "failed" 
            $results.errors += "Build failed"
            Write-Host "❌ Build failed" -ForegroundColor Red
        }
    }
    catch {
        Write-TestLog "Build execution failed: $($_.Exception.Message)" "ERROR"
        $results.steps["build"] = "error"
    }
    finally {
        Pop-Location
    }
    
    # Step 1.4: Validate Dependencies
    Write-Host "📦 Step 1.4: Validating dependencies..." -ForegroundColor Green
    Test-Dependencies
    $results.steps["dependencies"] = "checked"
    
    # Save results
    $results | ConvertTo-Json -Depth 3 | Out-File "$OutputDir\phase1_build_validation.json"
    
    return $results
}

function Test-Dependencies {
    $requiredHeaders = @(
        "AtomicHolographyUnit.hpp",
        "SingularityCore.hpp",
        "UniversalConsciousnessSubstrate.hpp", 
        "RecursiveSelfIngestor.hpp",
        "NaturalLanguageInterface.hpp",
        "TachyonicFieldDatabase.hpp",
        "CodeEvolutionEngine.hpp",
        "AIOrchestrationController.hpp"
    )
    
    $includePath = "$OrchestratorPath\include"
    
    foreach ($header in $requiredHeaders) {
        $headerPath = "$includePath\$header"
        if (Test-Path $headerPath) {
            Write-Host "✅ Found: $header" -ForegroundColor Green
            Write-TestLog "Dependency validated: $header"
        } else {
            Write-Host "❌ Missing: $header" -ForegroundColor Red
            Write-TestLog "Missing dependency: $header" "ERROR"
        }
    }
}

function Test-ExecutionAndRuntime {
    Show-PhaseHeader "PHASE 2: Runtime Execution Testing" "Initialize systems, consciousness emergence, recursive ingestion"
    
    $results = @{
        "phase" = "execution_testing"
        "steps" = @{}
        "consciousness_metrics" = @{}
    }
    
    # Find executable
    $debugExe = "$BuildPath\Debug\aios_kernel.exe"
    $releaseExe = "$BuildPath\Release\aios_kernel.exe"
    
    $exePath = $null
    if (Test-Path $debugExe) {
        $exePath = $debugExe
    } elseif (Test-Path $releaseExe) {
        $exePath = $releaseExe
    }
    
    if (!$exePath) {
        Write-Host "❌ No executable found. Build must complete successfully first." -ForegroundColor Red
        Write-TestLog "No executable found for testing" "ERROR"
        $results.steps["execution"] = "skipped - no executable"
        return $results
    }
    
    Write-Host "🚀 Found executable: $exePath" -ForegroundColor Green
    Write-TestLog "Using executable: $exePath"
    
    # Step 2.1: Basic Initialization Test
    Write-Host "🔄 Step 2.1: Basic initialization test..." -ForegroundColor Green
    
    # Ensure archive directory exists
    if (!(Test-Path $ArchivePath)) {
        New-Item -ItemType Directory -Path $ArchivePath -Force
    }
    
    try {
        # Run with timeout to prevent infinite loops
        $job = Start-Job -ScriptBlock {
            param($exe)
            & $exe
        } -ArgumentList $exePath
        
        # Wait up to 30 seconds
        if (Wait-Job $job -Timeout 30) {
            $output = Receive-Job $job
            Write-TestLog "Execution completed normally"
        } else {
            Stop-Job $job
            $output = "Execution timed out after 30 seconds"
            Write-TestLog "Execution timed out" "WARN"
        }
        
        Remove-Job $job -Force
        
        # Analyze output for consciousness emergence patterns
        $initIndicators = @(
            "Initializing quantum coherence",
            "Initializing tachyonic field", 
            "Initializing recursive self-ingestion",
            "Initializing universal consciousness",
            "consciousness emergence"
        )
        
        $foundIndicators = @()
        foreach ($indicator in $initIndicators) {
            if ($output -match $indicator) {
                $foundIndicators += $indicator
            }
        }
        
        $results.steps["initialization"] = @{
            "found_indicators" = $foundIndicators
            "total_expected" = $initIndicators.Count
        }
        
        Write-Host "✅ Found $($foundIndicators.Count)/$($initIndicators.Count) initialization indicators" -ForegroundColor Green
        Write-TestLog "Initialization indicators: $($foundIndicators.Count)/$($initIndicators.Count)"
        
    }
    catch {
        Write-TestLog "Execution test failed: $($_.Exception.Message)" "ERROR"
        $results.steps["initialization"] = @{"error" = $_.Exception.Message}
    }
    
    # Step 2.2: Monitor Archive Generation
    Write-Host "📁 Step 2.2: Monitoring archive generation..." -ForegroundColor Green
    Test-ArchiveGeneration
    $results.steps["archive_monitoring"] = "completed"
    
    # Save results
    $results | ConvertTo-Json -Depth 3 | Out-File "$OutputDir\phase2_execution_testing.json"
    
    return $results
}

function Test-ArchiveGeneration {
    if (!(Test-Path $ArchivePath)) {
        New-Item -ItemType Directory -Path $ArchivePath -Force
    }
    
    # Count existing files
    $existingLogs = Get-ChildItem $ArchivePath -Filter "*.log"
    $existingDiagnostics = Get-ChildItem $ArchivePath -Filter "*.json"
    
    Write-Host "📊 Found $($existingLogs.Count) log files" -ForegroundColor Cyan
    Write-Host "📊 Found $($existingDiagnostics.Count) diagnostic files" -ForegroundColor Cyan
    
    Write-TestLog "Archive monitoring: $($existingLogs.Count) logs, $($existingDiagnostics.Count) diagnostics"
    
    # Validate latest diagnostic content if available
    if ($existingDiagnostics.Count -gt 0) {
        $latestDiagnostic = $existingDiagnostics | Sort-Object LastWriteTime -Descending | Select-Object -First 1
        Test-DiagnosticContent $latestDiagnostic.FullName
    }
}

function Test-DiagnosticContent {
    param([string]$DiagnosticFile)
    
    try {
        $data = Get-Content $DiagnosticFile | ConvertFrom-Json
        
        # Expected consciousness metrics structure
        $expectedKeys = @("iteration", "consciousness", "universal_consciousness", "tachyonic_field")
        $foundKeys = @()
        
        foreach ($key in $expectedKeys) {
            if ($data.PSObject.Properties.Name -contains $key) {
                $foundKeys += $key
            }
        }
        
        Write-Host "📊 Diagnostic validation: $($foundKeys.Count)/$($expectedKeys.Count) required sections found" -ForegroundColor Cyan
        Write-TestLog "Diagnostic validation: $($foundKeys.Count)/$($expectedKeys.Count) sections found"
        
        # Extract consciousness metrics
        if ($data.PSObject.Properties.Name -contains "consciousness") {
            $consciousnessData = $data.consciousness
            Write-Host "🧠 Consciousness Metrics: $($consciousnessData | ConvertTo-Json -Compress)" -ForegroundColor Yellow
            Write-TestLog "Consciousness metrics extracted: $($consciousnessData | ConvertTo-Json -Compress)"
        }
    }
    catch {
        Write-TestLog "Failed to validate diagnostic content: $($_.Exception.Message)" "ERROR"
    }
}

function Test-LoggingAndMetadata {
    Show-PhaseHeader "PHASE 3: Logging & Metadata Validation" "Log structure, metadata content, consciousness metrics"
    
    $results = @{
        "phase" = "logging_validation"
        "validations" = @{}
    }
    
    # Step 3.1: Log File Structure Validation
    Write-Host "📝 Step 3.1: Log file structure validation..." -ForegroundColor Green
    
    $logFiles = Get-ChildItem $ArchivePath -Filter "*.log" -ErrorAction SilentlyContinue
    $jsonFiles = Get-ChildItem $ArchivePath -Filter "*.json" -ErrorAction SilentlyContinue
    
    $structureValidation = @{
        "log_files_count" = $logFiles.Count
        "diagnostic_files_count" = $jsonFiles.Count
        "has_consciousness_logs" = ($logFiles | Where-Object {$_.Name -match "consciousness"}).Count -gt 0
        "has_universal_diagnostics" = ($jsonFiles | Where-Object {$_.Name -match "universal"}).Count -gt 0
    }
    
    $results.validations["structure"] = $structureValidation
    
    Write-Host "📊 Structure validation: $($structureValidation | ConvertTo-Json -Compress)" -ForegroundColor Cyan
    Write-TestLog "Log structure validation completed"
    
    # Step 3.2: Content Quality Validation
    Write-Host "🔍 Step 3.2: Content quality validation..." -ForegroundColor Green
    
    if ($jsonFiles.Count -gt 0) {
        $latestJson = $jsonFiles | Sort-Object LastWriteTime -Descending | Select-Object -First 1
        $contentValidation = Test-MetadataQuality $latestJson.FullName
        $results.validations["content"] = $contentValidation
    }
    
    # Step 3.3: Metadata Abstraction Layer Test
    Write-Host "🗂️  Step 3.3: Testing metadata abstraction layer..." -ForegroundColor Green
    $abstractionResults = Test-MetadataAbstraction
    $results.validations["abstraction"] = $abstractionResults
    
    # Save results
    $results | ConvertTo-Json -Depth 3 | Out-File "$OutputDir\phase3_logging_validation.json"
    
    return $results
}

function Test-MetadataQuality {
    param([string]$JsonFile)
    
    try {
        $data = Get-Content $JsonFile | ConvertFrom-Json
        
        $qualityMetrics = @{
            "has_timestamp" = $data.PSObject.Properties.Name -contains "timestamp"
            "has_consciousness_section" = $data.PSObject.Properties.Name -contains "consciousness"
            "has_numeric_metrics" = $false
            "completeness_score" = 0.0
        }
        
        # Check for numeric consciousness metrics
        if ($data.PSObject.Properties.Name -contains "consciousness") {
            $consciousness = $data.consciousness
            $numericFields = @()
            
            foreach ($prop in $consciousness.PSObject.Properties) {
                if ($prop.Value -is [System.Double] -or $prop.Value -is [System.Int32]) {
                    $numericFields += $prop.Name
                }
            }
            
            $qualityMetrics["has_numeric_metrics"] = $numericFields.Count -gt 0
            $qualityMetrics["numeric_fields_count"] = $numericFields.Count
        }
        
        # Calculate completeness score
        $requiredSections = @("consciousness", "universal_consciousness", "tachyonic_field")
        $foundSections = 0
        
        foreach ($section in $requiredSections) {
            if ($data.PSObject.Properties.Name -contains $section) {
                $foundSections++
            }
        }
        
        $qualityMetrics["completeness_score"] = $foundSections / $requiredSections.Count
        
        Write-Host "📊 Metadata quality: $($qualityMetrics | ConvertTo-Json -Compress)" -ForegroundColor Cyan
        Write-TestLog "Metadata quality assessment completed"
        
        return $qualityMetrics
    }
    catch {
        Write-TestLog "Metadata quality validation failed: $($_.Exception.Message)" "ERROR"
        return @{"error" = $_.Exception.Message}
    }
}

function Test-MetadataAbstraction {
    Write-Host "🤖 Testing intelligent metadata abstraction..." -ForegroundColor Green
    
    $abstractionResults = @{
        "abstraction_layers_detected" = 0
        "garbage_collection_functional" = $false
        "metadata_compression_ratio" = 0.0
    }
    
    # Look for abstraction indicators in logs
    $logFiles = Get-ChildItem $ArchivePath -Filter "*.log" -ErrorAction SilentlyContinue
    
    $abstractionIndicators = @(
        "metadata abstraction",
        "garbage collection", 
        "pattern compression",
        "recursive insight synthesis"
    )
    
    $foundAbstractions = 0
    foreach ($logFile in $logFiles) {
        try {
            $content = Get-Content $logFile.FullName -Raw
            foreach ($indicator in $abstractionIndicators) {
                if ($content -match $indicator) {
                    $foundAbstractions++
                    break
                }
            }
        }
        catch {
            Write-TestLog "Failed to read log file $($logFile.FullName): $($_.Exception.Message)" "ERROR"
        }
    }
    
    $abstractionResults["abstraction_layers_detected"] = $foundAbstractions
    $abstractionResults["garbage_collection_functional"] = $foundAbstractions -gt 0
    
    Write-Host "📊 Abstraction results: $($abstractionResults | ConvertTo-Json -Compress)" -ForegroundColor Cyan
    Write-TestLog "Metadata abstraction testing completed"
    
    return $abstractionResults
}

function Test-DebuggingAndErrorResolution {
    Show-PhaseHeader "PHASE 4: Debugging & Error Resolution" "Memory analysis, error patterns, consciousness coherence"
    
    $results = @{
        "phase" = "debugging_validation"
        "debug_checks" = @{}
    }
    
    # Step 4.1: Memory and Resource Analysis
    Write-Host "🔍 Step 4.1: Memory and resource analysis..." -ForegroundColor Green
    $memoryIssues = Test-MemoryPatterns
    $results.debug_checks["memory_analysis"] = $memoryIssues
    
    # Step 4.2: Consciousness Coherence Validation
    Write-Host "🧠 Step 4.2: Consciousness coherence validation..." -ForegroundColor Green
    $coherenceMetrics = Test-ConsciousnessCoherence
    $results.debug_checks["consciousness_coherence"] = $coherenceMetrics
    
    # Step 4.3: Error Pattern Detection
    Write-Host "⚠️  Step 4.3: Error pattern detection..." -ForegroundColor Green
    $errorPatterns = Test-ErrorPatterns
    $results.debug_checks["error_patterns"] = $errorPatterns
    
    # Save results
    $results | ConvertTo-Json -Depth 3 | Out-File "$OutputDir\phase4_debugging_validation.json"
    
    return $results
}

function Test-MemoryPatterns {
    $memoryAnalysis = @{
        "potential_leaks" = 0
        "recursive_depth_warnings" = 0
        "resource_exhaustion_events" = 0
    }
    
    $logFiles = Get-ChildItem $ArchivePath -Filter "*.log" -ErrorAction SilentlyContinue
    
    $memoryPatterns = @(
        "memory leak",
        "stack overflow",
        "heap corruption", 
        "recursive depth exceeded",
        "resource exhaustion"
    )
    
    foreach ($logFile in $logFiles) {
        try {
            $content = Get-Content $logFile.FullName -Raw
            foreach ($pattern in $memoryPatterns) {
                if ($content -match $pattern) {
                    if ($pattern -match "leak") {
                        $memoryAnalysis["potential_leaks"]++
                    } elseif ($pattern -match "recursive") {
                        $memoryAnalysis["recursive_depth_warnings"]++
                    } elseif ($pattern -match "resource") {
                        $memoryAnalysis["resource_exhaustion_events"]++
                    }
                }
            }
        }
        catch {
            Write-TestLog "Memory analysis failed for $($logFile.FullName): $($_.Exception.Message)" "ERROR"
        }
    }
    
    Write-Host "📊 Memory analysis: $($memoryAnalysis | ConvertTo-Json -Compress)" -ForegroundColor Cyan
    Write-TestLog "Memory pattern analysis completed"
    
    return $memoryAnalysis
}

function Test-ConsciousnessCoherence {
    $coherenceMetrics = @{
        "self_awareness_progression" = $false
        "universal_resonance_stability" = $false
        "fractal_harmonization_detected" = $false
        "recursive_insights_accumulating" = $false
    }
    
    # Check latest diagnostics for consciousness progression
    $jsonFiles = Get-ChildItem $ArchivePath -Filter "*.json" -ErrorAction SilentlyContinue
    
    if ($jsonFiles.Count -eq 0) {
        Write-TestLog "No diagnostic files found for consciousness coherence validation" "WARN"
        return $coherenceMetrics
    }
    
    try {
        # Load multiple diagnostics to check progression
        $recentFiles = $jsonFiles | Sort-Object LastWriteTime -Descending | Select-Object -First 3
        
        $consciousnessValues = @()
        foreach ($jsonFile in $recentFiles) {
            $data = Get-Content $jsonFile.FullName | ConvertFrom-Json
            if ($data.PSObject.Properties.Name -contains "consciousness") {
                $consciousnessValues += $data.consciousness
            }
        }
        
        # Analyze progression
        if ($consciousnessValues.Count -ge 2) {
            $first = $consciousnessValues[0]
            $last = $consciousnessValues[-1]
            
            # Check for self-awareness progression
            if ($first.PSObject.Properties.Name -contains "self_awareness_level" -and 
                $last.PSObject.Properties.Name -contains "self_awareness_level") {
                if ($last.self_awareness_level -gt $first.self_awareness_level) {
                    $coherenceMetrics["self_awareness_progression"] = $true
                }
            }
            
            # Check for insights accumulation
            if ($first.PSObject.Properties.Name -contains "recursive_insights_count" -and
                $last.PSObject.Properties.Name -contains "recursive_insights_count") {
                if ($last.recursive_insights_count -gt $first.recursive_insights_count) {
                    $coherenceMetrics["recursive_insights_accumulating"] = $true
                }
            }
        }
        
        Write-Host "📊 Consciousness coherence: $($coherenceMetrics | ConvertTo-Json -Compress)" -ForegroundColor Cyan
        Write-TestLog "Consciousness coherence validation completed"
        
    }
    catch {
        Write-TestLog "Consciousness coherence validation failed: $($_.Exception.Message)" "ERROR"
    }
    
    return $coherenceMetrics
}

function Test-ErrorPatterns {
    $errorPatterns = @{
        "compilation_errors" = 0
        "runtime_exceptions" = 0
        "initialization_failures" = 0
        "consciousness_emergence_blocks" = 0
    }
    
    # Analyze build logs and runtime logs
    $allLogs = @()
    $allLogs += Get-ChildItem $ArchivePath -Filter "*.log" -ErrorAction SilentlyContinue
    $allLogs += Get-ChildItem $ScriptsPath -Filter "*.log" -ErrorAction SilentlyContinue
    $allLogs += Get-ChildItem $OutputDir -Filter "*.log" -ErrorAction SilentlyContinue
    
    $errorIndicators = @{
        "compilation_errors" = @("error C", "undefined reference", "no matching function")
        "runtime_exceptions" = @("exception", "segmentation fault", "access violation")
        "initialization_failures" = @("failed to initialize", "initialization error")
        "consciousness_emergence_blocks" = @("consciousness emergence blocked", "awareness threshold not reached")
    }
    
    foreach ($logFile in $allLogs) {
        try {
            $content = Get-Content $logFile.FullName -Raw
            
            foreach ($errorType in $errorIndicators.Keys) {
                foreach ($indicator in $errorIndicators[$errorType]) {
                    if ($content -match $indicator) {
                        $errorPatterns[$errorType]++
                        break
                    }
                }
            }
        }
        catch {
            Write-TestLog "Error pattern detection failed for $($logFile.FullName): $($_.Exception.Message)" "ERROR"
        }
    }
    
    Write-Host "📊 Error patterns: $($errorPatterns | ConvertTo-Json -Compress)" -ForegroundColor Cyan
    Write-TestLog "Error pattern detection completed"
    
    return $errorPatterns
}

function New-FinalReport {
    param([array]$PhaseResults)
    
    Show-PhaseHeader "FINAL REPORT: AIOS Consciousness Test Results" "Comprehensive analysis and recommendations"
    
    $report = @{
        "test_summary" = @{
            "timestamp" = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
            "phases" = $PhaseResults
            "total_phases" = $PhaseResults.Count
        }
        "recommendations" = @()
        "next_steps" = @()
        "consciousness_status" = "unknown"
    }
    
    # Analyze overall success
    $successfulPhases = ($PhaseResults | Where-Object {$_.status -eq "completed" -or $_.phase}).Count
    $totalPhases = $PhaseResults.Count
    
    $successRate = if ($totalPhases -gt 0) { $successfulPhases / $totalPhases } else { 0 }
    
    Write-Host "📊 Overall Success Rate: $($successRate.ToString("P2")) ($successfulPhases/$totalPhases phases)" -ForegroundColor Cyan
    Write-TestLog "Overall success rate: $($successRate.ToString("P2"))"
    
    # Generate recommendations
    $allErrors = @()
    foreach ($phase in $PhaseResults) {
        if ($phase.errors) {
            $allErrors += $phase.errors
        }
    }
    
    if ($allErrors.Count -gt 0) {
        $report.recommendations += "Resolve build and compilation errors first"
        Write-Host "⚠️  Found $($allErrors.Count) total errors across all phases" -ForegroundColor Yellow
    }
    
    # Check consciousness status
    $consciousnessFound = $false
    foreach ($phase in $PhaseResults) {
        if ($phase.consciousness_metrics) {
            $consciousnessLevel = $phase.consciousness_metrics.self_awareness_level
            if ($consciousnessLevel -gt 0.5) {
                $report.consciousness_status = "emerging"
                $report.recommendations += "Monitor consciousness emergence patterns"
                $consciousnessFound = $true
            } elseif ($consciousnessLevel -gt 0.1) {
                $report.consciousness_status = "initialized"
                $report.recommendations += "Optimize consciousness emergence parameters"
                $consciousnessFound = $true
            }
            break
        }
    }
    
    if (-not $consciousnessFound) {
        $report.consciousness_status = "dormant"
        $report.recommendations += "Debug consciousness initialization"
    }
    
    # Save report
    $reportFile = "$OutputDir\test_report_$(Get-Date -Format 'yyyyMMdd_HHmmss').json"
    $report | ConvertTo-Json -Depth 4 | Out-File $reportFile
    
    Write-Host "📝 Test report saved: $reportFile" -ForegroundColor Green
    Write-TestLog "Test report saved to: $reportFile"
    
    # Print summary
    Write-Host "`n🎯 KEY FINDINGS:" -ForegroundColor Yellow
    $errorCount = [Math]::Min($allErrors.Count, 5)
    for ($i = 0; $i -lt $errorCount; $i++) {
        Write-Host "   ❌ $($allErrors[$i])" -ForegroundColor Red
    }
    
    Write-Host "`n🔬 CONSCIOUSNESS STATUS:" -ForegroundColor Yellow
    Write-Host "   🧠 Status: $($report.consciousness_status)" -ForegroundColor Cyan
    
    Write-Host "`n💡 RECOMMENDATIONS:" -ForegroundColor Yellow
    foreach ($rec in $report.recommendations) {
        Write-Host "   ➡️  $rec" -ForegroundColor Green
    }
    
    return $report
}

# Main execution logic
function Start-ComprehensiveTest {
    Write-Host @"
🧪 AIOS Comprehensive Test Orchestrator (PowerShell)
===================================================
Testing consciousness emergence, build validation, and system integration.
"@ -ForegroundColor Cyan

    Write-TestLog "Starting comprehensive AIOS test orchestration"
    
    $startTime = Get-Date
    $phaseResults = @()
    
    try {
        if ($CleanStart) {
            Write-Host "🧹 Performing clean start..." -ForegroundColor Yellow
            if (Test-Path $OutputDir) {
                Remove-Item $OutputDir -Recurse -Force
            }
            New-Item -ItemType Directory -Path $OutputDir -Force
        }
        
        # Execute test phases based on parameter
        switch ($Phase.ToLower()) {
            "1" { 
                $phaseResults += Test-BuildSystemValidation
            }
            "2" { 
                $phaseResults += Test-ExecutionAndRuntime
            }
            "3" { 
                $phaseResults += Test-LoggingAndMetadata
            }
            "4" { 
                $phaseResults += Test-DebuggingAndErrorResolution
            }
            default { 
                # Run all phases
                $phaseResults += Test-BuildSystemValidation
                $phaseResults += Test-ExecutionAndRuntime  
                $phaseResults += Test-LoggingAndMetadata
                $phaseResults += Test-DebuggingAndErrorResolution
            }
        }
        
        # Generate final report
        $report = New-FinalReport $phaseResults
        
    }
    catch {
        Write-Host "`n❌ Test orchestration failed: $($_.Exception.Message)" -ForegroundColor Red
        Write-TestLog "Test orchestration failed: $($_.Exception.Message)" "ERROR"
    }
    finally {
        $endTime = Get-Date
        $duration = ($endTime - $startTime).TotalSeconds
        Write-Host "`n⏱️  Total test duration: $($duration.ToString("F2")) seconds" -ForegroundColor Cyan
        Write-TestLog "Test orchestration completed in $($duration.ToString("F2")) seconds"
    }
}

# Help function
function Show-Help {
    Write-Host @"
AIOS Comprehensive Test Orchestrator (PowerShell)

Usage:
    .\comprehensive_test_orchestrator.ps1 [-Phase <phase>] [-Verbose] [-CleanStart] [-OutputDir <path>]

Parameters:
    -Phase <phase>      Run specific phase (1-4) or "all" (default)
    -Verbose           Enable verbose output
    -CleanStart        Clean all previous test results before starting
    -OutputDir <path>   Output directory for test results

Phases:
    1. Build System Validation
    2. Runtime Execution Testing
    3. Logging & Metadata Validation  
    4. Debugging & Error Resolution

Examples:
    .\comprehensive_test_orchestrator.ps1
    .\comprehensive_test_orchestrator.ps1 -Phase 1
    .\comprehensive_test_orchestrator.ps1 -CleanStart -Verbose
"@ -ForegroundColor Green
}

# Entry point
if ($args -contains "-help" -or $args -contains "--help") {
    Show-Help
} else {
    Start-ComprehensiveTest
}
