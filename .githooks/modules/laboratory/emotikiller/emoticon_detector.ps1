# AIOS GitHook Emotikiller - Core Detection Module
# STRICT NO EMOTICON POLICY ENFORCED
# PowerShell implementation of emoticon detection for GitHook integration

param(
    [Parameter(Mandatory=$false)]
    [string[]]$FilePaths = @(),
    
    [Parameter(Mandatory=$false)]
    [switch]$ScanStaged,
    
    [Parameter(Mandatory=$false)]
    [switch]$AutoCleanup,
    
    [Parameter(Mandatory=$false)]
    [string]$ConfigPath = "",
    
    [Parameter(Mandatory=$false)]
    [switch]$ReturnResults
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# Global configuration and state
$script:Config = $null
$script:CompiledPatterns = @{}
$script:DetectionStats = @{
    FilesScanned = 0
    ViolationsFound = 0
    TotalEmoticons = 0
    ProcessingTime = 0
}

function Initialize-EmotikillerConfig {
    param([string]$ConfigPath)
    
    # Default config path
    if (-not $ConfigPath) {
        $ConfigPath = Join-Path $PSScriptRoot "policy_config.json"
    }
    
    if (-not (Test-Path $ConfigPath)) {
        Write-Warning "[EMOTIKILLER] Config file not found: $ConfigPath"
        return $false
    }
    
    try {
        $script:Config = Get-Content $ConfigPath -Raw | ConvertFrom-Json
        Write-Verbose "[EMOTIKILLER] Configuration loaded from: $ConfigPath"
        return $true
    }
    catch {
        Write-Error "[EMOTIKILLER] Failed to load configuration: $($_.Exception.Message)"
        return $false
    }
}

function Initialize-CompiledPatterns {
    if (-not $script:Config) { return }
    
    $script:CompiledPatterns = @{}
    
    # Unicode emoticon patterns
    if ($script:Config.detection_patterns.unicode_emoticons.enabled) {
        $unicodePattern = ($script:Config.detection_patterns.unicode_emoticons.ranges | ForEach-Object { "[$_]" }) -join "|"
        $script:CompiledPatterns["unicode"] = [regex]::new($unicodePattern, [System.Text.RegularExpressions.RegexOptions]::Compiled)
    }
    
    # ASCII emoticon patterns
    if ($script:Config.detection_patterns.ascii_emoticons.enabled) {
        $asciiPattern = ($script:Config.detection_patterns.ascii_emoticons.patterns) -join "|"
        $script:CompiledPatterns["ascii"] = [regex]::new($asciiPattern, [System.Text.RegularExpressions.RegexOptions]::Compiled -bor [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)
    }
    
    # Text expression patterns
    if ($script:Config.detection_patterns.text_expressions.enabled) {
        $textPattern = ($script:Config.detection_patterns.text_expressions.patterns) -join "|"
        $script:CompiledPatterns["text"] = [regex]::new($textPattern, [System.Text.RegularExpressions.RegexOptions]::Compiled -bor [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)
    }
    
    # Kaomoji patterns
    if ($script:Config.detection_patterns.kaomoji.enabled) {
        $kaomojiPattern = ($script:Config.detection_patterns.kaomoji.patterns) -join "|"
        $script:CompiledPatterns["kaomoji"] = [regex]::new($kaomojiPattern, [System.Text.RegularExpressions.RegexOptions]::Compiled)
    }
    
    Write-Verbose "[EMOTIKILLER] Compiled $($script:CompiledPatterns.Count) pattern sets"
}

function Test-ShouldScanFile {
    param([string]$FilePath)
    
    if (-not $script:Config) { return $false }
    
    # Check file extension
    $extension = [System.IO.Path]::GetExtension($FilePath).ToLower()
    if ($extension -notin $script:Config.file_filters.included_extensions) {
        return $false
    }
    
    # Check excluded paths
    foreach ($excludedPath in $script:Config.file_filters.excluded_paths) {
        if ($FilePath -like "*$excludedPath*") {
            return $false
        }
    }
    
    # Check excluded directories
    foreach ($excludedDir in $script:Config.file_filters.excluded_directories) {
        if ($FilePath -like "*$excludedDir*") {
            return $false
        }
    }
    
    # Check file size
    if (Test-Path $FilePath) {
        $fileSize = (Get-Item $FilePath).Length
        $maxSize = $script:Config.performance.max_file_size_mb * 1MB
        if ($fileSize -gt $maxSize) {
            Write-Verbose "[EMOTIKILLER] Skipping large file: $FilePath ($fileSize bytes)"
            return $false
        }
    }
    
    return $true
}

function Find-EmoticonsInContent {
    param(
        [string]$Content,
        [string]$FilePath = ""
    )
    
    if (-not $script:CompiledPatterns -or $script:CompiledPatterns.Count -eq 0) {
        return @()
    }
    
    $violations = @()
    
    foreach ($patternType in $script:CompiledPatterns.Keys) {
        $pattern = $script:CompiledPatterns[$patternType]
        $matches = $pattern.Matches($Content)
        
        foreach ($match in $matches) {
            # Get line number and context
            $beforeMatch = $Content.Substring(0, $match.Index)
            $lineNumber = ($beforeMatch -split "`n").Count
            
            # Get context lines
            $lines = $Content -split "`n"
            $contextStart = [Math]::Max(0, $lineNumber - 1 - $script:Config.reporting.context_lines)
            $contextEnd = [Math]::Min($lines.Count - 1, $lineNumber - 1 + $script:Config.reporting.context_lines)
            $context = $lines[$contextStart..$contextEnd] -join "`n"
            
            $violation = [PSCustomObject]@{
                FilePath = $FilePath
                LineNumber = $lineNumber
                PatternType = $patternType
                Match = $match.Value
                Index = $match.Index
                Length = $match.Length
                Context = if ($script:Config.reporting.include_context) { $context } else { "" }
            }
            
            $violations += $violation
        }
    }
    
    return $violations
}

function Invoke-EmoticonDetection {
    param([string]$FilePath)
    
    if (-not (Test-ShouldScanFile $FilePath)) {
        return @()
    }
    
    if (-not (Test-Path $FilePath)) {
        Write-Verbose "[EMOTIKILLER] File not found: $FilePath"
        return @()
    }
    
    try {
        # Read file content
        $content = Get-Content $FilePath -Raw -Encoding UTF8
        if (-not $content) {
            return @()
        }
        
        # Find emoticons
        $violations = Find-EmoticonsInContent -Content $content -FilePath $FilePath
        
        # Update statistics
        $script:DetectionStats.FilesScanned++
        if ($violations.Count -gt 0) {
            $script:DetectionStats.ViolationsFound++
            $script:DetectionStats.TotalEmoticons += $violations.Count
        }
        
        return $violations
    }
    catch {
        Write-Warning "[EMOTIKILLER] Error scanning file $FilePath`: $($_.Exception.Message)"
        return @()
    }
}

function Get-StagedFiles {
    try {
        $stagedFiles = git diff --cached --name-only --diff-filter=AM 2>$null
        if ($LASTEXITCODE -ne 0) {
            Write-Warning "[EMOTIKILLER] Failed to get staged files"
            return @()
        }
        
        return $stagedFiles | Where-Object { $_ -and (Test-Path $_) }
    }
    catch {
        Write-Warning "[EMOTIKILLER] Error getting staged files: $($_.Exception.Message)"
        return @()
    }
}

function Write-ViolationReport {
    param(
        [array]$Violations,
        [string]$ReportType = "commit"
    )
    
    if ($Violations.Count -eq 0) {
        Write-Host "[EMOTIKILLER] No emoticons detected - policy compliance verified" -ForegroundColor Green
        return $true
    }
    
    # Group violations by file
    $violationsByFile = $Violations | Group-Object FilePath
    
    Write-Host "[EMOTIKILLER] POLICY VIOLATION DETECTED" -ForegroundColor Red
    Write-Host "[POLICY] No emoticons allowed in AIOS codebase" -ForegroundColor Yellow
    Write-Host ""
    
    foreach ($fileGroup in $violationsByFile) {
        $filePath = $fileGroup.Name
        $fileViolations = $fileGroup.Group
        
        Write-Host "File: $filePath" -ForegroundColor Cyan
        Write-Host "Violations: $($fileViolations.Count)" -ForegroundColor Red
        
        foreach ($violation in $fileViolations | Select-Object -First 10) {
            Write-Host "  Line $($violation.LineNumber): [$($violation.PatternType)] '$($violation.Match)'" -ForegroundColor Yellow
        }
        
        if ($fileViolations.Count -gt 10) {
            Write-Host "  ... and $($fileViolations.Count - 10) more violations" -ForegroundColor Yellow
        }
        Write-Host ""
    }
    
    Write-Host "Total files with violations: $($violationsByFile.Count)" -ForegroundColor Red
    Write-Host "Total emoticons detected: $($Violations.Count)" -ForegroundColor Red
    Write-Host ""
    Write-Host "Action required: Remove all emoticons before $ReportType" -ForegroundColor Yellow
    
    # Log violations if enabled
    if ($script:Config.reporting.log_violations) {
        Write-ViolationLog -Violations $Violations -ReportType $ReportType
    }
    
    return $false
}

function Write-ViolationLog {
    param(
        [array]$Violations,
        [string]$ReportType
    )
    
    try {
        $logPath = $script:Config.reporting.log_path
        $logDir = Split-Path $logPath -Parent
        
        if (-not (Test-Path $logDir)) {
            New-Item -ItemType Directory -Path $logDir -Force | Out-Null
        }
        
        $logEntry = [ordered]@{
            timestamp = (Get-Date).ToString('o')
            type = "emotikon_violation"
            report_type = $ReportType
            violation_count = $Violations.Count
            files_affected = ($Violations | Select-Object -ExpandProperty FilePath -Unique).Count
            violations = $Violations | ForEach-Object {
                [ordered]@{
                    file = $_.FilePath
                    line = $_.LineNumber
                    pattern_type = $_.PatternType
                    match = $_.Match
                    context = $_.Context
                }
            }
            statistics = $script:DetectionStats
        }
        
        ($logEntry | ConvertTo-Json -Depth 10 -Compress) + [Environment]::NewLine | 
            Out-File $logPath -Append -Encoding UTF8
        
        Write-Verbose "[EMOTIKILLER] Violations logged to: $logPath"
    }
    catch {
        Write-Warning "[EMOTIKILLER] Failed to write violation log: $($_.Exception.Message)"
    }
}

function Invoke-AutoCleanup {
    param([array]$Violations)
    
    if (-not $AutoCleanup -or $Violations.Count -eq 0) {
        return $false
    }
    
    Write-Host "[EMOTIKILLER] Auto-cleanup option detected" -ForegroundColor Cyan
    
    if ($script:Config.enforcement_settings.auto_cleanup_prompt) {
        $response = Read-Host "Remove all detected emoticons automatically? (y/N)"
        if ($response -ne 'y' -and $response -ne 'Y') {
            Write-Host "Auto-cleanup cancelled by user" -ForegroundColor Yellow
            return $false
        }
    }
    
    $emotikillerPath = Join-Path (Split-Path $PSScriptRoot -Parent) "..\..\..\..\ai\laboratory\demos\emotikiller\python_emotikiller.py"
    
    if (-not (Test-Path $emotikillerPath)) {
        Write-Warning "[EMOTIKILLER] Python emotikiller not found: $emotikillerPath"
        return $false
    }
    
    try {
        $filesToClean = $Violations | Select-Object -ExpandProperty FilePath -Unique
        
        foreach ($file in $filesToClean) {
            Write-Host "Cleaning: $file" -ForegroundColor Yellow
            python $emotikillerPath $file
        }
        
        Write-Host "[SUCCESS] Auto-cleanup completed" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Error "[EMOTIKILLER] Auto-cleanup failed: $($_.Exception.Message)"
        return $false
    }
}

function Test-BypassCondition {
    $bypassVar = $script:Config.bypass_mechanism.env_var
    $bypassValue = [Environment]::GetEnvironmentVariable($bypassVar)
    
    if ($bypassValue) {
        Write-Host "[EMOTIKILLER] Bypass detected: $bypassVar=$bypassValue" -ForegroundColor Yellow
        
        if ($script:Config.bypass_mechanism.log_bypasses) {
            $logEntry = [ordered]@{
                timestamp = (Get-Date).ToString('o')
                type = "emotikiller_bypass"
                reason = $bypassValue
                user = $env:USERNAME
            }
            
            try {
                $logPath = $script:Config.reporting.log_path
                $logDir = Split-Path $logPath -Parent
                if (-not (Test-Path $logDir)) {
                    New-Item -ItemType Directory -Path $logDir -Force | Out-Null
                }
                
                ($logEntry | ConvertTo-Json -Compress) + [Environment]::NewLine | 
                    Out-File $logPath -Append -Encoding UTF8
            }
            catch {
                Write-Warning "[EMOTIKILLER] Failed to log bypass"
            }
        }
        
        return $true
    }
    
    return $false
}

# Main execution function
function Invoke-EmotikillerScan {
    param(
        [string[]]$TargetFiles = @(),
        [switch]$UseStaged = $false
    )
    
    $startTime = Get-Date
    
    # Initialize configuration
    if (-not (Initialize-EmotikillerConfig -ConfigPath $ConfigPath)) {
        Write-Error "[EMOTIKILLER] Failed to initialize configuration"
        return $false
    }
    
    # Check if emotikiller is enabled
    if (-not $script:Config.emotikiller_policy.enabled) {
        Write-Verbose "[EMOTIKILLER] Emotikiller is disabled"
        return $true
    }
    
    # Check bypass condition
    if (Test-BypassCondition) {
        Write-Host "[EMOTIKILLER] Policy check bypassed" -ForegroundColor Yellow
        return $true
    }
    
    # Initialize compiled patterns
    Initialize-CompiledPatterns
    
    # Determine files to scan
    $filesToScan = @()
    if ($UseStaged) {
        $filesToScan = Get-StagedFiles
    } elseif ($TargetFiles.Count -gt 0) {
        $filesToScan = $TargetFiles
    } else {
        Write-Warning "[EMOTIKILLER] No files specified for scanning"
        return $true
    }
    
    if ($filesToScan.Count -eq 0) {
        Write-Host "[EMOTIKILLER] No files to scan" -ForegroundColor Green
        return $true
    }
    
    Write-Verbose "[EMOTIKILLER] Scanning $($filesToScan.Count) files for emoticons"
    
    # Scan files for violations
    $allViolations = @()
    foreach ($file in $filesToScan) {
        $violations = Invoke-EmoticonDetection -FilePath $file
        $allViolations += $violations
    }
    
    # Update timing statistics
    $script:DetectionStats.ProcessingTime = (Get-Date) - $startTime
    
    # Handle violations
    if ($allViolations.Count -gt 0) {
        $reportType = if ($UseStaged) { "commit" } else { "scan" }
        $policyCompliant = Write-ViolationReport -Violations $allViolations -ReportType $reportType
        
        # Attempt auto-cleanup if requested
        if (-not $policyCompliant -and $AutoCleanup) {
            if (Invoke-AutoCleanup -Violations $allViolations) {
                Write-Host "[EMOTIKILLER] Re-scanning after cleanup..." -ForegroundColor Cyan
                return Invoke-EmotikillerScan -TargetFiles $TargetFiles -UseStaged:$UseStaged
            }
        }
        
        return $policyCompliant
    } else {
        Write-Host "[EMOTIKILLER] Policy compliance verified - no emoticons detected" -ForegroundColor Green
        return $true
    }
}

# Export functions for GitHook integration
function Test-EmoticonCompliance {
    param(
        [string[]]$FilePaths = @(),
        [switch]$ScanStaged = $false
    )
    
    return Invoke-EmotikillerScan -TargetFiles $FilePaths -UseStaged:$ScanStaged
}

# Main execution when called directly
if ($MyInvocation.InvocationName -eq $MyInvocation.MyCommand.Name) {
    $success = $false
    
    if ($ScanStaged) {
        $success = Invoke-EmotikillerScan -UseStaged
    } elseif ($FilePaths.Count -gt 0) {
        $success = Invoke-EmotikillerScan -TargetFiles $FilePaths
    } else {
        Write-Host "AIOS GitHook Emotikiller - Core Detection Module"
        Write-Host "Usage: .\emoticon_detector.ps1 [-ScanStaged] [-FilePaths @('file1', 'file2')] [-AutoCleanup]"
        $success = $true
    }
    
    if ($ReturnResults) {
        return $success
    } else {
        exit ([int](-not $success))
    }
}