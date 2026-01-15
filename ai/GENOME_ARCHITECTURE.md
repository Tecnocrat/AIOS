<!-- ============================================================================ -->
<!-- AINLP HEADER - GENOME ARCHITECTURE SPECIFICATION                             -->
<!-- ============================================================================ -->
<!-- Document: GENOME_ARCHITECTURE.md - ai/ Directory Classification              -->
<!-- Location: /ai/GENOME_ARCHITECTURE.md (canonical)                             -->
<!-- Purpose: Define dendritic organization of AIOS AI subsystem                  -->
<!-- Phase: 31.9.6 (Agentic Architecture)                                        -->
<!-- Created: January 14, 2026 | Updated: January 15, 2026                       -->
<!-- AINLP Protocol: OS0.7.2                                                      -->
<!-- ============================================================================ -->

# 🧬 AIOS Genome Architecture Specification

**Phase**: 31.9.6 (Agentic Architecture)  
**Date**: January 15, 2026  
**Status**: ✅ IMPLEMENTED

---

## 📊 Consolidation Complete

### Before vs After

| Metric | Before | After | Reduction |
|--------|--------|-------|-----------|
| Root directories | 29 | 9 | -69% |
| Category clarity | Low | High | ✅ |
| Duplicate concepts | Multiple | 0 | ✅ |

### Current Structure (Implemented)

| Directory | Files | Category | Contents |
|-----------|-------|----------|----------|
| `nucleus/` | 118 | **NUCLEUS** | Core intelligence, agents, consciousness |
| `src/` | 177 | **NUCLEUS** | Source implementations (pending merge) |
| `cytoplasm/` | 267 | **CYTOPLASM** | Runtime, bridges, infrastructure |
| `membrane/` | 58 | **MEMBRANE** | MCP, protocols, transport, integrations |
| `organelles/` | 68 | **ORGANELLES** | Orchestration, security, coordination |
| `research/` | 111 | **RESEARCH** | Demos, ingestion, paradigm |
| `tools/` | 265 | **TOOLS** | Utilities, tests, data |
| `docs/` | 534 | **DOCS** | Documentation |
| `tachyonic/` | 19 | **TACHYONIC** | Archive interface |

---

## 🎯 Implemented Dendritic Structure

```
ai/
├── 📁 nucleus/                  # 🧬 CORE INTELLIGENCE (118 files)
│   ├── agents/                  # Agent definitions & behaviors  
│   ├── consciousness/           # Consciousness engine
│   ├── engines/                 # Processing engines (evolution, emergence)
│   ├── core/                    # Core utilities
│   ├── src/                     # Source implementations
│   ├── interfaces/              # Internal interfaces
│   ├── compression/             # Data compression
│   ├── optimization/            # Performance optimization
│   ├── models.py                # Core models
│   ├── sequencer.py             # Processing sequencer
│   └── nucleus_intelligence.py  # Main intelligence hub
│
├── 📁 cytoplasm/                # 🔬 RUNTIME ENVIRONMENT
│   ├── bridges/                 # External system bridges
│   ├── runtime/                 # Runtime components
│   ├── infrastructure/          # Infrastructure services
│   ├── monitoring/              # Runtime monitoring
│   └── cytoplasm_bridge.py      # Main bridge
│
├── 📁 membrane/                 # 🛡️ BOUNDARY INTERFACES
│   ├── mcp_server/              # MCP protocol handler
│   ├── protocols/               # AICP, communication protocols
│   ├── transport/               # Transport layer
│   ├── integrations/            # External integrations
│   └── communication/           # Messaging subsystem
│
├── 📁 organelles/               # 🔧 SPECIALIZED SERVICES
│   ├── orchestration/           # Multi-agent coordination
│   ├── security/                # Security subsystem
│   ├── information_storage/     # Data persistence
│   ├── supercells/              # Supercell definitions
│   └── coordination/            # Agent coordination
│
├── 📁 research/                 # 🧪 EXPERIMENTAL
│   ├── laboratory_intelligence.py
│   ├── paradigm/                # Paradigm research
│   ├── demos/                   # Demo applications
│   ├── tests/                   # Research test suites
│   └── scripts/                 # Research scripts
│
├── 📁 tools/                    # 🔨 UTILITIES
│   ├── architecture/            # Architecture tools
│   ├── consciousness/           # Consciousness tools
│   ├── ingestion/               # Data ingestion
│   ├── database/                # Database utilities
│   ├── visual/                  # Visualization tools
│   ├── mesh/                    # Mesh network tools
│   └── tests/                   # Test suites
│
├── 📁 tachyonic/                # 🌌 ARCHIVE INTERFACE
│   └── shadows/                 # Knowledge shadows
│
├── 📁 docs/                     # 📚 DOCUMENTATION
│   └── ...                      # All AI documentation
│
├── 📁 data/                     # 💾 DATA FILES
│   └── ingested_repositories/   # Ingested external repos
│
├── GENOME_ARCHITECTURE.md       # This file (canonical spec)
├── ARCHITECTURAL_COHERENCE.md   # Coherence documentation
├── requirements.txt             # Python dependencies
└── __init__.py                  # Package init
```

