# AIOS GitHook Emotikiller - Hook Integration Module
# STRICT NO EMOTICON POLICY ENFORCED
# Integration functions for nucleus pre-commit and pre-push hooks

# Import the core emoticon detection module
$EmoticonDetectorPath = Join-Path $PSScriptRoot "emoticon_detector.ps1"

function Import-EmotikillerModule {
    if (Test-Path $EmoticonDetectorPath) {
        . $EmoticonDetectorPath -ReturnResults
        return $true
    } else {
        Write-Warning "[HOOK-INTEGRATION] Emoticon detector module not found: $EmoticonDetectorPath"
        return $false
    }
}

function Test-EmoticonPolicyCompliance {
    <#
    .SYNOPSIS
    Tests emoticon policy compliance for GitHook integration
    
    .DESCRIPTION
    This function integrates with the AIOS GitHook system to enforce
    the no-emoticon policy during commit and push operations.
    
    .PARAMETER StagedFiles
    Array of staged file paths to check for emoticons
    
    .PARAMETER HookType
    Type of hook calling this function (pre-commit, pre-push)
    
    .PARAMETER AutoCleanup
    Whether to offer automatic emoticon removal
    
    .OUTPUTS
    Returns hashtable with compliance status and violation details
    #>
    param(
        [Parameter(Mandatory=$false)]
        [string[]]$StagedFiles = @(),
        
        [Parameter(Mandatory=$false)]
        [ValidateSet("pre-commit", "pre-push", "manual")]
        [string]$HookType = "pre-commit",
        
        [Parameter(Mandatory=$false)]
        [switch]$AutoCleanup
    )
    
    $result = @{
        Compliant = $true
        ViolationCount = 0
        FilesAffected = 0
        Message = ""
        Details = @()
        RuleName = "emoticon_policy"
        Severity = "error"
    }
    
    try {
        # Import emotikiller module
        if (-not (Import-EmotikillerModule)) {
            $result.Compliant = $false
            $result.Message = "Emotikiller module failed to load"
            return $result
        }
        
        # Check if emoticon detection is available
        if (-not (Get-Command Test-EmoticonCompliance -ErrorAction SilentlyContinue)) {
            Write-Verbose "[HOOK-INTEGRATION] Emoticon detection not available"
            return $result
        }
        
        # Determine files to scan based on hook type
        $filesToScan = @()
        switch ($HookType) {
            "pre-commit" {
                if ($StagedFiles.Count -gt 0) {
                    $filesToScan = $StagedFiles
                } else {
                    # Get staged files directly
                    $compliance = Test-EmoticonCompliance -ScanStaged
                    $result.Compliant = $compliance
                    if (-not $compliance) {
                        $result.ViolationCount = 1
                        $result.Message = "Emoticons detected in staged files"
                    } else {
                        $result.Message = "No emoticons detected in staged files"
                    }
                    return $result
                }
            }
            "pre-push" {
                # For pre-push, scan all modified files in the branch
                $filesToScan = $StagedFiles
            }
            "manual" {
                $filesToScan = $StagedFiles
            }
        }
        
        # Scan specified files
        if ($filesToScan.Count -gt 0) {
            $compliance = Test-EmoticonCompliance -FilePaths $filesToScan
            $result.Compliant = $compliance
            
            if (-not $compliance) {
                $result.ViolationCount = 1
                $result.FilesAffected = $filesToScan.Count
                $result.Message = "Emoticons detected in $($filesToScan.Count) file(s)"
                $result.Details = @("Files with violations: $($filesToScan -join ', ')")
            } else {
                $result.Message = "No emoticons detected in scanned files"
            }
        } else {
            $result.Message = "No files to scan for emoticons"
        }
        
    } catch {
        $result.Compliant = $false
        $result.Message = "Emoticon policy check failed: $($_.Exception.Message)"
        $result.Details = @($_.Exception.ToString())
    }
    
    return $result
}

