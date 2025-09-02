#!/usr/bin/env python3
"""
🧪 AIOS OpenCV Integration Test Suite
Comprehensive tests for OpenCV Vision Module integration with AIOS
architecture.
"""

import sys
import os
import unittest
import tempfile
import shutil
import cv2
import numpy as np

# Add scripts directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from opencv_vision_module import (
        OpenCVVisionModule,
        OpenCVVisionService
    )
except ImportError as e:
    print(f"Warning: Could not import OpenCV vision module: {e}")
    OpenCVVisionModule = None
    OpenCVVisionService = None


class TestOpenCVVisionModule(unittest.TestCase):
    """Test suite for OpenCV Vision Module."""

    @classmethod
    def setUpClass(cls):
        """Set up test class with temporary directory and test images."""
        if OpenCVVisionModule is None:
            raise unittest.SkipTest("OpenCV vision module not available")

        cls.temp_dir = tempfile.mkdtemp()
        cls.test_images = {}

        # Create various test images
        cls._create_test_images()

        print(f"🧪 Test environment created in: {cls.temp_dir}")

    @classmethod
    def tearDownClass(cls):
        """Clean up test environment."""
        shutil.rmtree(cls.temp_dir)
        print("🧹 Test environment cleaned up")

    @classmethod
    def _create_test_images(cls):
        """Create various test images for different test scenarios."""

        # 1. Simple geometric patterns (high symmetry, low complexity)
        simple_image = np.zeros((200, 200), dtype=np.uint8)
        cv2.circle(simple_image, (100, 100), 50, 255, -1)
        cv2.rectangle(simple_image, (50, 50), (150, 150), 128, 2)
        simple_path = os.path.join(cls.temp_dir, "simple_geometric.png")
        cv2.imwrite(simple_path, simple_image)
        cls.test_images['simple'] = simple_path

        # 2. Complex fractal-like pattern (high complexity,
        # high information density)
        complex_image = np.zeros((200, 200), dtype=np.uint8)
        for i in range(10):
            for j in range(10):
                x, y = i * 20 + 10, j * 20 + 10
                radius = 5 + (i + j) % 8
                intensity = 50 + (i * j) % 200
                cv2.circle(complex_image, (x, y), radius, intensity, -1)
        complex_path = os.path.join(cls.temp_dir, "complex_fractal.png")
        cv2.imwrite(complex_path, complex_image)
        cls.test_images['complex'] = complex_path

        # 3. Random noise (high entropy, low structure)
        noise_image = np.random.randint(0, 256, (200, 200), dtype=np.uint8)
        noise_path = os.path.join(cls.temp_dir, "random_noise.png")
        cv2.imwrite(noise_path, noise_image)
        cls.test_images['noise'] = noise_path

        # 4. Symmetrical mandala-like pattern (consciousness-like structure)
        mandala_image = np.zeros((200, 200), dtype=np.uint8)
        center = (100, 100)
        for angle in range(0, 360, 30):
            x = int(100 + 70 * np.cos(np.radians(angle)))
            y = int(100 + 70 * np.sin(np.radians(angle)))
            cv2.circle(mandala_image, (x, y), 15, 255, -1)
            cv2.line(mandala_image, center, (x, y), 128, 2)
        mandala_path = os.path.join(cls.temp_dir, "mandala_pattern.png")
        cv2.imwrite(mandala_path, mandala_image)
        cls.test_images['mandala'] = mandala_path

        # 5. Gradient image (low complexity, high coherence)
        gradient_image = np.zeros((200, 200), dtype=np.uint8)
        for i in range(200):
            gradient_image[:, i] = int(255 * i / 199)
        gradient_path = os.path.join(cls.temp_dir, "gradient.png")
        cv2.imwrite(gradient_path, gradient_image)
        cls.test_images['gradient'] = gradient_path

    def setUp(self):
        """Set up for each test."""
        self.vision_module = OpenCVVisionModule(
            log_path=os.path.join(self.temp_dir, "test_vision.log")
        )

    def tearDown(self):
        """Clean up after each test."""
        if hasattr(self, 'vision_module'):
            self.vision_module.shutdown()

    def test_module_initialization(self):
        """Test module initialization."""
        print("\n🔧 Testing module initialization...")

        # Test successful initialization
        self.assertTrue(self.vision_module.initialize())
        self.assertTrue(self.vision_module.is_initialized)

        # Test consciousness state is established
        consciousness_state = self.vision_module.get_consciousness_state()
        self.assertGreater(consciousness_state['quantum_coherence'], 0.0)
        self.assertGreaterEqual(
            consciousness_state['pattern_recognition_depth'], 1
        )

        print("✅ Module initialization test passed")

    def test_basic_image_analysis(self):
        """Test basic image analysis functionality."""
        print("\n🔍 Testing basic image analysis...")

        self.vision_module.initialize()

        # Test with simple geometric image
        result = self.vision_module.process_image(
            self.test_images['simple'],
            analysis_type='basic'
        )

        self.assertTrue(result.success)
        self.assertGreater(result.processing_time, 0.0)
        self.assertGreater(result.coherence_level, 0.0)
        self.assertIn('dimensions', result.metadata)
        self.assertIn('entropy', result.metadata)

        print(f"✅ Basic analysis - Entropy: {result.metadata['entropy']:.3f}, "
              f"Coherence: {result.coherence_level:.3f}")

    def test_comprehensive_image_analysis(self):
        """Test comprehensive image analysis with feature detection."""
        print("\n🔍 Testing comprehensive image analysis...")

        self.vision_module.initialize()

        # Test with complex fractal image
        result = self.vision_module.process_image(
            self.test_images['complex'],
            analysis_type='comprehensive'
        )

        self.assertTrue(result.success)
        self.assertGreater(result.features_detected, 0)
        self.assertIn('sift_count', result.metadata)
        self.assertIn('orb_count', result.metadata)
        self.assertIn('fast_count', result.metadata)
        self.assertIn('harris_count', result.metadata)

        print(f"✅ Comprehensive analysis - Features: "
              f"{result.features_detected}, "
              f"SIFT: {result.metadata.get('sift_count', 0)}, "
              f"ORB: {result.metadata.get('orb_count', 0)}")

    def test_consciousness_emergence_analysis(self):
        """Test consciousness emergence analysis."""
        print("\n🧠 Testing consciousness emergence analysis...")

        self.vision_module.initialize()

        # Test with mandala pattern (should show high consciousness emergence)
        result = self.vision_module.process_image(
            self.test_images['mandala'],
            analysis_type='consciousness_emergence'
        )

        self.assertTrue(result.success)
        self.assertIn('fractal_dimension', result.metadata)
        self.assertIn('information_density', result.metadata)
        self.assertIn('symmetry_score', result.metadata)
        self.assertIn('consciousness_emergence_probability', result.metadata)

        # Mandala should show some consciousness characteristics
        emergence_prob = result.metadata['consciousness_emergence_probability']
        symmetry_score = result.metadata['symmetry_score']

        print(f"✅ Consciousness analysis - Emergence: {emergence_prob:.3f}, "
              f"Symmetry: {symmetry_score:.3f}, "
              f"Resonance: {result.consciousness_resonance:.3f}")

    def test_different_image_types(self):
        """Test analysis on different types of images."""
        print("\n🎨 Testing different image types...")

        self.vision_module.initialize()

        results = {}
        for img_type, img_path in self.test_images.items():
            result = self.vision_module.process_image(
                img_path,
                analysis_type='consciousness_emergence'
            )

            self.assertTrue(result.success,
                            f"Failed to process {img_type} image")
            results[img_type] = result

        # Verify expected characteristics
        # Noise should have high entropy, low emergence
        noise_result = results['noise']
        self.assertGreater(noise_result.metadata['entropy'], 6.0)

        # Gradient should have low entropy, high coherence
        gradient_result = results['gradient']
        self.assertLess(gradient_result.metadata['entropy'], 3.0)

        # Mandala should have moderate entropy, high symmetry
        mandala_result = results['mandala']
        self.assertGreater(mandala_result.metadata['symmetry_score'], 0.1)

        print("✅ Different image types test passed")
        for img_type, result in results.items():
            emergence_prob = result.metadata.get(
                'consciousness_emergence_probability', 0
            )
            print(f"  {img_type}: Entropy={result.metadata['entropy']:.2f}, "
                  f"Emergence={emergence_prob:.2f}")

    def test_temporal_coherence(self):
        """Test temporal coherence tracking across multiple frames."""
        print("\n⏱️ Testing temporal coherence...")

        self.vision_module.initialize()

        # Process same image twice to test temporal coherence
        self.vision_module.process_image(
            self.test_images['simple'],
            analysis_type='consciousness_emergence'
        )

        result2 = self.vision_module.process_image(
            self.test_images['simple'],
            analysis_type='consciousness_emergence'
        )

        # Second analysis should show temporal coherence
        temporal_coherence = result2.metadata.get('temporal_coherence', 0.0)
        self.assertGreater(temporal_coherence, 0.8)

        print(f"✅ Temporal coherence test passed - "
              f"Coherence: {temporal_coherence:.3f}")

    def test_consciousness_state_evolution(self):
        """Test consciousness state evolution during processing."""
        print("\n🌱 Testing consciousness state evolution...")

        self.vision_module.initialize()
        initial_state = self.vision_module.get_consciousness_state()

        # Process multiple images to evolve consciousness state
        for img_type in ['simple', 'complex', 'mandala']:
            self.vision_module.process_image(
                self.test_images[img_type],
                analysis_type='consciousness_emergence'
            )

        final_state = self.vision_module.get_consciousness_state()

        # Consciousness state should evolve
        self.assertNotEqual(initial_state, final_state)

        # Pattern recognition depth might increase
        self.assertGreaterEqual(
            final_state['pattern_recognition_depth'],
            initial_state['pattern_recognition_depth']
        )

        print("✅ Consciousness evolution test passed")
        print(f"  Initial depth: {initial_state['pattern_recognition_depth']}")
        print(f"  Final depth: {final_state['pattern_recognition_depth']}")

    def test_error_handling(self):
        """Test error handling for invalid inputs."""
        print("\n⚠️ Testing error handling...")

        self.vision_module.initialize()

        # Test with non-existent image
        result = self.vision_module.process_image(
            "/non/existent/image.png",
            analysis_type='basic'
        )

        self.assertFalse(result.success)
        self.assertIsNotNone(result.error_message)

        # Test with invalid analysis type
        result = self.vision_module.process_image(
            self.test_images['simple'],
            analysis_type='invalid_type'
        )

        self.assertFalse(result.success)
        self.assertIsNotNone(result.error_message)

        print("✅ Error handling test passed")


