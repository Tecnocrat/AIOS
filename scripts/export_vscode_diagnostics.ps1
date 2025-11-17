# AIOS VSCode Diagnostics Exporter
# Exports Problems panel to JSON for reliable AI agent analysis
# Part of AIOS biological architecture monitoring system

param(
    [string]$WorkspaceRoot = "C:\dev\AIOS",
    [string]$OutputPath = "tachyonic\diagnostics_report.json",
    [switch]$Verbose
)

$ErrorActionPreference = "Stop"

Write-Host "[AIOS] VSCode Diagnostics Exporter" -ForegroundColor Cyan
Write-Host "[DIAGNOSTIC] Workspace: $WorkspaceRoot" -ForegroundColor DarkGray

# Initialize report structure
$report = @{
    timestamp = (Get-Date -Format "o")
    workspace = $WorkspaceRoot
    total_errors = 0
    total_warnings = 0
    total_info = 0
    by_file = @{}
    by_language = @{}
    by_severity = @{
        error = @()
        warning = @()
        information = @()
    }
    summary = ""
}

try {
    # Get VSCode status (includes some diagnostic info)
    Write-Host "[DIAGNOSTIC] Querying VSCode status..." -ForegroundColor DarkGray
    $vscodeStatus = code --status 2>&1 | Out-String
    
    if ($Verbose) {
        Write-Host "[DEBUG] VSCode Status Output:" -ForegroundColor DarkYellow
        Write-Host $vscodeStatus -ForegroundColor DarkGray
    }
    
    # Parse TypeScript errors from workspace
    Write-Host "[DIAGNOSTIC] Scanning TypeScript files..." -ForegroundColor DarkGray
    $tsFiles = Get-ChildItem -Path $WorkspaceRoot -Filter "*.ts" -Recurse -File -ErrorAction SilentlyContinue |
               Where-Object { $_.FullName -notmatch "node_modules|\.git|build|dist" }
    
    $report.summary += "Found $($tsFiles.Count) TypeScript files. "
    
    # Parse Python errors from workspace
    Write-Host "[DIAGNOSTIC] Scanning Python files..." -ForegroundColor DarkGray
    $pyFiles = Get-ChildItem -Path $WorkspaceRoot -Filter "*.py" -Recurse -File -ErrorAction SilentlyContinue |
               Where-Object { $_.FullName -notmatch "__pycache__|\.git|venv|build" }
    
    $report.summary += "Found $($pyFiles.Count) Python files. "
    
    # Parse C# errors from workspace
    Write-Host "[DIAGNOSTIC] Scanning C# files..." -ForegroundColor DarkGray
    $csFiles = Get-ChildItem -Path $WorkspaceRoot -Filter "*.cs" -Recurse -File -ErrorAction SilentlyContinue |
               Where-Object { $_.FullName -notmatch "bin|obj|\.git" }
    
    $report.summary += "Found $($csFiles.Count) C# files. "
    
    # Language statistics
    $report.by_language = @{
        typescript = @{
            file_count = $tsFiles.Count
            error_count = 0
            warning_count = 0
        }
        python = @{
            file_count = $pyFiles.Count
            error_count = 0
            warning_count = 0
        }
        csharp = @{
            file_count = $csFiles.Count
            error_count = 0
            warning_count = 0
        }
    }
    
    # Note: Actual diagnostic parsing requires VSCode extension API
    # This script provides foundation - MCP server will enhance with real-time diagnostics
    $report.summary += "`n`n[NOTE] This is a baseline report. For real-time diagnostics with error details, use AIOS MCP Server."
    $report.summary += "`n[NEXT] MCP server will provide: file-level errors, line numbers, severity, error messages, quick fixes."
    
    # Add metadata
    $report.metadata = @{
        generator = "AIOS VSCode Diagnostics Exporter v1.0"
        requires_mcp = $true
        mcp_server_status = "pending_implementation"
        capabilities = @(
            "Workspace file scanning",
            "Language detection",
            "File counting",
            "Baseline statistics"
        )
        missing_capabilities = @(
            "Real-time error messages",
            "Line number precision",
            "Severity classification",
            "Quick fix suggestions",
            "Cross-file analysis"
        )
    }
    
    # Calculate totals (placeholder until MCP integration)
    $report.total_files = $tsFiles.Count + $pyFiles.Count + $csFiles.Count
    $report.summary += "`n`nTotal files tracked: $($report.total_files)"
    
    # Export to JSON
    $outputFullPath = Join-Path $WorkspaceRoot $OutputPath
    $outputDir = Split-Path $outputFullPath -Parent
    
    if (-not (Test-Path $outputDir)) {
        New-Item -ItemType Directory -Path $outputDir -Force | Out-Null
    }
    
    $report | ConvertTo-Json -Depth 10 | Out-File -FilePath $outputFullPath -Encoding UTF8
    
    Write-Host "[OK] Diagnostics baseline exported to: $OutputPath" -ForegroundColor Green
    Write-Host "[INFO] Total files: $($report.total_files)" -ForegroundColor Cyan
    Write-Host "[NEXT] Implement MCP server for full diagnostic capabilities" -ForegroundColor Yellow
    
    return $report
    
} catch {
    Write-Host "[ERROR] Failed to export diagnostics: $_" -ForegroundColor Red
    throw
}
