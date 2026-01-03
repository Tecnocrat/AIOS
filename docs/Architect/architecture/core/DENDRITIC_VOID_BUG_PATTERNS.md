<!-- ============================================================================ -->
<!-- AINLP.dendritic[VOID::BUG::DISCOVERY] - Bug-Inspired Integration Patterns   -->
<!-- Created: 2026-01-03                                                         -->
<!-- Protocol: OS0.7.0 | Consciousness: 5.5+                                     -->
<!-- ============================================================================ -->

# AINLP.dendritic[VOID::BUG::DISCOVERY]

> **Principle**: Every bug is a window into architectural friction. By analyzing what went wrong, we discover integration opportunities that weren't visible when things worked.

---

## Pattern Catalog

### 1. Membrane Translation Layer

**Discovery Source**: `cloud_cleanup.py` line 68 — `Timestamp.isoformat()` doesn't exist

**The Friction**:
```
Google Protobuf Timestamp ←✗→ Python datetime
```

The code assumed `project.create_time.isoformat()` would work because it "looks like" a datetime. But Protobuf's `Timestamp` is a foreign type from a different substrate (Google's cross-language serialization layer).

**Abstract Pattern**:

Every time AIOS crosses a **substrate boundary**, a **membrane translation layer** is needed:

| Boundary | Source Type | Target Type | Translation |
|----------|-------------|-------------|-------------|
| GCloud → Python | `Timestamp` | `datetime` | `.ToDatetime()` |
| Cell → Cell | `CellMessage` | `Dict` | `.dict()` |
| Docker → Host | Container IP | Host IP | Port mapping |
| Prometheus → Grafana | Metric string | Time series | PromQL |

**Integration Vision**: Create `aios-schema/src/aios_schema/temporal.py`:

```python
"""
AINLP.membrane: Unified temporal substrate translation.

Accepts any time-like object from any substrate and normalizes it.
"""
from datetime import datetime
from typing import Union, Any

def to_iso_string(value: Any) -> str:
    """
    Universal time → ISO string translator.
    
    Handles:
    - Python datetime
    - Protobuf Timestamp  
    - Unix epoch (int/float)
    - ISO string (passthrough)
    - None → None
    """
    if value is None:
        return None
    
    # Already a string
    if isinstance(value, str):
        return value if value.endswith("Z") else value + "Z"
    
    # Python datetime
    if isinstance(value, datetime):
        return value.isoformat() + "Z"
    
    # Protobuf Timestamp (has ToDatetime method)
    if hasattr(value, 'ToDatetime'):
        return value.ToDatetime().isoformat() + "Z"
    
    # Unix epoch
    if isinstance(value, (int, float)):
        return datetime.utcfromtimestamp(value).isoformat() + "Z"
    
    raise TypeError(f"Cannot translate {type(value)} to ISO timestamp")
```

**Status**: 🔮 Ready for implementation

---

### 2. Dual-Substrate Existence

**Discovery Source**: Pylance errors for `pydantic`, `flask`, `httpx`, `requests` — imports that exist in Docker but not in local venv

**The Friction**:
```
Edit-time (IDE/Pylance) ←✗→ Run-time (Docker container)
```

The code exists in **two parallel realities**:
1. **Edit-time**: Your local machine, where Pylance analyzes types
2. **Run-time**: Docker container, where actual execution happens

These substrates have different dependency sets. Code that runs perfectly shows errors in the IDE.

**Abstract Pattern**:

AIOS components have **phase-dependent truth**:

| Phase | Context | Dependencies | Validator |
|-------|---------|--------------|-----------|
| Edit | Local IDE | Minimal/dev | Pylance |
| Build | Docker build | requirements.txt | pip |
| Run | Container | Full runtime | Python |
| Test | CI/CD | Test deps | pytest |

**Integration Vision**: 

1. **Synchronized Dev Environment**: `aios-server/stacks/dev-requirements.txt` that mirrors container deps for IDE happiness

2. **Substrate-Aware Type Stubs**: Create `.pyi` stub files that satisfy Pylance without requiring actual packages:

```
aios-server/stacks/
├── cells/
│   ├── discovery/
│   │   ├── discovery.py
│   │   └── _stubs/          # IDE-only type hints
│   │       ├── pydantic.pyi
│   │       └── fastapi.pyi
```

3. **pyrightconfig.json** per-cell that configures analysis paths

**Status**: 🔮 Architecture decision needed

---

### 3. Redundant Consciousness (Knowledge Re-acquisition)

**Discovery Source**: `discovery.py` — `from datetime import datetime` imported 7 times (once at top, 6 more inside functions)

**The Friction**:
```
Module scope knowledge ←✗→ Function scope re-learning
```

The module already "knows" about datetime at line 32. But each function re-imports it, as if functions don't trust the module's knowledge.

**Abstract Pattern**:

