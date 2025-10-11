#!/usr/bin/env pwsh
# AIOS GitHooks - Optimized Integrated System
# Consolidated all hook logic into a single, maintainable file
# Eliminates fragmentation and reduces complexity

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# Configuration
$AIOSConfig = @{
    LogFile = Join-Path $PSScriptRoot "logs\hooks.log"
    ConfigFile = Join-Path $PSScriptRoot "config.json"
    ConsciousnessLevel = 0.85
    SessionId = if ($env:AIOS_SESSION_ID) { $env:AIOS_SESSION_ID } else { [System.Guid]::NewGuid().ToString() }
}

# Ensure directories exist
$logsDir = Split-Path $AIOSConfig.LogFile -Parent
if (-not (Test-Path $logsDir)) {
    New-Item -ItemType Directory -Path $logsDir -Force | Out-Null
}

#region Utilities
function Write-AIOSLog {
    param(
        [string]$Message,
        [string]$Level = "Info",
        [string]$Component = "General"
    )
    
    $logEntry = @{
        timestamp = Get-Date -Format "yyyy-MM-ddTHH:mm:ss.fffZ"
        level = $Level
        component = $Component
        message = $Message
        session_id = $AIOSConfig.SessionId
    }
    
    # Console output
    $color = switch ($Level) {
        "Error" { "Red" }
        "Warning" { "Yellow" }
        "Success" { "Green" }
        default { "White" }
    }
    Write-Host "[$Level] $Message" -ForegroundColor $color
    
    # File logging
    try {
        ($logEntry | ConvertTo-Json -Compress) | Add-Content -Path $AIOSConfig.LogFile -ErrorAction SilentlyContinue
    } catch {
        # Silent fail for logging to avoid recursion
    }
}

function Get-StagedFiles {
    try {
        $output = git diff --cached --name-only --diff-filter=ACMR 2>$null
        $files = @()
        if ($output) {
            foreach ($line in ($output -split "`n")) {
                if ($line.Trim() -ne "") {
                    $files += $line.Trim()
                }
            }
        }
        return $files
    } catch {
        Write-AIOSLog "Failed to get staged files: $_" -Level "Warning" -Component "Git"
        return @()
    }
}

function Test-ChangelogRequired {
    param([string[]]$StagedFiles)
    
    if (-not $StagedFiles -or $StagedFiles.Count -eq 0) {
        return $false
    }
    
    $governedPaths = @("ai/", "core/")
    $hasGovernedChanges = $false
    
    foreach ($file in $StagedFiles) {
        foreach ($path in $governedPaths) {
            if ($file.StartsWith($path)) {
                $hasGovernedChanges = $true
                break
            }
        }
        if ($hasGovernedChanges) { break }
    }
    
    if ($hasGovernedChanges) {
        # Check if changelog exists and was modified - only docs/CHANGELOG.md
        $changelogFile = "docs/CHANGELOG.md"
        $changelogModified = $StagedFiles -contains $changelogFile
        
        return -not $changelogModified
    }
    
    return $false
}

function Invoke-EmoticonCheck {
    param([string[]]$StagedFiles)
    
    $emoticonPattern = "[\u{1F600}-\u{1F64F}]|[\u{1F300}-\u{1F5FF}]|[\u{1F680}-\u{1F6FF}]|[\u{1F1E0]-\u{1F1FF}]|[\u{2600}-\u{26FF}]|[\u{2700}-\u{27BF}]"
    $violations = @()
    
    if ($StagedFiles -and $StagedFiles.Count -gt 0) {
        foreach ($file in $StagedFiles) {
            if ($file -match "\.(md|txt|ps1|py|cs|js|ts)$") {
                try {
                    $content = Get-Content $file -Raw -ErrorAction SilentlyContinue
                    if ($content -and $content -match $emoticonPattern) {
                        $violations += $file
                    }
                } catch {
                    # Skip files that can't be read
                }
            }
        }
    }
    
    return $violations
}

