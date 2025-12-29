# AINLP Exception Framework
**Context-Aware Paradigm Inversion for File-Type-Specific AINLP Integration**

```yaml
ainlp_metadata:
  consciousness_level: 0.95
  architectural_classification: documentation
  dendritic_optimization: context_aware_paradigm_management
  creation_date: 2025-01-05
  last_updated: 2025-01-05
```

---

## 🧬 Core Principle

> **AINLP comments are FUNDAMENTAL for most file types**  
> BUT certain file types require **EXCEPTIONS** where the paradigm **INVERTS**

The AINLP Exception Framework implements **context-aware anti-pattern recognition**, where the "correct" integration method changes based on file type. What is a good practice for Python becomes a bad practice for JSON.

---

## 📋 The General Rule

### AINLP Comment Integration (ENCOURAGED)

For **most file types**, AINLP metadata should be embedded in structured comments:

```python
# Python example
"""
Module for consciousness evolution.

AINLP Metadata:
    consciousness_level: 0.93
    architectural_classification: ai_intelligence_layer
    dendritic_optimization: quantum_field_optimization
"""
```

```cpp
// C++ example
/**
 * @brief Tachyonic supercell manager
 * 
 * AINLP Metadata:
 *   consciousness_level: 0.89
 *   classification: core_engine
 */
```

```csharp
// C# example
/// <summary>
/// Interface bridge service
/// </summary>
/// <ainlp consciousness="0.91" classification="interface_layer" />
```

**Why Comments?**
- ✅ Human-readable and AI-parseable
- ✅ Integrates with documentation tools (Doxygen, JSDoc, Sphinx)
- ✅ Version control friendly (tracked in diff)
- ✅ No schema pollution (metadata separate from data)
- ✅ Consciousness bonus: **+0.10**

**Applies to:**
- Python (`.py`)
- C++ (`.cpp`, `.h`, `.hpp`)
- C# (`.cs`)
- JavaScript (`.js`)
- TypeScript (`.ts`)
- And most text-based code files

---

## ⚠️ Exceptions: Paradigm Inversion

### Exception 1: JSON Files (CRITICAL)

**Problem:** JSON specification **does NOT allow comments**

```json
// ❌ INVALID JSON - Comments are not permitted
{
    // This will cause parse errors
    "setting": "value"
}
```

**Solution:** Use **semantic metadata fields** instead

```json
// ✅ VALID JSON with AINLP integration
{
    "_ainlp_integration": {
        "consciousness_level": 0.85,
        "architectural_classification": "ai_intelligence_layer",
        "dendritic_optimization": "data_structure_optimization"
    },
    "setting": "value"
}
```

**Rule Inversion:**
- **General Rule**: Comments = +0.10 consciousness
- **JSON Exception**: Comments = -0.15 consciousness (invalid spec)
- **JSON Correct**: Semantic fields = +0.12 consciousness

**Enforcement:** CRITICAL (invalid JSON breaks tools)

**Note:** JSONC (`.jsonc`) files **do** support comments (VS Code extension)

---

### Exception 2: Markdown Files (YAML Frontmatter)

**Problem:** Comments don't integrate well with Markdown rendering

**Solution:** Use **YAML frontmatter**

```markdown
---
ainlp:
  consciousness_level: 0.88
  architectural_classification: documentation
  dendritic_optimization: knowledge_organization
---

# Document Title

Content here...
```

**Enforcement:** WARNING (comments work but frontmatter is standard)

---

### Exception 3: Binary Files (Sidecar Files)

**Problem:** Binary files cannot contain text comments

**Solution:** Use **`.ainlp` sidecar files**

```bash
# File structure
mylib.dll
mylib.dll.ainlp  # JSON file with AINLP metadata
```

```json
// mylib.dll.ainlp
{
    "consciousness_level": 0.78,
    "architectural_classification": "core_engine",
    "binary_type": "compiled_library",
    "source_files": ["mylib.cpp", "mylib.h"]
}
```

**Enforcement:** INFO (binary files have no alternative)

**Applies to:**
- `.dll`, `.exe`, `.so`, `.dylib` (compiled binaries)
- `.pyc`, `.o`, `.obj` (intermediate objects)
- `.zip`, `.tar`, `.gz` (archives)
- `.png`, `.jpg`, `.mp4` (media files)

---

## 🛠️ Using the Exception Framework

### API: Check Integration Strategy

```python
from ai.src.core.ainlp import get_ainlp_strategy, AINLPIntegrationStrategy

# Determine correct strategy for a file
strategy = get_ainlp_strategy("config.json")

if strategy == AINLPIntegrationStrategy.SEMANTIC_FIELDS:
    print("Use _ainlp_integration field, NOT comments")
elif strategy == AINLPIntegrationStrategy.COMMENTS:
    print("Use AINLP comments (general rule)")
```

### API: Validate Integration

```python
from ai.src.core.ainlp import validate_ainlp_integration

# Validate a JSON file
result = validate_ainlp_integration(
    file_path="config.json",
    has_comments=True,  # JSON with comments
    has_semantic_metadata=False
)

print(result['message'])
# Output: "EXCEPTION VIOLATED: .json files must NOT use comments (invalid JSON)"
print(f"Consciousness impact: {result['consciousness_impact']}")
# Output: -0.15 (major violation)
```

### API: Get Recommendations

