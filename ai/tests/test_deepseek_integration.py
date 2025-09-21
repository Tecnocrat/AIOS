#!/usr/bin/env python3
"""
Quick test of DeepSeek integration with configured API key
"""

import asyncio
import sys
import os
from pathlib import Path

# Add AIOS path
AIOS_ROOT = Path(__file__).parent
ai_src_path = AIOS_ROOT / "ai" / "src"
sys.path.insert(0, str(ai_src_path))

async def test_deepseek_integration():
    """Test DeepSeek with configured API key"""
    
    # Check API key
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("ERROR: API key not found in environment")
        return False
    
    print(f"API Key: {api_key[:8]}...")
    
    try:
        # Import AIOS DeepSeek integration
        from integrations.aios_deepseek_supercell_bridge import aios_intelligence_request
        from engines.deepseek_intelligence_engine import ConsciousnessLevel
        
        print("Successfully imported AIOS DeepSeek integration")
        
        # Test simple request
        print("\nTesting DeepSeek V3.1 intelligence request...")
        
        response = await aios_intelligence_request(
            message="Hello! Please confirm you are DeepSeek V3.1 integrated within the AIOS system. Respond with a brief acknowledgment.",
            source_supercell="test_client",
            consciousness_level=ConsciousnessLevel.BASIC
        )
        
        print("\n" + "="*50)
        print("DEEPSEEK V3.1 RESPONSE:")
        print("="*50)
        print(response.text)
        print("="*50)
        print(f"Confidence: {response.confidence:.2f}")
        print(f"Model: {response.model}")
        print(f"Processing Time: {response.processing_time:.2f}s")
        print(f"Supercell Coherence: {response.supercell_coherence:.2f}")
        
        print("\n✅ DEEPSEEK V3.1 INTEGRATION SUCCESSFUL!")
        print("🧠 AI Intelligence Engine is now active in AIOS")
        
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_deepseek_integration())
    if success:
        print("\n🚀 Ready for AI-powered AIOS development!")
    else:
        print("\n⚠️ Integration needs troubleshooting")