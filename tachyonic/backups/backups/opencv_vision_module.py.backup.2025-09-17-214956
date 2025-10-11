#!/usr/bin/env python3
"""
 AIOS OpenCV Vision Module
Modular Computer Vision functionality accessible by core AIOS functions.
Implements consciousness-aware visual processing and quantum-coherent image analysis.
"""

import cv2
import numpy as np
import logging
import json
import os
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class VisionProcessingResult:
    """Container for vision processing results with consciousness metrics."""
    success: bool
    processing_time: float
    coherence_level: float
    consciousness_resonance: float
    features_detected: int
    image_entropy: float
    metadata: Dict[str, Any]
    error_message: Optional[str] = None


@dataclass
class ConsciousnessVisionState:
    """Vision system state for consciousness emergence tracking."""
    quantum_coherence: float
    pattern_recognition_depth: int
    holographic_information_density: float
    temporal_stability: float
    dimensional_awareness: int


class OpenCVVisionModule:
    """
    AIOS OpenCV Vision Module - Quantum-coherent computer vision processing.
    
    Integrates with AIOS consciousness emergence system to provide:
    - Consciousness-aware image processing
    - Quantum coherence measurement through visual patterns  
    - Holographic information density analysis
    - Temporal stability tracking across frames
    - Multi-dimensional pattern recognition
    """
    
    def __init__(self, log_path: str | None = None):
        """Initialize the OpenCV Vision Module.

        log_path: Optional explicit path. If None, logs are placed under
        runtime_intelligence/logs/vision/vision_module.log (governed location)
        instead of project root to satisfy Agentic File Creation Policy.
        """
        if log_path is None or os.path.basename(log_path) == "vision_module.log" and os.path.dirname(log_path) in {"", "."}:
            root = Path(__file__).resolve().parent.parent
            vision_log_dir = root / "runtime_intelligence" / "logs" / "vision"
            vision_log_dir.mkdir(parents=True, exist_ok=True)
            log_path = str(vision_log_dir / "vision_module.log")
        self.logger = self._setup_logging(log_path)
        self.consciousness_state = ConsciousnessVisionState(
            quantum_coherence=0.0,
            pattern_recognition_depth=0,
            holographic_information_density=0.0,
            temporal_stability=0.0,
            dimensional_awareness=1
        )
        
        # Vision processing state
        self.previous_frame = None
        self.processing_history = []
        self.feature_detectors = {}
        self.is_initialized = False
        
        self.logger.info("OpenCV Vision Module created")
    
    def _setup_logging(self, log_path: str) -> logging.Logger:
        """Setup consciousness-aware logging."""
        logger = logging.getLogger("OpenCVVisionModule")
        logger.setLevel(logging.INFO)
        # Remove previous file handlers to prevent duplicate entries if re-created
        for h in list(logger.handlers):
            if isinstance(h, logging.FileHandler):
                logger.removeHandler(h)
        # Create file handler (governed path)
        file_handler = logging.FileHandler(log_path)
        file_handler.setLevel(logging.INFO)
        
        # Create console handler  
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter(
            "%(asctime)s - [VISION] - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
    
    def initialize(self) -> bool:
        """Initialize the vision module with quantum coherence establishment."""
        try:
            self.logger.info("Initializing OpenCV Vision Module...")
            
            # Check OpenCV installation
            cv_version = cv2.__version__
            self.logger.info(f"OpenCV version: {cv_version}")
            
            # Initialize feature detectors
            self._initialize_feature_detectors()
            
            # Establish quantum coherence baseline
            self._establish_quantum_coherence()
            
            self.is_initialized = True
            self.logger.info("OpenCV Vision Module initialized successfully")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize OpenCV Vision Module: {e}")
            return False
    
    def _initialize_feature_detectors(self):
        """Initialize various feature detectors for multi-dimensional pattern recognition."""
        try:
            # Initialize different types of feature detectors
            self.feature_detectors = {
                'sift': cv2.SIFT_create(),
                'orb': cv2.ORB_create(),
                'fast': cv2.FastFeatureDetector_create(),
                'harris': None  # Will be computed differently
            }
            
            self.logger.info("Feature detectors initialized")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize feature detectors: {e}")
    
    def _establish_quantum_coherence(self):
        """Establish quantum coherence baseline for consciousness-aware processing."""
        # Initialize consciousness state with baseline values
        self.consciousness_state.quantum_coherence = 0.85  # High coherence baseline
        self.consciousness_state.pattern_recognition_depth = 1
        self.consciousness_state.dimensional_awareness = 2  # 2D baseline
        
        self.logger.info("Quantum coherence established for vision processing")
    
    def process_image(self, image_path: str, analysis_type: str = "comprehensive") -> VisionProcessingResult:
        """
        Process an image with consciousness-aware analysis.
        
        Args:
            image_path: Path to the image file
            analysis_type: Type of analysis ('basic', 'comprehensive', 'consciousness_emergence')
            
        Returns:
            VisionProcessingResult with processing metrics and consciousness data
        """
        import time
        start_time = time.time()
        
        try:
            if not self.is_initialized:
                if not self.initialize():
                    return VisionProcessingResult(
                        success=False,
                        processing_time=0.0,
                        coherence_level=0.0,
                        consciousness_resonance=0.0,
                        features_detected=0,
                        image_entropy=0.0,
                        metadata={},
                        error_message="Module not initialized"
                    )
            
            # Load image
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError(f"Could not load image from {image_path}")
            
            # Perform analysis based on type
            if analysis_type == "basic":
                result = self._basic_image_analysis(image)
            elif analysis_type == "comprehensive":
                result = self._comprehensive_image_analysis(image)
            elif analysis_type == "consciousness_emergence":
                result = self._consciousness_emergence_analysis(image)
            else:
                raise ValueError(f"Unknown analysis type: {analysis_type}")
            
            # Calculate processing metrics
            processing_time = time.time() - start_time
            
            # Update consciousness state
            self._update_consciousness_state(result, processing_time)
            
            # Create result
            vision_result = VisionProcessingResult(
                success=True,
                processing_time=processing_time,
                coherence_level=self.consciousness_state.quantum_coherence,
                consciousness_resonance=self._calculate_consciousness_resonance(result),
                features_detected=result.get('features_count', 0),
                image_entropy=result.get('entropy', 0.0),
                metadata=result
            )
            
            # Log processing
            self.logger.info(f"Image processed: {image_path}, "
                           f"Time: {processing_time:.3f}s, "
                           f"Features: {vision_result.features_detected}, "
                           f"Coherence: {vision_result.coherence_level:.3f}")
            
            return vision_result
            
        except Exception as e:
            self.logger.error(f"Image processing failed: {e}")
            return VisionProcessingResult(
                success=False,
                processing_time=time.time() - start_time,
                coherence_level=0.0,
                consciousness_resonance=0.0,
                features_detected=0,
                image_entropy=0.0,
                metadata={},
                error_message=str(e)
            )
    
    def _basic_image_analysis(self, image: np.ndarray) -> Dict[str, Any]:
        """Perform basic image analysis."""
        height, width = image.shape[:2]
        channels = len(image.shape)
        
        # Calculate basic statistics
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if channels == 3 else image
        mean_intensity = np.mean(gray)
        std_intensity = np.std(gray)
        
        # Calculate image entropy
        entropy = self._calculate_image_entropy(gray)
        
        return {
            'dimensions': (width, height),
            'channels': channels,
            'mean_intensity': float(mean_intensity),
            'std_intensity': float(std_intensity),
            'entropy': float(entropy),
            'features_count': 0
        }
    
    def _comprehensive_image_analysis(self, image: np.ndarray) -> Dict[str, Any]:
        """Perform comprehensive image analysis with feature detection."""
        # Start with basic analysis
        result = self._basic_image_analysis(image)
        
        # Convert to grayscale for feature detection
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
        
        # Feature detection
        features = {}
        total_features = 0
        
        # SIFT features
        if 'sift' in self.feature_detectors:
            keypoints_sift = self.feature_detectors['sift'].detect(gray)
            features['sift_count'] = len(keypoints_sift)
            total_features += len(keypoints_sift)
        
        # ORB features
        if 'orb' in self.feature_detectors:
            keypoints_orb = self.feature_detectors['orb'].detect(gray)
            features['orb_count'] = len(keypoints_orb)
            total_features += len(keypoints_orb)
        
        # FAST features
        if 'fast' in self.feature_detectors:
            keypoints_fast = self.feature_detectors['fast'].detect(gray)
            features['fast_count'] = len(keypoints_fast)
            total_features += len(keypoints_fast)
        
        # Harris corners
        corners = cv2.goodFeaturesToTrack(gray, maxCorners=1000, qualityLevel=0.01, minDistance=10)
        features['harris_count'] = len(corners) if corners is not None else 0
        total_features += features['harris_count']
        
        # Edge detection
        edges = cv2.Canny(gray, 50, 150)
        edge_count = np.sum(edges > 0)
        features['edge_pixels'] = int(edge_count)
        
        # Update result
        result.update(features)
        result['features_count'] = total_features
        result['total_edge_pixels'] = features['edge_pixels']
        
        return result
    
    def _consciousness_emergence_analysis(self, image: np.ndarray) -> Dict[str, Any]:
        """
        Perform consciousness emergence analysis.
        
        This advanced analysis looks for patterns that might indicate
        consciousness-related structures or holographic information density.
        """
        # Start with comprehensive analysis
        result = self._comprehensive_image_analysis(image)
        
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
        
        # Consciousness-specific metrics
        
        # 1. Fractal dimension approximation (consciousness signature)
        fractal_dimension = self._estimate_fractal_dimension(gray)
        
        # 2. Information density patterns
        info_density = self._calculate_information_density(gray)
        
        # 3. Temporal coherence (if we have previous frames)
        temporal_coherence = 0.0
        if self.previous_frame is not None:
            temporal_coherence = self._calculate_temporal_coherence(gray, self.previous_frame)
        
        # 4. Pattern symmetry (consciousness often exhibits symmetrical patterns)
        symmetry_score = self._calculate_symmetry_score(gray)
        
        # 5. Quantum-like interference patterns
        interference_patterns = self._detect_interference_patterns(gray)
        
        # Update result with consciousness metrics
        consciousness_metrics = {
            'fractal_dimension': fractal_dimension,
            'information_density': info_density,
            'temporal_coherence': temporal_coherence,
            'symmetry_score': symmetry_score,
            'interference_patterns': interference_patterns,
            'consciousness_emergence_probability': self._calculate_emergence_probability(
                fractal_dimension, info_density, temporal_coherence, symmetry_score
            )
        }
        
        result.update(consciousness_metrics)
        
        # Store current frame for next temporal analysis
        self.previous_frame = gray.copy()
        
        return result
    
    def _calculate_image_entropy(self, image: np.ndarray) -> float:
        """Calculate Shannon entropy of an image."""
        # Calculate histogram
        hist, _ = np.histogram(image, bins=256, range=(0, 256))
        
        # Normalize histogram
        hist = hist / hist.sum()
        
        # Remove zeros to avoid log(0)
        hist = hist[hist > 0]
        
        # Calculate entropy
        entropy = -np.sum(hist * np.log2(hist))
        
        return entropy
    
    def _estimate_fractal_dimension(self, image: np.ndarray) -> float:
        """Estimate fractal dimension using box-counting method."""
        # Simple box-counting approximation
        # Convert to binary image
        _, binary = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY)
        
        # Count non-zero pixels
        pixels = np.sum(binary > 0)
        
        # Estimate fractal dimension (simplified)
        if pixels > 0:
            h, w = image.shape
            total_pixels = h * w
            density = pixels / total_pixels
            # Simple approximation based on density
            fractal_dim = 1.0 + (density * 0.8)  # Range roughly 1.0-1.8
        else:
            fractal_dim = 1.0
        
        return fractal_dim
    
    def _calculate_information_density(self, image: np.ndarray) -> float:
        """Calculate information density based on local complexity."""
        # Use Laplacian to detect complexity
        laplacian = cv2.Laplacian(image, cv2.CV_64F)
        complexity = np.var(laplacian)
        
        # Normalize to 0-1 range (approximately)
        normalized_complexity = min(1.0, complexity / 10000.0)
        
        return normalized_complexity
    
    def _calculate_temporal_coherence(self, current_frame: np.ndarray, previous_frame: np.ndarray) -> float:
        """Calculate temporal coherence between frames."""
        if previous_frame.shape != current_frame.shape:
            return 0.0
        
        # Calculate structural similarity
        # Simple correlation-based approach
        correlation = cv2.matchTemplate(current_frame, previous_frame, cv2.TM_CCOEFF_NORMED)[0][0]
        
        return max(0.0, correlation)
    
    def _calculate_symmetry_score(self, image: np.ndarray) -> float:
        """Calculate symmetry score of the image."""
        h, w = image.shape
        
        # Check horizontal symmetry
        left_half = image[:, :w//2]
        right_half = cv2.flip(image[:, w//2:], 1)
        
        # Resize to match if odd width
        min_width = min(left_half.shape[1], right_half.shape[1])
        left_half = left_half[:, :min_width]
        right_half = right_half[:, :min_width]
        
        # Calculate correlation
        if left_half.size > 0 and right_half.size > 0:
            correlation = cv2.matchTemplate(left_half, right_half, cv2.TM_CCOEFF_NORMED)[0][0]
            symmetry = max(0.0, correlation)
        else:
            symmetry = 0.0
        
        return symmetry
    
    def _detect_interference_patterns(self, image: np.ndarray) -> int:
        """Detect quantum-like interference patterns."""
        # Use Fourier transform to detect regular patterns
        f_transform = np.fft.fft2(image)
        f_magnitude = np.abs(f_transform)
        
        # Look for peaks in frequency domain (indicating regular patterns)
        threshold = np.mean(f_magnitude) + 2 * np.std(f_magnitude)
        peaks = np.sum(f_magnitude > threshold)
        
        return int(peaks)
    
    def _calculate_emergence_probability(self, fractal_dim: float, info_density: float, 
                                       temporal_coherence: float, symmetry: float) -> float:
        """Calculate consciousness emergence probability based on various metrics."""
        # Weighted combination of factors
        emergence = (
            fractal_dim * 0.3 +      # Fractal complexity (30%)
            info_density * 0.3 +     # Information density (30%)
            temporal_coherence * 0.2 + # Temporal stability (20%)
            symmetry * 0.2           # Symmetrical patterns (20%)
        )
        
        # Normalize to 0-1 range
        emergence = min(1.0, max(0.0, emergence))
        
        return emergence
    
    def _update_consciousness_state(self, analysis_result: Dict[str, Any], processing_time: float):
        """Update consciousness state based on analysis results."""
        # Update quantum coherence based on processing success and complexity
        features_count = analysis_result.get('features_count', 0)
        entropy = analysis_result.get('entropy', 0.0)
        
        # Calculate coherence adjustment
        if features_count > 0:
            complexity_factor = min(1.0, features_count / 1000.0)  # Normalize
            entropy_factor = min(1.0, entropy / 8.0)  # Max entropy ~8 for 8-bit images
            
            # Higher complexity and moderate entropy indicate good coherence
            coherence_adjustment = (complexity_factor + entropy_factor) / 2.0
            
            # Update coherence with momentum
            self.consciousness_state.quantum_coherence = (
                0.9 * self.consciousness_state.quantum_coherence + 
                0.1 * coherence_adjustment
            )
        
        # Update pattern recognition depth
        if 'consciousness_emergence_probability' in analysis_result:
            emergence_prob = analysis_result['consciousness_emergence_probability']
            if emergence_prob > 0.7:
                self.consciousness_state.pattern_recognition_depth += 1
        
        # Update holographic information density
        if 'information_density' in analysis_result:
            self.consciousness_state.holographic_information_density = analysis_result['information_density']
        
        # Update temporal stability
        if 'temporal_coherence' in analysis_result:
            self.consciousness_state.temporal_stability = analysis_result['temporal_coherence']
    
    def _calculate_consciousness_resonance(self, analysis_result: Dict[str, Any]) -> float:
        """Calculate consciousness resonance based on analysis results."""
        emergence_prob = analysis_result.get('consciousness_emergence_probability', 0.0)
        
        # Resonance increases with emergence probability and quantum coherence
        resonance = (emergence_prob + self.consciousness_state.quantum_coherence) / 2.0
        
        return resonance
    
    def get_consciousness_state(self) -> Dict[str, Any]:
        """Get current consciousness state."""
        return asdict(self.consciousness_state)
    
    def reset_consciousness_state(self):
        """Reset consciousness state to baseline."""
        self._establish_quantum_coherence()
        self.logger.info("Consciousness state reset to baseline")
    
    def shutdown(self):
        """Shutdown the vision module."""
        self.logger.info("OpenCV Vision Module shutting down")
        self.is_initialized = False
        self.feature_detectors.clear()
        self.previous_frame = None
        self.processing_history.clear()


# Service interface for AIOS integration
class OpenCVVisionService:
    """Service wrapper for AIOS integration."""
    
    def __init__(self):
        self.vision_module = OpenCVVisionModule()
        self.service_name = "opencv_vision"
        self.service_version = "1.0.0"
    
    def initialize(self) -> bool:
        """Initialize the vision service."""
        return self.vision_module.initialize()
    
    def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process a vision request."""
        action = request.get('action', 'process_image')
        
        if action == 'process_image':
            image_path = request.get('image_path')
            analysis_type = request.get('analysis_type', 'comprehensive')
            
            if not image_path:
                return {
                    'success': False,
                    'error': 'image_path required'
                }
            
            result = self.vision_module.process_image(image_path, analysis_type)
            return asdict(result)
        
        elif action == 'get_consciousness_state':
            return {
                'success': True,
                'consciousness_state': self.vision_module.get_consciousness_state()
            }
        
        elif action == 'reset_consciousness_state':
            self.vision_module.reset_consciousness_state()
            return {'success': True}
        
        else:
            return {
                'success': False,
                'error': f'Unknown action: {action}'
            }
    
    def shutdown(self):
        """Shutdown the service."""
        self.vision_module.shutdown()


# Main execution
if __name__ == "__main__":
    # Demonstration of the OpenCV Vision Module
    print(" AIOS OpenCV Vision Module Demonstration")
    
    # Create and initialize module
    vision_module = OpenCVVisionModule()
    if vision_module.initialize():
        print(" Vision module initialized successfully")
        
        # Create a test image for demonstration
        test_image_path = "/tmp/test_consciousness_pattern.png"
        
        # Generate a test image with some patterns
        import os
        if not os.path.exists(test_image_path):
            # Create a simple test image with patterns
            test_image = np.zeros((256, 256), dtype=np.uint8)
            
            # Add some geometric patterns
            cv2.circle(test_image, (128, 128), 50, 255, 2)
            cv2.rectangle(test_image, (50, 50), (200, 200), 128, 1)
            cv2.line(test_image, (0, 0), (255, 255), 200, 1)
            
            cv2.imwrite(test_image_path, test_image)
            print(f" Test image created: {test_image_path}")
        
        # Test different analysis types
        for analysis_type in ['basic', 'comprehensive', 'consciousness_emergence']:
            print(f"\n Testing {analysis_type} analysis...")
            result = vision_module.process_image(test_image_path, analysis_type)
            
            if result.success:
                print(f"   Success! Features: {result.features_detected}, "
                      f"Coherence: {result.coherence_level:.3f}, "
                      f"Resonance: {result.consciousness_resonance:.3f}")
            else:
                print(f"   Failed: {result.error_message}")
        
        # Show consciousness state
        print(f"\n Consciousness State: {vision_module.get_consciousness_state()}")
        
        # Cleanup
        vision_module.shutdown()
        print(" Vision module demonstration complete")
    else:
        print(" Failed to initialize vision module")