# Deprecated Integrations Archive

**Archived**: 2025-12-06  
**Reason**: Consolidating to canonical two-tier integration (Ollama local + Google AI Studio cloud)

## Files Archived

| File | Original Location | Reason |
|------|-------------------|--------|
| `openrouter_tier3_validator.py` | ai/tools/ | Replaced by aios_gemini_bridge.py |
| `unified_openrouter_handler.py` | ai/tools/ | OpenRouter too expensive, using Gemini |
| `test_openrouter_models.py` | ai/tools/ | Test files for deprecated integration |
| `test_openrouter_key.py` | ai/tools/ | Test files for deprecated integration |
| `test_openrouter_key.py` | ai/ | Duplicate test file |

## New Canonical Architecture

```
AIOS Triangular Agent System (Canonical)
├── GEMMA (1B) - Scout - aios_gemma_bridge.py
│   └── Pattern detection, signal routing, pre-filtering
├── MISTRAL (7B) - Worker - aios_mistral_bridge.py
│   └── Code generation, E501 fixing, mutations
└── GEMINI (Cloud) - Oracle - aios_gemini_bridge.py
    └── Validation, architecture analysis, final arbiter

Coordinator: triangular_agent_coordinator.py
```

## Cost Comparison

| Integration | Cost | Status |
|-------------|------|--------|
| Ollama (Gemma + Mistral) | FREE | ✅ Active |
| Google AI Studio (Gemini) | ~$0.01/1M tokens | ✅ Active |
| OpenRouter (DeepSeek) | ~$0.14/1M tokens | ❌ Archived |
| GitHub Models | Rate-limited | ❌ Not used |

## Restoration

If needed, these files can be restored:
```powershell
Move-Item -Path "tachyonic/archive/deprecated_integrations/*.py" -Destination "ai/tools/"
```

---
*AINLP.tachyonic[ARCHIVE] - Deprecated integrations preserved for future reference*
