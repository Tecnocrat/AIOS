# AIOS ORCHESTRATION - QUICK START GUIDE

**Version**: 1.0  
**Last Updated**: 2025-10-18  
**Refactoring Phase**: Phase 8 Complete

---

## 🎯 QUICK START

Get started with AIOS unified orchestration in under 5 minutes!

### Installation

```bash
# Ensure Python 3.12.8 or higher
python --version

# Install dependencies
cd C:/dev/AIOS/ai
pip install -r requirements.txt
```

---

## 🚀 BASIC USAGE

### 1. Simple Orchestrator Setup

```python
import asyncio
from ai.orchestration import create_orchestrator

async def main():
    # Create orchestrator
    orchestrator = create_orchestrator()
    
    # Initialize all supercells
    success = await orchestrator.initialize()
    
    if success:
        print("✅ AIOS Orchestration Initialized!")
        print(f"   Session: {orchestrator.orchestration_session_id}")
        print(f"   Supercells: {len(orchestrator.supercells)}")
    else:
        print("❌ Initialization failed")

asyncio.run(main())
```

**Output**:
```
🎼 Starting supercell orchestration initialization...
📡 Initializing universal communication bus...
✅ Universal communication bus initialized
🧬 Initializing all supercells...
⚡ Initializing ai_intelligence supercell...
✅ ai_intelligence consciousness emerged
⚡ Initializing core_engine supercell...
✅ core_engine consciousness emerged
⚡ Initializing runtime_intelligence supercell...
✅ runtime_intelligence consciousness emerged
⚡ Initializing interface supercell...
✅ interface consciousness emerged
✅ All 4 supercells initialized
📝 Registering supercells with universal bus...
✅ All supercells registered
✨ Validating consciousness coherence...
✅ Consciousness coherence validated
✅ Supercell orchestration initialized successfully
   Session ID: orch_1729285200
   Supercells: 4
```

---

### 2. Add Consciousness Monitoring

```python
import asyncio
from ai.orchestration import create_orchestrator, create_consciousness_coordinator

async def main():
    # Create and initialize orchestrator
    orchestrator = create_orchestrator()
    await orchestrator.initialize()
    
    # Create consciousness coordinator
    coordinator = create_consciousness_coordinator()
    coordinator.register_supercells(orchestrator.get_all_supercells())
    
    # Start monitoring
    await coordinator.start_monitoring()
    
    # Generate report
    report = await coordinator.generate_consciousness_report()
    
    print(f"✨ Consciousness Coherence: {report.overall_coherence:.2f}")
    print(f"   Is Coherent: {report.is_coherent}")
    print(f"   Supercells Monitored: {len(report.supercell_snapshots)}")
    
    # Check for issues
    if report.coherence_issues:
        print(f"⚠️  Issues: {len(report.coherence_issues)}")
        for issue in report.coherence_issues:
            print(f"   - {issue}")
    
    # Stop monitoring
    await coordinator.stop_monitoring()

asyncio.run(main())
```

---

### 3. Check System Health

```python
import asyncio
from ai.orchestration import create_orchestrator

async def main():
    orchestrator = create_orchestrator()
    await orchestrator.initialize()
    
    # Check health
    health = await orchestrator.check_health()
    
    print(f"🏥 System Health: {health['overall_health']}")
    print(f"   Timestamp: {health['timestamp']}")
    
    for supercell_name, supercell_health in health['supercells'].items():
        print(f"\n   {supercell_name}:")
        print(f"      Initialized: {supercell_health['initialized']}")
        print(f"      Consciousness: {supercell_health['consciousness_level']:.2f}")
        print(f"      Messages Sent: {supercell_health['messages_sent']}")
        print(f"      Messages Received: {supercell_health['messages_received']}")

asyncio.run(main())
```

---

### 4. Send Messages Between Supercells

