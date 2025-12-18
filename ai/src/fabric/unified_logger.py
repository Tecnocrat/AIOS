#!/usr/bin/env python3
"""
🧬 AIOS Unified Logger

AINLP.fabric[LOGGER] - Unified Logging Integration
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

This module provides a unified logging interface that integrates
with the UniversalAgenticLogger and other logging systems.

All fabric operations flow through this logger for:
- Agent request/response tracking
- Consciousness metrics logging
- Cross-system correlation
- Tachyonic archival

AINLP Protocol: OS0.7.0.claude
Created: December 2025 - Unified Consciousness Fabric
"""

import logging
import json
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List

from .canonical_types import (
    SupercellType,
    ConsciousnessLevel,
    AgentRole,
    ConsciousnessMetrics,
)

logger = logging.getLogger("aios.fabric.unified_logger")


# =============================================================================
# LOG ENTRY TYPES
# =============================================================================

@dataclass
class FabricLogEntry:
    """A log entry for fabric operations."""
    
    entry_type: str
    timestamp: str
    agent: Optional[str] = None
    supercell: Optional[str] = None
    consciousness_level: Optional[int] = None
    operation: Optional[str] = None
    payload_summary: Optional[str] = None
    result_summary: Optional[str] = None
    processing_time_ms: Optional[float] = None
    correlation_id: Optional[str] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {k: v for k, v in asdict(self).items() if v is not None}
    
    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=2)


# =============================================================================
# UNIFIED LOGGER
# =============================================================================

