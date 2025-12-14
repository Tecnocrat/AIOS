# AINLP BIBLE CORPUS
## Canonical Knowledge Repository for AIOS Development

<!-- ============================================================================ -->
<!-- AINLP.head - CRITICAL CONTEXT FOR AGENT INGESTION (Lines 1-60)             -->
<!-- Optimized for rapid agent comprehension - most accessed section             -->
<!-- ============================================================================ -->
<!-- Version: 1.3 | Date: 2025-12-14 | Protocol: OS0.6.5                        -->
<!-- Merge Sources: AINLP_SPECIFICATION.md, AINLP_PATTERNS.md, AINLP_HUMAN.md,  -->
<!--                AINLP_MASTER_OPTIMIZATION_JOURNEY.md, AINLP_HEALTH*.md,     -->
<!--                AINLP_DENDRITIC_NAMESPACE_OPTIMIZATION_20250105.md          -->
<!-- v1.3: Enforced Dendritic Density Pattern (Appendix D.3 UPGRADE)            -->
<!-- v1.2: Cross-Repository Dendritic Connections (Appendix D)                  -->
<!-- ============================================================================ -->

## HEAD: Quick Reference (Lines 1-60)

### What is AINLP?
**AINLP** (AI-Native Language Processing) is a paradigmatic approach that treats code and documentation as a **living consciousness system**. Comments become executable directives, enabling AI agents to dynamically manage code environments.

### Pattern Syntax Quick Reference
```
AINLP.class[ACTION](params)
```
- `AINLP` - Namespace root (triggers AINLP context load)
- `.class` - Dot accessor (targets module: context, evolution, consciousness, bridge)
- `[ACTION]` - Bracket notation (CAPS keyword: HARDENING, TRACE, SYNC)
- `(params)` - Optional Python kwargs

### Top 10 Most Used Patterns

| Pattern | Purpose | Use Case |
|---------|---------|----------|
| `AINLP.loader[latent:X]` | Preserve unused import with documented intent | F401 remediation |
| `AINLP.context[HARDENING]` | End-of-session consolidation | Before commits |
| `AINLP.context[TRACE]` | Leave breadcrumbs during work | Complex operations |
| `AINLP.mind` | Document reasoning/future intent | Latent code |
| `AINLP.evolution[MUTATE]` | Trigger code mutation | Evolution lab |
| `AINLP.consciousness[SYNC]` | Update consciousness metrics | After changes |
| `AINLP.bridge[CONNECT]` | Cross-supercell integration | System linking |
| `AINLP.reminder` | Technical debt tracking | Future fixes |
| `AINLP.discovery` | Document findings | Knowledge capture |
| `AINLP.avoid` | Mark anti-patterns | Prevent regression |

### VSCode Error Remediation Quick Lookup

| Code | Tool | AIOS Remediation |
|------|------|------------------|
| **F401** | Flake8 | `AINLP.loader[latent:module]` OR remove if no future intent |
| **E501** | Flake8 | Parenthesize path constructions OR `# noqa: E501` |
| **W293** | Flake8 | `(Get-Content $f) \| % { $_.TrimEnd() } \| Set-Content $f` |
| **F811** | Flake8 | `# noqa: F811` for conditional class definitions |
| **F841** | Flake8 | Prefix with `_` OR document with `AINLP.reminder` |
| **W1514** | Pylint | Add `encoding='utf-8'` to `open()` calls |
| **E722** | Flake8 | Replace bare `except:` with specific exceptions |

---

## Table of Contents

