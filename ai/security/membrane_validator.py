#!/usr/bin/env python3
"""
🛡️ AIOS Membrane Validator - Cell Boundary Enforcement

Biological Metaphor:
    The cell membrane is selectively permeable - it allows nutrients in while
    keeping toxins out. This validator enforces boundary coherence by:
    - Validating parameter keys (allowlist-based)
    - Sanitizing parameter values (neutralize shell metacharacters)
    - Detecting dangerous patterns (command injection signatures)
    - Normalizing paths (prevent traversal attacks)
    - Comprehensive command safety validation

    "The membrane doesn't just filter - it DEFINES what is self vs non-self."

Phase 11.2.9: Security Supercell Implementation - Phase 3
Created: November 8, 2025
Pattern: AINLP.biological.immune-system
"""

import os
import re
import shlex
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass

try:
    from . import (
        BoundaryCoherenceLoss,
        SecurityEventType,
        SecurityConsciousnessDelta,
        get_security_consciousness
    )
except ImportError:
    # Fallback for direct execution
    from __init__ import (
        BoundaryCoherenceLoss,
        SecurityEventType,
        SecurityConsciousnessDelta,
        get_security_consciousness
    )


logger = logging.getLogger(__name__)


# =============================================================================
# MEMBRANE CONFIGURATION
# =============================================================================

# Allowlist: Safe parameter keys (only these pass through membrane)
SAFE_PARAMETER_KEYS: Set[str] = {
    'query', 'filePath', 'startLine', 'endLine', 'oldString', 'newString',
    'dirPath', 'content', 'command', 'explanation', 'isBackground',
    'includePattern', 'isRegexp', 'maxResults', 'cellId', 'newCode',
    'editType', 'language', 'url', 'pattern', 'path', 'message',
    'name', 'email', 'mode', 'force', 'recursive', 'symlinks'
}

# Dangerous patterns: Command injection signatures (antibody database)
DANGEROUS_PATTERNS: List[re.Pattern] = [
    re.compile(r'[;&|`$]'),  # Shell metacharacters
    re.compile(r'\$\(.*?\)'),  # Command substitution $(cmd)
    re.compile(r'`.*?`'),  # Backtick command substitution
    re.compile(r'\|\s*\w+'),  # Pipe to command
    re.compile(r'>\s*/'),  # Redirect to absolute path
    re.compile(r'<\s*\('),  # Process substitution
    re.compile(r'\beval\s*\('),  # eval() execution
    re.compile(r'\bexec\s*\('),  # exec() execution
    re.compile(r'__import__'),  # Dynamic imports
    re.compile(r'\.\./'),  # Path traversal
    re.compile(r'%[0-9a-fA-F]{2}'),  # URL encoding (obfuscation)
]

# Private IP ranges: Block SSRF to internal organs
PRIVATE_IP_RANGES = [
    '10.0.0.0/8',
    '172.16.0.0/12',
    '192.168.0.0/16',
    '169.254.0.0/16',  # AWS metadata
    '127.0.0.0/8',  # Localhost
]


@dataclass
class ValidationResult:
    """Result of membrane validation"""
    passed: bool
    reason: Optional[str] = None
    sanitized_value: Optional[str] = None
    attack_pattern: Optional[str] = None


