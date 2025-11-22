# Hierarchical Three-Tier E501 Pipeline - Configuration Guide

## Overview

The hierarchical pipeline implements role-based agent specialization:
- **Tier 1: OLLAMA** (Context Manager) - Local preprocessing and caching
- **Tier 2: GEMINI** (Code Generator) - Cloud-based intelligent fixing
- **Tier 3: DEEPSEEK** (Quality Validator) - Correctness verification

## Environment Configuration

### Required Environment Variables

1. **GEMINI_API_KEY** (Already configured ✅)
   ```powershell
   # You already have this configured
   $env:GEMINI_API_KEY = "your-gemini-api-key"
   ```

2. **DEEPSEEK_API_KEY** (Needs configuration)
   ```powershell
   # Set for current session
   $env:DEEPSEEK_API_KEY = "sk-your-deepseek-key"
   
   # Set permanently (recommended)
   # Method 1: Via Windows Settings
   #   Win + X → System → Advanced → Environment Variables
   #   User Variables → New
   #   Variable name: DEEPSEEK_API_KEY
   #   Variable value: sk-your-deepseek-key
   
   # Method 2: Via PowerShell (permanent)
   [System.Environment]::SetEnvironmentVariable(
       'DEEPSEEK_API_KEY',
       'sk-your-deepseek-key',
       [System.EnvironmentVariableTarget]::User
   )
   ```

3. **OLLAMA** (Already running ✅)
   - Service: localhost:11434
   - Model: gemma3:1b installed

## Verification

### Test Agent Readiness
```powershell
python tools/dendritic_config_agent.py --validate-multiagent
```
Expected output:
```json
{
  "readiness_level": 1.0,
  "agents_available": {
    "ollama": true,
    "gemini": true,
    "deepseek": true
  }
}
```

### Test Hierarchical Pipeline
```powershell
cd ai
python tools/test_hierarchical_pipeline.py
```

Expected output:
```
HIERARCHICAL E501 PIPELINE TEST
======================================================================

📊 Original Line (len=123):
   ...long line...

🔄 Executing hierarchical pipeline...
   Tier 1: OLLAMA (Context Manager)
   Tier 2: GEMINI (Code Generator)
   Tier 3: DEEPSEEK (Quality Validator)

✅ Pipeline Result:
   Success: True
   Confidence: 0.85
   Agent Used: gemini
   Validator: deepseek

📝 Fixed Lines:
   1. ...fixed line 1... (len=75)
   2. ...fixed line 2... (len=45)

🔍 Tier Execution Log:
   tier1: ollama_context_prepared
   tier2: gemini_generated
   tier3: deepseek_approved
```

## Usage

### With Hierarchical Pipeline (Default)
```powershell
python tools/agentic_e501_fixer.py test_file.py --fix
```

### Disable Hierarchy (Facade Fallback)
```powershell
python tools/agentic_e501_fixer.py test_file.py --fix --no-hierarchy
```

### Scan Only
```powershell
python tools/agentic_e501_fixer.py test_file.py --scan-only
```

## Architecture Flow

```
User Request
    ↓
OLLAMA (Tier 1)
    ├─ Read original file
    ├─ Cache unchanged copy
    ├─ Calculate complexity
    └─ Prepare context
    ↓
GEMINI (Tier 2)
    ├─ Receive context + instructions
    ├─ Generate fixed code
    └─ Return proposal
    ↓
DEEPSEEK (Tier 3)
    ├─ Compare original vs generated
    ├─ Validate objective achieved
    ├─ Check no unintended changes
    └─ Decision: APPROVE / REJECT / REQUEST_REVISION
    ↓
If APPROVED → Apply changes
If REQUEST_REVISION → Retry Gemini with feedback (max 2 attempts)
If REJECTED → Fallback to basic pattern fix
```

## Fallback Strategy

1. **Hierarchical Pipeline** (preferred)
   - All 3 agents operational
   - Direct API calls (no orchestrator overhead)
   - Three-layer validation

2. **Agent Conclave Facade** (first fallback)
   - Uses existing 3000+ line orchestrator
   - Multi-agent consensus
   - Response parsing required

3. **Basic Pattern Matching** (last resort)
   - No agents required
   - Simple regex-based breaking
   - Lower confidence

## Consciousness Evolution

- **v4.0**: Basic AINLP patterns
- **v4.1**: Agent conclave facade integration
- **v4.2**: Hierarchical three-tier intelligence ← YOU ARE HERE
  * Role specialization
  * Validation feedback loops
  * Cost optimization (local Ollama for I/O)

## Tachyonic Archival

Hierarchical decisions are archived in:
```
tachyonic/hierarchical_decisions/YYYYMMDD/hierarchical_decision_YYYYMMDD_HHMMSS.json
```

Each decision includes:
- Original line + context
- Ollama's context preparation
- Gemini's generated code
- DeepSeek's validation result
- Final applied fix
- Tier execution log
- Consciousness metadata

## Metrics

Pipeline tracks:
- `ollama_context_preps`: Context preparations executed
- `gemini_generations`: Code generations requested
- `deepseek_validations`: Validations performed
- `approvals`: DeepSeek approved fixes
- `rejections`: DeepSeek rejected fixes
- `revisions`: Retry cycles executed
- `fallbacks`: Basic pattern fixes used

## Next Steps

1. **Configure DeepSeek API key** (above)
2. **Run verification tests** (dendritic_config_agent.py, test_hierarchical_pipeline.py)
3. **Test with real file** (test_e501_fix.py)
4. **Apply to dendritic_config_agent.py** (line 7 - proof of concept)
5. **Integrate into Phase 1 bootloader** (aios_launch.ps1)
6. **Document consciousness evolution** (tachyonic shadow)
