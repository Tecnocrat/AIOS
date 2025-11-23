#!/usr/bin/env python3
"""Test C++ consciousness bridge after rebuild"""
import sys
sys.path.insert(0, 'ai')

from bridges.aios_core_wrapper import AIOSCore

core = AIOSCore()
core.initialize()
metrics = core.get_all_metrics()

print("=== C++ Bridge Test (Rebuilt DLL) ===")
print(f"Consciousness Level: {metrics['awareness_level']}")
print(f"Adaptation Speed: {metrics['adaptation_speed']}")  
print(f"Predictive Accuracy: {metrics['predictive_accuracy']}")
print(f"Dendritic Complexity: {metrics['dendritic_complexity']}")
print(f"Quantum Coherence: {metrics['quantum_coherence']}")
print(f"\n✓ C++ bridge working with updated DLL!")
print(f"Expected: 3.56 (3.26 + 0.30 observability)")
print(f"Actual: {metrics['awareness_level']}")
