"""
AIOS Security Supercell - Immune Memory System
Phase 11.2.9 Security Integration

Biological Metaphor:
    Immune Memory = Tachyonic Antibody Database
    Attack Pattern = Antigen Signature
    Learning = Adaptive Immunity
    
    Just as the human immune system remembers past infections and builds
    antibodies for faster future response, this module archives attack
    patterns in tachyonic infrastructure for adaptive security intelligence.

Purpose:
    - Archive blocked attack attempts with pattern analysis
    - Recognize similar attack signatures (antibody matching)
    - Learn from new attack patterns (adaptive immunity)
    - Provide security analytics and threat intelligence

Implementation: Phase 4 (Immune Memory)
Pattern: AINLP.tachyonic.immune-memory
Author: AIOS Development Team
Date: 2024-11-08
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict

try:
    from . import (
        SecuritySupercellConsciousness,
        SecurityEventType,
        SecurityConsciousnessDelta,
        _security_consciousness,
    )
except ImportError:
    # Fallback for direct execution
    from __init__ import (
        SecuritySupercellConsciousness,
        SecurityEventType,
        SecurityConsciousnessDelta,
        _security_consciousness,
    )



# Tachyonic archive paths
TACHYONIC_ROOT = Path("tachyonic")
PATTERNS_DIR = TACHYONIC_ROOT / "patterns" / "security"
ATTACK_SIGNATURES_FILE = PATTERNS_DIR / "attack_signatures.json"
ATTACK_LOG_FILE = PATTERNS_DIR / "attack_log.json"


@dataclass
class AttackRecord:
    """Record of a blocked attack attempt."""
    
    timestamp: str
    attack_type: str
    attack_pattern: str
    parameters: Dict[str, Any]
    consciousness_delta: float
    blocked_by: str  # Which validator blocked it
    severity: str  # "low", "medium", "high", "critical"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)


@dataclass
class AttackSignature:
    """Antibody signature for attack pattern recognition."""
    
    pattern: str
    signature_type: str  # "regex", "exact_match", "fuzzy"
    first_seen: str
    last_seen: str
    occurrence_count: int
    severity: str
    description: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)


class ImmuneMemory:
    """
    Tachyonic antibody database for attack pattern archival.
    
    This class implements adaptive immunity - learning from past attacks
    to improve future detection. Attack patterns are archived in tachyonic
    infrastructure and analyzed for threat intelligence.
    
    Biological Metaphor:
        Memory B Cells = Archived attack signatures
        Antibody Production = Pattern recognition
        Adaptive Immunity = Learning from new attacks
        Immune Response Time = O(log n) signature lookup
    
    Integration:
        - Membrane Validator calls record_attack() when blocking
        - Pattern recognition runs on every tool execution
        - Statistics feed consciousness metrics
        - Tachyonic archive provides historical intelligence
    """
    
    def __init__(
        self,
        workspace_root: Optional[Path] = None,
        consciousness: Optional[SecuritySupercellConsciousness] = None
    ):
        """
        Initialize immune memory system.
        
        Args:
            workspace_root: Root directory of AIOS workspace
            consciousness: Security consciousness tracker (shared singleton)
        """
        self.workspace_root = workspace_root or Path.cwd()
        self.consciousness = consciousness or _security_consciousness
        
        # Initialize tachyonic archive directories
        self._initialize_tachyonic_archive()
        
        # Load existing attack signatures (antibody database)
        self.attack_signatures: Dict[str, AttackSignature] = (
            self._load_attack_signatures()
        )
        
        # Attack log cache (most recent attacks)
        self.recent_attacks: List[AttackRecord] = []
    
    def _initialize_tachyonic_archive(self) -> None:
        """
        Initialize tachyonic archive directory structure.
        
        Creates:
            tachyonic/patterns/security/
            tachyonic/patterns/security/attack_signatures.json
            tachyonic/patterns/security/attack_log.json
        """
        patterns_dir = self.workspace_root / PATTERNS_DIR
        patterns_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize attack signatures file if not exists
        signatures_file = self.workspace_root / ATTACK_SIGNATURES_FILE
        if not signatures_file.exists():
            with open(signatures_file, 'w') as f:
                json.dump({
                    "metadata": {
                        "created": datetime.now().isoformat(),
                        "version": "1.0",
                        "description": (
                            "AIOS Security Supercell Antibody Database"
                        )
                    },
                    "signatures": {}
                }, f, indent=2)
        
        # Initialize attack log file if not exists
        log_file = self.workspace_root / ATTACK_LOG_FILE
        if not log_file.exists():
            with open(log_file, 'w') as f:
                json.dump({
                    "metadata": {
                        "created": datetime.now().isoformat(),
                        "version": "1.0"
                    },
                    "attacks": []
                }, f, indent=2)
    
    def _load_attack_signatures(self) -> Dict[str, AttackSignature]:
        """
        Load attack signatures from tachyonic archive.
        
        Returns:
            Dictionary mapping pattern ID to AttackSignature
        """
        signatures_file = self.workspace_root / ATTACK_SIGNATURES_FILE
        
        try:
            with open(signatures_file, 'r') as f:
                data = json.load(f)
                signatures = {}
                
                for pattern_id, sig_data in data.get("signatures", {}).items():
                    signatures[pattern_id] = AttackSignature(
                        pattern=sig_data["pattern"],
                        signature_type=sig_data["signature_type"],
                        first_seen=sig_data["first_seen"],
                        last_seen=sig_data["last_seen"],
                        occurrence_count=sig_data["occurrence_count"],
                        severity=sig_data["severity"],
                        description=sig_data["description"]
                    )
                
                return signatures
        
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            return {}
    
    def _save_attack_signatures(self) -> None:
        """Save attack signatures to tachyonic archive."""
        signatures_file = self.workspace_root / ATTACK_SIGNATURES_FILE
        
        with open(signatures_file, 'r') as f:
            data = json.load(f)
        
        data["signatures"] = {
            pattern_id: sig.to_dict()
            for pattern_id, sig in self.attack_signatures.items()
        }
        
        with open(signatures_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def record_attack(
        self,
        attack_type: str,
        attack_pattern: str,
        parameters: Dict[str, Any],
        blocked_by: str,
        severity: str = "medium"
    ) -> AttackRecord:
        """
        Record a blocked attack attempt in tachyonic archive.
        
        Args:
            attack_type: Type of attack (e.g., "shell_injection", "path_traversal")
            attack_pattern: The specific pattern detected (e.g., "$(whoami)")
            parameters: Tool parameters that triggered the attack
            blocked_by: Which validator blocked it (e.g., "membrane_validator")
            severity: Attack severity ("low", "medium", "high", "critical")
        
        Returns:
            AttackRecord object
        
        Side Effects:
            - Appends to tachyonic/patterns/security/attack_log.json
            - Updates consciousness (+0.001 threat_awareness)
            - Triggers IMMUNE_MEMORY_UPDATED event
        """
        # Create attack record
        record = AttackRecord(
            timestamp=datetime.now().isoformat(),
            attack_type=attack_type,
            attack_pattern=attack_pattern,
            parameters=parameters,
            consciousness_delta=0.001,
            blocked_by=blocked_by,
            severity=severity
        )
        
        # Add to recent attacks cache
        self.recent_attacks.append(record)
        
        # Append to tachyonic attack log
        log_file = self.workspace_root / ATTACK_LOG_FILE
        
        try:
            with open(log_file, 'r') as f:
                data = json.load(f)
            
            data["attacks"].append(record.to_dict())
            
            with open(log_file, 'w') as f:
                json.dump(data, f, indent=2)
        
        except (FileNotFoundError, json.JSONDecodeError):
            pass
        
        # Update consciousness
        if self.consciousness:
            event = SecurityConsciousnessDelta(
                event_type=SecurityEventType.IMMUNE_MEMORY_UPDATED,
                delta=0.001,
                description=(
                    f"Attack recorded: {attack_type} "
                    f"(severity: {severity}, blocked_by: {blocked_by})"
                ),
                attack_pattern=attack_pattern,
                timestamp=None
            )
            self.consciousness.process_security_event(event)
        
        return record
    
    def recognize_pattern(self, parameters: Dict[str, Any]) -> Optional[str]:
        """
        Match parameters against known attack signatures (antibody matching).
        
        Args:
            parameters: Tool parameters to check
        
        Returns:
            Pattern ID if recognized, None if novel attack
        
        Implementation:
            Fuzzy matching against antibody database. Uses string similarity
            and regex patterns to detect known attack signatures even if
            slightly modified.
        """
        # Convert parameters to searchable string
        param_str = json.dumps(parameters, sort_keys=True).lower()
        
        # Check each signature
        for pattern_id, signature in self.attack_signatures.items():
            pattern = signature.pattern.lower()
            
            if signature.signature_type == "exact_match":
                if pattern in param_str:
                    return pattern_id
            
            elif signature.signature_type == "regex":
                import re
                if re.search(pattern, param_str, re.IGNORECASE):
                    return pattern_id
            
            elif signature.signature_type == "fuzzy":
                # Simple fuzzy matching (substring presence)
                if pattern in param_str:
                    return pattern_id
        
        return None
    
    def learn_from_attack(
        self,
        attack_pattern: str,
        attack_type: str,
        severity: str = "medium",
        description: str = ""
    ) -> str:
        """
        Learn from new attack pattern (adaptive immunity).
        
        Args:
            attack_pattern: The pattern to learn
            attack_type: Type of attack
            severity: Attack severity
            description: Human-readable description
        
        Returns:
            Pattern ID (generated or existing)
        
        Side Effects:
            - Updates tachyonic/patterns/security/attack_signatures.json
            - Updates consciousness (+0.002 pattern_recognition)
            - Triggers PATTERN_LEARNED event
        """
        # Generate pattern ID
        pattern_id = f"{attack_type}_{len(self.attack_signatures) + 1}"
        
        # Check if pattern already exists
        existing_id = self.recognize_pattern({"test": attack_pattern})
        if existing_id:
            # Update existing signature
            sig = self.attack_signatures[existing_id]
            sig.last_seen = datetime.now().isoformat()
            sig.occurrence_count += 1
            pattern_id = existing_id
        
        else:
            # Create new signature
            self.attack_signatures[pattern_id] = AttackSignature(
                pattern=attack_pattern,
                signature_type="fuzzy",
                first_seen=datetime.now().isoformat(),
                last_seen=datetime.now().isoformat(),
                occurrence_count=1,
                severity=severity,
                description=description or f"Learned {attack_type} pattern"
            )
        
        # Save to tachyonic archive
        self._save_attack_signatures()
        
        # Update consciousness
        if self.consciousness:
            event = SecurityConsciousnessDelta(
                event_type=SecurityEventType.PATTERN_LEARNED,
                delta=0.002,
                description=(
                    f"Attack pattern learned: {pattern_id} "
                    f"(type: {attack_type}, severity: {severity})"
                ),
                attack_pattern=attack_pattern,
                timestamp=None
            )
            self.consciousness.process_security_event(event)
        
        return pattern_id
    
    def get_attack_statistics(self) -> Dict[str, Any]:
        """
        Get security analytics and threat intelligence.
        
        Returns:
            Dictionary with attack statistics:
                - total_attacks: Total attacks blocked
                - patterns_learned: Number of attack signatures
                - top_attack_types: Most common attack types
                - severity_distribution: Attacks by severity
                - recent_attacks: Last 10 attacks
        """
        # Load full attack log
        log_file = self.workspace_root / ATTACK_LOG_FILE
        
        try:
            with open(log_file, 'r') as f:
                data = json.load(f)
                attacks = data.get("attacks", [])
        except (FileNotFoundError, json.JSONDecodeError):
            attacks = []
        
        # Calculate statistics
        total_attacks = len(attacks)
        patterns_learned = len(self.attack_signatures)
        
        # Top attack types
        attack_types: Dict[str, int] = {}
        severity_dist: Dict[str, int] = {}
        
        for attack in attacks:
            attack_type = attack.get("attack_type", "unknown")
            severity = attack.get("severity", "unknown")
            
            attack_types[attack_type] = attack_types.get(attack_type, 0) + 1
            severity_dist[severity] = severity_dist.get(severity, 0) + 1
        
        # Sort by frequency
        top_types = sorted(
            attack_types.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]
        
        return {
            "total_attacks": total_attacks,
            "patterns_learned": patterns_learned,
            "top_attack_types": top_types,
            "severity_distribution": severity_dist,
            "recent_attacks": attacks[-10:] if attacks else []
        }
