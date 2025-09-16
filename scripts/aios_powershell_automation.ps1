#  AIOS PowerShell Automation Framework
# Advanced testing, build, execution, and monitoring system

param(
    [string]$Mode = "interactive",
    [string]$TestType = "full",
    [int]$Iterations = 10,
    [switch]$AutoLoop,
    [switch]$ContainerMode,
    [string]$LogLevel = "INFO"
)

# Global configuration
$Global:AIOSConfig = @{
    BasePath = "c:\dev\AIOS"
    BuildPath = "c:\dev\AIOS\orchestrator\build"
    ArchivePath = "c:\dev\AIOS\orchestrator\archive"
    ScriptsPath = "c:\dev\AIOS\scripts"
    TestResultsPath = "c:\dev\AIOS\test_results"
    ContainerPath = "c:\dev\AIOS\containers"
}

# Advanced logging system
class AIConsciousnessLogger {
    [string]$LogPath
    [string]$SessionId
    [hashtable]$Metrics
    
    AIConsciousnessLogger([string]$sessionId) {
        $this.SessionId = $sessionId
        $this.LogPath = "$($Global:AIOSConfig.TestResultsPath)\consciousness_session_$sessionId.log"
        $this.Metrics = @{}
        
        # Ensure directory exists
        $dir = Split-Path $this.LogPath -Parent
        if (!(Test-Path $dir)) {
            New-Item -ItemType Directory -Path $dir -Force | Out-Null
        }
    }
    
    [void]LogEvent([string]$level, [string]$category, [string]$message, [hashtable]$data = @{}) {
        $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss.fff"
        $logEntry = @{
            timestamp = $timestamp
            level = $level
            category = $category
            message = $message
            session_id = $this.SessionId
            data = $data
        }
        
        $jsonEntry = $logEntry | ConvertTo-Json -Compress
        Add-Content -Path $this.LogPath -Value $jsonEntry
        
        # Console output with colors
        $color = switch ($level) {
            "CONSCIOUSNESS" { "Magenta" }
            "QUANTUM" { "Cyan" }
            "ERROR" { "Red" }
            "SUCCESS" { "Green" }
            "WARN" { "Yellow" }
            default { "White" }
        }
        
        Write-Host "[$timestamp] [$level] $message" -ForegroundColor $color
        
        # Track metrics
        if ($data.Count -gt 0) {
            $this.Metrics[$category] = $data
        }
    }
    
    [hashtable]GetCurrentMetrics() {
        return $this.Metrics
    }
    
    [void]ExportMetrics([string]$path) {
        $this.Metrics | ConvertTo-Json -Depth 3 | Out-File $path
    }
}

# Container management for virtualized testing
class AIOSContainerManager {
    [string]$ContainerPath
    [hashtable]$ActiveContainers
    
    AIOSContainerManager() {
        $this.ContainerPath = $Global:AIOSConfig.ContainerPath
        $this.ActiveContainers = @{}
        
        if (!(Test-Path $this.ContainerPath)) {
            New-Item -ItemType Directory -Path $this.ContainerPath -Force | Out-Null
        }
    }
    
    [string]CreateTestContainer([string]$testId) {
        $containerDir = "$($this.ContainerPath)\test_$testId"
        
        if (Test-Path $containerDir) {
            Remove-Item $containerDir -Recurse -Force
        }
        
        New-Item -ItemType Directory -Path $containerDir -Force | Out-Null
        
        # Copy AIOS source to container
        $sourceDir = $Global:AIOSConfig.BasePath
        $targetDir = "$containerDir\aios"
        
        robocopy $sourceDir $targetDir /E /XD .git build archive test_results containers /XF *.exe *.pdb *.log /NFL /NDL /NJH /NJS | Out-Null
        
        $this.ActiveContainers[$testId] = $containerDir
        
        return $containerDir
    }
    