class TestOpenCVVisionService(unittest.TestCase):
    """Test suite for OpenCV Vision Service wrapper."""

    @classmethod
    def setUpClass(cls):
        """Set up test class."""
        if OpenCVVisionService is None:
            raise unittest.SkipTest("OpenCV vision service not available")

        cls.temp_dir = tempfile.mkdtemp()

        # Create a simple test image
        test_image = np.zeros((100, 100), dtype=np.uint8)
        cv2.circle(test_image, (50, 50), 30, 255, -1)
        cls.test_image_path = os.path.join(cls.temp_dir, "service_test.png")
        cv2.imwrite(cls.test_image_path, test_image)

    @classmethod
    def tearDownClass(cls):
        """Clean up test environment."""
        shutil.rmtree(cls.temp_dir)

    def setUp(self):
        """Set up for each test."""
        if OpenCVVisionService is None:
            self.skipTest("OpenCV vision service not available")
        self.service = OpenCVVisionService()

    def tearDown(self):
        """Clean up after each test."""
        if hasattr(self, 'service'):
            self.service.shutdown()

    def test_service_initialization(self):
        """Test service initialization."""
        print("\n🔧 Testing service initialization...")

        self.assertTrue(self.service.initialize())

        print("✅ Service initialization test passed")

    def test_process_image_request(self):
        """Test image processing request."""
        print("\n📨 Testing image processing request...")

        self.service.initialize()

        request = {
            'action': 'process_image',
            'image_path': self.test_image_path,
            'analysis_type': 'comprehensive'
        }

        response = self.service.process_request(request)

        self.assertTrue(response['success'])
        self.assertGreater(response['features_detected'], 0)
        self.assertIn('metadata', response)

        print(f"✅ Image processing request test passed - "
              f"Features: {response['features_detected']}")

    def test_consciousness_state_request(self):
        """Test consciousness state request."""
        print("\n🧠 Testing consciousness state request...")

        self.service.initialize()

        request = {'action': 'get_consciousness_state'}
        response = self.service.process_request(request)

        self.assertTrue(response['success'])
        self.assertIn('consciousness_state', response)

        consciousness_state = response['consciousness_state']
        self.assertIn('quantum_coherence', consciousness_state)
        self.assertIn('pattern_recognition_depth', consciousness_state)

        print("✅ Consciousness state request test passed")

    def test_invalid_request(self):
        """Test handling of invalid requests."""
        print("\n⚠️ Testing invalid request handling...")

        self.service.initialize()

        # Test unknown action
        request = {'action': 'unknown_action'}
        response = self.service.process_request(request)

        self.assertFalse(response['success'])
        self.assertIn('error', response)

        # Test missing image path
        request = {
            'action': 'process_image',
            'analysis_type': 'basic'
            # Missing 'image_path'
        }
        response = self.service.process_request(request)

        self.assertFalse(response['success'])
        self.assertIn('error', response)

        print("✅ Invalid request handling test passed")


