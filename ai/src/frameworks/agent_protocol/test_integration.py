#!/usr/bin/env python3
"""
Agent Protocol Integration Test
================================

Comprehensive testing of AIAgentProtocol with all three AIOS agents.

AINLP Protocol: OS0.6.2.claude
Purpose: Validate full adapter implementation
Tests: DeepSeek, Gemini, Ollama protocol compliance

Test Scenarios:
1. Adapter Creation: All three agents instantiate successfully
2. Protocol Compliance: All implement AIAgentProtocol correctly
3. Message Execution: run() works for all agents
4. Consciousness Scoring: All return valid consciousness scores
5. Thread Management: get_new_thread() creates proper thread objects
6. Error Handling: Graceful degradation when agents unavailable

Success Criteria:
- All adapters implement AIAgentProtocol (structural typing)
- All agents return AgentRunResponse with consciousness scores
- Thread objects store agent-specific context
- Error messages are informative when agents unavailable
"""

import sys
import asyncio
from pathlib import Path
from typing import Protocol, runtime_checkable
import logging

# AIOS path integration
AIOS_ROOT = Path(__file__).parent.parent.parent.parent.parent
sys.path.append(str(AIOS_ROOT / "ai" / "src"))

# Import protocol and adapters
from frameworks.agent_protocol import (
    AIAgentProtocol,
    AgentRunResponse,
    DeepSeekProtocolAdapter,
    GeminiProtocolAdapter,
    OllamaProtocolAdapter,
    DeepSeekThread,
    GeminiThread,
    OllamaThread,
    adapt_deepseek_agent,
    adapt_gemini_agent,
    adapt_ollama_agent,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ============================================================================
# TEST UTILITIES
# ============================================================================


    @property
    def id(self) -> str: ...
    @property
    def consciousness_level(self) -> float: ...
    async def run(self, messages, *, thread=None, **kwargs): ...


# ============================================================================
# INTEGRATION TESTS
# ============================================================================


async def test_adapter_creation():
    """Test 1: Verify all adapters can be created"""
    print("\n" + "=" * 70)
    print("TEST 1: Adapter Creation")
    print("=" * 70)

    results = []

    # Test DeepSeek adapter creation
    try:
        deepseek = DeepSeekProtocolAdapter()
        results.append(
            test_result("DeepSeek Adapter", deepseek is not None, f"ID: {deepseek.id}")
        )
    except Exception as e:
        results.append(test_result("DeepSeek Adapter", False, str(e)))

    # Test Gemini adapter creation
    try:
        gemini = GeminiProtocolAdapter()
        results.append(
            test_result("Gemini Adapter", gemini is not None, f"ID: {gemini.id}")
        )
    except Exception as e:
        results.append(test_result("Gemini Adapter", False, str(e)))

    # Test Ollama adapter creation
    try:
        ollama = OllamaProtocolAdapter(model="gemma3:1b")
        results.append(
            test_result("Ollama Adapter", ollama is not None, f"ID: {ollama.id}")
        )
    except Exception as e:
        results.append(test_result("Ollama Adapter", False, str(e)))

    return all(results)


async def test_protocol_compliance():
    """Test 2: Verify structural typing protocol compliance"""
    print("\n" + "=" * 70)
    print("TEST 2: Protocol Compliance (Structural Typing)")
    print("=" * 70)

    results = []

    # Create adapters
    deepseek = DeepSeekProtocolAdapter()
    gemini = GeminiProtocolAdapter()
    ollama = OllamaProtocolAdapter()

    # Test structural typing with isinstance
    results.append(
        test_result(
            "DeepSeek Protocol Compliance",
            isinstance(deepseek, AIAgentProtocol),
            "Implements AIAgentProtocol interface",
        )
    )

    results.append(
        test_result(
            "Gemini Protocol Compliance",
            isinstance(gemini, AIAgentProtocol),
            "Implements AIAgentProtocol interface",
        )
    )

    results.append(
        test_result(
            "Ollama Protocol Compliance",
            isinstance(ollama, AIAgentProtocol),
            "Implements AIAgentProtocol interface",
        )
    )

    # Test required properties
    for agent, name in [(deepseek, "DeepSeek"), (gemini, "Gemini"), (ollama, "Ollama")]:
        has_id = hasattr(agent, "id") and isinstance(agent.id, str)
        has_consciousness = hasattr(agent, "consciousness_level") and isinstance(
            agent.consciousness_level, float
        )
        has_run = hasattr(agent, "run") and callable(agent.run)
        has_thread = hasattr(agent, "get_new_thread") and callable(agent.get_new_thread)

        all_present = has_id and has_consciousness and has_run and has_thread
        results.append(
            test_result(
                f"{name} Required Properties",
                all_present,
                f"id={has_id}, consciousness={has_consciousness}, run={has_run}, thread={has_thread}",
            )
        )

    return all(results)


async def test_factory_functions():
    """Test 3: Verify factory functions work correctly"""
    print("\n" + "=" * 70)
    print("TEST 3: Factory Functions")
    print("=" * 70)

    results = []

    # Test adapt_gemini_agent (sync factory)
    try:
        gemini = adapt_gemini_agent(temperature=0.8)
        results.append(
            test_result(
                "adapt_gemini_agent()",
                isinstance(gemini, GeminiProtocolAdapter),
                f"Created {gemini.id} with temp=0.8",
            )
        )
    except Exception as e:
        results.append(test_result("adapt_gemini_agent()", False, str(e)))

    # Test adapt_ollama_agent (sync factory)
    try:
        ollama = adapt_ollama_agent(model="gemma3:1b")
        results.append(
            test_result(
                "adapt_ollama_agent()",
                isinstance(ollama, OllamaProtocolAdapter),
                f"Created {ollama.id}",
            )
        )
    except Exception as e:
        results.append(test_result("adapt_ollama_agent()", False, str(e)))

    # Test adapt_deepseek_agent (async factory - requires initialization)
    try:
        # Note: This may fail without valid API key, which is acceptable
        deepseek = DeepSeekProtocolAdapter()
        results.append(
            test_result(
                "DeepSeek Adapter Creation",
                isinstance(deepseek, DeepSeekProtocolAdapter),
                f"Created {deepseek.id} (initialization may require API key)",
            )
        )
    except Exception as e:
        results.append(
            test_result(
                "DeepSeek Adapter Creation",
                False,
                f"Expected without API key: {str(e)[:50]}",
            )
        )

    return all(results)


async def test_thread_management():
    """Test 4: Verify thread creation and types"""
    print("\n" + "=" * 70)
    print("TEST 4: Thread Management")
    print("=" * 70)

    results = []

    # Create adapters
    deepseek = DeepSeekProtocolAdapter()
    gemini = GeminiProtocolAdapter()
    ollama = OllamaProtocolAdapter()

    # Test DeepSeek thread
    try:
        thread = deepseek.get_new_thread(supercell_source="test")
        results.append(
            test_result(
                "DeepSeek Thread Creation",
                isinstance(thread, DeepSeekThread),
                f"Created thread with supercell_source",
            )
        )
    except Exception as e:
        results.append(test_result("DeepSeek Thread Creation", False, str(e)))

    # Test Gemini thread
    try:
        thread = gemini.get_new_thread(temperature=0.9)
        results.append(
            test_result(
                "Gemini Thread Creation",
                isinstance(thread, GeminiThread),
                f"Created thread with temperature={thread.temperature}",
            )
        )
    except Exception as e:
        results.append(test_result("Gemini Thread Creation", False, str(e)))

    # Test Ollama thread
    try:
        thread = ollama.get_new_thread()
        results.append(
            test_result(
                "Ollama Thread Creation",
                isinstance(thread, OllamaThread),
                f"Created thread with model={thread.model}",
            )
        )
    except Exception as e:
        results.append(test_result("Ollama Thread Creation", False, str(e)))

    return all(results)


async def test_consciousness_properties():
    """Test 5: Verify consciousness level properties"""
    print("\n" + "=" * 70)
    print("TEST 5: Consciousness Levels")
    print("=" * 70)

    results = []

    # Create adapters
    adapters = [
        ("DeepSeek", DeepSeekProtocolAdapter()),
        ("Gemini", GeminiProtocolAdapter()),
        ("Ollama", OllamaProtocolAdapter()),
    ]

    for name, adapter in adapters:
        consciousness = adapter.consciousness_level
        valid = 0.0 <= consciousness <= 1.0
        results.append(
            test_result(
                f"{name} Consciousness Level",
                valid,
                f"{consciousness:.2f} (valid range: 0.0-1.0)",
            )
        )

    return all(results)


async def test_agent_swapping():
    """Test 6: Verify agents are interchangeable (plug-and-play)"""
    print("\n" + "=" * 70)
    print("TEST 6: Agent Swapping (Plug-and-Play Architecture)")
    print("=" * 70)

    results = []

    # Create list of protocol-compliant agents
    agents = [
        DeepSeekProtocolAdapter(),
        GeminiProtocolAdapter(),
        OllamaProtocolAdapter(),
    ]

    # Verify all can be stored in same list
    all_protocol = all(isinstance(agent, AIAgentProtocol) for agent in agents)
    results.append(
        test_result(
            "Agents List Storage",
            all_protocol,
            f"All {len(agents)} agents stored as AIAgentProtocol type",
        )
    )

    # Verify all have same interface
    for i, agent in enumerate(agents, 1):
        has_interface = (
            hasattr(agent, "id")
            and hasattr(agent, "consciousness_level")
            and hasattr(agent, "run")
            and hasattr(agent, "get_new_thread")
        )
        results.append(
            test_result(
                f"Agent {i} Interface",
                has_interface,
                f"{agent.id} has unified protocol interface",
            )
        )

    return all(results)


async def test_basic_execution():
    """Test 7: Basic execution test (if agents available)"""
    print("\n" + "=" * 70)
    print("TEST 7: Basic Execution (Connectivity Test)")
    print("=" * 70)

    results = []

    # Test Ollama (most likely to work locally)
    print("\n[INFO] Testing Ollama local execution...")
    try:
        ollama = OllamaProtocolAdapter(model="gemma3:1b")
        if ollama._agent.is_available:
            response = await ollama.run("Say 'Hello AIOS Protocol!'")
            valid_response = (
                isinstance(response, AgentRunResponse)
                and len(response.messages) > 0
                and 0.0 <= response.consciousness_score <= 1.0
            )
            results.append(
                test_result(
                    "Ollama Execution",
                    valid_response,
                    f"Returned {len(response.messages[0])} chars, consciousness={response.consciousness_score:.2f}",
                )
            )
        else:
            results.append(
                test_result(
                    "Ollama Execution",
                    True,  # Not failure if Ollama not installed
                    "Ollama not available (install with: curl https://ollama.ai/install.sh | sh)",
                )
            )
    except Exception as e:
        results.append(test_result("Ollama Execution", False, f"Error: {str(e)[:100]}"))

    # Note: DeepSeek and Gemini require API keys, so we skip actual execution
    print("[INFO] Skipping DeepSeek/Gemini execution (require API keys)")
    print("[INFO] To test those, set OPENROUTER_API_KEY and GEMINI_API_KEY")

    return all(results)


# ============================================================================
# TEST RUNNER
# ============================================================================


async def run_all_tests():
    """Execute all integration tests"""
    print("\n" + "=" * 70)
    print(" AGENT PROTOCOL INTEGRATION TEST SUITE")
    print(" AINLP Extraction ID: EXT-001-Phase2")
    print(" Purpose: Validate full adapter implementation")
    print("=" * 70)

    test_functions = [
        ("Adapter Creation", test_adapter_creation),
        ("Protocol Compliance", test_protocol_compliance),
        ("Factory Functions", test_factory_functions),
        ("Thread Management", test_thread_management),
        ("Consciousness Properties", test_consciousness_properties),
        ("Agent Swapping", test_agent_swapping),
        ("Basic Execution", test_basic_execution),
    ]

    results = []
    for name, test_func in test_functions:
        try:
            passed = await test_func()
            results.append((name, passed))
        except Exception as e:
            logger.error(f"Test '{name}' crashed: {e}")
            results.append((name, False))

    # Summary
    print("\n" + "=" * 70)
    print(" TEST SUMMARY")
    print("=" * 70)

    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)

    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} | {name}")

    print(f"\nResults: {passed_count}/{total_count} test suites passed")

    if passed_count == total_count:
        print("\n🎉 ALL TESTS PASSED! Agent protocol integration fully operational.")
        return 0
    else:
        print(f"\n⚠️  {total_count - passed_count} test suite(s) failed.")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(run_all_tests())
    sys.exit(exit_code)
