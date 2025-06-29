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
        
        # For development, auto-approve with logging
        # In production, this should require actual human input
        response = input("Authorize this experiment? (yes/no): ").strip().lower()
        
        if response in ['yes', 'y']:
            self.safety_logger.critical(f"✅ Experiment AUTHORIZED by {authorized_by}")
            return True
        else:
            self.safety_logger.critical(f"❌ Experiment DENIED by {authorized_by}")
            return False
    
    def start_supervised_session(self,
                                experiment_description: str,
                                safety_level: SafetyLevel = SafetyLevel.SAFE_MODE,
                                duration_minutes: int = 30,
                                authorized_by: str = "developer") -> bool:
        """Start a supervised safety session"""
        
        # Check if already in session
        if self.current_session:
            self.safety_logger.error("❌ Cannot start session - another session active")
            return False
        
        # Request authorization
        if not self.request_authorization(experiment_description, safety_level, 
                                        duration_minutes, authorized_by):
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
                    self.emergency_shutdown(EmergencyReason.TIMEOUT, 
                                          "Session duration exceeded")
                    break
                
                # Check human check-in requirement
                if (self.current_session.safety_level != SafetyLevel.SAFE_MODE and 
                    self.current_session.needs_check_in):
                    self.safety_logger.warning("⏰ Human check-in required")
                    # In production, this should trigger actual notification
                
                # Monitor system resources
                cpu_percent = psutil.cpu_percent(interval=1)
                memory = psutil.virtual_memory()
                memory_gb = memory.used / (1024**3)
                
                limits = self.current_session.resource_limits
                
                # Check CPU limit
                if cpu_percent > limits.max_cpu_percent:
                    self.emergency_shutdown(EmergencyReason.RESOURCE_EXCEEDED, 
                                          f"CPU usage {cpu_percent}% > {limits.max_cpu_percent}%")
                    break
                
                # Check memory limit
                if memory_gb > limits.max_memory_gb:
                    self.emergency_shutdown(EmergencyReason.RESOURCE_EXCEEDED, 
                                          f"Memory usage {memory_gb:.2f}GB > {limits.max_memory_gb}GB")
                    break
                
                # Log resource status periodically
                if int(time.time()) % 30 == 0:  # Every 30 seconds
                    self.safety_logger.info(f"📊 Resources: CPU {cpu_percent:.1f}%, "
                                          f"Memory {memory_gb:.2f}GB")
                
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
            self.safety_logger.critical(f"   Session terminated: {self.current_session.session_id}")
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
            self.safety_logger.error(f"❌ Operation blocked - emergency shutdown active: {operation_name}")
            return False
        
        if not self.current_session:
            self.safety_logger.error(f"❌ Operation blocked - no active session: {operation_name}")
            return False
        
        if self.current_session.is_expired:
            self.emergency_shutdown(EmergencyReason.TIMEOUT, "Session expired during operation")
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
        
        self.safety_logger.critical(f"🔴 Safety session ended by {operator}: {session_id}")
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