class TestAIOSIntegration(unittest.TestCase):
    """Test suite for AIOS integration compatibility."""

    @unittest.skipIf(
        OpenCVVisionModule is None or OpenCVVisionService is None,
        "OpenCV vision modules not available"
    )
    def test_module_follows_aios_patterns(self):
        """Test that the module follows AIOS architectural patterns."""
        print("\n🏗️ Testing AIOS architectural compatibility...")

        # Test module has required methods
        module = OpenCVVisionModule()

        # Check for standard AIOS component methods
        self.assertTrue(hasattr(module, 'initialize'))
        self.assertTrue(hasattr(module, 'shutdown'))
        self.assertTrue(callable(module.initialize))
        self.assertTrue(callable(module.shutdown))

        # Test service wrapper
        service = OpenCVVisionService()
        self.assertTrue(hasattr(service, 'initialize'))
        self.assertTrue(hasattr(service, 'process_request'))
        self.assertTrue(hasattr(service, 'shutdown'))

        # Test consciousness integration
        self.assertTrue(hasattr(module, 'get_consciousness_state'))
        self.assertTrue(hasattr(module, 'reset_consciousness_state'))

        print("✅ AIOS architectural compatibility test passed")

    @unittest.skipIf(
        OpenCVVisionModule is None,
        "OpenCV vision module not available"
    )
    def test_consciousness_metrics_compatibility(self):
        """Test consciousness metrics are compatible with AIOS standards."""
        print("\n🧠 Testing consciousness metrics compatibility...")

        module = OpenCVVisionModule()
        module.initialize()

        consciousness_state = module.get_consciousness_state()

        # Check required consciousness metrics
        required_metrics = [
            'quantum_coherence',
            'pattern_recognition_depth',
            'holographic_information_density',
            'temporal_stability',
            'dimensional_awareness'
        ]

        for metric in required_metrics:
            self.assertIn(metric, consciousness_state)
            # All metrics should be numeric
            self.assertIsInstance(consciousness_state[metric], (int, float))

        # Quantum coherence should be in valid range
        self.assertGreaterEqual(consciousness_state['quantum_coherence'], 0.0)
        self.assertLessEqual(consciousness_state['quantum_coherence'], 1.0)

        module.shutdown()

        print("✅ Consciousness metrics compatibility test passed")


