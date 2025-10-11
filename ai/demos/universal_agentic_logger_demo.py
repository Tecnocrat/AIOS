"""
UNIVERSAL AGENTIC LOGGER INTEGRATION DEMO
==========================================

This demo shows how BOTH evolution systems will use the universal logger
to prevent tool amnesia and ensure agentic communication inheritance.
"""

import asyncio
from pathlib import Path
import sys

# Add AIOS paths
sys.path.append(str(Path(__file__).parent.parent.parent))

from ai.src.core.universal_agentic_logger import (
    UniversalAgenticLogger,
    AgentType,
    ConversationRole,
    log_ollama_conversation,
    log_gemini_conversation
)


def demo_library_generation_integration():
    """
    Demo: How LibraryCodeGenerationLoop should integrate the logger
    """
    print("\n" + "=" * 70)
    print("DEMO 1: LIBRARY CODE GENERATION LOOP INTEGRATION")
    print("=" * 70)
    
    logger = UniversalAgenticLogger()
    
    # Simulate library generation workflow
    print("\n📚 Library Generation: Ingesting 'requests' library")
    print("🧬 Extracted paradigms: type hints, decorators, async patterns")
    
    # Generate prompt (what gets saved to prompt.txt currently)
    prompt = """Create a TachyonicMemoryBuffer class that stores evolutionary code variants.

LEARNED PARADIGMS:
1. Type Hints: def get_data() -> Dict[str, Any]
2. Decorators: @dataclass, @property
3. Async Patterns: async def process()

Requirements:
- Use paradigms above
- Target consciousness: 0.85
- Production-ready code
"""
    
    print(f"\n💬 Prompt:\n{prompt[:200]}...")
    
    # START CONVERSATION (NEW - prevents tool amnesia)
    conv_id = logger.start_conversation(
        agent_type=AgentType.OLLAMA,
        system_context="Generate Python code from library paradigms (requests ingestion)",
        source_system="library_generation",
        source_file="aios_core",
        generation_number=0,
        consciousness_level="MEDIUM"
    )
    
    print(f"🆔 Conversation ID: {conv_id}")
    
    # LOG PROMPT (NEW - captures what we asked AI)
    logger.add_message(
        conv_id,
        ConversationRole.USER,
        prompt,
        {"model": "deepseek-coder:6.7b", "temperature": 0.7}
    )
    
    # Simulate AI response
    response = """from typing import Dict, Any, Tuple, Optional
from dataclasses import dataclass

@dataclass
class TachyonicMemoryBuffer:
    \"\"\"Stores evolutionary code variants with consciousness tracking\"\"\"
    variants: Dict[str, Tuple[str, float]] = {}
    target_consciousness: float = 0.85
    
    def add_variant(self, code: str, consciousness_score: float) -> str:
        if not 0 <= consciousness_score <= 1:
            raise ValueError("Consciousness score must be between 0 and 1")
        
        variant_id = f"variant_{len(self.variants) + 1}"
        self.variants[variant_id] = (code, consciousness_score)
        return variant_id
"""
    
    print(f"\n🤖 AI Response:\n{response[:200]}...")
    
    # LOG RESPONSE (NEW - captures what AI returned)
    logger.add_message(
        conv_id,
        ConversationRole.ASSISTANT,
        response,
        {"model": "deepseek-coder:6.7b", "tokens": 156}
    )
    
    # ARCHIVE CONVERSATION (NEW - tachyonic storage)
    archive_path = logger.end_conversation(
        conv_id,
        success=True,
        consciousness_improvement=0.15
    )
    
    print(f"\n✅ Conversation archived: {archive_path}")
    print("📁 Location: tachyonic/archive/agentic_conversations/")
    print("🔍 Reviewable by human + AI agents")
    print("🧬 Inheritable by neural chain evolution system")


