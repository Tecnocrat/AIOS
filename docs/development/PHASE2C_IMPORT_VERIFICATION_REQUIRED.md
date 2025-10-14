# Phase 2C Import Path Update - Verification Required

**Date**: January 18, 2025  
**Status**: ⏸️ BLOCKED - Awaiting module location verification  
**Tool Enhanced**: ai/tools/update_import_paths.py (537→731 lines, +194 lines)  
**Branch**: OS0.6.2.claude (18 commits ahead of origin)

## Executive Summary

The import path updater tool has been successfully enhanced with Phase 2C support (core.* → computational_layer.*), but import updates are BLOCKED pending module location verification. The tool detected 10 files with 11 core.* imports, but analysis revealed that the referenced modules **have NOT actually migrated to computational_layer/** yet.

## Critical Discovery

**Problem**: The enhanced tool would update imports to point to `computational_layer.*`, but the actual modules are still in their original locations:

| Module | Import Statement References | Actual Location | Expected Location |
|--------|----------------------------|-----------------|-------------------|
| `consciousness_emergence_analyzer` | 3 files | `ai/src/intelligence/` | `computational_layer/` ❌ |
| `core_engine_supercell_interface` | 1 file | `tachyonic/` | `computational_layer/` ❌ |
| `library_ingestion_protocol` | 2 files | `ai/src/intelligence/` | `computational_layer/` ❌ |
| `analysis_tools` | 3 files | `core/` (C++ interface?) | `computational_layer/` ❌ |
| `integration.mcp` | 1 file | `core/` (C++ interface?) | `computational_layer/` ❌ |
| `intent_handlers` | 1 file | `core/` (C++ interface?) | `computational_layer/` ❌ |

**Impact**: Applying the suggested import changes would **break all imports** because the modules don't exist at the target locations.

## Tool Enhancement Summary

### Documentation Governance Applied
- ✅ Searched for existing import update tools (not created new file)
- ✅ Found mature `ai/tools/update_import_paths.py` (537 lines)
- ✅ Decision: EXPAND existing tool (anti-proliferation principle)
- ✅ Result: Single tool with dual-purpose (runtime + Phase 2C migrations)

### Enhancements Made (+194 lines)

#### 1. Module Mapping (PHASE2C_MODULES)
```python
PHASE2C_MODULES = {
    "assemblers": ["tree_assembler", "context_assembler", "integration_assembler", "file_assembler"],
    "bridges": ["consciousness_bridge", "analysis_bridge", "transport_bridge", "tachyonic_bridge"],
    "core_systems": ["monitors", "optimizers", "organizers"],
    "engines": ["assembly_3d_engine", "quantum_noise_engine", "spherical_geometry_engine"],
    "modules": ["comprehensive_tester", "connectivity_demo", "file_monitor_supercell"],
    "runtime_intelligence": ["evolution_monitor", "meta_evolutionary_enhancer"],
    "utilities": ["common_patterns", "shared_imports"]
}
```

#### 2. Import Detection (detect_phase2c_imports)
Detects 7 import patterns:
1. `from core.assemblers import X`
2. `from core.bridges.consciousness_bridge import Y`
3. `from core.engines import Z`
4. `import core.module_name`
5. `from core import something`
6. `from core.integration.mcp import MCPServer`
7. `from core.consciousness_emergence_analyzer import ConsciousnessEmergenceAnalyzer`

#### 3. Import Transformation (generate_phase2c_import)
- Transforms `core.*` → `computational_layer.*`
- Preserves aliases (`import X as Y`)
- Maintains import structure (from/import variations)

#### 4. File Update (update_file_phase2c)
- Phase 2C-specific file update logic
- Creates `.backup` files before modification
- Records all changes with pattern metadata
- Supports dry-run and execute modes

#### 5. CLI Enhancement
```bash
# Preview Phase 2C migrations
python ai/tools/update_import_paths.py --dry-run --phase2c

# Apply Phase 2C migrations  
python ai/tools/update_import_paths.py --execute --phase2c
```

## Detection Results (Dry-Run)

**Files Scanned**: 927 Python files  
**Files with core.* imports**: 10 files  
**Import statements detected**: 11 imports  
**Pattern detected**: `from_core_module` (all 11 imports)

### Files Requiring Updates (if modules were in computational_layer/)

1. **tachyonic/activate_tachyonic_evolution.py** (1 import)
   ```python
   # Line 37
   OLD: from core.core_engine_supercell_interface import CoreEngineSupercell
   NEW: from computational_layer.core_engine_supercell_interface import CoreEngineSupercell
   ACTUAL: Module is in tachyonic/ (not computational_layer/)
   ```

2. **tachyonic/aios_documentation_supercell_enhancer.py** (2 imports)
   ```python
   # Line 55
   OLD: from core.analysis_tools import CellularIntelligenceDiagnostic
   NEW: from computational_layer.analysis_tools import CellularIntelligenceDiagnostic
   ACTUAL: analysis_tools may be C++ interface (stays in core/)
   
   # Line 56
   OLD: from core.analysis_tools.aios_core_consciousness_monitor import ConsciousnessMonitor
   NEW: from computational_layer.analysis_tools.aios_core_consciousness_monitor import ConsciousnessMonitor
   ACTUAL: Same as above
   ```

3. **tachyonic/aios_unified_consciousness_system.py** (1 import)
   ```python
   # Line 44
   OLD: from core.analysis_tools import CellularIntelligenceDiagnostic
   NEW: from computational_layer.analysis_tools import CellularIntelligenceDiagnostic
   ACTUAL: analysis_tools may be C++ interface (stays in core/)
   ```

4. **ai/infrastructure/ui_interaction_bridge.py** (1 import)
   ```python
   # Line 23
   OLD: from core.consciousness_emergence_analyzer import ConsciousnessEmergenceAnalyzer
   NEW: from computational_layer.consciousness_emergence_analyzer import ConsciousnessEmergenceAnalyzer
   ACTUAL: Module is in ai/src/intelligence/ (not computational_layer/)
   CORRECT: from ai.src.intelligence.consciousness_emergence_analyzer import ConsciousnessEmergenceAnalyzer
   ```

5. **ai/src/engines/enhanced_visual_intelligence_engine.py** (1 import)
   ```python
   # Line 22
   OLD: from core.consciousness_emergence_analyzer import ConsciousnessEmergenceAnalyzer
   NEW: from computational_layer.consciousness_emergence_analyzer import ConsciousnessEmergenceAnalyzer
   ACTUAL: Module is in ai/src/intelligence/ (not computational_layer/)
   CORRECT: from ai.src.intelligence.consciousness_emergence_analyzer import ConsciousnessEmergenceAnalyzer
   ```

6. **ai/src/integrations/visual_ai_integration_bridge.py** (1 import)
   ```python
   # Line 17
   OLD: from core.consciousness_emergence_analyzer import ConsciousnessEmergenceAnalyzer
   NEW: from computational_layer.consciousness_emergence_analyzer import ConsciousnessEmergenceAnalyzer
   ACTUAL: Module is in ai/src/intelligence/ (not computational_layer/)
   CORRECT: from ai.src.intelligence.consciousness_emergence_analyzer import ConsciousnessEmergenceAnalyzer
   ```

7. **ai/src/intelligence/cpp_stl_ingestion_pipeline.py** (1 import)
   ```python
   # Line 39
   OLD: from core.library_ingestion_protocol import (
   NEW: from computational_layer.library_ingestion_protocol import (
   ACTUAL: Module is in ai/src/intelligence/ (not computational_layer/)
   CORRECT: from ai.src.intelligence.library_ingestion_protocol import (
   ```

8. **ai/src/parsers/cpp_documentation_parser.py** (1 import)
   ```python
   # Line 41
   OLD: from core.library_ingestion_protocol import (
   NEW: from computational_layer.library_ingestion_protocol import (
   ACTUAL: Module is in ai/src/intelligence/ (not computational_layer/)
   CORRECT: from ai.src.intelligence.library_ingestion_protocol import (
   ```

9. **ai/nucleus/src/mcp_server.py** (1 import)
   ```python
   # Line 11
   OLD: from core.integration.mcp import MCPServer, Tool
   NEW: from computational_layer.integration.mcp import MCPServer, Tool
   ACTUAL: MCP may be C++ interface (should stay in core/)
   DECISION: Verify if Python wrapper exists or if this is C++ interface
   ```

10. **ai/infrastructure/dendritic/supervisor.py** (1 import)
    ```python
    # Line 40
    OLD: from core.intent_handlers import IntentHandler
    NEW: from computational_layer.intent_handlers import IntentHandler
    ACTUAL: intent_handlers may be C++ interface (should stay in core/)
    DECISION: Verify if Python wrapper exists or if this is C++ interface
    ```

## What computational_layer/ Actually Contains

**Verified Contents**:
```
computational_layer/
├── assemblers/              ✅ Migrated Python code
│   ├── tree_assembler.py
│   ├── context_assembler.py
│   ├── integration_assembler.py
│   └── file_assembler.py
├── bridges/                 ✅ Migrated Python code
│   ├── consciousness_bridge.py
│   ├── analysis_bridge.py
│   ├── transport_bridge.py
│   └── tachyonic_bridge.py
├── core_systems/            ✅ Migrated Python code
│   ├── monitors/
│   ├── optimizers/
│   └── organizers/
├── engines/                 ✅ Migrated Python code
│   ├── assembly_3d_engine.py
│   ├── quantum_noise_engine.py
│   └── spherical_geometry_engine.py
├── modules/                 ✅ Migrated Python code
│   ├── comprehensive_tester.py
│   ├── connectivity_demo.py
│   └── file_monitor_supercell.py
├── runtime_intelligence/    ✅ Migrated Python code
│   ├── evolution_monitor.py
│   └── meta_evolutionary_enhancer.py
└── utilities/               ✅ Migrated Python code
    ├── common_patterns.py
    └── shared_imports.py
```

**NOT in computational_layer/**:
- ❌ consciousness_emergence_analyzer (actually in ai/src/intelligence/)
- ❌ core_engine_supercell_interface (actually in tachyonic/)
- ❌ library_ingestion_protocol (actually in ai/src/intelligence/)
- ❌ analysis_tools (C++ interface in core/?)
- ❌ integration.mcp (C++ interface in core/?)
- ❌ intent_handlers (C++ interface in core/?)

## Required Actions (Decision Tree)

### Decision Point 1: Module Migration Status
**Question**: Which modules should actually migrate to computational_layer/?

**Options**:
1. **Migrate missing modules** to computational_layer/:
   - consciousness_emergence_analyzer (from ai/src/intelligence/)
   - library_ingestion_protocol (from ai/src/intelligence/)
   - core_engine_supercell_interface (from tachyonic/)

2. **Leave modules in current locations** and update imports to point there:
   - consciousness_emergence_analyzer → ai.src.intelligence
   - library_ingestion_protocol → ai.src.intelligence
   - core_engine_supercell_interface → tachyonic

### Decision Point 2: C++ Interface Classification
**Question**: Which imports are C++ interfaces that should stay in core/?

**Candidates** (need verification):
- `core.analysis_tools` (3 references)
- `core.integration.mcp` (1 reference)
- `core.intent_handlers` (1 reference)

**Verification Method**:
```bash
# Search for Python wrappers
grep -r "class CellularIntelligenceDiagnostic" core/
grep -r "class MCPServer" core/
grep -r "class IntentHandler" core/

# Check if they're C++ interfaces
grep -r "extern \"C\"" core/ | grep -E "(analysis_tools|mcp|intent_handlers)"
```

### Decision Point 3: Import Update Strategy
**Question**: How should imports be updated?

**Options**:
1. **Two-phase approach**:
   - Phase 1: Update imports for modules that migrated to computational_layer/ (assemblers, bridges, engines, etc.)
   - Phase 2: Update imports for modules in ai/src/intelligence/ to point there
   - Phase 3: Leave C++ interface imports pointing to core/

2. **Custom mapping approach**:
   - Enhance tool with module location mapping
   - Different transformation rules per module:
     * `core.consciousness_emergence_analyzer` → `ai.src.intelligence.consciousness_emergence_analyzer`
     * `core.assemblers` → `computational_layer.assemblers`
     * `core.integration.mcp` → stays as `core.integration.mcp` (C++ interface)

3. **Migration-first approach**:
   - Migrate all missing Python modules to computational_layer/ first
   - Then run import updater with simple core→computational_layer transformation

## Recommended Next Steps

### Immediate (Before Import Updates)
1. **Verify C++ interface status**:
   ```bash
   # Check if these are Python wrappers or C++ interfaces
   python -c "from core.analysis_tools import CellularIntelligenceDiagnostic"  # Does this work?
   python -c "from core.integration.mcp import MCPServer"  # Does this work?
   python -c "from core.intent_handlers import IntentHandler"  # Does this work?
   ```

2. **Identify actual module locations**:
   ```bash
   # Find where these modules actually exist
   find . -name "consciousness_emergence_analyzer.py"
   find . -name "library_ingestion_protocol.py"
   find . -name "core_engine_supercell_interface.py"
   find . -name "intent_handlers.py"
   ```

3. **Review Phase 2C migration scope**:
   - Re-read Phase 2C documentation
   - Determine original intent: What was supposed to migrate?
   - Compare planned vs actual migration

### Short-Term (Once Verified)
1. **Option A**: Migrate missing Python modules to computational_layer/
   - Move consciousness_emergence_analyzer → computational_layer/
   - Move library_ingestion_protocol → computational_layer/
   - Move core_engine_supercell_interface → computational_layer/
   - Then apply import updates with --phase2c

2. **Option B**: Update imports to point to actual current locations
   - Enhance tool with module location mapping
   - Apply targeted updates per module location
   - Leave C++ interfaces pointing to core/

3. **Option C**: Hybrid approach
   - Migrate consciousness_emergence_analyzer + library_ingestion_protocol
   - Leave core_engine_supercell_interface in tachyonic/
   - Update imports with custom mapping

## Tool Enhancement Success

Despite the module location issue, the tool enhancement was successful:

✅ Documentation governance applied (expanded existing tool)  
✅ Phase 2C detection working (11 imports found)  
✅ Import transformation logic implemented (7 patterns)  
✅ Dry-run mode preventing accidental breakage  
✅ Detailed reporting (by pattern, with line numbers)  
✅ Exclusion patterns preventing archive processing  
✅ CLI integration (--phase2c flag)  

**Next**: Apply tool to actual import updates once module locations are verified.

## Related Files

- **Enhanced Tool**: `ai/tools/update_import_paths.py` (731 lines)
- **Detection Report**: `ai/tools/import_update_report.json` (auto-generated)
- **Dev Path**: `docs/development/AIOS_DEV_PATH.md` (needs update)
- **Phase 2C Spec**: `docs/architecture/PHASE2C_LANGUAGE_SEPARATION.md` (review needed)

## Conclusion

The import path updater tool has been successfully enhanced with Phase 2C support and is ready to use, but **import updates are BLOCKED** pending module location verification. The tool correctly detected 11 imports that reference core.*, but analysis revealed the target modules haven't actually migrated to computational_layer/ yet.

**Status**: ⏸️ BLOCKED - Awaiting decision on module migration vs custom mapping  
**Next Action**: Verify C++ interface status + identify actual module locations  
**Impact**: Cannot proceed with import updates without breaking imports
