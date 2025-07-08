#!/usr/bin/env python3
"""
AIOS Environment Integration System
Integrates Python environment management with AINLP and UI components
"""

import json
import os
import subprocess
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional

# Import the clean environment manager
try:
    from python_environment_manager_clean import PythonEnvironmentManager
except ImportError:
    # Fallback if running from different directory
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from python_environment_manager_clean import PythonEnvironmentManager


class AIOSEnvironmentIntegration:
    """Integration layer between AIOS components and Python environment"""

    def __init__(self, aios_root: str = None):
        self.manager = PythonEnvironmentManager(aios_root)
        self.integration_log = []

    def initialize_environment(self) -> Dict[str, Any]:
        """Initialize and validate AIOS Python environment"""
        result = {
            "success": False,
            "environment_info": None,
            "issues": [],
            "actions_taken": [],
            "recommendations": []
        }

        try:
            print("🚀 Initializing AIOS Python Environment...")

            # Run diagnostics first
            diagnostics = self.manager.diagnose_issues()
            result["environment_info"] = diagnostics

            # Auto-heal if needed
            if diagnostics["aios_compatibility"] != "compatible":
                print("🔧 Environment needs setup - running auto-heal...")
                result["actions_taken"].append("auto_heal_initiated")

                if self.manager.auto_heal_environment():
                    result["actions_taken"].append("auto_heal_successful")
                    result["success"] = True

                    # Re-run diagnostics to confirm
                    updated_diagnostics = self.manager.diagnose_issues()
                    result["environment_info"] = updated_diagnostics
                else:
                    result["actions_taken"].append("auto_heal_failed")
                    result["issues"].append("Failed to configure Python environment")
                    result["recommendations"].append(
                        "Manual Python installation may be required")
            else:
                print("✅ Environment already compatible")
                result["success"] = True
                result["actions_taken"].append("no_action_needed")

            # Log the initialization
            self._log_integration_event("environment_initialization", result)

        except Exception as e:
            result["issues"].append(f"Environment initialization error: {e}")
            print(f"❌ Environment initialization failed: {e}")

        return result

    def get_python_command_for_context(self, context: str = "default") -> str:
        """Get appropriate Python command for different contexts"""
        try:
            base_command = self.manager.get_environment_command_prefix()

            # Context-specific modifications
            if context == "terminal":
                return base_command
            elif context == "vscode":
                # Ensure paths are properly escaped for VS Code
                return base_command.replace("\\", "\\\\")
            elif context == "ainlp":
                # AINLP compiler context
                return base_command
            elif context == "ui":
                # C# UI subprocess context
                return base_command
            else:
                return base_command

        except Exception as e:
            print(f"Error getting Python command: {e}")
            return "python"  # Fallback

    def validate_environment_for_component(self, component: str) -> Dict[str, Any]:
        """Validate environment for specific AIOS component"""
        validation = {
            "component": component,
            "valid": False,
            "issues": [],
            "requirements_met": False,
            "python_path": None,
            "recommendations": []
        }

        try:
            # Get current environment info
            config = self.manager.load_environment_config()

            if not config or "selected_environment" not in config:
                validation["issues"].append("No environment configuration found")
                validation["recommendations"].append("Run environment initialization")
                return validation

            env_info = config["selected_environment"]
            python_path = env_info["executable_path"]
            validation["python_path"] = python_path

            # Check if Python executable exists
            if not os.path.exists(python_path):
                validation["issues"].append("Configured Python executable not found")
                validation["recommendations"].append("Re-run environment setup")
                return validation

            # Component-specific validation
            if component == "ai_core":
                # Check AI/ML packages
                required_packages = ["numpy", "scipy", "tensorflow", "torch"]
                missing = self._check_missing_packages(python_path, required_packages)
                if missing:
                    validation["issues"].append(f"Missing AI packages: {', '.join(missing)}")
                    validation["recommendations"].append(f"Install: pip install {' '.join(missing)}")
                else:
                    validation["requirements_met"] = True

            elif component == "web_interface":
                # Check web packages
                required_packages = ["fastapi", "uvicorn", "websockets", "aiohttp"]
                missing = self._check_missing_packages(python_path, required_packages)
                if missing:
                    validation["issues"].append(f"Missing web packages: {', '.join(missing)}")
                    validation["recommendations"].append(f"Install: pip install {' '.join(missing)}")
                else:
                    validation["requirements_met"] = True

            elif component == "testing":
                # Check testing packages
                required_packages = ["pytest", "pytest-asyncio"]
                missing = self._check_missing_packages(python_path, required_packages)
                if missing:
                    validation["issues"].append(f"Missing test packages: {', '.join(missing)}")
                    validation["recommendations"].append(f"Install: pip install {' '.join(missing)}")
                else:
                    validation["requirements_met"] = True

            # Overall validation
            validation["valid"] = len(validation["issues"]) == 0

        except Exception as e:
            validation["issues"].append(f"Validation error: {e}")

        return validation

    def _check_missing_packages(self, python_path: str, required_packages: List[str]) -> List[str]:
        """Check which packages are missing from the environment"""
        missing = []

        try:
            # Get installed packages
            cmd = [python_path, "-m", "pip", "list", "--format=freeze"]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

            if result.returncode == 0:
                installed = [line.split('==')[0].lower() for line in result.stdout.split('\n') if '==' in line]
                missing = [pkg for pkg in required_packages if pkg.lower() not in installed]
            else:
                # If pip list fails, assume all are missing
                missing = required_packages

        except Exception:
            # If check fails, assume all are missing
            missing = required_packages

        return missing

    def create_environment_script(self, target_dir: str = None) -> str:
        """Create a script to set up the Python environment"""
        if target_dir is None:
            target_dir = os.path.join(self.manager.aios_root, "scripts")

        os.makedirs(target_dir, exist_ok=True)
        script_path = os.path.join(target_dir, "setup_python_environment.py")

        script_content = f'''#!/usr/bin/env python3
"""
AIOS Python Environment Setup Script
Auto-generated by AIOS Environment Integration System
Generated: {datetime.now()}
"""

import sys
import os

# Add AIOS paths
sys.path.insert(0, r"{self.manager.aios_root}")
sys.path.insert(0, r"{os.path.dirname(os.path.abspath(__file__))}")

from ai.src.core.integration.environment_integration import AIOSEnvironmentIntegration

def main():
    print("🚀 AIOS Python Environment Setup")
    print("=" * 50)

    integration = AIOSEnvironmentIntegration()
    result = integration.initialize_environment()

    if result["success"]:
        print("✅ Environment setup completed successfully!")

        # Show environment info
        env_info = result["environment_info"]
        if env_info and "current_environment" in env_info:
            current = env_info["current_environment"]
            print(f"\\n📋 Environment Information:")
            print(f"   Python Path: {{current['executable_path']}}")
            print(f"   Version: {{current['version']}}")
            print(f"   Type: {{current['environment_type']}}")
            print(f"   Health: {{current['health_status']}}")

        # Show Python command
        python_cmd = integration.get_python_command_for_context("terminal")
        print(f"\\n🔧 Use this Python command: {{python_cmd}}")

    else:
        print("❌ Environment setup failed!")
        for issue in result["issues"]:
            print(f"   Issue: {{issue}}")
        for rec in result["recommendations"]:
            print(f"   Recommendation: {{rec}}")

        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
'''

        try:
            with open(script_path, 'w') as f:
                f.write(script_content)
            print(f"✅ Environment setup script created: {script_path}")
            return script_path
        except Exception as e:
            print(f"❌ Failed to create setup script: {e}")
            return ""

    def generate_vscode_settings(self) -> Dict[str, Any]:
        """Generate VS Code settings for Python environment"""
        settings = {}

        try:
            config = self.manager.load_environment_config()

            if config and "selected_environment" in config:
                python_path = config["selected_environment"]["executable_path"]

                # Convert Windows path for VS Code
                if os.name == 'nt':
                    python_path = python_path.replace("\\", "/")

                settings = {
                    "python.pythonPath": python_path,
                    "python.defaultInterpreterPath": python_path,
                    "python.terminal.activateEnvironment": True,
                    "python.analysis.autoImportCompletions": True,
                    "python.analysis.autoSearchPaths": True,
                    "python.analysis.extraPaths": [
                        "${workspaceFolder}/ai/src",
                        "${workspaceFolder}/ai/src/core",
                        "${workspaceFolder}/ai/src/core/integration"
                    ],
                    "python.testing.pytestEnabled": True,
                    "python.testing.unittestEnabled": False,
                    "python.testing.pytestArgs": [
                        "ai/src/core/integration"
                    ],
                    "terminal.integrated.env.windows": {
                        "PYTHONPATH": "${workspaceFolder}/ai/src;${workspaceFolder}/ai/src/core;${workspaceFolder}/ai/src/core/integration"
                    }
                }

        except Exception as e:
            print(f"Error generating VS Code settings: {e}")

        return settings

    def update_vscode_settings(self) -> bool:
        """Update VS Code workspace settings with Python configuration"""
        try:
            workspace_dir = self.manager.aios_root
            vscode_dir = os.path.join(workspace_dir, ".vscode")
            settings_file = os.path.join(vscode_dir, "settings.json")

            # Create .vscode directory if it doesn't exist
            os.makedirs(vscode_dir, exist_ok=True)

            # Load existing settings
            existing_settings = {}
            if os.path.exists(settings_file):
                try:
                    with open(settings_file, 'r') as f:
                        existing_settings = json.load(f)
                except Exception:
                    pass

            # Generate new Python settings
            python_settings = self.generate_vscode_settings()

            # Merge settings
            existing_settings.update(python_settings)

            # Save settings
            with open(settings_file, 'w') as f:
                json.dump(existing_settings, f, indent=2)

            print(f"✅ VS Code settings updated: {settings_file}")
            return True

        except Exception as e:
            print(f"❌ Failed to update VS Code settings: {e}")
            return False

    def _log_integration_event(self, event_type: str, data: Any):
        """Log integration events for debugging"""
        log_entry = {
            "timestamp": str(datetime.now()),
            "event_type": event_type,
            "data": data
        }

        self.integration_log.append(log_entry)

        # Keep only last 100 entries
        if len(self.integration_log) > 100:
            self.integration_log = self.integration_log[-100:]

    def get_integration_status(self) -> Dict[str, Any]:
        """Get comprehensive integration status"""
        status = {
            "environment_ready": False,
            "components_validated": {},
            "python_command": None,
            "issues": [],
            "last_update": None
        }

        try:
            # Check environment
            config = self.manager.load_environment_config()
            if config and "selected_environment" in config:
                status["environment_ready"] = True
                status["python_command"] = self.get_python_command_for_context()
                status["last_update"] = config["selected_environment"].get("configured_at")

            # Validate components
            components = ["ai_core", "web_interface", "testing"]
            for component in components:
                validation = self.validate_environment_for_component(component)
                status["components_validated"][component] = validation
                if not validation["valid"]:
                    status["issues"].extend(validation["issues"])

        except Exception as e:
            status["issues"].append(f"Status check error: {e}")

        return status


def main():
    """Test the integration system"""
    integration = AIOSEnvironmentIntegration()

    print("🔍 AIOS Environment Integration Test")
    print("=" * 50)

    # Initialize environment
    result = integration.initialize_environment()
    print(f"\\nInitialization: {'✅ Success' if result['success'] else '❌ Failed'}")

    # Create setup script
    script_path = integration.create_environment_script()
    if script_path:
        print(f"Setup script: {script_path}")

    # Update VS Code settings
    if integration.update_vscode_settings():
        print("VS Code settings updated")

    # Show integration status
    status = integration.get_integration_status()
    print(f"\\n📋 Integration Status:")
    print(f"   Environment Ready: {'✅' if status['environment_ready'] else '❌'}")
    print(f"   Python Command: {status['python_command']}")

    for component, validation in status["components_validated"].items():
        symbol = "✅" if validation["valid"] else "❌"
        print(f"   {component}: {symbol}")

    if status["issues"]:
        print(f"\\n⚠️  Issues Found:")
        for issue in status["issues"]:
            print(f"   - {issue}")


if __name__ == "__main__":
    main()
