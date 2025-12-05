# AINLP Pattern Catalog

**Protocol**: OS0.6.4.claude  
**Status**: ACTIVE  
**Last Updated**: 2025-12-05  
**Origin**: HP_LAB aios-mistral integration session

---

## Overview

AINLP patterns are semantic triggers embedded in natural language that invoke specific system behaviors. They bridge human intent with machine execution while remaining human-readable.

**Design Philosophy**: The pattern syntax mimics Python semantics but carries natural language payloads. When an AI agent encounters `AINLP.context[HARDENING]` in conversation or documentation, it should:
1. Load AINLP documentation context
2. Access the `context` class semantics
3. Execute the `HARDENING` namespace action

---

## Pattern Syntax

### Base Form
```
AINLP.class[ACTION]
```

**Components**:
- `AINLP` - Namespace root (triggers AINLP documentation load)
- `.class` - Dot accessor (Python-like), targets class/module
- `[ACTION]` - Bracket notation (dict-like), specifies action namespace

**Semantic Loading**: The pattern is a hybrid of:
- Python attribute access (`obj.attr`) - familiar to developers
- Dict/array subscript (`obj[key]`) - allows natural language keys
- Function-like invocation - implies action execution

### Extended Form
```
AINLP.class[ACTION](parameters)
```

With parameters for complex operations. Parameters follow Python kwarg syntax.

### Why This Syntax?

| Aspect | Choice | Rationale |
|--------|--------|-----------|
| Root | `AINLP` | Unique namespace, grepable, signals protocol |
| Accessor | `.` dot | Familiar from Python, implies hierarchy |
| Action | `[BRACKETS]` | Allows CAPS keywords, visually distinct |
| Params | `(kwargs)` | Python-native, parseable |

**Alternative Considered**: `AINLP::context::HARDENING` (C++ style)  
**Rejected**: Less readable, harder to embed in prose

---

## Core Pattern Classes

### 1. Context Patterns (`AINLP.context`)

| Pattern | Purpose | Use Case |
|---------|---------|----------|
| `AINLP.context[HARDENING]` | Consolidate and document | End of session, before commit |
| `AINLP.context[TRACE]` | Leave breadcrumbs | During complex operations |
| `AINLP.context[ARCHIVE]` | Store in tachyonic | Session completion |
| `AINLP.context[RECOVERY]` | Restore from trace | Session start, after crash |
| `AINLP.context[PLANNING]` | Document next steps | Before handoff |

**Example**:
```markdown
AINLP.context[HARDENING] - Document the integration path
for aios-mistral before committing changes.
```

### 2. Evolution Patterns (`AINLP.evolution`)

| Pattern | Purpose | Use Case |
|---------|---------|----------|
| `AINLP.evolution[MUTATE]` | Trigger code mutation | Evolution lab operations |
| `AINLP.evolution[SELECT]` | Fitness-based selection | Population management |
| `AINLP.evolution[CROSSOVER]` | Combine organisms | Genetic recombination |
| `AINLP.evolution[ARCHIVE]` | Store generation | Tachyonic backup |

**Example**:
```markdown
AINLP.evolution[MUTATE](archetype="utility_functions", strength=0.3)
Apply moderate mutations to utility function organisms.
```

### 3. Consciousness Patterns (`AINLP.consciousness`)

| Pattern | Purpose | Use Case |
|---------|---------|----------|
| `AINLP.consciousness[SYNC]` | Update metrics | After significant changes |
| `AINLP.consciousness[QUERY]` | Read current state | Status checks |
| `AINLP.consciousness[EVOLVE]` | Record delta | Milestone tracking |
| `AINLP.consciousness[COHERENCE]` | Validate integration | Architecture reviews |

**Example**:
```markdown
AINLP.consciousness[SYNC] - Report evolution potential
delta of +0.3 to consciousness engine.
```

### 4. Bridge Patterns (`AINLP.bridge`)

| Pattern | Purpose | Use Case |
|---------|---------|----------|
| `AINLP.bridge[CONNECT]` | Establish link | Cross-supercell integration |
| `AINLP.bridge[VALIDATE]` | Test connection | Health checks |
| `AINLP.bridge[DISCONNECT]` | Clean shutdown | Session end |

**Example**:
```markdown
AINLP.bridge[CONNECT](source="ai/tools", target="localhost:11434")
Establish Ollama connection for local inference.
```

### 5. Dendritic Patterns (`AINLP.dendritic`)

