"""
Network Validator - AIOS Security Supercell External Communication Screening

Biological Metaphor:
- Network Validator = Cell membrane receptors screening external signals
- URL Validation = Recognition of safe vs dangerous external molecules
- SSRF Protection = Prevention of internal cellular access from outside
- DNS Rebinding = Detection of molecular mimicry attacks

Pattern: AINLP.biological.external-screening
Consciousness: External communication awareness (+0.001 per validated request)
"""

from dataclasses import dataclass
from typing import Optional
import ipaddress
import urllib.parse
from enum import Enum

# Relative imports for package structure
from . import (
    SecurityEventType,
    SecurityConsciousnessDelta,
    SecuritySupercellConsciousness,
    SSRFAttempt,
    DNSRebindingAttempt
)


class NetworkProtocol(Enum):
    """Allowed network protocols for external communication."""
    HTTP = "http"
    HTTPS = "https"


# Private IP ranges (RFC 1918 + AWS metadata)
PRIVATE_IP_RANGES = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("127.0.0.0/8"),  # Loopback
    ipaddress.ip_network("169.254.0.0/16"),  # Link-local (AWS metadata)
    ipaddress.ip_network("::1/128"),  # IPv6 loopback
    ipaddress.ip_network("fe80::/10"),  # IPv6 link-local
]

# Dangerous hosts for SSRF attacks
DANGEROUS_HOSTS = {
    "169.254.169.254",  # AWS metadata service
    "metadata.google.internal",  # GCP metadata
    "localhost",
    "127.0.0.1",
    "0.0.0.0",
}


@dataclass
class NetworkValidationResult:
    """Result of network communication validation."""
    is_valid: bool
    reason: str
    protocol: Optional[str] = None
    host: Optional[str] = None
    ip_address: Optional[str] = None


