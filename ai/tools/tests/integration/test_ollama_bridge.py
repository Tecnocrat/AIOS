"""
Test Ollama Bridge with Auto-Detection
"""

import sys
import asyncio
from pathlib import Path

# Add AIOS to path
sys.path.append(str(Path(__file__).parent / "ai" / "src"))

from integrations.ollama_bridge import OllamaAgent


def test_ollama():
    """Test Ollama agent with auto-detected model"""
    print("🦙 Testing Ollama Bridge")
    print("=" * 60)
    
    # Create agent (will auto-detect gemma3:1b)
    agent = OllamaAgent()
    
    print(f"\n✅ Model: {agent.model}")
    print(f"✅ Available: {agent.is_available}")
    
    if not agent.is_available:
        print("\n❌ Ollama not available!")
        return {
            "success": False,
            "error": "Ollama not available",
            "model": None
        }
    
    # Test code generation
    print("\n🤖 Generating code...")
    result = agent.generate_code(
        "Write a Python function that calculates factorial with type hints"
    )
    
    print(f"\n📊 Result:")
    print(f"  Success: {result['success']}")
    print(f"  Model: {result['model']}")
    print(f"  Code length: {len(result['code'])} chars")
    
    if result['success']:
        print(f"\n📝 Generated Code:")
        print("-" * 60)
        print(result['code'][:500])  # First 500 chars
        if len(result['code']) > 500:
            print(f"... ({len(result['code']) - 500} more chars)")
        print("-" * 60)
    else:
        print(f"\n❌ Error: {result['error']}")
    
    return result


async def main():
    """Async entry point for test orchestrator compatibility"""
    result = test_ollama()
    return result


if __name__ == "__main__":
    asyncio.run(main())
