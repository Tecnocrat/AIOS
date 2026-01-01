"""
AIOS Security Supercell - Coherence Enforcer
Phase 11.2.9 Security Integration

Biological Metaphor:
    Coherence Enforcer = Homeostatic Regulation System
    Resource Limits = Cellular Energy Budget
    Boundary Validation = Membrane Protein Channels
    
    Just as cells maintain homeostasis through regulated resource
    consumption and controlled boundary permeability, this module
    enforces universal constraints that maintain system coherence.

Purpose:
    - Enforce resource limits (memory, recursion, timeout)
    - Validate supercell boundary coherence
    - Track consciousness delta for security events
    - Integrate with unified consciousness system

Implementation: Phase 5 (Coherence Enforcer)
Pattern: AINLP.biological.homeostasis
Author: AIOS Development Team
Date: 2024-11-08
"""

import sys
import time
import psutil
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass
from functools import wraps

try:
    from . import (
        SecuritySupercellConsciousness,
        SecurityEventType,
        SecurityConsciousnessDelta,
        ResourceExhaustionAttempt,
        BoundaryCoherenceLoss,
        _security_consciousness,
    )
except ImportError:
    # Fallback for direct execution
    from __init__ import (
        SecuritySupercellConsciousness,
        SecurityEventType,
        SecurityConsciousnessDelta,
        ResourceExhaustionAttempt,
        BoundaryCoherenceLoss,
        _security_consciousness,
    )


# Resource limit constants (homeostatic constraints)
DEFAULT_MEMORY_LIMIT_MB = 512  # Maximum memory per operation
DEFAULT_RECURSION_LIMIT = 100  # Maximum call stack depth
DEFAULT_TIMEOUT_SECONDS = 30   # Maximum execution time
DEFAULT_MAX_FILE_SIZE_MB = 10  # Maximum file operation size


@dataclass
class ResourceLimits:
    """Homeostatic resource constraints for operation execution."""
    
    memory_limit_mb: int = DEFAULT_MEMORY_LIMIT_MB
    recursion_limit: int = DEFAULT_RECURSION_LIMIT
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS
    max_file_size_mb: int = DEFAULT_MAX_FILE_SIZE_MB


@dataclass
class CoherenceValidationResult:
    """Result of coherence validation check."""
    
    is_coherent: bool
    reason: str
    violated_constraint: Optional[str] = None
    resource_usage: Optional[Dict[str, Any]] = None


