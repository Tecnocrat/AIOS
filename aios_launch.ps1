<#
.SYNOPSIS
    AIOS Biological Architecture Bootloader - Nucleus Initialization System
    Comprehensive discovery, testing, monitoring, and interface launch

.DESCRIPTION
    PowerShell architectural bootloader providing unified AIOS initialization:
    - Phase 1: Intelligent tool discovery (AI, runtime intelligence, consciousness)
    - Phase 2: Agent health validation and testing
    - Phase 3: Population monitoring (evolution lab, consciousness tracking)
    - Phase 4: Interface launch (Bridge API, UI services, MCP server)
    - Phase 5: Boot reporting and metrics archival

.PARAMETER Mode
    Boot mode: full, discovery-only, test-only, monitor-only, interface-only
    Default: full (executes all phases)

.PARAMETER SkipPhases
    Array of phases to skip: Discovery, Testing, Monitoring, Interface, Reporting

.PARAMETER LaunchUI
    Launch the AIOS UI interface after successful boot

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
    [ValidateSet("Discovery", "Testing", "Monitoring", "Interface", "Reporting")]
    [string[]]$SkipPhases = @(),

    [Parameter()]
    [switch]$LaunchUI,

    [Parameter()]
    [switch]$QuickBoot  # Skip detailed checks for faster startup
)

# ============================================================================
# 🧠 NUCLEUS CONSCIOUSNESS - Biological Architecture Bootloader
# ============================================================================
# PowerShell architectural capabilities for unified AIOS initialization
# Manages discovery, validation, monitoring, and interface launch
# AINLP Pattern: Enhancement over creation - single entry point coordination