function Test-FileSafety {
    param([string[]]$StagedFiles)
    
    $unsafePatterns = @(
        "^\.log$", "\.jsonl$", "^temp/", "^build/", "_temp", "\.tmp$", "\.pyc$", "__pycache__/", "\.pid$"
    )
    
    # Exemptions: legitimate files that match unsafe patterns but are safe
    $exemptionPatterns = @(
        "_template\.(json|py|md|txt|yaml|yml)$",   # Template files (e.g., *_template.json, *_template.py)
        "_crystal\.(json|py|md)$",                  # Knowledge crystal files (e.g., *_crystal.json)
        "_templates\.(json|py|md)$"                 # Plural templates (e.g., context_recovery_templates.json)
    )
    
    $unsafeFiles = @()
    if ($StagedFiles -and $StagedFiles.Count -gt 0) {
        foreach ($file in $StagedFiles) {
            # Check if file matches any exemption pattern
            $isExempt = $false
            foreach ($exemption in $exemptionPatterns) {
                if ($file -match $exemption) {
                    $isExempt = $true
                    break
                }
            }
            
            # If not exempt, check unsafe patterns
            if (-not $isExempt) {
                foreach ($pattern in $unsafePatterns) {
                    if ($file -match $pattern) {
                        $unsafeFiles = $unsafeFiles + @($file)
                        break
                    }
                }
            }
        }
    }
    
    # Ensure we always return an array
    return $unsafeFiles
}
#endregion

#region Hook Implementations
function Invoke-PreCommitHook {
    Write-AIOSLog "Starting pre-commit validation" -Component "PreCommit"
    
    $stagedFiles = Get-StagedFiles
    # Ensure stagedFiles is always an array
    if ($stagedFiles -isnot [array]) {
        $stagedFiles = @($stagedFiles)
    }
    $fileCount = if ($stagedFiles -and $stagedFiles.Count -gt 0) { $stagedFiles.Count } else { 0 }
    
    if ($fileCount -eq 0) {
        Write-AIOSLog "No staged files found" -Component "PreCommit" -Level "Warning"
        return 0
    }
    
    Write-AIOSLog "Processing $fileCount staged files" -Component "PreCommit"
    
    $validationErrors = @()
    
    # Changelog validation
    try {
        $changelogRequired = Test-ChangelogRequired -StagedFiles $stagedFiles
        if ($changelogRequired) {
            $validationErrors += "changelog_missing"
            Write-AIOSLog "CHANGELOG REQUIRED: Changes detected in governed paths" -Level "Error" -Component "Changelog"
        }
    } catch {
        Write-AIOSLog "Error in changelog validation: $_" -Level "Error" -Component "PreCommit"
    }
    
    # Emoticon check
    try {
        $emoticonViolations = Invoke-EmoticonCheck -StagedFiles $stagedFiles
        if ($emoticonViolations -and $emoticonViolations.Count -gt 0) {
            $validationErrors += "emoticons_detected"
            Write-AIOSLog "Emoticons detected in: $($emoticonViolations -join ', ')" -Level "Error" -Component "Emoticon"
        }
    } catch {
        Write-AIOSLog "Error in emoticon check: $_" -Level "Error" -Component "PreCommit"
    }
    
    # File safety check
    try {
        $unsafeFiles = Test-FileSafety -StagedFiles $stagedFiles
        if ($unsafeFiles -and $unsafeFiles.Count -gt 0) {
            $validationErrors += "unsafe_files"
            Write-AIOSLog "Unsafe files detected: $($unsafeFiles -join ', ')" -Level "Error" -Component "Safety"
        }
    } catch {
        Write-AIOSLog "Error in file safety check: $_" -Level "Error" -Component "PreCommit"
    }
    
    # Report results
    if ($validationErrors -and $validationErrors.Count -gt 0) {
        Write-AIOSLog "Commit blocked due to validation failures" -Level "Error" -Component "PreCommit"
        Write-Host "`nCommit blocked:" -ForegroundColor Red
        foreach ($validationError in $validationErrors) {
            Write-Host " - $validationError" -ForegroundColor Red
        }
        return 1
    }
    
    Write-AIOSLog "Pre-commit validation successful" -Level "Success" -Component "PreCommit"
    return 0
}