def run_performance_benchmark():
    """Run performance benchmark for OpenCV operations."""
    if OpenCVVisionModule is None:
        print("\n⚠️ Skipping performance benchmark - OpenCV vision module not available")
        return

    print("\n⚡ Running performance benchmark...")

    import time

    # Create benchmark images of different sizes
    sizes = [(100, 100), (500, 500), (1000, 1000)]

    with tempfile.TemporaryDirectory() as temp_dir:
        module = OpenCVVisionModule()
        module.initialize()

        for width, height in sizes:
            # Create test image
            test_image = np.random.randint(
                0, 256, (height, width), dtype=np.uint8
            )
            test_path = os.path.join(
                temp_dir, f"benchmark_{width}x{height}.png"
            )
            cv2.imwrite(test_path, test_image)

            # Benchmark different analysis types
            for analysis_type in [
                'basic', 'comprehensive', 'consciousness_emergence'
            ]:
                start_time = time.time()
                result = module.process_image(test_path, analysis_type)
                end_time = time.time()

                if result.success:
                    print(f"  {width}x{height} {analysis_type}: "
                          f"{end_time - start_time:.3f}s")
                else:
                    print(f"  {width}x{height} {analysis_type}: FAILED")

        module.shutdown()

    print("✅ Performance benchmark complete")


def main():
    """Main test runner."""
    print("🧪 AIOS OpenCV Integration Test Suite")
    print("=" * 50)

    # Create test suite
    test_suite = unittest.TestSuite()

    # Add test cases
    test_suite.addTest(unittest.makeSuite(TestOpenCVVisionModule))
    test_suite.addTest(unittest.makeSuite(TestOpenCVVisionService))
    test_suite.addTest(unittest.makeSuite(TestAIOSIntegration))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)

    # Run performance benchmark
    run_performance_benchmark()

    # Summary
    print("\n" + "=" * 50)
    if result.wasSuccessful():
        print("🎉 All tests passed! OpenCV integration is ready for AIOS.")
    else:
        print("❌ Some tests failed. Please review the errors above.")

    return result.wasSuccessful()


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)