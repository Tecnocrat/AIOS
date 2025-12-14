#!/usr/bin/env python3
"""
AINLP Dendritic Validation Script for AIOS VSCode Integration Module
Deep testing of consolidated architecture functionality
"""

import sys
from pathlib import Path

# Add module path
sys.path.insert(0, str(Path(__file__).parent.parent))


def test_imports():
    """Test all module imports work correctly"""
    print("🔍 Testing module imports...")

    try:
        # Test main module
        import main
        assert hasattr(main, 'app')
        print("  ✅ main module imported")

        # Test service modules
        import services.debug_manager
        assert hasattr(services.debug_manager, '_debug_manager')
        import services.fractal_cache_manager
        assert hasattr(services.fractal_cache_manager, 'FractalCacheManager')
        print("  ✅ service modules imported")

        # Test endpoint modules
        import endpoints.ai_endpoints
        assert hasattr(endpoints.ai_endpoints, 'router')
        import endpoints.development_endpoints
        assert hasattr(endpoints.development_endpoints, 'router')
        import endpoints.system_endpoints
        assert hasattr(endpoints.system_endpoints, 'router')
        import endpoints.ux_endpoints
        assert hasattr(endpoints.ux_endpoints, 'router')
        print("  ✅ endpoint modules imported")

        # Test models
        import models
        assert hasattr(models, 'AIOSRequest')
        print("  ✅ models module imported")

        return True
    except Exception as e:
        print(f"  ❌ Import error: {e}")
        return False


def test_app_initialization():
    """Test FastAPI app initializes correctly"""
    print("🔍 Testing FastAPI app initialization...")

    try:
        import main

        # Check app exists
        assert hasattr(main, 'app')
        app = main.app
        assert app is not None
        print("  ✅ app object exists")

        # Check routes exist
        assert hasattr(app, 'routes')
        assert len(app.routes) > 0
        print(f"  ✅ {len(app.routes)} routes registered")

        # Check state exists
        assert hasattr(app, 'state')
        print("  ✅ app state initialized")

        return True
    except Exception as e:
        print(f"  ❌ App initialization error: {e}")
        return False


def test_debug_manager():
    """Test debug manager functionality"""
    print("🔍 Testing debug manager...")

    try:
        from services.debug_manager import _debug_manager

        # Test logging
        initial_count = _debug_manager.session_metadata['total_requests']
        _debug_manager.log_request("/test", "test_data")

        assert (
            _debug_manager.session_metadata['total_requests']
            == initial_count + 1
        )
        print("  ✅ request logging works")

        # Test error logging
        initial_errors = _debug_manager.session_metadata['total_errors']
        _debug_manager.log_error(ValueError("test error"))

        assert (
            _debug_manager.session_metadata['total_errors']
            == initial_errors + 1
        )
        print("  ✅ error logging works")

        return True
    except Exception as e:
        print(f"  ❌ Debug manager error: {e}")
        return False


def test_intent_processing():
    """Test intent processing functionality"""
    print("🔍 Testing intent processing...")

    try:
        import endpoints.ai_endpoints

        # Test response generation
        response = endpoints.ai_endpoints.generate_aios_response(
            "test message", {"workspace": "test"}
        )
        assert isinstance(response, str)
        assert len(response) > 0
        print("  ✅ response generation works")

        # Test different intents
        intents = ["aios", "code", "architecture", "performance", "help"]
        for intent in intents:
            response = endpoints.ai_endpoints.generate_aios_response(
                f"tell me about {intent}", {}
            )
            assert isinstance(response, str)
            assert len(response) > 0

        print("  ✅ multiple intents processed")

        return True
    except Exception as e:
        print(f"  ❌ Intent processing error: {e}")
        return False


def test_endpoint_routers():
    """Test endpoint routers are properly configured"""
    print("🔍 Testing endpoint routers...")

    try:
        import endpoints.ai_endpoints
        import endpoints.development_endpoints
        import endpoints.system_endpoints
        import endpoints.ux_endpoints

        # Test AI endpoints - check routes exist
        assert hasattr(endpoints.ai_endpoints.router, 'routes')
        assert len(endpoints.ai_endpoints.router.routes) > 0
        print("  ✅ AI endpoints router configured")

        # Test development endpoints
        assert hasattr(endpoints.development_endpoints.router, 'routes')
        assert len(endpoints.development_endpoints.router.routes) > 0
        print("  ✅ Development endpoints router configured")

        # Test system endpoints
        assert hasattr(endpoints.system_endpoints.router, 'routes')
        assert len(endpoints.system_endpoints.router.routes) > 0
        print("  ✅ System endpoints router configured")

        # Test UX endpoints
        assert hasattr(endpoints.ux_endpoints.router, 'routes')
        assert len(endpoints.ux_endpoints.router.routes) > 0
        print("  ✅ UX endpoints router configured")

        return True
    except Exception as e:
        print(f"  ❌ Endpoint router error: {e}")
        return False


def test_models():
    """Test Pydantic models"""
    print("🔍 Testing Pydantic models...")

    try:
        import models

        # Test that models module has expected classes
        assert hasattr(models, 'AIOSRequest')
        assert hasattr(models, 'NLUIntentRequest')
        assert hasattr(models, 'CodeReviewRequest')
        print("  ✅ Models module has expected classes")

        # Test basic model instantiation
        request_class = getattr(models, 'NLUIntentRequest')
        request = request_class(message="test", context={})
        assert request.message == "test"
        print("  ✅ Model instantiation works")

        return True
    except Exception as e:
        print(f"  ❌ Model validation error: {e}")
        return False


def main():
    """Run all validation tests"""
    print("🧠 AINLP Dendritic Validation Suite")
    print("=" * 50)

    tests = [
        ("Module Imports", test_imports),
        ("FastAPI App", test_app_initialization),
        ("Debug Manager", test_debug_manager),
        ("Intent Processing", test_intent_processing),
        ("Endpoint Routers", test_endpoint_routers),
        ("Pydantic Models", test_models),
    ]

    results = []
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        success = test_func()
        results.append(success)

    # Summary
    print("\n" + "=" * 50)
    print("📊 VALIDATION SUMMARY")
    print("=" * 50)

    passed = sum(results)
    total = len(results)

    for i, (test_name, _) in enumerate(tests):
        status = "✅ PASS" if results[i] else "❌ FAIL"
        print(f"  {status} {test_name}")

    print(f"\n🎯 Overall: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 ALL TESTS PASSED! AINLP dendritic consolidation is")
        print("successful.")
        return 0
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
