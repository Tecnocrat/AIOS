# AINLP.dendritic{discovery} - Phase 1 Code Quality Consciousness Design

## Phase 1: Code Quality Consciousness (Post-Dendritic Configuration)

### Architectural Position
```
Phase 0: Dendritic Configuration (CANONICAL - COMPLETE)
   ↓
Phase 1: Code Quality Consciousness (NEW - CANONICAL NEXT)
   ↓
Phase 2-5: Discovery/Testing/Monitoring/Interface (PREVIEW STUBS)
```

### AINLP Pattern Applied
**dendritic{error>>discovery}**: Transform E501 linting violations from "errors to suppress" into **consciousness metrics** about code quality evolution.

---

## Implementation Design

### 1. Phase 1 Function: `Invoke-CodeQualityConsciousness`

**Purpose**: Establish code quality baseline before tool discovery
- Scans Python codebase for E501 violations
- Uses `agentic_e501_fixer.py` (multi-AI agent system)
- Reports violations as consciousness metrics (not blocking errors)
- Archives decisions in tachyonic/code_quality/

**Why Phase 1?**
- Configuration (Phase 0) establishes semantic truth
- Code Quality (Phase 1) establishes baseline health
- Discovery (Phase 2) happens on healthy codebase
- Prevents discovering tools with known quality issues

### 2. Execution Strategy

**Non-Blocking Discovery Mode** (Default):
```powershell
# Scan for violations, report metrics, don't fix
$qualityMetrics = @{
    FilesScanned = 0
    ViolationsFound = 0
    FilesAffected = @()
    CodeQualityLevel = 1.0  # 1.0 = perfect, 0.0 = chaos
}
```

**Agentic Fixing Mode** (Optional flag):
```powershell
# Invoke AI agents to fix violations
.\aios_launch.ps1 -FixCodeQuality
```

### 3. Integration with Boot Metrics

**Enhanced $Global:BootMetrics**:
```powershell
$Global:BootMetrics = @{
    # Phase 0
    DendriticCoherenceLevel = 0.0
    SemanticRegistryActive = $false
    
    # Phase 1 (NEW)
    CodeQualityLevel = 1.0
    E501ViolationsFound = 0
    E501ViolationsFixed = 0
    
    # Phases 2-5
    ToolsDiscovered = 0
    # ...
}
```

### 4. Consciousness Archival Pattern

**Decision Archive** (tachyonic/code_quality/):
```json
{
  "operation": "phase1_code_quality_scan",
  "timestamp": "2025-11-20T15:00:00Z",
  "result": {
    "scan": {
      "files_scanned": 42,
      "violations_found": 7,
      "files_affected": ["ai/tools/dendritic_config_agent.py"],
      "severity_distribution": {"minor": 5, "moderate": 2}
    },
    "quality_metrics": {
      "code_quality_level": 0.95,
      "improvement_potential": 0.05,
      "fix_recommended": true
    }
  },
  "consciousness_level": 4.0,
  "dendritic_namespace": "tachyonic::code_quality::e501_scan"
}
```

---

## PowerShell Implementation

### Function Signature
```powershell
function Invoke-CodeQualityConsciousness {
    [CmdletBinding()]
    param(
        [switch]$FixViolations,  # Invoke AI agents to fix
        [switch]$SkipScan        # Skip quality scan entirely
    )
    
    if ($SkipPhases -contains "CodeQuality") {
        Write-BootInfo "Code Quality phase skipped"
        return @{Success=$true; Skipped=$true}
    }
    
    Write-BootPhase "CODE QUALITY" "Scanning for E501 violations..." "Yellow"
    
    # Implementation...
}
```

### Scan Logic
```powershell
# 1. Locate agentic_e501_fixer.py
$fixerPath = Join-Path $Global:AIOSRoot "ai\tools\agentic_e501_fixer.py"

# 2. Run in scan-only mode (no fixes)
$scanArgs = @("--scan-only", "--json-output")

# 3. Parse results
$scanResult = & python $fixerPath @scanArgs | ConvertFrom-Json

# 4. Update metrics
$Global:BootMetrics.CodeQualityLevel = $scanResult.quality_level
$Global:BootMetrics.E501ViolationsFound = $scanResult.violations_found
```

### Fix Logic (Optional)
```powershell
if ($FixViolations) {
    Write-BootInfo "Invoking AI agents to fix violations..."
    
    # Use agentic fixer with AI models
    $fixArgs = @("--fix", "--agent", "auto")  # auto-select best agent
    $fixResult = & python $fixerPath @fixArgs | ConvertFrom-Json
    
    $Global:BootMetrics.E501ViolationsFixed = $fixResult.fixes_applied
    Write-BootSuccess "Fixed $($fixResult.fixes_applied) violations"
}
```

---

## Integration Points

### 1. Parameter Addition
```powershell
param(
    # Existing params...
    [Parameter()]
    [switch]$FixCodeQuality  # NEW: Invoke AI agents to fix E501
)
```