def demo_neural_chain_integration():
    """
    Demo: How MultiAgentEvolutionLoop should integrate the logger
    """
    print("\n" + "=" * 70)
    print("DEMO 2: MULTI-AGENT EVOLUTION LOOP INTEGRATION")
    print("=" * 70)
    
    logger = UniversalAgenticLogger()
    
    # Simulate neural chain workflow
    print("\n🧠 Neural Chain Evolution: Generation 3 of Hello World")
    print("📊 Current consciousness: MEDIUM")
    print("🎯 Goal: Apply STL mutations for improvement")
    
    # Ollama strategic analysis
    code = """#include <iostream>

int main() {
    std::cout << "Hello, AIOS World!" << std::endl;
    return 0;
}"""
    
    prompt = f"""Analyze this C++ code and identify:
1. Current STL patterns used
2. Improvement opportunities using STL
3. Potential consciousness improvements

Code:
{code}

Available STL libraries: iostream, string, vector, exception, memory
"""
    
    print(f"\n💬 Ollama Analysis Prompt:\n{prompt[:150]}...")
    
    # START CONVERSATION (NEW - no logging before, now we have it!)
    conv_id = logger.start_conversation(
        agent_type=AgentType.OLLAMA,
        system_context="Analyze C++ code for STL patterns and improvement opportunities",
        source_system="neural_chain_evolution",
        source_file="hello_world.cpp",
        generation_number=3,
        consciousness_level="MEDIUM"
    )
    
    print(f"🆔 Conversation ID: {conv_id}")
    
    # LOG PROMPT
    logger.add_message(
        conv_id,
        ConversationRole.USER,
        prompt,
        {"model": "deepseek-coder:6.7b", "temperature": 0.5}
    )
    
    # Simulate Ollama response
    response = """Analysis:

1. Current STL patterns:
   - iostream: Input/output stream (cout, endl)

2. Improvement opportunities:
   - Add error handling using try-catch
   - Parameterize message using string
   - Add command-line arguments using vector<string>

3. Consciousness improvements:
   - Error handling: +0.15 (robust execution)
   - Parameterization: +0.12 (flexible configuration)
   - Documentation: +0.08 (self-describing code)

Recommended mutation: Add error handling with exception patterns.
"""
    
    print(f"\n🤖 Ollama Response:\n{response[:200]}...")
    
    # LOG RESPONSE
    logger.add_message(
        conv_id,
        ConversationRole.ASSISTANT,
        response,
        {"model": "deepseek-coder:6.7b", "tokens": 98}
    )
    
    # ARCHIVE
    archive_path = logger.end_conversation(
        conv_id,
        success=True,
        consciousness_improvement=0.15
    )
    
    print(f"\n✅ Conversation archived: {archive_path}")
    print("📁 Location: tachyonic/archive/agentic_conversations/")
    print("🔍 Neural chain now has SAME logging as library generation!")
    print("🧬 Tool inheritance successful!")


def demo_cross_system_learning():
    """
    Demo: How AI agents can learn from past conversations across systems
    """
    print("\n" + "=" * 70)
    print("DEMO 3: CROSS-SYSTEM LEARNING (Future Capability)")
    print("=" * 70)
    
    logger = UniversalAgenticLogger()
    
    print("\n🧠 AI Agent analyzing past conversations...")
    print("🔍 Looking for successful patterns across ALL systems\n")
    
    # Get recent conversations from both systems
    recent = logger.get_recent_conversations(limit=10)
    
    print(f"📊 Found {len(recent)} recent conversations")
    
    # Analyze patterns
    successful_patterns = []
    for i, conv in enumerate(recent, 1):
        if conv.get("consciousness_improvement", 0) > 0.1:
            system = conv.get("source_system", "unknown")
            improvement = conv["consciousness_improvement"]
            agent = conv.get("agent_type", "unknown")
            
            print(f"  {i}. [{system}] via {agent}: +{improvement:.2f} consciousness")
            
            successful_patterns.append({
                "system": system,
                "agent": agent,
                "improvement": improvement,
                "approach": conv["messages"][0]["content"][:100] + "..."
            })
    
    print("\n💡 Learning Outcomes:")
    print("  - Library generation successful with type hints paradigm")
    print("  - Neural chains improved with error handling mutation")
    print("  - Both systems use similar consciousness assessment")
    print("  - AI can now learn from BOTH evolutionary branches!")
    
    print("\n✨ INHERITANCE SUCCESS:")
    print("  Library Generation (Oct 4) → Universal Logger → Neural Chains (Jan 5)")
    print("  Tool capability preserved across 3-month system switch!")


