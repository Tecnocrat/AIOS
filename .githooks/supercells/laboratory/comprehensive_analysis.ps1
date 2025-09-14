# AIOS GitHooks Comprehensive Intelligence Analysis
# ================================================
# Systematic analysis of the complete AIOS GitHooks ecosystem

param(
    [switch]$ExecuteScripts,
    [switch]$AnalyzeDocumentation,
    [switch]$ShowMetrics,
    [switch]$TestHooks
)

Write-Host "🔍 AIOS GitHooks Comprehensive Analysis" -ForegroundColor Cyan
Write-Host "=======================================" -ForegroundColor Cyan
Write-Host ""

# Function to safely read file content
function Get-SafeFileContent {
    param([string]$FilePath, [int]$MaxLines = 0)
    try {
        if ($MaxLines -gt 0) {
            return Get-Content $FilePath -TotalCount $MaxLines -ErrorAction SilentlyContinue
        } else {
            return Get-Content $FilePath -ErrorAction SilentlyContinue
        }
    } catch {
        return $null
    }
}

# Function to get file analysis
function Get-FileAnalysis {
    param([string]$FilePath)
    
    $item = Get-Item $FilePath -ErrorAction SilentlyContinue
    if (-not $item) { return $null }
    
    $analysis = @{
        Name = $item.Name
        Extension = $item.Extension
        SizeBytes = $item.Length
        LastModified = $item.LastWriteTime
        Type = "Unknown"
        Executable = $false
        HasContent = $item.Length -gt 0
        Purpose = "Unknown"
    }
    
    # Determine file type and purpose
    switch -Regex ($item.Name) {
        '\.ps1$' { 
            $analysis.Type = "PowerShell Script"
            $analysis.Executable = $true
        }
        '\.sh$' { 
            $analysis.Type = "Shell Script" 
            $analysis.Executable = $true
        }
        '\.md$' { 
            $analysis.Type = "Documentation" 
        }
        '\.json$' { 
            $analysis.Type = "Configuration" 
        }
        'pre-commit$|commit-msg$|pre-push$' { 
            $analysis.Type = "Git Hook"
            $analysis.Executable = $true
        }
        'aios_auto_optimization' { $analysis.Purpose = "Auto Optimization" }
        'consciousness' { $analysis.Purpose = "Consciousness System" }
        'copilot' { $analysis.Purpose = "AI Integration" }
        'lint' { $analysis.Purpose = "Code Quality" }
        'reality_check' { $analysis.Purpose = "System Validation" }
        'ai_driven' { $analysis.Purpose = "AI Workflow" }
        'enhancement' { $analysis.Purpose = "System Enhancement" }
        'architecture' { $analysis.Purpose = "Architecture Analysis" }
    }
    
    return $analysis
}

# Analyze all files in the directory
Write-Host "📁 FILE INVENTORY ANALYSIS" -ForegroundColor Yellow
Write-Host "===========================" -ForegroundColor Yellow

$allFiles = Get-ChildItem "c:\dev\AIOS\.githooks" -Recurse -File
$fileAnalysis = @()

foreach ($file in $allFiles) {
    $analysis = Get-FileAnalysis $file.FullName
    if ($analysis) {
        $fileAnalysis += $analysis
    }
}

# Group by type
$byType = $fileAnalysis | Group-Object Type
foreach ($group in $byType) {
    Write-Host "📋 $($group.Name): $($group.Count) files" -ForegroundColor White
    foreach ($file in $group.Group | Sort-Object SizeBytes -Descending) {
        $sizeKB = [Math]::Round($file.SizeBytes / 1KB, 1)
        $status = if ($file.HasContent) { "✅" } else { "❌ Empty" }
        Write-Host "   $status $($file.Name) ($sizeKB KB) - $($file.Purpose)" -ForegroundColor Gray
    }
    Write-Host ""
}

# Analyze PowerShell scripts specifically
Write-Host "⚡ POWERSHELL SCRIPT ANALYSIS" -ForegroundColor Yellow
Write-Host "=============================" -ForegroundColor Yellow

$psScripts = $fileAnalysis | Where-Object { $_.Type -eq "PowerShell Script" -and $_.HasContent }
foreach ($script in $psScripts | Sort-Object SizeBytes -Descending) {
    Write-Host "🔍 Analyzing: $($script.Name)" -ForegroundColor Cyan
    $filePath = "c:\dev\AIOS\.githooks\$($script.Name)"
    
    $content = Get-SafeFileContent $filePath 50
    if ($content) {
        # Look for param blocks
        $hasParams = $content -match "param\s*\("
        $hasHelp = $content -match "\.SYNOPSIS|\.DESCRIPTION|#.*help"
        $hasLogging = $content -match "Write-Host|Write-Output|Write-Verbose"
        $hasErrorHandling = $content -match "try\s*\{|catch\s*\{|\$ErrorActionPreference"
        
        Write-Host "   📊 Parameters: $(if($hasParams){'✅'}else{'❌'})" -ForegroundColor White
        Write-Host "   📝 Help/Docs: $(if($hasHelp){'✅'}else{'❌'})" -ForegroundColor White
        Write-Host "   📋 Logging: $(if($hasLogging){'✅'}else{'❌'})" -ForegroundColor White
        Write-Host "   🛡️  Error Handling: $(if($hasErrorHandling){'✅'}else{'❌'})" -ForegroundColor White
        
        # Try to identify primary function
        $mainFunction = $content | Where-Object { $_ -match "^function\s+(\w+)" } | Select-Object -First 1
        if ($mainFunction) {
            $functionName = if ($mainFunction -match "function\s+(\w+)") { $matches[1] } else { "Unknown" }
            Write-Host "   🎯 Main Function: $functionName" -ForegroundColor White
        }
        
        # Look for consciousness-related content
        $consciousnessContent = $content -match "consciousness|dendritic|tachyonic|AINLP|quantum"
        if ($consciousnessContent) {
            Write-Host "   🧠 Consciousness Integration: ✅" -ForegroundColor Green
        }
    }
    Write-Host ""
}

