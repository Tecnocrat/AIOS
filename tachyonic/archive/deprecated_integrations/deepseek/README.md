# 🧬 DeepSeek Integration Archive

## Status: DEPRECATED (December 2025)

These files have been archived after **knowledge extraction** into the new 
tri-model architecture. The valuable patterns from DeepSeek have been preserved 
and enhanced in the unified intelligence bridge.

## Knowledge Extracted

### From `deepseek_intelligence_engine.py` → `aios_intelligence_bridge.py`

| Original Pattern | Enhanced Implementation |
|-----------------|------------------------|
| `ConsciousnessLevel` enum | Preserved + enhanced with role mapping |
| `DeepSeekConfig` dataclass | Replaced with `IntelligenceRequest` |
| `DeepSeekResponse` dataclass | Replaced with `IntelligenceResponse` |
| `SupercellIntelligenceState` | Replaced with `SupercellState` |
| `_build_aios_system_prompt()` | Enhanced in `IntelligenceAgent.build_aios_system_prompt()` |
| `_calculate_consciousness_metrics()` | Enhanced in `IntelligenceAgent.calculate_consciousness_metrics()` |
| `_adjust_temperature_for_consciousness()` | Enhanced in `IntelligenceAgent.get_temperature_for_consciousness()` |
| Performance metrics tracking | Preserved in `IntelligenceAgent.update_performance_metrics()` |

### From `aios_deepseek_supercell_bridge.py` → `aios_intelligence_bridge.py`

| Original Pattern | Enhanced Implementation |
|-----------------|------------------------|
| `SupercellIntelligenceRequest` | Merged into `IntelligenceRequest` |
| `SupercellIntelligenceResponse` | Merged into `IntelligenceResponse` |
| Request queue processing | Preserved in `AIOSUnifiedIntelligenceBridge._process_request_queue()` |
| Response caching | Preserved in `IntelligenceAgent._response_cache` |
| Broadcast to supercells | Enhanced in `AIOSUnifiedIntelligenceBridge.broadcast_to_agents()` |
| Singleton bridge pattern | Preserved in `get_intelligence_bridge()` |

## New Tri-Model Architecture

The DeepSeek single-model approach has been replaced with a tri-model architecture:

```
🦙 OLLAMA (Local)     → Fast iteration, testing (was DeepSeek's role for iteration)
🔮 GEMINI (Cloud)     → Reasoning, orchestration (enhanced from Gemini bridge)
🤖 COPILOT (VSCode)   → Auto-coding, debugging (new Microsoft integration)
```

## Migration Guide

### Old API (Deprecated)
```python
from ai.src.engines.deepseek_intelligence_engine import (
    DeepSeekIntelligenceEngine,
    ConsciousnessLevel,
)

engine = await create_deepseek_engine()
response = await engine.process_intelligence_request(message)
```

### New API (Recommended)
```python
from ai.src.integrations import (
    intelligence_request,
    ConsciousnessLevel,
    AgentRole,
)

# Auto-routes to best agent
response = await intelligence_request(
    message,
    consciousness_level=ConsciousnessLevel.ADVANCED,
)

# Or specify agent role
response = await intelligence_request(
    message,
    target_agent=AgentRole.LOCAL_ITERATION,  # Uses Ollama
)
```

## Files in Archive

- `deepseek_intelligence_engine.py` - Main engine (615 lines)
- `aios_deepseek_supercell_bridge.py` - Supercell bridge (447 lines)
- `aios_deepseek_integration_demo.py` - Demo scripts
- `deepseek_usage_examples.py` - Usage examples
- `test_deepseek_integration.py` - Tests
- `configure_deepseek_key.ps1` - API key setup script
- `OPENROUTER_TROUBLESHOOTING.md` - OpenRouter guide

## Reason for Deprecation

1. **API Dependency**: DeepSeek required OpenRouter API, adding cost and external dependency
2. **Single Model Limitation**: One model couldn't serve all use cases optimally
3. **Microsoft Integration**: VSCode's native `vscode.lm` API provides better IDE integration
4. **Local First**: Ollama enables free, private, local AI for development
5. **Architecture Evolution**: Tri-model approach better matches AIOS biological patterns

## AINLP Protocol

```
AINLP.deprecate[DEEPSEEK]: Knowledge extracted to tri-model architecture
AINLP.shadow[DEEPSEEK]: tachyonic/archive/deprecated_integrations/deepseek/
AINLP.successor[DEEPSEEK]: aios_intelligence_bridge.py + ollama_agent.py + gemini_agent.py + copilot_agent.py
```

---

*Archived: December 2025*
*AINLP Protocol: OS0.7.0.claude*