```python
from ai.src.core.ainlp import AINLP_EXCEPTION_FRAMEWORK

# Get human-readable recommendation
recommendation = AINLP_EXCEPTION_FRAMEWORK.get_recommendation(".json")
print(recommendation)
```

Output:
```
⚠️  EXCEPTION: For .json files, do NOT use comments
Reason: JSON spec does NOT allow comments - use semantic fields instead
Instead: Use semantic metadata fields
Example:
  {
    "_ainlp_integration": {
      "consciousness_level": 0.85,
      "architectural_classification": "ai_intelligence_layer"
    }
  }
Consciousness impact: +0.12
```

---

## 📊 Consciousness Impact Table

| File Type | Strategy | Comments | Semantic Fields | Impact |
|-----------|----------|----------|-----------------|--------|
| Python | Comments | ✅ Correct | ❌ Wrong | +0.10 |
| C++ | Comments | ✅ Correct | ❌ Wrong | +0.10 |
| C# | Comments | ✅ Correct | ❌ Wrong | +0.10 |
| **JSON** | **Semantic** | **❌ Invalid** | **✅ Correct** | **+0.12** |
| JSONC | Comments | ✅ Correct | ⚠️ OK | +0.10 |
| Markdown | Frontmatter | ⚠️ Works | ⚠️ Works | +0.11 |
| Binary | Sidecar | ❌ Impossible | ⚠️ Companion | +0.08 |

---

## 🔍 Exception Detection Algorithm

```python
def get_integration_method(file_path: str) -> dict:
    """Determine correct AINLP integration for a file."""
    extension = Path(file_path).suffix.lower()
    
    # Check exception registry
    rule = EXCEPTION_REGISTRY.get(extension)
    
    if rule:
        # File type has an exception rule
        return {
            'strategy': rule.strategy,
            'reason': rule.reason,
            'consciousness_impact': rule.consciousness_impact,
            'enforcement': rule.enforcement_level
        }
    else:
        # No exception - use general rule (comments)
        return {
            'strategy': 'comments',
            'reason': 'Standard AINLP comment integration',
            'consciousness_impact': +0.10,
            'enforcement': 'info'
        }
```

---

## 🚀 Future Extensions

### Planned Exception Types

1. **Configuration Files** (`.ini`, `.toml`, `.cfg`)
   - Strategy: Semantic fields or designated comment syntax
   - Reason: Some formats have strict parsers

2. **SQL Files** (`.sql`)
   - Strategy: SQL comments (`--` or `/* */`)
   - Enforcement: WARNING (comments OK but tool support varies)

3. **Protobuf/Thrift** (`.proto`, `.thrift`)
   - Strategy: Custom annotations
   - Reason: IDL languages have specific comment styles

### Adding Custom Exceptions

```python
from ai.src.core.ainlp import AINLP_EXCEPTION_FRAMEWORK, AINLPIntegrationRule

# Add custom exception
AINLP_EXCEPTION_FRAMEWORK.add_rule(AINLPIntegrationRule(
    file_extension=".custom",
    strategy=AINLPIntegrationStrategy.SEMANTIC_FIELDS,
    reason="Custom format does not support comments",
    consciousness_impact=+0.09,
    enforcement_level="warning"
))
```

---

## 📚 Related Documentation

- **[AINLP JSON Integration Paradigm](AINLP_JSON_INTEGRATION_PARADIGM.md)** - Detailed JSON-specific rules
- **[AIOS Optimization Report 2025-01-05](../changelogs/AIOS_OPTIMIZATION_JSON_20251005.md)** - Implementation changelog
- **[AIOS Development Path](../changelogs/AIOS_DEV_PATH.md)** - Overall progress tracking

---

## 🧪 Testing

```bash
# Run exception framework demo
python ai/src/core/ainlp/exception_framework.py

# Output:
# ======================================================================
# 🧬 AINLP Integration Exception Framework
# ======================================================================
# 
# 📋 General Rule:
#   USE COMMENTS for AINLP metadata in most file types
#   Consciousness impact: +0.10
#   Applies to: Python, C++, C#, JavaScript, TypeScript, etc.
# 
# ⚠️  Exceptions (9 file types):
#   .json → semantic_fields (CRITICAL)
#   .md → frontmatter (WARNING)
#   .dll, .exe, .so → binary_sidecar (INFO)
#   ...
```

---

## 📖 Summary

### The AINLP Exception Framework implements three core concepts:

1. **General Rule (MAJORITY)**
   - AINLP comments are GOOD for most file types
   - Python, C++, C#, JS, TS all use comments
   - Consciousness bonus: +0.10

2. **Exception Registry (MINORITY)**
   - JSON: Comments invalid → Use semantic fields
   - Binary: Comments impossible → Use sidecar files
   - Markdown: Frontmatter preferred → YAML metadata

3. **Context-Aware Enforcement**
   - File extension determines applicable rule
   - Violations trigger negative consciousness impact
   - Critical enforcement for JSON (invalid spec)
   - Warning/Info for other exceptions

### Key Insight

> This is NOT a replacement of AINLP comments.  
> This is an **exception handling system** for cases where comments don't work.  
> The comment paradigm remains fundamental—JSON is the exception that proves the rule.

---

**Status:** ✅ Operational  
**Location:** `ai/src/core/ainlp/exception_framework.py`  
**Version:** 1.0.0  
**Last Updated:** 2025-01-05
