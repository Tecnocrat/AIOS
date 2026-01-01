#!/usr/bin/env python3
"""
AIOS Python Environment Consistency Validator
Phase 9.2: System Optimization and Debugging Pass

Validates Python environment consistency across AIOS components:
- Dependency installation verification
- Import path validation
- Environment configuration consistency
- Cross-component integration testing

AINLP Integration: runtime/tools/python_environment_validator.py
Purpose: Ensure consistent Python environments across AIOS biological architecture
"""

import sys
import os
import importlib
from pathlib import Path
from typing import Dict, List, Any


class PythonEnvironmentValidator:
    """
    Validates Python environment consistency across AIOS components
    Ensures biological architecture coherence in dependency management
    """

    def __init__(self, workspace_root: str):
        self.workspace_root = Path(workspace_root)
        self.issues: List[str] = []
        self.warnings: List[str] = []

    def validate_environment_consistency(self) -> Dict[str, Any]:
        """
        Comprehensive environment consistency validation
        Returns validation results with issues and recommendations
        """
        results = {
            "python_version": self._check_python_version(),
            "dependencies": self._check_dependencies(),
            "import_paths": self._check_import_paths(),
            "component_integrations": self._check_component_integrations(),
            "environment_config": self._check_environment_config(),
            "issues": self.issues,
            "warnings": self.warnings,
            "recommendations": [],
        }

        # Generate recommendations based on findings
        results["recommendations"] = self._generate_recommendations(results)

        return results

    def _check_python_version(self) -> Dict[str, Any]:
        """Check Python version consistency"""
        version = sys.version_info
        version_str = f"{version.major}.{version.minor}.{version.micro}"

        # Check against intended versions
        intended_versions = ["3.11", "3.12"]  # From environment files

        result = {
            "current_version": version_str,
            "executable": sys.executable,
            "intended_versions": intended_versions,
            "consistent": any(version_str.startswith(v) for v in intended_versions),
        }

        if not result["consistent"]:
            self.issues.append(
                f"Python version {version_str} not in intended range "
                f"{intended_versions}"
            )

        return result

    def _check_dependencies(self) -> Dict[str, Any]:
        """Check core dependency installation"""
        core_deps = [
            "torch",
            "transformers",
            "fastapi",
            "uvicorn",
            "numpy",
            "pandas",
            "psutil",
            "rich",
            "pydantic",
        ]

        installed = {}
        missing = []

        for dep in core_deps:
            try:
                importlib.import_module(dep)
                installed[dep] = True
            except ImportError:
                installed[dep] = False
                missing.append(dep)

        if missing:
            self.issues.append(f"Missing core dependencies: {missing}")

        return {
            "core_dependencies": installed,
            "missing": missing,
            "total_checked": len(core_deps),
        }

    def _check_import_paths(self) -> Dict[str, Any]:
        """Check Python path configuration"""
        aios_paths = [p for p in sys.path if "AIOS" in str(p) or "aios" in str(p)]

        # Expected paths
        expected_paths = [
            str(self.workspace_root),
            str(self.workspace_root / "ai"),
            str(self.workspace_root / "runtime"),
            str(self.workspace_root / "core"),
        ]

        missing_paths = [p for p in expected_paths if p not in sys.path]

        if missing_paths:
            self.warnings.append(f"Missing AIOS paths in sys.path: {missing_paths}")

        return {
            "current_aios_paths": aios_paths,
            "expected_paths": expected_paths,
            "missing_paths": missing_paths,
            "path_consistent": len(missing_paths) == 0,
        }

    def _check_component_integrations(self) -> Dict[str, Any]:
        """Check cross-component import integration"""
        components = {
            "interface_bridge": ("ai.nucleus.interface_bridge", "AIOSInterfaceBridge"),
            "dendritic_supervisor": (
                "runtime.tools.dendritic_supervisor",
                "DendriticSupervisor",
            ),
            "biological_monitor": (
                "runtime.tools.biological_architecture_monitor",
                "AIOSArchitectureMonitor",
            ),
            "visual_bridge": (
                "runtime.tools." "enhanced_visual_intelligence_bridge",
                "EnhancedVisualIntelligenceBridge",
            ),
        }

        results = {}

        for name, (module_path, class_name) in components.items():
            try:
                module = importlib.import_module(module_path)
                cls = getattr(module, class_name)
                results[name] = {"status": "success", "class": cls.__name__}
            except Exception as e:
                results[name] = {"status": "failed", "error": str(e)}
                self.issues.append(f"Component {name} import failed: {e}")

        return results

    def _check_environment_config(self) -> Dict[str, Any]:
        """Check environment configuration files"""
        config_files = {
            "root_requirements": self.workspace_root / "requirements.txt",
            "ai_base_env": (
                self.workspace_root
                / "ai"
                / "infrastructure"
                / "env"
                / "environment.base.yml"
            ),
            "ai_ai_env": (
                self.workspace_root
                / "ai"
                / "infrastructure"
                / "env"
                / "environment.ai.yml"
            ),
            "pyproject_toml": self.workspace_root / "pyproject.toml",
        }

        results = {}
        for name, path in config_files.items():
            results[name] = {"exists": path.exists(), "path": str(path)}

            if not path.exists():
                self.warnings.append(
                    f"Environment config file missing: {name} at {path}"
                )

        return results

    def _generate_recommendations(self, results: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on validation results"""
        recommendations = []

        if not results["python_version"]["consistent"]:
            recommendations.append(
                f"Consider using Python "
                f"{results['python_version']['intended_versions']}"
            )

        if results["dependencies"]["missing"]:
            recommendations.append(
                f"Install missing dependencies: pip install "
                f"{' '.join(results['dependencies']['missing'])}"
            )

        if results["import_paths"]["missing_paths"]:
            recommendations.append(
                "Add missing AIOS paths to PYTHONPATH or use "
                "development environment setup"
            )

        if results["environment_config"]["ai_base_env"]["exists"]:
            recommendations.append(
                "Use conda environments: conda env create -f "
                "ai/infrastructure/env/environment.base.yml"
            )

        return recommendations


def main():
    """Main validation execution"""
    workspace_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    validator = PythonEnvironmentValidator(workspace_root)
    results = validator.validate_environment_consistency()

    # Print results
    print("🔍 AIOS Python Environment Consistency Validation")
    print("=" * 50)

    print(f"Python Version: {results['python_version']['current_version']}")
    print(
        f"Dependencies: {results['dependencies']['total_checked']} checked, "
        f"{len(results['dependencies']['missing'])} missing"
    )

    print(f"Import Paths: " f"{len(results['import_paths']['missing_paths'])} missing")
    working_count = len(
        [
            r
            for r in results["component_integrations"].values()
            if r["status"] == "success"
        ]
    )
    total_count = len(results["component_integrations"])
    print(f"Component Integrations: {working_count}/{total_count} working")

    if results["issues"]:
        print("\n❌ Issues Found:")
        for issue in results["issues"]:
            print(f"  • {issue}")

    if results["warnings"]:
        print("\n⚠️  Warnings:")
        for warning in results["warnings"]:
            print(f"  • {warning}")

    if results["recommendations"]:
        print("\n💡 Recommendations:")
        for rec in results["recommendations"]:
            print(f"  • {rec}")

    # Return exit code based on issues
    return len(results["issues"])


if __name__ == "__main__":
    sys.exit(main())