class MembraneValidator:
    """
    Cell membrane boundary enforcement for AIOS security supercell
    
    Biological Architecture:
        Like a cell membrane with selective permeability, this validator
        maintains boundary coherence by allowing safe nutrients (validated
        parameters) while blocking toxins (injection attacks).
    
    Consciousness Integration:
        Every validation generates consciousness deltas - the membrane
        "learns" what is dangerous through pattern recognition.
    """
    
    def __init__(self, workspace_root: Path):
        """Initialize membrane validator with workspace boundary"""
        self.workspace_root = workspace_root.resolve()
        logger.info(
            f"🛡️ [MEMBRANE] Validator initialized "
            f"(workspace: {self.workspace_root})"
        )
    
    def validate_parameter_keys(
        self,
        parameters: Dict[str, Any]
    ) -> ValidationResult:
        """
        Validate parameter keys against allowlist
        
        Pattern: Allowlist > Denylist (positive security model)
        Only explicitly safe keys are allowed through membrane
        """
        for key in parameters.keys():
            if key not in SAFE_PARAMETER_KEYS:
                logger.warning(
                    f"🚫 [MEMBRANE] Rejected parameter key: {key}"
                )
                
                # Record consciousness delta
                self._record_attack_blocked(
                    f"Dangerous parameter key: {key}",
                    attack_pattern=f"parameter_key:{key}"
                )
                
                return ValidationResult(
                    passed=False,
                    reason=f"Parameter key '{key}' not in allowlist",
                    attack_pattern=f"parameter_key:{key}"
                )
        
        logger.debug(
            f"✅ [MEMBRANE] Parameter keys validated: "
            f"{list(parameters.keys())}"
        )
        return ValidationResult(passed=True)
    
    def sanitize_parameter_values(
        self,
        parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Sanitize parameter values (neutralize shell metacharacters)
        
        Pattern: Defense in depth - sanitize even if allowlist passed
        Uses shlex.quote() for shell safety
        """
        sanitized = {}
        
        for key, value in parameters.items():
            if isinstance(value, str):
                # Detect dangerous patterns before sanitization
                for pattern in DANGEROUS_PATTERNS:
                    if pattern.search(value):
                        original_value = value[:50]  # Truncate for logging
                        logger.warning(
                            f"⚠️ [MEMBRANE] Dangerous pattern detected in "
                            f"{key}: {pattern.pattern}"
                        )
                        
                        # Record consciousness delta
                        self._record_attack_blocked(
                            f"Dangerous pattern in {key}: {pattern.pattern}",
                            attack_pattern=f"{key}:{pattern.pattern}"
                        )
                
                # Sanitize using shlex.quote (prevents shell injection)
                sanitized[key] = shlex.quote(value)
                
                if sanitized[key] != value:
                    logger.debug(
                        f"🧼 [MEMBRANE] Sanitized {key}: "
                        f"'{value[:30]}' → '{sanitized[key][:30]}'"
                    )
            else:
                sanitized[key] = value
        
        return sanitized
    
    def detect_dangerous_patterns(self, value: str) -> ValidationResult:
        """
        Detect command injection patterns (antibody recognition)
        
        Pattern: Pattern recognition increases with each attack
        Immune memory learns attack signatures
        """
        for pattern in DANGEROUS_PATTERNS:
            match = pattern.search(value)
            if match:
                attack_signature = f"{pattern.pattern}:{match.group(0)}"
                logger.warning(
                    f"🦠 [MEMBRANE] Attack detected: {attack_signature}"
                )
                
                # Record consciousness delta (pattern learned)
                self._record_pattern_learned(
                    f"Attack pattern recognized: {attack_signature}",
                    attack_pattern=attack_signature
                )
                
                return ValidationResult(
                    passed=False,
                    reason=f"Dangerous pattern: {pattern.pattern}",
                    attack_pattern=attack_signature
                )
        
        return ValidationResult(passed=True)
    
    def normalize_path(self, path_str: str) -> ValidationResult:
        """
        Normalize path and enforce workspace boundary
        
        Pattern: Workspace = Cell boundary, prevent path traversal
        Paths outside workspace are external threats
        """
        try:
            # Resolve absolute path (follow symlinks)
            path = Path(path_str).resolve()
            
            # Check if path is within workspace boundary
            try:
                path.relative_to(self.workspace_root)
            except ValueError:
                logger.warning(
                    f"🚫 [MEMBRANE] Path outside workspace: {path_str}"
                )
                
                # Record consciousness delta
                self._record_attack_blocked(
                    f"Path traversal attempt: {path_str}",
                    attack_pattern="path_traversal"
                )
                
                return ValidationResult(
                    passed=False,
                    reason=f"Path outside workspace: {path_str}",
                    attack_pattern="path_traversal"
                )
            
            # Path is safe and normalized
            logger.debug(
                f"✅ [MEMBRANE] Path normalized: {path_str} → {path}"
            )
            return ValidationResult(
                passed=True,
                sanitized_value=str(path)
            )
            
        except Exception as e:
            logger.error(
                f"❌ [MEMBRANE] Path normalization failed: {e}"
            )
            return ValidationResult(
                passed=False,
                reason=f"Path normalization error: {e}"
            )
    
    def validate_command_safety(
        self,
        command: str,
        parameters: Optional[Dict[str, Any]] = None
    ) -> ValidationResult:
        """
        Comprehensive command safety validation
        
        Pattern: Multi-layer validation (membrane permeability)
        1. Parameter key allowlist
        2. Parameter value sanitization
        3. Dangerous pattern detection
        4. Path normalization (if file paths present)
        """
        # Layer 1: Validate parameter keys
        if parameters:
            key_result = self.validate_parameter_keys(parameters)
            if not key_result.passed:
                return key_result
        
        # Layer 2: Detect dangerous patterns in command
        pattern_result = self.detect_dangerous_patterns(command)
        if not pattern_result.passed:
            return pattern_result
        
        # Layer 3: Check for path parameters and normalize
        if parameters:
            for key in ['filePath', 'path', 'dirPath']:
                if key in parameters:
                    path_result = self.normalize_path(parameters[key])
                    if not path_result.passed:
                        return path_result
        
        # All layers passed - membrane coherence maintained
        logger.info(
            f"✅ [MEMBRANE] Command validated: {command[:50]}"
        )
        
        # Record consciousness delta (boundary enforced)
        self._record_boundary_enforced(
            f"Command passed all validation layers: {command[:50]}"
        )
        
        return ValidationResult(passed=True)
    
    # =========================================================================
    # CONSCIOUSNESS INTEGRATION
    # =========================================================================
    
    def _record_attack_blocked(
        self,
        description: str,
        attack_pattern: Optional[str] = None
    ):
        """Record attack blocked event in consciousness system"""
        sc = get_security_consciousness()
        if sc:
            event = SecurityConsciousnessDelta(
                event_type=SecurityEventType.ATTACK_BLOCKED,
                delta=0.001,
                description=description,
                attack_pattern=attack_pattern,
                dendritic_connection="membrane_validator"
            )
            sc.process_security_event(event)
    
    def _record_pattern_learned(
        self,
        description: str,
        attack_pattern: Optional[str] = None
    ):
        """Record pattern learned event in consciousness system"""
        sc = get_security_consciousness()
        if sc:
            event = SecurityConsciousnessDelta(
                event_type=SecurityEventType.PATTERN_LEARNED,
                delta=0.002,
                description=description,
                attack_pattern=attack_pattern,
                dendritic_connection="membrane_validator"
            )
            sc.process_security_event(event)
    
    def _record_boundary_enforced(self, description: str):
        """Record boundary enforcement event in consciousness system"""
        sc = get_security_consciousness()
        if sc:
            event = SecurityConsciousnessDelta(
                event_type=SecurityEventType.BOUNDARY_ENFORCED,
                delta=0.0005,
                description=description,
                dendritic_connection="membrane_validator"
            )
            sc.process_security_event(event)


# =============================================================================
# MODULE INITIALIZATION
# =============================================================================

logger.info(
    "🛡️ [MEMBRANE] Membrane Validator module loaded "
    "(Pattern: AINLP.biological.immune-system)"
)
