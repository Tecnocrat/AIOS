"""
AIOS System Health Monitor
Comprehensive system-wide health checking and module harmonization
"""

import importlib
import importlib.util
import json
import logging
import os
import sys
import time


# --- Utility Functions ---
def path_exists(path: str) -> bool:
    """Utility for checking if a path exists."""
    return os.path.exists(path)


def file_exists(path: str) -> bool:
    """Utility for checking if a file exists."""
    return os.path.isfile(path)


def dir_exists(path: str) -> bool:
    """Utility for checking if a directory exists."""
    return os.path.isdir(path)


# --- Logging Setup ---
logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
logger = logging.getLogger("AIOSHealthMonitor")


class AIOSSystemHealthMonitor:
    def __init__(self):
        self.health_results = {}
        self.start_time = time.time()
        self.checks = [
            ("Python Environment", self.check_python_environment),
            ("Project Structure", self.check_aios_structure),
            ("VSCode Extension", self.check_vscode_extension),
            ("AIOS AI Modules", self.check_aios_modules),
            ("Configuration Files", self.check_configuration_files),
        ]

    def check_python_environment(self) -> bool:
        logger.info("Checking Python Environment...")
        results = {
            "python_version": sys.version,
            "python_executable": sys.executable,
            "path": sys.path[:3],
            "packages": {},
        }
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
                    exec(f"import {package}")
                    results["packages"][package] = "built-in"
                else:
                    module = importlib.import_module(package)
                    version = getattr(module, "__version__", "unknown")
                    results["packages"][package] = version
                logger.info(f"{package}: {results['packages'][package]}")
            except ImportError as e:
                results["packages"][package] = f"MISSING: {e}"
                logger.warning(f"{package}: MISSING")
        self.health_results["python_environment"] = results
        return all("MISSING" not in str(v) for v in results["packages"].values())

    def check_aios_structure(self) -> bool:
        logger.info("Checking AIOS Project Structure...")
        cwd = os.getcwd()
        if (
            os.path.basename(cwd) == "tests"
            and os.path.basename(os.path.dirname(cwd)) == "ai"
        ):
            root_prefix = "../.."
            tests_prefix = "./"
        elif os.path.basename(cwd) == "tests":
            root_prefix = "../"
            tests_prefix = "./"
        else:
            root_prefix = ""
            tests_prefix = "ai/tests/"
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
            results[directory] = {"exists": dir_exists(dir_path), "files": {}}
            if results[directory]["exists"]:
                logger.info(f"{directory}: EXISTS")
                for file in files:
                    file_path = os.path.join(dir_path, file)
                    file_exists = path_exists(file_path)
                    results[directory]["files"][file] = file_exists
                    if file_exists:
                        logger.info(f"   {file}: EXISTS")
                    else:
                        logger.warning(f"   {file}: MISSING")
                        all_good = False
            else:
                logger.warning(f"{directory}: MISSING")
                all_good = False
        self.health_results["project_structure"] = results
        return all_good

    def check_vscode_extension(self) -> bool:
        logger.info("Checking VSCode Extension...")
        extension_dir = "vscode-extension"
        results = {
            "package_json": False,
            "typescript_compiled": False,
            "dependencies": {},
        }
        package_json_path = os.path.join(extension_dir, "package.json")
        if file_exists(package_json_path):
            results["package_json"] = True
            logger.info("package.json: EXISTS")
            try:
                with open(package_json_path, "r") as f:
                    package_data = json.load(f)
                    results["dependencies"] = package_data.get("dependencies", {})
                    logger.info(
                        f"Dependencies: {len(results['dependencies'])} packages"
                    )
            except Exception as e:
                logger.warning(f"Error reading package.json: {e}")
        else:
            logger.warning("package.json: MISSING")
        dist_dir = os.path.join(extension_dir, "dist")
        out_dir = os.path.join(extension_dir, "out")
        if dir_exists(dist_dir) or dir_exists(out_dir):
            results["typescript_compiled"] = True
            logger.info("TypeScript compiled: EXISTS")
        else:
            logger.warning("TypeScript compiled: NOT FOUND")
        self.health_results["vscode_extension"] = results
        return results["package_json"]

    def check_aios_modules(self) -> bool:
        logger.info("Checking AIOS AI Modules...")
        cwd = os.getcwd()
        if (
            os.path.basename(cwd) == "tests"
            and os.path.basename(os.path.dirname(cwd)) == "ai"
        ):
            ai_dir = os.path.join("..", "..", "ai")
            ai_src_dir = os.path.join("..", "..", "ai", "src", "core")
        elif os.path.basename(cwd) == "tests":
            ai_dir = os.path.join("..", "ai")
            ai_src_dir = os.path.join("..", "ai", "src", "core")
        else:
            ai_dir = os.path.join(".", "ai")
            ai_src_dir = os.path.join(".", "ai", "src", "core")
        if ai_dir not in sys.path:
            sys.path.insert(0, ai_dir)
        if ai_src_dir not in sys.path:
            sys.path.insert(0, ai_src_dir)
        modules = [
            "nlp",
            "prediction",
            "automation",
            "learning",
            "integration",
        ]
        results = {}
        for module_name in modules:
            try:
                module_path = os.path.join(ai_src_dir, module_name, "__init__.py")
                if file_exists(module_path):
                    spec = importlib.util.spec_from_file_location(
                        module_name, module_path
                    )
                    if spec is not None and spec.loader is not None:
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)
                        results[module_name] = "importable"
                        logger.info(f"{module_name}: IMPORTABLE")
                    else:
                        results[module_name] = "spec_error"
                        logger.warning(f"{module_name}: SPEC/LOADER ERROR")
                else:
                    results[module_name] = "file_missing"
                    logger.warning(f"{module_name}: FILE MISSING")
            except Exception as e:
                results[module_name] = f"error: {str(e)[:50]}"
                logger.warning(f"{module_name}: ERROR - {str(e)[:50]}")
        self.health_results["aios_modules"] = results
        return all("importable" in str(v) for v in results.values())

    def check_configuration_files(self) -> bool:
        logger.info("Checking Configuration Files...")
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
            exists = file_exists(file_path)
            results[file_path] = {"exists": exists, "importance": importance}
            if exists:
                logger.info(f"{file_path}: EXISTS")
            else:
                if importance == "required":
                    logger.warning(f"{file_path}: MISSING (REQUIRED)")
                    required_missing += 1
                else:
                    logger.warning(f"{file_path}: MISSING (optional)")
        self.health_results["configuration_files"] = results
        return required_missing == 0

    def run_comprehensive_health_check(self) -> tuple[int, int, str]:
        logger.info("AIOS System Health Check - Comprehensive Analysis")
        logger.info("=" * 60)
        passed_checks = 0
        total_checks = len(self.checks)
        for check_name, check_func in self.checks:
            logger.info(f"\n{check_name}")
            logger.info("-" * 30)
            try:
                if check_func():
                    passed_checks += 1
                    logger.info(f"{check_name}: PASSED")
                else:
                    logger.warning(f"{check_name}: ISSUES FOUND")
            except Exception as e:
                logger.error(f"{check_name}: ERROR - {e}")
        total_time = time.time() - self.start_time
        logger.info("\n" + "=" * 60)
        logger.info("SYSTEM HEALTH SUMMARY")
        logger.info("=" * 60)
        logger.info(f"Checks Passed: {passed_checks}/{total_checks}")
        logger.info(f"Total Time: {total_time:.2f} seconds")
        if passed_checks == total_checks:
            logger.info("SYSTEM HEALTH: EXCELLENT - All systems operational!")
            health_status = "EXCELLENT"
        elif passed_checks >= total_checks * 0.8:
            logger.info("SYSTEM HEALTH: GOOD - Minor issues detected")
            health_status = "GOOD"
        elif passed_checks >= total_checks * 0.6:
            logger.info("SYSTEM HEALTH: FAIR - Several issues need attention")
            health_status = "FAIR"
        else:
            logger.info("SYSTEM HEALTH: POOR - Critical issues detected")
            health_status = "POOR"
        health_report = {
            "timestamp": time.time(),
            "total_checks": total_checks,
            "passed_checks": passed_checks,
            "health_status": health_status,
            "detailed_results": self.health_results,
        }
        # --- Tachyonic Database Archival ---
        tachyonic_dir = os.path.join("docs", "tachyonic_archive")
        os.makedirs(tachyonic_dir, exist_ok=True)
        report_file = os.path.join(tachyonic_dir, "system_health_report.json")
        with open(report_file, "w") as f:
            json.dump(health_report, f, indent=2)
        logger.info(f"Detailed health report saved to: {report_file}")
        return passed_checks, total_checks, health_status


def main() -> int:
    monitor = AIOSSystemHealthMonitor()
    passed, total, status = monitor.run_comprehensive_health_check()
    if status in ["EXCELLENT", "GOOD"]:
        return 0
    elif status == "FAIR":
        return 1
    else:
        return 2


if __name__ == "__main__":
    exit(main())