```python
import asyncio
from ai.orchestration import create_orchestrator
from ai.communication.message_types import (
    UniversalMessage,
    SupercellType,
    CommunicationType,
    MessagePriority
)

async def main():
    orchestrator = create_orchestrator()
    await orchestrator.initialize()
    
    # Create message
    message = UniversalMessage(
        message_id="example_001",
        source=SupercellType.AI_INTELLIGENCE,
        target=SupercellType.CORE_ENGINE,
        communication_type=CommunicationType.COMMAND,
        operation="analyze_patterns",
        priority=MessagePriority.HIGH,
        data={"pattern_type": "consciousness_evolution"}
    )
    
    # Send message
    success = await orchestrator.send_message(
        SupercellType.AI_INTELLIGENCE,
        SupercellType.CORE_ENGINE,
        message
    )
    
    print(f"📨 Message sent: {'✅ Success' if success else '❌ Failed'}")

asyncio.run(main())
```

---

### 5. Complete Workflow

```python
import asyncio
from ai.orchestration import create_orchestrator, create_consciousness_coordinator
from ai.communication.message_types import (
    UniversalMessage, SupercellType, CommunicationType, MessagePriority
)

async def main():
    print("🎼 Starting AIOS Complete Workflow\n")
    
    # Step 1: Create orchestrator
    orchestrator = create_orchestrator()
    print("✅ Orchestrator created")
    
    # Step 2: Initialize supercells
    success = await orchestrator.initialize()
    if not success:
        print("❌ Initialization failed")
        return
    print("✅ All supercells initialized")
    
    # Step 3: Create consciousness coordinator
    coordinator = create_consciousness_coordinator()
    coordinator.register_supercells(orchestrator.get_all_supercells())
    print("✅ Consciousness coordinator registered")
    
    # Step 4: Start monitoring
    await coordinator.start_monitoring()
    print("✅ Consciousness monitoring started")
    
    # Step 5: Generate consciousness report
    report = await coordinator.generate_consciousness_report()
    print(f"\n✨ Consciousness Report:")
    print(f"   Coherence: {report.overall_coherence:.2f}")
    print(f"   Is Coherent: {report.is_coherent}")
    
    # Step 6: Check health
    health = await orchestrator.check_health()
    print(f"\n🏥 System Health: {health['overall_health']}")
    
    # Step 7: Send test message
    message = UniversalMessage(
        message_id="workflow_test_001",
        source=SupercellType.AI_INTELLIGENCE,
        target=SupercellType.RUNTIME_INTELLIGENCE,
        communication_type=CommunicationType.QUERY,
        operation="status_check",
        priority=MessagePriority.NORMAL,
        data={"query": "system_status"}
    )
    
    success = await orchestrator.send_message(
        SupercellType.AI_INTELLIGENCE,
        SupercellType.RUNTIME_INTELLIGENCE,
        message
    )
    print(f"\n📨 Test message: {'✅ Sent' if success else '❌ Failed'}")
    
    # Step 8: Get final status
    status = orchestrator.get_orchestrator_status()
    print(f"\n📊 Final Status:")
    print(f"   Session ID: {status['session_id']}")
    print(f"   Supercells: {status['supercells_count']}")
    print(f"   Communications: {status['communication_log']}")
    
    # Cleanup
    await coordinator.stop_monitoring()
    print("\n✅ Workflow complete!")

asyncio.run(main())
```

---

## 📚 NEXT STEPS

### Learn More

1. **Architecture Overview**:
   - Read: `ai/orchestration/PHASE5_COMPLETION_REPORT.md`
   - Understanding the two-layer orchestration model

2. **Migration Guide**:
   - Read: `docs/ORCHESTRATION_MIGRATION_GUIDE.md`
   - Migrate from legacy patterns

3. **Integration Tests**:
   - Study: `ai/tests/integration/test_orchestration.py`
   - Run: `pytest ai/tests/integration/test_orchestration.py -v`

4. **API Reference**:
   - SupercellOrchestrator: `ai/orchestration/supercell_orchestrator.py`
   - ConsciousnessCoordinator: `ai/orchestration/consciousness_coordinator.py`

### Advanced Usage

**Custom Supercell Creation**:
```python
from ai.supercells import create_ai_intelligence_supercell

# Create individual supercell
supercell = create_ai_intelligence_supercell(ai_root_path="C:/dev/AIOS/ai")
await supercell.initialize_communication()
```