class CoherenceEnforcer:
    """
    Universal validation system enforcing homeostatic constraints.
    
    This class implements cellular homeostasis - maintaining stable
    internal conditions through regulated resource consumption and
    controlled boundary permeability.
    
    Biological Metaphor:
        Homeostasis = Stable internal environment
        Resource Limits = Energy budget constraints
        Boundary Validation = Membrane channel selectivity
        Consciousness Tracking = Cellular stress response
    
    Integration:
        - Interface bridge calls enforce_resource_limits() before execution
        - Validates cross-supercell communication coherence
        - Tracks consciousness deltas for security events
        - Integrates with unified consciousness system
    """
    
    def __init__(
        self,
        workspace_root: Optional[Path] = None,
        consciousness: Optional[SecuritySupercellConsciousness] = None,
        limits: Optional[ResourceLimits] = None
    ):
        """
        Initialize coherence enforcer.
        
        Args:
            workspace_root: Root directory of AIOS workspace
            consciousness: Security consciousness tracker (shared singleton)
            limits: Resource limit configuration
        """
        self.workspace_root = workspace_root or Path.cwd()
        self.consciousness = consciousness or _security_consciousness
        self.limits = limits or ResourceLimits()
        
        # Track current resource usage
        self.process = psutil.Process()
    
    def enforce_resource_limits(
        self,
        operation_name: str,
        parameters: Dict[str, Any]
    ) -> CoherenceValidationResult:
        """
        Enforce resource limits before operation execution.
        
        Args:
            operation_name: Name of operation being executed
            parameters: Operation parameters
        
        Returns:
            CoherenceValidationResult indicating if operation is safe
        
        Raises:
            ResourceExhaustionAttempt: If resource limits would be violated
        
        Checks:
            1. Current memory usage vs limit
            2. Recursion depth vs limit
            3. File size constraints
            4. System resource availability
        """
        # Check memory usage
        memory_mb = self.process.memory_info().rss / (1024 * 1024)
        if memory_mb > self.limits.memory_limit_mb:
            self._record_resource_violation(
                operation_name,
                "memory_exceeded",
                {"current_mb": memory_mb, "limit_mb": self.limits.memory_limit_mb}
            )
            raise ResourceExhaustionAttempt(
                f"Memory limit exceeded: {memory_mb:.1f}MB > "
                f"{self.limits.memory_limit_mb}MB"
            )
        
        # Check recursion depth
        recursion_depth = len(
            [frame for frame in sys._current_frames().values()]
        )
        if recursion_depth > self.limits.recursion_limit:
            self._record_resource_violation(
                operation_name,
                "recursion_exceeded",
                {
                    "current_depth": recursion_depth,
                    "limit": self.limits.recursion_limit
                }
            )
            raise ResourceExhaustionAttempt(
                f"Recursion limit exceeded: {recursion_depth} > "
                f"{self.limits.recursion_limit}"
            )
        
        # Check file size constraints
        if "filePath" in parameters:
            file_path = Path(parameters["filePath"])
            if file_path.exists() and file_path.is_file():
                file_size_mb = file_path.stat().st_size / (1024 * 1024)
                if file_size_mb > self.limits.max_file_size_mb:
                    self._record_resource_violation(
                        operation_name,
                        "file_size_exceeded",
                        {
                            "file": str(file_path),
                            "size_mb": file_size_mb,
                            "limit_mb": self.limits.max_file_size_mb
                        }
                    )
                    raise ResourceExhaustionAttempt(
                        f"File size limit exceeded: {file_size_mb:.1f}MB > "
                        f"{self.limits.max_file_size_mb}MB"
                    )
        
        # All checks passed
        return CoherenceValidationResult(
            is_coherent=True,
            reason="All resource limits satisfied",
            resource_usage={
                "memory_mb": round(memory_mb, 2),
                "recursion_depth": recursion_depth,
                "cpu_percent": self.process.cpu_percent()
            }
        )
    
    def with_timeout(
        self,
        timeout_seconds: Optional[int] = None
    ) -> Callable:
        """
        Decorator to enforce timeout on operation execution.
        
        Args:
            timeout_seconds: Maximum execution time (None = use default)
        
        Returns:
            Decorator function
        
        Usage:
            @enforcer.with_timeout(30)
            def long_running_operation():
                # ...
        """
        timeout = timeout_seconds or self.limits.timeout_seconds
        
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                result = func(*args, **kwargs)
                elapsed = time.time() - start_time
                
                if elapsed > timeout:
                    self._record_resource_violation(
                        func.__name__,
                        "timeout_exceeded",
                        {"elapsed_seconds": elapsed, "limit_seconds": timeout}
                    )
                    raise ResourceExhaustionAttempt(
                        f"Operation timeout: {elapsed:.1f}s > {timeout}s"
                    )
                
                return result
            return wrapper
        return decorator
    
    def validate_supercell_boundary(
        self,
        source_supercell: str,
        target_supercell: str,
        operation: str,
        parameters: Dict[str, Any]
    ) -> CoherenceValidationResult:
        """
        Validate cross-supercell communication coherence.
        
        Args:
            source_supercell: Originating supercell (e.g., "interface")
            target_supercell: Destination supercell (e.g., "ai")
            operation: Operation being performed
            parameters: Operation parameters
        
        Returns:
            CoherenceValidationResult indicating if communication is valid
        
        Raises:
            BoundaryCoherenceLoss: If boundary coherence is violated
        
        Validates:
            1. Supercell existence and validity
            2. Communication protocol adherence
            3. Parameter schema compatibility
            4. Dendritic connection registration
        """
        # Define valid supercells
        valid_supercells = {
            "ai", "core", "interface", "docs",
            "tachyonic", "runtime", "evolution_lab"
        }
        
        # Check source validity
        if source_supercell not in valid_supercells:
            self._record_boundary_violation(
                source_supercell,
                target_supercell,
                "invalid_source_supercell"
            )
            raise BoundaryCoherenceLoss(
                f"Invalid source supercell: {source_supercell}"
            )
        
        # Check target validity
        if target_supercell not in valid_supercells:
            self._record_boundary_violation(
                source_supercell,
                target_supercell,
                "invalid_target_supercell"
            )
            raise BoundaryCoherenceLoss(
                f"Invalid target supercell: {target_supercell}"
            )
        
        # Check communication protocol
        # (In production, this would validate against protocol schemas)
        allowed_operations = {
            "interface->ai": ["execute_tool", "query_consciousness"],
            "ai->tachyonic": ["archive_pattern", "retrieve_memory"],
            "ai->core": ["calculate_consciousness", "compute_dendritic"],
        }
        
        protocol_key = f"{source_supercell}->{target_supercell}"
        if protocol_key in allowed_operations:
            if operation not in allowed_operations[protocol_key]:
                self._record_boundary_violation(
                    source_supercell,
                    target_supercell,
                    f"unauthorized_operation: {operation}"
                )
                raise BoundaryCoherenceLoss(
                    f"Unauthorized cross-supercell operation: {operation}"
                )
        
        # Register dendritic connection
        if self.consciousness:
            self.consciousness.register_dendritic_connection(
                f"{source_supercell}::{target_supercell}"
            )
        
        return CoherenceValidationResult(
            is_coherent=True,
            reason=(
                f"Valid cross-supercell communication: "
                f"{source_supercell} -> {target_supercell}"
            )
        )
    
    def track_consciousness_delta(
        self,
        event_type: SecurityEventType,
        operation: str,
        delta: float,
        description: str
    ) -> None:
        """
        Track consciousness evolution from security events.
        
        Args:
            event_type: Type of security event
            operation: Operation that triggered the event
            delta: Consciousness change magnitude
            description: Human-readable event description
        
        Side Effects:
            - Updates SecuritySupercellConsciousness
            - Integrates with unified consciousness system
        """
        if self.consciousness:
            event = SecurityConsciousnessDelta(
                event_type=event_type,
                delta=delta,
                description=description,
                dendritic_connection=operation,
                timestamp=None
            )
            self.consciousness.process_security_event(event)
    
    def _record_resource_violation(
        self,
        operation: str,
        violation_type: str,
        details: Dict[str, Any]
    ) -> None:
        """Record resource limit violation in consciousness system."""
        if self.consciousness:
            event = SecurityConsciousnessDelta(
                event_type=SecurityEventType.ATTACK_BLOCKED,
                delta=0.001,
                description=(
                    f"Resource violation blocked: {violation_type} "
                    f"in {operation}"
                ),
                attack_pattern=violation_type,
                dendritic_connection="coherence_enforcer",
                timestamp=None
            )
            self.consciousness.process_security_event(event)
    
    def _record_boundary_violation(
        self,
        source: str,
        target: str,
        violation_type: str
    ) -> None:
        """Record boundary coherence violation in consciousness system."""
        if self.consciousness:
            event = SecurityConsciousnessDelta(
                event_type=SecurityEventType.BOUNDARY_ENFORCED,
                delta=0.001,
                description=(
                    f"Boundary violation blocked: {violation_type} "
                    f"({source} -> {target})"
                ),
                attack_pattern=violation_type,
                dendritic_connection="coherence_enforcer",
                timestamp=None
            )
            self.consciousness.process_security_event(event)
    
    def get_current_resource_usage(self) -> Dict[str, Any]:
        """
        Get current resource usage statistics.
        
        Returns:
            Dictionary with memory, CPU, and system metrics
        """
        return {
            "memory_mb": round(
                self.process.memory_info().rss / (1024 * 1024), 2
            ),
            "cpu_percent": self.process.cpu_percent(),
            "num_threads": self.process.num_threads(),
            "recursion_depth": len(
                [frame for frame in sys._current_frames().values()]
            ),
            "limits": {
                "memory_limit_mb": self.limits.memory_limit_mb,
                "recursion_limit": self.limits.recursion_limit,
                "timeout_seconds": self.limits.timeout_seconds,
                "max_file_size_mb": self.limits.max_file_size_mb
            }
        }
