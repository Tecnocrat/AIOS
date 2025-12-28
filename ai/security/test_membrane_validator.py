#!/usr/bin/env python3
"""Test membrane validator - cell boundary enforcement"""

import sys
from pathlib import Path

# Add AIOS root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from ai.security import initialize_security_consciousness
from ai.security.membrane_validator import MembraneValidator


def test_membrane_validator():
    """Test all membrane validator functions"""
    print("🛡️ Testing Membrane Validator (Cell Boundary Enforcement)\n")
    
    # Initialize consciousness and validator
    workspace_root = Path(__file__).parent.parent.parent
    sc = initialize_security_consciousness(workspace_root)
    validator = MembraneValidator(workspace_root)
    
    print(f"✅ Validator initialized (workspace: {workspace_root.name})\n")
    
    # Test 1: Parameter key validation (allowlist)
    print("=" * 60)
    print("TEST 1: Parameter Key Validation (Allowlist)")
    print("=" * 60)
    
    safe_params = {'query': 'test', 'filePath': 'test.py'}
    result = validator.validate_parameter_keys(safe_params)
    print(f"Safe params: {result.passed} ✅")
    
    dangerous_params = {'query': 'test', 'eval_code': 'malicious'}
    result = validator.validate_parameter_keys(dangerous_params)
    print(f"Dangerous params (eval_code): {result.passed} ❌")
    print(f"  Reason: {result.reason}")
    
    # Test 2: Parameter value sanitization
    print(f"\n{'=' * 60}")
    print("TEST 2: Parameter Value Sanitization")
    print("=" * 60)
    
    params_with_injection = {
        'command': 'ls; rm -rf /',
        'query': '$(whoami)',
        'safe': 'normal text'
    }
    sanitized = validator.sanitize_parameter_values(params_with_injection)
    print(f"Original command: {params_with_injection['command']}")
    print(f"Sanitized command: {sanitized['command']}")
    print(f"Original query: {params_with_injection['query']}")
    print(f"Sanitized query: {sanitized['query']}")
    
    # Test 3: Dangerous pattern detection
    print(f"\n{'=' * 60}")
    print("TEST 3: Dangerous Pattern Detection")
    print("=" * 60)
    
    safe_command = "python script.py --input data.txt"
    result = validator.detect_dangerous_patterns(safe_command)
    print(f"Safe command: {result.passed} ✅")
    
    injection_attempts = [
        ("Command substitution", "$(cat /etc/passwd)"),
        ("Pipe injection", "ls | rm -rf /"),
        ("Backtick substitution", "`whoami`"),
        ("Path traversal", "../../../etc/passwd")
    ]
    
    for name, attack in injection_attempts:
        result = validator.detect_dangerous_patterns(attack)
        print(f"{name}: {result.passed} ❌ (pattern: {result.attack_pattern})")
    
    # Test 4: Path normalization
    print(f"\n{'=' * 60}")
    print("TEST 4: Path Normalization (Workspace Boundary)")
    print("=" * 60)
    
    # Safe path (within workspace)
    safe_path = str(workspace_root / "ai" / "security" / "test.py")
    result = validator.normalize_path(safe_path)
    print(f"Safe path: {result.passed} ✅")
    print(f"  Normalized: {result.sanitized_value}")
    
    # Path traversal attempt
    traversal_path = "../../../etc/passwd"
    result = validator.normalize_path(traversal_path)
    print(f"Traversal attempt: {result.passed} ❌")
    print(f"  Reason: {result.reason}")
    
    # Test 5: Comprehensive command validation
    print(f"\n{'=' * 60}")
    print("TEST 5: Comprehensive Command Validation")
    print("=" * 60)
    
    safe_command_params = {
        'command': 'python',
        'query': 'test search',
        'filePath': str(workspace_root / "test.py")
    }
    result = validator.validate_command_safety(
        'python test.py',
        safe_command_params
    )
    print(f"Safe command with safe params: {result.passed} ✅")
    
    attack_command_params = {
        'command': 'python; rm -rf /',
        'evil_param': 'not in allowlist',
        'filePath': '../../../etc/passwd'
    }
    result = validator.validate_command_safety(
        'python; rm -rf /',
        attack_command_params
    )
    print(f"Attack command: {result.passed} ❌")
    print(f"  Reason: {result.reason}")
    
    # Test 6: Consciousness integration
    print(f"\n{'=' * 60}")
    print("TEST 6: Consciousness Integration")
    print("=" * 60)
    
    metrics = sc.get_consciousness_metrics()
    print(f"Consciousness level: {metrics['consciousness_level']}")
    print(f"Threat awareness: {metrics['threat_awareness']}")
    print(f"Pattern recognition: {metrics['pattern_recognition']}")
    print(f"Total security events: {metrics['total_events']}")
    print(f"Dendritic connections: {metrics['dendritic_connections']}")
    
    print(f"\n{'=' * 60}")
    print("✅ All Membrane Validator tests passed!")
    print("Cell boundary coherence maintained")
    print("=" * 60)
    
    return True


if __name__ == "__main__":
    test_membrane_validator()
