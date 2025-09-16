# AI-Guided Refactoring Engine
# AINLP Module: Intelligent code organization and enhancement suggestions
# Purpose: Stimulate AI agent to make real-time refactoring decisions

param(
    [string]$ScanPath = ".",
    [switch]$InteractiveMode = $true
)

function Invoke-AIGuidedRefactoring {
    param([string]$ProjectRoot)
    
    Write-Host "`n🧠 [AIOS-AI-REFACTORING-ENGINE] Analyzing codebase for enhancement opportunities..." -ForegroundColor Cyan
    
    # Detect root hygiene violations and improvement opportunities
    $RootFiles = Get-ChildItem -Path $ProjectRoot -File | Where-Object { 
        $_.Name -match '\.(md|json|log|txt)$' -and 
        $_.Name -notmatch '^(README|LICENSE|\.gitignore|CHANGELOG)' 
    }
    
    $RefactoringOpportunities = @()
    
    foreach ($File in $RootFiles) {
        $Enhancement = Analyze-FileForEnhancement -FilePath $File.FullName
        if ($Enhancement) {
            $RefactoringOpportunities += $Enhancement
        }
    }
    
    if ($RefactoringOpportunities.Count -gt 0) {
        Write-Host "`n🔍 [AI-ANALYSIS] Found $($RefactoringOpportunities.Count) refactoring opportunities" -ForegroundColor Yellow
        
        # Generate natural language AI stimulation prompt
        $AIPrompt = Generate-AIStimulationPrompt -Opportunities $RefactoringOpportunities
        
        # Save AI stimulation context for VS Code AI agent
        $AIContextPath = ".vscode\ai_refactoring_context.md"
        Set-Content -Path $AIContextPath -Value $AIPrompt -Encoding UTF8
        
        Write-Host "`n💡 [AI-STIMULATION] Generated intelligent refactoring context at: $AIContextPath" -ForegroundColor Green
        Write-Host "🤖 [INTEGRATION] VS Code AI agent can now access real-time enhancement suggestions" -ForegroundColor Magenta
        
        if ($InteractiveMode) {
            Write-Host "`n📋 [PREVIEW] AI Enhancement Suggestions:" -ForegroundColor Cyan
            Write-Host $AIPrompt -ForegroundColor White
            
            Write-Host "`n🎯 [ACTION-REQUIRED] Open VS Code and let the AI agent decide implementation approach" -ForegroundColor Yellow
            Write-Host "💭 [HINT] The AI will analyze these suggestions and choose optimal refactoring strategy" -ForegroundColor DarkCyan
        }
        
        return $true
    } else {
        Write-Host "`n✅ [CLEAN] No refactoring opportunities detected - codebase is well organized" -ForegroundColor Green
        return $false
    }
}

function Analyze-FileForEnhancement {
    param([string]$FilePath)
    
    $FileName = Split-Path $FilePath -Leaf
    $FileContent = Get-Content $FilePath -Raw -ErrorAction SilentlyContinue
    
    $Analysis = @{
        File = $FileName
        Path = $FilePath
        Issues = @()
        Suggestions = @()
        Priority = "Medium"
    }
    
    # Analyze file type and suggest proper location
    switch -Regex ($FileName) {
        '.*_ANALYSIS\.md$|.*_REPORT\.md$|.*_SUMMARY\.md$' {
            $Analysis.Issues += "Documentation file in root directory"
            $Analysis.Suggestions += "Move to docs/reports/ or docs/analysis/"
            $Analysis.Priority = "High"
        }
        '.*\.json$' {
            if ($FileContent -match '"optimization"|"report"|"session"') {
                $Analysis.Issues += "Report/session data in root"
                $Analysis.Suggestions += "Move to docs/reports/ or runtime_intelligence/logs/"
            }
        }
        '.*\.log$' {
            $Analysis.Issues += "Log file in root directory"
            $Analysis.Suggestions += "Move to appropriate logs/ subdirectory"
            $Analysis.Priority = "High"
        }
        'CHANGELOG.*|.*EVOLUTION.*|.*SUCCESS.*' {
            $Analysis.Issues += "Change documentation in root"
            $Analysis.Suggestions += "Organize in docs/changelog/ or docs/evolution/"
        }
    }
    
    # Analyze content for enhancement opportunities
    if ($FileContent) {
        if ($FileContent -match 'TODO|FIXME|HACK') {
            $Analysis.Issues += "Contains technical debt markers"
            $Analysis.Suggestions += "Review and resolve technical debt before commit"
        }
        
        if ($FileContent -match '😀|😎|🤖|🚀|⚡|💡' -and $FileName -notmatch 'README') {
            $Analysis.Issues += "Contains emoticons (violates professional standards)"
            $Analysis.Suggestions += "Replace emoticons with professional text equivalents"
            $Analysis.Priority = "Critical"
        }
    }
    
    if ($Analysis.Issues.Count -gt 0) {
        return $Analysis
    }
    
    return $null
}

