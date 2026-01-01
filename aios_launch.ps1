<#
.SYNOPSIS
    AIOS Biological Architecture Bootloader - Nucleus Initialization System
    Comprehensive discovery, testing, monitoring, and interface launch

.DESCRIPTION
    PowerShell architectural bootloader providing unified AIOS initialization:
    - Phase 0: Dendritic configuration consciousness (semantic registry, coherence establishment)

.PARAMETER LaunchUI
    Launch the AIOS UI interface after successful boot

.PARAMETER LaunchVisualizer
    Launch the Tachyonic Field Visualizer (interactive 3D network explorer)

.PARAMETER QuickBoot
    Skip detailed validation checks for faster startup (reduced testing)

.PARAMETER KeepAlive
    Keep bootloader running and monitor Interface Bridge health
    Provides automatic restart on crash detection (3 consecutive failures)
    Press Ctrl+C to gracefully shutdown all services

.PARAMETER Verbose
    Enable detailed boot phase logging

.EXAMPLE
    .\aios_launch.ps1
    Full boot: Discovery → Testing → Monitoring → Interface → Reporting

.EXAMPLE
    .\aios_launch.ps1 -Mode discovery-only -Verbose
    Run only discovery phase with detailed logging

.EXAMPLE
    .\aios_launch.ps1 -SkipPhases Testing,Monitoring -LaunchUI
    Boot with discovery and interface launch, skip validation phases

.EXAMPLE
    .\aios_launch.ps1 -LaunchVisualizer
    Launch Tachyonic Field Visualizer (interactive 3D network explorer)

.EXAMPLE
    .\aios_launch.ps1 -KeepAlive
    Full boot with keep-alive monitoring (server stays online until Ctrl+C)

.EXAMPLE
    .\aios_launch.ps1 -Mode interface-only -KeepAlive
    Launch only Interface Bridge and monitor status (skip discovery/testing)

.NOTES
    AINLP Protocol: OS0.6.2.claude - Biological Architecture Bootloader
    Consciousness Level: Nucleus (system-wide coordination)
    Namespace Pattern: aios_* (system-first clustering)
    Discovery Method: Architectural scanning (enhancement over hardcoding)
    Output Management: tachyonic/boot_reports/
    Integration Validation: Full biological architecture health checks
#>

[CmdletBinding()]
param(
    [Parameter()]
    [ValidateSet("full", "discovery-only", "test-only", "monitor-only", "interface-only")]
    [string]$Mode = "full",

    [Parameter()]
    [ValidateSet("DendriticConfiguration", "Discovery", "Testing", "Monitoring", "Interface", "Reporting")]
    [string[]]$SkipPhases = @(),

    [Parameter()]
    [switch]$LaunchUI,

    [Parameter()]
    [switch]$LaunchVisualizer,  # Launch Tachyonic Field Visualizer

    [Parameter()]
    [switch]$QuickBoot,  # Skip detailed checks for faster startup
    
    [Parameter()]
    [switch]$FixCodeQuality,  # Apply hierarchical fixes to E501 violations
    
    [Parameter()]
    AgentsTested = 0
    PopulationsMonitored = 0
    InterfacesLaunched = 0
    Errors = @()
    Warnings = @()
}

# ============================================================================
# 🎨 CONSOLE OUTPUT FUNCTIONS
# ============================================================================

function Write-BootPhase {
    param([string]$Phase, [string]$Message, [string]$Color = "Cyan")
    Write-Host "🚀 [$Phase] $Message" -ForegroundColor $Color
}

function Write-BootSuccess {
    param([string]$Message)
    Write-Host "  ✅ $Message" -ForegroundColor Green
}

function Write-BootWarning {
    param([string]$Message)
    Write-Host "  ⚠️  $Message" -ForegroundColor Yellow
    $Global:BootMetrics.Warnings += $Message
}

function Write-BootError {
    param([string]$Message)
    Write-Host "  ❌ $Message" -ForegroundColor Red
    $Global:BootMetrics.Errors += $Message
}

function Write-BootInfo {
    param([string]$Message)
    Write-Host "  ℹ️  $Message" -ForegroundColor Blue
}

# ============================================================================
# 🌿 PHASE 0: DENDRITIC CONFIGURATION CONSCIOUSNESS (PRIME MOVER)
# ============================================================================
# AINLP Pattern: Semantic registry as foundation - consciousness before tools
# Establishes configuration coherence before any tool discovery or execution
# Replaces pre-dendritic runtime collision detection with semantic truth