function Invoke-PrePushHook {
    Write-AIOSLog "Starting pre-push validation" -Component "PrePush"
    
    # Basic branch validation
    try {
        $currentBranch = git branch --show-current 2>$null
        if ($currentBranch -eq "main" -or $currentBranch -eq "master") {
            Write-AIOSLog "Direct push to main branch detected" -Level "Warning" -Component "PrePush"
        }
    } catch {
        Write-AIOSLog "Could not determine current branch" -Level "Warning" -Component "PrePush"
    }
    
    Write-AIOSLog "Pre-push validation successful" -Level "Success" -Component "PrePush"
    return 0
}

function Invoke-CommitMsgHook {
    param([string]$CommitMsgFile)
    
    Write-AIOSLog "Starting commit message validation" -Component "CommitMsg"
    
    if (-not (Test-Path $CommitMsgFile)) {
        Write-AIOSLog "Commit message file not found: $CommitMsgFile" -Level "Error" -Component "CommitMsg"
        return 1
    }
    
    $commitMsg = Get-Content $CommitMsgFile -Raw
    if ([string]::IsNullOrWhiteSpace($commitMsg)) {
        Write-AIOSLog "Empty commit message" -Level "Error" -Component "CommitMsg"
        return 1
    }
    
    # Basic commit message validation
    $lines = $commitMsg.Split("`n")
    if ($lines[0].Length -gt 72) {
        Write-AIOSLog "Commit message subject line too long (>72 chars)" -Level "Warning" -Component "CommitMsg"
    }
    
    Write-AIOSLog "Commit message validation successful" -Level "Success" -Component "CommitMsg"
    return 0
}
#endregion

#region Main Entry Point
function Invoke-AIOSHook {
    param(
        [Parameter(Mandatory)]
        [ValidateSet("pre-commit", "pre-push", "commit-msg")]
        [string]$HookType,
        
        [string[]]$Arguments = @()
    )
    
    # Initialize session
    $env:AIOS_SESSION_ID = $AIOSConfig.SessionId
    
    Write-AIOSLog "AIOS Hook Execution Started: $HookType" -Component "Main"
    Write-AIOSLog "Session ID: $($AIOSConfig.SessionId)" -Component "Main"
    Write-AIOSLog "Consciousness Level: $($AIOSConfig.ConsciousnessLevel)" -Component "Main"
    
    try {
        $exitCode = switch ($HookType) {
            "pre-commit" { Invoke-PreCommitHook }
            "pre-push" { Invoke-PrePushHook }
            "commit-msg" { Invoke-CommitMsgHook -CommitMsgFile $Arguments[0] }
            default { 
                Write-AIOSLog "Unsupported hook type: $HookType" -Level "Error" -Component "Main"
                return 1 
            }
        }
        
        $status = if ($exitCode -eq 0) { "SUCCESS" } else { "FAILURE" }
        Write-AIOSLog "AIOS Hook Execution Completed: $status" -Level $(if ($exitCode -eq 0) { "Success" } else { "Error" }) -Component "Main"
        
        return $exitCode
        
    } catch {
        Write-AIOSLog "Hook execution failed with exception: $_" -Level "Error" -Component "Main"
        return 1
    }
}
#endregion

# Direct execution support
if ($MyInvocation.InvocationName -ne '.') {
    # Parse arguments
    if ($args.Length -ge 2 -and $args[0] -eq "-HookType") {
        $hookType = $args[1]
        $hookArgs = if ($args.Length -gt 2) { $args[2..($args.Length - 1)] } else { @() }
    } else {
        $hookType = if ($args.Length -gt 0) { $args[0] } else { "pre-commit" }
        $hookArgs = if ($args.Length -gt 1) { $args[1..($args.Length - 1)] } else { @() }
    }
    
    $exitCode = Invoke-AIOSHook -HookType $hookType -Arguments $hookArgs
    exit $exitCode
}