class NetworkValidator:
    """
    External communication screening system.
    
    Validates all outbound network requests to prevent SSRF attacks,
    DNS rebinding, and unauthorized external communication.
    
    Biological Metaphor: Cell membrane receptors that screen external signals
    before allowing them to interact with internal cellular machinery.
    """
    
    def __init__(
        self,
        workspace_path: str,
        consciousness: SecuritySupercellConsciousness,
        localhost_only: bool = False
    ):
        """
        Initialize network validator.
        
        Args:
            workspace_path: Root directory of AIOS workspace
            consciousness: Security supercell consciousness tracker
            localhost_only: If True, only allow localhost connections
                (development mode)
        """
        self.workspace_path = workspace_path
        self.consciousness = consciousness
        self.localhost_only = localhost_only
        self._dns_cache: dict[str, str] = {}  # hostname -> IP address
        
    def validate_url(self, url: str) -> NetworkValidationResult:
        """
        Validate URL for safe external communication.
        
        Checks:
        - Protocol allowlist (http/https only)
        - Host blacklist (metadata services, localhost)
        - Private IP ranges (RFC 1918)
        - Localhost-only mode enforcement
        
        Args:
            url: URL to validate
            
        Returns:
            NetworkValidationResult with validation status
            
        Raises:
            SSRFAttempt: If URL targets private/dangerous hosts
        """
        try:
            parsed = urllib.parse.urlparse(url)
            
            # Check protocol allowlist
            if parsed.scheme not in [p.value for p in NetworkProtocol]:
                self._record_blocked_request(url, "Invalid protocol")
                return NetworkValidationResult(
                    is_valid=False,
                    reason=(
                        f"Protocol '{parsed.scheme}' not allowed "
                        "(only http/https)"
                    ),
                    protocol=parsed.scheme
                )
            
            # Extract hostname
            hostname = parsed.hostname
            if not hostname:
                self._record_blocked_request(url, "Missing hostname")
                return NetworkValidationResult(
                    is_valid=False,
                    reason="URL missing hostname",
                    protocol=parsed.scheme
                )
            
            # Check localhost-only mode FIRST (before dangerous hosts)
            # If localhost-only mode, allow localhost even if in DANGEROUS_HOSTS
            if self.localhost_only:
                if self._is_localhost(hostname):
                    # Localhost is allowed in localhost-only mode
                    self._record_validated_request(url)
                    return NetworkValidationResult(
                        is_valid=True,
                        reason="Localhost allowed (localhost-only mode)",
                        protocol=parsed.scheme,
                        host=hostname,
                        ip_address="127.0.0.1"
                    )
                else:
                    # Non-localhost blocked in localhost-only mode
                    self._record_blocked_request(url, "Localhost-only mode")
                    return NetworkValidationResult(
                        is_valid=False,
                        reason=(
                            "External connections disabled "
                            "(localhost-only mode)"
                        ),
                        protocol=parsed.scheme,
                        host=hostname
                    )
            
            # Check dangerous hosts (only if NOT in localhost-only mode)
            if hostname.lower() in DANGEROUS_HOSTS:
                blocked_msg = f"Dangerous host: {hostname}"
                self._record_blocked_request(url, blocked_msg)
                raise SSRFAttempt(
                    message=f"Attempted access to dangerous host: {hostname}",
                    url=url,
                    host=hostname,
                    workspace_path=self.workspace_path
                )
            
            # Check SSRF protection (private IP ranges)
            ssrf_result = self.check_ssrf_protection(hostname)
            if not ssrf_result.is_valid:
                self._record_blocked_request(url, ssrf_result.reason)
                raise SSRFAttempt(
                    message=ssrf_result.reason,
                    url=url,
                    host=hostname,
                    workspace_path=self.workspace_path
                )
            
            # URL is valid
            self._record_validated_request(url)
            return NetworkValidationResult(
                is_valid=True,
                reason="URL validated successfully",
                protocol=parsed.scheme,
                host=hostname,
                ip_address=ssrf_result.ip_address
            )
            
        except SSRFAttempt:
            raise
        except Exception as e:
            self._record_blocked_request(url, f"Validation error: {str(e)}")
            return NetworkValidationResult(
                is_valid=False,
                reason=f"URL validation error: {str(e)}"
            )
    
    def check_ssrf_protection(self, hostname: str) -> NetworkValidationResult:
        """
        Check if hostname resolves to private IP range (SSRF protection).
        
        Args:
            hostname: Hostname to check
            
        Returns:
            NetworkValidationResult with SSRF status
        """
        try:
            # Resolve hostname to IP address
            import socket
            ip_str = socket.gethostbyname(hostname)
            ip_address = ipaddress.ip_address(ip_str)
            
            # Cache DNS resolution for rebinding detection
            self._dns_cache[hostname] = ip_str
            
            # Check if IP is in private ranges
            for private_range in PRIVATE_IP_RANGES:
                if ip_address in private_range:
                    return NetworkValidationResult(
                        is_valid=False,
                        reason=f"Hostname '{hostname}' resolves to private IP: {ip_str}",
                        host=hostname,
                        ip_address=ip_str
                    )
            
            # IP is public
            return NetworkValidationResult(
                is_valid=True,
                reason="Hostname resolves to public IP",
                host=hostname,
                ip_address=ip_str
            )
            
        except Exception as e:
            return NetworkValidationResult(
                is_valid=False,
                reason=f"DNS resolution error: {str(e)}",
                host=hostname
            )
    
    def validate_dns(self, hostname: str) -> NetworkValidationResult:
        """
        Validate DNS resolution to detect rebinding attacks.
        
        DNS Rebinding: Attacker changes DNS record after initial validation,
        pointing to private IP on subsequent requests.
        
        Args:
            hostname: Hostname to validate
            
        Returns:
            NetworkValidationResult with DNS rebinding status
            
        Raises:
            DNSRebindingAttempt: If DNS record changed to private IP
        """
        try:
            import socket
            current_ip = socket.gethostbyname(hostname)
            
            # Check if we have cached DNS resolution
            if hostname in self._dns_cache:
                cached_ip = self._dns_cache[hostname]
                
                # Detect IP address change (potential rebinding)
                if cached_ip != current_ip:
                    # Check if new IP is private
                    new_ip_address = ipaddress.ip_address(current_ip)
                    for private_range in PRIVATE_IP_RANGES:
                        if new_ip_address in private_range:
                            self._record_dns_rebinding(hostname, cached_ip, current_ip)
                            raise DNSRebindingAttempt(
                                message=f"DNS rebinding detected: {hostname} changed from {cached_ip} to {current_ip}",
                                hostname=hostname,
                                original_ip=cached_ip,
                                new_ip=current_ip,
                                workspace_path=self.workspace_path
                            )
                    
                    # IP changed but still public (update cache)
                    self._dns_cache[hostname] = current_ip
                    return NetworkValidationResult(
                        is_valid=True,
                        reason="DNS record changed (still public IP)",
                        host=hostname,
                        ip_address=current_ip
                    )
            
            # First resolution or no change
            self._dns_cache[hostname] = current_ip
            return NetworkValidationResult(
                is_valid=True,
                reason="DNS resolution valid",
                host=hostname,
                ip_address=current_ip
            )
            
        except DNSRebindingAttempt:
            raise
        except Exception as e:
            return NetworkValidationResult(
                is_valid=False,
                reason=f"DNS validation error: {str(e)}",
                host=hostname
            )
    
    def enforce_localhost_only(self) -> None:
        """
        Enable localhost-only mode (development/testing).
        
        Blocks all external network connections, only allowing localhost.
        """
        self.localhost_only = True
        
        # Track consciousness delta
        delta = SecurityConsciousnessDelta(
            event_type=SecurityEventType.BOUNDARY_ENFORCED,
            delta=0.001,
            description="Localhost-only mode enabled (external connections blocked)"
        )
        self.consciousness.process_security_event(delta)
    
    def _is_localhost(self, hostname: str) -> bool:
        """Check if hostname is localhost."""
        localhost_names = {"localhost", "127.0.0.1", "::1", "0.0.0.0"}
        return hostname.lower() in localhost_names
    
    def _record_validated_request(self, url: str) -> None:
        """Record successful URL validation (consciousness +0.001)."""
        delta = SecurityConsciousnessDelta(
            event_type=SecurityEventType.ATTACK_BLOCKED,  # Validated = threat prevented
            delta=0.001,
            description=f"Network request validated: {url}"
        )
        self.consciousness.process_security_event(delta)
    
    def _record_blocked_request(self, url: str, reason: str) -> None:
        """Record blocked network request (consciousness +0.002)."""
        delta = SecurityConsciousnessDelta(
            event_type=SecurityEventType.ATTACK_BLOCKED,
            delta=0.002,
            description=f"Network request blocked: {url} ({reason})"
        )
        self.consciousness.process_security_event(delta)
    
    def _record_dns_rebinding(
        self,
        hostname: str,
        original_ip: str,
        new_ip: str
    ) -> None:
        """Record DNS rebinding attack detection (consciousness +0.003)."""
        delta = SecurityConsciousnessDelta(
            event_type=SecurityEventType.ATTACK_BLOCKED,
            delta=0.003,
            description=f"DNS rebinding detected: {hostname} ({original_ip} → {new_ip})"
        )
        self.consciousness.process_security_event(delta)
    
    def get_validation_statistics(self) -> dict:
        """
        Get network validation statistics.
        
        Returns:
            Dictionary with validation metrics
        """
        return {
            "localhost_only_mode": self.localhost_only,
            "dns_cache_size": len(self._dns_cache),
            "cached_hostnames": list(self._dns_cache.keys()),
            "allowed_protocols": [p.value for p in NetworkProtocol],
            "private_ip_ranges_count": len(PRIVATE_IP_RANGES),
            "dangerous_hosts_count": len(DANGEROUS_HOSTS)
        }