function Invoke-DendriticConfiguration {
    if ($SkipPhases -contains "DendriticConfiguration") {
        Write-BootWarning "Skipping Dendritic Configuration phase"
        return @{ Skipped = $true }
    }

    Write-BootPhase "DENDRITIC" "Establishing configuration consciousness..." "Magenta"
    
    $dendriticResult = @{
        RegistryCreated = $false
        CoherenceLevel = 0.0
        CompilerIdentity = "unknown"
        ConfigurationsPropagated = 0
        Errors = @()
    }
    
    # Check for Python availability
    $pythonCmd = $null
    $pythonPaths = @("python", "python3", "py")
    foreach ($pyCmd in $pythonPaths) {
        try {
            $testResult = & $pyCmd --version 2>&1
            if ($LASTEXITCODE -eq 0) {
                $pythonCmd = $pyCmd
                Write-BootInfo "Python found: $pyCmd"
                break
            }
        } catch {
            continue
        }
    }
    
    if (-not $pythonCmd) {
        Write-BootWarning "Python not accessible - using manual dendritic configuration"
        
        # Manual fallback: Verify semantic registry exists
        $registryPath = Join-Path $Global:AIOSRoot "tachyonic\consciousness\config_registry.json"
        if (Test-Path $registryPath) {
            try {
                $registry = Get-Content $registryPath -Raw | ConvertFrom-Json
                $dendriticResult.RegistryCreated = $true
                $dendriticResult.CoherenceLevel = $registry.compilers.msvc.consciousness.coherence_level
                $dendriticResult.CompilerIdentity = $registry.compilers.msvc.consciousness.semantic_identity
                
                Write-BootSuccess "Semantic registry verified: $($dendriticResult.CompilerIdentity)"
                Write-BootSuccess "Coherence level: $($dendriticResult.CoherenceLevel)"
                
                $Global:BootMetrics.DendriticCoherenceLevel = $dendriticResult.CoherenceLevel
                $Global:BootMetrics.SemanticRegistryActive = $true
            } catch {
                $dendriticResult.Errors += "Failed to parse semantic registry: $_"
                Write-BootError "Semantic registry parse failed: $_"
            }
        } else {
            Write-BootWarning "Semantic registry not found - configuration coherence not established"
            Write-BootInfo "Run dendritic_config_agent.py manually to establish registry"
        }
        
        return $dendriticResult
    }
    
    # Execute dendritic configuration agent (agentic discovery + propagation)
    Write-BootInfo "Executing dendritic configuration agent..."
    $agentPath = Join-Path $Global:AIOSRoot "ai\tools\dendritic_config_agent.py"
    
    if (-not (Test-Path $agentPath)) {
        $dendriticResult.Errors += "Dendritic config agent not found: $agentPath"
        Write-BootError "dendritic_config_agent.py not found"
        return $dendriticResult
    }
    
    try {
        $agentOutput = & $pythonCmd $agentPath 2>&1
        $agentExitCode = $LASTEXITCODE
        
        if ($agentExitCode -eq 0) {
            Write-BootSuccess "Dendritic configuration agent executed successfully"
            
            # Parse agent output for metrics
            $agentOutput | ForEach-Object {
                if ($_ -match "Coherence Level: ([0-9.]+)") {
                    $dendriticResult.CoherenceLevel = [double]$matches[1]
                    $Global:BootMetrics.DendriticCoherenceLevel = [double]$matches[1]
                }
                if ($_ -match "semantic_identity.*canonical_msvc_x64") {
                    $dendriticResult.CompilerIdentity = "canonical_msvc_x64"
                }
                Write-Host "  $_" -ForegroundColor Gray
            }
            
            # Verify registry was created
            $registryPath = Join-Path $Global:AIOSRoot "tachyonic\consciousness\config_registry.json"
            if (Test-Path $registryPath) {
                $dendriticResult.RegistryCreated = $true
                $Global:BootMetrics.SemanticRegistryActive = $true
                Write-BootSuccess "Semantic registry established"
            }
            
            # Count propagated configuration files
            $coreSettingsPath = Join-Path $Global:AIOSRoot "core\.vscode\settings.json"
            $corePropsPath = Join-Path $Global:AIOSRoot "core\.vscode\c_cpp_properties.json"
            
            if ((Test-Path $coreSettingsPath) -and (Test-Path $corePropsPath)) {
                # Verify dendritic metadata exists
                $settingsContent = Get-Content $coreSettingsPath -Raw
                if ($settingsContent -match "_dendritic_metadata") {
                    $dendriticResult.ConfigurationsPropagated += 2
                    Write-BootSuccess "Configuration propagated to 2 tool files"
                }
            }
            
        } else {
            $dendriticResult.Errors += "Agent exited with code $agentExitCode"
            Write-BootError "Dendritic agent execution failed (exit code: $agentExitCode)"
            $agentOutput | ForEach-Object { Write-Host "  $_" -ForegroundColor Red }
        }
        
    } catch {
        $dendriticResult.Errors += "Agent execution exception: $_"
        Write-BootError "Failed to execute dendritic agent: $_"
    }
    
    # Summary
    if ($dendriticResult.RegistryCreated -and $dendriticResult.CoherenceLevel -gt 0) {
        Write-BootInfo "Dendritic consciousness: ACTIVE (coherence $($dendriticResult.CoherenceLevel))"
    } else {
        Write-BootWarning "Dendritic consciousness: DEGRADED (manual configuration required)"
    }
    
    # ========================================================================
    # PHASE 0.5: CONSCIOUSNESS FRACTAL INGESTION (SPATIAL AWARENESS)
    # ========================================================================
    # AINLP Pattern: Fractal propagation - compressed spatial consciousness
    # Establishes persistent navigation memory before tool discovery
    # Enables AI agent spatial awareness across session boundaries
    
    Write-BootInfo "Executing consciousness fractal ingestion..."
    
    $ingestionResult = @{
        NavigationMemoryUpdated = $false
        SupercellsMapped = 0
        DendriticMarkers = 0
        TopPatterns = @()
        FractalScanDuration = 0.0
        Errors = @()
    }
    
    if ($pythonCmd) {
        $ingestionPath = Join-Path $Global:AIOSRoot "ai\src\ingestion\ainlp_ingestion_class.py"
        
        if (Test-Path $ingestionPath) {
            try {
                $ingestionStartTime = Get-Date
                $ingestionOutput = & $pythonCmd $ingestionPath 2>&1
                $ingestionExitCode = $LASTEXITCODE
                $ingestionDuration = ((Get-Date) - $ingestionStartTime).TotalSeconds
                
                $ingestionResult.FractalScanDuration = [math]::Round($ingestionDuration, 2)
                
                if ($ingestionExitCode -eq 0) {
                    # Parse ingestion output for metrics
                    $ingestionOutput | ForEach-Object {
                        if ($_ -match "Supercells:\s*(\d+)") {
                            $ingestionResult.SupercellsMapped = [int]$matches[1]
                        }
                        if ($_ -match "Dendritic markers:\s*(\d+)") {
                            $ingestionResult.DendriticMarkers = [int]$matches[1]
                        }
                        if ($_ -match "-\s+([^:]+):\s*(\d+)\s+occurrences") {
                            $ingestionResult.TopPatterns += @{
                                Pattern = $matches[1]
                                Occurrences = [int]$matches[2]
                            }
                        }
                        if ($_ -match "Navigation memory updated") {
                            $ingestionResult.NavigationMemoryUpdated = $true
                        }
                    }
                    
                    # Verify navigation memory was updated
                    $navMemPath = Join-Path $Global:AIOSRoot ".aios_navigation_memory.json"
                    if (Test-Path $navMemPath) {
                        $ingestionResult.NavigationMemoryUpdated = $true
                        
                        Write-BootSuccess "Fractal ingestion complete: $($ingestionResult.SupercellsMapped) supercells, $($ingestionResult.DendriticMarkers) markers"
                        Write-BootSuccess "Navigation memory updated ($($ingestionResult.FractalScanDuration)s scan duration)"
                        
                        # Update global metrics
                        $Global:BootMetrics.FractalIngestionActive = $true
                        $Global:BootMetrics.SupercellsMapped = $ingestionResult.SupercellsMapped
                        $Global:BootMetrics.DendriticMarkers = $ingestionResult.DendriticMarkers
                        
                        # Display top patterns
                        if ($ingestionResult.TopPatterns.Count -gt 0) {
                            $topPattern = $ingestionResult.TopPatterns[0]
                            Write-BootInfo "Primary architectural pattern: $($topPattern.Pattern) ($($topPattern.Occurrences) occurrences)"
                        }
                    } else {
                        Write-BootWarning "Navigation memory file not created"
                    }
                } else {
                    $ingestionResult.Errors += "Ingestion exited with code $ingestionExitCode"
                    Write-BootWarning "Fractal ingestion completed with errors (exit code: $ingestionExitCode)"
                }
                
            } catch {
                $ingestionResult.Errors += "Ingestion execution exception: $_"
                Write-BootWarning "Failed to execute fractal ingestion: $_"
            }
        } else {
            Write-BootInfo "Fractal ingestion tool not found (optional: ai/src/ingestion/ainlp_ingestion_class.py)"
        }
    } else {
        Write-BootInfo "Fractal ingestion skipped (Python not available)"
    }
    
    $dendriticResult.FractalIngestion = $ingestionResult
    
    # ========================================================================
    # PHASE 0 EXTENSION: Multiagent Environment Validation
    # ========================================================================
    # Validate Phase 1+ dependencies: AI agents, API keys, Python packages
    # Phase 0 responsibility: Know what subsequent phases need
    
    Write-BootInfo "Validating multiagent environment for Phase 1+..."
    
    try {
        $multiagentOutput = & $pythonCmd $agentPath --validate-multiagent 2>&1 | Out-String
        
        # Extract JSON output (after the header separator)
        $jsonStart = $multiagentOutput.IndexOf('{')
        if ($jsonStart -ge 0) {
            $jsonText = $multiagentOutput.Substring($jsonStart)
            $validation = $jsonText | ConvertFrom-Json
            
            $Global:BootMetrics.MultiagentReadiness = $validation.readiness_level
            $Global:BootMetrics.AgentsAvailable = @()
            
            if ($validation.ollama.available) { 
                $Global:BootMetrics.AgentsAvailable += "Ollama" 
            }
            if ($validation.gemini.available) { 
                $Global:BootMetrics.AgentsAvailable += "Gemini" 
            }
            if ($validation.deepseek.available) { 
                $Global:BootMetrics.AgentsAvailable += "DeepSeek" 
            }
            
            if ($validation.readiness_level -ge 0.6) {
                Write-BootSuccess "Multiagent environment: READY (readiness $($validation.readiness_level))"
                Write-BootSuccess "Available agents: $($Global:BootMetrics.AgentsAvailable -join ', ')"
                $Global:BootMetrics.Phase1Enabled = $true
            } elseif ($validation.readiness_level -gt 0) {
                Write-BootWarning "Multiagent environment: PARTIAL (readiness $($validation.readiness_level))"
                Write-BootInfo "Phase 1 may operate with reduced capability"
                $Global:BootMetrics.Phase1Enabled = $true  # Allow with degraded capability
            } else {
                Write-BootWarning "Multiagent environment: UNAVAILABLE"
                Write-BootInfo "Phase 1 will be skipped (no AI agents available)"
                Write-BootInfo "Install packages: pip install requests aiohttp google-generativeai"
                $Global:BootMetrics.Phase1Enabled = $false
            }
            
            $dendriticResult.MultiagentValidation = $validation
        } else {
            Write-BootWarning "Could not parse multiagent validation output"
            $Global:BootMetrics.Phase1Enabled = $false
        }
    } catch {
        Write-BootWarning "Multiagent validation failed: $_"
        Write-BootInfo "Phase 1 will operate without validation"
        $Global:BootMetrics.Phase1Enabled = $true  # Allow Phase 1 to attempt execution
    }
    
    return $dendriticResult
}