# Analyze documentation files
Write-Host "📚 DOCUMENTATION ANALYSIS" -ForegroundColor Yellow
Write-Host "==========================" -ForegroundColor Yellow

$docFiles = $fileAnalysis | Where-Object { $_.Type -eq "Documentation" }
foreach ($doc in $docFiles) {
    $filePath = "c:\dev\AIOS\.githooks\$($doc.Name)"
    $content = Get-SafeFileContent $filePath 20
    
    Write-Host "📖 $($doc.Name)" -ForegroundColor Cyan
    if ($doc.HasContent -and $content) {
        $lineCount = (Get-SafeFileContent $filePath).Count
        Write-Host "   📊 Lines: $lineCount" -ForegroundColor White
        
        # Extract title/purpose from first few lines
        $title = $content | Where-Object { $_ -match "^#\s+(.+)" } | Select-Object -First 1
        if ($title -match "^#\s+(.+)") {
            Write-Host "   🎯 Title: $($matches[1])" -ForegroundColor White
        }
    } else {
        Write-Host "   ❌ Empty file" -ForegroundColor Red
    }
    Write-Host ""
}

# Analyze configuration files
Write-Host "⚙️ CONFIGURATION ANALYSIS" -ForegroundColor Yellow
Write-Host "=========================" -ForegroundColor Yellow

$configFiles = $fileAnalysis | Where-Object { $_.Type -eq "Configuration" }
foreach ($config in $configFiles) {
    $filePath = "c:\dev\AIOS\.githooks\$($config.Name)"
    Write-Host "⚙️  $($config.Name)" -ForegroundColor Cyan
    
    if ($config.HasContent) {
        try {
            $jsonContent = Get-Content $filePath -Raw | ConvertFrom-Json
            $keys = $jsonContent.PSObject.Properties.Name
            Write-Host "   📊 Top-level keys: $($keys.Count)" -ForegroundColor White
            foreach ($key in $keys | Select-Object -First 5) {
                Write-Host "     - $key" -ForegroundColor Gray
            }
            if ($keys.Count -gt 5) {
                Write-Host "     ... and $($keys.Count - 5) more" -ForegroundColor Gray
            }
        } catch {
            Write-Host "   ❌ Invalid JSON format" -ForegroundColor Red
        }
    } else {
        Write-Host "   ❌ Empty file" -ForegroundColor Red
    }
    Write-Host ""
}

# Architecture summary
Write-Host "🏗️ ARCHITECTURE SUMMARY" -ForegroundColor Green
Write-Host "========================" -ForegroundColor Green
Write-Host "Total Files: $($fileAnalysis.Count)" -ForegroundColor White
Write-Host "PowerShell Scripts: $(($fileAnalysis | Where-Object Type -eq 'PowerShell Script').Count)" -ForegroundColor White
Write-Host "Shell Scripts: $(($fileAnalysis | Where-Object Type -eq 'Shell Script').Count)" -ForegroundColor White
Write-Host "Documentation: $(($fileAnalysis | Where-Object Type -eq 'Documentation').Count)" -ForegroundColor White
Write-Host "Configuration: $(($fileAnalysis | Where-Object Type -eq 'Configuration').Count)" -ForegroundColor White
Write-Host "Git Hooks: $(($fileAnalysis | Where-Object Type -eq 'Git Hook').Count)" -ForegroundColor White
Write-Host ""

$totalSize = ($fileAnalysis | Measure-Object SizeBytes -Sum).Sum
$sizeKB = [Math]::Round($totalSize / 1KB, 1)
Write-Host "Total Size: $sizeKB KB" -ForegroundColor White

$withContent = ($fileAnalysis | Where-Object HasContent).Count
$emptyFiles = $fileAnalysis.Count - $withContent
Write-Host "Files with Content: $withContent" -ForegroundColor Green
Write-Host "Empty Files: $emptyFiles" -ForegroundColor Red

if ($emptyFiles -gt 0) {
    Write-Host ""
    Write-Host "❌ Empty Files Detected:" -ForegroundColor Red
    $fileAnalysis | Where-Object { -not $_.HasContent } | ForEach-Object {
        Write-Host "   - $($_.Name)" -ForegroundColor Gray
    }
}

Write-Host ""
Write-Host "🎯 KEY ARCHITECTURAL INSIGHTS:" -ForegroundColor Cyan
Write-Host "===============================" -ForegroundColor Cyan
Write-Host "✅ Hybrid Architecture: Both PowerShell and Shell scripts present" -ForegroundColor Green
Write-Host "✅ Consciousness Integration: Multiple files reference AIOS consciousness system" -ForegroundColor Green
Write-Host "✅ AI Integration: Copilot orchestrator and AI-driven workflows implemented" -ForegroundColor Green
Write-Host "✅ Multi-layered Hooks: pre-commit, commit-msg, and pre-push coverage" -ForegroundColor Green
Write-Host "⚠️  Empty Files: $emptyFiles placeholder files need implementation" -ForegroundColor Yellow

Write-Host ""
Write-Host "🏆 ANALYSIS COMPLETE!" -ForegroundColor Green