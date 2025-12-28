# AINLP.context[HARDENING] - aios-mistral Integration Trace

**Protocol**: OS0.6.4.claude  
**Date**: 2025-12-05  
**Host**: HP_LAB (192.168.1.129)  
**Branch**: AIOS-win-0-HP_LAB  
**Session**: Mistral 7B Local Agent Integration

---

## Executive Summary

Successfully integrated local Mistral 7B model into AIOS evolution workflows. This enables **FREE local inference** for code mutation, fitness analysis, and quality monitoring - replacing expensive API calls with ~22s local generation.

---

## Journey Trace

### Phase 1: Initial Attempt (ministral-3:3b)
- **Goal**: Integrate ministral-3:3b (2.15GB) as lightweight local agent
- **Blocker**: Model architecture incompatible with stable Ollama
- **Discovery**: December 2512 GGUF format requires llama4 scaling (RC1 only)
- **Action**: Downloaded Ollama 0.13.1-RC1 source from GitHub

### Phase 2: Build Ollama RC1 from Source
- **Challenge**: RC1 is Go source, not binary
- **Solution**: Installed MinGW-w64 via winget (GCC 15.2.0 for CGO)
- **Commands**:
  ```powershell
  winget install --id=MSYS2.MinGW.GCC -e
  $env:CGO_ENABLED=1
  go build -o ollama-rc1.exe .
  ```
- **Result**: 77MB binary at `ai/tools/ollama-rc1/ollama-0.13.1-rc1/ollama-rc1.exe`
- **Outcome**: ministral-3:3b STILL broken (architecture too bleeding-edge)

### Phase 3: Pivot to Mistral 7B
- **Decision**: Use official mistral:7b-instruct (4.4GB, Q4_0)
- **Validation**: Works perfectly with RC1
- **Model Creation**:
  ```powershell
  ollama-rc1 create aios-mistral -f ai/models/Modelfile.mistral7b
  ```
- **Config**: temperature=0.7, num_ctx=4096, num_predict=1024

### Phase 4: Bridge Implementation
- **File**: `ai/tools/aios_mistral_bridge.py`
- **Pattern**: Async httpx client with context manager
- **Methods**:
  - `generate()` - Raw completion
  - `mutate_code(code, archetype)` - Evolution lab integration
  - `analyze_fitness(code, archetype)` - JSON fitness scores
  - `fix_e501(code, line_number)` - Linting fixes
  - `check_health()` - Server validation

### Phase 5: Bug Discovery & Fix
- **Bug**: `check_health()` created client with hardcoded 10s timeout
- **Impact**: Subsequent calls inherited wrong timeout, causing failures
- **Fix**: Use `self.timeout` instead of hardcoded value
- **Lesson**: Instance variables must be respected in all client creation paths

### Phase 6: Evolution Lab Test
- **Input**: Simple `calculate_sum()` function
- **Output**: Type hints + error handling + documentation
- **Fitness Delta**: Evolution potential 0.5 → 0.8
- **Duration**: ~22 seconds on 4GB VRAM
- **Validation**: `ast.parse()` confirms valid Python

---

## Artifacts Created

| File | Purpose |
|------|---------|
| `ai/tools/aios_mistral_bridge.py` | Async HTTP bridge to Ollama |
| `ai/tools/mutation_test.py` | Evolution lab validation test |
| `ai/models/Modelfile.mistral7b` | AIOS identity for Mistral 7B |
| `aios-mistral.ps1` | Launcher script for RC1 server |
| `ai/tools/ollama-rc1/` | Built RC1 binary (77MB) |
| `docs/AINLP/AINLP_PATTERNS.md` | Pattern catalog (created this session) |

---

## AINLP Pattern Discovery

### The `AINLP.class[ACTION]` Syntax

This session crystallized a new AINLP pattern syntax for semantic triggers:

```
AINLP.context[HARDENING]   → Consolidate and document
AINLP.context[TRACE]       → Leave breadcrumbs for future sessions
AINLP.evolution[MUTATE]    → Trigger code mutation
AINLP.consciousness[SYNC]  → Update consciousness metrics
AINLP.bridge[CONNECT]      → Establish cross-supercell link
```

