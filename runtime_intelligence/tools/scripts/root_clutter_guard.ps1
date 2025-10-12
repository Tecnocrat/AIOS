#!/usr/bin/env pwsh
# AIOS Root Clutter Guard
# Prevents accumulation of temporary and clutter files in root directory
# AINLP Harmonized - Biological Architecture Compliance

param(
    [Parameter(Mandatory=$false)]
    [switch]$ReportOnly,

    [Parameter(Mandatory=$false)]
    [switch]$Clean,

    [Parameter(Mandatory=$false)]
    [switch]$Quiet
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# Configuration
$AIOS_ROOT = Split-Path $PSScriptRoot -Parent
$CONFIG_FILE = Join-Path $AIOS_ROOT "config/system.json"

# Clutter patterns to check
$CLUTTER_PATTERNS = @(
    # Temporary files
    "*.tmp",
    "*.temp",
    "*.bak",
    "*~",

    # OS generated files
    "Thumbs.db",
    ".DS_Store",
    "desktop.ini",

    # IDE files (should be in .gitignore)
    "*.swp",
    "*.swo",
    ".vscode/settings.json",  # Should be in .vscode/ not root
    ".vscode/launch.json",    # Should be in .vscode/ not root

    # Build artifacts
    "*.exe",
    "*.dll",
    "*.so",
    "*.dylib",

    # Log files in root
    "*.log",

    # Test artifacts
    "test_results/",
    "coverage.xml",
    ".coverage",

    # Python artifacts
    "__pycache__/",
    "*.pyc",
    "*.pyo",
    "*.pyd",
    ".pytest_cache/",
    "*.egg-info/",

    # Node artifacts
    "node_modules/",
    "package-lock.json",  # Should be committed if present
    "yarn.lock",          # Should be committed if present

    # Generated documentation
    "coherence_metrics.json",
    "guard_report.json",

    # Backup files
    "*.orig",
    "*.rej"
)

# Allowed root files (everything else is suspicious)
$ALLOWED_ROOT_FILES = @(
    # Core project files
    "AIOS.code-workspace",
    "AIOS.sln",
    "README.md",
    "pyproject.toml",
    "requirements.txt",
    "requirements.in",
    "aios_launch.ps1",  # AINLP namespace coherence: aios_* pattern

    # Config files
    ".editorconfig",
    ".gitignore",
    ".pylintrc",

    # Git files
    ".gitattributes",
    ".gitmodules",

    # VS Code (directory allowed, individual files checked separately)
    ".vscode/",

    # AIOS specific
    ".aios_context.json",
    ".aios_spatial_metadata.json",

    # Documentation
    "AIOS_DEV_PATH.md",

    # Scripts directory
    "scripts/"
)

function Write-Output-IfNotQuiet {
    param([string]$Message)
    if (-not $Quiet) {
        Write-Host $Message
    }
}

function Get-ClutterFiles {
    $clutterFiles = @()

    # Check for files matching clutter patterns
    foreach ($pattern in $CLUTTER_PATTERNS) {
        try {
            $files = Get-ChildItem -Path $AIOS_ROOT -Recurse -File -Filter $pattern -ErrorAction SilentlyContinue
            foreach ($file in $files) {
                $clutterFiles += @{
                    Path = $file.FullName
                    Pattern = $pattern
                    Size = $file.Length
                    LastWriteTime = $file.LastWriteTime
                }
            }
        } catch {
            Write-Output-IfNotQuiet "Warning: Error checking pattern '$pattern': $_"
        }
    }

    # Check for suspicious files in root directory
    $rootFiles = Get-ChildItem -Path $AIOS_ROOT -File
    foreach ($file in $rootFiles) {
        $fileName = $file.Name
        $isAllowed = $false

        foreach ($allowed in $ALLOWED_ROOT_FILES) {
            if ($allowed.EndsWith("/")) {
                # Directory pattern
                if ($fileName.StartsWith($allowed.TrimEnd("/"))) {
                    $isAllowed = $true
                    break
                }
            } elseif ($fileName -eq $allowed) {
                $isAllowed = $true
                break
            }
        }

        if (-not $isAllowed) {
            $clutterFiles += @{
                Path = $file.FullName
                Pattern = "suspicious_root_file"
                Size = $file.Length
                LastWriteTime = $file.LastWriteTime
            }
        }
    }

    return $clutterFiles
}

function Remove-ClutterFile {
    param([string]$FilePath)

    try {
        if (Test-Path $FilePath) {
            Remove-Item $FilePath -Force
            Write-Output-IfNotQuiet "Removed: $FilePath"
            return $true
        }
    } catch {
        Write-Output-IfNotQuiet "Error removing '$FilePath': $_"
    }
    return $false
}

function Get-ClutterReport {
    $clutterFiles = Get-ClutterFiles

    $report = @{
        Timestamp = Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ"
        TotalClutterFiles = $clutterFiles.Count
        TotalSize = ($clutterFiles | Measure-Object -Property Size -Sum).Sum
        Files = $clutterFiles
        Patterns = @{}
    }

    # Group by pattern
    foreach ($file in $clutterFiles) {
        $pattern = $file.Pattern
        if (-not $report.Patterns.ContainsKey($pattern)) {
            $report.Patterns[$pattern] = @()
        }
        $report.Patterns[$pattern] += $file.Path
    }

    return $report
}

# Main execution
Write-Output-IfNotQuiet "AIOS Root Clutter Guard - Scanning for workspace clutter..."

$report = Get-ClutterReport

if ($ReportOnly) {
    # Just report, don't clean
    Write-Output-IfNotQuiet "Found $($report.TotalClutterFiles) clutter files ($([math]::Round($report.TotalSize / 1MB, 2)) MB)"

    if ($report.TotalClutterFiles -gt 0) {
        Write-Output-IfNotQuiet "Clutter files by pattern:"
        foreach ($pattern in $report.Patterns.Keys) {
            Write-Output-IfNotQuiet "  $pattern ($($report.Patterns[$pattern].Count) files):"
            foreach ($file in $report.Patterns[$pattern]) {
                Write-Output-IfNotQuiet "    $file"
            }
        }
    } else {
        Write-Output-IfNotQuiet "No clutter files found - workspace is clean!"
    }

    # Output JSON for CI
    $report | ConvertTo-Json -Depth 10
} elseif ($Clean) {
    # Clean mode - remove clutter
    Write-Output-IfNotQuiet "Cleaning $($report.TotalClutterFiles) clutter files..."

    $removedCount = 0
    foreach ($file in $report.Files) {
        if (Remove-ClutterFile -FilePath $file.Path) {
            $removedCount++
        }
    }

    Write-Output-IfNotQuiet "Cleaned $removedCount of $($report.TotalClutterFiles) clutter files"

    if ($removedCount -ne $report.TotalClutterFiles) {
        Write-Output-IfNotQuiet "Warning: Some files could not be removed"
        exit 1
    }
} else {
    # Default mode - check and fail if clutter found
    if ($report.TotalClutterFiles -gt 0) {
        Write-Output-IfNotQuiet "ERROR: Found $($report.TotalClutterFiles) clutter files in workspace!"
        Write-Output-IfNotQuiet "Run with -Clean to remove clutter, or -ReportOnly to see details"

        foreach ($file in $report.Files) {
            Write-Output-IfNotQuiet "  $($file.Pattern): $($file.Path)"
        }

        exit 1
    } else {
        Write-Output-IfNotQuiet "Workspace clutter check passed - no clutter files found"
    }
}