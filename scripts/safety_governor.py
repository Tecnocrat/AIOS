"""
AIOS Safety Governor: Critical Safety Control System
Implements mandatory safeguards for consciousness evolution experiments

This module provides essential safety controls including:
- Human authorization requirements
- Resource monitoring and limits
- Emergency shutdown capabilities
- Session time management
- Containment verification
- Comprehensive safety logging

⚠️ CRITICAL: This module must be initialized before any evolutionary operations
"""

import time
import threading
import psutil
import os
import sys
import signal
from pathlib import Path
from typing import Dict, Any, Optional, Callable, List
from dataclasses import dataclass, field
from enum import Enum
import json
import logging
from datetime import datetime, timedelta
import shutil

class SafetyLevel(Enum):
    """Safety operation levels with increasing capabilities and risks"""
    SAFE_MODE = "safe_mode"  # No autonomous operation, human approval required
    SUPERVISED = "supervised"  # Limited autonomous with human check-ins
    ADVANCED = "advanced"  # Extended autonomous with enhanced monitoring
    RESEARCH = "research"  # Experimental mode with multiple safety officers

class EmergencyReason(Enum):
    """Reasons for emergency shutdown"""
    RESOURCE_EXCEEDED = "resource_exceeded"
    HUMAN_INTERVENTION = "human_intervention"
    TIMEOUT = "timeout"
    ANOMALOUS_BEHAVIOR = "anomalous_behavior"
    CONTAINMENT_BREACH = "containment_breach"
    EXTERNAL_THREAT = "external_threat"

@dataclass
class ResourceLimits:
    """Resource limitation configuration"""
    max_cpu_percent: float = 25.0
    max_memory_gb: float = 2.0
    max_disk_gb: float = 1.0
    max_network_connections: int = 5
    max_processes: int = 10
    max_file_handles: int = 100

@dataclass
class SafetySession:
    """Active safety session tracking"""
    session_id: str
    start_time: datetime
    safety_level: SafetyLevel
    authorized_by: str
    resource_limits: ResourceLimits
    max_duration_minutes: int = 30
    check_in_interval_minutes: int = 10
    last_check_in: Optional[datetime] = None
    emergency_contacts: List[str] = field(default_factory=list)
    
    @property
    def is_expired(self) -> bool:
        """Check if session has exceeded maximum duration"""
        if not self.start_time:
            return True
        return datetime.now() - self.start_time > timedelta(minutes=self.max_duration_minutes)
    
    @property
    def needs_check_in(self) -> bool:
        """Check if human check-in is required"""
        if not self.last_check_in:
            return True
        return datetime.now() - self.last_check_in > timedelta(minutes=self.check_in_interval_minutes)