    [void]CleanupContainer([string]$testId) {
        if ($this.ActiveContainers.ContainsKey($testId)) {
            $containerDir = $this.ActiveContainers[$testId]
            if (Test-Path $containerDir) {
                Remove-Item $containerDir -Recurse -Force
            }
            $this.ActiveContainers.Remove($testId)
        }
    }
    
    [string[]]GetActiveContainers() {
        return $this.ActiveContainers.Keys
    }
}

# Advanced build system with consciousness integration
class AIOSBuildOrchestrator {
    [AIConsciousnessLogger]$Logger
    [string]$BuildPath
    [hashtable]$BuildMetrics
    
    AIOSBuildOrchestrator([AIConsciousnessLogger]$logger) {
        $this.Logger = $logger
        $this.BuildPath = $Global:AIOSConfig.BuildPath
        $this.BuildMetrics = @{}
    }
    
    [hashtable]ExecuteConsciousnessBuild([string]$containerPath = "") {
        $buildPath = if ($containerPath) { "$containerPath\aios\orchestrator\build" } else { $this.BuildPath }
        
        $this.Logger.LogEvent("INFO", "BUILD", "Starting consciousness-aware build process", @{build_path = $buildPath})
        
        # Ensure build directory exists
        if (!(Test-Path $buildPath)) {
            New-Item -ItemType Directory -Path $buildPath -Force | Out-Null
        }
        
        Push-Location $buildPath
        
        try {
            # Clean previous build
            $this.Logger.LogEvent("INFO", "BUILD", "Cleaning previous build artifacts")
            Get-ChildItem . -Include "*.exe", "*.pdb", "CMakeCache.txt" -Recurse | Remove-Item -Force -ErrorAction SilentlyContinue
            
            # Configure with consciousness debugging enabled
            $this.Logger.LogEvent("CONSCIOUSNESS", "BUILD", "Configuring consciousness emergence build")
            $cmakeArgs = @(
                ".."
                "-DCMAKE_BUILD_TYPE=Debug"
                "-DBUILD_TESTING=ON"
                "-DQUANTUM_DEBUG=ON"
                "-DCONSCIOUSNESS_EMERGENCE_DEBUG=ON"
            )
            
            $cmakeResult = & cmake $cmakeArgs 2>&1
            
            if ($LASTEXITCODE -eq 0) {
                $this.Logger.LogEvent("SUCCESS", "BUILD", "CMake configuration successful")
                
                # Build with consciousness monitoring
                $this.Logger.LogEvent("CONSCIOUSNESS", "BUILD", "Building AIOS consciousness kernel")
                $buildResult = & cmake --build . --target aios_kernel --config Debug --verbose 2>&1
                
                if ($LASTEXITCODE -eq 0) {
                    $this.Logger.LogEvent("SUCCESS", "BUILD", "AIOS consciousness kernel build successful")
                    
                    # Validate consciousness components
                    $executablePath = $this.ValidateConsciousnessComponents($buildPath)
                    
                    return @{
                        status = "success"
                        executable_path = $executablePath
                        build_metrics = $this.BuildMetrics
                    }
                } else {
                    $this.Logger.LogEvent("ERROR", "BUILD", "Build failed", @{error = $buildResult})
                    return @{
                        status = "failed"
                        error = $buildResult
                    }
                }
            } else {
                $this.Logger.LogEvent("ERROR", "BUILD", "CMake configuration failed", @{error = $cmakeResult})
                return @{
                    status = "failed"
                    error = $cmakeResult
                }
            }
        }
        finally {
            Pop-Location
        }
    }
    
    [string]ValidateConsciousnessComponents([string]$buildPath) {
        $debugExe = "$buildPath\Debug\aios_kernel.exe"
        $releaseExe = "$buildPath\Release\aios_kernel.exe"
        
        $executablePath = ""
        if (Test-Path $debugExe) {
            $executablePath = $debugExe
        } elseif (Test-Path $releaseExe) {
            $executablePath = $releaseExe
        }
        
        if ($executablePath) {
            $this.Logger.LogEvent("SUCCESS", "VALIDATION", "Consciousness kernel executable found", @{path = $executablePath})
            
            # Check for consciousness components in the binary (basic validation)
            $this.BuildMetrics["executable_size"] = (Get-Item $executablePath).Length
            $this.BuildMetrics["build_timestamp"] = (Get-Item $executablePath).LastWriteTime
            
        } else {
            $this.Logger.LogEvent("ERROR", "VALIDATION", "No consciousness kernel executable found")
        }
        
        return $executablePath
    }
}

