# AIOS GitHooks Empty File Cleanup
# =================================
# Identifies and handles empty placeholder files

param(
    [switch]$ListOnly,
    [switch]$RemoveEmpty,
    [switch]$CreateStubs,
    [switch]$DetailedReport
)

$GitHooksPath = Split-Path $PSScriptRoot -Parent | Split-Path -Parent
$EmptyFiles = @()
$TotalFiles = 0
$TotalSize = 0

Write-Host "AIOS GITHOOKS EMPTY FILE CLEANUP" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""

# Scan for empty files
Get-ChildItem $GitHooksPath -Recurse -File | ForEach-Object {
    $TotalFiles++
    $TotalSize += $_.Length
    
    if ($_.Length -eq 0) {
        $EmptyFiles += $_
    }
}

Write-Host "SCAN RESULTS:" -ForegroundColor Yellow
Write-Host "Total Files: $TotalFiles" -ForegroundColor White
Write-Host "Total Size: $([math]::Round($TotalSize / 1KB, 1)) KB" -ForegroundColor White
Write-Host "Empty Files: $($EmptyFiles.Count)" -ForegroundColor $(if ($EmptyFiles.Count -gt 0) { "Red" } else { "Green" })
Write-Host ""

if ($EmptyFiles.Count -eq 0) {
    Write-Host "[CLEAN] No empty files found!" -ForegroundColor Green
    exit 0
}

Write-Host "EMPTY FILES DETECTED:" -ForegroundColor Red
Write-Host "=====================" -ForegroundColor Red

$FilesByCategory = @{
    "PowerShell Scripts" = @()
    "Shell Scripts" = @()
    "Documentation" = @()
    "Configuration" = @()
    "Other" = @()
}

foreach ($File in $EmptyFiles) {
    $RelativePath = $File.FullName.Replace($GitHooksPath, "").TrimStart('\')
    $Category = switch ($File.Extension.ToLower()) {
        ".ps1" { "PowerShell Scripts" }
        ".sh" { "Shell Scripts" }
        ".md" { "Documentation" }
        ".json" { "Configuration" }
        ".yml" { "Configuration" }
        ".yaml" { "Configuration" }
        default { "Other" }
    }
    
    $FilesByCategory[$Category] += $RelativePath
    
    if ($DetailedReport) {
        $LastWrite = $File.LastWriteTime.ToString("yyyy-MM-dd HH:mm")
        Write-Host "  [EMPTY] $RelativePath (Modified: $LastWrite)" -ForegroundColor Gray
    }
}

# Display categorized results
foreach ($Category in $FilesByCategory.Keys) {
    if ($FilesByCategory[$Category].Count -gt 0) {
        Write-Host ""
        Write-Host "$Category ($($FilesByCategory[$Category].Count) files):" -ForegroundColor Yellow
        foreach ($File in $FilesByCategory[$Category]) {
            Write-Host "  - $File" -ForegroundColor Gray
        }
    }
}

if ($ListOnly) {
    Write-Host ""
    Write-Host "[LIST-ONLY] Use -RemoveEmpty or -CreateStubs to take action" -ForegroundColor Yellow
    exit 0
}

if ($RemoveEmpty) {
    Write-Host ""
    Write-Host "REMOVING EMPTY FILES..." -ForegroundColor Red
    
    foreach ($File in $EmptyFiles) {
        try {
            Remove-Item $File.FullName -Force
            $RelativePath = $File.FullName.Replace($GitHooksPath, "").TrimStart('\')
            Write-Host "  [REMOVED] $RelativePath" -ForegroundColor Red
        } catch {
            Write-Host "  [ERROR] Failed to remove $($File.Name): $($_.Exception.Message)" -ForegroundColor Red
        }
    }
    
    Write-Host ""
    Write-Host "[CLEANUP COMPLETE] $($EmptyFiles.Count) empty files removed" -ForegroundColor Green
}

if ($CreateStubs) {
    Write-Host ""
    Write-Host "CREATING IMPLEMENTATION STUBS..." -ForegroundColor Green
    
    $StubTemplates = @{
        ".ps1" = @"
# AIOS GitHook Script
# ===================
# TODO: Implement this script

param(
    [switch]`$Help
)

if (`$Help) {
    Write-Host "AIOS GitHook Script" -ForegroundColor Cyan
    Write-Host "TODO: Add help documentation" -ForegroundColor Yellow
    exit 0
}

Write-Host "TODO: Implement script functionality" -ForegroundColor Yellow
exit 0
"@
        ".sh" = @"
#!/bin/bash
# AIOS GitHook Shell Script
# =========================
# TODO: Implement this script

echo "TODO: Implement shell script functionality"
exit 0
"@
        ".md" = @"
# AIOS GitHook Documentation

## Purpose
TODO: Document the purpose of this component

## Usage
TODO: Add usage instructions

## Implementation Status
- [ ] TODO: Implement functionality
- [ ] TODO: Add comprehensive documentation
- [ ] TODO: Add examples
"@
        ".json" = @"
{
  "TODO": "Implement configuration",
  "version": "1.0.0",
  "description": "AIOS GitHook configuration file"
}
"@
    }
    
    foreach ($File in $EmptyFiles) {
        $Extension = $File.Extension.ToLower()
        $Template = $StubTemplates[$Extension]
        
        if ($Template) {
            try {
                Set-Content -Path $File.FullName -Value $Template -Encoding UTF8
                $RelativePath = $File.FullName.Replace($GitHooksPath, "").TrimStart('\')
                Write-Host "  [CREATED] Stub for $RelativePath" -ForegroundColor Green
            } catch {
                Write-Host "  [ERROR] Failed to create stub for $($File.Name): $($_.Exception.Message)" -ForegroundColor Red
            }
        } else {
            $RelativePath = $File.FullName.Replace($GitHooksPath, "").TrimStart('\')
            Write-Host "  [SKIPPED] No template for $RelativePath" -ForegroundColor Yellow
        }
    }
    
    Write-Host ""
    Write-Host "[STUB CREATION COMPLETE] Implementation stubs created" -ForegroundColor Green
}

Write-Host ""
Write-Host "RECOMMENDATIONS:" -ForegroundColor Yellow
Write-Host "=================" -ForegroundColor Yellow
Write-Host "1. Review empty files and determine which are needed" -ForegroundColor Gray
Write-Host "2. Use -CreateStubs to create implementation templates" -ForegroundColor Gray
Write-Host "3. Use -RemoveEmpty to clean up unnecessary files" -ForegroundColor Gray
Write-Host "4. Prioritize implementing critical missing functionality" -ForegroundColor Gray

exit 0