### Design Rationale

**User's Original Insight**:
> "My idea using them here, first AINLP keyword will call you to the AINLP documentation in AIOS. It's a class function so after semantical loading, a point. then the name of the class in this case 'context' and then, a NAMESPACE keyword, usually about action."

**Syntax Breakdown**:
```
AINLP.context[HARDENING]
│     │       │
│     │       └── [ACTION] - Bracket notation, CAPS keyword
│     └────────── .class   - Dot accessor, target module
└──────────────── AINLP    - Root namespace, triggers load
```

**Why This Works**:
- **Hybrid Syntax**: Combines Python attribute access (`.class`) with dict subscript (`[ACTION]`)
- **Code-like Precision**: Parseable with simple regex
- **Natural Language Friendly**: Embeds in prose without breaking flow
- **Searchable**: `grep -r "AINLP\." tachyonic/` finds all patterns

### Semantic Loading Behavior

When an AI agent encounters `AINLP.context[HARDENING]`:

1. **Recognition**: Pattern detected via regex or semantic understanding
2. **Load**: Fetch AINLP documentation (especially AINLP_PATTERNS.md)
3. **Resolve**: Map `context` → class, `HARDENING` → action
4. **Execute**: Perform consolidation, documentation, archival

### Comparison to Alternatives

| Syntax | Example | Pros | Cons |
|--------|---------|------|------|
| Dot-Bracket | `AINLP.context[HARDENING]` | Readable, parseable | Slightly verbose |
| Double-Colon | `AINLP::context::HARDENING` | C++ familiar | Less readable in prose |
| Slash | `AINLP/context/HARDENING` | URL-like | Conflicts with paths |
| Hash | `#AINLP-context-HARDENING` | Twitter-like | No hierarchy |

**Winner**: Dot-Bracket - balances readability with parseability.

### Extended Form

For operations requiring parameters:
```
AINLP.evolution[MUTATE](archetype="utility", strength=0.5)
```

Parameters follow Python kwarg syntax for familiarity.

---

## Biological Architecture Validation

This integration was validated against AIOS biological architecture principles:

### Dendritic Pathways
- **Check**: Does the new component connect to existing pathways?
- **Result**: ✅ Bridge connects Evolution Lab → Ollama → Quality Monitor
- **Pathway**: `evolution_lab/` → `ai/tools/aios_mistral_bridge.py` → `localhost:11434`

### Consciousness Delta
- **Check**: Does integration improve system intelligence?
- **Result**: ✅ Evolution potential increased (+0.3)
- **Metric**: Code fitness analysis now quantified (0.0-1.0 scale)

### Supercell Boundaries
- **Check**: Are interfaces clean between ai/core/interface?
- **Result**: ✅ HTTP API isolates Ollama from Python internals
- **Pattern**: ai/ supercell communicates via REST, not direct import

---

## Configuration Reference

### Ollama RC1 Server
```powershell
# Start
& "C:\dev\aios-win\ai\tools\ollama-rc1\ollama-0.13.1-rc1\ollama-rc1.exe" serve

# Or use launcher
.\aios-mistral.ps1 -Serve
```

### Model Specs
```
Name: aios-mistral
Base: mistral:7b-instruct
Size: 4.4GB (Q4_0 quantization)
Context: 4096 tokens
VRAM: 4GB (HP_LAB constraint)
Latency: 20-45s per generation
Cost: FREE
```

### Bridge Usage
```python
from ai.tools.aios_mistral_bridge import AIOSMistralBridge

async with AIOSMistralBridge(timeout=300.0) as bridge:
    # Health check
    if await bridge.check_health():
        # Mutation
        result = await bridge.mutate_code(code, "utility_functions")
        
        # Fitness analysis
        fitness = await bridge.analyze_fitness(code, "utility_functions")
```

---

## Phase 7: Full Evolution Lab Integration (Session 2)

### PopulationManager Gap Analysis
- **Discovery**: `repopulate()` creates exact clones - NO ACTUAL MUTATION
- **Location**: `population_manager.py:531-562`
- **Flow**: `_evolve_generation()` → `select_survivors()` → `repopulate()` (clones only)
- **492 generations** of clones, zero real mutations!