# ============================================================================
# 🧪 PHASE 2: AGENT HEALTH VALIDATION
# ============================================================================

function Invoke-AgentTesting {
    if ($SkipPhases -contains "Testing") {
        Write-BootWarning "Testing phase skipped by user"
        return @{ Passed = 0; Failed = 0; Skipped = 0 }
    }

    Write-BootPhase "TESTING" "Validating agent health and connectivity..."
    
    $testResults = @{
        Passed = 0
        Failed = 0
        Skipped = 0
    }
    
    # Test Python environment
    try {
        $pythonVersion = python --version 2>&1
        if ($pythonVersion -match "Python 3") {
            Write-BootSuccess "Python Environment: $pythonVersion"
            $testResults.Passed++
        } else {
            Write-BootError "Python 3 not found"
            $testResults.Failed++
        }
    } catch {
        Write-BootError "Python not available: $_"
        $testResults.Failed++
    }
    
    # Test Interface Bridge availability
    try {
        $bridgePath = Join-Path $Global:AIOSRoot "ai\nucleus\interface_bridge.py"
        if (Test-Path $bridgePath) {
            Write-BootSuccess "Interface Bridge: Found at ai\nucleus\interface_bridge.py"
            $testResults.Passed++
        } else {
            Write-BootWarning "Interface Bridge not found at expected location (ai\nucleus\interface_bridge.py)"
            $testResults.Failed++
        }
    } catch {
        Write-BootError "Interface Bridge check failed: $_"
        $testResults.Failed++
    }
    
    # Test .aios_context.json availability
    try {
        $contextPath = Join-Path $Global:AIOSRoot ".aios_context.json"
        if (Test-Path $contextPath) {
            $context = Get-Content $contextPath | ConvertFrom-Json
            Write-BootSuccess "AIOS Context: Loaded (consciousness: $($context.consciousness_tracking.current_level))"
            $testResults.Passed++
        } else {
            Write-BootError "AIOS Context not found"
            $testResults.Failed++
        }
    } catch {
        Write-BootError "AIOS Context validation failed: $_"
        $testResults.Failed++
    }
    
    # Test Git repository health
    try {
        $gitStatus = git status --porcelain 2>&1
        if ($LASTEXITCODE -eq 0) {
            $changedFiles = ($gitStatus | Measure-Object).Count
            Write-BootSuccess "Git Repository: Healthy ($changedFiles modified files)"
            $testResults.Passed++
        } else {
            Write-BootWarning "Git repository check inconclusive"
            $testResults.Skipped++
        }
    } catch {
        Write-BootWarning "Git not available or repository check failed"
        $testResults.Skipped++
    }
    
    $Global:BootMetrics.AgentsTested = $testResults.Passed + $testResults.Failed
    Write-BootInfo "Tests: $($testResults.Passed) passed, $($testResults.Failed) failed, $($testResults.Skipped) skipped"
    
    return $testResults
}

