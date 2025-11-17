#!/usr/bin/env pwsh
<#
.SYNOPSIS
    AIOS Backup Management System - Enforces centralized backup storage policy

.DESCRIPTION
    This script enforces the AIOS backup policy by:
    1. Moving any scattered backup files to the centralized tachyonic/archive/backups/ folder
    2. Providing functions to create properly named backups
    3. Cleaning up old backup files based on retention policies
    4. Ensuring compliance with AIOS spatial awareness guidelines

.PARAMETER Action
    Action to perform: 'consolidate', 'cleanup', 'create', 'status'

.PARAMETER SourceFile
    Source file to backup (when Action is 'create')

.PARAMETER DaysToKeep
    Number of days to keep backups (default: 30)

.EXAMPLE
    .\backup_manager.ps1 -Action consolidate
    .\backup_manager.ps1 -Action create -SourceFile "README.md"
    .\backup_manager.ps1 -Action cleanup -DaysToKeep 14
#>

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("consolidate", "cleanup", "create", "status")]
    [string]$Action,
    
    [Parameter(Mandatory=$false)]
    [string]$SourceFile = "",
    
    [Parameter(Mandatory=$false)]
    [int]$DaysToKeep = 30
)

# AIOS Backup Management Configuration
$script:BackupDir = "tachyonic\archive\backups"
$script:WorkspaceRoot = Get-Location
$script:BackupPath = Join-Path $WorkspaceRoot $BackupDir

# Ensure backup directory exists with proper spatial metadata
function Initialize-BackupDirectory {
    if (-not (Test-Path $script:BackupPath)) {
        New-Item -ItemType Directory -Path $script:BackupPath -Force | Out-Null
        Write-Host "Created centralized backup directory: $script:BackupPath" -ForegroundColor Green
    }
    
    # Ensure spatial metadata exists
    $metadataPath = Join-Path $script:BackupPath ".aios_spatial_metadata.json"
    if (-not (Test-Path $metadataPath)) {
        Write-Warning "Spatial metadata missing in backup directory. Please ensure .aios_spatial_metadata.json exists."
    }
}

