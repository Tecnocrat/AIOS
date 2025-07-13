"""
AIOS System Health Monitor
Comprehensive system-wide health checking and module harmonization
"""

import importlib
import importlib.util
import json
import os
import sys
import time
from typing import Any, Dict, List


class AIOSSystemHealthMonitor:
    def __init__(self):
        self.health_results = {}
        self.start_time = time.time()

    def check_python_environment(self):
        """Check Python environment and core packages"""
        print("🐍 Checking Python Environment...")

        results = {
            "python_version": sys.version,
            "python_executable": sys.executable,
            "path": sys.path[:3],  # First 3 paths
            "packages": {},
        }

        # Check critical packages
        critical_packages = [
            "requests",
            "fastapi",
            "uvicorn",
            "pydantic",
            "json",
            "time",
            "os",
            "sys",
        ]

        for package in critical_packages:
            try:
                if package in ["json", "time", "os", "sys"]:
                    # Built-in modules
                    exec(f"import {package}")
                    results["packages"][package] = "built-in"
                else:
                    # External packages
                    module = importlib.import_module(package)
                    version = getattr(module, "__version__", "unknown")
                    results["packages"][package] = version
                print(f"   ✅ {package}: {results['packages'][package]}")
            except ImportError as e:
                results["packages"][package] = f"MISSING: {e}"
                print(f"   ❌ {package}: MISSING")

        self.health_results["python_environment"] = results
        return all("MISSING" not in str(v) for v in results["packages"].values())

    def check_aios_structure(self):
        """Check AIOS project structure and key files"""
        print("🏗️  Checking AIOS Project Structure...")

        # Determine if we're running from root or tests/ directory
        if os.path.basename(os.getcwd()) == "tests":
            root_prefix = "../"
            tests_prefix = "./"
        else:
            root_prefix = ""
            tests_prefix = "tests/"

        expected_structure = {
            f"{root_prefix}ai/": ["aios_vscode_integration_server.py"],
            f"{root_prefix}vscode-extension/": ["package.json", "src/"],
            f"{root_prefix}vscode-extension/src/": [
                "aiosBridge.ts",
                "contextManager.ts",
                "extension.ts",
            ],
            f"{tests_prefix}": ["test_aios_integration.py"],
            f"{root_prefix}docs/": ["AIOS/PATH_1_TESTING_GUIDE.md"],
            f"{root_prefix}config/": ["system.json"],
            f"{root_prefix}core/": ["CMakeLists.txt", "src/", "include/"],
            f"{root_prefix}interface/": ["AIOS.sln"],
        }

        results = {}
        all_good = True

        for directory, files in expected_structure.items():
            dir_path = os.path.join(".", directory)
            results[directory] = {"exists": os.path.exists(dir_path), "files": {}}

            if results[directory]["exists"]:
                print(f"   ✅ {directory}: EXISTS")
                for file in files:
                    file_path = os.path.join(dir_path, file)
                    file_exists = os.path.exists(file_path)
                    results[directory]["files"][file] = file_exists
                    if file_exists:
                        print(f"      ✅ {file}")
                    else:
                        print(f"      ❌ {file}: MISSING")
                        all_good = False
            else:
                print(f"   ❌ {directory}: MISSING")
                all_good = False

        self.health_results["project_structure"] = results
        return all_good

    def check_vscode_extension(self):
        """Check VSCode extension configuration and build"""
        print("📦 Checking VSCode Extension...")

        extension_dir = "vscode-extension"
        results = {
            "package_json": False,
            "typescript_compiled": False,
            "dependencies": {},
        }

        # Check package.json
        package_json_path = os.path.join(extension_dir, "package.json")
        if os.path.exists(package_json_path):
            results["package_json"] = True
            print("   ✅ package.json: EXISTS")

            try:
                with open(package_json_path, "r") as f:
                    package_data = json.load(f)
                    results["dependencies"] = package_data.get("dependencies", {})
                    print(
                        f"   📋 Dependencies: {len(results['dependencies'])} packages"
                    )
            except Exception as e:
                print(f"   ⚠️  Error reading package.json: {e}")
        else:
            print("   ❌ package.json: MISSING")

        # Check compiled output
        dist_dir = os.path.join(extension_dir, "dist")
        out_dir = os.path.join(extension_dir, "out")
        if os.path.exists(dist_dir) or os.path.exists(out_dir):
            results["typescript_compiled"] = True
            print("   ✅ TypeScript compiled: EXISTS")
        else:
            print("   ⚠️  TypeScript compiled: NOT FOUND")

        self.health_results["vscode_extension"] = results
        return results["package_json"]  # Minimum requirement

    def check_aios_modules(self):
        """Check AIOS AI modules connectivity"""
        print(
            "🧠 Checking AIOS AI Modules..."
        )  # Add ai directory to Python path (adjust based on current directory)
        if os.path.basename(os.getcwd()) == "tests":
            ai_dir = os.path.join("..", "ai")
            ai_src_dir = os.path.join("..", "ai", "src", "core")
        else:
            ai_dir = os.path.join(".", "ai")
            ai_src_dir = os.path.join(".", "ai", "src", "core")

        if ai_dir not in sys.path:
            sys.path.insert(0, ai_dir)

        if ai_src_dir not in sys.path:
            sys.path.insert(0, ai_src_dir)

        modules = ["nlp", "prediction", "automation", "learning", "integration"]
        results = {}

        for module_name in modules:
            try:
                # Try to import the module
                module_path = os.path.join(ai_src_dir, module_name, "__init__.py")
                if os.path.exists(module_path):
                    spec = importlib.util.spec_from_file_location(
                        module_name, module_path
                    )
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    results[module_name] = "importable"
                    print(f"   ✅ {module_name}: IMPORTABLE")
                else:
                    results[module_name] = "file_missing"
                    print(f"   ❌ {module_name}: FILE MISSING")
            except Exception as e:
                results[module_name] = f"error: {str(e)[:50]}"
                print(f"   ⚠️  {module_name}: ERROR - {str(e)[:50]}")

        self.health_results["aios_modules"] = results
        return all("importable" in str(v) for v in results.values())

    def check_configuration_files(self):
        """Check AIOS configuration files"""
        print("⚙️  Checking Configuration Files...")

        config_files = {
            "config/system.json": "required",
            "config/ai-models.json": "optional",
            "config/ui-themes.json": "optional",
            "AIOS_PROJECT_CONTEXT.md": "required",
            "docs/AIOS/PATH_1_TESTING_GUIDE.md": "required",
        }

        results = {}
        required_missing = 0

        for file_path, importance in config_files.items():
            exists = os.path.exists(file_path)
            results[file_path] = {"exists": exists, "importance": importance}

            if exists:
                print(f"   ✅ {file_path}: EXISTS")
            else:
                if importance == "required":
                    print(f"   ❌ {file_path}: MISSING (REQUIRED)")
                    required_missing += 1
                else:
                    print(f"   ⚠️  {file_path}: MISSING (optional)")

        self.health_results["configuration_files"] = results
        return required_missing == 0

    def run_comprehensive_health_check(self):
        """Run complete system health check"""
        print("🏥 AIOS System Health Check - Comprehensive Analysis")
        print("=" * 60)

        checks = [
            ("Python Environment", self.check_python_environment),
            ("Project Structure", self.check_aios_structure),
            ("VSCode Extension", self.check_vscode_extension),
            ("AIOS AI Modules", self.check_aios_modules),
            ("Configuration Files", self.check_configuration_files),
        ]

        passed_checks = 0
        total_checks = len(checks)

        for check_name, check_func in checks:
            print(f"\n🔍 {check_name}")
            print("-" * 30)
            try:
                if check_func():
                    passed_checks += 1
                    print(f"   🎯 {check_name}: PASSED")
                else:
                    print(f"   ⚠️  {check_name}: ISSUES FOUND")
            except Exception as e:
                print(f"   ❌ {check_name}: ERROR - {e}")

        # Summary
        total_time = time.time() - self.start_time
        print("\n" + "=" * 60)
        print("🎯 SYSTEM HEALTH SUMMARY")
        print("=" * 60)
        print(f"✅ Checks Passed: {passed_checks}/{total_checks}")
        print(f"⏱️  Total Time: {total_time:.2f} seconds")

        if passed_checks == total_checks:
            print("🎉 SYSTEM HEALTH: EXCELLENT - All systems operational!")
            health_status = "EXCELLENT"
        elif passed_checks >= total_checks * 0.8:
            print("🟡 SYSTEM HEALTH: GOOD - Minor issues detected")
            health_status = "GOOD"
        elif passed_checks >= total_checks * 0.6:
            print("🟠 SYSTEM HEALTH: FAIR - Several issues need attention")
            health_status = "FAIR"
        else:
            print("🔴 SYSTEM HEALTH: POOR - Critical issues detected")
            health_status = "POOR"

        # Save health report
        health_report = {
            "timestamp": time.time(),
            "total_checks": total_checks,
            "passed_checks": passed_checks,
            "health_status": health_status,
            "detailed_results": self.health_results,
        }

        report_file = "system_health_report.json"
        with open(report_file, "w") as f:
            json.dump(health_report, f, indent=2)

        print(f"\n📄 Detailed health report saved to: {report_file}")
        return passed_checks, total_checks, health_status


def main():
    """Main health check execution"""
    monitor = AIOSSystemHealthMonitor()
    passed, total, status = monitor.run_comprehensive_health_check()

    # Return appropriate exit code
    if status in ["EXCELLENT", "GOOD"]:
        return 0
    elif status == "FAIR":
        return 1
    else:
        return 2


if __name__ == "__main__":
    exit(main())