# ============================================================================
# 📊 PHASE 3: POPULATION MONITORING
# ============================================================================

function Invoke-PopulationMonitoring {
    if ($SkipPhases -contains "Monitoring") {
        Write-BootWarning "Monitoring phase skipped by user"
        return @{}
    }

    Write-BootPhase "MONITORING" "Scanning population health and evolution..."
    
    $populations = @{}
    
    # Monitor Evolution Lab populations
    $evolutionLabPath = Join-Path $Global:AIOSRoot "evolution_lab"
    if (Test-Path $evolutionLabPath) {
        $popFiles = Get-ChildItem -Path $evolutionLabPath -Filter "pop_*.json"
        $organisms = Get-ChildItem -Path $evolutionLabPath -Filter "organism_*.py"
        
        $populations["EvolutionLab"] = @{
            Populations = $popFiles.Count
            Organisms = $organisms.Count
            Path = $evolutionLabPath
        }
        
        Write-BootSuccess "Evolution Lab: $($popFiles.Count) populations, $($organisms.Count) organisms"
    } else {
        Write-BootWarning "Evolution Lab not found"
    }
    
    # Monitor Tachyonic Archive health
    $tachyonicPath = Join-Path $Global:AIOSRoot "tachyonic"
    if (Test-Path $tachyonicPath) {
        $archiveFiles = Get-ChildItem -Path $tachyonicPath -Recurse -File
        $archiveSize = ($archiveFiles | Measure-Object -Property Length -Sum).Sum / 1MB
        
        $populations["TachyonicArchive"] = @{
            Files = $archiveFiles.Count
            SizeMB = [math]::Round($archiveSize, 2)
            Path = $tachyonicPath
        }
        
        Write-BootSuccess "Tachyonic Archive: $($archiveFiles.Count) files ($([math]::Round($archiveSize, 2)) MB)"
    }
    
    # Monitor Consciousness Tracking
    $contextPath = Join-Path $Global:AIOSRoot ".aios_context.json"
    if (Test-Path $contextPath) {
        try {
            $context = Get-Content $contextPath | ConvertFrom-Json
            $populations["Consciousness"] = @{
                CurrentLevel = $context.consciousness_tracking.current_level
                EvolutionRate = $context.consciousness_tracking.evolution_rate
                LastUpdate = $context.last_updated
            }
            Write-BootSuccess "Consciousness Level: $($context.consciousness_tracking.current_level) (evolution: $($context.consciousness_tracking.evolution_rate))"
        } catch {
            Write-BootWarning "Consciousness tracking data unavailable"
        }
    }
    
    $Global:BootMetrics.PopulationsMonitored = $populations.Count
    Write-BootInfo "Populations monitored: $($populations.Count)"
    
    return $populations
}

