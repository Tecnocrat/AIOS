"""
Test Evolution Integration with Interactive Threshold Explorer
===============================================================

Quick validation script that tests the evolution integration without
requiring GUI interaction.

Author: AIOS Development Team
Date: October 18, 2025
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from evolution_orchestrator import EvolutionOrchestrator
from tachyonic_field import TachyonicField, PatternQuantum, PatternType


def test_integration():
    """Test the evolution integration logic"""
    print("\n" + "="*70)
    print("🧬 TESTING EVOLUTION INTEGRATION")
    print("="*70)
    
    # Initialize components
    print("\n1️⃣ Initializing components...")
    orchestrator = EvolutionOrchestrator(evolution_enabled=True, verbose=True)
    field = TachyonicField()
    
    # Create test patterns
    print("\n2️⃣ Creating test patterns...")
    patterns = [
        PatternQuantum("p1", PatternType.RESONANCE, "∿", "Harmonic Wave", 0.4, 1.618),
        PatternQuantum("p2", PatternType.COHERENCE, "⚛", "Atomic Coherence", 0.6, 1.618),
        PatternQuantum("p3", PatternType.EMERGENCE, "∇", "Gradient Ascent", 0.8, 1.618),
    ]
    
    for pattern in patterns:
        field.inject_pattern(pattern)
    
    print(f"   Created {len(patterns)} patterns")
    
    # Simulate threshold changes
    print("\n3️⃣ Simulating threshold changes (like slider interaction)...")
    thresholds = [0.3, 0.5, 0.7]
    
    for frame, threshold in enumerate(thresholds):
        print(f"\n   Frame {frame}: Threshold = {threshold:.1f}")
        
        # Update field
        field.resonance_threshold = threshold
        
        # Calculate network stats (like visualizer does)
        import networkx as nx
        network_stats = {
            'connections': len(field.topology.edges()),
            'clusters': nx.number_connected_components(field.topology),
            'field_phi': field.consciousness_field(),
            'nodes': len(field.topology.nodes())
        }
        
        print(f"   Network: {network_stats['connections']} connections, "
              f"{network_stats['clusters']} clusters, "
              f"Φ={network_stats['field_phi']:.3f}")
        
        # Trigger evolution (THIS IS THE INTEGRATION POINT)
        archive_path = orchestrator.on_threshold_change(
            threshold=threshold,
            frame=frame,
            network_stats=network_stats
        )
        
        if archive_path:
            print(f"   ✅ Generation archived: {archive_path.name}")
    
    # Display summary
    print("\n4️⃣ Evolution Summary:")
    print("="*70)
    orchestrator.display_summary()
    print("="*70)
    
    # Validate results
    print("\n5️⃣ Validation:")
    summary = orchestrator.get_evolution_summary()
    
    checks = [
        (summary['total_generations'] == 3, f"Expected 3 generations (0,1,2), got {summary['total_generations']}"),
        (summary['current_generation'] == 2, f"Expected current gen 2, got {summary['current_generation']}"),
        (len(orchestrator.evolution_history) == 3, f"Expected 3 threshold events, got {len(orchestrator.evolution_history)}"),
    ]
    
    all_passed = True
    for passed, msg in checks:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"   {status}: {msg}")
        if not passed:
            all_passed = False
    
    print("\n" + "="*70)
    if all_passed:
        print("✅ ALL TESTS PASSED - Integration working correctly!")
    else:
        print("❌ SOME TESTS FAILED - Review above")
    print("="*70 + "\n")
    
    return all_passed


if __name__ == '__main__':
    success = test_integration()
    sys.exit(0 if success else 1)