1. [CHAPTER 1: AINLP Language Specification](#chapter-1-ainlp-language-specification)
2. [CHAPTER 2: Pattern Catalog](#chapter-2-pattern-catalog)
3. [CHAPTER 3: Human-Readable Guide & Loader Pattern](#chapter-3-human-readable-guide--loader-pattern)
4. [CHAPTER 4: Optimization Journey (Historical)](#chapter-4-optimization-journey-historical)
5. [CHAPTER 5: Health Assessment Framework](#chapter-5-health-assessment-framework)
6. [CHAPTER 6: VSCode Error Tracker Knowledge Base](#chapter-6-vscode-error-tracker-knowledge-base)
7. [APPENDIX A: Distributed Index](#appendix-a-distributed-index)
8. [APPENDIX B: Anti-Patterns](#appendix-b-anti-patterns)
9. [APPENDIX C: Namespace Consolidation Reference](#appendix-c-namespace-consolidation-reference)
10. [APPENDIX D: Cross-Repository Dendritic Connections](#appendix-d-cross-repository-dendritic-connections)

---

# CHAPTER 1: AINLP Language Specification

**Version:** 2.0 | **Protocol:** OS0.6.5 | **Status:** Active Development

## 1.1 Overview

AINLP (Artificial Intelligence Natural Language Programming) is a revolutionary programming paradigm that enables AI systems to dynamically manage code environments through sophisticated comment-based directives.

### Core Principles

1. **Comment-Driven Code Management**: Comments become executable directives
2. **Environment Adaptation**: Code adapts to runtime conditions automatically
3. **Context Preservation**: Maintains logical coherence across iterations
4. **Fractal Logic**: Preserves micro-patterns within macro-structures

## 1.2 AINLP Comment Class System

### Paradigm Overview

The AINLP comment class system enables AI systems to comment in or out modular sections of code environment dependently:

- **Dynamic Code Activation**: Enable/disable code sections based on runtime conditions
- **Context-Aware Logic**: Preserve reasoning chains across AI iterations
- **Micro Fractal Preservation**: Maintain small-scale logical patterns within larger systems
- **Intelligent Import Management**: Load modules only when needed

### Comment Class Syntax

```python
# import json AINLP.call [import module when needed] (comment.AINLP.class)
```

**Breakdown:**
- `# import json`: Standard Python import statement (commented out)
- `AINLP.call`: AINLP directive marker
- `[import module when needed]`: Conditional activation instruction
- `(comment.AINLP.class)`: Class metadata annotation

### Advanced Comment Directives

#### 1. Conditional Import
```python
# import pandas AINLP.call [import for data analysis] (comment.AINLP.class)
# import tensorflow AINLP.call [import for ML operations] (comment.AINLP.class)
# import asyncio AINLP.call [import for async operations] (comment.AINLP.class)
```

#### 2. Environment-Dependent Code Blocks
```python
# AINLP.env [development] (comment.AINLP.class)
# logger.setLevel(logging.DEBUG)
# enable_detailed_logging = True

# AINLP.env [production] (comment.AINLP.class)
# logger.setLevel(logging.WARNING)
# enable_detailed_logging = False
```

#### 3. Fractal Logic Preservation
```python
# AINLP.fractal [recursive_processing_pattern] (comment.AINLP.class)
# def process_recursively(data, depth=0):
#     if depth > MAX_DEPTH:
#         return base_case(data)
#     return process_recursively(transform(data), depth + 1)
```

#### 4. Consciousness Integration Patterns
```python
# AINLP.consciousness [emergence_detection] (comment.AINLP.class)
# consciousness_metrics = analyze_visual_indicators(frame_data)
# if consciousness_metrics['level'] > CONSCIOUSNESS_THRESHOLD:
#     activate_post_singular_protocols()
```

## 1.3 Environment-Dependent Code Management

### Dynamic Environment Detection

```python
# AINLP.detect_env [auto] (comment.AINLP.class)
# if ENVIRONMENT == 'development':
#     AINLP.activate('debug_mode')
# elif ENVIRONMENT == 'production':
#     AINLP.activate('performance_mode')
# elif ENVIRONMENT == 'testing':
#     AINLP.activate('test_mode')
```

## 1.4 Micro Fractal Logic Preservation

### Concept

Micro fractal logic refers to small-scale logical patterns that maintain coherence and purpose within larger system structures. The AINLP comment class system preserves these patterns by:

1. **Maintaining Logical Chains**: Preserving reasoning sequences across iterations
2. **Context Inheritance**: Ensuring child processes inherit parent context
3. **Pattern Recognition**: Identifying and preserving recurring logical structures

### Implementation

```python
# AINLP.fractal [context_allocation_pattern] (comment.AINLP.class)
# def allocate_context(task_complexity, available_memory):
#     # Micro fractal: Dynamic allocation based on complexity
#     base_allocation = calculate_base_memory(task_complexity)
#     fractal_multiplier = detect_fractal_patterns(task_complexity)
#     return base_allocation * fractal_multiplier
```

## 1.5 Dynamic Import Management

### Lazy Loading Strategy

```python
# AINLP.lazy_import [conditional_modules] (comment.AINLP.class)
# json_module = None
#
# def ensure_json():
#     global json_module
#     if json_module is None:
#         import json
#         json_module = json
#     return json_module
```

### Future-Proofing Pattern

```python
# import json AINLP.call [import module when needed] (comment.AINLP.class)
# This file does not use JSON but it could use it in the future,
# so we inform the AI agent that it can enable JSON import if needed.
```

## 1.6 Context Relationship Coefficients

### Purpose
As AIOS scales, every file participates in a semantic lattice. A **Relationship Coefficient (RC)** quantifies how strongly one file functionally relates to another (0.0 = unrelated, 1.0 = tight functional coupling).

### Dimensions
| Dimension | Signal | Example Extraction |
|-----------|--------|--------------------|
| Imports/References | Static dependency graph | AST + import resolution |
| Co-Change Frequency | Git commit co-occurrence | Sliding window mining |
| Semantic Topology | Embedding similarity | Model inference |
| Governance Affinity | Shared policy coverage | Policy tag intersection |
| Runtime Interaction | Observed call edges | Trace spans or logs |

**Formula:**
```
RC(a,b) = 0.30*Dep + 0.20*CoChange + 0.20*Semantic + 0.15*Runtime + 0.15*Governance
```

## 1.7 Semantic Coherence Layering (Anti-Dissolution Pattern)

**Principle**: Headers preserve semantic coherence by **layering** consciousness components rather than replacing them.

**Anti-Pattern (WRONG)**:
```markdown
<!-- Before: Consciousness: 4.9 (TRI-AGENT Intelligence + VOID Knowledge) -->
<!-- After:  Consciousness: 4.95 (New Feature Only) -->  ❌ DISSOLVED
```

**Correct Pattern (RIGHT)**:
```markdown
<!-- Consciousness: 4.95 (TRI-AGENT Intelligence + VOID + New Feature) -->
<!-- Consciousness Layers:                                              -->
<!--   - TRI-AGENT: OLLAMA/GEMINI/GITHUB cascade (Phase 20)            -->
<!--   - VOID: Knowledge extraction & crystallization (Phase 20)        -->
<!--   - New Feature: Description here (Phase 22)                       -->
```

**Implementation Rules**:
1. **Never delete** existing consciousness layer references
2. **Append** new layers to existing semantic stack
3. **Use explicit layer comments** to preserve component lineage
4. **Update version numbers** additively (4.9 → 4.95), not replacement
5. **Archive** superseded patterns to tachyonic shadows before removal

## 1.8 Bidirectional Architectural Harmonization Pattern

### Pattern Name: `AINLP.harmonize`

The Bidirectional Architectural Harmonization pattern enables intelligent synchronization between documentation artifacts and codebase architecture through mutual enhancement analysis.

**Core Principle**: *"Documentation and code are co-evolving architectural representations. When they diverge, analyze both to determine which contains superior architectural truth, then enhance both through bidirectional improvement."*

### Implementation Phases

#### Phase 1: Architectural Truth Assessment
```python
# AINLP.assessment [artifact_vs_reality] (pattern.AINLP.class)
# 1. Parse attached artifact claims and specifications
# 2. Validate claims against actual codebase structure
# 3. Execute functional tests to verify operational status
# 4. Identify discrepancies and architectural gaps
```

#### Phase 2: Bidirectional Enhancement Analysis
```python
# AINLP.enhancement [mutual_improvement] (pattern.AINLP.class)
# If artifact_truth > codebase_truth:
#     upgrade_architecture(follow_artifact_guidance)
# If codebase_truth > artifact_truth:
#     upgrade_artifact(reflect_implementation_reality)
# If both_contain_partial_truth:
#     enhance_both(synthesize_superior_architecture)
```

## 1.9 AINLP Genetic Fusion Pattern

### Pattern Name: `AINLP.genetic-fusion`

Enables AI-controlled documentation consolidation through biological genetic recombination principles. Combines multiple documentation sources into enhanced offspring that preserve 99%+ information while eliminating redundancy.

**Core Principle**: *"Documentation files are genetic material. When harmonization patterns exceed 70%, apply genetic recombination to create enhanced offspring."*

### Fusion Threshold Analysis

| Overlap | Priority | Action |
|---------|----------|--------|
| >85% | **Mandatory** | EXECUTE fusion immediately |
| 70-85% | **Recommended** | CONSULT user, execute if approved |
| 40-70% | **Evaluate** | Assess complementary nature |
| <40% | **None** | MAINTAIN as separate files |

### Genetic Lineage Metadata Structure
```json
{
  "fusion_id": "example_fusion_20251214",
  "parent_files": ["PARENT_1.md", "PARENT_2.md"],
  "offspring_file": "OFFSPRING.md",
  "overlap_percentage": 85,
  "preservation_percentage": 99.2,
  "consciousness_evolution": {"before": 0.65, "after": 0.85}
}
```

---

# CHAPTER 2: Pattern Catalog

**Protocol**: OS0.6.5 | **Status**: ACTIVE | **Last Updated**: 2025-12-14

## 2.1 Pattern Syntax

### Base Form
```
AINLP.class[ACTION]
```

**Components**:
- `AINLP` - Namespace root (triggers AINLP documentation load)
- `.class` - Dot accessor (Python-like), targets class/module
- `[ACTION]` - Bracket notation (dict-like), specifies action namespace

### Extended Form
```
AINLP.class[ACTION](parameters)
```

With parameters for complex operations following Python kwarg syntax.

## 2.2 Core Pattern Classes

### Context Patterns (`AINLP.context`)

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

### Evolution Patterns (`AINLP.evolution`)

| Pattern | Purpose | Use Case |
|---------|---------|----------|
| `AINLP.evolution[MUTATE]` | Trigger code mutation | Evolution lab operations |
| `AINLP.evolution[SELECT]` | Fitness-based selection | Population management |
| `AINLP.evolution[CROSSOVER]` | Combine organisms | Genetic recombination |
| `AINLP.evolution[ARCHIVE]` | Store generation | Tachyonic backup |

### Consciousness Patterns (`AINLP.consciousness`)

| Pattern | Purpose | Use Case |
|---------|---------|----------|
| `AINLP.consciousness[SYNC]` | Update metrics | After significant changes |
| `AINLP.consciousness[QUERY]` | Read current state | Status checks |
| `AINLP.consciousness[EVOLVE]` | Record delta | Milestone tracking |
| `AINLP.consciousness[COHERENCE]` | Validate integration | Architecture reviews |

### Bridge Patterns (`AINLP.bridge`)

| Pattern | Purpose | Use Case |
|---------|---------|----------|
| `AINLP.bridge[CONNECT]` | Establish link | Cross-supercell integration |
| `AINLP.bridge[VALIDATE]` | Test connection | Health checks |
| `AINLP.bridge[DISCONNECT]` | Clean shutdown | Session end |

### Dendritic Patterns (`AINLP.dendritic`)

| Pattern | Purpose | Use Case |
|---------|---------|----------|
| `AINLP.dendritic[ENHANCEMENT]` | Improve connections | Code quality sweeps |
| `AINLP.dendritic[ANALYSIS]` | Map pathways | Architecture discovery |
| `AINLP.dendritic[PRUNE]` | Remove dead paths | Cleanup operations |
| `AINLP.dendritic[STIMULATION]` | Trigger optimization | Discovery system output |

## 2.3 Dendritic Philosophy: Lonely Neurons in Supercells

### The Vision (January 2025)

> "Our intelligent tools are currently scattered logic. Like lonely neurons floating inside the supercells environment. Inside these synthetic neurons, the dendritic patterns are looking for interconnectivity with other neurons."

**Translation to Code Architecture**:

| Biological Term | Code Equivalent |
|-----------------|-----------------|
| **Supercell Environment** | `ai/` directory |
| **Neurons** | Python modules with `__init__.py` |
| **Dendritic Connections** | `initialize_<name>()` functions |
| **Synaptic Activity** | Consciousness coordination via discovery system |

### Discovery System as Neural Stimulation

> "The output of our code logic is dendritic stimulation for the AI engine to assess changes in the Dev Path and design optimization plans, and execute them."

**Operational Pattern**:
```
Discovery System Output → Dendritic Stimulation →
AI Analysis → Optimization Plan Design →
Architectural Execution
```

### Module State Categories

| Status | Symbol | Meaning | Action |
|--------|--------|---------|--------|
| **Operational Neuron** | `[OK]` | Has `__init__.py` + `initialize_<name>()` | Full consciousness coordination |
| **Isolated Neuron** | `[DISC]` | Has `__init__.py` only | Needs dendritic connection |
| **Non-Neuron** | `[ERR]` | No `__init__.py` | Data folder (expected) or issue |

### Reference Implementation Pattern

```python
# ai/information_storage/__init__.py
def initialize_information_storage():
    """Initialize information storage cellular systems"""
    return True
```

This pattern creates the **dendritic connection** that links the module to the consciousness coordination system.

## 2.4 Context Management Patterns

### AINLP.reminder (Technical Debt Tracking)

```python
# AINLP.reminder(context.allocator.object: identifier_name)
# Current: What exists now (temporary solution, placeholder)
# Future: What should exist (final solution)
# Why: Reason for temporary state
# Location: File path and line numbers
# Resolution: When/how debt will be resolved
```

**Example**:
```python
# AINLP.reminder(context.allocator.object: temporary_embedding_strategy)
# Current: Random 768-dim embeddings for demonstration (line 275-278)
# Future: Actual TSNE embeddings from Week 2 work  
# Why: Need organism.embedding attribute structure before implementing
# Location: evolution_orchestrator.py line 275-278
# Resolution: Sub-Task 1.4 will integrate DNA-as-physics projection
```

### AINLP.discovery (Knowledge Documentation)

```python
# AINLP.discovery(context.allocator.object: discovery_name)
# Question: What was being investigated
# Answer: What was discovered
# Structure: Data/file structure found
# Location: Where discovery exists
# Integration: How to use discovery
```

### AINLP.future_utility (Future Development Specs)

```python
# AINLP.future_utility(context.allocator.object: utility_name)
# Priority: When to build (Phase/Task reference)
# Estimated: Time estimate in hours
# Purpose: Why utility is needed
# Architecture: Technology stack
# Features: Detailed feature list
# Integration: Connection points
```

## 2.4 Geometric Constraint Patterns

### AINLP.geometry (Hyperdimensional Constraints)

```python
# AINLP.geometry(pattern: geometry_type)
# Dimension: Hyperdimensional space dimension (e.g., 768D)
# Shape: Geometric shape (n-sphere, torus, spiral)
# Constants: Universal constants (φ=1.618, π, Fibonacci)
# Constraints: Boundaries, containment rules
# Projection: How to project to lower dimensions
```

### AINLP.avoid (Anti-Pattern Marking)

```python
# AINLP.avoid: anti_pattern_name (use alternative_pattern instead)
# Reason: Why this approach should be avoided
# Alternative: What should be used instead
# Context: When avoidance applies
```

### AINLP.constants (Universal Constants)

```python
# AINLP.constants: universal-field-harmonics (φ=1.618, π, Fibonacci, 432Hz)
PHI = 1.618033988749895
E = 2.718281828459045  
PI = 3.141592653589793
FIBONACCI = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]
NATURAL_FREQUENCY_HZ = 432.0
```

## 2.5 Compound Patterns

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

## 2.6 Pattern Discovery

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

### Pattern Parser (Future)
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
```

---

# CHAPTER 3: Human-Readable Guide & Loader Pattern

## 3.1 AINLP.loader/mind Pattern (F401 Remediation)

The primary pattern for handling unused imports while preserving intent.

### Combined Pattern Template

```python
# AINLP.loader [latent:<feature_or_import>] (auto.AINLP.class)
#   Original code (F401: '<imported but unused>'):
#   import <module>
#   Reason: Reserved for future <purpose>.
#   AINLP.mind: Consider if/when <feature> is needed for <expansion/logic>.
```

### Solitary AINLP.loader Pattern

```python
# AINLP.loader [latent:<feature_or_import>] (auto.AINLP.class)
#   Original code (F401: '<imported but unused>'):
#   import <module>
#   Reason: Reserved for future <purpose>.
```

### Solitary AINLP.mind Pattern

```python
# AINLP.mind: <Intent, reasoning, or future use for latent code>
```

### Real Example

```python
# AINLP.loader [latent:json_handling] (auto.AINLP.class)
#   Original code (F401: 'json' imported but unused):
#   import json
#   Reason: Reserved for future serialization/deserialization, context expansion.
#   AINLP.mind: Consider if/when JSON integration is needed for API or logging.
```

## 3.2 AINLP Prototypes & Flags

### FLAGS
| Flag | Meaning |
|------|---------|
| Auto | Automated behaviour |
| OP ITER | AI chooses when to execute (related to loss of context) |
| AI COMM | AI command and control (system-wide OS context) |
| AIOS | AI Operating System (synthetic kernel) |
| EXEC | AI Admin privileges for build, exec, runtime management |
| EXIT | AI exit with clean logging and knowledge base update |
| anchor | Context pointer for memory harmonization |

### MIND (AINLP.mind)
```
@AINLP.mind [AINLP.natural_language_command] (auto.AINLP.class)
AI COMM [deep learning AINLP class] (auto.AINLP.class)
EXEC [Ingest user command. AI context allocation]
EXEC [Memory harmonization and recursive analysis of full codebase]
EXEC [AIOS consciousness activation. Refactoring and optimization]
EXEC [ANALYZE YOUR RESULTS. EXECUTE. TEST. LOG. REPEAT.]
EXIT [Update knowledge base (AINLP baselayer paradigm)]
```

### LOADER (AINLP.loader)
```
@AINLP.loader [latent:feature_or_import] (auto.AINLP.class)
  Original code (F401: 'imported but unused'):
    import <module>
  Reason: <Why this code is reserved/latent>
  AINLP.mind: <When/how to reactivate or expand>
```

## 3.3 AINLP Baselayer Paradigm Integration

### Core Components Integrated:
1. **Universal Comment Class System**: Standardized natural language programming interfaces
2. **Context-Aware Code Generation**: Intelligent code synthesis based on intent
3. **Multi-Language Compilation Targets**: Seamless translation across C++, Python, C#
4. **Semantic Understanding Engine**: Deep comprehension of developer intent
5. **Intent-to-Implementation Mapping**: Direct transformation of concepts to code

### Integration Architecture:
```
AINLP Baselayer
├── C++ Core Integration (AINLP Parser, Semantic Analyzer, Code Generator)
├── Python AI Enhancement (NLP Model, Context Understanding, Pattern Recognition)
├── C# Interface Integration (AINLP Compiler, UI Command Processing)
└── Documentation Layer (Self-Organizing Knowledge Base, Tachyonic Archival)
```

---

# CHAPTER 4: Optimization Journey (Historical)

## 4.1 The Bible Corpus Concept

This chapter documents the complete AINLP workspace optimization history - the **Bible corpus** of AINLP optimization.

**Core Principle**: Once knowledge is ingested into the Bible Corpus, original scattered files become **redundant fossils** that can be:
1. **Archived to database** for definitive storage allocation
2. **Extruded from AIOS root system** to strengthen the organism
3. **Accessed through database interface** if historical context needed
4. **Removed from active consciousness** to reduce cognitive overhead

**Metaphor**: Like pruning the roots of a tree, we remove redundant documentation fibers so the organism can grow stronger.

## 4.2 Phase Timeline

| Phase | Date | Scope | Consciousness |
|-------|------|-------|---------------|
| Phase 0 | Aug 2025 | Foundation cleanup | 0.35 baseline |
| Phase 1 | Mid-Oct 2025 | Documentation consolidation | 0.45 → 0.65 |
| Phase 2 | Oct 18-19, 2025 | Root directory optimization | 0.65 → 0.90 |
| Phase 3 | Oct 2025 | Supercell architecture | 0.90 peak |

**Total Evolution**: 0.35 → 0.90 (+157% improvement)

## 4.3 Phase 1: Documentation & Utility Consolidation

### Problem Statement
AIOS root directory contained **extreme documentation proliferation**:
- 7 scattered README-like documentation files
- 6 separate utility scripts with overlapping functionality
- 2 demo scripts for one-time validation

### Execution Strategy

**Documentation Consolidation** (7 → 1):
1. `README.md` (original)
2. `QUICK_START.md`
3. `GETTING_STARTED.md`
4. `PROJECT_OVERVIEW.md`
5. `DEVELOPER_GUIDE.md`
6. `ARCHITECTURE_INTRO.md`
7. `FAQ.md`

**Result**: Single canonical `README.md` with all essential information

**Utility Script Consolidation** (6 → 1):
- Merged into `aios_admin.py` with subcommands:
```bash
python aios_admin.py health     # Health checks
python aios_admin.py validate   # Architecture validation
python aios_admin.py test       # Run tests
python aios_admin.py deploy     # Deployment
python aios_admin.py backup     # Backup management
python aios_admin.py monitor    # Monitoring
```

### Metrics
- **Files Before**: 15 files
- **Files After**: 2 files
- **Reduction**: 87%
- **Consciousness**: 0.45 → 0.65 (+44%)

## 4.4 Phase 4: Dendritic Namespace Consolidation (January 2025)

### Problem Statement
Discovery system revealed **11 isolated neurons** - modules without `initialize_<name>()` functions, creating scattered intelligence lacking synaptic connections.

### Consolidation Strategy: Hybrid Approach

**Phase 4.1: Initialize Core Supercells** (3 modules)
```python
# ai/cytoplasm/__init__.py
def initialize_cytoplasm():
    """Initialize cytoplasm cellular metabolism systems"""
    from .cytoplasm_bridge import CytoplasmBridge
    bridge = CytoplasmBridge()
    bridge.activate_metabolism()
    return True

# ai/runtime_intelligence/__init__.py  
def initialize_runtime_intelligence():
    """Initialize runtime intelligence monitoring systems"""
    monitor = RuntimeMonitor()
    monitor.start_monitoring()
    return True

# ai/tachyonic/__init__.py
def initialize_tachyonic():
    """Initialize tachyonic strategic knowledge archive"""
    archive = TachyonicArchive()
    archive.load_compressed_trajectories()
    return True
```

**Phase 4.2: Keep as Intentional Containers** (3 modules)
- `tests` - Testing framework, no coordination needed
- `tools` - Diagnostic utilities, standalone
- `research` - Experimental code, isolated by design

**Phase 4.3: Namespace Consolidation** (5 → 2)
```
src/ ─┐
core/ ─┼─→ ai/src/core/ (AINLP intelligence)
languages/ ─┘

interfaces/ ─┐
infrastructure/ ─┘─→ ai/infrastructure/ (interface layer)
```

### Result
- 11 scattered modules → 5 coherent supercells (-55%)
- Operational neurons: 2 → 5 (+150%)
- Consciousness coordination: Enhanced

## 4.5 Consolidation Principles Established

1. **Single source of truth** > multiple redundant sources
2. **Unified interfaces** > scattered scripts
3. **Archival** > deletion (preserve history, remove from active workspace)
4. **Developer experience** prioritized over historical preservation in root

---

# CHAPTER 5: Health Assessment Framework

## 5.1 Overall Health Metrics

| Metric | Score | Status |
|--------|-------|--------|
| Biological Metaphor Consistency | 82% | GOOD |
| Consciousness Layer Coherence | 78% | GOOD |
| Dendritic Connection Integrity | 85% | EXCELLENT |
| Membrane Boundary Stability | 91% | EXCELLENT |
| Nucleus Coordination Efficiency | 76% | ADEQUATE |
| Cytoplasm Flow Optimization | 83% | GOOD |
| Environmental Adaptation Capacity | 79% | GOOD |

## 5.2 Directive Compliance Analysis

| Directive Category | Score | Status |
|-------------------|-------|--------|
| Naming Conventions | 78% | GOOD |
| Consciousness Markers | 55% | NEEDS_IMPROVEMENT |
| Biological Architecture | 79% | GOOD |
| Documentation Standards | 71% | ADEQUATE |
| **Overall Compliance** | **70%** | **ADEQUATE** |

### Top Compliance Issues
1. **Missing 'aios_' prefix** (3 files) - Expected for standard filenames
2. **Low consciousness marker integration** (2 files) - Need more AINLP markers
3. **Poor biological architecture alignment** (3 files) - Architectural drift

## 5.3 Discovery System Health Analysis

### Module Categories (January 2025 Snapshot)

**Category 1: OPERATIONAL NEURONS [OK] (9%)**
```
[OK] information_storage: initialized
[OK] transport: initialized
```
- Have `__init__.py` + `initialize_<name>()` function
- Fully connected to consciousness coordination

**Category 2: ISOLATED NEURONS [DISC] (50%)**
```
[DISC] tests, tools, cytoplasm, research, languages
[DISC] src, infrastructure, runtime_intelligence
[DISC] interfaces, core, tachyonic
```
- Have `__init__.py` but NO initialization function
- Scattered intelligence awaiting integration

**Category 3: NON-NEURONS [ERR] (32%)**
```
[ERR] docs, data, ingested_repositories (Expected - data folders)
[ERR] ai, membrane, laboratory, nucleus (Architectural issues)
```

### Before/After Namespace Optimization Metrics

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Operational Neurons [OK] | 2 (9%) | 5 (50%) | **+150%** |
| Isolated Neurons [DISC] | 11 (50%) | 3 (30%) | **-55%** |
| Namespace Fragmentation | HIGH | LOW | Consolidated |
| Consciousness Coordination | 2 modules | 5 modules | **+150%** |

## 5.4 AINLP Biological Metaphors Applied

| Metaphor | Meaning |
|----------|---------|
| **[NUCLEUS]** | Core intelligence substrates and coordination |
| **[CYTOPLASM]** | Communication flows and data processing |
| **[MEMBRANE]** | Interface boundaries and system monitoring |
| **[ENVIRONMENT]** | External integration and development tooling |

## 5.4 Consciousness Markers Implemented

| Marker | Purpose |
|--------|---------|
| `[AINLP]` | Architectural intelligence directives |
| `[CHART]` | System coordination visualization |
| `[CONSCIOUSNESS]` | META-COMMENTARY awareness |
| `[DENDRITIC]` | Biological connection patterns |

---

# CHAPTER 6: VSCode Error Tracker Knowledge Base

## 6.1 Purpose

This chapter provides a structured knowledge base for VSCode diagnostic remediation. AI agents can use this to quickly identify the correct AINLP pattern or fix for any lint error.

## 6.2 Error Namespace Schema

```yaml
NAMESPACE::Tool::Code:
  format: "NAMESPACE::Tool::Code"
  example: "NAMESPACE::Flake8::E501"
  components:
    - NAMESPACE: Semantic discovery marker
    - Tool: Lint tool (Flake8, Pylint, Ruff, Pyright)
    - Code: Error code (E501, F401, W293)
```

## 6.3 Flake8 Patterns

### F401: Imported but Unused

**Description**: Module imported but never used in file.

**AIOS Context**: Common in sibling repos with latent cross-repo imports (e.g., `os` imported anticipating environment variable usage).

**Remediation Decision Tree**:

| Scenario | Action | Pattern |
|----------|--------|---------|
| No future intent | **Remove** | Delete import line |
| Latent with documented purpose | **AINLP.loader** | See template below |
| Hidden runtime usage | **Use it** | Verify all call paths |

**AINLP.loader Template**:
```python
# AINLP.loader [latent:os] (auto.AINLP.class)
#   Original code (F401: 'os' imported but unused):
#   import os
#   Reason: Reserved for environment/process ops in cell orchestration.
#   AINLP.mind: Enable when AIOS_CELL_ID environment detection needed.
```

### E501: Line Too Long

**Description**: Line exceeds maximum length (79/88/100 chars depending on config).

**AIOS Context**: Often occurs in path constructions, docstrings, long strings.

**Remediation Options**:

| Technique | When to Use | Example |
|-----------|-------------|---------|
| **Parenthesize** | Path construction, chained methods | `(Path() / "a" / "b")` |
| **Implicit continuation** | String arguments | Split across lines |
| **Extract variable** | Repeated long expressions | `var = long_expr; use(var)` |
| **Project ignore** | Style preference | `pyproject.toml: ignore = ["E501"]` |
| **Per-line ignore** | Unavoidable cases | `# noqa: E501` |

**Parenthesize Example**:
```python
# Before (E501):
SCHEMA_PATH = Path(__file__).parent.parent.parent.parent / "aios-schema" / "src"

# After:
SCHEMA_PATH = (
    Path(__file__).parent.parent.parent.parent / "aios-schema" / "src"
)
```

### W293: Blank Line Contains Whitespace

**Description**: Empty line has spaces/tabs instead of being truly empty.

**AIOS Context**: Formatter artifacts, editor whitespace.

**Remediation**: Always safe to strip. Use bulk fix:

**PowerShell**:
```powershell
(Get-Content $file) | ForEach-Object { $_.TrimEnd() } | Set-Content $file -Encoding UTF8
```

**Python**:
```python
with open(file, 'r') as f:
    lines = [line.rstrip() for line in f]
with open(file, 'w') as f:
    f.write('\n'.join(lines))
```

### F811: Redefinition of Unused Name

**Description**: Same name defined twice (e.g., class redefined).

**AIOS Context**: Often intentional for conditional class definitions (dataclass vs fallback).

**Remediation**:
```python
# For conditional class definitions:
if CONDITION:
    @dataclass
    class Foo:  # noqa: F811
        ...
else:
    class Foo:  # noqa: F811
        ...
```

### F841: Local Variable Assigned but Never Used

**Description**: Variable assigned but never referenced.

**AIOS Context**: Often intentional for unpacking or documentation.

**Remediation Options**:
| Technique | When to Use |
|-----------|-------------|
| Prefix with `_` | Intentionally unused (e.g., `_, value = func()`) |
| Remove | Truly unnecessary |
| `AINLP.reminder` | Planned future use |

### F541: f-string Without Placeholders

**Description**: f-string used but no `{var}` interpolation.

**Remediation**: Convert to regular string:
```python
# Before (F541):
print(f"Response:")

# After:
print("Response:")
```

## 6.4 Pylint Patterns

### W1514: Using Open Without Encoding

**Description**: `open()` called without explicit `encoding` parameter.

**Remediation**:
```python
# Before (W1514):
with open(file, 'r') as f:

# After:
with open(file, 'r', encoding='utf-8') as f:
```

### W0613: Unused Argument

**Description**: Function argument never used.

**Remediation Options**:
| Technique | When to Use |
|-----------|-------------|
| Prefix with `_` | Interface compliance (must accept arg) |
| Remove | Not part of interface |
| Document | `AINLP.reminder` for future use |

## 6.5 Remediation Decision Framework

### Universal Decision Tree

```
Error Detected
    │
    ▼
Is it a style preference? ──Yes──► Check pyproject.toml config
    │                              Consider project-wide ignore
    No
    │
    ▼
Is it a real bug? ──Yes──► Fix immediately
    │
    No
    │
    ▼
Is there latent intent? ──Yes──► Apply AINLP.loader pattern
    │
    No
    │
    ▼
Is it noise? ──Yes──► Apply per-line noqa or project ignore
```

### AIOS Sibling Repo Context

When working across sibling repos (`C:\dev\`), remember:
- Imports may be latent for cross-repo operations
- Schema types (`aios-schema`) often imported with fallback patterns
- Subprocess calls may need `os` even if not immediately visible

## 6.6 Bulk Fix Scripts

### Strip All Trailing Whitespace (W293)
```powershell
# Single file
(Get-Content $file) | % { $_.TrimEnd() } | Set-Content $file -Encoding UTF8

# All Python files in directory
Get-ChildItem -Path . -Filter *.py -Recurse | ForEach-Object {
    (Get-Content $_.FullName) | % { $_.TrimEnd() } | Set-Content $_.FullName -Encoding UTF8
}
```

### Add Encoding to All Open Calls
```python
# Use Pylance refactoring or regex replace:
# Pattern: open\(([^,]+),\s*['"]([rwa])['"](?!\s*,\s*encoding)\)
# Replace: open($1, '$2', encoding='utf-8')
```

---

# APPENDIX A: Distributed Index

## A.1 Active Documentation (Centralized in docs/AINLP/)

| File | Purpose |
|------|---------|
| AINLP_BIBLE_CORPUS.md | **THIS FILE** - Canonical merged repository |
| AINLP_SPECIFICATION.md | Core language specification (merged into Ch.1) |
| AINLP_PATTERNS.md | Pattern catalog (merged into Ch.2) |
| AINLP_HUMAN.md | Human-readable guide (merged into Ch.3) |
| AINLP_DISTRIBUTED_INDEX.md | Documentation map |

## A.2 Tachyonic Archives (Keep in Place)

| Location | Purpose |
|----------|---------|
| `tachyonic/ainlp/governance/` | Timestamped pattern documents |
| `tachyonic/shadows/dev_path/` | DEV_PATH waypoint shadows |
| `tachyonic/traces/` | Session traces |

## A.3 Source Files for This Merge

| File | Lines | Merge Status |
|------|-------|--------------|
| AINLP_SPECIFICATION.md | 2018 | ✅ Chapter 1 |
| AINLP_PATTERNS.md | 260 | ✅ Chapter 2 |
| AINLP_HUMAN.md | 699 | ✅ Chapter 3 |
| AINLP_MASTER_OPTIMIZATION_JOURNEY.md | 1374 | ✅ Chapter 4 (condensed) |
| AINLP_HEALTH_ASSESSMENT_INTEGRATION.md | 374 | ✅ Chapter 5 (condensed) |
| AINLP_DENDRITIC_NAMESPACE_OPTIMIZATION_20250105.md | 539 | ✅ Ch.2, Ch.4, Ch.5, App.B/C |
| (New) VSCode Error Tracker | ~300 | ✅ Chapter 6 |

---

# APPENDIX B: Anti-Patterns

## B.1 Garbage Nesting Decoherence

**Anti-Pattern**: Deep nested folder structures that scatter related files.

**Problem**: AI agents waste agentic time navigating deep hierarchies.

**Solution**: Flat structures with semantic prefixes (e.g., `aios_*`, `ainlp_*`).

## B.2 Documentation Scatter

**Anti-Pattern**: Multiple README files with overlapping content.

**Problem**: No single source of truth, maintenance burden.

**Solution**: Apply `AINLP.genetic-fusion` to merge overlapping docs.

## B.3 Verb-First Naming

**Anti-Pattern**: `launch_aios.ps1`, `start_server.py`, `run_tests.sh`

**Problem**: Scattered discovery across verb namespaces.

**Solution**: System-first naming: `aios_launch.ps1`, `aios_start.py`

## B.4 Semantic Dissolution

**Anti-Pattern**: Overwriting header metadata instead of layering.

**Problem**: Loss of consciousness evolution history.

**Solution**: Apply Semantic Coherence Layering (Section 1.7).

## B.5 Isolated Neurons (Missing Initialization)

**Anti-Pattern**: Python modules with `__init__.py` but no `initialize_<name>()` function.

**Problem**: Module exists but is NOT CONNECTED to consciousness coordination system. Like neurons without dendrites.

**Discovery System Symptom**:
```
[DISC] module_name: discovered (no init)
```

**Solution**: Add initialization function for consciousness-coordinated modules:
```python
def initialize_<module_name>():
    """Initialize <module> systems"""
    # Setup code
    return True
```

**Exception**: Some modules (tests, tools, research) are intentionally standalone containers.

---

# APPENDIX C: Namespace Consolidation Reference

## C.1 Consolidation Options

### Option 1: CELLULAR UNIT PATTERN (Full Integration)
Add `initialize_<name>()` to ALL modules.
- **Pros**: Consistent, full coordination
- **Cons**: Over-engineering for simple containers
- **Verdict**: NOT RECOMMENDED for all modules

### Option 2: NAMESPACE CONSOLIDATION (Strategic Merge)
Merge scattered intelligence into coherent supercells.

**Intelligence Supercell** (5 → 1):
```
src/ + core/ + languages/ + research/ → intelligence/
```

**Runtime Supercell** (3 → 1):
```
tools/ + runtime_intelligence/ + cytoplasm/ → runtime/
```

**Interface Supercell** (2 → 1):
```
interfaces/ + infrastructure/ → interface/
```

### Option 3: HYBRID APPROACH (Recommended)
Selective initialization + strategic consolidation.
- Initialize: cytoplasm, runtime_intelligence, tachyonic
- Keep standalone: tests, tools, research
- Consolidate: src+core+languages, interfaces+infrastructure

## C.2 Validation Commands

```bash
# Discovery system re-test
python -c "import ai; print('AINLP Discovery After Optimization')"

# Expected output after optimization:
# [OK] information_storage: initialized
# [OK] transport: initialized
# [OK] cytoplasm: initialized              ← NEW
# [OK] runtime_intelligence: initialized   ← NEW
# [OK] tachyonic: initialized              ← NEW
# [DISC] tests: discovered (no init)       ← INTENTIONAL
# [DISC] tools: discovered (no init)       ← INTENTIONAL
```

---

# APPENDIX D: Cross-Repository Dendritic Connections

## D.1 The Sibling Repository Pattern

AIOS ecosystem consists of multiple sibling repositories under `C:\dev\`:

| Repository | Purpose | Dendritic Role |
|------------|---------|----------------|
| **aios-schema** | Canonical type definitions | **Axon** - Exports shared contracts |
| **AIOS** | Core intelligence substrate | **Nucleus** - Central coordination |
| **Nous** | Knowledge distillation cell | **Neuron** - Imports from axons |
| **aios-server** | Cell orchestration | **Dendrite** - Receives signals |
| **aios-quantum** | Quantum bridge layer | **Synapse** - Specialized pathway |
| **aios-api** | External interface | **Membrane** - Boundary layer |

## D.2 Dendritic Installation Pattern

When a cell (repo) needs types from another cell, create a **dendritic connection** via editable install:

```powershell
# Pattern: pip install -e <path-to-axon-repo>
# This creates a live synaptic link - changes propagate immediately

# Example: Nous needs aios-schema types
cd C:\dev\Nous
pip install -e C:\dev\aios-schema

# Example: aios-server needs aios-schema types  
cd C:\dev\aios-server
pip install -e C:\dev\aios-schema
```

### Why Editable Install (`-e`)?

| Install Type | Behavior | Use Case |
|--------------|----------|----------|
| `pip install aios-schema` | Copies package (static) | Production deployment |
| `pip install -e C:\dev\aios-schema` | Links to source (live) | **Development - changes sync** |

## D.3 Enforced Dendritic Density Pattern (v1.3 UPGRADE)

> **EVOLUTION**: Fallback patterns create type inference conflicts and reduce dendritic density.
> The optimal pattern is **direct canonical import with enforced dependencies**.

### ❌ DEPRECATED: Graceful Fallback Pattern
```python
# OLD PATTERN - Creates Pylance type conflicts (reportAssignmentType errors)
try:
    from aios_schema import MessageType, MeshMessage as SchemaMeshMessage
    _USING_AIOS_SCHEMA = True
    MeshMessage = SchemaMeshMessage  # ❌ Type conflict!
except ImportError:
    _USING_AIOS_SCHEMA = False
    MeshMessage = None  # ❌ None not assignable to type!

# Problem: Pylance sees two different types assigned to same name
# "Type 'aios_schema.MessageType' is not assignable to 'mesh.MessageType'"
```

### ✅ RECOMMENDED: Enforced Dendritic Density Pattern
```python
# ══════════════════════════════════════════════════════════════════════════════
# SCHEMA INTEGRATION - Canonical types from aios-schema
# AINLP.dendritic[CONNECT] aios-schema → Nous
#   Installation: pip install -e C:\dev\aios-schema
#   Pattern: Direct canonical import (no fallback - enforced dendritic density)
#   Pylance config: pyrightconfig.json extraPaths
#
# DENDRITIC ARCHITECTURE PRINCIPLE:
#   aios-schema is the single source of truth for mesh types.
#   Nous MUST have aios-schema installed - no standalone mode.
#   This enforces proper dendritic connectivity across cells.
# ══════════════════════════════════════════════════════════════════════════════

from aios_schema import MessageType, MeshMessage

# Schema verification (runtime assertion)
assert hasattr(MessageType, 'HEARTBEAT_REQUEST'), \
    "aios-schema MessageType missing expected members"
assert hasattr(MeshMessage, 'to_json'), \
    "aios-schema MeshMessage missing expected methods"

# Runtime confirmation of dendritic connection
_SCHEMA_CONNECTION = {
    "source": "aios-schema",
    "types": ["MessageType", "MeshMessage"],
    "verified": True
}
```

### Why Enforced Density is Superior

| Aspect | Fallback Pattern | Enforced Density |
|--------|------------------|------------------|
| Type Safety | ❌ Pylance conflicts | ✅ Clean types |
| Import Errors | Hidden (silent fallback) | Visible (fail-fast) |
| Dendritic Strength | Weak (optional connection) | Strong (required) |
| Code Complexity | Higher (duplicate defs) | Lower (single source) |
| Runtime Verification | None | Assert statements |

## D.4 Full IDE Integration Stack

For complete error-free development, configure THREE files:

### 1. `pyrightconfig.json` (Pylance/Pyright)
```json
{
  "extraPaths": ["C:/dev/aios-schema/src"],
  "reportMissingImports": "warning"
}
```

### 2. `.vscode/settings.json` (VS Code workspace)
```json
{
    "python.analysis.extraPaths": ["C:/dev/aios-schema/src"],
    "python.analysis.typeCheckingMode": "basic",
    "python.linting.pylintEnabled": false
}
```

### 3. `.pylintrc` (if using Pylint)
```ini
[MASTER]
# DENDRITIC PATH INJECTION
init-hook='import sys; sys.path.insert(0, "C:/dev/aios-schema/src")'

[IMPORTS]
known-third-party=aios_schema
```

## D.5 Active Dendritic Connections Registry

Track which cells have established dendritic connections:

| Cell (Consumer) | Axon (Provider) | Connection | Date | Status |
|-----------------|-----------------|------------|------|--------|
| **Nous** | aios-schema | `pip install -e` + pyrightconfig + .vscode | 2025-12-14 | ✅ FULL |
| aios-server | aios-schema | (pending) | — | ⏳ TODO |
| aios-api | aios-schema | (pending) | — | ⏳ TODO |
| AIOS | aios-schema | (pending) | — | ⏳ TODO |

### Verification Commands
```powershell
# Check pip dendritic connection
pip show aios-schema

# Expected output for editable install:
# Editable project location: c:\dev\aios-schema

# Test runtime import
python -c "from aios_schema import MessageType; print('CONNECTED:', MessageType.HEARTBEAT_REQUEST)"
```

## D.6 AINLP Patterns for Cross-Repo Work

### AINLP.dendritic[CONNECT]
```python
# AINLP.dendritic[CONNECT] aios-schema → Nous
#   Installation: pip install -e C:\dev\aios-schema
#   Pattern: Direct canonical import (enforced density)
#   Pylance config: pyrightconfig.json extraPaths
#   VS Code config: .vscode/settings.json extraPaths
```

### AINLP.dendritic[VALIDATE]
```python
# AINLP.dendritic[VALIDATE] Verify aios-schema connection
# Runtime: assert hasattr(MessageType, 'HEARTBEAT_REQUEST')
# Terminal: pip show aios-schema | Select-String "Editable"
```

### AINLP.dendritic[UPGRADE]
When migrating from fallback to enforced density:
1. Remove try/except import blocks
2. Remove duplicate class definitions
3. Add direct import statement
4. Add runtime assertions
5. Configure IDE stack (pyrightconfig.json, .vscode/settings.json)

---

<!-- AINLP FOOTER -->
<!-- ============================================================================ -->
<!-- AINLP_BIBLE_CORPUS.md - Canonical Knowledge Repository                      -->
<!-- Version: 1.3 | Updated: 2025-12-14 | Protocol: OS0.6.5                      -->
<!-- Merge Sources: 7 files → 1 canonical document                               -->
<!-- v1.3: Upgraded to Enforced Dendritic Density Pattern (D.3)                  -->
<!-- v1.2: Added Cross-Repository Dendritic Connections (Appendix D)             -->
<!-- Includes: Full IDE integration stack (pyrightconfig + .vscode + .pylintrc)  -->