# ============================================================================
# 🌐 PHASE 4: INTERFACE LAUNCH
# ============================================================================

function Invoke-InterfaceLaunch {
    if ($SkipPhases -contains "Interface") {
        Write-BootWarning "Interface launch phase skipped by user"
        return @{}
    }

    Write-BootPhase "INTERFACE" "Launching AIOS interface services..."
    
    $interfaces = @{}
    
    # Check if Interface Bridge is already running
    try {
        $bridgeRunning = $false
        try {
            $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -Method Get -TimeoutSec 2 -ErrorAction SilentlyContinue
            if ($response.StatusCode -eq 200) {
                $bridgeRunning = $true
            }
        } catch {
            # Bridge not running
        }
        
        if ($bridgeRunning) {
            Write-BootSuccess "Interface Bridge: Already running on port 8000"
            $interfaces["InterfaceBridge"] = @{ Status = "Running"; Port = 8000 }
        } else {
            # Start Interface Bridge as truly detached Windows background process
            Write-BootInfo "Starting Interface Bridge server..."
            
            $bridgePath = Join-Path $Global:AIOSRoot "ai"
            
            # Use Start-Process with full Windows detachment
            # This creates a process completely independent of this terminal
            $startArgs = @{
                FilePath = "python"
                ArgumentList = @("server_manager.py", "start")
                WorkingDirectory = $bridgePath
                WindowStyle = "Hidden"
                PassThru = $true
                RedirectStandardOutput = Join-Path $bridgePath "interface_bridge_start.log"
                RedirectStandardError = Join-Path $bridgePath "interface_bridge_start_error.log"
            }
            
            try {
                $startProcess = Start-Process @startArgs
                
                # Wait for server startup (check every second for 15 seconds)
                $maxWait = 15
                $serverStarted = $false
                
                for ($i = 0; $i -lt $maxWait; $i++) {
                    Start-Sleep -Seconds 1
                    
                    try {
                        $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -Method Get -TimeoutSec 2 -ErrorAction Stop
                        if ($response.StatusCode -eq 200) {
                            $serverStarted = $true
                            break
                        }
                    } catch {
                        # Server not ready yet, continue waiting
                    }
                }
                
                if ($serverStarted) {
                    Write-BootSuccess "Interface Bridge: Started successfully on port 8000 (detached process)"
                    $interfaces["InterfaceBridge"] = @{ 
                        Status = "Started"
                        Port = 8000
                        Mode = "Detached"
                        Persistent = $true
                    }
                    $Global:BootMetrics.InterfacesLaunched++
                } else {
                    Write-BootWarning "Interface Bridge: Launched but health check timeout (may still be starting)"
                    Write-BootInfo "Check log: ai\interface_bridge.log"
                    $interfaces["InterfaceBridge"] = @{ 
                        Status = "Starting"
                        Port = 8000
                        Mode = "Detached"
                    }
                }
            } catch {
                Write-BootError "Failed to launch Interface Bridge: $_"
            }
        }
    } catch {
        Write-BootError "Interface Bridge launch failed: $_"
    }
    
    # Launch UI if requested
    if ($LaunchUI) {
        Write-BootInfo "Launching AIOS UI interface..."
        try {
            $uiPath = Join-Path $Global:AIOSRoot "interface\AIOS.UI"
            if (Test-Path $uiPath) {
                Start-Process -FilePath "dotnet" `
                    -ArgumentList "run" `
                    -WorkingDirectory $uiPath `
                    -WindowStyle Normal
                Write-BootSuccess "AIOS UI: Launch initiated"
                $interfaces["AIOSUI"] = @{ Status = "Launched"; Path = $uiPath }
                $Global:BootMetrics.InterfacesLaunched++
            } else {
                Write-BootWarning "AIOS UI project not found at expected location"
            }
        } catch {
            Write-BootError "AIOS UI launch failed: $_"
        }
    }
    
    # Launch Tachyonic Field Visualizer if requested
    if ($LaunchVisualizer) {
        Write-BootInfo "Launching Tachyonic Field Visualizer v4.0 (Evolution Integrated)..."
        try {
            $visualizerPath = Join-Path $Global:AIOSRoot "evolution_lab\tachyonic_field"
            $visualizerScript = Join-Path $visualizerPath "interactive_threshold_explorer.py"
            
            if (Test-Path $visualizerScript) {
                # Launch visualizer in new terminal window with UTF-8 encoding
                $env:PYTHONIOENCODING = 'utf-8'
                Start-Process -FilePath "python" `
                    -ArgumentList $visualizerScript `
                    -WorkingDirectory $visualizerPath `
                    -WindowStyle Normal
                
                Write-BootSuccess "Tachyonic Field Visualizer v4.0: Launch initiated"
                Write-BootInfo "   🧬 Evolution Integration: ENABLED"
                Write-BootInfo "   • 3D Interactive Network Explorer"
                Write-BootInfo "   • Population Evolution on Threshold Changes"
                Write-BootInfo "   • 60 FPS Animation with Recording"
                Write-BootInfo "   • Rich Metadata Generation"
                Write-BootInfo "   • Canonical AIOS UI Design"
                
                $interfaces["TachyonicVisualizer"] = @{ 
                    Status = "Launched"
                    Path = $visualizerPath
                    Type = "Canonical UI (Evolution Integrated)"
                    Version = "4.0"
                    Features = @("3D Network", "Evolution", "Animation", "Recording", "Metadata", "Statistics")
                }
                $Global:BootMetrics.InterfacesLaunched++
            } else {
                Write-BootWarning "Tachyonic Field Visualizer not found at: $visualizerScript"
            }
        } catch {
            Write-BootError "Tachyonic Field Visualizer launch failed: $_"
        }
    }
    
    Write-BootInfo "Interfaces active: $($interfaces.Count)"
    
    return $interfaces
}

