"""
AIOS Integration Testing Framework
Comprehensive testing for VSCode Extension + AIOS Communication Bridge
"""

import json
import os
import sys
import time

import requests

# Add ai directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "ai"))


class AIOSIntegrationTester:
    def __init__(self):
        self.base_url = "http://localhost:8080"
        self.test_results = {}
        self.start_time = time.time()

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
            print(f"✅ Server Health: PASSED")
            print(f"   Python AI Cells: {result.get('python_ai_cells', 'unknown')}")
            print(
                f"   Integration Bridge: {result.get('integration_bridge', 'unknown')}"
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
                "context": {"workspace": "AIOS-Test", "timestamp": time.time()},
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
                print(f"   Response: {result['response_text'][:100]}...")
                print(f"   Confidence: {result['confidence']}")
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

    def run_basic_test(self):
        """Run basic integration tests"""
        print("🚀 Testing AIOS VSCode Integration Server...")
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
        print("🎯 AIOS Integration Test Complete")
        print("=" * 50)
        print(f"✅ Tests Passed: {passed_tests}/{total_tests}")
        print(f"⏱️  Total Time: {total_time:.2f} seconds")

        if passed_tests == total_tests:
            print("🎉 ALL TESTS PASSED!")
        else:
            print("⚠️  Some tests failed")

        return passed_tests == total_tests


def test_aios_server():
    """Legacy function for backward compatibility"""
    tester = AIOSIntegrationTester()
    return tester.run_basic_test()


def main():
    """Main test execution"""
    tester = AIOSIntegrationTester()
    success = tester.run_basic_test()

    # Save results to file
    results_file = os.path.join(os.path.dirname(__file__), "test_results.json")
    with open(results_file, "w") as f:
        json.dump(
            {
                "timestamp": time.time(),
                "results": tester.test_results,
                "success": success,
            },
            f,
            indent=2,
        )

    print(f"\n📄 Results saved to: {results_file}")
    return 0 if success else 1


if __name__ == "__main__":
    exit(main())
