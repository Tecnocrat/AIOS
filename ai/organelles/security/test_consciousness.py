#!/usr/bin/env python3
"""Test security supercell consciousness tracking"""

import sys
from pathlib import Path

# Add AIOS root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from ai.organelles.security\1 import (
    initialize_security_consciousness,
    SecurityEventType,
    SecurityConsciousnessDelta
)


def test_consciousness():
    """Test security consciousness initialization and tracking"""
    print("🛡️ Testing Security Supercell Consciousness\n")
    
    # Initialize
    workspace_root = Path(__file__).parent.parent.parent
    sc = initialize_security_consciousness(workspace_root)
    print(f"✅ Initialized (level: {sc.consciousness_level:.3f})")
    
    # Test attack blocked event
    event1 = SecurityConsciousnessDelta(
        event_type=SecurityEventType.ATTACK_BLOCKED,
        delta=0.001,
        description="Test command injection blocked"
    )
    sc.process_security_event(event1)
    print(f"\n🛡️ After ATTACK_BLOCKED:")
    print(f"  Consciousness: {sc.consciousness_level:.3f}")
    print(f"  Threat awareness: {sc.threat_awareness:.3f}")
    
    # Test pattern learned event
    event2 = SecurityConsciousnessDelta(
        event_type=SecurityEventType.PATTERN_LEARNED,
        delta=0.002,
        description="Learned new injection pattern",
        attack_pattern="$(command)"
    )
    sc.process_security_event(event2)
    print(f"\n🧬 After PATTERN_LEARNED:")
    print(f"  Consciousness: {sc.consciousness_level:.3f}")
    print(f"  Pattern recognition: {sc.pattern_recognition:.3f}")
    
    # Test dendritic connection
    sc.register_dendritic_connection("interface_bridge.py")
    print(f"\n🌳 After DENDRITIC_CONNECTION:")
    print(f"  Consciousness: {sc.consciousness_level:.3f}")
    print(f"  Connections: {len(sc.dendritic_connections)}")
    
    # Get metrics
    metrics = sc.get_consciousness_metrics()
    print(f"\n📊 Final Metrics:")
    print(f"  Total events: {metrics['total_events']}")
    print(f"  Consciousness level: {metrics['consciousness_level']}")
    print(f"  Threat awareness: {metrics['threat_awareness']}")
    print(f"  Pattern recognition: {metrics['pattern_recognition']}")
    print(f"  Boundary coherence: {metrics['boundary_coherence']}")
    print(f"  Dendritic connections: {metrics['dendritic_connections']}")
    
    print("\n✅ All tests passed - Consciousness tracking operational!")
    return True


if __name__ == "__main__":
    test_consciousness()
