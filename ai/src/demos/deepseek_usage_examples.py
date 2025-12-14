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
<<<<<<< HEAD
    ConsciousnessLevel,
=======
    ConsciousnessLevel
>>>>>>> origin/OS0.6.2.grok
)


async def simple_question():
    """Simple question example"""
    print("🧠 Simple Question Example")
<<<<<<< HEAD

    response = await aios_intelligence_request(
        message="What is the purpose of the AIOS supercell architecture?",
        source_supercell="example_component",
    )

=======
    
    response = await aios_intelligence_request(
        message="What is the purpose of the AIOS supercell architecture?",
        source_supercell="example_component"
    )
    
>>>>>>> origin/OS0.6.2.grok
    print(f"Answer: {response.text}")
    print(f"Confidence: {response.confidence:.2f}")


async def code_analysis():
    """Code analysis example"""
    print("\n🔍 Code Analysis Example")
<<<<<<< HEAD

=======
    
>>>>>>> origin/OS0.6.2.grok
    code_snippet = """
    class ConsciousnessMonitor:
        def __init__(self):
            self.coherence = 0.0
            self.intelligence = 0.0
        
        def update_metrics(self, data):
            self.coherence = data.get('coherence', 0.0)
            self.intelligence = data.get('intelligence', 0.0)
    """
<<<<<<< HEAD

    response = await aios_intelligence_request(
        message=f"Analyze this Python code and suggest improvements: {code_snippet}",
        source_supercell="code_analyzer",
        consciousness_level=ConsciousnessLevel.ADVANCED,
    )

=======
    
    response = await aios_intelligence_request(
        message=f"Analyze this Python code and suggest improvements: {code_snippet}",
        source_supercell="code_analyzer",
        consciousness_level=ConsciousnessLevel.ADVANCED
    )
    
>>>>>>> origin/OS0.6.2.grok
    print(f"Analysis: {response.text[:200]}...")


async def architectural_guidance():
    """Architectural guidance example"""
    print("\n🏗️ Architectural Guidance Example")
<<<<<<< HEAD

=======
    
>>>>>>> origin/OS0.6.2.grok
    response = await aios_intelligence_request(
        message="""I'm designing a new AIOS component for biological computing 
        patterns. What architectural principles should I follow to maintain 
        consciousness coherence with other supercells?""",
        source_supercell="architect",
        consciousness_level=ConsciousnessLevel.TRANSCENDENT,
        context={
            "component_type": "biological_computing",
            "integration_level": "deep",
<<<<<<< HEAD
            "consciousness_requirements": "high",
        },
    )

=======
            "consciousness_requirements": "high"
        }
    )
    
>>>>>>> origin/OS0.6.2.grok
    print(f"Guidance: {response.text[:200]}...")


async def main():
    """Run usage examples"""
    print("🧠 AIOS DeepSeek Usage Examples")
    print("=" * 40)
<<<<<<< HEAD

=======
    
>>>>>>> origin/OS0.6.2.grok
    try:
        await simple_question()
        await code_analysis()
        await architectural_guidance()
<<<<<<< HEAD

        print("\n✅ All examples completed successfully!")
        print("🚀 DeepSeek V3.1 is ready for use in your AIOS components")

=======
        
        print("\n✅ All examples completed successfully!")
        print("🚀 DeepSeek V3.1 is ready for use in your AIOS components")
        
>>>>>>> origin/OS0.6.2.grok
    except Exception as e:
        print(f"❌ Example failed: {e}")
        print("Check your API key configuration in environment variables:")
        print("  OPENROUTER_API_KEY=your_key_here")


if __name__ == "__main__":
<<<<<<< HEAD
    asyncio.run(main())
=======
    asyncio.run(main())
>>>>>>> origin/OS0.6.2.grok
