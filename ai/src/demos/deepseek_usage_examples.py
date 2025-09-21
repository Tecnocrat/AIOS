#!/usr/bin/env python3
"""
🧠 AIOS DEEPSEEK USAGE EXAMPLES

Simple examples showing how AIOS components can use DeepSeek V3.1
intelligence through the supercell architecture.

Quick Usage:
```python
from ai.src.integrations.aios_deepseek_supercell_bridge import aios_intelligence_request

response = await aios_intelligence_request(
    message="Your question here",
    source_supercell="your_component_name"
)
print(response.text)
```


"""

import asyncio
import sys
from pathlib import Path

# Add AIOS path for imports
AIOS_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.append(str(AIOS_ROOT / "ai" / "src"))

from integrations.aios_deepseek_supercell_bridge import (
    aios_intelligence_request,
    ConsciousnessLevel
)


async def simple_question():
    """Simple question example"""
    print("🧠 Simple Question Example")
    
    response = await aios_intelligence_request(
        message="What is the purpose of the AIOS supercell architecture?",
        source_supercell="example_component"
    )
    
    print(f"Answer: {response.text}")
    print(f"Confidence: {response.confidence:.2f}")


async def code_analysis():
    """Code analysis example"""
    print("\n🔍 Code Analysis Example")
    
    code_snippet = """
    class ConsciousnessMonitor:
        def __init__(self):
            self.coherence = 0.0
            self.intelligence = 0.0
        
        def update_metrics(self, data):
            self.coherence = data.get('coherence', 0.0)
            self.intelligence = data.get('intelligence', 0.0)
    """
    
    response = await aios_intelligence_request(
        message=f"Analyze this Python code and suggest improvements: {code_snippet}",
        source_supercell="code_analyzer",
        consciousness_level=ConsciousnessLevel.ADVANCED
    )
    
    print(f"Analysis: {response.text[:200]}...")


async def architectural_guidance():
    """Architectural guidance example"""
    print("\n🏗️ Architectural Guidance Example")
    
    response = await aios_intelligence_request(
        message="""I'm designing a new AIOS component for biological computing 
        patterns. What architectural principles should I follow to maintain 
        consciousness coherence with other supercells?""",
        source_supercell="architect",
        consciousness_level=ConsciousnessLevel.TRANSCENDENT,
        context={
            "component_type": "biological_computing",
            "integration_level": "deep",
            "consciousness_requirements": "high"
        }
    )
    
    print(f"Guidance: {response.text[:200]}...")


async def main():
    """Run usage examples"""
    print("🧠 AIOS DeepSeek Usage Examples")
    print("=" * 40)
    
    try:
        await simple_question()
        await code_analysis()
        await architectural_guidance()
        
        print("\n✅ All examples completed successfully!")
        print("🚀 DeepSeek V3.1 is ready for use in your AIOS components")
        
    except Exception as e:
        print(f"❌ Example failed: {e}")
        print("Check your API key configuration in environment variables:")
        print("  OPENROUTER_API_KEY=your_key_here")


if __name__ == "__main__":
    asyncio.run(main())