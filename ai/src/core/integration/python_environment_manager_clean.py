#!/usr/bin/env python3
"""
AIOS Python Environment Manager - Clean Version
Robust, OS-resilient Python interpreter and PATH management system
"""

import json
import os
import platform
import shutil
import subprocess
import sys
import urllib.request
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

try:
    import winreg
    HAS_WINREG = True
except ImportError:
    HAS_WINREG = False


@dataclass
class PythonEnvironment:
    """Python environment configuration"""
    executable_path: str
    version: str
    architecture: str
    environment_type: str
    pip_available: bool
    packages: List[str]
    health_status: str
    issues: List[str]
    recommendations: List[str]


class PythonEnvironmentManager:
    """Comprehensive Python environment management and diagnostics"""

    def __init__(self, aios_root: str = None):
        if aios_root:
            self.aios_root = aios_root
        else:
            current_file = os.path.abspath(__file__)
            self.aios_root = os.path.dirname(os.path.dirname(
                os.path.dirname(os.path.dirname(current_file))))

        config_dir = os.path.join(self.aios_root, "config")
        self.config_path = os.path.join(config_dir, "python-environment.json")
        self.backup_config_path = os.path.join(config_dir,
                                               "python-environment-backup.json")
        self.portable_python_path = os.path.join(self.aios_root, "runtime",
                                                 "python")
        self.environment_cache = {}

        # Ensure config directory exists
        os.makedirs(config_dir, exist_ok=True)

    def detect_all_python_installations(self) -> List[PythonEnvironment]:
        """Detect all available Python installations on the system"""
        installations = []

        # Check current interpreter first
        current_env = self._analyze_python_executable(sys.executable)
        if current_env:
            installations.append(current_env)

        # Check Windows Registry for installed Python versions
        if platform.system() == "Windows" and HAS_WINREG:
            installations.extend(self._detect_windows_python_installations())

        # Check common installation paths
        installations.extend(self._detect_common_path_installations())

        # Check conda environments
        installations.extend(self._detect_conda_environments())

        # Check virtual environments
        installations.extend(self._detect_virtual_environments())

        # Remove duplicates
        unique_installations = []
        seen_paths = set()
        for env in installations:
            if env.executable_path not in seen_paths:
                unique_installations.append(env)
                seen_paths.add(env.executable_path)

        return unique_installations

    def _detect_windows_python_installations(self) -> List[PythonEnvironment]:
        """Detect Python installations via Windows Registry"""
        installations = []

        if not HAS_WINREG:
            return installations

        try:
            hives = [winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER]
            for hive in hives:
                try:
                    key_path = r"SOFTWARE\Python\PythonCore"
                    python_key = winreg.OpenKey(hive, key_path)
                    num_versions = winreg.QueryInfoKey(python_key)[0]

                    for i in range(num_versions):
                        version = winreg.EnumKey(python_key, i)
                        try:
                            install_path_key = winreg.OpenKey(
                                python_key, f"{version}\\InstallPath")
                            install_path = winreg.QueryValue(install_path_key,
                                                           "")
                            executable = os.path.join(install_path,
                                                     "python.exe")

                            if os.path.exists(executable):
                                env = self._analyze_python_executable(executable)
                                if env:
                                    installations.append(env)

                        except (OSError, FileNotFoundError):
                            continue

                except (OSError, FileNotFoundError):
                    continue

        except Exception as e:
            print(f"Registry detection error: {e}")

        return installations

    def _detect_common_path_installations(self) -> List[PythonEnvironment]:
        """Check common Python installation paths"""
        installations = []

        common_patterns = [
            r"C:\Python*\python.exe",
            r"C:\Program Files\Python*\python.exe",
            r"C:\Program Files (x86)\Python*\python.exe",
            r"C:\Users\*\AppData\Local\Programs\Python\Python*\python.exe",
            r"C:\msys64\mingw64\bin\python.exe",
            r"C:\msys64\usr\bin\python.exe",
        ]

        for pattern in common_patterns:
            try:
                from glob import glob
                for path in glob(pattern):
                    if os.path.exists(path):
                        env = self._analyze_python_executable(path)
                        if env:
                            installations.append(env)
            except Exception:
                continue

        # Check PATH
        path_dirs = os.environ.get("PATH", "").split(os.pathsep)
        for path_dir in path_dirs:
            python_exe = os.path.join(path_dir, "python.exe")
            if os.path.exists(python_exe):
                env = self._analyze_python_executable(python_exe)
                if env:
                    installations.append(env)

        return installations

    def _detect_conda_environments(self) -> List[PythonEnvironment]:
        """Detect Conda/Miniconda environments"""
        installations = []

        try:
            cmd = ["conda", "info", "--envs"]
            result = subprocess.run(cmd, capture_output=True, text=True,
                                  timeout=10)
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if line.strip() and not line.startswith('#'):
                        parts = line.split()
                        if len(parts) >= 2:
                            env_path = parts[-1]
                            python_exe = os.path.join(env_path, "python.exe")
                            if os.path.exists(python_exe):
                                env = self._analyze_python_executable(python_exe)
                                if env:
                                    env.environment_type = "conda"
                                    installations.append(env)
        except Exception:
            pass

        return installations

    def _detect_virtual_environments(self) -> List[PythonEnvironment]:
        """Detect virtual environments"""
        installations = []

        venv_locations = [
            os.path.join(os.path.expanduser("~"), ".virtualenvs"),
            os.path.join(os.path.expanduser("~"), "venvs"),
            os.path.join(self.aios_root, "venv"),
            os.path.join(self.aios_root, ".venv"),
        ]

        for venv_dir in venv_locations:
            if os.path.exists(venv_dir):
                for item in os.listdir(venv_dir):
                    venv_path = os.path.join(venv_dir, item)
                    if os.path.isdir(venv_path):
                        # Windows
                        python_exe = os.path.join(venv_path, "Scripts",
                                                 "python.exe")
                        if not os.path.exists(python_exe):
                            # Unix-like
                            python_exe = os.path.join(venv_path, "bin",
                                                     "python")

                        if os.path.exists(python_exe):
                            env = self._analyze_python_executable(python_exe)
                            if env:
                                env.environment_type = "venv"
                                installations.append(env)

        return installations

    def _analyze_python_executable(self, executable_path: str
                                  ) -> Optional[PythonEnvironment]:
        """Analyze a specific Python executable"""
        try:
            if not os.path.exists(executable_path):
                return None

            # Get version info
            version_cmd = [
                executable_path, "-c",
                ("import sys; "
                 "print(f'{sys.version_info.major}.{sys.version_info.minor}."
                 "{sys.version_info.micro}'); "
                 "print(sys.platform); "
                 "print(sys.maxsize > 2**32)")
            ]

            result = subprocess.run(version_cmd, capture_output=True,
                                  text=True, timeout=10)

            if result.returncode != 0:
                return None

            lines = result.stdout.strip().split('\n')
            if len(lines) < 3:
                return None

            version = lines[0]
            platform_name = lines[1]
            is_64bit = lines[2] == "True"
            architecture = "64-bit" if is_64bit else "32-bit"

            # Check pip availability
            pip_cmd = [executable_path, "-m", "pip", "--version"]
            pip_result = subprocess.run(pip_cmd, capture_output=True,
                                      text=True, timeout=10)
            pip_available = pip_result.returncode == 0

            # Get installed packages
            packages = []
            if pip_available:
                try:
                    pkg_cmd = [executable_path, "-m", "pip", "list",
                             "--format=freeze"]
                    pkg_result = subprocess.run(pkg_cmd, capture_output=True,
                                              text=True, timeout=30)
                    if pkg_result.returncode == 0:
                        packages = [line.strip() for line in
                                  pkg_result.stdout.split('\n')
                                  if line.strip()]
                except Exception:
                    pass

            # Determine environment type
            env_type = self._determine_environment_type(executable_path)

            # Health assessment
            health_status, issues, recommendations = (
                self._assess_environment_health(
                    executable_path, version, pip_available, packages, env_type
                )
            )

            return PythonEnvironment(
                executable_path=executable_path,
                version=version,
                architecture=architecture,
                environment_type=env_type,
                pip_available=pip_available,
                packages=packages,
                health_status=health_status,
                issues=issues,
                recommendations=recommendations
            )

        except Exception as e:
            print(f"Error analyzing {executable_path}: {e}")
            return None

    def _determine_environment_type(self, executable_path: str) -> str:
        """Determine the type of Python environment"""
        path_lower = executable_path.lower()

        if "msys64" in path_lower or "mingw" in path_lower:
            return "msys2"
        elif ("conda" in path_lower or "miniconda" in path_lower or
              "anaconda" in path_lower):
            return "conda"
        elif "venv" in path_lower or ".virtualenv" in path_lower:
            return "venv"
        elif "program files" in path_lower:
            return "system"
        elif "appdata" in path_lower:
            return "user"
        else:
            return "unknown"

    def _assess_environment_health(self, executable_path: str, version: str,
                                 pip_available: bool, packages: List[str],
                                 env_type: str) -> Tuple[str, List[str],
                                                       List[str]]:
        """Assess the health of a Python environment"""
        issues = []
        recommendations = []

        # Version check
        version_parts = version.split('.')
        if len(version_parts) >= 2:
            major, minor = int(version_parts[0]), int(version_parts[1])
            if major < 3 or (major == 3 and minor < 8):
                issues.append(f"Python version {version} is outdated")
                recommendations.append("Upgrade to Python 3.8 or newer")

        # Pip availability
        if not pip_available:
            issues.append("pip package manager not available")
            recommendations.append("Install pip: python -m ensurepip --upgrade")

        # MSYS2 specific issues
        if env_type == "msys2":
            issues.append("MSYS2 Python may have package compatibility issues")
            recommendations.append(
                "Consider using standard Windows Python distribution")

        # Required packages for AIOS
        required_packages = [
            "numpy", "scipy", "matplotlib", "pandas", "scikit-learn",
            "tensorflow", "torch", "transformers", "asyncio", "websockets"
        ]

        installed_package_names = [
            pkg.split('==')[0].split('>=')[0].split('<=')[0]
            for pkg in packages
        ]

        missing_packages = [pkg for pkg in required_packages
                          if pkg not in installed_package_names]

        if missing_packages:
            missing_str = ', '.join(missing_packages)
            issues.append(f"Missing AIOS required packages: {missing_str}")
            install_str = ' '.join(missing_packages)
            recommendations.append(f"Install missing packages: "
                                 f"pip install {install_str}")

        # Health status
        if not issues:
            health_status = "excellent"
        elif len(issues) == 1 and "MSYS2" in issues[0]:
            health_status = "good"
        elif len(issues) <= 2:
            health_status = "fair"
        else:
            health_status = "poor"

        return health_status, issues, recommendations

    def get_recommended_environment(self) -> Optional[PythonEnvironment]:
        """Get the best Python environment for AIOS"""
        environments = self.detect_all_python_installations()

        if not environments:
            return None

        def score_environment(env: PythonEnvironment) -> int:
            score = 0

            # Health status
            health_scores = {"excellent": 100, "good": 80, "fair": 50,
                           "poor": 20}
            score += health_scores.get(env.health_status, 0)

            # Environment type preference
            type_scores = {"system": 20, "user": 15, "conda": 10, "venv": 8,
                         "msys2": 5, "unknown": 0}
            score += type_scores.get(env.environment_type, 0)

            # Version preference (newer is better)
            try:
                version_parts = env.version.split('.')
                major, minor = int(version_parts[0]), int(version_parts[1])
                if major == 3:
                    score += minor * 2  # Python 3.x preference
            except Exception:
                pass

            # Pip availability
            if env.pip_available:
                score += 20

            # Architecture preference
            if env.architecture == "64-bit":
                score += 10

            return score

        # Sort by score
        environments.sort(key=score_environment, reverse=True)
        return environments[0]

    def create_portable_python_environment(self) -> bool:
        """Create a portable Python environment for AIOS"""
        try:
            print("Creating portable Python environment...")

            # Create runtime directory
            os.makedirs(self.portable_python_path, exist_ok=True)

            # Download Python embeddable package
            python_version = "3.11.9"  # Stable version
            base_url = "https://www.python.org/ftp/python"
            download_url = (f"{base_url}/{python_version}/"
                          f"python-{python_version}-embed-amd64.zip")

            zip_path = os.path.join(self.portable_python_path,
                                   "python-embed.zip")

            print(f"Downloading Python {python_version}...")
            urllib.request.urlretrieve(download_url, zip_path)

            # Extract
            import zipfile
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(self.portable_python_path)

            os.remove(zip_path)

            # Configure Python paths
            version_short = python_version.replace('.', '')[:2]
            pth_file = os.path.join(self.portable_python_path,
                                   f"python{version_short}._pth")
            with open(pth_file, 'w') as f:
                f.write("python311.zip\n")
                f.write(".\n")
                f.write("Lib\n")
                f.write("Lib/site-packages\n")
                f.write("import site\n")

            # Install pip
            get_pip_url = "https://bootstrap.pypa.io/get-pip.py"
            get_pip_path = os.path.join(self.portable_python_path,
                                       "get-pip.py")
            urllib.request.urlretrieve(get_pip_url, get_pip_path)

            python_exe = os.path.join(self.portable_python_path, "python.exe")
            subprocess.run([python_exe, get_pip_path], check=True)

            os.remove(get_pip_path)

            print("Portable Python environment created successfully!")
            return True

        except Exception as e:
            print(f"Failed to create portable Python environment: {e}")
            return False

    def install_aios_requirements(self, python_executable: str) -> bool:
        """Install AIOS requirements in the specified Python environment"""
        try:
            requirements_file = os.path.join(self.aios_root, "ai",
                                           "requirements.txt")

            if not os.path.exists(requirements_file):
                print("Creating AIOS requirements.txt...")
                requirements = [
                    "numpy>=1.21.0",
                    "scipy>=1.7.0",
                    "matplotlib>=3.4.0",
                    "pandas>=1.3.0",
                    "scikit-learn>=1.0.0",
                    "tensorflow>=2.8.0",
                    "torch>=1.11.0",
                    "transformers>=4.15.0",
                    "websockets>=10.0",
                    "aiohttp>=3.8.0",
                    "fastapi>=0.75.0",
                    "uvicorn>=0.17.0",
                    "pytest>=7.0.0",
                    "pytest-asyncio>=0.18.0"
                ]

                with open(requirements_file, 'w') as f:
                    f.write('\n'.join(requirements))

            print(f"Installing AIOS requirements using {python_executable}...")
            cmd = [python_executable, "-m", "pip", "install", "-r",
                   requirements_file]
            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                print("AIOS requirements installed successfully!")
                return True
            else:
                print(f"Failed to install requirements: {result.stderr}")
                return False

        except Exception as e:
            print(f"Error installing AIOS requirements: {e}")
            return False

    def save_environment_config(self, environment: PythonEnvironment):
        """Save environment configuration for persistence"""
        config = {
            "selected_environment": {
                "executable_path": environment.executable_path,
                "version": environment.version,
                "architecture": environment.architecture,
                "environment_type": environment.environment_type,
                "health_status": environment.health_status,
                "configured_at": str(datetime.now())
            },
            "backup_environments": [
                env.__dict__ for env in
                self.detect_all_python_installations()[:5]
            ]
        }

        try:
            with open(self.config_path, 'w') as f:
                json.dump(config, f, indent=2)

            # Create backup
            shutil.copy2(self.config_path, self.backup_config_path)

            print(f"Environment configuration saved to {self.config_path}")

        except Exception as e:
            print(f"Failed to save environment config: {e}")

    def load_environment_config(self) -> Optional[Dict]:
        """Load saved environment configuration"""
        for config_file in [self.config_path, self.backup_config_path]:
            try:
                if os.path.exists(config_file):
                    with open(config_file, 'r') as f:
                        return json.load(f)
            except Exception as e:
                print(f"Failed to load config from {config_file}: {e}")
                continue
        return None

    def auto_heal_environment(self) -> bool:
        """Automatically diagnose and fix environment issues"""
        print("🔧 Starting AIOS Python environment auto-healing...")

        # Load saved config
        config = self.load_environment_config()

        # Check if saved environment still works
        if config and "selected_environment" in config:
            saved_env = config["selected_environment"]
            if os.path.exists(saved_env["executable_path"]):
                current_env = self._analyze_python_executable(
                    saved_env["executable_path"])
                if (current_env and
                    current_env.health_status in ["excellent", "good"]):
                    print(f"✅ Saved environment still healthy: "
                          f"{saved_env['executable_path']}")
                    return True

        # Find best available environment
        recommended_env = self.get_recommended_environment()

        if not recommended_env:
            print("❌ No suitable Python environment found. "
                  "Creating portable environment...")
            if self.create_portable_python_environment():
                portable_python = os.path.join(self.portable_python_path,
                                             "python.exe")
                recommended_env = self._analyze_python_executable(
                    portable_python)
            else:
                print("❌ Failed to create portable environment")
                return False

        if recommended_env:
            print(f"✅ Selected Python environment: "
                  f"{recommended_env.executable_path}")
            print(f"   Version: {recommended_env.version}")
            print(f"   Type: {recommended_env.environment_type}")
            print(f"   Health: {recommended_env.health_status}")

            # Install requirements
            if self.install_aios_requirements(recommended_env.executable_path):
                self.save_environment_config(recommended_env)
                return True
            else:
                print("❌ Failed to install AIOS requirements")
                return False

        return False

    def get_environment_command_prefix(self) -> str:
        """Get the command prefix for running Python in the current env"""
        config = self.load_environment_config()

        if config and "selected_environment" in config:
            executable = config["selected_environment"]["executable_path"]
            if os.path.exists(executable):
                return f'"{executable}"'

        # Fallback to system Python
        return "python"

    def diagnose_issues(self) -> Dict[str, Any]:
        """Comprehensive environment diagnostics"""
        print("🔍 Running AIOS Python environment diagnostics...")

        diagnostics = {
            "timestamp": str(datetime.now()),
            "platform": platform.platform(),
            "python_installations": [],
            "current_environment": None,
            "issues": [],
            "recommendations": [],
            "aios_compatibility": "unknown"
        }

        # Detect all Python installations
        environments = self.detect_all_python_installations()
        diagnostics["python_installations"] = [env.__dict__ for env in
                                              environments]

        # Current environment
        current_env = self._analyze_python_executable(sys.executable)
        if current_env:
            diagnostics["current_environment"] = current_env.__dict__

        # Overall assessment
        if not environments:
            diagnostics["issues"].append("No Python installations detected")
            diagnostics["recommendations"].append(
                "Install Python from python.org")
            diagnostics["aios_compatibility"] = "incompatible"
        else:
            recommended = self.get_recommended_environment()
            if (recommended and
                recommended.health_status in ["excellent", "good"]):
                diagnostics["aios_compatibility"] = "compatible"
            else:
                diagnostics["aios_compatibility"] = "needs_setup"
                diagnostics["recommendations"].append(
                    "Run auto-heal to configure optimal environment")

        return diagnostics


