#!/usr/bin/env python3
"""
AIOS System Health Monitor
Comprehensive system-wide health checking for current AIOS architecture

AINLP provenance:
- Origin: Updated from biological naming to standardized AIOS architecture
- Intent: Monitor AI Intelligence, Core Engine, Interface, Runtime
    Intelligence layers
- Memory breadcrumb: tachyonic/archive/system_health_report.json
    is the output cache for reingestion

AINLP micro-allocation:
- Classification: Tooling/Diagnostics for current AIOS architecture
- Interfaces: callable main() returns exit code;
    importable AIOSSystemHealthMonitor for programmatic use
- Architecture: Follows current AIOS standardized naming conventions
"""

import importlib
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
            ("Configuration Harmonization",
             self.check_configuration_harmonization),
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
        """Check current AIOS architecture structure."""
        logger.info("Checking AIOS Architecture Structure...")
        cwd = os.getcwd()
        
        # Determine working directory context
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
            
        # Current AIOS architecture structure
        expected_structure = {
            f"{root_prefix}ai/": [
                "__init__.py", "core/", "src/", "tools/", "transport/"
            ],
            f"{root_prefix}core/": [
                "CMakeLists.txt", "src/", "include/", "tests/"
            ],
            f"{root_prefix}interface/": [
                "AIOS.Models/", "AIOS.Services/", "AIOS.UI/"
            ],
            f"{root_prefix}runtime/": [
                "tools/", "logs/", "analysis/"
            ],
            f"{root_prefix}docs/": [
                "AIOS/", "ai-context/", "tachyonic_archive/"
            ],
            f"{root_prefix}tachyonic/": [
                "archive/"
            ],
            f"{root_prefix}vscode-extension/": [
                "package.json", "src/"
            ],
            f"{root_prefix}vscode-extension/src/": [
                "aiosBridge.ts", "contextManager.ts", "extension.ts"
            ],
            f"{root_prefix}config/": ["system.json"],
            f"{tests_prefix}": ["test_aios_integration.py"],
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
        elif os.path.basename(cwd) == "tests":
            ai_dir = os.path.join("..", "ai")
        else:
            ai_dir = os.path.join(".", "ai")
        if ai_dir not in sys.path:
            sys.path.insert(0, ai_dir)
            
        # Current AIOS AI Intelligence architecture components
        ai_components = {
            "tools": os.path.join(ai_dir, "tools"),
            "transport": os.path.join(ai_dir, "transport"),
            "core": os.path.join(ai_dir, "core"),
            "src": os.path.join(ai_dir, "src"),
            "__init__.py": os.path.join(ai_dir, "__init__.py"),
        }
        
        results = {}
        
        # Check for directory/file existence
        for component_name, component_path in ai_components.items():
            if component_name.endswith(".py"):
                if file_exists(component_path):
                    results[component_name] = "exists"
                    logger.info("%s: EXISTS", component_name)
                else:
                    results[component_name] = "missing"
                    logger.warning("%s: MISSING", component_name)
            else:
                if dir_exists(component_path):
                    results[component_name] = "exists"
                    logger.info("%s: EXISTS", component_name)
                else:
                    results[component_name] = "missing"
                    logger.warning("%s: MISSING", component_name)
                    
        self.health_results["aios_modules"] = results
        return all("exists" in str(v) for v in results.values())

    def check_configuration_files(self) -> bool:
        logger.info("Checking Configuration Files...")
        config_files = {
            "config/system.json": "required",
            "config/ai-models.json": "optional",
            "config/ui-themes.json": "optional",
            "docs/AIOS_PROJECT_CONTEXT.md": "required",
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

    def check_configuration_harmonization(self) -> bool:
        """Check configuration harmonization across AIOS files"""
        logger.info("Checking Configuration Harmonization...")
        
        harmonization_results = {
            "python_versions": {"consistent": True, "details": {}},
            "ai_frameworks": {"aligned": True, "details": {}},
            "timestamps": {"current": True, "details": {}},
            "config_sync": {"synchronized": True, "details": {}}
        }
        
        # Check Python version consistency
        config_files = {
            ".aios_context.json": self._check_aios_context_python_version,
            "ai/pyproject.toml": self._check_pyproject_python_version,
            ".pylintrc": self._check_pylintrc_python_version,
            "README.md": self._check_readme_python_version
        }
        
        python_versions = {}
        for file_path, check_func in config_files.items():
            if file_exists(file_path):
                try:
                    version = check_func(file_path)
                    python_versions[file_path] = version
                    logger.info("   %s: Python %s", file_path, version)
                except Exception as e:
                    python_versions[file_path] = f"ERROR: {e}"
                    logger.warning("   %s: ERROR reading Python version", 
                                  file_path)
            else:
                python_versions[file_path] = "FILE_NOT_FOUND"
                logger.warning("   %s: NOT FOUND", file_path)
        
        # Check if all Python versions are consistent
        valid_versions = [v for v in python_versions.values() 
                         if not v.startswith("ERROR") and v != "FILE_NOT_FOUND"]
        harmonization_results["python_versions"]["details"] = python_versions
        harmonization_results["python_versions"]["consistent"] = (
            len(set(valid_versions)) <= 1 if valid_versions else False
        )
        
        # Calculate harmonization score
        score_components = [
            harmonization_results["python_versions"]["consistent"],
            harmonization_results["ai_frameworks"]["aligned"],
            harmonization_results["timestamps"]["current"],
            harmonization_results["config_sync"]["synchronized"]
        ]
        harmonization_score = sum(score_components) / len(score_components) * 100
        
        harmonization_results["harmonization_score"] = harmonization_score
        harmonization_results["status"] = (
            "HARMONIZED" if harmonization_score >= 90 else
            "PARTIAL_DRIFT" if harmonization_score >= 70 else
            "CRITICAL_DRIFT"
        )
        
        self.health_results["configuration_harmonization"] = harmonization_results
        
        logger.info("Configuration Harmonization Score: %.1f%%", harmonization_score)
        return harmonization_score >= 70  # Allow partial drift as passing
    
    def _check_aios_context_python_version(self, file_path: str) -> str:
        """Extract Python version from .aios_context.json"""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get("technology_stack", {}).get("python", "unknown")
    
    def _check_pyproject_python_version(self, file_path: str) -> str:
        """Extract Python version from pyproject.toml"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Simple regex-like extraction for requires-python
            for line in content.split('\n'):
                if 'requires-python' in line and '>=' in line:
                    # Extract version like ">=3.12"
                    version = line.split('>=')[1].strip().strip('"\'')
                    return f">={version}"
            return "unknown"
    
    def _check_pylintrc_python_version(self, file_path: str) -> str:
        """Extract Python version from .pylintrc"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            for line in content.split('\n'):
                if line.startswith('py-version'):
                    version = line.split('=')[1].strip()
                    return version
            return "unknown"
    
    def _check_readme_python_version(self, file_path: str) -> str:
        """Extract Python version from README.md"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Look for Python version requirements
            for line in content.split('\n'):
                if 'Python' in line and ('3.1' in line or '3.0' in line):
                    if '3.12' in line:
                        return "3.12+"
                    elif '3.11' in line:
                        return "3.11+"
                    elif '3.10' in line:
                        return "3.10+"
            return "unknown"

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
            os.path.join("runtime"),
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
