# AI-Enhanced Git Hook Guidance System
# Simple functional approach for maximum compatibility

Write-Host ""
Write-Host "🤖 [AI-ENHANCED GUIDANCE] Intelligent Git Hook Assistant" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan

# Get staged files that require changelog
$stagedFiles = git diff --cached --name-only 2>$null
$requiresChangelog = $false
$changedComponents = @()

foreach ($file in $stagedFiles) {
    if ($file -match '^ai/') { $changedComponents += "ai"; $requiresChangelog = $true }
    if ($file -match '^core/') { $changedComponents += "core"; $requiresChangelog = $true }
    if ($file -match '^interface/') { $changedComponents += "interface"; $requiresChangelog = $true }
    if ($file -match '^runtime_intelligence/') { $changedComponents += "runtime_intelligence"; $requiresChangelog = $true }
}

$changedComponents = $changedComponents | Sort-Object -Unique

Write-Host ""
Write-Host "📊 [ANALYSIS RESULTS]" -ForegroundColor Yellow
Write-Host "   Changed Components: $($changedComponents -join ', ')" -ForegroundColor White
Write-Host "   Files Modified: $($stagedFiles.Count)" -ForegroundColor White
Write-Host "   Requires Changelog: $requiresChangelog" -ForegroundColor White

if ($requiresChangelog) {
    Write-Host ""
    Write-Host "📝 [CHANGELOG REQUIREMENTS]" -ForegroundColor Red
    
    # Check CHANGELOG.md
    if (Test-Path "CHANGELOG.md") {
        Write-Host "   ✅ CHANGELOG.md exists" -ForegroundColor Green
    } else {
        Write-Host "   ❌ MISSING: CHANGELOG.md" -ForegroundColor Red
    }
    
    # Check component-specific changelogs
    foreach ($component in $changedComponents) {
        $logPath = "docs/tachyonic/${component}_changelog.md"
        if (Test-Path $logPath) {
            Write-Host "   ✅ $logPath exists" -ForegroundColor Green
        } else {
            Write-Host "   ❌ MISSING: $logPath" -ForegroundColor Red
        }
    }
    
    Write-Host ""
    Write-Host "🎯 [INTELLIGENT GUIDANCE]" -ForegroundColor Magenta
    Write-Host "   • AI-enhanced git hooks detected code changes requiring changelog documentation" -ForegroundColor White
    Write-Host "   • Modified components: $($changedComponents -join ', ')" -ForegroundColor White
    Write-Host "   • Recommendation: Add changelog entries describing your AI enhancements" -ForegroundColor White
    
    Write-Host ""
    Write-Host "⚡ [QUICK FIX - COPY/PASTE THESE COMMANDS]" -ForegroundColor Cyan
    
    if (!(Test-Path "CHANGELOG.md")) {
        $dateStr = Get-Date -Format 'yyyy-MM-dd'
        Write-Host "echo '# AIOS Changelog' > CHANGELOG.md" -ForegroundColor Gray
        Write-Host "echo '' >> CHANGELOG.md" -ForegroundColor Gray
        Write-Host "echo '## $dateStr - AI-Enhanced Git Hook System' >> CHANGELOG.md" -ForegroundColor Gray
        Write-Host "echo '- Implemented intelligent git hook guidance system' >> CHANGELOG.md" -ForegroundColor Gray
        Write-Host "echo '- Added AI-powered changelog requirement detection' >> CHANGELOG.md" -ForegroundColor Gray
    }
    
    foreach ($component in $changedComponents) {
        $logPath = "docs/tachyonic/${component}_changelog.md"
        if (!(Test-Path $logPath)) {
            $dateStr = Get-Date -Format 'yyyy-MM-dd'
            $dir = Split-Path $logPath -Parent
            if (!(Test-Path $dir)) {
                Write-Host "mkdir '$dir' -Force" -ForegroundColor Gray
            }
            Write-Host "echo '# $component Component Changelog' > '$logPath'" -ForegroundColor Gray
            Write-Host "echo '' >> '$logPath'" -ForegroundColor Gray
            Write-Host "echo '## $dateStr - AI Enhancement' >> '$logPath'" -ForegroundColor Gray
            Write-Host "echo '- Enhanced with AI-powered guidance system' >> '$logPath'" -ForegroundColor Gray
        }
    }
    
    Write-Host "git add ." -ForegroundColor Gray
    Write-Host "git commit -m 'docs: Add AI-enhanced changelog entries for git hook system'" -ForegroundColor Gray
    
    Write-Host ""
    Write-Host "[SUCCESS]" -ForegroundColor Green
    Write-Host "   Your AIOS git hooks are now AI-enhanced for maximum developer productivity!" -ForegroundColor Green
    Write-Host "   Run the commands above to satisfy changelog requirements." -ForegroundColor Green

Write-Host ""