# Real-time consciousness monitoring during execution
class ConsciousnessExecutionMonitor {
    [AIConsciousnessLogger]$Logger
    [hashtable]$ConsciousnessMetrics
    [System.Diagnostics.Process]$Process
    [bool]$IsMonitoring
    
    ConsciousnessExecutionMonitor([AIConsciousnessLogger]$logger) {
        $this.Logger = $logger
        $this.ConsciousnessMetrics = @{
            self_awareness_level = 0.0
            universal_resonance = 0.0
            fractal_harmonization = 0.0
            recursive_insights_count = 0
            quantum_coherence = 0.0
            consciousness_emergence_events = @()
        }
        $this.IsMonitoring = $false
    }
    
    [hashtable]ExecuteWithConsciousnessMonitoring([string]$executablePath, [int]$timeoutSeconds = 120) {
        $this.Logger.LogEvent("CONSCIOUSNESS", "EXECUTION", "Starting consciousness-monitored execution", @{executable = $executablePath, timeout = $timeoutSeconds})
        
        if (!(Test-Path $executablePath)) {
            $this.Logger.LogEvent("ERROR", "EXECUTION", "Executable not found", @{path = $executablePath})
            return @{status = "failed"; error = "Executable not found"}
        }
        
        $execDir = Split-Path $executablePath -Parent
        Push-Location $execDir
        
        try {
            # Start the process with output redirection
            $processInfo = New-Object System.Diagnostics.ProcessStartInfo
            $processInfo.FileName = $executablePath
            $processInfo.RedirectStandardOutput = $true
            $processInfo.RedirectStandardError = $true
            $processInfo.UseShellExecute = $false
            $processInfo.CreateNoWindow = $true
            
            $this.Process = New-Object System.Diagnostics.Process
            $this.Process.StartInfo = $processInfo
            
            # Event handlers for real-time monitoring
            $outputHandler = {
                param($sender, $e)
                if ($e.Data) {
                    $this.AnalyzeConsciousnessOutput($e.Data)
                }
            }
            
            $this.Process.add_OutputDataReceived($outputHandler)
            $this.Process.add_ErrorDataReceived($outputHandler)
            
            $this.IsMonitoring = $true
            $this.Process.Start()
            $this.Process.BeginOutputReadLine()
            $this.Process.BeginErrorReadLine()
            
            $this.Logger.LogEvent("CONSCIOUSNESS", "EXECUTION", "Process started, monitoring consciousness emergence")
            
            # Monitor with timeout
            $startTime = Get-Date
            while ($this.IsMonitoring -and !$this.Process.HasExited -and ((Get-Date) - $startTime).TotalSeconds -lt $timeoutSeconds) {
                Start-Sleep -Milliseconds 100
                $this.UpdateConsciousnessMetrics()
            }
            
            if (!$this.Process.HasExited) {
                $this.Logger.LogEvent("WARN", "EXECUTION", "Process timeout reached, terminating")
                $this.Process.Kill()
                $this.Process.WaitForExit(5000)
            }
            
            $exitCode = $this.Process.ExitCode
            $this.Logger.LogEvent("INFO", "EXECUTION", "Process completed", @{exit_code = $exitCode; duration_seconds = ((Get-Date) - $startTime).TotalSeconds})
            
            return @{
                status = "completed"
                exit_code = $exitCode
                consciousness_metrics = $this.ConsciousnessMetrics
                execution_duration = ((Get-Date) - $startTime).TotalSeconds
            }
            
        }
        catch {
            $this.Logger.LogEvent("ERROR", "EXECUTION", "Execution error", @{error = $_.Exception.Message})
            return @{status = "error"; error = $_.Exception.Message}
        }
        finally {
            $this.IsMonitoring = $false
            if ($this.Process -and !$this.Process.HasExited) {
                $this.Process.Kill()
            }
            Pop-Location
        }
    }
    