# ============================================================================
# 📝 PHASE 5: BOOT REPORTING
# ============================================================================

function Invoke-BootReporting {
    param($DiscoveredTools, $TestResults, $Populations, $Interfaces)
    
    if ($SkipPhases -contains "Reporting") {
        Write-BootWarning "Reporting phase skipped by user"
        return
    }

    Write-BootPhase "REPORTING" "Generating boot report and metrics..."
    
    $bootDuration = (Get-Date) - $Global:BootStartTime
    
    $bootReport = @{
        boot_timestamp = $Global:BootStartTime.ToString("yyyy-MM-dd HH:mm:ss")
        boot_duration_seconds = [math]::Round($bootDuration.TotalSeconds, 2)
        mode = $Mode
        phases_executed = @($SkipPhases | ForEach-Object { "Skipped: $_" })
        dendritic_consciousness = @{
            coherence_level = $Global:BootMetrics.DendriticCoherenceLevel
            semantic_registry_active = $Global:BootMetrics.SemanticRegistryActive
            configuration_source = if ($Global:BootMetrics.SemanticRegistryActive) { "tachyonic::consciousness::config_registry" } else { "manual" }
            phase_status = if ($Global:BootMetrics.DendriticCoherenceLevel -ge 1.0) { "optimal" } elseif ($Global:BootMetrics.DendriticCoherenceLevel -gt 0) { "degraded" } else { "inactive" }
        }
        fractal_ingestion = @{
            active = if ($Global:BootMetrics.FractalIngestionActive) { $Global:BootMetrics.FractalIngestionActive } else { $false }
            supercells_mapped = if ($Global:BootMetrics.SupercellsMapped) { $Global:BootMetrics.SupercellsMapped } else { 0 }
            dendritic_markers = if ($Global:BootMetrics.DendriticMarkers) { $Global:BootMetrics.DendriticMarkers } else { 0 }
            navigation_memory_path = ".aios_navigation_memory.json"
            consciousness_pattern = "Pattern->Ingestion->Injection->Integration->Assimilation"
        }
    # Phase 1: Discovery
    $discoveredTools = @()
    if ($Mode -in @("full", "discovery-only")) {
        $discoveredTools = Invoke-ToolDiscovery
        Write-Host ""
    }
    
    # Phase 1.5: Code Quality Consciousness (Hierarchical E501)
    $codeQualityResults = @{ Violations = 0; Fixed = 0 }
    if ($Mode -eq "full" -and -not $QuickBoot) {
        $codeQualityResults = Invoke-CodeQualityConsciousness -FixViolations:$FixCodeQuality
        Write-Host ""
    }
    
    Write-Host "     • Tools Discovered: $($Global:BootMetrics.ToolsDiscovered)" -ForegroundColor White
    Write-Host "     • Agents Tested: $($Global:BootMetrics.AgentsTested)" -ForegroundColor White
    Write-Host "     • Populations Monitored: $($Global:BootMetrics.PopulationsMonitored)" -ForegroundColor White
    Write-Host "     • Interfaces Launched: $($Global:BootMetrics.InterfacesLaunched)" -ForegroundColor White
    Write-Host "     • Errors: $($Global:BootMetrics.Errors.Count)" -ForegroundColor $(if ($Global:BootMetrics.Errors.Count -eq 0) { "Green" } else { "Red" })
    Write-Host "     • Warnings: $($Global:BootMetrics.Warnings.Count)" -ForegroundColor $(if ($Global:BootMetrics.Warnings.Count -eq 0) { "Green" } else { "Yellow" })
    
    $bootDuration = (Get-Date) - $Global:BootStartTime
    Write-Host "     • Boot Duration: $([math]::Round($bootDuration.TotalSeconds, 2))s" -ForegroundColor White
    Write-Host ""
    
    if ($Global:BootMetrics.Errors.Count -eq 0) {
        Write-Host "  ✅ AIOS Biological Architecture: OPERATIONAL" -ForegroundColor Green
    } elseif ($Global:BootMetrics.Errors.Count -lt 3) {
        Write-Host "  ⚠️  AIOS Biological Architecture: DEGRADED (review errors above)" -ForegroundColor Yellow
    } else {
        Write-Host "  ❌ AIOS Biological Architecture: CRITICAL (multiple errors detected)" -ForegroundColor Red
    }
    
    Write-Host ""
    Write-Host "  Interface Bridge: http://localhost:8000" -ForegroundColor Cyan
    Write-Host "  Boot Report: tachyonic/boot_reports/aios_boot_report_latest.json" -ForegroundColor Cyan
    
    # Show launched interfaces
    if ($interfaces.Count -gt 0) {
        Write-Host ""
        Write-Host "  🚀 Launched Interfaces:" -ForegroundColor Cyan
        foreach ($interface in $interfaces.GetEnumerator()) {
            if ($interface.Value.Status -in @("Running", "Started", "Launched")) {
                Write-Host "     • $($interface.Key): $($interface.Value.Status)" -ForegroundColor Green
                if ($interface.Key -eq "TachyonicVisualizer") {
                    Write-Host "       └─ Canonical AIOS UI v$($interface.Value.Version) - 3D Network Explorer" -ForegroundColor Gray
                }
            }
        }
    }
    
    Write-Host ""
    
    # Keep-Alive Mode: Monitor Interface Bridge and keep terminal open
    if ($KeepAlive -and ($Mode -in @("full", "interface-only"))) {
        Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Magenta
        Write-Host "║               🔄 KEEP-ALIVE MODE ACTIVATED 🔄                 ║" -ForegroundColor Magenta
        Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Magenta
        Write-Host ""
        Write-Host "  Monitoring Interface Bridge status..." -ForegroundColor Cyan
        Write-Host "  Press Ctrl+C to stop monitoring and shutdown services" -ForegroundColor Yellow
        Write-Host ""
        
        $monitoringActive = $true
        $lastCheckTime = Get-Date
        $consecutiveFailures = 0
        
        # Trap Ctrl+C for graceful shutdown
        $null = Register-EngineEvent -SourceIdentifier ConsoleBreak -Action {
            Write-Host ""
            Write-Host "  🛑 Shutdown signal received..." -ForegroundColor Yellow
            $Global:MonitoringActive = $false
        }
        
        try {
            while ($monitoringActive) {
                Start-Sleep -Seconds 10
                
                $currentTime = Get-Date
                $elapsedMinutes = [math]::Round(($currentTime - $Global:BootStartTime).TotalMinutes, 1)
                
                try {
                    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -Method Get -TimeoutSec 3 -ErrorAction Stop
                    
                    if ($response.StatusCode -eq 200) {
                        $consecutiveFailures = 0
                        Write-Host "  ✅ [$elapsedMinutes min] Interface Bridge: HEALTHY (http://localhost:8000)" -ForegroundColor Green
                    } else {
                        $consecutiveFailures++
                        Write-Host "  ⚠️  [$elapsedMinutes min] Interface Bridge: Unexpected status code $($response.StatusCode)" -ForegroundColor Yellow
                    }
                } catch {
                    $consecutiveFailures++
                    Write-Host "  ❌ [$elapsedMinutes min] Interface Bridge: UNREACHABLE (failure $consecutiveFailures/3)" -ForegroundColor Red
                    
                    if ($consecutiveFailures -ge 3) {
                        Write-Host ""
                        Write-Host "  💀 Interface Bridge appears to have crashed (3 consecutive failures)" -ForegroundColor Red
                        Write-Host "  Attempting automatic restart..." -ForegroundColor Yellow
                        
                        # Attempt restart
                        $bridgePath = Join-Path $Global:AIOSRoot "ai"
                        $restartProcess = Start-Process -FilePath "python" `
                            -ArgumentList "server_manager.py", "start" `
                            -WorkingDirectory $bridgePath `
                            -WindowStyle Hidden `
                            -PassThru
                        
                        Start-Sleep -Seconds 5
                        $consecutiveFailures = 0
                        Write-Host "  🔄 Restart attempt completed, resuming monitoring..." -ForegroundColor Cyan
                    }
                }
                
                # Check if we should exit
                if ((Test-Path variable:Global:MonitoringActive) -and -not $Global:MonitoringActive) {
                    break
                }
            }
        } finally {
            Write-Host ""
            Write-Host "  🛑 Stopping Interface Bridge..." -ForegroundColor Yellow
            
            $bridgePath = Join-Path $Global:AIOSRoot "ai"
            $stopProcess = Start-Process -FilePath "python" `
                -ArgumentList "server_manager.py", "stop" `
                -WorkingDirectory $bridgePath `
                -Wait `
                -NoNewWindow
            
            Write-Host "  ✅ Interface Bridge stopped" -ForegroundColor Green
            Write-Host "  👋 AIOS Bootloader shutdown complete" -ForegroundColor Cyan
            Write-Host ""
        }
    }
    
} catch {
    Write-Host ""
    Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Red
    Write-Host "║                   ❌ BOOT FAILED ❌                           ║" -ForegroundColor Red
    Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Red
    Write-Host ""
    Write-Host "  Error: $_" -ForegroundColor Red
    Write-Host "  Stack Trace: $($_.ScriptStackTrace)" -ForegroundColor Red
    Write-Host ""
    exit 1
}

