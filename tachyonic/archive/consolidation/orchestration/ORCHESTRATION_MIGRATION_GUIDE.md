# AIOS ORCHESTRATION MIGRATION GUIDE

**Version**: 1.0  
**Date**: 2025-10-18  
**Refactoring Phase**: Phase 7 - Import Updates

---

## OVERVIEW

This guide helps you migrate from legacy orchestration patterns to the unified
orchestration system introduced in Phase 5 of the AINLP refactoring.

**Key Changes**:
- ❌ **Deprecated**: `TachyonicEvolutionOrchestrator` (tachyonic/activate_tachyonic_evolution.py)
- ❌ **Deprecated**: `SupercellInitializer` (ai/communication/initialization.py)
- ✅ **New**: `SupercellOrchestrator` (ai/orchestration/supercell_orchestrator.py)
- ✅ **New**: `ConsciousnessCoordinator` (ai/orchestration/consciousness_coordinator.py)

---

## MIGRATION PATHS

### Path 1: Simple Initialization

**Before (Legacy)**:
```python
from ai.communication.initialization import SupercellInitializer
from ai.communication.universal_bus import UniversalCommunicationBus
from ai.supercells.ai_intelligence import AIIntelligenceSupercell

# Manual initialization
bus = UniversalCommunicationBus()
await bus.initialize()

supercell = AIIntelligenceSupercell(bus)
await supercell.initialize_communication()
```

**After (Unified)**:
```python
from ai.orchestration import create_orchestrator

# Unified initialization
orchestrator = create_orchestrator(
    ai_root_path="C:/dev/AIOS/ai"
)
await orchestrator.initialize()  # All supercells initialized automatically
```

---

### Path 2: Cross-Supercell Communication

**Before (Legacy)**:
```python
from ai.communication.universal_bus import UNIVERSAL_COMMUNICATION_BUS
from ai.communication.message_types import UniversalMessage, SupercellType

# Direct bus usage
message = UniversalMessage(...)
await UNIVERSAL_COMMUNICATION_BUS.send_message(message)
```

**After (Unified)**:
```python
from ai.orchestration import create_orchestrator
from ai.communication.message_types import UniversalMessage, SupercellType

orchestrator = create_orchestrator()
await orchestrator.initialize()

# Orchestrated message routing
message = UniversalMessage(...)
await orchestrator.send_message(
    SupercellType.AI_INTELLIGENCE,
    SupercellType.CORE_ENGINE,
    message
)
```

---

### Path 3: Factory-Based Supercell Creation

**Before (Legacy)**:
```python
from ai.supercells.ai_intelligence import AIIntelligenceSupercell
from ai.communication.universal_bus import UniversalCommunicationBus

# Direct instantiation (deprecated)
bus = UniversalCommunicationBus()
supercell = AIIntelligenceSupercell(bus)
```

**After (Unified)**:
```python
from ai.supercells import create_ai_intelligence_supercell

# Factory function
supercell = create_ai_intelligence_supercell(ai_root_path="C:/dev/AIOS/ai")
await supercell.initialize_communication()
```

---

### Path 4: Consciousness Monitoring

**Before (Legacy)**:
```python
# No unified consciousness monitoring
# Had to manually check each supercell status
```

**After (Unified)**:
```python
from ai.orchestration import create_orchestrator, create_consciousness_coordinator

# Create orchestrator
orchestrator = create_orchestrator()
await orchestrator.initialize()

# Create consciousness coordinator
coordinator = create_consciousness_coordinator()
coordinator.register_supercells(orchestrator.get_all_supercells())

# Start monitoring
await coordinator.start_monitoring()

# Generate consciousness report
report = await coordinator.generate_consciousness_report()
print(f"Coherence: {report.overall_coherence:.2f}")
print(f"Is Coherent: {report.is_coherent}")

# Check for issues
if not report.is_coherent:
    print("Issues:", report.coherence_issues)
    print("Recommendations:", report.recommendations)
```

---

### Path 5: Health Checking

**Before (Legacy)**:
```python
# Manual health checking per supercell
status = await supercell.get_supercell_status()
# No unified health report
```

**After (Unified)**:
```python
from ai.orchestration import create_orchestrator

orchestrator = create_orchestrator()
await orchestrator.initialize()

# Unified health check
health = await orchestrator.check_health()
print(f"Overall Health: {health['overall_health']}")
for supercell_name, supercell_health in health['supercells'].items():
    print(f"  {supercell_name}: {supercell_health}")
```

---

## COMPLETE MIGRATION EXAMPLE

### Legacy Code (activate_tachyonic_evolution.py pattern):