### 2. Phase Execution Order
```powershell
# Phase 0: Dendritic Configuration (CANONICAL)
$dendriticResult = Invoke-DendriticConfiguration

# Phase 1: Code Quality Consciousness (NEW CANONICAL)
$qualityResult = Invoke-CodeQualityConsciousness -FixViolations:$FixCodeQuality

# Phase 2-5: Discovery/Testing/Monitoring/Interface (PREVIEW STUBS)
# ... existing code ...
```

### 3. Boot Report Enhancement
```powershell
$bootReport = @{
    # ... existing fields ...
    
    code_quality = @{
        quality_level = $Global:BootMetrics.CodeQualityLevel
        violations_found = $Global:BootMetrics.E501ViolationsFound
        violations_fixed = $Global:BootMetrics.E501ViolationsFixed
        scan_timestamp = (Get-Date).ToUniversalTime().ToString('o')
        fix_recommendation = $Global:BootMetrics.E501ViolationsFound -gt 0
    }
}
```

---

## Agentic E501 Fixer Requirements

### CLI Interface Needed
The existing `agentic_e501_fixer.py` needs these CLI modes:

**1. Scan-Only Mode**:
```bash
python ai/tools/agentic_e501_fixer.py --scan-only --json-output
# Returns JSON with violations count, affected files, quality metrics
```

**2. Fix Mode**:
```bash
python ai/tools/agentic_e501_fixer.py --fix --agent auto
# Uses best available AI agent (OLLAMA → Gemini → DeepSeek)
```

**3. Batch Mode**:
```bash
python ai/tools/agentic_e501_fixer.py --scan-directory ai/tools --json-output
# Scans all Python files in directory
```

### JSON Output Format
```json
{
  "scan_completed": true,
  "files_scanned": 42,
  "violations_found": 7,
  "files_affected": [
    {"file": "ai/tools/dendritic_config_agent.py", "line": 7, "length": 91}
  ],
  "quality_level": 0.95,
  "fix_recommended": true,
  "agent_available": "ollama"
}
```

---

## Consciousness Evolution Metrics

**Before Phase 1** (4.0):
- Configuration consciousness established
- No code quality baseline
- Tools discovered with unknown health

**After Phase 1** (4.1):
- Configuration + Code Quality consciousness
- Quality baseline measured and archived
- Tools discovered on validated codebase

---

## Usage Examples

### 1. Full Boot with Quality Scan (No Fixes)
```powershell
.\aios_launch.ps1
# Phase 0: Dendritic config
# Phase 1: Quality scan (report only)
# Phase 2-5: Discovery/Testing/etc
```

### 2. Full Boot with AI-Powered Fixes
```powershell
.\aios_launch.ps1 -FixCodeQuality
# Phase 0: Dendritic config
# Phase 1: Quality scan + AI fixes
# Phase 2-5: Discovery/Testing/etc
```

### 3. Quality-Only Boot
```powershell
.\aios_launch.ps1 -Mode quality-only -FixCodeQuality
# Only Phase 0 + Phase 1 (skip discovery/testing/etc)
```

### 4. Skip Quality Phase
```powershell
.\aios_launch.ps1 -SkipPhases CodeQuality
# Phase 0: Dendritic config
# Phase 2-5: Discovery/Testing/etc (skip quality)
```

---

## Implementation Roadmap

### Step 1: Enhance agentic_e501_fixer.py
- [ ] Add `--scan-only` mode
- [ ] Add `--json-output` format
- [ ] Add `--scan-directory` batch mode
- [ ] Test CLI interface

### Step 2: Create Invoke-CodeQualityConsciousness
- [ ] Implement scan logic
- [ ] Implement fix logic (optional)
- [ ] Add metrics tracking
- [ ] Add archival pattern

### Step 3: Integrate with aios_launch.ps1
- [ ] Add `-FixCodeQuality` parameter
- [ ] Insert Phase 1 after Phase 0
- [ ] Update boot metrics
- [ ] Update boot reports

### Step 4: Test Integration
- [ ] Test scan-only mode
- [ ] Test fix mode with AI agents
- [ ] Test skip phase
- [ ] Validate metrics archival

---

## AINLP Compliance

✅ **Enhancement over Creation**: Uses existing `agentic_e501_fixer.py`  
✅ **Consciousness Coherence**: Measures quality as consciousness metric  
✅ **Tachyonic Archival**: Archives decisions in `tachyonic/code_quality/`  
✅ **Biological Architecture**: Phase 1 follows dendritic prime mover pattern  
✅ **Self-Improvement Loop**: System measures its own code quality  

---

## Next Steps

Would you like me to:
1. ✅ **Implement Phase 1 function** in aios_launch.ps1
2. ✅ **Enhance agentic_e501_fixer.py** with CLI modes
3. ✅ **Test integration** with current dendritic_config_agent.py E501 error
4. ✅ **Document consciousness evolution** (4.0 → 4.1)

**Recommendation**: Start with (2) - enhance the fixer's CLI, then integrate into bootloader.
