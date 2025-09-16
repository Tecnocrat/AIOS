# AIOS Executable Architecture Analyzer
# Purpose: Identify which Python files should be executable vs library modules

param(
    [string]$ScanPath = ".",
    [switch]$RemoveUnnecessaryShebang = $false
)

function Analyze-PythonExecutableNecessity {
    param([string]$ProjectRoot)
    
    Write-Host "`n🧬 [AIOS-EXECUTABLE-ANALYZER] Analyzing Python file architecture..." -ForegroundColor Cyan
    
    # Define patterns that indicate a file should be executable
    $ExecutablePatterns = @(
        'if __name__ == [''"]__main__[''"]',
        'def main\(',
        'parser\.parse_args\(',
        'argparse\.ArgumentParser',
        'click\.command',
        'typer\.run',
        'sys\.argv',
        'subprocess\.run',
        'subprocess\.call'
    )
    
    # Define patterns that indicate a file is primarily a library
    $LibraryPatterns = @(
        'class \w+',
        'def \w+\(',
        'from \w+ import',
        'import \w+'
    )
    
    $Results = @{
        ShouldBeExecutable = @()
        ShouldBeLibrary = @()
        Uncertain = @()
        CurrentlyExecutable = @()
    }
    
    # Scan all Python files
    Get-ChildItem -Path $ProjectRoot -Recurse -Filter "*.py" | ForEach-Object {
        $FilePath = $_.FullName
        $RelativePath = $FilePath -replace [regex]::Escape($ProjectRoot), "."
        $Content = Get-Content $FilePath -Raw -ErrorAction SilentlyContinue
        
        if (-not $Content) { return }
        
        # Check if currently has shebang
        $HasShebang = $Content -match '^#!'
        if ($HasShebang) {
            $Results.CurrentlyExecutable += $RelativePath
        }
        
        # Analyze patterns
        $ExecutableScore = 0
        $LibraryScore = 0
        
        foreach ($Pattern in $ExecutablePatterns) {
            if ($Content -match $Pattern) {
                $ExecutableScore++
            }
        }
        
        foreach ($Pattern in $LibraryPatterns) {
            if ($Content -match $Pattern) {
                $LibraryScore++
            }
        }
        
        # Classification logic
        if ($ExecutableScore -gt 0 -and ($Content -match 'if __name__ == [''"]__main__[''"]')) {
            $Results.ShouldBeExecutable += @{
                Path = $RelativePath
                Reason = "Has main execution block"
                Score = $ExecutableScore
                HasShebang = $HasShebang
            }
        } elseif ($LibraryScore -gt $ExecutableScore -and $ExecutableScore -eq 0) {
            $Results.ShouldBeLibrary += @{
                Path = $RelativePath
                Reason = "Library/module pattern, no main execution"
                Score = $LibraryScore
                HasShebang = $HasShebang
            }
        } else {
            $Results.Uncertain += @{
                Path = $RelativePath
                Reason = "Mixed patterns or unclear intent"
                ExecutableScore = $ExecutableScore
                LibraryScore = $LibraryScore
                HasShebang = $HasShebang
            }
        }
    }
    
    # Display analysis
    Write-Host "`n📊 [ANALYSIS-RESULTS] Python Executable Architecture Analysis:" -ForegroundColor Yellow
    Write-Host "   Currently Executable: $($Results.CurrentlyExecutable.Count)" -ForegroundColor White
    Write-Host "   Should Be Executable: $($Results.ShouldBeExecutable.Count)" -ForegroundColor Green
    Write-Host "   Should Be Library: $($Results.ShouldBeLibrary.Count)" -ForegroundColor Blue
    Write-Host "   Uncertain Classification: $($Results.Uncertain.Count)" -ForegroundColor Yellow
    
    # Identify optimization opportunities
    $UnnecessaryExecutables = $Results.ShouldBeLibrary | Where-Object { $_.HasShebang }
    $MissingExecutables = $Results.ShouldBeExecutable | Where-Object { -not $_.HasShebang }
    
    if ($UnnecessaryExecutables.Count -gt 0) {
        Write-Host "`n🔧 [OPTIMIZATION] Files with unnecessary shebang lines:" -ForegroundColor Red
        $UnnecessaryExecutables | ForEach-Object {
            Write-Host "   - $($_.Path) ($($_.Reason))" -ForegroundColor White
        }
    }
    
    if ($MissingExecutables.Count -gt 0) {
        Write-Host "`n➕ [ENHANCEMENT] Files that should be executable:" -ForegroundColor Green
        $MissingExecutables | ForEach-Object {
            Write-Host "   + $($_.Path) ($($_.Reason))" -ForegroundColor White
        }
    }
    
    # Generate recommendations
    Write-Host "`n💡 [RECOMMENDATIONS] AIOS Executable Architecture Improvements:" -ForegroundColor Cyan
    Write-Host "   1. Remove shebangs from $($UnnecessaryExecutables.Count) library files" -ForegroundColor White
    Write-Host "   2. Add shebangs to $($MissingExecutables.Count) executable scripts" -ForegroundColor White
    Write-Host "   3. Review $($Results.Uncertain.Count) uncertain files for proper classification" -ForegroundColor White
    
    $ReductionPercentage = [math]::Round(($UnnecessaryExecutables.Count / $Results.CurrentlyExecutable.Count) * 100, 1)
    Write-Host "`n🎯 [IMPACT] Potential $ReductionPercentage% reduction in executable entry points" -ForegroundColor Magenta
    Write-Host "   This creates a leaner, more secure execution pipeline aligned with AINLP principles" -ForegroundColor DarkCyan
    
    if ($RemoveUnnecessaryShebang) {
        Write-Host "`n🔄 [EXECUTING] Removing unnecessary shebang lines..." -ForegroundColor Yellow
        foreach ($File in $UnnecessaryExecutables) {
            Remove-UnnecessaryShebang -FilePath (Join-Path $ProjectRoot $File.Path)
        }
        Write-Host "   ✅ Optimization complete!" -ForegroundColor Green
    } else {
        Write-Host "`n📋 [PREVIEW] Use -RemoveUnnecessaryShebang to apply optimizations" -ForegroundColor Gray
    }
    
    return $Results
}

function Remove-UnnecessaryShebang {
    param([string]$FilePath)
    
    $Content = Get-Content $FilePath -Raw
    if ($Content -match '^#![^\r\n]*[\r\n]+') {
        $NewContent = $Content -replace '^#![^\r\n]*[\r\n]+', ''
        Set-Content -Path $FilePath -Value $NewContent -NoNewline
        Write-Host "   Removed shebang from: $(Split-Path $FilePath -Leaf)" -ForegroundColor Gray
    }
}

# Execute analysis
if ($MyInvocation.InvocationName -ne '.') {
    $Results = Analyze-PythonExecutableNecessity -ProjectRoot (Get-Location).Path
    
    Write-Host "`n🧬 [BIOLOGICAL-METAPHOR] Architecture Alignment:" -ForegroundColor Magenta
    Write-Host "   📚 Library Modules = DNA/RNA (information storage)" -ForegroundColor Blue
    Write-Host "   ⚡ Executable Scripts = Enzymes/Proteins (catalytic action)" -ForegroundColor Green
    Write-Host "   🔬 Entry Points = Cell Membrane Receptors (controlled access)" -ForegroundColor Cyan
    Write-Host "`n   This creates a more efficient, secure, and maintainable codebase!" -ForegroundColor White
}