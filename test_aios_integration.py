"""
Simple test to verify AIOS VSCode integration server is working
"""

import json

import requests


def test_aios_server():
    base_url = "http://localhost:8080"

    print("🚀 Testing AIOS VSCode Integration Server...")

    # Test 1: Health check
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health check: PASSED")
        else:
            print(f"❌ Health check: FAILED ({response.status_code})")
    except Exception as e:
        print(f"❌ Health check: ERROR - {e}")

    # Test 2: Process message
    try:
        test_message = {
            "message": "Hello AIOS, can you help me with code analysis?",
            "context": {"workspace": "AIOS-Test", "timestamp": 1642089600000},
        }

        response = requests.post(f"{base_url}/process", json=test_message, timeout=10)

        if response.status_code == 200:
            result = response.json()
            print("✅ Message processing: PASSED")
            print(f"   Response: {result['response_text'][:100]}...")
            print(f"   Confidence: {result['confidence']}")
        else:
            print(f"❌ Message processing: FAILED ({response.status_code})")
    except Exception as e:
        print(f"❌ Message processing: ERROR - {e}")

    print("\n🎯 AIOS Integration Test Complete")


if __name__ == "__main__":
    test_aios_server()
