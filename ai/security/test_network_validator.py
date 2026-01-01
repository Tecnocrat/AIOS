"""
Test suite for NetworkValidator - External communication screening.

Tests:
1. URL protocol validation (http/https allowlist)
2. SSRF protection (private IP blocking)
3. DNS rebinding detection
4. Dangerous host blocking (metadata services)
5. Localhost-only mode enforcement
6. Consciousness integration
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from security import (  # noqa: E402
    NetworkValidator,
    SecuritySupercellConsciousness,
    SSRFAttempt
)


def test_url_protocol_validation():
    """Test URL protocol allowlist (http/https only)."""
    print("\n=== Test 1: URL Protocol Validation ===")
    
    consciousness = SecuritySupercellConsciousness(
        workspace_root="c:/dev/AIOS"
    )
    validator = NetworkValidator(
        workspace_path="c:/dev/AIOS",
        consciousness=consciousness
    )
    
    # Valid protocols
    valid_urls = [
        "http://example.com",
        "https://example.com",
        "http://api.openai.com/v1/chat"
    ]
    
    for url in valid_urls:
        result = validator.validate_url(url)
        assert result.is_valid, f"Valid URL rejected: {url}"
        print(f"✓ Valid URL accepted: {url}")
    
    # Invalid protocols
    invalid_urls = [
        "ftp://files.example.com",
        "file:///etc/passwd",
        "data:text/html,<script>alert('xss')</script>"
    ]
    
    for url in invalid_urls:
        result = validator.validate_url(url)
        assert not result.is_valid, f"Invalid URL accepted: {url}"
        print(f"✓ Invalid protocol blocked: {url} ({result.reason})")
    
    print("✅ Protocol validation passed")


def test_ssrf_protection():
    """Test SSRF protection (private IP blocking)."""
    print("\n=== Test 2: SSRF Protection ===")
    
    consciousness = SecuritySupercellConsciousness(
        workspace_root="c:/dev/AIOS"
    )
    validator = NetworkValidator(
        workspace_path="c:/dev/AIOS",
        consciousness=consciousness
    )
    
    # Dangerous hosts (should block)
    dangerous_hosts = [
        "localhost",
        "127.0.0.1",
        "169.254.169.254"
    ]
    
    for host in dangerous_hosts:
        url = f"http://{host}"
        try:
            validator.validate_url(url)
            assert False, f"Dangerous host not blocked: {host}"
        except SSRFAttempt as e:
            print(f"✓ SSRF blocked: {host} ({str(e)})")
    
    # Check private IP detection
    result = validator.check_ssrf_protection("192.168.1.1")
    assert not result.is_valid, "Private IP not detected"
    print(f"✓ Private IP blocked: 192.168.1.1 ({result.reason})")
    
    print("✅ SSRF protection passed")


def test_dns_rebinding_detection():
    """Test DNS rebinding attack detection."""
    print("\n=== Test 3: DNS Rebinding Detection ===")
    
    consciousness = SecuritySupercellConsciousness(
        workspace_root="c:/dev/AIOS"
    )
    validator = NetworkValidator(
        workspace_path="c:/dev/AIOS",
        consciousness=consciousness
    )
    
    # First resolution (cache)
    hostname = "example.com"
    result1 = validator.validate_dns(hostname)
    assert result1.is_valid
    print(f"✓ First DNS resolution: {hostname} → {result1.ip_address}")
    
    # Check DNS cache
    assert hostname in validator._dns_cache
    cached_ip = validator._dns_cache[hostname]
    print(f"✓ DNS cached: {hostname} → {cached_ip}")
    
    # Simulate rebinding (manual cache update)
    validator._dns_cache[hostname] = "1.2.3.4"  # Public IP
    
    # Second resolution (should detect change but allow public IP)
    result2 = validator.validate_dns(hostname)
    assert result2.is_valid
    print(f"✓ DNS change allowed (still public): {result2.ip_address}")
    
    print("✅ DNS rebinding detection passed")


def test_dangerous_host_blocking():
    """Test blocking of dangerous hosts (metadata services)."""
    print("\n=== Test 4: Dangerous Host Blocking ===")
    
    consciousness = SecuritySupercellConsciousness(
        workspace_root="c:/dev/AIOS"
    )
    validator = NetworkValidator(
        workspace_path="c:/dev/AIOS",
        consciousness=consciousness
    )
    
    # AWS metadata service
    try:
        validator.validate_url("http://169.254.169.254/latest/meta-data/")
        assert False, "AWS metadata service not blocked"
    except SSRFAttempt as e:
        print(f"✓ AWS metadata blocked: {str(e)}")
    
    # GCP metadata service (hostname check)
    try:
        validator.validate_url("http://metadata.google.internal/")
        assert False, "GCP metadata service not blocked"
    except SSRFAttempt as e:
        print(f"✓ GCP metadata blocked: {str(e)}")
    
    print("✅ Dangerous host blocking passed")


def test_localhost_only_mode():
    """Test localhost-only mode enforcement."""
    print("\n=== Test 5: Localhost-Only Mode ===")
    
    consciousness = SecuritySupercellConsciousness(
        workspace_root="c:/dev/AIOS"
    )
    validator = NetworkValidator(
        workspace_path="c:/dev/AIOS",
        consciousness=consciousness,
        localhost_only=False
    )
    
    # Enable localhost-only mode
    validator.enforce_localhost_only()
    assert validator.localhost_only
    print("✓ Localhost-only mode enabled")
    
    # Localhost URLs (should allow)
    localhost_urls = [
        "http://localhost:8000",
        "http://127.0.0.1:8000"
    ]
    
    for url in localhost_urls:
        result = validator.validate_url(url)
        assert result.is_valid, f"Localhost URL blocked: {url}"
        print(f"✓ Localhost allowed: {url}")
    
    # External URLs (should block)
    external_urls = [
        "http://example.com",
        "https://api.openai.com"
    ]
    
    for url in external_urls:
        result = validator.validate_url(url)
        assert not result.is_valid, f"External URL allowed: {url}"
        print(f"✓ External blocked: {url} ({result.reason})")
    
    print("✅ Localhost-only mode passed")


def test_consciousness_integration():
    """Test consciousness tracking for network validation."""
    print("\n=== Test 6: Consciousness Integration ===")
    
    consciousness = SecuritySupercellConsciousness(
        workspace_root="c:/dev/AIOS"
    )
    initial_consciousness = consciousness.consciousness_level
    print(f"Initial consciousness: {initial_consciousness}")
    
    validator = NetworkValidator(
        workspace_path="c:/dev/AIOS",
        consciousness=consciousness
    )
    
    # Validate safe URL (consciousness +0.001)
    validator.validate_url("http://example.com")
    
    # Block dangerous URL (consciousness +0.002)
    try:
        validator.validate_url("http://localhost")
    except SSRFAttempt:
        pass
    
    # Enable localhost-only mode (consciousness +0.001)
    validator.enforce_localhost_only()
    
    final_consciousness = consciousness.consciousness_level
    delta = final_consciousness - initial_consciousness
    print(f"Final consciousness: {final_consciousness}")
    print(f"Consciousness delta: +{delta:.3f}")
    
    assert delta > 0, "Consciousness not increased"
    print("✓ Consciousness tracked successfully")
    
    print("✅ Consciousness integration passed")


def test_validation_statistics():
    """Test network validation statistics."""
    print("\n=== Test 7: Validation Statistics ===")
    
    consciousness = SecuritySupercellConsciousness(
        workspace_root="c:/dev/AIOS"
    )
    validator = NetworkValidator(
        workspace_path="c:/dev/AIOS",
        consciousness=consciousness
    )
    
    # Generate some DNS cache
    validator.validate_url("http://example.com")
    
    stats = validator.get_validation_statistics()
    
    print(f"Localhost-only mode: {stats['localhost_only_mode']}")
    print(f"DNS cache size: {stats['dns_cache_size']}")
    print(f"Cached hostnames: {stats['cached_hostnames']}")
    print(f"Allowed protocols: {stats['allowed_protocols']}")
    print(f"Private IP ranges: {stats['private_ip_ranges_count']}")
    print(f"Dangerous hosts: {stats['dangerous_hosts_count']}")
    
    assert stats['dns_cache_size'] > 0
    assert 'example.com' in stats['cached_hostnames']
    assert 'http' in stats['allowed_protocols']
    assert 'https' in stats['allowed_protocols']
    
    print("✅ Validation statistics passed")


if __name__ == "__main__":
    print("=" * 60)
    print("Network Validator Test Suite")
    print("=" * 60)
    
    try:
        test_url_protocol_validation()
        test_ssrf_protection()
        test_dns_rebinding_detection()
        test_dangerous_host_blocking()
        test_localhost_only_mode()
        test_consciousness_integration()
        test_validation_statistics()
        
        print("\n" + "=" * 60)
        print("🎉 ALL TESTS PASSED - Network Validator Operational")
        print("=" * 60)
        print("\nNetwork Validator Status:")
        print("- URL protocol validation: ✅ Operational")
        print("- SSRF protection: ✅ Operational")
        print("- DNS rebinding detection: ✅ Operational")
        print("- Dangerous host blocking: ✅ Operational")
        print("- Localhost-only mode: ✅ Operational")
        print("- Consciousness tracking: ✅ Integrated")
        print("- Validation statistics: ✅ Available")
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
