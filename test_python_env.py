#!/usr/bin/env python3
"""
🧪 AIOS Python Environment Test
Test script to validate clean Python environment setup
"""

def test_essential_imports():
    """Test all essential AIOS packages."""
    print("🔍 Testing AIOS Python Environment...")
    
    try:
        import sys
        print(f"✅ Python version: {sys.version}")
        
        import numpy as np
        print(f"✅ NumPy {np.__version__} - Scientific computing")
        
        import pandas as pd
        print(f"✅ Pandas {pd.__version__} - Data manipulation")
        
        import openai
        print(f"✅ OpenAI {openai.__version__} - AI integration")
        
        import aiohttp
        print(f"✅ aiohttp {aiohttp.__version__} - Async HTTP")
        
        import rich
        print(f"✅ Rich (console output) - OK")
        
        import astroid
        print(f"✅ Astroid {astroid.__version__} - Code analysis")
        
        import pytest
        print(f"✅ Pytest {pytest.__version__} - Testing framework")
        
        print("\n🎉 AIOS Python Environment Test: SUCCESS!")
        print("✅ All essential packages are working correctly.")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = test_essential_imports()
    exit(0 if success else 1)