function Generate-AIStimulationPrompt {
    param([array]$Opportunities)
    
    $Prompt = @"
# 🧠 AIOS AI Agent Refactoring Context
**Generated**: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
**Purpose**: Intelligent codebase enhancement and organization

## 🎯 Enhancement Opportunities Detected

The AIOS pre-commit system has analyzed the codebase and identified specific improvement opportunities. As an AI agent, you should evaluate these suggestions and implement the most appropriate solutions using your intelligence and understanding of the AIOS architecture.

### 📊 Analysis Summary
- **Total Issues Found**: $($Opportunities.Count)
- **Critical Priority**: $($Opportunities | Where-Object { $_.Priority -eq "Critical" } | Measure-Object | Select-Object -ExpandProperty Count)
- **High Priority**: $($Opportunities | Where-Object { $_.Priority -eq "High" } | Measure-Object | Select-Object -ExpandProperty Count)

### 🔍 Detailed Enhancement Opportunities

"@

    foreach ($Opportunity in $Opportunities) {
        $Prompt += @"

#### 📁 File: ``$($Opportunity.File)``
**Location**: ``$($Opportunity.Path)``
**Priority**: **$($Opportunity.Priority)**

**Issues Identified**:
$($Opportunity.Issues | ForEach-Object { "- $_" } | Out-String)

**AI Enhancement Suggestions**:
$($Opportunity.Suggestions | ForEach-Object { "- $_" } | Out-String)

**AI Decision Points**:
- Should this file be moved, refactored, or enhanced in place?
- What is the optimal directory structure for this content?
- Are there any AINLP architectural patterns that should be applied?
- How does this change align with the AIOS consciousness evolution?

---
"@
    }
    
    $Prompt += @"

## 🤖 AI Agent Instructions

### Decision Framework
1. **Analyze Each Opportunity**: Use your understanding of AIOS architecture to evaluate each suggestion
2. **Consider AINLP Patterns**: Apply holographic and biological metaphor principles
3. **Prioritize Impact**: Focus on changes that improve maintainability and clarity
4. **Maintain Coherence**: Ensure changes align with existing AIOS consciousness structure

### Implementation Approach
- **Use VS Code Tools**: Leverage file operations, directory creation, and content modification tools
- **Apply Intelligence**: Don't just follow suggestions blindly - adapt and improve them
- **Consider Dependencies**: Understand how file moves might affect imports and references
- **Document Changes**: Update any relevant documentation or index files

### Suggested Workflow
1. Create necessary directory structures if they don't exist
2. Move files to appropriate locations with proper path updates
3. Fix any emoticon violations with professional alternatives
4. Update any references or imports that might be affected
5. Consider if moved files need content enhancements or restructuring

## 🎯 Expected Outcome
The AI agent should process these suggestions and create a well-organized, professional codebase that follows AIOS architectural principles while maintaining all functionality and improving long-term maintainability.

**Remember**: These are suggestions, not commands. Use your AI intelligence to make the best decisions for the AIOS project.
"@

    return $Prompt
}

# Execute the AI-guided refactoring analysis
if ($MyInvocation.InvocationName -ne '.') {
    $RefactoringNeeded = Invoke-AIGuidedRefactoring -ProjectRoot (Get-Location).Path
    
    if ($RefactoringNeeded) {
        Write-Host "`n🔄 [INTEGRATION] AI context prepared for intelligent refactoring decisions" -ForegroundColor Cyan
        exit 1  # Indicate that manual AI intervention is recommended
    } else {
        Write-Host "`n✅ [SUCCESS] Codebase organization meets AIOS standards" -ForegroundColor Green
        exit 0
    }
}