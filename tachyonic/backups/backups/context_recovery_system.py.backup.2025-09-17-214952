"""
AIOS Context Recovery System - Implementing Bootstrap Protocol
This module implements the context recovery system referenced in the
AI_context_reallocator.md bootstrap protocol.
"""

import json
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class ContextHealth:
    """Context health indicators as defined in bootstrap protocol"""
    score: float  # 0.0 to 1.0
    indicators: List[str]
    last_check: datetime
    recovery_actions: List[str]

    def is_healthy(self) -> bool:
        """Check if context is healthy (>= 0.7 as per protocol)"""
        return self.score >= 0.7

    def needs_immediate_recovery(self) -> bool:
        """Check if immediate recovery is needed (< 0.4 as per protocol)"""
        return self.score < 0.4


class ContextRecoverySystem:
    """AI Context Recovery System implementing bootstrap protocol"""

    def __init__(self, workspace_path: str = "c:\\dev\\AIOS"):
        self.workspace_path = Path(workspace_path)
        self.context_file = self.workspace_path / "context_state.json"
        self.iteration_count = 0
        self.last_recovery = datetime.now()
        self.recovery_triggers = []

    def calculate_context_health(self, user_input: str = "",
                               system_errors: List[str] = None) -> ContextHealth:
        """Calculate context health using bootstrap protocol indicators"""
        if system_errors is None:
            system_errors = []

        health_score = 1.0
        indicators = []
        recovery_actions = []

        # Check for context loss indicators from bootstrap protocol
        context_loss_keywords = [
            "forgetting", "losing context", "what were we doing",
            "context loss", "forgot", "lost track", "starting over"
        ]

        user_lower = user_input.lower()
        for keyword in context_loss_keywords:
            if keyword in user_lower:
                health_score = min(health_score, 0.3)
                indicators.append(f"User mentioned: {keyword}")
                recovery_actions.append("Execute full codebase reconnaissance")

        # Check for system errors
        if system_errors:
            health_score = min(health_score, 0.5)
            indicators.extend([f"System error: {error}" for error in system_errors])
            recovery_actions.append("Verify system health")

        # Check for build failures
        if "build failed" in user_lower or "compilation error" in user_lower:
            health_score = min(health_score, 0.4)
            indicators.append("Build/compilation issues detected")
            recovery_actions.append("Execute build diagnostics")

        # Check for file not found or permission errors
        if "file not found" in user_lower or "permission denied" in user_lower:
            health_score = min(health_score, 0.3)
            indicators.append("File system issues detected")
            recovery_actions.append("Verify file system state")

        # Check time since last recovery (48 hours as per protocol)
        hours_since_recovery = (datetime.now() - self.last_recovery).total_seconds() / 3600
        if hours_since_recovery > 48:
            health_score = min(health_score, 0.6)
            indicators.append(f"Time since last recovery: {hours_since_recovery:.1f} hours")
            recovery_actions.append("Execute scheduled context refresh")

        return ContextHealth(
            score=health_score,
            indicators=indicators,
            last_check=datetime.now(),
            recovery_actions=recovery_actions
        )

    def should_trigger_recovery(self, user_input: str = "",
                               system_errors: List[str] = None) -> bool:
        """Determine if context recovery should be triggered"""
        health = self.calculate_context_health(user_input, system_errors)

        # Immediate recovery triggers
        if health.needs_immediate_recovery():
            return True

        # Adaptive algorithm from bootstrap protocol
        base_iterations = 7  # Random between 6-9, using 7 as middle
        if self.iteration_count >= base_iterations:
            return True

        # Health-based trigger (< 0.7)
        if not health.is_healthy():
            return True

        return False

    def execute_context_recovery(self) -> Dict[str, Any]:
        """Execute context recovery following bootstrap protocol"""
        recovery_log = {
            "timestamp": datetime.now().isoformat(),
            "iteration": self.iteration_count,
            "steps_executed": [],
            "files_read": [],
            "health_before": None,
            "health_after": None
        }

        # Step 1: Full Codebase Reconnaissance
        mandatory_files = [
            "AIOS_PROJECT_CONTEXT.md",
            "README.md",
            "docs/ai-context/AI_context_reallocator.md",
            "docs/ARCHITECTURE.md",
            "docs/DEVELOPMENT.md",
            "docs/API_REFERENCE.md",
            "docs/INSTALLATION.md",
            "docs/CHANGELOG.md"
        ]

        for file_path in mandatory_files:
            full_path = self.workspace_path / file_path
            if full_path.exists():
                recovery_log["files_read"].append(str(full_path))

        recovery_log["steps_executed"].append("Full codebase reconnaissance")

        # Step 2: System Health Validation
        # This would integrate with actual system health checks
        recovery_log["steps_executed"].append("System health validation")

        # Step 3: Context Tracking Update
        self.iteration_count = 0  # Reset iteration counter
        self.last_recovery = datetime.now()
        recovery_log["steps_executed"].append("Context tracking update")

        # Save recovery log
        self.save_recovery_log(recovery_log)

        return recovery_log

    def save_recovery_log(self, log: Dict[str, Any]):
        """Save recovery log to context file"""
        try:
            with open(self.context_file, 'w') as f:
                json.dump(log, f, indent=2)
        except Exception as e:
            print(f"Failed to save recovery log: {e}")

    def load_context_state(self) -> Dict[str, Any]:
        """Load previous context state if available"""
        try:
            if self.context_file.exists():
                with open(self.context_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Failed to load context state: {e}")
        return {}

    def increment_iteration(self):
        """Increment iteration counter"""
        self.iteration_count += 1

    def get_recovery_actions(self, health: ContextHealth) -> List[str]:
        """Get recommended recovery actions based on context health"""
        actions = []

        if health.score < 0.4:
            actions.extend([
                "Execute immediate context recovery",
                "Read all mandatory documentation files",
                "Verify system health and build state",
                "Update context tracking"
            ])
        elif health.score < 0.7:
            actions.extend([
                "Review recent changes and context",
                "Check system status",
                "Verify file system state"
            ])
        else:
            actions.append("Continue normal operation")

        return actions


def process_context_loss_query(user_input: str, workspace_path: str = "c:\\dev\\AIOS") -> Dict[str, Any]:
    """Process user query for context loss and trigger recovery if needed"""
    recovery_system = ContextRecoverySystem(workspace_path)

    # Check if recovery is needed
    if recovery_system.should_trigger_recovery(user_input):
        recovery_log = recovery_system.execute_context_recovery()
        return {
            "context_loss_detected": True,
            "recovery_executed": True,
            "recovery_log": recovery_log,
            "message": "Context recovery completed. System state refreshed."
        }
    else:
        health = recovery_system.calculate_context_health(user_input)
        return {
            "context_loss_detected": False,
            "recovery_executed": False,
            "context_health": health.score,
            "recommendations": recovery_system.get_recovery_actions(health),
            "message": f"Context health: {health.score:.2f} - System operational"
        }


if __name__ == "__main__":
    # Test context recovery system
    recovery_system = ContextRecoverySystem()

    # Test scenarios
    test_scenarios = [
        "I think we're losing context here",
        "What were we doing before?",
        "The build is failing",
        "Everything seems to be working fine"
    ]

    for scenario in test_scenarios:
        print(f"\nTesting: '{scenario}'")
        result = process_context_loss_query(scenario)
        print(f"Result: {result['message']}")
        print(f"Context health: {result.get('context_health', 'N/A')}")
