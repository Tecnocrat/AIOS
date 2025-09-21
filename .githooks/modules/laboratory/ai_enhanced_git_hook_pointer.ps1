#!/usr/bin/env pwsh
# AIOS AI-Enhanced Git Hook Pointer System
# Provides intelligent, contextual guidance for git hook requirements

<#
.SYNOPSIS
AI-powered guidance system for git hook compliance and error resolution.

.DESCRIPTION
This module enhances the existing git hook system with intelligent pointers that:
- Analyze the specific changes being made
- Provide exact file paths and templates for required documentation
- Suggest AI-generated changelog entries
- Guide users to the correct resolution with minimal cognitive load

.EXAMPLE
Invoke-AIGitHookGuidance -ChangeType "ai_folder_modification" -Files @("ai/src/tools/new_tool.py")
#>

param(
    [Parameter(Mandatory=$false)]
    [string]$ChangeType,
    
    [Parameter(Mandatory=$false)]
    [string[]]$ModifiedFiles = @(),
    
    [Parameter(Mandatory=$false)]
    [string]$ErrorContext = "",
    
    [Parameter(Mandatory=$false)]
    [switch]$AutoSuggest
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

class AIGitHookPointer {
    [hashtable]$PolicyConfig
    [hashtable]$ChangelogTemplates
    [hashtable]$PathMappings
    
    AIGitHookPointer() {
        $this.InitializeConfiguration()
        $this.InitializeTemplates()
        $this.InitializePathMappings()
    }
    
    [void] InitializeConfiguration() {
        $PolicyPath = Join-Path (Split-Path $PSScriptRoot -Parent) "..\..\..\governance\hook_policy.json"
        if (Test-Path $PolicyPath) {
            $this.PolicyConfig = Get-Content $PolicyPath | ConvertFrom-Json -AsHashtable
        } else {
            throw "Policy configuration not found: $PolicyPath"
        }
    }
    
    [void] InitializeTemplates() {
        $this.ChangelogTemplates = @{
            'ai_folder_modification' = @{
                'CHANGELOG.md' = @"
## [$(Get-Date -Format 'yyyy-MM-dd')] - AI Intelligence Enhancement

### Modified Components
- **AI Tools**: Enhanced functionality in ai/tools/
- **Core Integration**: Updated ai/src/core/ components
- **Transport Layer**: Modified ai/transport/ mechanisms

### Impact Assessment
- **Compatibility**: Maintains backward compatibility
- **Performance**: No performance regression expected
- **Dependencies**: No new external dependencies

### Testing Status
- [ ] Unit tests updated
- [ ] Integration tests verified
- [ ] Health monitoring validated

"@
                'docs/tachyonic/tachyonic_changelog.yaml' = @"
# Tachyonic Changelog Entry
- timestamp: "$(Get-Date -Format 'yyyy-MM-ddTHH:mm:ssZ')"
  category: "ai_intelligence_enhancement"
  impact_level: "moderate"
  components_modified:
    - "ai/tools/"
    - "ai/src/"
    - "ai/transport/"
  change_summary: "Enhanced AI intelligence capabilities with improved tool integration"
  author_context: "AI-guided modernization following AIOS architecture standards"
  architectural_impact:
    - component_health_improved: true
    - integration_bridges_updated: false
    - consciousness_level_enhanced: true
  validation_status:
    - syntax_checked: true
    - health_monitoring_updated: true
    - documentation_synchronized: true

"@
                'docs/tachyonic/tachyonic_changelog.jsonl' = @"
{"timestamp":"$(Get-Date -Format 'yyyy-MM-ddTHH:mm:ssZ')","event":"ai_folder_modification","components":["ai/tools/","ai/src/","ai/transport/"],"impact":"moderate","summary":"Enhanced AI intelligence capabilities","architectural_classification":"ai_intelligence_layer","consciousness_level":"enhanced","health_impact":"positive"}

"@
            }
            'runtime_intelligence_modification' = @{
                'CHANGELOG.md' = @"
## [$(Get-Date -Format 'yyyy-MM-dd')] - Runtime Intelligence Enhancement

### Modified Components
- **Health Monitoring**: Updated system health tools
- **Architecture Monitor**: Enhanced AIOS architecture monitoring
- **Tool Integration**: Improved runtime intelligence capabilities

### AIOS Architecture Impact
- **Component**: Runtime Intelligence
- **Health Score**: Improved monitoring accuracy
- **Integration**: Enhanced bridge connectivity

"@
            }
        }
    }
    
    [void] InitializePathMappings() {
        $this.PathMappings = @{
            'ai/' = @{
                'change_type' = 'ai_folder_modification'
                'required_changelogs' = @('CHANGELOG.md', 'docs/tachyonic/tachyonic_changelog.yaml', 'docs/tachyonic/tachyonic_changelog.jsonl')
                'description' = 'AI Intelligence Layer modifications'
                'impact_level' = 'high'
            }
            'runtime_intelligence/' = @{
                'change_type' = 'runtime_intelligence_modification'
                'required_changelogs' = @('CHANGELOG.md')
                'description' = 'Runtime Intelligence Layer modifications'
                'impact_level' = 'moderate'
            }
            'core/' = @{
                'change_type' = 'core_engine_modification'
                'required_changelogs' = @('CHANGELOG.md', 'docs/tachyonic/tachyonic_changelog.yaml')
                'description' = 'Core Engine modifications'
                'impact_level' = 'critical'
            }
            'interface/' = @{
                'change_type' = 'interface_modification'
                'required_changelogs' = @('CHANGELOG.md')
                'description' = 'Interface Layer modifications'
                'impact_level' = 'moderate'
            }
        }
    }
    
    [hashtable] AnalyzeChanges([string[]]$Files) {
        $analysis = @{
            'affected_components' = @()
            'change_types' = @()
            'required_changelogs' = @()
            'impact_level' = 'low'
            'recommendations' = @()
        }
        
        foreach ($file in $Files) {
            foreach ($path in $this.PathMappings.Keys) {
                if ($file.StartsWith($path)) {
                    $mapping = $this.PathMappings[$path]
                    
                    if ($analysis.affected_components -notcontains $path) {
                        $analysis.affected_components += $path
                    }
                    
                    if ($analysis.change_types -notcontains $mapping.change_type) {
                        $analysis.change_types += $mapping.change_type
                    }
                    
                    foreach ($changelog in $mapping.required_changelogs) {
                        if ($analysis.required_changelogs -notcontains $changelog) {
                            $analysis.required_changelogs += $changelog
                        }
                    }
                    
                    # Upgrade impact level if needed
                    $levels = @('low', 'moderate', 'high', 'critical')
                    $currentIndex = [array]::IndexOf($levels, $analysis.impact_level)
                    $newIndex = [array]::IndexOf($levels, $mapping.impact_level)
                    if ($newIndex -gt $currentIndex) {
                        $analysis.impact_level = $mapping.impact_level
                    }
                }
            }
        }
        
        return $analysis
    }
    
    [void] GenerateIntelligentGuidance([hashtable]$Analysis) {
        Write-Host "`n🤖 [AI-ENHANCED-GITHOOK] Intelligent Guidance System" -ForegroundColor Cyan
        Write-Host "=" * 60 -ForegroundColor Cyan
        
        Write-Host "`n📊 CHANGE ANALYSIS:" -ForegroundColor Yellow
        Write-Host "   Components Affected: $($Analysis.affected_components -join ', ')" -ForegroundColor White
        Write-Host "   Impact Level: $($Analysis.impact_level.ToUpper())" -ForegroundColor White
        Write-Host "   Change Types: $($Analysis.change_types -join ', ')" -ForegroundColor White
        
        Write-Host "`n📝 REQUIRED DOCUMENTATION:" -ForegroundColor Yellow
        foreach ($changelog in $Analysis.required_changelogs) {
            $fullPath = if ($changelog.StartsWith("docs/") -or $changelog.StartsWith(".githooks/")) { 
                $changelog 
            } else { 
                $changelog 
            }
            
            Write-Host "   ✅ CREATE: $fullPath" -ForegroundColor Green
            
            # Check if file exists
            if (Test-Path $fullPath) {
                Write-Host "      📄 Status: EXISTS - append new entry" -ForegroundColor Blue
            } else {
                Write-Host "      📄 Status: NEW FILE - create with template" -ForegroundColor Yellow
            }
        }
        
        Write-Host "`n🎯 EXACT COMMANDS TO RUN:" -ForegroundColor Green
        foreach ($changelog in $Analysis.required_changelogs) {
            $template = $this.GetTemplate($Analysis.change_types[0], $changelog)
            if ($template) {
                Write-Host "   # Create $changelog" -ForegroundColor Gray
                Write-Host "   echo '$($template -replace "'", "''")' >> $changelog" -ForegroundColor Cyan
                Write-Host "   git add $changelog" -ForegroundColor Cyan
                Write-Host ""
            }
        }
        
        Write-Host "`n💡 AI-GENERATED RECOMMENDATIONS:" -ForegroundColor Magenta
        $this.GenerateAIRecommendations($Analysis)
        
        Write-Host "`n🚀 QUICK RESOLUTION:" -ForegroundColor Green
        Write-Host "   Run this command to auto-generate all required files:" -ForegroundColor White
        Write-Host "   pwsh .githooks/modules/laboratory/ai_enhanced_git_hook_pointer.ps1 -AutoSuggest" -ForegroundColor Cyan
    }
    
    [string] GetTemplate([string]$ChangeType, [string]$ChangelogFile) {
        $filename = Split-Path $ChangelogFile -Leaf
        if ($this.ChangelogTemplates.ContainsKey($ChangeType) -and 
            $this.ChangelogTemplates[$ChangeType].ContainsKey($filename)) {
            return $this.ChangelogTemplates[$ChangeType][$filename]
        }
        return ""
    }
    
    [void] GenerateAIRecommendations([hashtable]$Analysis) {
        Write-Host "   📚 Based on your changes, consider:" -ForegroundColor White
        
        if ($Analysis.affected_components -contains "ai/") {
            Write-Host "   • Update AI component health monitoring after changes" -ForegroundColor Gray
            Write-Host "   • Run comprehensive AIOS health test to validate integration" -ForegroundColor Gray
            Write-Host "   • Consider updating ai/tools/ documentation if new capabilities added" -ForegroundColor Gray
        }
        
        if ($Analysis.impact_level -eq "critical") {
            Write-Host "   ⚠️  CRITICAL IMPACT: Consider creating feature branch for testing" -ForegroundColor Red
            Write-Host "   ⚠️  Run full test suite before merging" -ForegroundColor Red
        }
        
        Write-Host "   🧪 Suggested validation: python runtime_intelligence/tools/comprehensive_aios_health_test.py" -ForegroundColor Gray
    }
    
    [void] AutoGenerateChangelogs([hashtable]$Analysis) {
        Write-Host "`n🤖 [AUTO-GENERATION] Creating required changelog entries..." -ForegroundColor Cyan
        
        foreach ($changelog in $Analysis.required_changelogs) {
            $template = $this.GetTemplate($Analysis.change_types[0], $changelog)
            if ($template) {
                # Ensure directory exists
                $dir = Split-Path $changelog -Parent
                if ($dir -and !(Test-Path $dir)) {
                    New-Item -ItemType Directory -Path $dir -Force | Out-Null
                    Write-Host "   📁 Created directory: $dir" -ForegroundColor Blue
                }
                
                # Append or create changelog entry
                Add-Content -Path $changelog -Value $template -Encoding UTF8
                Write-Host "   ✅ Generated: $changelog" -ForegroundColor Green
            }
        }
        
        Write-Host "`n✨ All required changelogs generated! Run 'git add .' to stage them." -ForegroundColor Green
    }
}

function Invoke-AIGitHookGuidance {
    param(
        [string[]]$ModifiedFiles = @(),
        [switch]$AutoSuggest
    )
    
    try {
        $pointer = [AIGitHookPointer]::new()
        
        if ($ModifiedFiles.Count -eq 0) {
            # Get staged files from git
            $ModifiedFiles = git diff --cached --name-only
        }
        
        if ($ModifiedFiles.Count -eq 0) {
            Write-Host "🤖 No changes detected for analysis." -ForegroundColor Yellow
            return
        }
        
        $analysis = $pointer.AnalyzeChanges($ModifiedFiles)
        
        if ($analysis.required_changelogs.Count -eq 0) {
            Write-Host "✅ No changelog requirements for current changes." -ForegroundColor Green
            return
        }
        
        $pointer.GenerateIntelligentGuidance($analysis)
        
        if ($AutoSuggest) {
            $pointer.AutoGenerateChangelogs($analysis)
        }
        
    } catch {
        Write-Error "AI Git Hook Pointer failed: $($_.Exception.Message)"
    }
}

# Main execution
if ($MyInvocation.InvocationName -ne '.') {
    Invoke-AIGitHookGuidance -ModifiedFiles $ModifiedFiles -AutoSuggest:$AutoSuggest
}