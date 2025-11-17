#!/usr/bin/env python3
"""
AIOS System Health Monitor
Comprehensive system-wide health checking and module harmonization

AINLP provenance:
- Origin: migrated from ai/tests/system_health_check.py
    (diagnostic helper) on 2025-08-10
- Intent: keep side-effectful diagnostics out of pytest;
    expose as tooling for ops/dev
- Memory breadcrumb: docs/tachyonic_archive/system_health_report.json
    is the output cache for reingestion

AINLP micro-allocation:
- Classification: Tooling/Diagnostics
    (not part of runtime execution path)
- Interfaces: callable main() returns exit code;
    importable AIOSSystemHealthMonitor for programmatic use
- Reingestion note: keep signatures stable so higher layers
    can orchestrate structured health runs
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
            (
                "Engineering Tenets Advisory",
                self.check_engineering_tenets_advisory,
            ),
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
                    __import__(package)
                    results["packages"][package] = "built-in"
                else:
                    module = importlib.import_module(package)
                    version = getattr(module, "__version__", "unknown")
                    results["packages"][package] = version
                logger.info("%s: %s", package, results['packages'][package])
            except ImportError as e:
                results["packages"][package] = f"MISSING: {e}"
                logger.warning("%s: MISSING", package)
        self.health_results["python_environment"] = results
        return all(
            "MISSING" not in str(v)
            for v in results["packages"].values()
        )

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
                logger.info("%s: EXISTS", directory)
                for file in files:
                    file_path = os.path.join(dir_path, file)
                    file_present = path_exists(file_path)
                    results[directory]["files"][file] = file_present
                    if file_present:
                        logger.info("   %s: EXISTS", file)
                    else:
                        logger.warning("   %s: MISSING", file)
                        all_good = False
            else:
                logger.warning("%s: MISSING", directory)
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
                with open(package_json_path, "r", encoding="utf-8") as f:
                    package_data = json.load(f)
                    results["dependencies"] = package_data.get(
                        "dependencies", {}
                    )
                    dep_count = len(results["dependencies"])
                    logger.info("Dependencies: %d packages", dep_count)
            except (OSError, json.JSONDecodeError) as e:
                logger.warning("Error reading package.json: %s", e)
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
            core_dir = os.path.join("..", "..", "ai", "src", "core")
        elif os.path.basename(cwd) == "tests":
            ai_dir = os.path.join("..", "ai")
            core_dir = os.path.join("..", "ai", "src", "core")
        else:
            ai_dir = os.path.join(".", "ai")
            core_dir = os.path.join(".", "ai", "src", "core")
        if ai_dir not in sys.path:
            sys.path.insert(0, ai_dir)
        if core_dir not in sys.path:
            sys.path.insert(0, core_dir)
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
                pkg_init = os.path.join(core_dir, module_name, "__init__.py")
                mod_file = os.path.join(core_dir, f"{module_name}.py")

                target_path = None
                if file_exists(pkg_init):
                    target_path = pkg_init
                elif file_exists(mod_file):
                    target_path = mod_file

                if target_path:
                    spec = importlib.util.spec_from_file_location(
                        module_name, target_path
                    )
                    if spec is not None and spec.loader is not None:
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)
                        results[module_name] = "importable"
                        logger.info("%s: IMPORTABLE", module_name)
                    else:
                        results[module_name] = "spec_error"
                        logger.warning("%s: SPEC/LOADER ERROR", module_name)
                else:
                    results[module_name] = "file_missing"
                    logger.warning("%s: FILE MISSING", module_name)
            except (OSError, ImportError) as e:
                results[module_name] = f"error: {str(e)[:50]}"
                logger.warning("%s: ERROR - %s", module_name, str(e)[:50])
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
                logger.info("%s: EXISTS", file_path)
            else:
                if importance == "required":
                    logger.warning("%s: MISSING (REQUIRED)", file_path)
                    required_missing += 1
                else:
                    logger.warning("%s: MISSING (optional)", file_path)
        self.health_results["configuration_files"] = results
        return required_missing == 0

    # --- Advisory scan aligned with engineering tenets ---
    def check_engineering_tenets_advisory(self) -> bool:
        """
        Non-fatal advisory check: quickly scan selected Python sources for
        patterns that often violate kernel-grade tenets (ambiguous parameters
        like 'a,b' in asymmetric helpers; over-generic helpers that manipulate
        bit halves). Returns True always (advisory), but records findings for
        the report.
        """
        logger.info("Running Engineering Tenets advisory scan...")
        findings: list[dict] = []
        roots = [
            os.path.join("ai", "src"),
            os.path.join("runtime_intelligence"),
        ]
        try:
            for root in roots:
                if not dir_exists(root):
                    continue
                for dirpath, _dirnames, filenames in os.walk(root):
                    for fname in filenames:
                        if not fname.endswith(".py"):
                            continue
                        fpath = os.path.join(dirpath, fname)
                        try:
                            with open(
                                fpath,
                                "r",
                                encoding="utf-8",
                                errors="ignore",
                            ) as fh:
                                text = fh.read()
                            # Heuristic 1: helpers with two unnamed params
                            if "def make_" in text and "(a, b)" in text:
                                findings.append({
                                    "file": fpath,
                                    "issue": (
                                        "Ambiguous helper parameters (a,b). "
                                        "Prefer explicit names (hi, lo)."
                                    ),
                                })
                            # Heuristic 2: bit reassembly without role names
                            if (
                                "<< 16" in text
                                and "def " in text
                                and "hi" not in text
                                and "lo" not in text
                            ):
                                findings.append({
                                    "file": fpath,
                                    "issue": (
                                        "Bit reassembly without role naming. "
                                        "Encode roles and endianness."
                                    ),
                                })
                        except (OSError, UnicodeError) as e:
                            findings.append({
                                "file": fpath,
                                "issue": f"scan_error: {str(e)[:60]}",
                            })
        except OSError as e:
            findings.append({
                "file": "<scan>",
                "issue": f"walk_error: {str(e)[:60]}",
            })

        self.health_results["engineering_tenets_advisory"] = {
            "findings": findings,
            "tenets_doc": "docs/AIOS/ENGINEERING_TENETS_KERNEL_GRADE.md",
            "note": "Advisory only. Improve clarity and scoping per tenets.",
        }
        # Non-fatal: always return True
        logger.info(
            "Advisory findings: %d potential items",
            len(findings),
        )
        return True

    def run_comprehensive_health_check(self) -> tuple[int, int, str]:
        logger.info("AIOS System Health Check - Comprehensive Analysis")
        logger.info("=" * 60)
        passed_checks = 0
        total_checks = len(self.checks)
        for check_name, check_func in self.checks:
            logger.info("\n%s", check_name)
            logger.info("-" * 30)
            try:
                if check_func():
                    passed_checks += 1
                    logger.info("%s: PASSED", check_name)
                else:
                    logger.warning("%s: ISSUES FOUND", check_name)
            except Exception as e:  # pylint: disable=broad-except
                logger.error("%s: ERROR - %s", check_name, e)
        total_time = time.time() - self.start_time
        logger.info("\n%s", "=" * 60)
        logger.info("SYSTEM HEALTH SUMMARY")
        logger.info("=" * 60)
        logger.info("Checks Passed: %d/%d", passed_checks, total_checks)
        logger.info("Total Time: %.2f seconds", total_time)
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
        # --- Tachyonic Archival (append-only, time-indexed) ---
        tachyonic_dir = os.path.join("docs", "tachyonic_archive")
        os.makedirs(tachyonic_dir, exist_ok=True)

        # Use UTC timestamp in filename for immutability
        ts_utc = time.strftime("%Y%m%d_%H%M%S", time.gmtime())
        report_name = f"system_health_report_{ts_utc}.json"
        report_file = os.path.join(tachyonic_dir, report_name)

        # 1) Write immutable, timestamped snapshot
        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(health_report, f, indent=2)

        # 2) Update the moving pointer to the latest snapshot
        latest_file = os.path.join(
            tachyonic_dir, "system_health_report.latest.json"
        )
        try:
            with open(latest_file, "w", encoding="utf-8") as f:
                json.dump(health_report, f, indent=2)
        except OSError as e:
            logger.warning("Could not update latest pointer: %s", e)

        # 3) Append entry to index for historical navigation
        index_file = os.path.join(tachyonic_dir, "system_health_index.json")
        index = []
        try:
            if os.path.exists(index_file):
                with open(index_file, "r", encoding="utf-8") as f:
                    index = json.load(f) or []
        except (OSError, json.JSONDecodeError):
            index = []
        index.append({
            "filename": report_name,
            "timestamp": health_report["timestamp"],
            "health_status": health_status,
            "passed_checks": passed_checks,
            "total_checks": total_checks,
        })
        try:
            with open(index_file, "w", encoding="utf-8") as f:
                json.dump(index, f, indent=2)
        except OSError as e:
            logger.warning("Could not update tachyonic index: %s", e)

        logger.info("Detailed health report saved to: %s", report_file)
        return passed_checks, total_checks, health_status


def main() -> int:
    monitor = AIOSSystemHealthMonitor()
    _passed, _total, status = monitor.run_comprehensive_health_check()
    if status in ["EXCELLENT", "GOOD"]:
        return 0
    elif status == "FAIR":
        return 1
    else:
        return 2


if __name__ == "__main__":
    exit(main())
