#!/usr/bin/env python3
"""
🧪 AIOS OpenCV Integration Validation Test
Simple validation test for OpenCV integration with AIOS core functions.
"""

import sys
import os

# Add scripts directory to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scripts'))

def test_opencv_import():
    """Test OpenCV import and basic functionality."""
    print("🔍 Testing OpenCV import...")
    try:
        import cv2
        print(f"✅ OpenCV {cv2.__version__} imported successfully")
        return True
    except ImportError as e:
        print(f"❌ OpenCV import failed: {e}")
        return False

def test_opencv_vision_module():
    """Test OpenCV Vision Module creation and initialization."""
    print("🔍 Testing OpenCV Vision Module...")
    try:
        from opencv_vision_module import OpenCVVisionModule
        
        # Create module
        module = OpenCVVisionModule()
        print("✅ OpenCV Vision Module created")
        
        # Initialize module
        if module.initialize():
            print("✅ OpenCV Vision Module initialized")
            
            # Get consciousness state
            state = module.get_consciousness_state()
            print(f"✅ Consciousness state: coherence={state['quantum_coherence']:.3f}")
            
            # Shutdown
            module.shutdown()
            print("✅ OpenCV Vision Module shutdown")
            return True
        else:
            print("❌ OpenCV Vision Module initialization failed")
            return False
            
    except Exception as e:
        print(f"❌ OpenCV Vision Module test failed: {e}")
        return False

def test_opencv_service_integration():
    """Test OpenCV Service integration with AIOS."""
    print("🔍 Testing OpenCV Service integration...")
    try:
        from opencv_vision_module import OpenCVVisionService
        
        # Create service
        service = OpenCVVisionService()
        print("✅ OpenCV Vision Service created")
        
        # Initialize service
        if service.initialize():
            print("✅ OpenCV Vision Service initialized")
            
            # Test consciousness state request
            request = {'action': 'get_consciousness_state'}
            response = service.process_request(request)
            
            if response['success']:
                print("✅ Consciousness state request successful")
                coherence = response['consciousness_state']['quantum_coherence']
                print(f"✅ Quantum coherence: {coherence:.3f}")
            else:
                print("❌ Consciousness state request failed")
                return False
            
            # Shutdown
            service.shutdown()
            print("✅ OpenCV Vision Service shutdown")
            return True
        else:
            print("❌ OpenCV Vision Service initialization failed")
            return False
            
    except Exception as e:
        print(f"❌ OpenCV Service integration test failed: {e}")
        return False

def test_main_orchestrator_integration():
    """Test integration with main AIOS orchestrator."""
    print("🔍 Testing main orchestrator integration...")
    try:
        # Import main orchestrator functions
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scripts'))
        
        from main import initialize_services, get_service, shutdown_services
        
        # Initialize services
        initialize_services()
        print("✅ AIOS services initialized")
        
        # Get OpenCV service
        opencv_service = get_service('opencv_vision')
        if opencv_service:
            print("✅ OpenCV service found in registry")
            
            # Test service functionality
            request = {'action': 'get_consciousness_state'}
            response = opencv_service.process_request(request)
            
            if response['success']:
                print("✅ OpenCV service functioning through orchestrator")
            else:
                print("❌ OpenCV service request failed")
                return False
        else:
            print("❌ OpenCV service not found in registry")
            return False
        
        # Shutdown services
        shutdown_services()
        print("✅ AIOS services shutdown")
        return True
        
    except Exception as e:
        print(f"❌ Main orchestrator integration test failed: {e}")
        return False

def main():
    """Run all validation tests."""
    print("🧪 AIOS OpenCV Integration Validation")
    print("=" * 50)
    
    tests = [
        ("OpenCV Import", test_opencv_import),
        ("OpenCV Vision Module", test_opencv_vision_module),
        ("OpenCV Service Integration", test_opencv_service_integration),
        ("Main Orchestrator Integration", test_main_orchestrator_integration),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        print("-" * 30)
        
        try:
            result = test_func()
            results.append((test_name, result))
            
            if result:
                print(f"✅ {test_name}: PASSED")
            else:
                print(f"❌ {test_name}: FAILED")
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"  {test_name}: {status}")
    
    print(f"\n📈 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All OpenCV integration tests passed!")
        print("✅ OpenCV is successfully integrated with AIOS core functions.")
        return True
    else:
        print("⚠️ Some tests failed. Please review the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)