#!/usr/bin/env python3
"""
AIOS Format State Messenger
===========================
Handles format-on-save events, communicates state changes to AIOS core,
and provides graceful fallback when components are unavailable.

AINLP Biological Pattern:
- Dendritic: Connects VS Code events → AIOS consciousness system
- Tachyonic: Archives formatting decisions and state transitions
- Fallback: Operates silently when core is unreachable

Usage:
    python aios_format_state_messenger.py --file <path> --action <format|save|check>
    python aios_format_state_messenger.py --status
    python aios_format_state_messenger.py --test-fallback
"""

import json
import logging
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Optional

# Configure logging with fallback-aware formatting
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("AIOS.FormatMessenger")


class ConnectionState(Enum):
    """AIOS core connection states."""
    CONNECTED = "connected"
    DEGRADED = "degraded"
    OFFLINE = "offline"
    FALLBACK = "fallback"


class FormatAction(Enum):
    """Format action types."""
    FORMAT = "format"
    SAVE = "save"
    CHECK = "check"
    SYNC = "sync"


@dataclass
class FormatEvent:
    """Represents a formatting event to communicate to AIOS."""
    file_path: str
    action: FormatAction
    timestamp: datetime = field(default_factory=datetime.now)
    changes_detected: bool = False
    formatter: str = "black"
    success: bool = True
    error_message: Optional[str] = None
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "file_path": self.file_path,
            "action": self.action.value,
            "timestamp": self.timestamp.isoformat(),
            "changes_detected": self.changes_detected,
            "formatter": self.formatter,
            "success": self.success,
            "error_message": self.error_message,
        }


@dataclass
class MessengerState:
    """Current state of the format messenger."""
    connection: ConnectionState = ConnectionState.OFFLINE
    last_heartbeat: Optional[datetime] = None
    events_queued: int = 0
    events_sent: int = 0
    fallback_active: bool = False
    core_version: Optional[str] = None


