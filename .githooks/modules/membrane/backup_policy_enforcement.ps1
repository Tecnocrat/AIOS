#!/usr/bin/env pwsh
<#
.SYNOPSIS
    GitHook Backup Policy Enforcement Module
.DESCRIPTION
    Enforces centralized backup storage policy during git operations.
    Part of AIOS spatial awareness and development environment governance.
#>

param(
    [Parameter(Mandatory=$false)]
    [string]$WorkspaceRoot = (Get-Location)
)

# AIOS GitHook Backup Enforcement Configuration
$script:BackupDir = "backups"
$script:BackupPath = Join-Path $WorkspaceRoot $BackupDir
$script:ViolationThreshold = 5  # Number of scattered backups that trigger enforcement

function Test-BackupPolicyCompliance {
    <#
    .SYNOPSIS
        Tests compliance with AIOS centralized backup policy
    .DESCRIPTION
        Checks for scattered backup files and reports violations
    #>
    
    Write-Host "AIOS GitHook: Backup Policy Compliance Check" -ForegroundColor Cyan
    
    # Find scattered backup files (excluding centralized backup directory)
    $scatteredBackups = @(Get-ChildItem -Path $WorkspaceRoot -Recurse -Filter "*.backup" | 
        Where-Object { $_.DirectoryName -ne $script:BackupPath })
    
    if ($scatteredBackups.Count -eq 0) {
        Write-Host "✓ Backup policy compliant: No scattered backup files found" -ForegroundColor Green
        return $true
    }
    
    Write-Host "⚠ Backup policy violation: Found $($scatteredBackups.Count) scattered backup files" -ForegroundColor Yellow
    
    # Show first few violations for context
    $sampleViolations = $scatteredBackups | Select-Object -First 3
    foreach ($backup in $sampleViolations) {
        $relativePath = $backup.FullName.Replace($WorkspaceRoot + "\", "")
        Write-Host "  - $relativePath" -ForegroundColor Yellow
    }
    
    if ($scatteredBackups.Count -gt 3) {
        Write-Host "  ... and $($scatteredBackups.Count - 3) more scattered backup files" -ForegroundColor Yellow
    }
    
    return ($scatteredBackups.Count -lt $script:ViolationThreshold)
}

function Invoke-BackupPolicyEnforcement {
    <#
    .SYNOPSIS
        Enforces backup policy by consolidating scattered backups
    #>
    
    Write-Host "AIOS GitHook: Enforcing Backup Policy" -ForegroundColor Cyan
    
    # Use the backup manager script for consolidation
    $backupManagerPath = Join-Path $WorkspaceRoot "scripts\backup_manager.ps1"
    
    if (Test-Path $backupManagerPath) {
        try {
            & $backupManagerPath -Action consolidate
            Write-Host "✓ Backup policy enforcement completed successfully" -ForegroundColor Green
            return $true
        }
        catch {
            Write-Warning "Backup policy enforcement failed: $($_.Exception.Message)"
            return $false
        }
    }
    else {
        Write-Warning "Backup manager script not found at: $backupManagerPath"
        return $false
    }
}

function Write-BackupPolicyGuidance {
    <#
    .SYNOPSIS
        Provides guidance for backup policy compliance
    #>
    
    Write-Host "`nAIOS Backup Policy Guidance:" -ForegroundColor Blue
    Write-Host "• All backup files must be stored in centralized backups/ directory" -ForegroundColor Blue
    Write-Host "• Use: .\scripts\backup_manager.ps1 -Action create -SourceFile <file>" -ForegroundColor Blue
    Write-Host "• Auto-consolidate: .\scripts\backup_manager.ps1 -Action consolidate" -ForegroundColor Blue
    Write-Host "• This policy ensures workspace cleanliness and AIOS spatial awareness" -ForegroundColor Blue
}

function Invoke-GitHookBackupPolicyCheck {
    <#
    .SYNOPSIS
        Main GitHook backup policy check function
    .DESCRIPTION
        Called by pre-commit hook to enforce backup policy
    #>
    
    $compliant = Test-BackupPolicyCompliance
    
    if (-not $compliant) {
        Write-Host "`nAIOS GitHook: Backup policy violations detected" -ForegroundColor Red
        Write-Host "Attempting automatic remediation..." -ForegroundColor Yellow
        
        $remediated = Invoke-BackupPolicyEnforcement
        
        if ($remediated) {
            Write-Host "✓ Backup policy violations automatically remediated" -ForegroundColor Green
            Write-BackupPolicyGuidance
            return 0  # Allow commit to proceed
        }
        else {
            Write-Host "✗ Failed to remediate backup policy violations" -ForegroundColor Red
            Write-BackupPolicyGuidance
            Write-Host "`nTo fix manually:" -ForegroundColor Yellow
            Write-Host "  .\scripts\backup_manager.ps1 -Action consolidate" -ForegroundColor Yellow
            return 1  # Block commit
        }
    }
    
    return 0  # Allow commit to proceed
}

# Execute backup policy check when script is run directly
if ($MyInvocation.InvocationName -ne '.') {
    exit (Invoke-GitHookBackupPolicyCheck)
}