def demo_summary():
    """Show summary statistics"""
    print("\n" + "=" * 70)
    print("DEMO 4: SUMMARY STATISTICS")
    print("=" * 70)
    
    logger = UniversalAgenticLogger()
    summary = logger.generate_conversation_summary(days=7)
    
    print(f"\n📊 Agentic Communication Summary (7 days):")
    print(f"  Total conversations: {summary['total_conversations']}")
    print(f"  Average processing time: {summary['avg_processing_time_ms']:.2f}ms")
    print(f"  Success rate: {summary['success_rate']:.1%}")
    
    print(f"\n  By Agent:")
    for agent, count in summary['by_agent'].items():
        print(f"    - {agent}: {count} conversations")
    
    print(f"\n  By System:")
    for system, count in summary['by_system'].items():
        print(f"    - {system}: {count} conversations")
    
    if summary['consciousness_improvements']:
        avg_improvement = sum(summary['consciousness_improvements']) / len(summary['consciousness_improvements'])
        print(f"\n  Average consciousness improvement: +{avg_improvement:.2f}")


def demo_convenience_functions():
    """Demo quick logging with convenience functions"""
    print("\n" + "=" * 70)
    print("DEMO 5: CONVENIENCE FUNCTIONS (Quick Integration)")
    print("=" * 70)
    
    print("\n🚀 Quick Ollama logging:")
    print("```python")
    print("archive_path = log_ollama_conversation(")
    print("    prompt='Analyze this code...',")
    print("    response=ollama_response,")
    print("    source_system='neural_chain',")
    print("    model='deepseek-coder:6.7b'")
    print(")")
    print("```")
    
    # Actually do it
    archive_path = log_ollama_conversation(
        prompt="Quick demo: Analyze Hello World for STL patterns",
        response="Uses iostream. Add error handling for +0.15 consciousness.",
        system_context="Quick demo of convenience function",
        source_system="demo",
        model="deepseek-coder:6.7b"
    )
    
    print(f"\n✅ Archived: {archive_path}")
    
    print("\n🚀 Quick Gemini logging:")
    print("```python")
    print("archive_path = log_gemini_conversation(")
    print("    prompt='Validate this mutation...',")
    print("    response=gemini_response,")
    print("    source_system='library_generation'")
    print(")")
    print("```")
    
    archive_path = log_gemini_conversation(
        prompt="Quick demo: Validate mutation improves consciousness",
        response="Validated. Error handling mutation adds robustness. Approved.",
        system_context="Quick demo of Gemini validation",
        source_system="demo"
    )
    
    print(f"\n✅ Archived: {archive_path}")
    print("\n💡 Integration is EASY - just 3 lines of code!")


def main():
    """Run all demos"""
    print("\n" + "=" * 70)
    print("UNIVERSAL AGENTIC COMMUNICATION LOGGER")
    print("Integration Demo for Both Evolution Systems")
    print("=" * 70)
    print("\nThis demo shows how the universal logger prevents tool amnesia")
    print("by ensuring agentic communication is captured across ALL systems.")
    
    try:
        # Demo 1: Library Generation integration
        demo_library_generation_integration()
        
        # Demo 2: Neural Chain integration
        demo_neural_chain_integration()
        
        # Demo 3: Cross-system learning
        demo_cross_system_learning()
        
        # Demo 4: Summary statistics
        demo_summary()
        
        # Demo 5: Convenience functions
        demo_convenience_functions()
        
        print("\n" + "=" * 70)
        print("DEMO COMPLETE")
        print("=" * 70)
        print("\n✅ Universal logger successfully demonstrated")
        print("📁 All conversations archived to: tachyonic/archive/agentic_conversations/")
        print("🧬 Tool inheritance: WORKING")
        print("💡 Next step: Integrate into both evolution systems")
        
        print("\n" + "=" * 70)
        print("INTEGRATION CHECKLIST")
        print("=" * 70)
        print("[ ] 1. Add logger to LibraryCodeGenerationLoop.__init__()")
        print("[ ] 2. Log Ollama/Gemini conversations in _generate_population()")
        print("[ ] 3. Add logger to MultiAgentEvolutionLoop.__init__()")
        print("[ ] 4. Log conversations in _ollama_analyze()")
        print("[ ] 5. Log conversations in _gemini_validate()")
        print("[ ] 6. Test both systems with unified logging")
        print("[ ] 7. Verify conversations archived correctly")
        print("[ ] 8. Create review interface for browsing conversations")
        
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