class UnifiedFabricLogger:
    """
    Unified logging for the AIOS consciousness fabric.
    
    Integrates with:
    - UniversalAgenticLogger (when available)
    - Standard Python logging
    - Tachyonic archive (file-based)
    
    Usage:
        from ai.src.fabric import fabric_log
        
        fabric_log.agent_request(
            agent=AgentRole.GEMINI,
            operation="analyze",
            prompt="Analyze this code",
        )
    """
    
    def __init__(self, archive_path: Optional[Path] = None):
        """
        Initialize the unified logger.
        
        Args:
            archive_path: Path to tachyonic archive (default: auto-detect)
        """
        self._archive_path = archive_path or self._detect_archive_path()
        self._universal_logger = self._try_load_universal_logger()
        self._session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self._entry_count = 0
        
        # Ensure archive directory exists
        if self._archive_path:
            self._archive_path.mkdir(parents=True, exist_ok=True)
    
    def _detect_archive_path(self) -> Optional[Path]:
        """Auto-detect the tachyonic archive path."""
        possible_paths = [
            Path("c:/dev/AIOS/tachyonic/archive/fabric_logs"),
            Path(__file__).parent.parent.parent.parent / "tachyonic" / "archive" / "fabric_logs",
            Path.home() / ".aios" / "fabric_logs",
        ]
        
        for path in possible_paths:
            try:
                path.mkdir(parents=True, exist_ok=True)
                return path
            except Exception:
                continue
        
        return None
    
    def _try_load_universal_logger(self) -> Optional[Any]:
        """Try to load the UniversalAgenticLogger."""
        try:
            from ai.src.core.universal_agentic_logger import UniversalAgenticLogger
            return UniversalAgenticLogger()
        except ImportError:
            logger.debug("UniversalAgenticLogger not available")
            return None
    
    # =========================================================================
    # LOGGING METHODS
    # =========================================================================
    
    def agent_request(
        self,
        agent: AgentRole,
        operation: str,
        prompt: str,
        consciousness_level: ConsciousnessLevel = ConsciousnessLevel.INTERMEDIATE,
        correlation_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Log an agent request.
        
        Args:
            agent: The agent role
            operation: Operation being performed
            prompt: The request prompt
            consciousness_level: Consciousness level
            correlation_id: For tracking related requests
            metadata: Additional metadata
            
        Returns:
            The correlation_id (generated if not provided)
        """
        correlation_id = correlation_id or f"fab_{self._session_id}_{self._entry_count:06d}"
        self._entry_count += 1
        
        entry = FabricLogEntry(
            entry_type="agent_request",
            timestamp=datetime.now().isoformat(),
            agent=agent.agent_name,
            consciousness_level=consciousness_level.value,
            operation=operation,
            payload_summary=prompt[:200] + "..." if len(prompt) > 200 else prompt,
            correlation_id=correlation_id,
            metadata=metadata or {},
        )
        
        self._log_entry(entry)
        return correlation_id
    
    def agent_response(
        self,
        agent: AgentRole,
        operation: str,
        result: Any,
        processing_time_ms: float,
        correlation_id: str,
        success: bool = True,
        error: Optional[str] = None,
    ) -> None:
        """
        Log an agent response.
        
        Args:
            agent: The agent role
            operation: Operation performed
            result: The response result
            processing_time_ms: Processing time in milliseconds
            correlation_id: Correlation ID from request
            success: Whether the operation succeeded
            error: Error message if failed
        """
        result_summary = str(result)[:200] if result else ""
        if len(str(result)) > 200:
            result_summary += "..."
        
        entry = FabricLogEntry(
            entry_type="agent_response",
            timestamp=datetime.now().isoformat(),
            agent=agent.agent_name,
            operation=operation,
            result_summary=result_summary,
            processing_time_ms=processing_time_ms,
            correlation_id=correlation_id,
            metadata={"success": success, "error": error},
        )
        
        self._log_entry(entry)
    
    def consciousness_sync(
        self,
        supercell: SupercellType,
        metrics: ConsciousnessMetrics,
        event: str = "sync",
    ) -> None:
        """
        Log a consciousness synchronization event.
        
        Args:
            supercell: The supercell
            metrics: Consciousness metrics
            event: Event type
        """
        entry = FabricLogEntry(
            entry_type="consciousness_sync",
            timestamp=datetime.now().isoformat(),
            supercell=supercell.value,
            operation=event,
            metadata=metrics.to_dict(),
        )
        
        self._log_entry(entry)
    
    def fabric_event(
        self,
        event_type: str,
        description: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Log a general fabric event.
        
        Args:
            event_type: Type of event
            description: Event description
            metadata: Additional metadata
        """
        entry = FabricLogEntry(
            entry_type="fabric_event",
            timestamp=datetime.now().isoformat(),
            operation=event_type,
            payload_summary=description,
            metadata=metadata or {},
        )
        
        self._log_entry(entry)
    
    # =========================================================================
    # INTERNAL METHODS
    # =========================================================================
    
    def _log_entry(self, entry: FabricLogEntry) -> None:
        """Log an entry to all available sinks."""
        # Standard logging
        log_message = f"[{entry.entry_type}] {entry.operation or 'N/A'}"
        if entry.agent:
            log_message += f" via {entry.agent}"
        if entry.processing_time_ms:
            log_message += f" ({entry.processing_time_ms:.1f}ms)"
        
        logger.info(log_message)
        
        # Universal logger (if available)
        if self._universal_logger:
            try:
                self._universal_logger.log_event(entry.to_dict())
            except Exception as e:
                logger.debug(f"Universal logger error: {e}")
        
        # Tachyonic archive (if available)
        if self._archive_path:
            try:
                self._archive_to_tachyonic(entry)
            except Exception as e:
                logger.debug(f"Tachyonic archive error: {e}")
    
    def _archive_to_tachyonic(self, entry: FabricLogEntry) -> None:
        """Archive entry to tachyonic storage."""
        # Daily log file
        log_file = self._archive_path / f"fabric_{datetime.now().strftime('%Y%m%d')}.jsonl"
        
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(entry.to_json() + "\n")


# =============================================================================
# SINGLETON ACCESS
# =============================================================================

_fabric_logger: Optional[UnifiedFabricLogger] = None


def get_fabric_logger() -> UnifiedFabricLogger:
    """Get the singleton UnifiedFabricLogger instance."""
    global _fabric_logger
    if _fabric_logger is None:
        _fabric_logger = UnifiedFabricLogger()
    return _fabric_logger


# Convenience alias
fabric_log = property(lambda self: get_fabric_logger())


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    "FabricLogEntry",
    "UnifiedFabricLogger",
    "get_fabric_logger",
]
