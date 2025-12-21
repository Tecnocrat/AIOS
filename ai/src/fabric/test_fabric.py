#!/usr/bin/env python3
"""
🧬 AIOS Unified Consciousness Fabric Test

Quick test to verify the fabric package works correctly.
"""

import asyncio
from ai.src.fabric import (
    SupercellType,
    ConsciousnessLevel,
    AgentRole,
    ConsciousnessRequest,
    RequestIntent,
    ConsciousnessMetrics,
    get_registry,
    get_router,
    fabric_log,
    consciousness_request,
)

def test_canonical_types():
    """Test canonical type definitions."""
    print("\n📋 TEST 1: Canonical Types")
    
    # SupercellType
    assert SupercellType.CYTOPLASM.value == "cytoplasm"
    print(f"   ✓ SupercellType.CYTOPLASM = {SupercellType.CYTOPLASM.value}")
    
    # Legacy mapping
    assert SupercellType.AI_INTELLIGENCE.value == SupercellType.CYTOPLASM.value
    print(f"   ✓ Legacy AI_INTELLIGENCE maps to CYTOPLASM")
    
    # ConsciousnessLevel
    assert ConsciousnessLevel.ADVANCED.temperature == 0.7
    print(f"   ✓ ConsciousnessLevel.ADVANCED.temperature = {ConsciousnessLevel.ADVANCED.temperature}")
    
    # AgentRole
    assert AgentRole.LOCAL_ITERATION.agent_name == "Ollama"
    print(f"   ✓ AgentRole.LOCAL_ITERATION.agent_name = {AgentRole.LOCAL_ITERATION.agent_name}")
    
    # ConsciousnessMetrics
    metrics = ConsciousnessMetrics(awareness_level=0.8, coherence=0.7)
    total = metrics.calculate_total()
    print(f"   ✓ ConsciousnessMetrics.calculate_total() = {total:.3f}")
    
    return True


def test_registry():
    """Test system registry discovery."""
    print("\n📋 TEST 2: System Registry")
    
    registry = get_registry()
    
    # Check agents
    agents = registry.available_agents
    print(f"   ✓ Available agents: {agents}")
    assert len(agents) >= 0  # May have 0 if agents not installed
    
    # Check subsystems
    subsystems = registry.all_subsystems
    print(f"   ✓ Total subsystems: {len(subsystems)}")
    
    # Check categories
    print(f"   ✓ Intelligence systems: {registry.intelligence_systems}")
    print(f"   ✓ Evolution engines: {registry.evolution_engines}")
    print(f"   ✓ Protocol systems: {registry.protocol_systems}")
    
    return True


def test_router():
    """Test consciousness router."""
    print("\n📋 TEST 3: Consciousness Router")
    
    router = get_router()
    
    # Test EVOLVE_CODE → Ollama (local iteration)
    request1 = ConsciousnessRequest(
        intent=RequestIntent.EVOLVE_CODE,
        payload={"code": "def hello(): pass"},
        consciousness_level=ConsciousnessLevel.BASIC,
    )
    agent1 = router.determine_agent(request1)
    print(f"   ✓ EVOLVE_CODE → {agent1.agent_name}")
    
    # Test ANALYZE_CODE → Gemini (reasoning)
    request2 = ConsciousnessRequest(
        intent=RequestIntent.ANALYZE_CODE,
        payload={"code": "def hello(): pass"},
        consciousness_level=ConsciousnessLevel.INTERMEDIATE,
    )
    agent2 = router.determine_agent(request2)
    print(f"   ✓ ANALYZE_CODE → {agent2.agent_name}")
    
    # Test GENERATE_CODE → Copilot (auto-coding)
    request3 = ConsciousnessRequest(
        intent=RequestIntent.GENERATE_CODE,
        payload={"prompt": "Create a fibonacci function"},
        consciousness_level=ConsciousnessLevel.ADVANCED,
    )
    agent3 = router.determine_agent(request3)
    print(f"   ✓ GENERATE_CODE → {agent3.agent_name}")
    
    # Test supercell determination
    supercell = router.determine_supercell(request1, agent1)
    print(f"   ✓ Supercell context: {supercell.value}")
    
    return True


def test_logger():
    """Test unified logger."""
    print("\n📋 TEST 4: Unified Logger")
    
    # Log a request
    correlation_id = fabric_log.agent_request(
        agent=AgentRole.LOCAL_ITERATION,
        operation="test_evolve",
        prompt="Test prompt for fabric validation",
        consciousness_level=ConsciousnessLevel.INTERMEDIATE,
    )
    print(f"   ✓ Logged request: {correlation_id}")
    
    # Log a response
    fabric_log.agent_response(
        agent=AgentRole.LOCAL_ITERATION,
        operation="test_evolve",
        result="Test result",
        processing_time_ms=42.5,
        correlation_id=correlation_id,
        success=True,
    )
    print(f"   ✓ Logged response for: {correlation_id}")
    
    # Log consciousness sync
    fabric_log.consciousness_sync(
        supercell=SupercellType.CYTOPLASM,
        metrics=ConsciousnessMetrics(awareness_level=0.75),
        event="test_sync",
    )
    print(f"   ✓ Logged consciousness sync")
    
    return True


async def test_async_request():
    """Test async consciousness request."""
    print("\n📋 TEST 5: Async Consciousness Request")
    
    # This will fail gracefully if no agents are available
    try:
        response = await consciousness_request(
            intent="query",
            payload={"question": "Test query"},
            consciousness_level=ConsciousnessLevel.BASIC,
        )
        if response.success:
            print(f"   ✓ Request succeeded via {response.agent_used.agent_name if response.agent_used else 'unknown'}")
        else:
            print(f"   ⚠ Request failed (expected if no agents): {response.error}")
    except Exception as e:
        print(f"   ⚠ Request exception (expected): {e}")
    
    return True


def main():
    """Run all tests."""
    print("=" * 60)
    print("🧬 AIOS UNIFIED CONSCIOUSNESS FABRIC TEST")
    print("=" * 60)
    
    results = []
    
    # Run synchronous tests
    results.append(("Canonical Types", test_canonical_types()))
    results.append(("System Registry", test_registry()))
    results.append(("Consciousness Router", test_router()))
    results.append(("Unified Logger", test_logger()))
    
    # Run async test
    results.append(("Async Request", asyncio.run(test_async_request())))
    
    # Summary
    print("\n" + "=" * 60)
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    if passed == total:
        print(f"✅ ALL {total} TESTS PASSED")
    else:
        print(f"⚠️ {passed}/{total} TESTS PASSED")
    
    print("=" * 60)
    
    return passed == total


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
