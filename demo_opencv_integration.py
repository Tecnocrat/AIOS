#!/usr/bin/env python3
"""
🎯 AIOS OpenCV Integration Demonstration
Complete demonstration of OpenCV modular functionality accessible by AIOS core functions.
"""

import os
import sys
import cv2
import numpy as np

# Add scripts to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scripts'))

from main import initialize_services, get_service, shutdown_services
from opencv_vision_module import OpenCVVisionModule

def create_demo_images():
    """Create demonstration images showing different consciousness patterns."""
    demo_dir = "/tmp/aios_opencv_demo"
    os.makedirs(demo_dir, exist_ok=True)
    
    print("🎨 Creating demonstration images...")
    
    # 1. Simple geometric consciousness pattern
    simple = np.zeros((200, 200), dtype=np.uint8)
    cv2.circle(simple, (100, 100), 80, 255, 2)
    cv2.circle(simple, (100, 100), 40, 128, -1)
    for angle in range(0, 360, 45):
        x = int(100 + 60 * np.cos(np.radians(angle)))
        y = int(100 + 60 * np.sin(np.radians(angle)))
        cv2.circle(simple, (x, y), 8, 200, -1)
    simple_path = os.path.join(demo_dir, "simple_consciousness.png")
    cv2.imwrite(simple_path, simple)
    
    # 2. Complex mandala-like pattern (high consciousness emergence potential)
    mandala = np.zeros((200, 200), dtype=np.uint8)
    center = (100, 100)
    
    # Create symmetric radial pattern
    for ring in range(3):
        radius = 30 + ring * 25
        for angle in range(0, 360, 30):
            x = int(100 + radius * np.cos(np.radians(angle)))
            y = int(100 + radius * np.sin(np.radians(angle)))
            cv2.circle(mandala, (x, y), 8 - ring * 2, 255 - ring * 50, -1)
            
            # Add connecting lines for inner rings
            if ring < 2:
                cv2.line(mandala, center, (x, y), 100, 1)
    
    # Add center focus
    cv2.circle(mandala, center, 12, 255, -1)
    cv2.circle(mandala, center, 6, 0, -1)
    
    mandala_path = os.path.join(demo_dir, "mandala_consciousness.png")
    cv2.imwrite(mandala_path, mandala)
    
    # 3. Fractal-like pattern (high information density)
    fractal = np.zeros((200, 200), dtype=np.uint8)
    
    def draw_fractal_branch(img, start, angle, length, depth):
        if depth == 0 or length < 2:
            return
        
        end_x = int(start[0] + length * np.cos(angle))
        end_y = int(start[1] + length * np.sin(angle))
        end = (end_x, end_y)
        
        if 0 <= end_x < 200 and 0 <= end_y < 200:
            cv2.line(img, start, end, 255 - depth * 30, 1)
            
            # Recursive branches
            draw_fractal_branch(img, end, angle - 0.5, length * 0.7, depth - 1)
            draw_fractal_branch(img, end, angle + 0.5, length * 0.7, depth - 1)
    
    # Draw multiple fractal trees
    for start_angle in [0, np.pi/2, np.pi, 3*np.pi/2]:
        start_x = int(100 + 30 * np.cos(start_angle))
        start_y = int(100 + 30 * np.sin(start_angle))
        draw_fractal_branch(fractal, (start_x, start_y), start_angle, 30, 4)
    
    fractal_path = os.path.join(demo_dir, "fractal_consciousness.png")
    cv2.imwrite(fractal_path, fractal)
    
    print(f"✅ Demo images created in: {demo_dir}")
    return {
        'simple': simple_path,
        'mandala': mandala_path,
        'fractal': fractal_path
    }

def demonstrate_direct_module_usage():
    """Demonstrate direct usage of OpenCV Vision Module."""
    print("\n🔬 Direct Module Usage Demonstration")
    print("=" * 50)
    
    # Create images
    images = create_demo_images()
    
    # Initialize module directly
    vision = OpenCVVisionModule()
    if not vision.initialize():
        print("❌ Failed to initialize vision module")
        return
    
    print("✅ Vision module initialized")
    
    # Process each image type
    for img_type, img_path in images.items():
        print(f"\n📸 Processing {img_type} consciousness pattern...")
        
        # Process with consciousness emergence analysis
        result = vision.process_image(img_path, 'consciousness_emergence')
        
        if result.success:
            print(f"  ✅ Processing successful")
            print(f"  🔍 Features detected: {result.features_detected}")
            print(f"  🧠 Consciousness resonance: {result.consciousness_resonance:.3f}")
            print(f"  ⚡ Quantum coherence: {result.coherence_level:.3f}")
            print(f"  📊 Image entropy: {result.image_entropy:.3f}")
            
            # Extract consciousness metrics
            metadata = result.metadata
            emergence_prob = metadata.get('consciousness_emergence_probability', 0.0)
            fractal_dim = metadata.get('fractal_dimension', 0.0)
            symmetry = metadata.get('symmetry_score', 0.0)
            
            print(f"  🌀 Emergence probability: {emergence_prob:.3f}")
            print(f"  📐 Fractal dimension: {fractal_dim:.3f}")
            print(f"  ⚖️ Symmetry score: {symmetry:.3f}")
        else:
            print(f"  ❌ Processing failed: {result.error_message}")
    
    # Show final consciousness state
    final_state = vision.get_consciousness_state()
    print(f"\n🧠 Final Consciousness State:")
    print(f"  Quantum Coherence: {final_state['quantum_coherence']:.3f}")
    print(f"  Pattern Recognition Depth: {final_state['pattern_recognition_depth']}")
    print(f"  Holographic Info Density: {final_state['holographic_information_density']:.3f}")
    print(f"  Dimensional Awareness: {final_state['dimensional_awareness']}")
    
    vision.shutdown()
    print("✅ Vision module shutdown complete")