def main():
    """Main entry point for environment management"""
    import argparse

    parser = argparse.ArgumentParser(
        description="AIOS Python Environment Manager")
    parser.add_argument("--diagnose", action="store_true",
                       help="Run environment diagnostics")
    parser.add_argument("--heal", action="store_true",
                       help="Auto-heal environment issues")
    parser.add_argument("--list", action="store_true",
                       help="List all Python installations")
    parser.add_argument("--portable", action="store_true",
                       help="Create portable Python environment")

    args = parser.parse_args()

    manager = PythonEnvironmentManager()

    if args.diagnose:
        diagnostics = manager.diagnose_issues()
        print(json.dumps(diagnostics, indent=2))

    elif args.heal:
        success = manager.auto_heal_environment()
        print("✅ Environment healed successfully!" if success else
              "❌ Healing failed")

    elif args.list:
        environments = manager.detect_all_python_installations()
        for i, env in enumerate(environments):
            print(f"\n{i+1}. {env.executable_path}")
            print(f"   Version: {env.version} ({env.architecture})")
            print(f"   Type: {env.environment_type}")
            print(f"   Health: {env.health_status}")
            print(f"   Pip: {'✅' if env.pip_available else '❌'}")

    elif args.portable:
        success = manager.create_portable_python_environment()
        print("✅ Portable environment created!" if success else
              "❌ Creation failed")

    else:
        # Auto-heal by default
        success = manager.auto_heal_environment()
        if success:
            print("✅ AIOS Python environment ready!")
            prefix = manager.get_environment_command_prefix()
            print(f"Use this command prefix: {prefix}")
        else:
            print("❌ Environment setup failed")


if __name__ == "__main__":
    main()