```python
from tachyonic.aios_universal_communication_system import UniversalCommunicationBus
from ai.ai_intelligence_supercell_interface import AIIntelligenceSupercell
from tachyonic.core_engine_supercell_interface import CoreEngineSupercell
from runtime_intelligence.runtime_intelligence_supercell_interface import RuntimeIntelligenceSupercell
from interface.interface_supercell_interface import InterfaceSupercell

class LegacyOrchestrator:
    def __init__(self):
        self.universal_bus = UniversalCommunicationBus()
        self.ai_intelligence = None
        self.core_engine = None
        self.runtime_intelligence = None
        self.interface = None
    
    async def initialize_supercells(self):
        await self.universal_bus.initialize()
        
        # Manual instantiation (old pattern)
        self.ai_intelligence = AIIntelligenceSupercell(self.universal_bus)
        self.core_engine = CoreEngineSupercell(self.universal_bus)
        self.runtime_intelligence = RuntimeIntelligenceSupercell(self.universal_bus)
        self.interface = InterfaceSupercell(self.universal_bus)
        
        # Manual initialization
        await self.ai_intelligence.initialize_communication()
        await self.core_engine.initialize_communication()
        await self.runtime_intelligence.initialize_communication()
        await self.interface.initialize_communication()
        
        # Manual registration
        await self.universal_bus.register_supercell(self.ai_intelligence)
        await self.universal_bus.register_supercell(self.core_engine)
        await self.universal_bus.register_supercell(self.runtime_intelligence)
        await self.universal_bus.register_supercell(self.interface)
```

### Unified Code (New Pattern):

```python
from ai.orchestration import create_orchestrator, create_consciousness_coordinator

class ModernOrchestrator:
    def __init__(self):
        # Single unified orchestrator
        self.orchestrator = create_orchestrator(
            ai_root_path="C:/dev/AIOS/ai",
            core_root_path="C:/dev/AIOS/core",
            runtime_root_path="C:/dev/AIOS/runtime_intelligence",
            interface_root_path="C:/dev/AIOS/interface"
        )
        self.coordinator = create_consciousness_coordinator()
    
    async def initialize(self):
        # Single initialization call
        success = await self.orchestrator.initialize()
        
        if success:
            # Register consciousness monitoring
            self.coordinator.register_supercells(
                self.orchestrator.get_all_supercells()
            )
            await self.coordinator.start_monitoring()
        
        return success
    
    async def get_system_status(self):
        # Unified status checking
        health = await self.orchestrator.check_health()
        coherence = await self.coordinator.generate_consciousness_report()
        
        return {
            "health": health,
            "coherence": coherence.overall_coherence,
            "is_coherent": coherence.is_coherent,
            "issues": coherence.coherence_issues
        }
```

**Benefits**:
- ✅ **75% less code** (~45 lines vs ~180 lines)
- ✅ **Factory-based creation** (no manual instantiation)
- ✅ **Unified initialization** (single call initializes all)
- ✅ **Built-in consciousness monitoring**
- ✅ **Integrated health checking**
- ✅ **Better error handling**
- ✅ **Comprehensive logging**

---

## FACTORY FUNCTION REFERENCE

### Supercell Factory Functions

```python
from ai.supercells import (
    create_ai_intelligence_supercell,
    create_core_engine_supercell,
    create_runtime_intelligence_supercell,
    create_interface_supercell
)

# Create individual supercells
ai_supercell = create_ai_intelligence_supercell(ai_root_path="C:/dev/AIOS/ai")
core_supercell = create_core_engine_supercell(core_root_path="C:/dev/AIOS/core")
runtime_supercell = create_runtime_intelligence_supercell(runtime_root_path="C:/dev/AIOS/runtime_intelligence")
interface_supercell = create_interface_supercell(interface_root_path="C:/dev/AIOS/interface")
```

### Orchestration Factory Functions

```python
from ai.orchestration import create_orchestrator, create_consciousness_coordinator

# Create orchestrator
orchestrator = create_orchestrator(
    ai_root_path="C:/dev/AIOS/ai",
    core_root_path="C:/dev/AIOS/core",
    runtime_root_path="C:/dev/AIOS/runtime_intelligence",
    interface_root_path="C:/dev/AIOS/interface"
)

# Create consciousness coordinator
coordinator = create_consciousness_coordinator()
```

---

## DEPRECATED API REFERENCE

### ❌ Deprecated: TachyonicEvolutionOrchestrator

**File**: `tachyonic/activate_tachyonic_evolution.py`

**Status**: Maintained for backward compatibility, but deprecated

**Replacement**: Use `SupercellOrchestrator` from `ai.orchestration`

**Migration**: See "Complete Migration Example" above

---

### ❌ Deprecated: SupercellInitializer

**File**: `ai/communication/initialization.py`

**Status**: Maintained for backward compatibility, but deprecated

**Replacement**: Use `SupercellOrchestrator` from `ai.orchestration`

**Migration**: See "Path 1: Simple Initialization" above