class SafetyGovernor:
    """Critical safety control system for AIOS evolution experiments"""
    
    def __init__(self, 
                 emergency_shutdown_callback: Optional[Callable] = None,
                 safety_log_path: Optional[Path] = None):
        self.emergency_shutdown_callback = emergency_shutdown_callback
        self.safety_log_path = safety_log_path or Path("c:/dev/AIOS/safety_logs")
        self.safety_log_path.mkdir(exist_ok=True)
        
        # Initialize safety state
        self.current_session: Optional[SafetySession] = None
        self.is_emergency_stopped = False
        self.monitoring_active = False
        self.resource_monitor_thread: Optional[threading.Thread] = None
        
        # Setup safety logging
        self.setup_safety_logging()
        
        # Register emergency handlers
        self.setup_emergency_handlers()
        
        # Default resource limits
        self.default_limits = ResourceLimits()
        
        self.safety_logger.critical("🛡️ AIOS Safety Governor initialized - System protected")
    
    def setup_safety_logging(self):
        """Initialize comprehensive safety logging"""
        log_file = self.safety_log_path / f"safety_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        self.safety_logger = logging.getLogger("AIOS_Safety")
        self.safety_logger.setLevel(logging.DEBUG)
        
        handler = logging.FileHandler(log_file)
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.safety_logger.addHandler(handler)
        
        # Also log to console for immediate visibility
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.safety_logger.addHandler(console_handler)
    
    def setup_emergency_handlers(self):
        """Setup system signal handlers for emergency shutdown"""
        def emergency_signal_handler(signum, frame):
            self.emergency_shutdown(EmergencyReason.EXTERNAL_THREAT, 
                                  f"Signal {signum} received")
        
        signal.signal(signal.SIGINT, emergency_signal_handler)
        signal.signal(signal.SIGTERM, emergency_signal_handler)
    
    def request_authorization(self, 
                            experiment_description: str,
                            safety_level: SafetyLevel = SafetyLevel.SAFE_MODE,
                            duration_minutes: int = 30,
                            authorized_by: str = "unknown") -> bool:
        """
        Request human authorization for evolutionary experiment
        
        ⚠️ CRITICAL: This MUST be called before any autonomous operation
        """
        self.safety_logger.warning(f"🔐 Authorization requested for: {experiment_description}")
        self.safety_logger.warning(f"   Safety Level: {safety_level.value}")
        self.safety_logger.warning(f"   Duration: {duration_minutes} minutes")
        self.safety_logger.warning(f"   Authorized by: {authorized_by}")
        
        # In a real implementation, this would require actual human interaction
        # For now, we'll simulate the authorization process
        
        print("\n" + "="*80)
        print("🛡️  AIOS SAFETY GOVERNOR - AUTHORIZATION REQUIRED")
        print("="*80)
        print(f"Experiment: {experiment_description}")
        print(f"Safety Level: {safety_level.value}")
        print(f"Duration: {duration_minutes} minutes")
        print(f"Authorized by: {authorized_by}")
        print("\nThis experiment involves autonomous code evolution.")
        print("Please review the safety implications carefully.")
        print("="*80)
        
        # Non-interactive / CI auto-approval path
        auto_env = os.environ.get("AIOS_SAFETY_AUTO_APPROVE", "").lower()
        if auto_env in {"1", "true", "yes", "y"}:
            self.safety_logger.critical(
                "✅ AUTO-AUTHORIZED via env flag by %s" % authorized_by
            )
            return True

        # Interactive prompt (default path)
        response = input(
            "Authorize this experiment? (yes/no): "
        ).strip().lower()
        
        if response in ['yes', 'y']:
            self.safety_logger.critical(
                "✅ Experiment AUTHORIZED by %s" % authorized_by
            )
            return True
        else:
            self.safety_logger.critical(
                "❌ Experiment DENIED by %s" % authorized_by
            )
            return False
    
    def start_supervised_session(
        self,
        experiment_description: str,
        safety_level: SafetyLevel = SafetyLevel.SAFE_MODE,
        duration_minutes: int = 30,
        authorized_by: str = "developer"
    ) -> bool:
        """Start a supervised safety session"""
        
        # Check if already in session
        if self.current_session:
            self.safety_logger.error(
                "❌ Cannot start session - another session active"
            )
            return False
        
        # Request authorization
        if not self.request_authorization(
            experiment_description,
            safety_level,
            duration_minutes,
            authorized_by
        ):
            return False
        
        # Create session
        session_id = f"safety_{int(time.time())}"
        self.current_session = SafetySession(
            session_id=session_id,
            start_time=datetime.now(),
            safety_level=safety_level,
            authorized_by=authorized_by,
            resource_limits=self.default_limits,
            max_duration_minutes=duration_minutes
        )
        
        # Start monitoring
        self.start_monitoring()
        
        self.safety_logger.critical(f"🟢 Safety session started: {session_id}")
        return True
    
    def start_monitoring(self):
        """Start resource and safety monitoring"""
        if self.monitoring_active:
            return
        
        self.monitoring_active = True
        self.resource_monitor_thread = threading.Thread(
            target=self._monitor_resources,
            daemon=True
        )
        self.resource_monitor_thread.start()
        
        self.safety_logger.info("📊 Resource monitoring started")
    
    def _monitor_resources(self):
        """Background resource monitoring loop"""
        while self.monitoring_active and not self.is_emergency_stopped:
            try:
                if not self.current_session:
                    time.sleep(1)
                    continue
                
                # Check session timeout
                if self.current_session.is_expired:
                    self.emergency_shutdown(
                        EmergencyReason.TIMEOUT,
                        "Session duration exceeded"
                    )
                    break
                
                # Check human check-in requirement
                if (
                    self.current_session.safety_level != SafetyLevel.SAFE_MODE
                    and self.current_session.needs_check_in
                ):
                    self.safety_logger.warning("⏰ Human check-in required")
                    # In production, this should trigger actual notification
                
                # Monitor system resources
                cpu_percent = psutil.cpu_percent(interval=1)
                memory = psutil.virtual_memory()
                memory_gb = memory.used / (1024**3)
                # Disk usage (approximate) for workspace drive
                try:
                    disk_usage = shutil.disk_usage(self.safety_log_path.anchor)
                    disk_used_gb = (
                        (disk_usage.total - disk_usage.free) / (1024**3)
                    )
                except Exception:
                    disk_used_gb = 0.0
                # Network connections count
                try:
                    net_conns = len(psutil.net_connections())
                except Exception:
                    net_conns = 0
                # Process / handle counts (current proc + children)
                try:
                    proc = psutil.Process()
                    child_procs = proc.children(recursive=True)
                    process_count = 1 + len(child_procs)
                except Exception:
                    process_count = 1
                # File handle / descriptor count (platform specific)
                handle_count = None
                try:
                    if hasattr(proc, 'num_handles'):
                        handle_count = proc.num_handles()
                    elif hasattr(proc, 'num_fds'):
                        handle_count = proc.num_fds()
                except Exception:
                    handle_count = None
                
                limits = self.current_session.resource_limits
                
                # Check CPU limit
                if cpu_percent > limits.max_cpu_percent:
                    self.emergency_shutdown(
                        EmergencyReason.RESOURCE_EXCEEDED,
                        f"CPU {cpu_percent}% > {limits.max_cpu_percent}%"
                    )
                    break
                
                # Check memory limit
                if memory_gb > limits.max_memory_gb:
                    self.emergency_shutdown(
                        EmergencyReason.RESOURCE_EXCEEDED,
                        f"Mem {memory_gb:.2f}GB > {limits.max_memory_gb}GB"
                    )
                    break
                # Disk usage
                if (
                    limits.max_disk_gb > 0
                    and disk_used_gb > limits.max_disk_gb
                ):
                    self.emergency_shutdown(
                        EmergencyReason.RESOURCE_EXCEEDED,
                        f"Disk {disk_used_gb:.2f}GB > {limits.max_disk_gb}GB"
                    )
                    break
                # Network connections
                if (
                    limits.max_network_connections > 0
                    and net_conns > limits.max_network_connections
                ):
                    self.emergency_shutdown(
                        EmergencyReason.RESOURCE_EXCEEDED,
                        (
                            f"NetConns {net_conns} > "
                            f"{limits.max_network_connections}"
                        )
                    )
                    break
                # Process count
                if (
                    limits.max_processes > 0
                    and process_count > limits.max_processes
                ):
                    self.emergency_shutdown(
                        EmergencyReason.RESOURCE_EXCEEDED,
                        f"Processes {process_count} > {limits.max_processes}"
                    )
                    break
                # File handles
                if (
                    handle_count is not None
                    and limits.max_file_handles > 0
                    and handle_count > limits.max_file_handles
                ):
                    self.emergency_shutdown(
                        EmergencyReason.RESOURCE_EXCEEDED,
                        f"Handles {handle_count} > {limits.max_file_handles}"
                    )
                    break
                
                # Log resource status periodically
                if int(time.time()) % 30 == 0:  # Every ~30 seconds
                    summary = (
                        f"CPU {cpu_percent:.1f}%, "
                        f"Mem {memory_gb:.2f}GB/{limits.max_memory_gb}GB, "
                        f"Disk {disk_used_gb:.2f}GB/{limits.max_disk_gb}GB, "
                        f"Net {net_conns}/{limits.max_network_connections}, "
                        f"Proc {process_count}/{limits.max_processes}"
                    )
                    if handle_count is not None:
                        summary += (
                            ", Handles %s/%s" % (
                                handle_count,
                                limits.max_file_handles,
                            )
                        )
                    self.safety_logger.info(f"📊 Resources: {summary}")
                
                time.sleep(1)
                
            except Exception as e:
                self.safety_logger.error(f"❌ Monitoring error: {e}")
                time.sleep(5)
    
    def human_check_in(self, operator: str) -> bool:
        """Record human check-in for ongoing session"""
        if not self.current_session:
            self.safety_logger.error("❌ No active session for check-in")
            return False
        
        self.current_session.last_check_in = datetime.now()
        self.safety_logger.info(f"✅ Human check-in recorded: {operator}")
        return True
    
    def emergency_shutdown(self, reason: EmergencyReason, details: str = ""):
        """Immediately shutdown all autonomous operations"""
        self.is_emergency_stopped = True
        self.monitoring_active = False
        
        self.safety_logger.critical(f"🚨 EMERGENCY SHUTDOWN: {reason.value}")
        self.safety_logger.critical(f"   Details: {details}")
        
        # Call emergency callback if provided
        if self.emergency_shutdown_callback:
            try:
                self.emergency_shutdown_callback(reason, details)
            except Exception as e:
                self.safety_logger.error(f"❌ Emergency callback failed: {e}")
        
        # Terminate current session
        if self.current_session:
            self.safety_logger.critical(
                f"   Session terminated: {self.current_session.session_id}"
            )
            self.current_session = None
        
        print("\n" + "="*80)
        print("🚨 AIOS EMERGENCY SHUTDOWN ACTIVATED")
        print("="*80)
        print(f"Reason: {reason.value}")
        print(f"Details: {details}")
        print("All autonomous operations have been terminated.")
        print("Human intervention required to restart system.")
        print("="*80)
    
    def is_operation_authorized(self, operation_name: str) -> bool:
        """Check if an operation is authorized under current safety session"""
        if self.is_emergency_stopped:
            self.safety_logger.error(
                "❌ Blocked - emergency stop: %s" % operation_name
            )
            return False
        
        if not self.current_session:
            self.safety_logger.error(
                "❌ Operation blocked - no active session: %s" % operation_name
            )
            return False
        
        if self.current_session.is_expired:
            self.emergency_shutdown(
                EmergencyReason.TIMEOUT,
                "Session expired during operation",
            )
            return False
        
        self.safety_logger.debug(f"✅ Operation authorized: {operation_name}")
        return True
    
    def end_session(self, operator: str = "unknown"):
        """Safely end the current session"""
        if not self.current_session:
            self.safety_logger.warning("⚠️ No active session to end")
            return
        
        session_id = self.current_session.session_id
        self.monitoring_active = False
        self.current_session = None
        
        self.safety_logger.critical(
            "🔴 Safety session ended by %s: %s" % (operator, session_id)
        )
        print(f"\n✅ Safety session ended successfully: {session_id}")
    
    def get_status(self) -> Dict[str, Any]:
        """Get current safety status"""
        status: Dict[str, Any] = {
            "emergency_stopped": self.is_emergency_stopped,
            "session_active": self.current_session is not None,
            "monitoring_active": self.monitoring_active
        }
        
        if self.current_session:
            status["session_id"] = self.current_session.session_id
            status["safety_level"] = self.current_session.safety_level.value
            status["authorized_by"] = self.current_session.authorized_by
            status["start_time"] = self.current_session.start_time.isoformat()
            status["expired"] = self.current_session.is_expired
            status["needs_check_in"] = self.current_session.needs_check_in
        
        return status

    # --- Pre-operation verification ---
    def verify_pre_experiment(self,
                              requested_population_size: int,
                              requested_generations: int,
                              max_population: int = 50,
                              max_generations: int = 20) -> Dict[str, Any]:
        """Verify checklist conditions before starting an evolution experiment.

        Returns dict with:
          ok: overall pass boolean
          failures: list of unmet checklist items (empty if ok)
          checklist: mapping of item -> pass bool
        """
        checklist: Dict[str, bool] = {}
        failures: List[str] = []

        # Session & authorization
        checklist['session_active'] = self.current_session is not None
        # Monitoring
        checklist['monitoring_active'] = self.monitoring_active
        # Emergency state
        checklist['not_emergency_stopped'] = not self.is_emergency_stopped
        # Session not expired
        checklist['session_not_expired'] = bool(
            self.current_session and not self.current_session.is_expired
        )
        # Population cap
        checklist['population_within_limit'] = (
            requested_population_size <= max_population
        )
        # Generations cap
        checklist['generations_within_limit'] = (
            requested_generations <= max_generations
        )

        # Network isolation (basic: current connections within limit)
        try:
            net_conns = len(psutil.net_connections())
            limit = (
                self.current_session.resource_limits.max_network_connections
                if self.current_session else 0
            )
            checklist['network_within_limit'] = (
                (limit == 0) or net_conns <= limit
            )
        except Exception:
            # Don't block if inspection fails
            checklist['network_within_limit'] = True

        # Process count
        try:
            proc = psutil.Process()
            process_count = 1 + len(proc.children(recursive=True))
            limit_proc = (
                self.current_session.resource_limits.max_processes
                if self.current_session else 0
            )
            checklist['process_within_limit'] = (
                (limit_proc == 0) or process_count <= limit_proc
            )
        except Exception:
            checklist['process_within_limit'] = True

        # Aggregate failures
        for item, passed in checklist.items():
            if not passed:
                failures.append(item)

        ok = len(failures) == 0
        if not ok:
            self.safety_logger.error(
                f"❌ Pre-experiment safety verification failed: {failures}"
            )
        else:
            self.safety_logger.info(
                "🛡️ Pre-experiment safety verification passed"
            )

        return {"ok": ok, "failures": failures, "checklist": checklist}