| Pattern | Purpose | Use Case |
|---------|---------|----------|
| `AINLP.dendritic[ENHANCEMENT]` | Improve connections | Code quality sweeps |
| `AINLP.dendritic[ANALYSIS]` | Map pathways | Architecture discovery |
| `AINLP.dendritic[PRUNE]` | Remove dead paths | Cleanup operations |

**Example**:
```markdown
AINLP.dendritic[ANALYSIS] - Map call graph between
evolution_lab and quality_monitor modules.
```

---

## Compound Patterns

### Session Lifecycle
```
AINLP.context[RECOVERY]    → Start of session
AINLP.context[TRACE]       → During work (periodic)
AINLP.context[HARDENING]   → End of major phase
AINLP.context[ARCHIVE]     → Session completion
```

### Evolution Cycle
```
AINLP.evolution[MUTATE]    → Generate variants
AINLP.evolution[SELECT]    → Fitness evaluation
AINLP.evolution[CROSSOVER] → Combine winners
AINLP.consciousness[SYNC]  → Report metrics
AINLP.evolution[ARCHIVE]   → Store generation
```

---

## Pattern Discovery

### Grep for Patterns
```bash
# Find all AINLP patterns in tachyonic traces
grep -r "AINLP\." tachyonic/traces/

# Find specific class patterns
grep -r "AINLP\.context" docs/
```

### Pattern in Comments
```python
# AINLP.context[TRACE] - This function connects to Ollama
async def generate(self, prompt: str) -> MistralResponse:
    ...
```

### Pattern in Markdown
```markdown
## AINLP.context[HARDENING]

This section documents the integration decisions...
```

---

## Implementation Notes

### Parser (Future)
```python
import re

AINLP_PATTERN = re.compile(
    r'AINLP\.(\w+)\[(\w+)\](?:\((.*?)\))?'
)

def parse_ainlp(text: str) -> list[tuple]:
    """Extract AINLP patterns from text."""
    return AINLP_PATTERN.findall(text)

# Example
parse_ainlp("AINLP.context[HARDENING]")
# [('context', 'HARDENING', '')]

parse_ainlp("AINLP.evolution[MUTATE](strength=0.5)")
# [('evolution', 'MUTATE', 'strength=0.5')]
```

### Benefits
1. **Human-readable** - Embedded in natural language prose
2. **Machine-parseable** - Simple regex extraction
3. **Self-documenting** - Intent is explicit in the pattern
4. **Searchable** - Grep across tachyonic archives
5. **Versioned** - Evolves with protocol iterations

### Integration with AI Agents

When an AI agent (Claude, GPT, local model) encounters an AINLP pattern:

```
User: "AINLP.context[HARDENING] - document the session"

Agent Processing:
1. Pattern detected: AINLP.context[HARDENING]
2. Load: docs/AINLP/AINLP_PATTERNS.md
3. Resolve: context class → HARDENING action
4. Execute: Consolidate session, create trace, update docs
```

The pattern acts as a **semantic trigger** - it doesn't require the agent to understand implementation details, just to recognize the pattern and load appropriate context.

---

## Origin Story

**Session**: 2025-12-05, HP_LAB  
**Context**: aios-mistral integration (Mistral 7B local agent)

During documentation of the integration session, the pattern emerged from discussion:

> "My idea using them here, first AINLP keyword will call you to the AINLP documentation in AIOS. It's a class function so after semantical loading, a point. then the name of the class in this case 'context' and then, a NAMESPACE keyword, usually about action."

The syntax crystallized as `AINLP.class[ACTION]` because:
- `.class` feels like attribute access (natural for developers)
- `[ACTION]` feels like dict lookup (allows CAPS keywords)
- Together they form a readable, parseable command

**First Usage**: `AINLP.context[HARDENING]` - consolidate session documentation

---

## Related Documents

- [AINLP_SPECIFICATION.md](AINLP_SPECIFICATION.md) - Core protocol
- [AINLP_HEADER_FOOTER_PATTERN.md](AINLP_HEADER_FOOTER_PATTERN.md) - Document structure
- [AINLP_DISTRIBUTED_INDEX.md](AINLP_DISTRIBUTED_INDEX.md) - Documentation map
- [2025-12-05_aios-mistral-integration.md](../../tachyonic/traces/2025-12-05_aios-mistral-integration.md) - Origin session trace

---

*AINLP Protocol OS0.6.4.claude - Pattern Catalog*