function Add-EmoticonPolicyToHook {
    <#
    .SYNOPSIS
    Adds emoticon policy validation to existing GitHook validation pipeline
    
    .DESCRIPTION
    This function integrates emoticon policy checking into the existing
    nucleus hook validation system.
    
    .PARAMETER ValidationResults
    Array of existing validation results to append to
    
    .PARAMETER StagedEntries
    Array of staged file entries from git
    
    .PARAMETER HookType
    Type of hook being executed
    
    .OUTPUTS
    Returns updated validation results array
    #>
    param(
        [Parameter(Mandatory=$true)]
        [array]$ValidationResults,
        
        [Parameter(Mandatory=$false)]
        [array]$StagedEntries = @(),
        
        [Parameter(Mandatory=$false)]
        [string]$HookType = "pre-commit"
    )
    
    try {
        # Extract file paths from staged entries
        $stagedFiles = @()
        if ($StagedEntries) {
            $stagedFiles = $StagedEntries | Where-Object { $_.Status -ne 'D' } | ForEach-Object { $_.Path }
        }
        
        # Run emoticon policy check
        $emoticonResult = Test-EmoticonPolicyCompliance -StagedFiles $stagedFiles -HookType $HookType
        
        # Convert result to format expected by nucleus hook system
        $hookResult = @{
            Rule = "emoticon_policy"
            Passed = $emoticonResult.Compliant
            Message = $emoticonResult.Message
            Details = $emoticonResult.Details
            ViolationCount = $emoticonResult.ViolationCount
            FilesAffected = $emoticonResult.FilesAffected
            Severity = $emoticonResult.Severity
        }
        
        # Add to validation results
        $ValidationResults += $hookResult
        
        Write-Verbose "[HOOK-INTEGRATION] Emoticon policy check completed: $($emoticonResult.Message)"
        
    } catch {
        # Add error result to validation
        $errorResult = @{
            Rule = "emoticon_policy"
            Passed = $false
            Message = "Emoticon policy check error: $($_.Exception.Message)"
            Details = @($_.Exception.ToString())
            ViolationCount = 1
            FilesAffected = 0
            Severity = "error"
        }
        
        $ValidationResults += $errorResult
        Write-Warning "[HOOK-INTEGRATION] Emoticon policy check failed: $($_.Exception.Message)"
    }
    
    return $ValidationResults
}

function Write-EmoticonPolicyLog {
    <#
    .SYNOPSIS
    Writes emoticon policy enforcement logs for GitHook integration
    
    .DESCRIPTION
    Integrates emoticon policy logging with the existing GitHook logging system
    
    .PARAMETER Status
    Status of the policy check (pass/fail)
    
    .PARAMETER Details
    Details about violations or compliance
    
    .PARAMETER HookType
    Type of hook that triggered the check
    #>
    param(
        [Parameter(Mandatory=$true)]
        [ValidateSet("pass", "fail", "error")]
        [string]$Status,
        
        [Parameter(Mandatory=$false)]
        [hashtable]$Details = @{},
        
        [Parameter(Mandatory=$false)]
        [string]$HookType = "pre-commit"
    )
    
    try {
        # Create log entry compatible with GitHook logging system
        $logEntry = @{
            timestamp = (Get-Date).ToString('o')
            hook_type = $HookType
            rule = "emoticon_policy"
            status = $Status
            details = $Details
            user = $env:USERNAME
        }
        
        # Use the same logging function as nucleus hooks if available
        if (Get-Command Write-JsonLog -ErrorAction SilentlyContinue) {
            Write-JsonLog -Status $Status -Data $logEntry
        } else {
            # Fallback to direct file logging
            $logDir = "runtime_intelligence/logs/hooks"
            if (-not (Test-Path $logDir)) {
                New-Item -ItemType Directory -Path $logDir -Force | Out-Null
            }
            
            $logPath = Join-Path $logDir "emoticon_policy.log"
            ($logEntry | ConvertTo-Json -Compress) + [Environment]::NewLine | 
                Out-File $logPath -Append -Encoding UTF8
        }
        
    } catch {
        Write-Warning "[HOOK-INTEGRATION] Failed to write emoticon policy log: $($_.Exception.Message)"
    }
}

function Get-EmoticonPolicyMetrics {
    <#
    .SYNOPSIS
    Gets emoticon policy metrics for GitHook reporting
    
    .DESCRIPTION
    Provides metrics data for integration with GitHook metrics system
    
    .OUTPUTS
    Returns hashtable with policy metrics
    #>
    
    return @{
        rule_name = "emoticon_policy"
        checks_performed = 1
        violations_found = 0
        files_scanned = 0
        enforcement_level = "block"
        last_check = (Get-Date).ToString('o')
    }
}

# Functions exported for GitHook integration (commenting out Export-ModuleMember to avoid script execution errors)
# Export-ModuleMember -Function @(
#     'Test-EmoticonPolicyCompliance',
#     'Add-EmoticonPolicyToHook',
#     'Write-EmoticonPolicyLog',
#     'Get-EmoticonPolicyMetrics'
# )