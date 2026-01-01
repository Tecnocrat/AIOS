#!/usr/bin/env python3
"""
Verify Gemini Bridge Setup
Tests that Gemini API is properly configured and working
"""

import os
import sys
import asyncio
from pathlib import Path

# Add AI src to path
sys.path.insert(0, str(Path(__file__).parent / "ai" / "src"))


async def main():
    print("\n🔍 Gemini Bridge Verification")
    print("=" * 60)
    
    # Check 1: API Key
    api_key = os.environ.get('GEMINI_API_KEY')
    if api_key:
        print(f"✅ API Key: Set ({api_key[:10]}...{api_key[-4:]})")
    else:
        print("❌ API Key: NOT SET")
        print("   Set with: $env:GEMINI_API_KEY = \"your-api-key\"")
        print("   Get key from: https://aistudio.google.com/app/apikey")
        return
    
    # Check 2: Package Installation
    try:
        import google.generativeai as genai
        print("✅ google-generativeai: Installed")
    except ImportError:
        print("❌ google-generativeai: NOT INSTALLED")
        print("   Install with: pip install google-generativeai")
        return
    
    # Check 3: Bridge Import
    try:
        from integrations.gemini_bridge.gemini_evolution_bridge import GeminiEvolutionBridge
        print("✅ GeminiEvolutionBridge: Importable")
    except ImportError as e:
        print(f"❌ GeminiEvolutionBridge: Import failed - {e}")
        return
    
    # Check 4: Initialize Bridge
    try:
        bridge = GeminiEvolutionBridge()
        print("✅ Bridge: Initialized")
    except Exception as e:
        print(f"❌ Bridge: Initialization failed - {e}")
        return
    
    # Check 5: Test Code Generation
    print("\n🧪 Testing code generation...")
    try:
        code = await bridge.generate_code(
            prompt="Write a Python function that returns 'Hello, AIOS!'",
            temperature=0.7,
            max_tokens=500
        )
        print("✅ Code Generation: SUCCESS")
        print(f"\n📝 Generated Code ({len(code)} chars):")
        print("-" * 60)
        print(code[:200] + ("..." if len(code) > 200 else ""))
        print("-" * 60)
    except Exception as e:
        print(f"❌ Code Generation: FAILED")
        print(f"   Error: {e}")
        return
    
    print("\n" + "=" * 60)
    print("🎉 Gemini Bridge is FULLY OPERATIONAL!")
    print("   Ready to use with library code generation loop")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