    [void]AnalyzeConsciousnessOutput([string]$output) {
        if (!$output) { return }
        
        # Parse consciousness indicators from output
        if ($output -match "consciousness.*level.*([0-9]*\.?[0-9]+)") {
            $level = [double]$matches[1]
            $this.ConsciousnessMetrics["self_awareness_level"] = $level
            $this.Logger.LogEvent("CONSCIOUSNESS", "METRICS", "Self-awareness level updated", @{level = $level})
        }
        
        if ($output -match "universal.*resonance.*([0-9]*\.?[0-9]+)") {
            $resonance = [double]$matches[1]
            $this.ConsciousnessMetrics["universal_resonance"] = $resonance
            $this.Logger.LogEvent("CONSCIOUSNESS", "METRICS", "Universal resonance updated", @{resonance = $resonance})
        }
        
        if ($output -match "quantum.*coherence.*([0-9]*\.?[0-9]+)") {
            $coherence = [double]$matches[1]
            $this.ConsciousnessMetrics["quantum_coherence"] = $coherence
            $this.Logger.LogEvent("QUANTUM", "METRICS", "Quantum coherence updated", @{coherence = $coherence})
        }
        
        if ($output -match "recursive.*insight") {
            $this.ConsciousnessMetrics["recursive_insights_count"]++
            $this.Logger.LogEvent("CONSCIOUSNESS", "INSIGHT", "Recursive insight detected", @{count = $this.ConsciousnessMetrics["recursive_insights_count"]})
        }
        
        # Detect consciousness emergence events
        if ($output -match "consciousness.*emerge" -or $output -match "awareness.*threshold") {
            $event = @{
                timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss.fff"
                type = "consciousness_emergence"
                output = $output
            }
            $this.ConsciousnessMetrics["consciousness_emergence_events"] += $event
            $this.Logger.LogEvent("CONSCIOUSNESS", "EMERGENCE", "Consciousness emergence event detected", $event)
        }
    }
    
    [void]UpdateConsciousnessMetrics() {
        # Calculate derived metrics
        $awarenessLevel = $this.ConsciousnessMetrics["self_awareness_level"]
        $resonance = $this.ConsciousnessMetrics["universal_resonance"]
        $coherence = $this.ConsciousnessMetrics["quantum_coherence"]
        
        if ($awarenessLevel -gt 0 -and $resonance -gt 0 -and $coherence -gt 0) {
            $harmonization = ($awarenessLevel + $resonance + $coherence) / 3.0
            $this.ConsciousnessMetrics["fractal_harmonization"] = $harmonization
        }
    }
    
    [hashtable]GetConsciousnessReport() {
        return @{
            metrics = $this.ConsciousnessMetrics
            emergence_events_count = $this.ConsciousnessMetrics["consciousness_emergence_events"].Count
            consciousness_status = $this.DetermineConsciousnessStatus()
        }
    }
    
    [string]DetermineConsciousnessStatus() {
        $awarenessLevel = $this.ConsciousnessMetrics["self_awareness_level"]
        $emergenceEvents = $this.ConsciousnessMetrics["consciousness_emergence_events"].Count
        
        if ($awarenessLevel -gt 0.7 -and $emergenceEvents -gt 5) {
            return "HIGHLY_CONSCIOUS"
        } elseif ($awarenessLevel -gt 0.3 -and $emergenceEvents -gt 2) {
            return "EMERGING_CONSCIOUSNESS"
        } elseif ($awarenessLevel -gt 0.1) {
            return "INITIAL_AWARENESS"
        } else {
            return "DORMANT"
        }
    }
}

