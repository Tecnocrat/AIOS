"""
AIOS Python Environment Integration
=================================

Integrates robust Python environment management with AIOS fractal/holographic
context system, enabling self-healing and context-aware environment handling.
"""

import json
import logging
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

from robust_python_environment_manager import (
    PythonEnvironment,
    RobustPythonEnvironmentManager,
    get_environment_manager,
)


class AIOSPythonEnvironmentIntegration:
    """
    AIOS integration for Python environment management.
    Provides context-aware environment handling and self-healing capabilities.
    """

    def __init__(self, context_manager=None):
        self.env_manager = get_environment_manager()
        self.context_manager = context_manager
        self.logger = logging.getLogger("AIOS.PythonEnvIntegration")

        # Integration state
        self.last_health_check = None
        self.environment_snapshots = {}
        self.recovery_strategies = []

        # Initialize integration
        self._initialize_integration()

    def _initialize_integration(self):
        """Initialize the AIOS-Python environment integration."""
        self.logger.info("Initializing AIOS Python Environment Integration")

        # Perform initial health check
        self.perform_health_check()

        # Set up auto-recovery strategies
        self._setup_recovery_strategies()

        # Register with context manager if available
        if self.context_manager:
            self._register_with_context_manager()

    def _setup_recovery_strategies(self):
        """Set up automatic recovery strategies for common issues."""
        self.recovery_strategies = [
            {
                "name": "path_recovery",
                "description": "Recover from PATH issues by rediscovering environments",  # noqa
                "condition": lambda health: health["healthy_environments"] == 0,  # noqa
                "action": self._recover_from_path_issues,
            },
            {
                "name": "missing_active_environment",
                "description": "Set active environment when none is active",
                "condition": lambda health: health["active_environment"]
                is None,  # noqa
                "action": self._recover_missing_active_environment,
            },
            {
                "name": "broken_environment_cleanup",
                "description": "Clean up broken/missing environments",
                "condition": lambda health: health["missing_environments"] > 0,  # noqa
                "action": self._cleanup_broken_environments,
            },
        ]

    def _register_with_context_manager(self):
        """Register Python environment state with AIOS context manager."""
        if hasattr(self.context_manager, "register_subsystem"):
            self.context_manager.register_subsystem(
                "python_environment",
                self.get_environment_snapshot,
                self.restore_environment_snapshot,
            )

    def perform_health_check(self) -> Dict[str, Any]:
        """Perform comprehensive health check with AIOS integration."""
        self.logger.info("Performing Python environment health check")

        # Get basic health report
        health_report = self.env_manager.health_check()

        # Add AIOS-specific information
        health_report["aios_integration"] = {
            "integration_active": True,
            "context_manager_available": self.context_manager is not None,
            "recovery_strategies_available": len(self.recovery_strategies),
            "last_health_check": self.last_health_check,
            "environment_snapshots_count": len(self.environment_snapshots),
        }

        # Check for issues and apply recovery strategies
        recovery_applied = self._apply_recovery_strategies(health_report)
        health_report["aios_integration"]["recovery_applied"] = recovery_applied

        self.last_health_check = datetime.now().isoformat()
        return health_report

    def _apply_recovery_strategies(
        self, health_report: Dict[str, Any]
    ) -> List[str]:  # noqa
        """Apply recovery strategies based on health report."""
        applied_strategies = []

        for strategy in self.recovery_strategies:
            try:
                if strategy["condition"](health_report):
                    self.logger.info(
                        f"Applying recovery strategy: {strategy['name']}"
                    )  # noqa
                    success = strategy["action"](health_report)

                    if success:
                        applied_strategies.append(strategy["name"])
                        self.logger.info(
                            f"Recovery strategy '{strategy['name']}' applied successfully"
                        )  # noqa
                    else:
                        self.logger.warning(
                            f"Recovery strategy '{strategy['name']}' failed"
                        )  # noqa

            except Exception as e:
                self.logger.error(
                    f"Error applying recovery strategy '{strategy['name']}': {e}"
                )  # noqa

        return applied_strategies

    def _recover_from_path_issues(self, health_report: Dict[str, Any]) -> bool:
        """Recover from Python PATH issues."""
        try:
            self.logger.info("Attempting to recover from PATH issues")

            # Force rediscovery of environments
            healthy_count = self.env_manager.refresh_environments()

            if healthy_count > 0:
                self.logger.info(
                    f"Recovered {healthy_count} healthy environments"
                )  # noqa
                return True
            else:
                self.logger.warning(
                    "No healthy environments found after PATH recovery"
                )  # noqa
                return False

        except Exception as e:
            self.logger.error(f"PATH recovery failed: {e}")
            return False

    def _recover_missing_active_environment(
        self, health_report: Dict[str, Any]
    ) -> bool:  # noqa
        """Recover when no active environment is set."""
        try:
            environments = self.env_manager.list_environments()
            healthy_envs = [
                env for env in environments if env.health_status == "healthy"
            ]

            if healthy_envs:
                # Prefer virtual environments
                preferred_env = None
                for env in healthy_envs:
                    if env.is_virtual:
                        preferred_env = env
                        break

                if not preferred_env:
                    preferred_env = healthy_envs[0]

                success = self.env_manager.set_active_environment(
                    preferred_env.id
                )  # noqa
                if success:
                    self.logger.info(
                        f"Set active environment: {preferred_env.name}"
                    )  # noqa
                    return True

            return False

        except Exception as e:
            self.logger.error(f"Active environment recovery failed: {e}")
            return False

    def _cleanup_broken_environments(
        self, health_report: Dict[str, Any]
    ) -> bool:  # noqa
        """Clean up broken/missing environments."""
        try:
            environments = self.env_manager.list_environments()
            cleaned_count = 0

            for env in environments:
                if env.health_status in ["missing", "broken"]:
                    # Create snapshot before removal
                    self.create_environment_snapshot(
                        env.id, f"cleanup_{env.id}"
                    )  # noqa

                    # Remove from active environments
                    if env.id in self.env_manager.environments:
                        del self.env_manager.environments[env.id]
                        cleaned_count += 1

            if cleaned_count > 0:
                self.env_manager._save_environments()
                self.logger.info(
                    f"Cleaned up {cleaned_count} broken environments"
                )  # noqa
                return True

            return False

        except Exception as e:
            self.logger.error(f"Environment cleanup failed: {e}")
            return False

    def get_environment_snapshot(self) -> Dict[str, Any]:
        """Get current environment state snapshot for context preservation."""
        snapshot = {
            "timestamp": datetime.now().isoformat(),
            "active_environment": None,
            "environments": [],
            "health_status": None,
        }

        try:
            # Get active environment
            active_env = self.env_manager.get_active_environment()
            if active_env:
                snapshot["active_environment"] = {
                    "id": active_env.id,
                    "name": active_env.name,
                    "python_path": active_env.python_path,
                    "version": active_env.version,
                }

            # Get all environments
            for env in self.env_manager.list_environments():
                snapshot["environments"].append(
                    {
                        "id": env.id,
                        "name": env.name,
                        "python_path": env.python_path,
                        "version": env.version,
                        "is_virtual": env.is_virtual,
                        "health_status": env.health_status,
                        "is_active": env.is_active,
                    }
                )

            # Get health status
            snapshot["health_status"] = self.env_manager.health_check()

        except Exception as e:
            self.logger.error(f"Error creating environment snapshot: {e}")

        return snapshot

    def restore_environment_snapshot(self, snapshot: Dict[str, Any]) -> bool:
        """Restore environment state from snapshot."""
        try:
            self.logger.info("Restoring Python environment from snapshot")

            # Refresh current environments first
            self.env_manager.refresh_environments()

            # Try to restore active environment
            if snapshot.get("active_environment"):
                active_env_info = snapshot["active_environment"]

                # Find matching environment by path
                for env in self.env_manager.list_environments():
                    if (
                        os.path.normpath(env.python_path).lower()
                        == os.path.normpath(active_env_info["python_path"]).lower()
                    ):  # noqa
                        success = self.env_manager.set_active_environment(
                            env.id
                        )  # noqa
                        if success:
                            self.logger.info(
                                f"Restored active environment: {env.name}"
                            )  # noqa
                            return True

            # If specific environment not found, try recovery
            self._recover_missing_active_environment({})
            return True

        except Exception as e:
            self.logger.error(f"Environment snapshot restoration failed: {e}")
            return False

    def create_environment_snapshot(
        self, env_id: str, snapshot_name: str = None
    ) -> str:  # noqa
        """Create a named snapshot of a specific environment."""
        if snapshot_name is None:
            snapshot_name = (
                f"snapshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}"  # noqa
            )

        try:
            if env_id in self.env_manager.environments:
                env = self.env_manager.environments[env_id]
                snapshot = {
                    "timestamp": datetime.now().isoformat(),
                    "environment": {
                        "id": env.id,
                        "name": env.name,
                        "python_path": env.python_path,
                        "version": env.version,
                        "is_virtual": env.is_virtual,
                        "virtual_env_path": env.virtual_env_path,
                        "packages": env.packages,
                        "health_status": env.health_status,
                    },
                }

                self.environment_snapshots[snapshot_name] = snapshot
                self.logger.info(f"Created environment snapshot: {snapshot_name}")
                return snapshot_name

        except Exception as e:
            self.logger.error(f"Error creating environment snapshot: {e}")

        return ""

    def get_diagnostic_report(self) -> Dict[str, Any]:
        """Get comprehensive diagnostic report for troubleshooting."""
        report = {
            "timestamp": datetime.now().isoformat(),
            "platform": os.name,
            "current_working_directory": os.getcwd(),
            "python_path_env": os.environ.get("PYTHONPATH", "Not set"),
            "path_env": os.environ.get("PATH", "Not available"),
            "health_check": self.perform_health_check(),
            "environment_manager_state": {
                "config_dir": self.env_manager.config_dir,
                "environments_file_exists": os.path.exists(
                    self.env_manager.environments_file
                ),  # noqa
                "backup_file_exists": os.path.exists(
                    self.env_manager.backup_file
                ),  # noqa
                "total_environments": len(self.env_manager.environments),
            },
            "integration_state": {
                "context_manager_available": self.context_manager is not None,
                "recovery_strategies_count": len(self.recovery_strategies),
                "snapshots_count": len(self.environment_snapshots),
                "last_health_check": self.last_health_check,
            },
        }

        return report

    def prepare_for_os_reinstall(self) -> str:
        """Prepare environment configuration for OS reinstall."""
        self.logger.info("Preparing Python environment for OS reinstall")

        try:
            # Create comprehensive backup
            backup_data = {
                "export_timestamp": datetime.now().isoformat(),
                "platform": os.name,
                "aios_version": "1.0.0",
                "environment_snapshot": self.get_environment_snapshot(),
                "diagnostic_report": self.get_diagnostic_report(),
                "recovery_instructions": self._generate_recovery_instructions(),
            }

            # Save to backup file
            backup_filename = f"aios_python_env_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"  # noqa
            backup_path = os.path.join(
                self.env_manager.config_dir, backup_filename
            )  # noqa

            with open(backup_path, "w") as f:
                json.dump(backup_data, f, indent=2)

            self.logger.info(f"Environment backup created: {backup_path}")
            return backup_path

        except Exception as e:
            self.logger.error(f"Error preparing for OS reinstall: {e}")
            return ""

    def _generate_recovery_instructions(self) -> List[str]:
        """Generate step-by-step recovery instructions."""
        instructions = [
            "1. Install Python (recommended: latest stable version)",
            "2. Install pip and virtualenv",
            "3. Create virtual environment for AIOS",
            "4. Install required packages from requirements.txt",
            "5. Run AIOS Python environment initialization",
            "6. Import environment configuration backup",
            "7. Verify environment health",
            "8. Test AIOS integration",
        ]

        # Add specific package requirements if available
        active_env = self.env_manager.get_active_environment()
        if active_env and active_env.packages:
            instructions.append(
                f"Packages to install: {', '.join(active_env.packages[:10])}"
            )  # noqa

        return instructions

    def post_reinstall_recovery(self, backup_file: str) -> bool:
        """Recover environment configuration after OS reinstall."""
        try:
            self.logger.info(f"Recovering from backup: {backup_file}")

            # Load backup data
            with open(backup_file, "r") as f:
                backup_data = json.load(f)

            # Refresh current environments
            self.env_manager.refresh_environments()

            # Try to restore from snapshot
            if "environment_snapshot" in backup_data:
                success = self.restore_environment_snapshot(
                    backup_data["environment_snapshot"]
                )
                if success:
                    self.logger.info("Environment recovery successful")
                    return True

            # Fallback: try to set any healthy environment as active
            self._recover_missing_active_environment({})
            return True

        except Exception as e:
            self.logger.error(f"Post-reinstall recovery failed: {e}")
            return False


