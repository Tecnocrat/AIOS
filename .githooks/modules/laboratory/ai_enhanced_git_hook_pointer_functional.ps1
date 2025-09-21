# AI-Enhanced Git Hook Pointer - Functional Version
# Provides intelligent guidance for git hook compliance

function Write-AIGuidanceHeader {
    Write-Host "`n🤖 [AI-ENHANCED GUIDANCE] Intelligent Git Hook Assistant" -ForegroundColor Cyan
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
}

function Get-ChangeAnalysis {
    param([string]$RepositoryPath = (Get-Location))
    
    # Get changed files
    $stagedFiles = @(git diff --cached --name-only 2>$null)
    $changedPaths = @()
    $changeTypes = @()
    
    foreach ($file in $stagedFiles) {
        if ($file -match '^ai/') { $changedPaths += "ai" }
        if ($file -match '^core/') { $changedPaths += "core" }
        if ($file -match '^interface/') { $changedPaths += "interface" }
        if ($file -match '^runtime_intelligence/') { $changedPaths += "runtime_intelligence" }
        
        # Detect change type from file content
        if ($file -match '\.(py|cs|cpp|h)$') {
            $content = git show ":$file" 2>$null
            if ($content -match '(class|function|def|public|private)') {
                $changeTypes += "feat"
            }
        }
    }
    
    return @{
        changed_paths = ($changedPaths | Sort-Object -Unique)
        change_types = ($changeTypes | Sort-Object -Unique)
        staged_files = $stagedFiles
        requires_changelog = ($changedPaths.Count -gt 0)
    }
}

function Get-RequiredChangelogs {
    param([array]$ChangedPaths)
    
    $requiredLogs = @()
    
    # Root changelog always required for major changes
    if ($ChangedPaths.Count -gt 0) {
        $requiredLogs += "CHANGELOG.md"
    }
    
    # Tachyonic changelogs for specific paths
    foreach ($path in $ChangedPaths) {
        switch ($path) {
            "ai" { $requiredLogs += "docs/tachyonic/ai_changelog.md" }
            "core" { $requiredLogs += "docs/tachyonic/core_changelog.md" }
            "interface" { $requiredLogs += "docs/tachyonic/interface_changelog.md" }
            "runtime_intelligence" { $requiredLogs += "docs/tachyonic/runtime_intelligence_changelog.md" }
        }
    }
    
    return ($requiredLogs | Sort-Object -Unique)
}

function Write-IntelligentGuidance {
    param([hashtable]$Analysis)
    
    Write-Host "`n📊 [ANALYSIS RESULTS]" -ForegroundColor Yellow
    Write-Host "   Changed Components: $($Analysis.changed_paths -join ', ')" -ForegroundColor White
    Write-Host "   Change Types: $($Analysis.change_types -join ', ')" -ForegroundColor White
    Write-Host "   Files Modified: $($Analysis.staged_files.Count)" -ForegroundColor White
    Write-Host "   Requires Changelog: $($Analysis.requires_changelog)" -ForegroundColor White
    
    if ($Analysis.requires_changelog) {
        $requiredLogs = Get-RequiredChangelogs -ChangedPaths $Analysis.changed_paths
        
        Write-Host "`n📝 [REQUIRED CHANGELOGS]" -ForegroundColor Red
        foreach ($log in $requiredLogs) {
            if (Test-Path $log) {
                Write-Host "   ✅ EXISTS: $log" -ForegroundColor Green
            } else {
                Write-Host "   ❌ MISSING: $log" -ForegroundColor Red
                Write-Host "      Quick fix: echo '## $(Get-Date -Format 'yyyy-MM-dd') - AI Enhancement' >> '$log'" -ForegroundColor Gray
            }
        }
        
        Write-Host "`n🎯 [INTELLIGENT SUGGESTIONS]" -ForegroundColor Magenta
        Write-Host "   1. Create missing changelog entries using AI guidance templates" -ForegroundColor White
        Write-Host "   2. Include impact assessment for each component modified" -ForegroundColor White
        Write-Host "   3. Tag with appropriate change type: feat/fix/docs/refactor" -ForegroundColor White
        Write-Host "   4. Consider integration testing for multi-component changes" -ForegroundColor White
        
        Write-Host "`n⚡ [ONE-COMMAND FIX]" -ForegroundColor Cyan
        $dateStr = Get-Date -Format 'yyyy-MM-dd'
        foreach ($log in $requiredLogs) {
            if (!(Test-Path $log)) {
                $dir = Split-Path $log -Parent
                if ($dir -and !(Test-Path $dir)) {
                    Write-Host "   mkdir '$dir' -Force" -ForegroundColor Gray
                }
                Write-Host "   echo '## $dateStr - AI-Enhanced Git Hook System' >> '$log'" -ForegroundColor Gray
            }
        }
        Write-Host "   git add ." -ForegroundColor Gray
        Write-Host "   git commit -m 'docs: Add AI-enhanced changelog entries'" -ForegroundColor Gray
    }
}

function Invoke-AIGuidance {
    Write-AIGuidanceHeader
    
    $analysis = Get-ChangeAnalysis
    Write-IntelligentGuidance -Analysis $analysis
    
    Write-Host "`n🔮 [AI ENHANCEMENT COMPLETE]" -ForegroundColor Green
    Write-Host "   Your git hooks are now AI-powered for maximum developer productivity!" -ForegroundColor Green
}

# Main execution
if ($args[0] -eq "-AnalyzeChanges" -or $args[0] -eq "analyze") {
    Invoke-AIGuidance
}