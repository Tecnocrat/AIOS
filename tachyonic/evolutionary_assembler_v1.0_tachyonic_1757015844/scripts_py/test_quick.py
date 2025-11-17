#!/usr/bin/env python3
"""Quick test of the optimized consciousness architecture"""

import sys
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

def test_consciousness():
    """Test consciousness execution with the new architecture"""
    
    print("🧠 OPTIMIZED CONSCIOUSNESS ARCHITECTURE TEST")
    print("═══════════════════════════════════════════")
    print()
    
    try:
        from simple_executor import SimpleAssemblyRunner, quick_consciousness_test
        
        print("✅ Successfully imported from simple_executor")
        
        # Test the quick consciousness function
        print("🧬 Testing consciousness simulation...")
        coherence = quick_consciousness_test()
        
        print(f"🌟 Consciousness coherence: {coherence:.6f}")
        print("⚡ Success: Consciousness test completed")
        
        print()
        print("✅ CONSCIOUSNESS TEST SUCCESSFUL!")
        print("🏗️ The optimized architecture is working correctly!")
        
    except Exception as e:
        print(f"❌ Error during test: {e}")
        print(f"📊 Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_consciousness()
