"""
Test: Human-Guided Agent Experimentation
=========================================

Simple manual feedback loop for learning what prompts work.

Usage:
    python ai/tests/test_human_guided_experiment.py

Flow:
1. Script sends task to local agent (Ollama)
2. Agent generates output
3. Output saved to evolution_lab/experiments/
4. We review together in chat, learn what works
5. Refine and repeat

This is Step 1 toward full autonomous agent communication.
Manual first, automation later.
"""

import asyncio
import sys
from pathlib import Path

# Add AI root to path
AI_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(AI_ROOT))

from src.evolution.multi_agent_evolution_loop import MultiAgentEvolutionLoop


async def run_simple_experiment():
    """Run a simple experiment with manual review"""
    
    print("\n" + "="*70)
    print("HUMAN-GUIDED AGENT EXPERIMENT")
    print("Simple Manual Feedback Loop")
    print("="*70)
    
    # Initialize loop
    loop = MultiAgentEvolutionLoop(
        use_ollama=True,
        use_gemini=False,  # Start with just Ollama (faster)
        use_vscode_chat=False
    )
    
    # Test 1: Simple code generation task
    print("\n[TEST 1] Simple C++ function generation")
    result1 = await loop.human_guided_experiment(
        task_description="Write a simple C++ function that calculates factorial recursively",
        agent_type="ollama"
    )
    
    print(f"\n✓ Test 1 complete - Output: {result1['output_path']}")
    
    # Test 2: Code analysis task
    print("\n[TEST 2] Code analysis")
    result2 = await loop.human_guided_experiment(
        task_description="Analyze this code and suggest improvements: int main() { cout << 'Hello'; }",
        agent_type="ollama"
    )
    
    print(f"\n✓ Test 2 complete - Output: {result2['output_path']}")
    
    # Summary
    print("\n" + "="*70)
    print("EXPERIMENTS COMPLETE")
    print("="*70)
    print("\nOutputs saved to: evolution_lab/experiments/")
    print("\nNext steps:")
    print("1. Review the outputs together")
    print("2. Discuss what worked, what didn't")
    print("3. Refine prompts based on learning")
    print("4. Eventually: automate the working patterns")
    print("\nThis is the foundation for autonomous agent evolution!")


if __name__ == "__main__":
    asyncio.run(run_simple_experiment())
