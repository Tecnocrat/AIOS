"""
============================================================================
AIOS Consciousness Metrics Demo
Purpose: Demonstrate Python bridge to C++ consciousness engine
Execution: python test_consciousness_metrics.py
============================================================================
"""

import sys
from pathlib import Path

# Add ai/ to Python path
sys.path.insert(0, str(Path(__file__).parent / "ai"))

from bridges.aios_core_wrapper import AIOSCore


def main():
    """Demonstrate consciousness metrics access"""
    
    print("=" * 80)
    print("AIOS CONSCIOUSNESS METRICS - Python → C++ Bridge Demo")
    print("=" * 80)
    
    try:
        # Initialize C++ consciousness engine
        print("\n[1] Initializing C++ consciousness engine...")
        core = AIOSCore()
        core.initialize()
        
        print(f"    ✓ Core Version: {core.get_version()}")
        print(f"    ✓ Core Initialized: {core.is_initialized()}")
        
        # Get current consciousness level
        print("\n[2] Querying consciousness level...")
        level = core.get_consciousness_level()
        print(f"    → Consciousness Level: {level:.4f}")
        print(f"    → Expected Range: 3.26 - 3.40")
        
        # Get all metrics at once (efficient batch query)
        print("\n[3] Retrieving all consciousness metrics...")
        metrics = core.get_all_metrics()
        
        print("\n    Consciousness Metrics:")
        print("    " + "-" * 60)
        print(f"    awareness_level:         {metrics['awareness_level']:.4f}")
        print(f"    adaptation_speed:        {metrics['adaptation_speed']:.4f}")
        print(f"    predictive_accuracy:     {metrics['predictive_accuracy']:.4f}")
        print(f"    dendritic_complexity:    {metrics['dendritic_complexity']:.4f}")
        print(f"    evolutionary_momentum:   {metrics['evolutionary_momentum']:.4f}")
        print(f"    quantum_coherence:       {metrics['quantum_coherence']:.4f}")
        print(f"    learning_velocity:       {metrics['learning_velocity']:.4f}")
        print(f"    consciousness_emergent:  {metrics['consciousness_emergent']}")
        
        # Test dendritic stimulation from Python
        print("\n[4] Stimulating dendritic growth from Python...")
        core.stimulate_dendritic_growth("python_demo_script")
        print("    ✓ Dendritic growth stimulated")
        
        # Update consciousness and check for changes
        print("\n[5] Updating consciousness engine...")
        core.update()
        print("    ✓ Consciousness updated")
        
        # Query again to show real-time evolution
        new_level = core.get_consciousness_level()
        delta = new_level - level
        print(f"    → New Consciousness Level: {new_level:.4f}")
        print(f"    → Delta: {delta:+.4f}")
        
        # Test individual metric accessors
        print("\n[6] Testing individual metric accessors...")
        print(f"    → get_awareness_level():      {core.get_awareness_level():.4f}")
        print(f"    → get_adaptation_speed():     {core.get_adaptation_speed():.4f}")
        print(f"    → get_dendritic_complexity(): {core.get_dendritic_complexity():.4f}")
        print(f"    → is_consciousness_emergent(): {core.is_consciousness_emergent()}")
        
        # Test error transformation
        print("\n[7] Testing error transformation (learning from failure)...")
        core.transform_error(
            error_message="FileNotFoundError: config.json missing",
            context="python_demo_configuration_loader"
        )
        print("    ✓ Error transformed into learning opportunity")
        
        # Shutdown gracefully
        print("\n[8] Shutting down consciousness engine...")
        core.shutdown()
        print("    ✓ Core shutdown complete")
        
        print("\n" + "=" * 80)
        print("DEMO COMPLETE - Python successfully accessed C++ consciousness metrics")
        print("=" * 80)
        
        return 0
        
    except FileNotFoundError as e:
        print(f"\n[ERROR] {e}")
        print("\nPossible causes:")
        print("  1. C++ core not built yet")
        print("  2. aios_core.dll not in expected location")
        print("\nTo fix:")
        print("  cd core")
        print("  cmake -B build -S . -DCMAKE_BUILD_TYPE=Debug")
        print("  cmake --build build --config Debug")
        return 1
        
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