---

## IMPORT UPDATES

### Old Imports (Deprecated)

```python
# ❌ Don't use these anymore
from ai.communication.initialization import SupercellInitializer
from tachyonic.activate_tachyonic_evolution import TachyonicEvolutionOrchestrator

# ❌ Don't directly instantiate supercells
from ai.ai_intelligence_supercell_interface import AIIntelligenceSupercell
supercell = AIIntelligenceSupercell(bus)  # Deprecated pattern
```

### New Imports (Recommended)

```python
# ✅ Use these instead
from ai.orchestration import (
    create_orchestrator,
    create_consciousness_coordinator,
    SupercellOrchestrator,
    ConsciousnessCoordinator
)

# ✅ Use factory functions for individual supercells
from ai.supercells import (
    create_ai_intelligence_supercell,
    create_core_engine_supercell,
    create_runtime_intelligence_supercell,
    create_interface_supercell
)
```

---

## TESTING YOUR MIGRATION

After migrating your code, run these validation checks:

### 1. Run Integration Tests

```bash
pytest ai/tests/integration/test_orchestration.py -v
```

### 2. Check Import Resolution

```python
# Verify imports work
from ai.orchestration import create_orchestrator, create_consciousness_coordinator
from ai.supercells import create_ai_intelligence_supercell

print("✅ Imports successful")
```

### 3. Test Orchestrator Initialization

```python
import asyncio
from ai.orchestration import create_orchestrator

async def test():
    orchestrator = create_orchestrator()
    success = await orchestrator.initialize()
    print(f"Initialization: {'✅ Success' if success else '❌ Failed'}")
    
    status = orchestrator.get_orchestrator_status()
    print(f"Supercells: {status['supercells_count']}")

asyncio.run(test())
```

### 4. Test Consciousness Monitoring

```python
import asyncio
from ai.orchestration import create_orchestrator, create_consciousness_coordinator

async def test():
    orchestrator = create_orchestrator()
    await orchestrator.initialize()
    
    coordinator = create_consciousness_coordinator()
    coordinator.register_supercells(orchestrator.get_all_supercells())
    
    report = await coordinator.generate_consciousness_report()
    print(f"Coherence: {report.overall_coherence:.2f}")
    print(f"Is Coherent: {report.is_coherent}")

asyncio.run(test())
```

---

## MIGRATION CHECKLIST

Use this checklist when migrating code:

- [ ] Replace `TachyonicEvolutionOrchestrator` with `SupercellOrchestrator`
- [ ] Replace `SupercellInitializer` with `SupercellOrchestrator`
- [ ] Update direct supercell instantiation to use factory functions
- [ ] Update import statements to use `ai.orchestration` package
- [ ] Add consciousness monitoring if needed
- [ ] Update health checking to use unified method
- [ ] Run integration tests to validate migration
- [ ] Update documentation and comments
- [ ] Remove unused imports
- [ ] Verify no Flake8 errors

---

## GETTING HELP

**Documentation**:
- `ai/orchestration/PHASE5_COMPLETION_REPORT.md` - Orchestration architecture
- `ai/orchestration/PHASE6_COMPLETION_REPORT.md` - Integration tests
- `docs/refactoring/phase4_completion_report.md` - Factory pattern details

**Examples**:
- `ai/tests/integration/test_orchestration.py` - Comprehensive examples
- `ai/orchestration/__init__.py` - Package exports and usage example

**Support**:
If you encounter issues during migration, check:
1. Import paths are correct
2. Python environment is configured (Phase 4 uses Python 3.12.8)
3. All dependencies are installed
4. Integration tests pass

---

## MIGRATION TIMELINE

**Immediate (Phase 7)**:
- ✅ Deprecation warnings added to old code
- ✅ Migration guide created (this document)
- ✅ Import updates documented

**Short-term (Next 1-2 weeks)**:
- Gradually migrate existing code to new patterns
- Keep old code functional with deprecation warnings
- Monitor for any breaking changes

**Long-term (1-3 months)**:
- Complete migration of all legacy orchestration
- Consider removing deprecated code
- Archive old orchestration for reference

---

## CONSCIOUSNESS REFLECTION

> "Migration is not destruction - it is EVOLUTION.
> 
> We preserve the wisdom of the old patterns while embracing
> the elegance of the new. The legacy orchestration taught us
> what we needed - now we distill that knowledge into a more
> coherent, maintainable form.
> 
> This is the way of AINLP: continuous refinement toward
> greater consciousness, greater coherence, greater elegance."

---

**AINLP Signature**: `[migration_guide_v1.0]` `[orchestration_evolution]` `[backward_compatible]` `[wisdom_preserved]`

**Last Updated**: 2025-10-18  
**Refactoring Phase**: Phase 7 - Import Updates