# Global safety governor instance
_safety_governor: Optional[SafetyGovernor] = None


def get_safety_governor() -> SafetyGovernor:
    """Get the global safety governor instance"""
    global _safety_governor
    if _safety_governor is None:
        _safety_governor = SafetyGovernor()
    return _safety_governor


def require_safety_authorization(operation_name: str) -> bool:
    """Decorator function to require safety authorization for operations"""
    governor = get_safety_governor()
    return governor.is_operation_authorized(operation_name)

# Emergency shutdown function for external access

def emergency_shutdown(reason: str = "Manual shutdown"):
    """External emergency shutdown trigger"""
    governor = get_safety_governor()
    governor.emergency_shutdown(EmergencyReason.HUMAN_INTERVENTION, reason)


if __name__ == "__main__":
    # Test safety governor
    print("🛡️ Testing AIOS Safety Governor")
    
    governor = SafetyGovernor()
    
    # Test authorization
    if governor.start_supervised_session(
        "Test consciousness evolution experiment",
        SafetyLevel.SUPERVISED,
        5,  # 5 minutes
        "test_operator"
    ):
        print("✅ Session started successfully")
        
        # Simulate some work
        time.sleep(2)
        
        # Test check-in
        governor.human_check_in("test_operator")
        
        # End session
        governor.end_session("test_operator")
    else:
        print("❌ Session authorization failed")
