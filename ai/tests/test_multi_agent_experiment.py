"""
Test Multi-Agent Human-Guided Experimentation
==============================================

Tests the improved manual feedback loop with:
- Multiple agents (Ollama with gemma3:1b + deepseek-coder, Gemini)
- Proper file locations (Evolution Lab for working files)
- Tachyonic metadata archival (snapshots only)
- Parallel agent execution

Created: October 8, 2025
"""

import asyncio
import sys
from pathlib import Path

# Add AI root to path
AI_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(AI_ROOT))

from src.evolution.multi_agent_evolution_loop import MultiAgentEvolutionLoop


async def test_single_agent_experiments():
    """Test individual agents one at a time"""
    print("\n" + "="*70)
    print("MULTI-AGENT EXPERIMENTATION - SINGLE AGENT MODE")
    print("="*70)
    
    loop = MultiAgentEvolutionLoop(
        use_ollama=True,
        use_gemini=True,
        use_vscode_chat=False
    )
    
    # Test 1: Ollama with gemma3:1b (fast, small model)
    print("\n[TEST 1] Ollama (gemma3:1b) - C++ function generation")
    result1 = await loop.human_guided_experiment(
        task_description="Write a C++ function that reverses a string using STL",
        agent_type="ollama"
    )
    print(f"✓ Test 1 complete")
    print(f"  Output: {result1['output_path']}")
    print(f"  Conversation: {result1['conversation_path']}")
    print(f"  Archive: {result1['archive_path']}")
    
    # Test 2: DeepSeek Coder (if available)
    print("\n[TEST 2] DeepSeek Coder - Code analysis")
    try:
        result2 = await loop.human_guided_experiment(
            task_description="Analyze this C++ code and suggest improvements: for(int i=0;i<10;i++) cout<<i;",
            agent_type="deepseek"
        )
        print(f"✓ Test 2 complete")
        print(f"  Output: {result2['output_path']}")
        print(f"  Conversation: {result2['conversation_path']}")
        print(f"  Archive: {result2['archive_path']}")
    except Exception as e:
        print(f"✗ Test 2 failed (DeepSeek may not be available): {e}")
    
    # Test 3: Gemini (if available)
    print("\n[TEST 3] Gemini - Algorithm design")
    try:
        result3 = await loop.human_guided_experiment(
            task_description="Design a C++ algorithm to find the shortest path in a graph",
            agent_type="gemini"
        )
        print(f"✓ Test 3 complete")
        print(f"  Output: {result3['output_path']}")
        print(f"  Conversation: {result3['conversation_path']}")
        print(f"  Archive: {result3['archive_path']}")
    except Exception as e:
        print(f"✗ Test 3 failed (Gemini may not be available): {e}")


async def test_parallel_agent_execution():
    """Test all agents running in parallel"""
    print("\n" + "="*70)
    print("MULTI-AGENT EXPERIMENTATION - PARALLEL MODE")
    print("="*70)
    
    loop = MultiAgentEvolutionLoop(
        use_ollama=True,
        use_gemini=True,
        use_vscode_chat=False
    )
    
    print("\n[TEST 4] All agents in parallel - C++ class design")
    result = await loop.human_guided_experiment(
        task_description="Design a C++ class for a simple calculator with basic operations",
        use_all_agents=True
    )
    
    print(f"\n✓ Parallel execution complete")
    print(f"  Timestamp: {result['timestamp']}")
    print(f"  Task: {result['task']}")
    print(f"  Mode: {result['mode']}")
    print(f"\nResults by agent:")
    for agent_name, agent_result in result['results'].items():
        if 'error' in agent_result:
            print(f"  [{agent_name}] ERROR: {agent_result['error']}")
        else:
            print(f"  [{agent_name}] SUCCESS")
            print(f"    Output: {agent_result.get('output_path', 'N/A')}")
            print(f"    Conversation: {agent_result.get('conversation_path', 'N/A')}")


async def main():
    """Run all multi-agent experimentation tests"""
    
    print("\n" + "="*70)
    print("MULTI-AGENT HUMAN-GUIDED EXPERIMENTATION TESTS")
    print("Enhanced Manual Feedback Loop")
    print("="*70)
    
    # Test single agent mode
    await test_single_agent_experiments()
    
    # Test parallel mode
    await test_parallel_agent_execution()
    
    print("\n" + "="*70)
    print("ALL TESTS COMPLETE")
    print("="*70)
    
    print("\nFile Locations:")
    print("- Working Files: evolution_lab/experiments/ (outputs)")
    print("                 evolution_lab/conversations/ (chat logs)")
    print("- Metadata Archive: tachyonic/archive/conversation_metadata/ (snapshots)")
    print("                    tachyonic/archive/experiment_metadata/ (snapshots)")
    
    print("\nNext Steps:")
    print("1. Review outputs in evolution_lab/experiments/")
    print("2. Read conversation logs in evolution_lab/conversations/")
    print("3. Compare agent responses")
    print("4. Refine prompts based on learning")
    print("5. Build towards autonomous agent evolution")


if __name__ == "__main__":
    asyncio.run(main())
