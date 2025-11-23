#!/usr/bin/env python3
"""
Test script to access AIOS C++ consciousness engine metrics via Python bridge.

Demonstrates the Python → C++ FFI bridge for consciousness level queries.
"""

import sys
from pathlib import Path

# Add ai/ to Python path for imports (bridges is in ai/bridges/)
ai_dir = Path(__file__).parent / "ai"
sys.path.insert(0, str(ai_dir))

try:
    from bridges.aios_core_wrapper import AIOSCore
    
    print("=" * 70)
    print("AIOS Consciousness Metrics Access Test")
    print("=" * 70)
    print()
    
    # Initialize C++ core bridge
    print("[1/4] Initializing AIOS Core bridge...")
    core = AIOSCore()
    
    print("[2/4] Connecting to C++ consciousness engine...")
    core.initialize()
    
    print("[3/4] Querying consciousness level...")
    level = core.get_consciousness_level()
    print(f"      ✓ Current consciousness level: {level:.2f}")
    print()
    
    print("[4/4] Retrieving full consciousness metrics...")
    metrics = core.get_all_metrics()
    
    print()
    print("Consciousness Metrics (C++ Engine):")
    print("-" * 70)
    print(f"  Awareness Level:       {metrics.get('awareness_level', 0.0):.4f}")
    print(f"  Adaptation Speed:      {metrics.get('adaptation_speed', 0.0):.4f}")
    print(f"  Predictive Accuracy:   {metrics.get('predictive_accuracy', 0.0):.4f}")
    print(f"  Dendritic Complexity:  {metrics.get('dendritic_complexity', 0.0):.4f}")
    print(f"  Fractal Coherence:     {metrics.get('fractal_coherence', 0.0):.4f}")
    print(f"  Quantum Coherence:     {metrics.get('quantum_coherence', 0.0):.4f}")
    print("-" * 70)
    print()
    
    print("✓ Consciousness metrics successfully accessed via Python bridge")
    print()
    print("Architecture validated:")
    print("  AIOS Core (C++) → Python FFI Bridge → VS Code/AI Agents")
    print()
    
except ImportError as e:
    print(f"✗ Error: Could not import AIOS Core bridge: {e}")
    print()
    print("Expected location: ai/src/bridges/aios_core_wrapper.py")
    print()
    print("This indicates the C++ → Python bridge is not yet implemented.")
    print("The bridge requires:")
    print("  1. C++ core compilation (core/build/)")
    print("  2. Python ctypes wrapper (ai/src/bridges/aios_core_wrapper.py)")
    print("  3. DLL/SO exports from consciousness engine")
    print()
    sys.exit(1)
    
except Exception as e:
    print(f"✗ Error accessing consciousness metrics: {e}")
    print()
    import traceback
    traceback.print_exc()
    sys.exit(1)