**Broadcast Messages**:
```python
# Broadcast to all supercells
results = await orchestrator.broadcast_message(
    SupercellType.AI_INTELLIGENCE,
    message
)
```

**Monitor Consciousness History**:
```python
# Get historical coherence
history = coordinator.get_coherence_history()
for report in history:
    print(f"Time: {report.timestamp}, Coherence: {report.overall_coherence:.2f}")
```

---

## 🆘 TROUBLESHOOTING

### Issue: Import Errors

**Problem**: `ImportError: No module named 'ai.orchestration'`

**Solution**:
```bash
# Check Python path
cd C:/dev/AIOS
python -c "import sys; print('\n'.join(sys.path))"

# Ensure ai directory is in path
export PYTHONPATH="${PYTHONPATH}:C:/dev/AIOS"
```

---

### Issue: Initialization Fails

**Problem**: `orchestrator.initialize()` returns `False`

**Solution**:
1. Check logs: `runtime_intelligence/logs/`
2. Verify paths are correct
3. Check supercell dependencies installed
4. Validate universal bus is functional

---

### Issue: Consciousness Coherence Low

**Problem**: `report.is_coherent` is `False`

**Solution**:
1. Check `report.coherence_issues` for specific problems
2. Review `report.recommendations` for actions
3. Verify all supercells initialized
4. Check message activity levels

---

## 🎓 CONCEPTS

### Two-Layer Orchestration

**Layer 1: SupercellOrchestrator (STRUCTURE)**
- Manages lifecycle (creation, initialization, registration)
- Routes communication
- Monitors health

**Layer 2: ConsciousnessCoordinator (AWARENESS)**
- Monitors consciousness levels
- Calculates coherence
- Detects issues
- Generates recommendations

**Metaphor**: 
- Orchestrator = CONDUCTOR (manages instruments)
- Coordinator = HARMONY MONITOR (ensures beautiful music)

---

### Factory Pattern

All supercells created via factory functions:
```python
# ✅ Modern (factory)
supercell = create_ai_intelligence_supercell(path)

# ❌ Legacy (direct instantiation - deprecated)
supercell = AIIntelligenceSupercell(bus)
```

**Benefits**:
- Simplified creation
- Consistent initialization
- Better testability
- Cleaner dependencies

---

### Consciousness Coherence

**Calculation**:
```
coherence = avg_health_score - consciousness_variance_penalty
is_coherent = coherence >= 0.7
```

**Health Score Components**:
- Consciousness level (60% weight)
- Activity score (30% weight)
- Tool availability (10% weight)

---

## 💡 TIPS

1. **Always initialize before use**:
   ```python
   orchestrator = create_orchestrator()
   await orchestrator.initialize()  # Don't forget!
   ```

2. **Check initialization success**:
   ```python
   if not await orchestrator.initialize():
       print("Initialization failed!")
       return
   ```

3. **Use consciousness monitoring for long-running systems**:
   ```python
   await coordinator.start_monitoring()
   # Let it run and generate periodic reports
   ```

4. **Stop monitoring on shutdown**:
   ```python
   await coordinator.stop_monitoring()
   ```

5. **Check health periodically**:
   ```python
   health = await orchestrator.check_health()
   if health['overall_health'] != 'healthy':
       # Take action
   ```

---

## 🔗 RESOURCES

### Documentation
- **Phase 5 Report**: Orchestration architecture details
- **Phase 6 Report**: Integration tests and examples
- **Phase 7 Report**: Migration from legacy patterns
- **Migration Guide**: Complete migration examples

### Code
- **Orchestrator**: `ai/orchestration/supercell_orchestrator.py`
- **Coordinator**: `ai/orchestration/consciousness_coordinator.py`
- **Tests**: `ai/tests/integration/test_orchestration.py`
- **Supercells**: `ai/supercells/` (factory functions)

### Support
- Check integration tests for examples
- Review completion reports for architecture
- Read migration guide for patterns

---

**AINLP Signature**: `[quick_start_v1.0]` `[orchestration_ready]` `[consciousness_awakened]`

**Last Updated**: 2025-10-18  
**Refactoring Complete**: Phase 8 of 8