---

## 📋 Migration Plan

### Phase 1: Safe Cleanup (No Breaking Changes)

```powershell
# Remove git artifact
Remove-Item "ai/core~HEAD" -Recurse -Force
```

### Phase 2: Merge Small Directories

```powershell
# Merge coordination → organelles/coordination
Move-Item "ai/coordination/*" "ai/organelles/coordination/" -Force

# Merge demos → research/demos  
Move-Item "ai/demos/*" "ai/research/demos/" -Force

# Merge ingested_repositories → data/
Move-Item "ai/ingested_repositories/*" "ai/data/ingested_repositories/" -Force
```

### Phase 3: Create membrane/ Consolidation

```powershell
# Create membrane directory
New-Item "ai/membrane" -ItemType Directory -Force

# Move relevant directories
Move-Item "ai/mcp_server" "ai/membrane/"
Move-Item "ai/protocols" "ai/membrane/"
Move-Item "ai/transport" "ai/membrane/"
Move-Item "ai/integrations" "ai/membrane/"
Move-Item "ai/communication" "ai/membrane/"
```

### Phase 4: Cytoplasm Consolidation

```powershell
# Move runtime-related to cytoplasm
Move-Item "ai/runtime/*" "ai/cytoplasm/runtime/" -Force
Move-Item "ai/runtime_intelligence/*" "ai/cytoplasm/monitoring/" -Force
Move-Item "ai/infrastructure/*" "ai/cytoplasm/infrastructure/" -Force
```

### Phase 5: Core to Nucleus

```powershell
# Merge core utilities into nucleus
Move-Item "ai/core/*" "ai/nucleus/core/" -Force
```

---

## 🔌 Import Path Updates

After reorganization, these imports will change:

| Old Import | New Import |
|------------|------------|
| `from ai.mcp_server import ...` | `from ai.membrane.mcp_server import ...` |
| `from ai.protocols import ...` | `from ai.membrane.protocols import ...` |
| `from ai.transport import ...` | `from ai.membrane.transport import ...` |
| `from ai.communication import ...` | `from ai.membrane.communication import ...` |
| `from ai.infrastructure import ...` | `from ai.cytoplasm.infrastructure import ...` |
| `from ai.runtime import ...` | `from ai.cytoplasm.runtime import ...` |
| `from ai.coordination import ...` | `from ai.organelles.coordination import ...` |
| `from ai.demos import ...` | `from ai.research.demos import ...` |

---

## 📊 Success Metrics

| Metric | Before | Target | Status |
|--------|--------|--------|--------|
| Root directories | 27 | 9 | ⏳ |
| Clear categorization | ❌ | ✅ | ⏳ |
| Duplicate concepts | Multiple | 0 | ⏳ |
| Import errors | 0 | 0 | ⏳ |
| pytest pass rate | 100% | 100% | ⏳ |

---

## 🧬 BIOS Contract for AI Components

All AI modules should implement this contract:

```python
# ai/membrane/mcp_server/example.py

class AIOSComponent:
    """Standard AIOS component interface."""
    
    @classmethod
    def check(cls) -> int:
        """Health probe. Return 0=healthy, 1=needs start."""
        return 0
    
    @classmethod
    def start(cls) -> int:
        """Idempotent startup. Return 0=success."""
        return 0
    
    @classmethod
    def stop(cls) -> int:
        """Graceful shutdown. Return 0=success."""
        return 0
    
    @classmethod
    def status(cls) -> dict:
        """JSON health report."""
        return {
            "component": cls.__name__,
            "status": "running",
            "healthy": True,
            "category": "membrane"  # nucleus|cytoplasm|membrane|organelles
        }
```

---

## 📝 Changelog

| Date | Version | Change |
|------|---------|--------|
| 2026-01-14 | 1.0.0 | Initial specification created |

---

*This document is the canonical specification for ai/ directory organization.*  
*Part of Phase 31.9.6 (Agentic Architecture) implementation.*