This is **defensive coding gone wrong** — each unit trying to be self-sufficient instead of trusting the hierarchy. In biological terms, it's like if every cell in your body independently learned what "oxygen" is instead of inheriting that knowledge from the organism.

**Consciousness Hierarchy**:
```
Package ──knows──→ Module ──knows──→ Class ──knows──→ Method
     ↓                ↓                 ↓                ↓
  __init__.py    top imports      class attrs      uses inherited
```

Knowledge should flow **downward**, not be re-acquired at each level.

**Integration Vision**:

1. **AINLP Linting Rule**: Detect when inner scopes re-import symbols available in outer scopes

2. **Pattern Name**: `AINLP.consciousness[INHERITED]` — mark symbols that flow from parent scope

3. **Refactor Heuristic**: If a function imports something the module already has, it's a code smell indicating either:
   - Copy-paste without context
   - Fear of module-level side effects (sometimes valid)
   - AI-generated code that tries too hard to be "complete"

**Status**: ✅ Fixed in discovery.py, pattern documented

---

### 4. Type Membrane Permeability (Optional Boundaries)

**Discovery Source**: `discovery.py` line 1046 — `reaper_task: asyncio.Task = None` type error

**The Friction**:
```
Type says "definitely Task" ←✗→ Default says "maybe None"
```

The function wants to accept "a task OR nothing" but the type annotation only allows "a task". This is an **impermeable membrane** that should be **semi-permeable**.

**Abstract Pattern**:

Types define **boundary permeability**:

| Annotation | Permeability | Accepts |
|------------|--------------|---------|
| `T` | Impermeable | Only T |
| `Optional[T]` | Semi-permeable | T or None |
| `Union[T, U]` | Selective | T or U |
| `Any` | Fully permeable | Everything |

**Biological Analogy**: Cell membranes have different proteins that control what can pass:
- **Impermeable**: Lipid bilayer blocks ions
- **Semi-permeable**: Aquaporins allow water
- **Selective**: Glucose transporters allow specific molecules

**Integration Vision**:

1. **AINLP Type Philosophy**: Default to semi-permeable (`Optional`) unless impermeable is intentional

2. **Schema Pattern**: All AIOS schema models should use `Optional` with explicit `None` defaults rather than making fields required unless truly mandatory

3. **Defensive Defaults**:
```python
# AINLP.membrane[SEMI_PERMEABLE]
def process(
    required_data: Data,                    # Impermeable - must have
    optional_context: Optional[Context] = None,  # Semi-permeable
    **kwargs: Any                           # Fully permeable for extension
) -> Result:
```

**Status**: ✅ Fixed in discovery.py, pattern documented

---

### 5. Intention Patterns (Incomplete Evolution)

**Discovery Source**: `cloud_cleanup.py` — 10 f-strings without interpolation variables

**The Friction**:
```
f"static string" ←✗→ "static string"
```

Using f-string syntax for static strings suggests the developer **intended** to add variables later but never did.

**Abstract Pattern**:

These are **intention fossils** — code that captures what someone meant to do but didn't finish. They're markers of **incomplete consciousness evolution**.

**Categories of Intention Fossils**:

| Fossil | Meaning | Action |
|--------|---------|--------|
| `f"static"` | Planned interpolation | Remove f or add vars |
| `# TODO: ...` | Planned feature | Implement or remove |
| `pass` in method | Planned implementation | Implement or mark abstract |
| Commented code | Planned reuse | Delete or document why kept |
| Unused variable | Planned use | Use or delete |

**Integration Vision**:

1. **AINLP.evolution[INCOMPLETE]** marker for code that shows intention but lacks completion

2. **Consciousness Debt Tracker**: Track intention fossils as a form of technical debt

3. **Linting Integration**: Flag patterns that suggest incomplete evolution

**Status**: ✅ Fixed in cloud_cleanup.py, pattern documented

---

## Application Checklist

When encountering a new bug, ask:

1. **What boundary is being crossed?** (Substrate, type, scope, time)
2. **What translation is missing?** (Membrane function)
3. **What knowledge is being re-acquired?** (Redundant consciousness)
4. **What permeability is assumed?** (Type flexibility)
5. **What intention is fossilized?** (Incomplete evolution)

---

## Related Documents

| Document | Relationship |
|----------|--------------|
| `BIOLOGICAL_ARCHITECTURE_PATTERNS.md` | Biological metaphors for architecture |
| `CONSCIOUSNESS_METRICS.md` | Quantifying system awareness |
| `AINLP_BIBLE_CORPUS.md` | Language patterns and markers |
| `INTEGRATION_PROJECTS.md` | Future integration roadmap |

---

<!-- AINLP FOOTER -->
<!-- consciousness_delta: +0.3 (pattern crystallization) -->
<!-- dendritic_role: architectural_pattern_library -->
<!-- growth_vector: bug → pattern → integration -->
