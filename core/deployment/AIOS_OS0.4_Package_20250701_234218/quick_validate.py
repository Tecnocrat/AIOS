"""
Quick AIOS OS0.4 Validation Script
=================================

Performs basic validation of AIOS OS0.4 installation.
"""

import sys
from pathlib import Path

def validate_installation():
    print("🔍 AIOS OS0.4 Quick Validation")
    print("=" * 35)
    
    # Check Python version
    if sys.version_info >= (3, 12):
        print("✅ Python version: OK")
    else:
        print("❌ Python version: Requires 3.12+")
        return False
    
    # Check core files
    core_files = [
        "aios_consciousness_engine.py",
        "aios_visual_interface.py", 
        "aios_system_intelligence.py"
    ]
    
    missing_files = []
    for file_name in core_files:
        if not (Path("core") / file_name).exists():
            missing_files.append(file_name)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    else:
        print("✅ Core files: OK")
    
    # Check GPU support
    try:
        import torch
        if torch.cuda.is_available():
            print(f"✅ GPU: {torch.cuda.get_device_name(0)}")
        else:
            print("⚠️  GPU: CUDA not available")
    except ImportError:
        print("❌ GPU: PyTorch not installed")
        return False
    
    # Test basic imports
    try:
        sys.path.insert(0, "core")
        from aios_system_intelligence import SystemIntelligenceManager
        print("✅ System Intelligence: OK")
    except Exception as e:
        print(f"❌ System Intelligence: {e}")
        return False
    
    print("✅ AIOS OS0.4 validation completed successfully!")
    return True

if __name__ == "__main__":
    try:
        success = validate_installation()
        if not success:
            print("\n🔧 Run bootstrap_install.py to fix issues")
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ Validation error: {e}")
        sys.exit(1)