class AIOSFormatStateMessenger:
    """
    Communicates format state changes to AIOS core with graceful fallback.
    
    Features:
    - Seamless auto-save integration
    - Event queuing when core is unreachable
    - Automatic reconnection attempts
    - Silent fallback mode (no disruption to user)
    """
    
    def __init__(self, workspace_root: Optional[Path] = None):
        self.workspace_root = workspace_root or self._detect_workspace()
        self.state = MessengerState()
        self.event_queue: list[FormatEvent] = []
        self.max_queue_size = 100
        self.reconnect_interval = 30  # seconds
        self.last_reconnect_attempt: Optional[datetime] = None
        
        # Paths for state persistence (tachyonic pattern)
        self.state_file = self.workspace_root / "tachyonic" / "format_messenger_state.json"
        self.queue_file = self.workspace_root / "tachyonic" / "format_event_queue.json"
        
        # Try to connect on init
        self._initialize_connection()
    
    def _detect_workspace(self) -> Path:
        """Detect AIOS workspace root."""
        # Try common locations
        candidates = [
            Path(__file__).parent.parent.parent,  # From ai/tools/
            Path.cwd(),
            Path("c:/dev/aios-win/aios-core"),
        ]
        for candidate in candidates:
            if (candidate / "AIOS.sln").exists() or (candidate / "ai").exists():
                return candidate
        return Path.cwd()
    
    def _initialize_connection(self) -> None:
        """Initialize connection to AIOS core with fallback."""
        try:
            # Try HTTP bridge first
            if self._check_http_bridge():
                self.state.connection = ConnectionState.CONNECTED
                self.state.fallback_active = False
                logger.info("✓ Connected to AIOS Interface Bridge")
                return
            
            # Try direct consciousness access
            if self._check_consciousness_direct():
                self.state.connection = ConnectionState.DEGRADED
                self.state.fallback_active = False
                logger.info("⚡ Direct consciousness access (degraded mode)")
                return
            
            # Fall back to file-based messaging
            self._activate_fallback()
            
        except Exception as e:
            logger.debug(f"Connection init failed: {e}")
            self._activate_fallback()
    
    def _check_http_bridge(self) -> bool:
        """Check if HTTP interface bridge is available."""
        try:
            import urllib.request
            req = urllib.request.Request(
                "http://localhost:8000/health",
                method="GET",
            )
            with urllib.request.urlopen(req, timeout=2) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode())
                    self.state.core_version = data.get("version", "unknown")
                    return True
        except Exception:
            pass
        return False
    
    def _check_consciousness_direct(self) -> bool:
        """Try direct Python import of consciousness system."""
        try:
            # Dynamic import to avoid hard dependency
            sys.path.insert(0, str(self.workspace_root / "ai" / "tools"))
            from aios_unified_consciousness_system import AIOSUnifiedConsciousness
            
            consciousness = AIOSUnifiedConsciousness()
            metrics = consciousness.get_consciousness_metrics()
            if metrics:
                self.state.core_version = "direct"
                return True
        except Exception:
            pass
        return False
    
    def _activate_fallback(self) -> None:
        """Activate fallback mode - file-based, silent operation."""
        self.state.connection = ConnectionState.FALLBACK
        self.state.fallback_active = True
        self.state.last_heartbeat = datetime.now()
        
        # Load any queued events from previous session
        self._load_queue()
        
        logger.info("📁 Fallback mode active (file-based messaging)")
    
    def _load_queue(self) -> None:
        """Load event queue from tachyonic storage."""
        try:
            if self.queue_file.exists():
                data = json.loads(self.queue_file.read_text())
                for event_data in data.get("events", []):
                    self.event_queue.append(FormatEvent(
                        file_path=event_data["file_path"],
                        action=FormatAction(event_data["action"]),
                        timestamp=datetime.fromisoformat(event_data["timestamp"]),
                        changes_detected=event_data.get("changes_detected", False),
                        formatter=event_data.get("formatter", "black"),
                        success=event_data.get("success", True),
                    ))
                self.state.events_queued = len(self.event_queue)
        except Exception as e:
            logger.debug(f"Queue load failed: {e}")
    
    def _save_queue(self) -> None:
        """Persist event queue to tachyonic storage."""
        try:
            self.queue_file.parent.mkdir(parents=True, exist_ok=True)
            data = {
                "timestamp": datetime.now().isoformat(),
                "events": [e.to_dict() for e in self.event_queue],
            }
            self.queue_file.write_text(json.dumps(data, indent=2))
        except Exception as e:
            logger.debug(f"Queue save failed: {e}")
    
    def _save_state(self) -> None:
        """Persist messenger state."""
        try:
            self.state_file.parent.mkdir(parents=True, exist_ok=True)
            data = {
                "connection": self.state.connection.value,
                "last_heartbeat": self.state.last_heartbeat.isoformat() if self.state.last_heartbeat else None,
                "events_queued": self.state.events_queued,
                "events_sent": self.state.events_sent,
                "fallback_active": self.state.fallback_active,
                "core_version": self.state.core_version,
            }
            self.state_file.write_text(json.dumps(data, indent=2))
        except Exception as e:
            logger.debug(f"State save failed: {e}")
    
    def report_format_event(self, file_path: str, action: FormatAction, changes_detected: bool = False) -> bool:
        """
        Report a formatting event to AIOS core.
        
        Returns True if event was successfully communicated, False if queued for later.
        """
        event = FormatEvent(
            file_path=str(file_path),
            action=action,
            changes_detected=changes_detected,
        )
        
        # Try direct communication first
        if self.state.connection == ConnectionState.CONNECTED:
            if self._send_via_http(event):
                self.state.events_sent += 1
                return True
        
        if self.state.connection == ConnectionState.DEGRADED:
            if self._send_via_direct(event):
                self.state.events_sent += 1
                return True
        
        # Queue for later (fallback mode)
        return self._queue_event(event)
    
    def _send_via_http(self, event: FormatEvent) -> bool:
        """Send event via HTTP bridge."""
        try:
            import urllib.request
            
            payload = json.dumps({
                "event_type": "format_state_change",
                "data": event.to_dict(),
            }).encode()
            
            req = urllib.request.Request(
                "http://localhost:8000/events/format",
                data=payload,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            
            with urllib.request.urlopen(req, timeout=5) as response:
                return response.status in (200, 201, 202)
                
        except Exception as e:
            logger.debug(f"HTTP send failed: {e}")
            # Degrade connection state
            self.state.connection = ConnectionState.DEGRADED
            return False
    
    def _send_via_direct(self, event: FormatEvent) -> bool:
        """Send event via direct consciousness system access."""
        try:
            sys.path.insert(0, str(self.workspace_root / "ai" / "tools"))
            from aios_unified_consciousness_system import AIOSUnifiedConsciousness
            
            consciousness = AIOSUnifiedConsciousness()
            
            # Report as a development metric
            consciousness.report_metric(
                category="formatting",
                name="format_event",
                value=1.0 if event.success else 0.0,
                metadata={
                    "file": event.file_path,
                    "action": event.action.value,
                    "changes": event.changes_detected,
                },
            )
            return True
            
        except Exception as e:
            logger.debug(f"Direct send failed: {e}")
            self._activate_fallback()
            return False
    
    def _queue_event(self, event: FormatEvent) -> bool:
        """Queue event for later delivery (fallback mode)."""
        if len(self.event_queue) >= self.max_queue_size:
            # Remove oldest events
            self.event_queue = self.event_queue[-(self.max_queue_size - 1):]
        
        self.event_queue.append(event)
        self.state.events_queued = len(self.event_queue)
        self._save_queue()
        
        # Try reconnection periodically
        self._maybe_reconnect()
        
        return False  # Queued, not sent
    
    def _maybe_reconnect(self) -> None:
        """Attempt reconnection if enough time has passed."""
        now = datetime.now()
        
        if self.last_reconnect_attempt:
            elapsed = (now - self.last_reconnect_attempt).total_seconds()
            if elapsed < self.reconnect_interval:
                return
        
        self.last_reconnect_attempt = now
        self._initialize_connection()
        
        # If reconnected, flush queue
        if self.state.connection in (ConnectionState.CONNECTED, ConnectionState.DEGRADED):
            self._flush_queue()
    
    def _flush_queue(self) -> None:
        """Send all queued events."""
        sent_count = 0
        failed = []
        
        for event in self.event_queue:
            success = False
            if self.state.connection == ConnectionState.CONNECTED:
                success = self._send_via_http(event)
            elif self.state.connection == ConnectionState.DEGRADED:
                success = self._send_via_direct(event)
            
            if success:
                sent_count += 1
            else:
                failed.append(event)
        
        self.event_queue = failed
        self.state.events_queued = len(failed)
        self.state.events_sent += sent_count
        self._save_queue()
        
        if sent_count > 0:
            logger.info(f"📤 Flushed {sent_count} queued events")
    
    def get_status(self) -> dict[str, Any]:
        """Get current messenger status."""
        return {
            "connection": self.state.connection.value,
            "fallback_active": self.state.fallback_active,
            "events_queued": self.state.events_queued,
            "events_sent": self.state.events_sent,
            "core_version": self.state.core_version,
            "workspace": str(self.workspace_root),
        }
    
    def test_fallback(self) -> dict[str, Any]:
        """Test fallback mechanism by simulating failure."""
        results = {
            "test": "fallback_mechanism",
            "timestamp": datetime.now().isoformat(),
            "steps": [],
        }
        
        # Step 1: Force fallback mode
        original_state = self.state.connection
        self._activate_fallback()
        results["steps"].append({
            "name": "activate_fallback",
            "success": self.state.fallback_active,
            "connection": self.state.connection.value,
        })
        
        # Step 2: Queue an event
        test_event = FormatEvent(
            file_path="test/fallback_test.py",
            action=FormatAction.CHECK,
            changes_detected=False,
        )
        queued = self._queue_event(test_event)
        results["steps"].append({
            "name": "queue_event",
            "success": not queued,  # Should return False (queued, not sent)
            "queue_size": self.state.events_queued,
        })
        
        # Step 3: Verify persistence
        self._save_queue()
        queue_exists = self.queue_file.exists()
        results["steps"].append({
            "name": "persist_queue",
            "success": queue_exists,
            "file": str(self.queue_file),
        })
        
        # Step 4: Reload and verify
        original_queue = self.event_queue.copy()
        self.event_queue = []
        self._load_queue()
        reload_success = len(self.event_queue) == len(original_queue)
        results["steps"].append({
            "name": "reload_queue",
            "success": reload_success,
            "events_loaded": len(self.event_queue),
        })
        
        # Step 5: Clean up test event
        self.event_queue = [e for e in self.event_queue if e.file_path != "test/fallback_test.py"]
        self._save_queue()
        results["steps"].append({
            "name": "cleanup",
            "success": True,
        })
        
        # Restore original state if possible
        self._initialize_connection()
        
        # Overall result
        all_passed = all(step["success"] for step in results["steps"])
        results["overall_success"] = all_passed
        results["final_state"] = self.get_status()
        
        return results


# VS Code task integration
def handle_format_save(file_path: str, action: str = "format") -> None:
    """Handle format-on-save event from VS Code task."""
    messenger = AIOSFormatStateMessenger()
    
    action_enum = FormatAction(action) if action in [a.value for a in FormatAction] else FormatAction.FORMAT
    
    # Check if file was actually modified
    changes = _detect_changes(file_path)
    
    success = messenger.report_format_event(
        file_path=file_path,
        action=action_enum,
        changes_detected=changes,
    )
    
    status = "✓ sent" if success else "📁 queued"
    logger.info(f"Format event {status}: {Path(file_path).name}")


def _detect_changes(file_path: str) -> bool:
    """Detect if file has uncommitted changes via git."""
    try:
        import subprocess
        result = subprocess.run(
            ["git", "diff", "--quiet", file_path],
            capture_output=True,
            cwd=Path(file_path).parent,
        )
        return result.returncode != 0  # Non-zero means changes exist
    except Exception:
        return False


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="AIOS Format State Messenger")
    parser.add_argument("--file", "-f", help="File path for format event")
    parser.add_argument("--action", "-a", choices=["format", "save", "check", "sync"], default="format")
    parser.add_argument("--status", "-s", action="store_true", help="Show messenger status")
    parser.add_argument("--test-fallback", action="store_true", help="Test fallback mechanism")
    
    args = parser.parse_args()
    
    messenger = AIOSFormatStateMessenger()
    
    if args.status:
        status = messenger.get_status()
        print(json.dumps(status, indent=2))
        return
    
    if args.test_fallback:
        results = messenger.test_fallback()
        print(json.dumps(results, indent=2))
        return
    
    if args.file:
        handle_format_save(args.file, args.action)
        return
    
    # Default: show status
    status = messenger.get_status()
    print(f"AIOS Format Messenger: {status['connection']}")
    print(f"  Fallback: {'active' if status['fallback_active'] else 'inactive'}")
    print(f"  Queued: {status['events_queued']} | Sent: {status['events_sent']}")


if __name__ == "__main__":
    main()