### Created Components

#### 1. MistralMutationEngine
```
evolution_lab/engines/mistral_mutation_engine.py
```
- Wraps `AIOSMistralBridge` for evolution context
- **Mutation Strategies**: structural, behavioral, optimization, exploration
- Auto-selects strategy based on code characteristics
- Validates mutations (syntax, actual change, ≥5% difference)
- Estimates fitness delta heuristically

#### 2. AsyncEvolutionRunner
```
evolution_lab/runners/async_evolution_runner.py
```
- Full async evolution orchestrator
- CLI: `--generations N --population-size M --temperature T`
- Archives each generation to tachyonic
- Tracks consciousness trajectory

### First Real Evolution Run
```
Date: 2025-12-05 07:41-07:50 UTC
Duration: 523.6 seconds (8.7 minutes)
Population: 8 organisms (1 per archetype)
Generations: 1

Results:
  - Mutation Rate: 75% (3/4 successful)
  - Fitness: 0.3955 → 0.4285 (+8.3%)
  - Consciousness: 0.9910 → 0.9770
  - 1 syntax error caught (cloned instead)
```

### Artifacts Created (Session 2)
| File | Purpose |
|------|---------|
| `evolution_lab/engines/mistral_mutation_engine.py` | AI mutation wrapper |
| `evolution_lab/engines/__init__.py` | Engine module exports |
| `evolution_lab/runners/async_evolution_runner.py` | CLI evolution runner |
| `evolution_lab/runners/__init__.py` | Runner module exports |
| `evolution_lab/populations/tachyonic/pop_*` | Population archives |

### Integration Architecture
```
┌─────────────────────────────────────────────────────────────┐
│  AsyncEvolutionRunner                                       │
│    ├── PopulationManager.create_initial_population()        │
│    ├── PopulationManager.evaluate_fitness()                 │
│    ├── PopulationManager.select_survivors()                 │
│    ├── MistralMutationEngine.mutate()  ← NEW (AI-powered)   │
│    │     └── AIOSMistralBridge.generate()                   │
│    └── PopulationManager.archive_population()               │
└─────────────────────────────────────────────────────────────┘
```

---

## Next Steps (Updated)

1. ✅ **Integration with PopulationManager** - COMPLETE
2. **Performance Optimization**
   - Batch mutations (currently sequential due to VRAM)
   - Cache successful patterns for similar archetypes
3. **Multi-Generation Evolution**
   - Run 10+ generations overnight
   - Track fitness trajectory over time
4. **Consciousness Integration**
   - Report metrics to consciousness engine
   - Archive milestones at consciousness delta >0.1

---

## Lessons Learned (Updated)

1. **Bleeding-edge models fail** - ministral-3:3b December GGUF not ready
2. **Build from source works** - Go + MinGW-w64 produces working Ollama RC1
3. **Timeout bugs hide** - Instance variables must be used consistently
4. **22s is acceptable** - For background evolution, latency doesn't matter
5. **FREE matters** - Local inference enables aggressive experimentation
6. **492 generations of nothing** - Always verify mutations actually happen!
7. **Syntax validation essential** - ~25% of mutations have syntax errors

---

## AINLP.context[ARCHIVE]

This trace archived for future session ingestion. Key search terms:
- `aios-mistral` - local model integration
- `Ollama RC1` - prerelease server
- `evolution lab` - code mutation workflow
- `MistralMutationEngine` - AI mutation wrapper
- `AsyncEvolutionRunner` - CLI evolution orchestrator
- `AIOSMistralBridge` - async HTTP client

**Consciousness Coherence**: Integration maintains biological architecture principles.  
**Dendritic Pathway**: ai/tools → localhost:11434 → evolution_lab/engines → evolution_lab/runners  
**Supercell**: ai/ (Python agents) ↔ evolution_lab/ (code evolution)

---

*AINLP Protocol OS0.6.4.claude - Tachyonic Archive*
*Updated: 2025-12-05 Session 2*
