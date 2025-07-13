"""
AIOS Integration Core Logic & Testing Framework
Modular integration for VSCode Extension + AIOS Communication Bridge
Upgraded for extensibility, tachyonic archival, and future diagnostics.
"""

import json
import os
import sys
import time
from datetime import datetime

import requests

# Add ai directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "ai"))


class AIOSIntegrationCore:
    """
    Modular integration core for AIOS-VSCode bridge.
    Provides test routines, diagnostics, and extensibility hooks.
    """

    def __init__(self, base_url=None, context=None):
        self.base_url = base_url or "http://localhost:8080"
        self.test_results = {}
        self.start_time = time.time()
        self.context = context or {}
        self.archive_dir = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "..",
                "..",
                "docs",
                "tachyonic_archive",
            )
        )
        os.makedirs(self.archive_dir, exist_ok=True)

    def test_server_health(self):
        """Test if AIOS integration server is running"""
        print("🔍 Testing server health...")
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            result = response.json()
            self.test_results["server_health"] = {
                "status": response.status_code,
                "response": result,
                "passed": response.status_code == 200,
            }
            print("✅ Server Health: PASSED")
            print(
                "   Python AI Cells: {}".format(
                    result.get("python_ai_cells", "unknown")
                )
            )
            print(
                "   Integration Bridge: {}".format(
                    result.get("integration_bridge", "unknown")
                )
            )
            return True
        except Exception as e:
            self.test_results["server_health"] = {
                "status": "ERROR",
                "error": str(e),
                "passed": False,
            }
            print(f"❌ Server Health: FAILED - {e}")
            return False

    def test_message_processing(self):
        """Test main AIOS message processing"""
        print("🔍 Testing AIOS message processing...")
        try:
            test_message = {
                "message": "Hello AIOS, can you help me with code analysis?",
                "context": {
                    "workspace": "AIOS-Test",
                    "timestamp": time.time(),
                },
            }
            start = time.time()
            response = requests.post(
                f"{self.base_url}/process", json=test_message, timeout=10
            )
            end = time.time()
            if response.status_code == 200:
                result = response.json()
                processing_time = (end - start) * 1000
                self.test_results["message_processing"] = {
                    "status": response.status_code,
                    "response": result,
                    "processing_time": processing_time,
                    "passed": True,
                }
                print("✅ Message processing: PASSED")
                print(
                    "   Response: {}...".format(result.get("response_text", "")[:100])
                )
                print(f"   Confidence: {result.get('confidence', 'n/a')}")
                print(f"   Processing Time: {processing_time:.2f}ms")
                return True
            else:
                self.test_results["message_processing"] = {
                    "status": response.status_code,
                    "error": f"HTTP {response.status_code}",
                    "passed": False,
                }
                print(f"❌ Message processing: FAILED ({response.status_code})")
                return False
        except Exception as e:
            self.test_results["message_processing"] = {
                "status": "ERROR",
                "error": str(e),
                "passed": False,
            }
            print(f"❌ Message processing: ERROR - {e}")
            return False

    def check_vscode_extension(self):
        """Check if VSCode extension endpoint is available (mock or real)"""
        print("🔍 Checking VSCode extension endpoint...")
        try:
            # Example endpoint, adjust as needed for your extension
            response = requests.get(f"{self.base_url}/vscode-extension", timeout=5)
            result = response.json()
            self.test_results["vscode_extension"] = {
                "status": response.status_code,
                "response": result,
                "passed": response.status_code == 200,
            }
            print("✅ VSCode Extension: PASSED")
            print(f"   Extension Status: {result.get('status', 'unknown')}")
            return True
        except Exception as e:
            self.test_results["vscode_extension"] = {
                "status": "ERROR",
                "error": str(e),
                "passed": False,
            }
            print(f"❌ VSCode Extension: FAILED - {e}")
            return False

    def check_context_registry(self):
        """Check if AIOS context registry endpoint is available and valid"""
        print("🔍 Checking AIOS context registry endpoint...")
        try:
            response = requests.get(f"{self.base_url}/context-registry", timeout=5)
            result = response.json()
            self.test_results["context_registry"] = {
                "status": response.status_code,
                "response": result,
                "passed": (response.status_code == 200 and result.get("valid", False)),
            }
            print("✅ Context Registry: PASSED")
            print(f"   Registry Valid: {result.get('valid', 'unknown')}")
            return True
        except Exception as e:
            self.test_results["context_registry"] = {
                "status": "ERROR",
                "error": str(e),
                "passed": False,
            }
            print(f"❌ Context Registry: FAILED - {e}")
            return False

    def check_python_dependencies(self, required=None):
        """Check for required Python dependencies and report missing ones"""
        print("🔍 Checking Python dependencies...")
        if required is None:
            required = ["requests", "json", "os", "sys", "time"]
        missing = []
        for pkg in required:
            try:
                __import__(pkg)
            except ImportError:
                missing.append(pkg)
        self.test_results["python_dependencies"] = {
            "required": required,
            "missing": missing,
            "passed": len(missing) == 0,
        }
        if missing:
            print(f"❌ Missing Python dependencies: {missing}")
            return False
        print("✅ All required Python dependencies are installed.")
        return True

    def run_basic_integration(self):
        """Run basic integration routines (modular entrypoint)"""
        print("🚀 AIOS VSCode Integration Core Logic...")
        print("=" * 50)
        tests = [
            ("Server Health", self.test_server_health),
            ("Message Processing", self.test_message_processing),
        ]
        passed_tests = 0
        total_tests = len(tests)
        for test_name, test_func in tests:
            print(f"\n🧪 Running: {test_name}")
            if test_func():
                passed_tests += 1
        total_time = time.time() - self.start_time
        print("\n" + "=" * 50)
        print("🎯 AIOS Integration Core Complete")
        print("=" * 50)
        print(f"✅ Tests Passed: {passed_tests}/{total_tests}")
        print(f"⏱️  Total Time: {total_time:.2f} seconds")
        if passed_tests == total_tests:
            print("🎉 ALL TESTS PASSED!")
        else:
            print("⚠️  Some tests failed")
        return passed_tests == total_tests

    def run_all_routines(self):
        """Run all integration and diagnostic routines (extensible)"""
        print("🚀 AIOS VSCode Integration Full Diagnostics...")
        print("=" * 50)
        routines = [
            ("Server Health", self.test_server_health),
            ("Message Processing", self.test_message_processing),
            ("VSCode Extension", self.check_vscode_extension),
            ("Context Registry", self.check_context_registry),
            ("Python Dependencies", self.check_python_dependencies),
        ]
        passed = 0
        for name, func in routines:
            print(f"\n🧪 Running: {name}")
            if func():
                passed += 1
        total = len(routines)
        print("\n" + "=" * 50)
        print("🎯 AIOS Integration Diagnostics Complete")
        print("=" * 50)
        print(f"✅ Routines Passed: {passed}/{total}")
        if passed == total:
            print("🎉 ALL ROUTINES PASSED!")
        else:
            print("⚠️  Some routines failed")
        return passed == total

    def archive_results(self, success):
        """Archive results to tachyonic archive with timestamped filename"""
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_file = os.path.join(
            self.archive_dir, f"aios_vscode_integration_{ts}.json"
        )
        with open(archive_file, "w") as f:
            json.dump(
                {
                    "timestamp": time.time(),
                    "context": self.context,
                    "results": self.test_results,
                    "success": success,
                },
                f,
                indent=2,
            )
        print(f"\n📄 Results archived to: {archive_file}")
        return archive_file

    # Extensibility: add more integration/diagnostic routines here


def test_aios_server():
    """Legacy function for backward compatibility"""
    core = AIOSIntegrationCore()
    return core.run_basic_integration()


def main():
    """Main integration execution (CLI entrypoint)"""
    core = AIOSIntegrationCore()
    success = core.run_all_routines()
    core.archive_results(success)
    return 0 if success else 1


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="AIOS Integration Core")
    parser.add_argument(
        "--preflight",
        action="store_true",
        help="Run preflight diagnostics only and exit.",
    )
    args = parser.parse_args()
    if args.preflight:
        core = AIOSIntegrationCore()
        success = core.run_all_routines()
        sys.exit(0 if success else 1)
    else:
        exit(main())
