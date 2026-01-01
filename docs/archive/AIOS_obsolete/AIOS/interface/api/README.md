# AIOS API Documentation

## DeepSeek Intelligence API

### Basic Usage
```python
from ai.src.integrations.aios_deepseek_supercell_bridge import aios_intelligence_request

# Simple intelligence request
response = await aios_intelligence_request(
    message="Your question here",
    source_supercell="your_component_name"
)

print(response.text)
print(f"Confidence: {response.confidence}")
```

### Advanced Usage
```python
from ai.src.integrations.aios_deepseek_supercell_bridge import (
    aios_intelligence_request,
    ConsciousnessLevel
)

# Advanced request with consciousness level and context
response = await aios_intelligence_request(
    message="Analyze this code and suggest improvements...",
    source_supercell="code_analyzer",
    consciousness_level=ConsciousnessLevel.TRANSCENDENT,
    context={
        "analysis_type": "code_review",
        "language": "python",
        "focus": "performance"
    }
)
```

## Component Interfaces

### Supercell Communication
All AIOS components can access AI intelligence through the unified bridge interface.

### Available Functions
- `aios_intelligence_request()` - Single AI request
- `aios_broadcast_intelligence()` - Broadcast to all supercells
- `get_aios_deepseek_bridge()` - Access bridge instance

## Response Format
```python
@dataclass
class DeepSeekResponse:
    text: str
    confidence: float
    processing_time: float
    model: str
    supercell_coherence: float
```

For complete API documentation, see:
- [DeepSeek Integration Guide](../AIOS/DEEPSEEK_INTEGRATION.md)
- [Integration Examples](../../ai/src/demos/)