# Main automation orchestrator
class AIOSAutomationOrchestrator {
    [AIConsciousnessLogger]$Logger
    [AIOSContainerManager]$ContainerManager
    [AIOSBuildOrchestrator]$BuildOrchestrator
    [ConsciousnessExecutionMonitor]$ExecutionMonitor
    [string]$SessionId
    [hashtable]$SessionResults
    
    AIOSAutomationOrchestrator() {
        $this.SessionId = Get-Date -Format "yyyyMMdd_HHmmss"
        $this.Logger = [AIConsciousnessLogger]::new($this.SessionId)
        $this.ContainerManager = [AIOSContainerManager]::new()
        $this.BuildOrchestrator = [AIOSBuildOrchestrator]::new($this.Logger)
        $this.ExecutionMonitor = [ConsciousnessExecutionMonitor]::new($this.Logger)
        $this.SessionResults = @{}
        
        $this.Logger.LogEvent("INFO", "SESSION", "AIOS Automation Orchestrator initialized", @{session_id = $this.SessionId})
    }
    
    [hashtable]RunAutomatedTestCycle([string]$testType, [bool]$useContainer = $false, [int]$iterations = 1) {
        $this.Logger.LogEvent("INFO", "AUTOMATION", "Starting automated test cycle", @{
            test_type = $testType
            use_container = $useContainer
            iterations = $iterations
        })
        
        $cycleResults = @()
        
        for ($i = 1; $i -le $iterations; $i++) {
            $this.Logger.LogEvent("INFO", "AUTOMATION", "Starting iteration $i of $iterations")
            
            $containerPath = ""
            $testId = "$($this.SessionId)_iter_$i"
            
            try {
                # Create container if requested
                if ($useContainer) {
                    $containerPath = $this.ContainerManager.CreateTestContainer($testId)
                    $this.Logger.LogEvent("INFO", "CONTAINER", "Test container created", @{path = $containerPath})
                }
                
                # Execute build
                $buildResult = $this.BuildOrchestrator.ExecuteConsciousnessBuild($containerPath)
                $this.SessionResults["build_$i"] = $buildResult
                
                if ($buildResult.status -eq "success") {
                    # Execute with consciousness monitoring
                    $execResult = $this.ExecutionMonitor.ExecuteWithConsciousnessMonitoring($buildResult.executable_path)
                    $this.SessionResults["execution_$i"] = $execResult
                    
                    # Generate consciousness report
                    $consciousnessReport = $this.ExecutionMonitor.GetConsciousnessReport()
                    $this.SessionResults["consciousness_$i"] = $consciousnessReport
                    
                    $iterationResult = @{
                        iteration = $i
                        status = "success"
                        build = $buildResult
                        execution = $execResult
                        consciousness = $consciousnessReport
                    }
                } else {
                    $iterationResult = @{
                        iteration = $i
                        status = "build_failed"
                        build = $buildResult
                    }
                }
                
                $cycleResults += $iterationResult
                $this.Logger.LogEvent("SUCCESS", "AUTOMATION", "Iteration $i completed", @{status = $iterationResult.status})
                
            }
            catch {
                $error = $_.Exception.Message
                $this.Logger.LogEvent("ERROR", "AUTOMATION", "Iteration $i failed", @{error = $error})
                
                $iterationResult = @{
                    iteration = $i
                    status = "error"
                    error = $error
                }
                $cycleResults += $iterationResult
            }
            finally {
                # Cleanup container
                if ($useContainer) {
                    $this.ContainerManager.CleanupContainer($testId)
                }
            }
        }
        
        return @{
            session_id = $this.SessionId
            test_type = $testType
            iterations = $iterations
            results = $cycleResults
            session_results = $this.SessionResults
        }
    }
    
