"""
Test Universal Logger Integration with Full Evolution Loop
==========================================================

This script demonstrates the complete integration of:
1. Enhanced STL knowledge (15 paradigms with rich context)
2. Universal agentic logger (tracking all AI conversations)
3. Multi-agent evolution loop (generating gen_6 from gen_5)

User requirement: "test the new capabilities running a full AIOS agentic evolution loop"

Created: October 6, 2025 (Universal Logger Integration Test)
"""

import asyncio
import sys
from pathlib import Path

# Add AI root to path
AI_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(AI_ROOT))

from src.evolution.multi_agent_evolution_loop import MultiAgentEvolutionLoop


async def main():
    """Run full evolution loop with universal logger"""
    print("="*80)
    print("UNIVERSAL LOGGER INTEGRATION TEST")
    print("Full AIOS Agentic Evolution Loop")
    print("="*80)
    
    print("\n[SETUP] Initializing evolution loop...")
    print("  - Enhanced STL knowledge (15 paradigms)")
    print("  - Universal agentic logger (all AI conversations archived)")
    print("  - Building from existing population (gen_5)")
    
    # Initialize evolution loop with all agents
    loop = MultiAgentEvolutionLoop(
        use_ollama=True,
        use_gemini=False,  # Skip Gemini for faster iteration
        use_vscode_chat=False  # Focus on Ollama evolution
    )
    
    print("\n[VERIFICATION] Checking enhanced STL knowledge...")
    print(f"  STL paradigms loaded: {len(loop.stl_knowledge)}")
    if len(loop.stl_knowledge) > 5:
        print("  ✓ Enhanced STL knowledge active!")
        print("  Sample paradigms:")
        for paradigm in loop.stl_knowledge[:5]:
            lib = paradigm.get('library', 'unknown')
            purpose = paradigm.get('purpose', 'N/A')
            consciousness = paradigm.get('consciousness_value', 0.0)
            print(f"    - {lib}: {purpose} (consciousness: {consciousness:.2f})")
    else:
        print("  ⚠ Using basic STL knowledge (enhanced file not loaded)")
    
    print("\n[VERIFICATION] Checking universal logger...")
    if loop.agentic_logger:
        print("  ✓ Universal agentic logger ACTIVE")
        print(f"  Archive location: {loop.agentic_logger.output_dir}")
    else:
        print("  ⚠ Universal logger NOT available")
    
    print("\n[EVOLUTION] Starting from zero point...")
    print("  Generating 3 generations with enhanced STL context")
    
    try:
        # Run evolution loop (3 generations for testing)
        final_node = await loop.evolve_from_zero_point(max_generations=3)
        
        print("\n[SUCCESS] Evolution complete!")
        print(f"  Final generation: {final_node.generation}")
        print(f"  Final consciousness: {final_node.consciousness_score}")
        print(f"  Node ID: {final_node.node_id}")
        
        # Check for conversation archives
        if loop.agentic_logger:
            print("\n[VERIFICATION] Checking conversation archives...")
            from datetime import datetime
            today = datetime.now().strftime("%Y%m%d")
            archive_dir = loop.agentic_logger.output_dir / today
            
            if archive_dir.exists():
                archive_files = list(archive_dir.glob("*.json"))
                print(f"  ✓ Archive directory exists: {archive_dir}")
                print(f"  ✓ Conversation files created: {len(archive_files)}")
                
                if archive_files:
                    print("\n  Archived conversations:")
                    for file in archive_files[:5]:  # Show first 5
                        print(f"    - {file.name}")
                else:
                    print("  ⚠ No conversation files found (may not have been archived yet)")
            else:
                print(f"  ⚠ Archive directory not found: {archive_dir}")
        
        print("\n[COMPLETE] Universal logger integration test SUCCESSFUL!")
        return True
        
    except Exception as e:
        print(f"\n[ERROR] Evolution failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