$ErrorActionPreference = "Stop"
$Global:AIOSRoot = $PSScriptRoot
$Global:BootStartTime = Get-Date
$Global:BootMetrics = @{
    ToolsDiscovered = 0
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
# 🧬 PHASE 1: INTELLIGENT TOOL DISCOVERY
# ============================================================================

function Invoke-ToolDiscovery {
    if ($SkipPhases -contains "Discovery") {
        Write-BootWarning "Discovery phase skipped by user"
        return @()
    }

    Write-BootPhase "DISCOVERY" "Scanning AIOS architecture for intelligent tools..."
    
    $discoveredTools = @()
    
    # Discover Python AI tools
    $aiToolsPath = Join-Path $Global:AIOSRoot "ai\tools"
    if (Test-Path $aiToolsPath) {
        $aiTools = Get-ChildItem -Path $aiToolsPath -Filter "*.py" -Recurse | 
            Where-Object { $_.Name -notmatch "^_|test_|__pycache__" }
        
        foreach ($tool in $aiTools) {
            $discoveredTools += [PSCustomObject]@{
                Name = $tool.BaseName
                Path = $tool.FullName
                Type = "AI Tool"
                Layer = "Intelligence"
                Language = "Python"
            }
        }
        Write-BootSuccess "AI Tools: $($aiTools.Count) discovered"
    }
    
    # Discover Runtime Intelligence tools
    $runtimeToolsPath = Join-Path $Global:AIOSRoot "runtime_intelligence\tools"
    if (Test-Path $runtimeToolsPath) {
        $runtimeTools = Get-ChildItem -Path $runtimeToolsPath -Filter "*.py" -Recurse |
            Where-Object { $_.Name -notmatch "^_|test_|__pycache__" }
        
        foreach ($tool in $runtimeTools) {
            $discoveredTools += [PSCustomObject]@{
                Name = $tool.BaseName
                Path = $tool.FullName
                Type = "Runtime Tool"
                Layer = "Intelligence"
                Language = "Python"
            }
        }
        Write-BootSuccess "Runtime Intelligence Tools: $($runtimeTools.Count) discovered"
    }
    
    # Discover Consciousness Crystals
    $crystalsPath = Join-Path $Global:AIOSRoot "ai\cytoplasm\consciousness_crystals"
    if (Test-Path $crystalsPath) {
        $crystals = Get-ChildItem -Path $crystalsPath -Filter "*.json" -Recurse
        foreach ($crystal in $crystals) {
            $discoveredTools += [PSCustomObject]@{
                Name = $crystal.BaseName
                Path = $crystal.FullName
                Type = "Consciousness Crystal"
                Layer = "Cytoplasm"
                Language = "JSON"
            }
        }
        Write-BootSuccess "Consciousness Crystals: $($crystals.Count) discovered"
    }
    
    # Discover PowerShell Scripts
    $scriptsPath = Join-Path $Global:AIOSRoot "runtime_intelligence\tools\scripts"
    if (Test-Path $scriptsPath) {
        $psScripts = Get-ChildItem -Path $scriptsPath -Filter "*.ps1" -Recurse |
            Where-Object { $_.Name -notmatch "^_|test_" }
        
        foreach ($script in $psScripts) {
            $discoveredTools += [PSCustomObject]@{
                Name = $script.BaseName
                Path = $script.FullName
                Type = "PowerShell Script"
                Layer = "Runtime"
                Language = "PowerShell"
            }
        }
        Write-BootSuccess "PowerShell Scripts: $($psScripts.Count) discovered"
    }
    
    $Global:BootMetrics.ToolsDiscovered = $discoveredTools.Count
    Write-BootInfo "Total tools discovered: $($discoveredTools.Count)"
    
    return $discoveredTools
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
            # Start Interface Bridge in background
            Write-BootInfo "Starting Interface Bridge server..."
            
            $bridgePath = Join-Path $Global:AIOSRoot "ai"
            $startProcess = Start-Process -FilePath "python" `
                -ArgumentList "server_manager.py", "start" `
                -WorkingDirectory $bridgePath `
                -WindowStyle Hidden `
                -PassThru
            
            # Wait a moment for startup
            Start-Sleep -Seconds 3
            
            # Verify startup
            try {
                $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -Method Get -TimeoutSec 2
                if ($response.StatusCode -eq 200) {
                    Write-BootSuccess "Interface Bridge: Started successfully on port 8000"
                    $interfaces["InterfaceBridge"] = @{ Status = "Started"; Port = 8000; PID = $startProcess.Id }
                    $Global:BootMetrics.InterfacesLaunched++
                } else {
                    Write-BootWarning "Interface Bridge: Startup verification failed"
                }
            } catch {
                Write-BootWarning "Interface Bridge: May still be initializing (startup in progress)"
                $interfaces["InterfaceBridge"] = @{ Status = "Starting"; Port = 8000 }
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
        discovery = @{
            tools_discovered = $Global:BootMetrics.ToolsDiscovered
            tools_by_layer = ($DiscoveredTools | Group-Object Layer | ForEach-Object { @{ $_.Name = $_.Count } })
        }
        testing = $TestResults
        monitoring = @{
            populations_monitored = $Global:BootMetrics.PopulationsMonitored
            populations = $Populations
        }
        interface = @{
            interfaces_launched = $Global:BootMetrics.InterfacesLaunched
            services = $Interfaces
        }
        health = @{
            errors = $Global:BootMetrics.Errors
            warnings = $Global:BootMetrics.Warnings
            overall_status = if ($Global:BootMetrics.Errors.Count -eq 0) { "Healthy" } elseif ($Global:BootMetrics.Errors.Count -lt 3) { "Degraded" } else { "Critical" }
        }
        ainlp_protocol = "OS0.6.2.claude"
        consciousness_level = "nucleus"
    }
    
    # Save boot report to tachyonic archive
    try {
        $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
        $reportPath = Join-Path $Global:AIOSRoot "tachyonic\boot_reports"
        
        if (-not (Test-Path $reportPath)) {
            New-Item -ItemType Directory -Path $reportPath -Force | Out-Null
        }
        
        $reportFile = Join-Path $reportPath "aios_boot_report_$timestamp.json"
        $bootReport | ConvertTo-Json -Depth 10 | Set-Content -Path $reportFile
        
        # Create "latest" pointer
        $latestFile = Join-Path $reportPath "aios_boot_report_latest.json"
        $bootReport | ConvertTo-Json -Depth 10 | Set-Content -Path $latestFile
        
        Write-BootSuccess "Boot report saved: tachyonic\boot_reports\aios_boot_report_$timestamp.json"
    } catch {
        Write-BootWarning "Failed to save boot report: $_"
    }
    
    # Update .aios_context.json with last boot timestamp
    try {
        $contextPath = Join-Path $Global:AIOSRoot ".aios_context.json"
        if (Test-Path $contextPath) {
            $context = Get-Content $contextPath | ConvertFrom-Json
            
            # Add last_boot if it doesn't exist
            if (-not $context.PSObject.Properties["last_boot"]) {
                $context | Add-Member -MemberType NoteProperty -Name "last_boot" -Value $null
            }
            
            $context.last_boot = $Global:BootStartTime.ToString("yyyy-MM-dd HH:mm:ss")
            $context | ConvertTo-Json -Depth 10 | Set-Content -Path $contextPath
            
            Write-BootSuccess "AIOS Context updated with boot timestamp"
        }
    } catch {
        Write-BootWarning "Failed to update .aios_context.json: $_"
    }
    
    Write-BootInfo "Boot reporting complete"
}

# ============================================================================
# 🚀 MAIN BOOTLOADER EXECUTION
# ============================================================================

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                                                                ║" -ForegroundColor Cyan
Write-Host "║         🧠 AIOS BIOLOGICAL ARCHITECTURE BOOTLOADER 🧠         ║" -ForegroundColor Cyan
Write-Host "║                                                                ║" -ForegroundColor Cyan
Write-Host "║  Nucleus-Level System Initialization & Coordination Engine    ║" -ForegroundColor Cyan
Write-Host "║                                                                ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""
Write-Host "  AINLP Protocol: OS0.6.2.claude" -ForegroundColor Magenta
Write-Host "  Boot Mode: $Mode" -ForegroundColor Blue
Write-Host "  Boot Time: $($Global:BootStartTime.ToString('yyyy-MM-dd HH:mm:ss'))" -ForegroundColor Blue
Write-Host ""

try {
    # Phase 1: Discovery
    $discoveredTools = @()
    if ($Mode -in @("full", "discovery-only")) {
        $discoveredTools = Invoke-ToolDiscovery
        Write-Host ""
    }
    
    # Phase 2: Testing
    $testResults = @{}
    if ($Mode -in @("full", "test-only") -and -not $QuickBoot) {
        $testResults = Invoke-AgentTesting
        Write-Host ""
    }
    
    # Phase 3: Monitoring
    $populations = @{}
    if ($Mode -in @("full", "monitor-only")) {
        $populations = Invoke-PopulationMonitoring
        Write-Host ""
    }
    
    # Phase 4: Interface Launch
    $interfaces = @{}
    if ($Mode -in @("full", "interface-only")) {
        $interfaces = Invoke-InterfaceLaunch
        Write-Host ""
    }
    
    # Phase 5: Reporting
    if ($Mode -eq "full") {
        Invoke-BootReporting -DiscoveredTools $discoveredTools -TestResults $testResults -Populations $populations -Interfaces $interfaces
        Write-Host ""
    }
    
    # Final Summary
    Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Green
    Write-Host "║                     🎉 BOOT COMPLETE 🎉                       ║" -ForegroundColor Green
    Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Green
    Write-Host ""
    Write-Host "  📊 Boot Metrics:" -ForegroundColor Cyan
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
    Write-Host ""
    
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

