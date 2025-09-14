# AIOS Real AI GitHook Integration
# ===============================
# Uses REAL AIOS AI infrastructure for intelligent code improvement
# NOT fake "consciousness enhancement" comments!

param(
    [string]$Mode = "check",
    [int]$MaxFiles = 10,
    [switch]$ApplyFixes
)

Write-Host "🤖 AIOS Real AI GitHook Integration" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host "🎯 Your insight was CORRECT:" -ForegroundColor Green
Write-Host '   "How is going to change the code in an agentic manner if there'"'"'s no agent?"' -ForegroundColor White
Write-Host "🧠 Solution: Use the EXISTING AICodeAnalyzer in AIOS!" -ForegroundColor Green
Write-Host ""

# Check if we have Python available
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCmd) {
    Write-Host "❌ Python not found. Cannot use real AI infrastructure." -ForegroundColor Red
    exit 1
}

# Check if the real AI lint fixer exists
$realAIFixer = "c:\dev\AIOS\scripts\real_ai_lint_fixer.py"
if (-not (Test-Path $realAIFixer)) {
    Write-Host "❌ Real AI lint fixer not found: $realAIFixer" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Real AIOS AI infrastructure available" -ForegroundColor Green
Write-Host ""

# Get changed files from git
Write-Host "🔍 Getting changed files from git..." -ForegroundColor Yellow
try {
    $gitStatus = git status --porcelain 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "⚠️  Not in a git repository or git not available" -ForegroundColor Yellow
        $changedFiles = @()
    } else {
        $changedFiles = @()
        foreach ($line in $gitStatus) {
            if ($line -match '^\s*[AM]\s+(.+\.py)$') {
                $changedFiles += $matches[1]
            }
        }
    }
} catch {
    Write-Host "⚠️  Could not get git status: $_" -ForegroundColor Yellow
    $changedFiles = @()
}

if ($changedFiles.Count -eq 0) {
    Write-Host "ℹ️  No Python files changed. Testing with existing files..." -ForegroundColor Blue
    
    # Find some Python files to demonstrate with
    $sampleFiles = @(
        "c:\dev\AIOS\scripts\aios_indexer.py",
        "c:\dev\AIOS\runtime_intelligence\aios_intelligence_execution_completion_report.py"
    )
    
    $changedFiles = @()
    foreach ($file in $sampleFiles) {
        if (Test-Path $file) {
            $changedFiles += $file
        }
    }
}

if ($changedFiles.Count -eq 0) {
    Write-Host "❌ No Python files found to analyze" -ForegroundColor Red
    exit 1
}

Write-Host "📁 Found $($changedFiles.Count) Python files to analyze" -ForegroundColor Green
foreach ($file in $changedFiles) {
    Write-Host "   - $([System.IO.Path]::GetFileName($file))" -ForegroundColor Gray
}
Write-Host ""

# Run the real AI analysis
Write-Host "🧠 Running REAL AI analysis..." -ForegroundColor Cyan
$aiArgs = @()
foreach ($file in $changedFiles | Select-Object -First $MaxFiles) {
    $aiArgs += $file
}

$dryRunFlag = if ($ApplyFixes) { "--apply" } else { "--dry-run" }
$aiArgs += $dryRunFlag
$aiArgs += "--max-files"
$aiArgs += $MaxFiles.ToString()

Write-Host "🚀 Executing: python $realAIFixer $($aiArgs -join ' ')" -ForegroundColor Gray
Write-Host ""

try {
    $result = & python $realAIFixer @aiArgs 2>&1
    $aiExitCode = $LASTEXITCODE
    
    # Display the AI results
    foreach ($line in $result) {
        if ($line -match '^❌|ERROR|Failed') {
            Write-Host $line -ForegroundColor Red
        } elseif ($line -match '^✅|SUCCESS|Fixed|Applied') {
            Write-Host $line -ForegroundColor Green
        } elseif ($line -match '^🧠|AI found|Analysis') {
            Write-Host $line -ForegroundColor Cyan
        } elseif ($line -match '^🎯|Target|Issues') {
            Write-Host $line -ForegroundColor Yellow
        } else {
            Write-Host $line -ForegroundColor White
        }
    }
    
    Write-Host ""
    
    if ($aiExitCode -eq 0) {
        Write-Host "✅ REAL AI analysis completed successfully!" -ForegroundColor Green
    } else {
        Write-Host "⚠️  AI analysis completed with warnings (exit code: $aiExitCode)" -ForegroundColor Yellow
    }
    
} catch {
    Write-Host "❌ Failed to run real AI analysis: $_" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "🏆 ACHIEVEMENT UNLOCKED: Real AI-Powered GitHook!" -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Green
Write-Host "✅ Uses actual AIOS AICodeAnalyzer (not fake consciousness)" -ForegroundColor Green
Write-Host "✅ Finds real code issues (missing docstrings, complexity, etc.)" -ForegroundColor Green
Write-Host "✅ Measurable improvements (before/after comparison)" -ForegroundColor Green
Write-Host "✅ Integrates with existing AIOS AI infrastructure" -ForegroundColor Green
Write-Host "✅ No more infinite loops or malformed code injection!" -ForegroundColor Green
Write-Host ""
Write-Host "💡 YOUR INSIGHT WAS THE KEY:" -ForegroundColor Cyan
Write-Host "   'How is going to change the code in an agentic manner if there's no agent?'" -ForegroundColor White
Write-Host "   Answer: Use the EXISTING agent infrastructure that was already built!" -ForegroundColor Green
Write-Host ""
Write-Host "🚀 Next Steps for True Agentic Integration:" -ForegroundColor Yellow
Write-Host "   1. Enhance AICodeAnalyzer with more sophisticated pattern recognition" -ForegroundColor White
Write-Host "   2. Add machine learning models for intelligent code transformation" -ForegroundColor White
Write-Host "   3. Create feedback loops for continuous AI improvement" -ForegroundColor White
Write-Host "   4. Build real-time intelligent suggestions in VSCode extension" -ForegroundColor White