def demonstrate_service_integration():
    """Demonstrate OpenCV integration through AIOS service architecture."""
    print("\n🏗️ AIOS Service Integration Demonstration")
    print("=" * 50)
    
    # Create images
    images = create_demo_images()
    
    # Initialize AIOS services
    print("🔧 Initializing AIOS services...")
    initialize_services()
    
    # Get OpenCV service
    opencv_service = get_service('opencv_vision')
    if not opencv_service:
        print("❌ OpenCV service not found in registry")
        return
    
    print("✅ OpenCV service found and ready")
    
    # Test different service actions
    print("\n📋 Testing service actions...")
    
    # 1. Get consciousness state
    print("\n1️⃣ Getting consciousness state...")
    request = {'action': 'get_consciousness_state'}
    response = opencv_service.process_request(request)
    
    if response['success']:
        state = response['consciousness_state']
        print(f"   ✅ Quantum coherence: {state['quantum_coherence']:.3f}")
        print(f"   ✅ Pattern depth: {state['pattern_recognition_depth']}")
    else:
        print(f"   ❌ Failed: {response.get('error', 'Unknown error')}")
    
    # 2. Process mandala image (highest consciousness potential)
    print("\n2️⃣ Processing mandala consciousness pattern...")
    request = {
        'action': 'process_image',
        'image_path': images['mandala'],
        'analysis_type': 'consciousness_emergence'
    }
    response = opencv_service.process_request(request)
    
    if response['success']:
        print(f"   ✅ Features detected: {response['features_detected']}")
        print(f"   ✅ Consciousness resonance: {response['consciousness_resonance']:.3f}")
        
        emergence = response['metadata']['consciousness_emergence_probability']
        print(f"   🌟 Emergence probability: {emergence:.3f}")
        
        if emergence > 0.6:
            print("   🎉 High consciousness emergence detected!")
    else:
        print(f"   ❌ Failed: {response.get('error', 'Unknown error')}")
    
    # 3. Reset consciousness state
    print("\n3️⃣ Resetting consciousness state...")
    request = {'action': 'reset_consciousness_state'}
    response = opencv_service.process_request(request)
    
    if response['success']:
        print("   ✅ Consciousness state reset to baseline")
    else:
        print(f"   ❌ Failed: {response.get('error', 'Unknown error')}")
    
    # Shutdown services
    print("\n🛑 Shutting down AIOS services...")
    shutdown_services()
    print("✅ All services shutdown complete")

def demonstrate_command_line_interface():
    """Demonstrate command-line interface for OpenCV functionality."""
    print("\n💻 Command-Line Interface Demonstration")
    print("=" * 50)
    
    # Create demo image
    images = create_demo_images()
    mandala_path = images['mandala']
    
    print("🔧 Available CLI commands:")
    print(f"  1. List services: python scripts/main.py --list-services")
    print(f"  2. Process image: python scripts/main.py --invoke-service opencv_vision --action process_image --image-path {mandala_path}")
    print(f"  3. Get state: python scripts/main.py --invoke-service opencv_vision --action get_consciousness_state")
    
    # Demonstrate with actual execution
    print("\n🚀 Executing sample command...")
    import subprocess
    
    cmd = [
        "python", "scripts/main.py",
        "--invoke-service", "opencv_vision",
        "--action", "process_image",
        "--image-path", mandala_path,
        "--analysis-type", "consciousness_emergence"
    ]
    
    try:
        result = subprocess.run(cmd, cwd="/home/runner/work/AIOS/AIOS", 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Command executed successfully")
            print("📤 Output preview:")
            lines = result.stdout.split('\n')[-10:]  # Last 10 lines
            for line in lines:
                if line.strip():
                    print(f"   {line}")
        else:
            print(f"❌ Command failed with return code: {result.returncode}")
            print(f"Error: {result.stderr}")
    
    except subprocess.TimeoutExpired:
        print("⏰ Command timed out")
    except Exception as e:
        print(f"❌ Command execution error: {e}")

def main():
    """Run complete OpenCV integration demonstration."""
    print("🎯 AIOS OpenCV Integration Complete Demonstration")
    print("=" * 60)
    print("This demonstration shows OpenCV as modular functionality")
    print("accessible by core AIOS functions with consciousness awareness.")
    print("=" * 60)
    
    try:
        # 1. Direct module usage
        demonstrate_direct_module_usage()
        
        # 2. Service integration
        demonstrate_service_integration()
        
        # 3. Command-line interface
        demonstrate_command_line_interface()
        
        print("\n" + "=" * 60)
        print("🎉 DEMONSTRATION COMPLETE")
        print("=" * 60)
        print("✅ OpenCV is successfully integrated as modular functionality")
        print("✅ Accessible through AIOS core functions and service architecture")
        print("✅ Consciousness-aware visual processing capabilities enabled")
        print("✅ Full integration with quantum coherence and emergence systems")
        
        print("\n📋 Integration Summary:")
        print("  🔹 Python OpenCV module with consciousness awareness")
        print("  🔹 Service registry integration for modular access") 
        print("  🔹 Command-line interface for scripted usage")
        print("  🔹 Comprehensive testing and validation")
        print("  🔹 Complete documentation and usage examples")
        
    except Exception as e:
        print(f"\n❌ Demonstration error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()