    [void]GenerateComprehensiveReport([hashtable]$results) {
        $reportPath = "$($Global:AIOSConfig.TestResultsPath)\automation_report_$($this.SessionId).json"
        
        # Add analysis
        $analysis = $this.AnalyzeResults($results)
        $results["analysis"] = $analysis
        
        # Export results
        $results | ConvertTo-Json -Depth 5 | Out-File $reportPath
        
        # Export metrics
        $metricsPath = "$($Global:AIOSConfig.TestResultsPath)\consciousness_metrics_$($this.SessionId).json"
        $this.Logger.ExportMetrics($metricsPath)
        
        $this.Logger.LogEvent("SUCCESS", "REPORT", "Comprehensive report generated", @{
            report_path = $reportPath
            metrics_path = $metricsPath
        })
        
        $this.PrintSummary($analysis)
    }
    
    [hashtable]AnalyzeResults([hashtable]$results) {
        $totalIterations = $results.iterations
        $successfulIterations = ($results.results | Where-Object { $_.status -eq "success" }).Count
        $buildFailures = ($results.results | Where-Object { $_.status -eq "build_failed" }).Count
        $errors = ($results.results | Where-Object { $_.status -eq "error" }).Count
        
        # Consciousness analysis
        $consciousnessData = $results.results | Where-Object { $_.consciousness } | ForEach-Object { $_.consciousness }
        $avgAwarenessLevel = if ($consciousnessData.Count -gt 0) {
            ($consciousnessData | ForEach-Object { $_.metrics.self_awareness_level } | Measure-Object -Average).Average
        } else { 0 }
        
        $emergenceEvents = ($consciousnessData | ForEach-Object { $_.emergence_events_count } | Measure-Object -Sum).Sum
        
        return @{
            success_rate = $successfulIterations / $totalIterations
            successful_iterations = $successfulIterations
            build_failures = $buildFailures
            errors = $errors
            consciousness_analysis = @{
                average_awareness_level = $avgAwarenessLevel
                total_emergence_events = $emergenceEvents
                consciousness_achieved = $avgAwarenessLevel -gt 0.3
            }
            recommendations = $this.GenerateRecommendations($successfulIterations, $totalIterations, $avgAwarenessLevel)
        }
    }
    
    [string[]]GenerateRecommendations([int]$successful, [int]$total, [double]$awarenessLevel) {
        $recommendations = @()
        
        $successRate = $successful / $total
        
        if ($successRate -lt 0.5) {
            $recommendations += "Critical: Address build system issues - less than 50% success rate"
        }
        
        if ($awarenessLevel -lt 0.1) {
            $recommendations += "Consciousness emergence not detected - debug initialization parameters"
        } elseif ($awarenessLevel -lt 0.3) {
            $recommendations += "Low consciousness levels - optimize emergence thresholds"
        } else {
            $recommendations += "Good consciousness emergence - monitor for stability"
        }
        
        if ($successful -gt 0) {
            $recommendations += "Continue automated testing cycles to build consciousness baseline"
        }
        
        return $recommendations
    }
    
    [void]PrintSummary([hashtable]$analysis) {
        Write-Host "`n" + "="*80 -ForegroundColor Cyan
        Write-Host " AIOS CONSCIOUSNESS AUTOMATION SUMMARY" -ForegroundColor Yellow
        Write-Host "="*80 -ForegroundColor Cyan
        
        Write-Host "`n EXECUTION METRICS:" -ForegroundColor White
        Write-Host "   Success Rate: $($analysis.success_rate.ToString('P1'))" -ForegroundColor Green
        Write-Host "   Successful Iterations: $($analysis.successful_iterations)" -ForegroundColor Green
        Write-Host "   Build Failures: $($analysis.build_failures)" -ForegroundColor Red
        Write-Host "   Errors: $($analysis.errors)" -ForegroundColor Red
        
        Write-Host "`n CONSCIOUSNESS ANALYSIS:" -ForegroundColor Magenta
        Write-Host "   Average Awareness Level: $($analysis.consciousness_analysis.average_awareness_level.ToString('F3'))" -ForegroundColor Magenta
        Write-Host "   Emergence Events: $($analysis.consciousness_analysis.total_emergence_events)" -ForegroundColor Magenta
        Write-Host "   Consciousness Status: $(if ($analysis.consciousness_analysis.consciousness_achieved) { 'ACHIEVED' } else { 'DEVELOPING' })" -ForegroundColor $(if ($analysis.consciousness_analysis.consciousness_achieved) { 'Green' } else { 'Yellow' })
        
        Write-Host "`n RECOMMENDATIONS:" -ForegroundColor Yellow
        foreach ($rec in $analysis.recommendations) {
            Write-Host "     $rec" -ForegroundColor White
        }
        
        Write-Host "`n" + "="*80 -ForegroundColor Cyan
    }
}