# Global integration instance
_global_integration = None


def get_aios_python_integration(context_manager=None):
    """Get the global AIOS Python environment integration instance."""
    global _global_integration
    if _global_integration is None:
        _global_integration = AIOSPythonEnvironmentIntegration(context_manager)
    return _global_integration


def initialize_aios_python_environment(context_manager=None):
    """Initialize AIOS Python environment integration."""
    integration = get_aios_python_integration(context_manager)

    # Perform initial health check
    health_report = integration.perform_health_check()

    print("AIOS Python Environment Integration Initialized")
    print(f"Healthy environments: {health_report['healthy_environments']}")
    print(
        f"Recovery strategies applied: {health_report['aios_integration']['recovery_applied']}"
    )  # noqa

    return integration


if __name__ == "__main__":
    # Demo the AIOS integration
    print("AIOS Python Environment Integration Demo")
    print("=" * 50)

    integration = initialize_aios_python_environment()

    # Show diagnostic report
    diagnostic = integration.get_diagnostic_report()
    print("\nDiagnostic Report:")
    print(
        f"Total environments: {diagnostic['health_check']['total_environments']}"
    )  # noqa
    print(
        f"Healthy environments: {diagnostic['health_check']['healthy_environments']}"
    )  # noqa

    if diagnostic["health_check"]["active_environment"]:
        print(
            f"Active environment: {diagnostic['health_check']['active_environment']['name']}"
        )  # noqa

    # Create backup for OS reinstall preparation
    backup_file = integration.prepare_for_os_reinstall()
    if backup_file:
        print(f"\nOS reinstall backup created: {backup_file}")
