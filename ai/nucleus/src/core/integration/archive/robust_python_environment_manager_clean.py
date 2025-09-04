"""
AIOS Robust Python Environment Manager
=====================================

Handles Python interpreter discovery, environment management, and PATH
resolution with resilience to OS reinstalls and environment changes.

Features:
- Auto-discovery of Python installations
- Virtual environment management
- PATH persistence and recovery
- Environment health monitoring
- Cross-platform compatibility
- Integration with AIOS fractal/holographic context
"""

import json
import logging
import os
import platform
import subprocess
import uuid
import winreg
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class PythonEnvironment:
    """Represents a Python environment configuration."""
    id: str
    name: str
    python_path: str
    version: str
    is_virtual: bool
    virtual_env_path: Optional[str]
    packages: List[str]
    is_active: bool
    last_verified: str
    health_status: str


class RobustPythonEnvironmentManager:
    """
    Robust Python environment manager for AIOS.
    Designed to survive OS reinstalls and PATH changes.
    """

    def __init__(self, config_dir: str = None):
        self.config_dir = config_dir or os.path.join(os.getcwd(), "config")
        self.environments_file = os.path.join(
            self.config_dir, "python_environments.json"
        )
        self.backup_file = os.path.join(
            self.config_dir, "python_environments_backup.json"
        )
        self.logger = self._setup_logging()

        # Ensure config directory exists
        os.makedirs(self.config_dir, exist_ok=True)

        # Load existing environments
        self.environments: Dict[str, PythonEnvironment] = (
            self._load_environments()
        )

        # Current active environment
        self.active_environment: Optional[PythonEnvironment] = None

    def _setup_logging(self) -> logging.Logger:
        """Setup logging for environment manager."""
        logger = logging.getLogger("AIOS.PythonEnvManager")
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    def _load_environments(self) -> Dict[str, PythonEnvironment]:
        """Load environments from configuration file."""
        environments = {}

        # Try to load from main file
        if os.path.exists(self.environments_file):
            try:
                with open(self.environments_file, 'r') as f:
                    data = json.load(f)
                    for env_id, env_data in data.items():
                        environments[env_id] = PythonEnvironment(**env_data)
                self.logger.info(
                    f"Loaded {len(environments)} environments from config"
                )
            except Exception as e:
                self.logger.error(f"Error loading environments: {e}")

        # Try backup if main file failed
        if not environments and os.path.exists(self.backup_file):
            try:
                with open(self.backup_file, 'r') as f:
                    data = json.load(f)
                    for env_id, env_data in data.items():
                        environments[env_id] = PythonEnvironment(**env_data)
                self.logger.info(
                    f"Loaded {len(environments)} environments from backup"
                )
            except Exception as e:
                self.logger.error(f"Error loading backup environments: {e}")

        return environments

    def _save_environments(self):
        """Save environments to configuration file with backup."""
        try:
            # Create backup first
            if os.path.exists(self.environments_file):
                import shutil
                shutil.copy2(self.environments_file, self.backup_file)

            # Save current state
            data = {
                env_id: asdict(
                env) for env_id, env in self.environments.items()
            }
            with open(self.environments_file, 'w') as f:
                json.dump(data, f, indent=2)

            self.logger.info(
                f"Saved {len(self.environments)} environments to config"
            )

        except Exception as e:
            self.logger.error(f"Error saving environments: {e}")

    def discover_python_installations(self) -> List[PythonEnvironment]:
        """Discover all Python installations on the system."""
        installations = []

        # Windows-specific discovery
        if platform.system() == "Windows":
            installations.extend(self._discover_windows_python())

        # Cross-platform discovery
        installations.extend(self._discover_path_python())
        installations.extend(self._discover_conda_environments())
        installations.extend(self._discover_virtual_environments())

        # Remove duplicates and verify
        unique_installations = self._deduplicate_installations(installations)
        verified_installations = []

        for env in unique_installations:
            if self._verify_python_installation(env.python_path):
                env.health_status = "healthy"
                env.last_verified = datetime.now().isoformat()
                verified_installations.append(env)

        self.logger.info(
            f"Discovered {len(verified_installations)} valid Python "
            f"installations"
        )
        return verified_installations

    def _discover_windows_python(self) -> List[PythonEnvironment]:
        """Discover Python installations on Windows using registry."""
        installations = []

        try:
            # Check Windows Registry for Python installations
            for hive in [winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER]:
                try:
                    with winreg.OpenKey(
                    hive, r"SOFTWARE\Python\PythonCore") as key:  # noqa
                        i = 0
                        while True:
                            try:
                                version = winreg.EnumKey(key, i)
                                with winreg.OpenKey(
                                    key, f"{version}\\InstallPath"
                                ) as install_key:
                                    install_path = winreg.QueryValue(
                                        install_key, ""
                                    )
                                    python_exe = os.path.join(
                                        install_path, "python.exe"
                                    )

                                    if os.path.exists(python_exe):
                                        env = PythonEnvironment(
                                            id=str(uuid.uuid4()),
                                            name=f"Python {version}",
                                            python_path=python_exe,
                                            version=version,
                                            is_virtual=False,
                                            virtual_env_path=None,
                                            packages=[],
                                            is_active=False,
                                            last_verified="",
                                            health_status="unknown"
                                        )
                                        installations.append(env)

                                i += 1
                            except OSError:
                                break

                except OSError:
                    continue

        except Exception as e:
            self.logger.error(
                f"Error discovering Windows Python installations: {e}"
            )

        return installations

    def _discover_path_python(self) -> List[PythonEnvironment]:
        """Discover Python installations in system PATH."""
        installations = []

        # Common Python executable names
        python_names = [
            "python", "python3", "python3.8", "python3.9",
            "python3.10", "python3.11", "python3.12"
        ]

        for python_name in python_names:
            try:
                result = subprocess.run(
                    ["where" if platform.system() == "Windows" else "which",
                     python_name],
                    capture_output=True,
                    text=True,
                    timeout=10
                )

                if result.returncode == 0:
                    python_path = result.stdout.strip().split('\n')[0]

                    # Get version
                    version_result = subprocess.run(
                        [python_path, "--version"],
                        capture_output=True,
                        text=True,
                        timeout=10
                    )

                    if version_result.returncode == 0:
                        version = version_result.stdout.strip().replace(
                            "Python ", ""
                        )

                        env = PythonEnvironment(
                            id=str(uuid.uuid4()),
                            name=f"Python {version} (PATH)",
                            python_path=python_path,
                            version=version,
                            is_virtual=False,
                            virtual_env_path=None,
                            packages=[],
                            is_active=False,
                            last_verified="",
                            health_status="unknown"
                        )
                        installations.append(env)

            except Exception as e:
                self.logger.debug(f"Could not find {python_name}: {e}")

        return installations

    def _discover_conda_environments(self) -> List[PythonEnvironment]:
        """Discover Conda environments."""
        installations = []

        try:
            # Try to find conda
            conda_cmd = "conda"
            if platform.system() == "Windows":
                # Try common conda locations
                conda_paths = [
                    os.path.expanduser("~/anaconda3/Scripts/conda.exe"),
                    os.path.expanduser("~/miniconda3/Scripts/conda.exe"),
                    "C:\\ProgramData\\Anaconda3\\Scripts\\conda.exe",
                    "C:\\ProgramData\\Miniconda3\\Scripts\\conda.exe"
                ]

                for path in conda_paths:
                    if os.path.exists(path):
                        conda_cmd = path
                        break

            # Get conda environments
            result = subprocess.run(
                [conda_cmd, "env", "list", "--json"],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                env_data = json.loads(result.stdout)

                for env_path in env_data.get("envs", []):
                    python_exe = ("python.exe" if platform.system() ==
                                  "Windows" else "python")
                    scripts_dir = ("Scripts" if platform.system() ==
                                   "Windows" else "bin")
                    python_path = os.path.join(
                        env_path, scripts_dir, python_exe
                    )

                    if os.path.exists(python_path):
                        env_name = os.path.basename(env_path)

                        # Get Python version
                        try:
                            version_result = subprocess.run(
                                [python_path, "--version"],
                                capture_output=True,
                                text=True,
                                timeout=10
                            )
                            version = (version_result.stdout.strip().replace(
                                "Python ",
                                 "") if version_result.returncode == 0
                                else "unknown")
                        except Exception:
                            version = "unknown"

                        env = PythonEnvironment(
                            id=str(uuid.uuid4()),
                            name=f"Conda: {env_name}",
                            python_path=python_path,
                            version=version,
                            is_virtual=True,
                            virtual_env_path=env_path,
                            packages=[],
                            is_active=False,
                            last_verified="",
                            health_status="unknown"
                        )
                        installations.append(env)

        except Exception as e:
            self.logger.debug(f"Could not discover conda environments: {e}")

        return installations

    def _discover_virtual_environments(self) -> List[PythonEnvironment]:
        """Discover virtual environments."""
        installations = []

        # Common venv locations
        search_paths = [
            os.path.expanduser("~/.virtualenvs"),
            os.path.expanduser("~/venv"),
            os.path.expanduser("~/virtualenvs"),
            os.path.join(os.getcwd(), "venv"),
            os.path.join(os.getcwd(), ".venv")
        ]

        for search_path in search_paths:
            if os.path.exists(search_path):
                try:
                    for item in os.listdir(search_path):
                        item_path = os.path.join(search_path, item)
                        if os.path.isdir(item_path):
                            python_exe = ("python.exe" if platform.system() ==
                                          "Windows" else "python")
                            scripts_dir = ("Scripts" if platform.system() ==
                                           "Windows" else "bin")
                            python_path = os.path.join(
                                item_path, scripts_dir, python_exe
                            )

                            if os.path.exists(python_path):
                                # Get Python version
                                try:
                                    version_result = subprocess.run(
                                        [python_path, "--version"],
                                        capture_output=True,
                                        text=True,
                                        timeout=10
                                    )
                                    version = (version_result.stdout.strip()
                                               .replace("Python ", "")
                                               if version_result.returncode ==
                                                0
                                               else "unknown")
                                except Exception:
                                    version = "unknown"

                                env = PythonEnvironment(
                                    id=str(uuid.uuid4()),
                                    name=f"VirtualEnv: {item}",
                                    python_path=python_path,
                                    version=version,
                                    is_virtual=True,
                                    virtual_env_path=item_path,
                                    packages=[],
                                    is_active=False,
                                    last_verified="",
                                    health_status="unknown"
                                )
                                installations.append(env)

                except Exception as e:
                    self.logger.debug(f"Error scanning {search_path}: {e}")

        return installations

    def _deduplicate_installations(
        self, installations: List[PythonEnvironment]
    ) -> List[PythonEnvironment]:
        """Remove duplicate Python installations."""
        seen_paths = set()
        unique_installations = []

        for env in installations:
            # Normalize path for comparison
            normalized_path = os.path.normpath(
                os.path.abspath(env.python_path)
            ).lower()

            if normalized_path not in seen_paths:
                seen_paths.add(normalized_path)
                unique_installations.append(env)

        return unique_installations

    def _verify_python_installation(self, python_path: str) -> bool:
        """Verify that a Python installation is working."""
        try:
            result = subprocess.run(
                [python_path, "-c", "import sys; print('OK')"],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode == 0 and "OK" in result.stdout

        except Exception as e:
            self.logger.debug(f"Verification failed for {python_path}: {e}")
            return False

    def refresh_environments(self) -> int:
        """Refresh all environments by rediscovering and verifying them."""
        self.logger.info("Refreshing Python environments...")

        # Discover all installations
        discovered = self.discover_python_installations()

        # Merge with existing environments (preserve custom settings)
        for new_env in discovered:
            # Check if we already know about this environment
            existing_env = None
            for env_id, env in self.environments.items():
                if (os.path.normpath(env.python_path).lower() ==
                        os.path.normpath(new_env.python_path).lower()):
                    existing_env = env
                    break

            if existing_env:
                # Update existing environment
                existing_env.version = new_env.version
                existing_env.health_status = new_env.health_status
                existing_env.last_verified = new_env.last_verified
            else:
                # Add new environment
                self.environments[new_env.id] = new_env

        # Mark missing environments as unhealthy
        for env in self.environments.values():
            if not self._verify_python_installation(env.python_path):
                env.health_status = "missing"

        # Save updated environments
        self._save_environments()

        healthy_count = sum(
            1 for env in self.environments.values()
            if env.health_status == "healthy"
        )
        self.logger.info(
            f"Refresh complete: {healthy_count}/{len(self.environments)} "
            f"environments healthy"
        )

        return healthy_count

    def set_active_environment(self, env_id: str) -> bool:
        """Set the active Python environment."""
        if env_id not in self.environments:
            self.logger.error(f"Environment {env_id} not found")
            return False

        env = self.environments[env_id]

        # Verify environment is healthy
        if not self._verify_python_installation(env.python_path):
            self.logger.error(f"Environment {env.name} is not healthy")
            return False

        # Deactivate current environment
        if self.active_environment:
            self.active_environment.is_active = False

        # Activate new environment
        env.is_active = True
        self.active_environment = env

        self.logger.info(f"Activated environment: {env.name}")
        self._save_environments()

        return True

    def get_active_environment(self) -> Optional[PythonEnvironment]:
        """Get the currently active Python environment."""
        return self.active_environment

    def list_environments(self) -> List[PythonEnvironment]:
        """List all available Python environments."""
        return list(self.environments.values())

    def health_check(self) -> Dict[str, Any]:
        """Perform a comprehensive health check of all environments."""
        health_report = {
            "timestamp": datetime.now().isoformat(),
            "total_environments": len(self.environments),
            "healthy_environments": 0,
            "missing_environments": 0,
            "broken_environments": 0,
            "active_environment": None,
            "recommendations": []
        }

        for env in self.environments.values():
            if self._verify_python_installation(env.python_path):
                env.health_status = "healthy"
                env.last_verified = datetime.now().isoformat()
                health_report["healthy_environments"] += 1
            else:
                if os.path.exists(env.python_path):
                    env.health_status = "broken"
                    health_report["broken_environments"] += 1
                else:
                    env.health_status = "missing"
                    health_report["missing_environments"] += 1

        # Active environment
        if self.active_environment:
            health_report["active_environment"] = {
                "name": self.active_environment.name,
                "path": self.active_environment.python_path,
                "health": self.active_environment.health_status
            }

        # Recommendations
        if health_report["healthy_environments"] == 0:
            health_report["recommendations"].append(
                "No healthy Python environments found. "
                "Run discovery or install Python."
            )

        if not self.active_environment:
            health_report["recommendations"].append(
                "No active Python environment set. Set an active environment."
            )

        if health_report["missing_environments"] > 0:
            health_report["recommendations"].append(
                f"{health_report['missing_environments']} environments are "
                f"missing. Consider cleanup."
            )

        self._save_environments()
        return health_report


# Global instance for AIOS
_global_env_manager = None


def get_environment_manager() -> RobustPythonEnvironmentManager:
    """Get the global environment manager instance."""
    global _global_env_manager
    if _global_env_manager is None:
        _global_env_manager = RobustPythonEnvironmentManager()
    return _global_env_manager


def initialize_python_environment_for_aios():
    """Initialize Python environment management for AIOS."""
    manager = get_environment_manager()

    # Refresh environments
    healthy_count = manager.refresh_environments()

    # Set active environment if none set
    if not manager.get_active_environment():
        environments = manager.list_environments()
        healthy_envs = [
            env for env in environments if env.health_status == "healthy"
        ]

        if healthy_envs:
            # Prefer the first virtual environment, or the first available
            preferred_env = None
            for env in healthy_envs:
                if env.is_virtual:
                    preferred_env = env
                    break

            if not preferred_env:
                preferred_env = healthy_envs[0]

            manager.set_active_environment(preferred_env.id)
            print(f"Set active Python environment: {preferred_env.name}")
        else:
            print("No healthy Python environments found!")

    return manager


if __name__ == "__main__":
    # Demo/test the environment manager
    print("AIOS Robust Python Environment Manager")
    print("=" * 50)

    manager = initialize_python_environment_for_aios()

    # Health check
    health = manager.health_check()
    print(f"\nHealth Check Results:")
    print(f"Total environments: {health['total_environments']}")
    print(f"Healthy: {health['healthy_environments']}")
    print(f"Missing: {health['missing_environments']}")
    print(f"Broken: {health['broken_environments']}")

    if health['active_environment']:
        print(f"Active: {health['active_environment']['name']}")

    # List environments
    print(f"\nAvailable Environments:")
    for env in manager.list_environments():
        status = "✓" if env.health_status == "healthy" else "✗"
        active = " (ACTIVE)" if env.is_active else ""
        print(f"  {status} {env.name}{active}")
        print(f"    Path: {env.python_path}")
        print(f"    Version: {env.version}")
        print()