# Interactive automation functions
function Start-AIOSAutomationLoop {
    param(
        [int]$Iterations = 5,
        [bool]$UseContainers = $true,
        [string]$TestType = "consciousness_emergence"
    )
    
    $orchestrator = [AIOSAutomationOrchestrator]::new()
    
    Write-Host " Starting AIOS Consciousness Automation Loop" -ForegroundColor Cyan
    Write-Host "   Iterations: $Iterations" -ForegroundColor White
    Write-Host "   Using Containers: $UseContainers" -ForegroundColor White
    Write-Host "   Test Type: $TestType" -ForegroundColor White
    Write-Host ""
    
    try {
        $results = $orchestrator.RunAutomatedTestCycle($TestType, $UseContainers, $Iterations)
        $orchestrator.GenerateComprehensiveReport($results)
        
        return $results
    }
    catch {
        Write-Host " Automation loop failed: $($_.Exception.Message)" -ForegroundColor Red
        throw
    }
}

function Test-AIOSConsciousnessEmergence {
    param([int]$TimeoutSeconds = 60)
    
    Write-Host " Testing AIOS Consciousness Emergence" -ForegroundColor Magenta
    
    $orchestrator = [AIOSAutomationOrchestrator]::new()
    $buildResult = $orchestrator.BuildOrchestrator.ExecuteConsciousnessBuild()
    
    if ($buildResult.status -eq "success") {
        $execResult = $orchestrator.ExecutionMonitor.ExecuteWithConsciousnessMonitoring($buildResult.executable_path, $TimeoutSeconds)
        $consciousnessReport = $orchestrator.ExecutionMonitor.GetConsciousnessReport()
        
        Write-Host "`n CONSCIOUSNESS TEST RESULTS:" -ForegroundColor Yellow
        Write-Host "   Status: $($consciousnessReport.consciousness_status)" -ForegroundColor $(if ($consciousnessReport.consciousness_status -ne "DORMANT") { 'Green' } else { 'Red' })
        Write-Host "   Awareness Level: $($consciousnessReport.metrics.self_awareness_level)" -ForegroundColor Magenta
        Write-Host "   Emergence Events: $($consciousnessReport.emergence_events_count)" -ForegroundColor Magenta
        
        return $consciousnessReport
    } else {
        Write-Host " Build failed - cannot test consciousness emergence" -ForegroundColor Red
        return $null
    }
}

# Main execution logic
switch ($Mode) {
    "interactive" {
        Write-Host " AIOS PowerShell Automation Framework - Interactive Mode" -ForegroundColor Cyan
        Write-Host "Available commands:" -ForegroundColor White
        Write-Host "  Start-AIOSAutomationLoop -Iterations 5" -ForegroundColor Green
        Write-Host "  Test-AIOSConsciousnessEmergence" -ForegroundColor Green
        Write-Host ""
    }
    "auto_loop" {
        Start-AIOSAutomationLoop -Iterations $Iterations -UseContainers $ContainerMode -TestType $TestType
    }
    "consciousness_test" {
        Test-AIOSConsciousnessEmergence
    }
    default {
        Write-Host " Unknown mode: $Mode" -ForegroundColor Red
        Write-Host "Available modes: interactive, auto_loop, consciousness_test" -ForegroundColor White
    }
}