# Consolidate scattered backup files to centralized location
function Invoke-BackupConsolidation {
    Write-Host "AIOS Backup Consolidation - Enforcing Centralized Backup Policy" -ForegroundColor Cyan
    Write-Host "=" * 60 -ForegroundColor Cyan
    
    Initialize-BackupDirectory
    
    # Find all backup files in workspace (excluding already consolidated ones)
    $scatteredBackups = Get-ChildItem -Path $script:WorkspaceRoot -Recurse -Filter "*.backup" | 
        Where-Object { $_.DirectoryName -ne $script:BackupPath }
    
    if ($scatteredBackups.Count -eq 0) {
        Write-Host "✓ No scattered backup files found. Backup policy is enforced." -ForegroundColor Green
        return
    }
    
    Write-Host "Found $($scatteredBackups.Count) scattered backup files:" -ForegroundColor Yellow
    foreach ($backup in $scatteredBackups) {
        $relativePath = $backup.FullName.Replace($script:WorkspaceRoot + "\", "")
        Write-Host "  - $relativePath" -ForegroundColor Yellow
    }
    
    Write-Host "`nConsolidating to centralized backup directory..." -ForegroundColor White
    
    $moved = 0
    foreach ($backup in $scatteredBackups) {
        try {
            # Create timestamp-based name to avoid conflicts
            $timestamp = Get-Date -Format "yyyy-MM-dd-HHmmss"
            $originalName = $backup.Name
            $newName = "$originalName.$timestamp"
            $destinationPath = Join-Path $script:BackupPath $newName
            
            Move-Item -Path $backup.FullName -Destination $destinationPath -Force
            Write-Host "  ✓ Moved: $originalName -> $newName" -ForegroundColor Green
            $moved++
        }
        catch {
            Write-Error "Failed to move $($backup.FullName): $($_.Exception.Message)"
        }
    }
    
    Write-Host "`n✓ Consolidation complete: $moved files moved to centralized backup directory" -ForegroundColor Green
    Write-Host "  Location: $script:BackupPath" -ForegroundColor Gray
}

# Create a properly named backup
function New-AIOSBackup {
    param([string]$FilePath)
    
    if (-not $FilePath) {
        Write-Error "SourceFile parameter is required for 'create' action"
        return
    }
    
    if (-not (Test-Path $FilePath)) {
        Write-Error "Source file not found: $FilePath"
        return
    }
    
    Initialize-BackupDirectory
    
    $sourceFile = Get-Item $FilePath
    $timestamp = Get-Date -Format "yyyy-MM-dd-HHmmss"
    $backupName = "$($sourceFile.Name).backup.$timestamp"
    $backupPath = Join-Path $script:BackupPath $backupName
    
    try {
        Copy-Item -Path $FilePath -Destination $backupPath -Force
        Write-Host "✓ Backup created: $backupName" -ForegroundColor Green
        Write-Host "  Source: $FilePath" -ForegroundColor Gray
        Write-Host "  Backup: $backupPath" -ForegroundColor Gray
    }
    catch {
        Write-Error "Failed to create backup: $($_.Exception.Message)"
    }
}

# Clean up old backup files
function Invoke-BackupCleanup {
    Write-Host "AIOS Backup Cleanup - Removing backups older than $DaysToKeep days" -ForegroundColor Cyan
    
    if (-not (Test-Path $script:BackupPath)) {
        Write-Host "No backup directory found. Nothing to clean up." -ForegroundColor Yellow
        return
    }
    
    $cutoffDate = (Get-Date).AddDays(-$DaysToKeep)
    $oldBackups = Get-ChildItem -Path $script:BackupPath -Filter "*.backup*" | 
        Where-Object { $_.LastWriteTime -lt $cutoffDate }
    
    if ($oldBackups.Count -eq 0) {
        Write-Host "✓ No old backup files found (older than $DaysToKeep days)" -ForegroundColor Green
        return
    }
    
    Write-Host "Found $($oldBackups.Count) old backup files:" -ForegroundColor Yellow
    foreach ($backup in $oldBackups) {
        $age = [math]::Round(((Get-Date) - $backup.LastWriteTime).TotalDays, 1)
        Write-Host "  - $($backup.Name) (${age} days old)" -ForegroundColor Yellow
    }
    
    $confirm = Read-Host "`nRemove these files? [y/N]"
    if ($confirm -eq 'y' -or $confirm -eq 'Y') {
        $removed = 0
        foreach ($backup in $oldBackups) {
            try {
                Remove-Item -Path $backup.FullName -Force
                Write-Host "  ✓ Removed: $($backup.Name)" -ForegroundColor Green
                $removed++
            }
            catch {
                Write-Error "Failed to remove $($backup.Name): $($_.Exception.Message)"
            }
        }
        Write-Host "`n✓ Cleanup complete: $removed files removed" -ForegroundColor Green
    }
    else {
        Write-Host "Cleanup cancelled by user" -ForegroundColor Yellow
    }
}

# Show backup status and statistics
function Show-BackupStatus {
    Write-Host "AIOS Backup Management Status" -ForegroundColor Cyan
    Write-Host "=" * 40 -ForegroundColor Cyan
    
    # Check if backup directory exists
    if (Test-Path $script:BackupPath) {
        Write-Host "✓ Centralized backup directory exists: $script:BackupPath" -ForegroundColor Green
        
        # Count backup files
        $backupFiles = Get-ChildItem -Path $script:BackupPath -Filter "*.backup*"
        Write-Host "  Total backup files: $($backupFiles.Count)" -ForegroundColor Gray
        
        if ($backupFiles.Count -gt 0) {
            $totalSize = ($backupFiles | Measure-Object Length -Sum).Sum
            $sizeGB = [math]::Round($totalSize / 1GB, 2)
            Write-Host "  Total size: $sizeGB GB" -ForegroundColor Gray
            
            $oldestBackup = ($backupFiles | Sort-Object LastWriteTime)[0]
            $newestBackup = ($backupFiles | Sort-Object LastWriteTime -Descending)[0]
            Write-Host "  Oldest backup: $($oldestBackup.LastWriteTime.ToString('yyyy-MM-dd HH:mm'))" -ForegroundColor Gray
            Write-Host "  Newest backup: $($newestBackup.LastWriteTime.ToString('yyyy-MM-dd HH:mm'))" -ForegroundColor Gray
        }
    }
    else {
        Write-Host "⚠ Centralized backup directory does not exist" -ForegroundColor Yellow
    }
    
    # Check for scattered backups
    $scatteredBackups = Get-ChildItem -Path $script:WorkspaceRoot -Recurse -Filter "*.backup" | 
        Where-Object { $_.DirectoryName -ne $script:BackupPath }
    
    if ($scatteredBackups.Count -eq 0) {
        Write-Host "✓ No scattered backup files found" -ForegroundColor Green
    }
    else {
        Write-Host "⚠ Found $($scatteredBackups.Count) scattered backup files" -ForegroundColor Yellow
        Write-Host "  Run: .\backup_manager.ps1 -Action consolidate" -ForegroundColor Gray
    }
    
    # Check spatial metadata
    $metadataPath = Join-Path $script:BackupPath ".aios_spatial_metadata.json"
    if (Test-Path $metadataPath) {
        Write-Host "✓ Spatial metadata present" -ForegroundColor Green
    }
    else {
        Write-Host "⚠ Spatial metadata missing" -ForegroundColor Yellow
    }
}

# Main execution
switch ($Action) {
    "consolidate" { Invoke-BackupConsolidation }
    "cleanup" { Invoke-BackupCleanup }
    "create" { New-AIOSBackup -FilePath $SourceFile }
    "status" { Show-BackupStatus }
}

Write-Host "`nAIOS Backup Management Policy:" -ForegroundColor Blue
Write-Host "• All backup files must be stored in centralized tachyonic/archive/backups/ directory" -ForegroundColor Blue
Write-Host "• Use this script to create properly named backups" -ForegroundColor Blue
Write-Host "• Regular cleanup prevents backup accumulation" -ForegroundColor Blue
Write-Host "• Follows AIOS spatial awareness guidelines" -ForegroundColor Blue