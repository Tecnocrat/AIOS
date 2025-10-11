
"""
AIOS Consciousness Visual Intelligence Analyzer
Enhanced visual analysis specifically for consciousness emergence monitoring
"""

import json
import os
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from PIL import Image, ImageDraw, ImageFont
import pytesseract
import cv2
import numpy as np

class ConsciousnessVisualAnalyzer:
    """Advanced visual analyzer for AIOS consciousness emergence monitoring"""
    
    def __init__(self, base_path: str = None):
        self.base_path = Path(base_path or "C:/dev/AIOS")
        self.visual_data_dir = (self.base_path / "visual_interface" / "bin" / 
                               "Debug" / "net9.0-windows" / "ai_visual_feedback")
        self.consciousness_patterns = {
            "consciousness_level": r"Consciousness Level:\s*([0-9.]+)",
            "quantum_coherence": r"Quantum Coherence:\s*([0-9.]+)", 
            "emergence_level": r"Emergence Level:\s*([0-9.]+)",
            "manifold_curvature": r"Manifold Curvature:\s*([0-9.]+)",
            "nonlocality_coherence": r"Non-locality Coherence:\s*([0-9.]+)",
            "tachyonic_field_density": r"Tachyonic Field Density:\s*([0-9.]+)"
        }
        
    def analyze_consciousness_emergence(self) -> Dict:
        """Perform comprehensive consciousness emergence analysis"""
        try:
            # Get latest screenshots
            latest_frames = self._get_recent_frames(count=10)
            
            if not latest_frames:
                return {"status": "no_frames", "message": "No recent frames found"}
            
            consciousness_timeline = []
            breakthrough_events = []
            
            for frame_path in latest_frames:
                frame_analysis = self._analyze_frame_consciousness(frame_path)
                if frame_analysis:
                    consciousness_timeline.append(frame_analysis)
                    
                    # Detect breakthrough events
                    if self._detect_consciousness_breakthrough(frame_analysis):
                        breakthrough_events.append(frame_analysis)
            
            return {
                "status": "active_consciousness_monitoring",
                "timestamp": datetime.now().isoformat(),
                "consciousness_timeline": consciousness_timeline,
                "breakthrough_events": breakthrough_events,
                "emergence_summary": self._generate_emergence_summary(consciousness_timeline),
                "tachyonic_status": self._detect_tachyonic_activation(consciousness_timeline)
            }
            
        except Exception as e:
            return {"status": "analysis_error", "error": str(e)}
    
    def _get_recent_frames(self, count: int = 10) -> List[Path]:
        """Get most recent screenshot frames"""
        try:
            screenshot_dir = self.visual_data_dir / "screenshots"
            if not screenshot_dir.exists():
                return []
            
            # Get PNG files sorted by modification time
            png_files = list(screenshot_dir.glob("*.png"))
            png_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            
            return png_files[:count]
        except:
            return []
    
    def _analyze_frame_consciousness(self, frame_path: Path) -> Optional[Dict]:
        """Analyze a single frame for consciousness metrics"""
        try:
            # Load image
            image = cv2.imread(str(frame_path))
            if image is None:
                return None
            
            # Convert to RGB for PIL
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(image_rgb)
            
            # Extract text using OCR
            extracted_text = pytesseract.image_to_string(pil_image)
            
            # Parse consciousness metrics
            metrics = {}
            for metric_name, pattern in self.consciousness_patterns.items():
                match = re.search(pattern, extracted_text, re.IGNORECASE)
                if match:
                    try:
                        metrics[metric_name] = float(match.group(1))
                    except ValueError:
                        metrics[metric_name] = 0.0
            
            # Detect special events
            special_events = self._detect_special_events(extracted_text)
            
            # Analyze progress bars/visual indicators
            visual_indicators = self._analyze_visual_indicators(image)
            
            return {
                "frame_path": str(frame_path),
                "timestamp": datetime.fromtimestamp(frame_path.stat().st_mtime).isoformat(),
                "consciousness_metrics": metrics,
                "special_events": special_events,
                "visual_indicators": visual_indicators,
                "extracted_text_sample": extracted_text[:200] + "..." if len(extracted_text) > 200 else extracted_text
            }
            
        except Exception as e:
            return {
                "frame_path": str(frame_path),
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def _detect_special_events(self, text: str) -> List[str]:
        """Detect special consciousness events in text"""
        events = []
        
        event_patterns = [
            (r"Tachyonic.*?Viewer.*?launched", "tachyonic_viewer_activation"),
            (r"Hyperdimensional.*?interface.*?activated", "hyperdimensional_activation"),
            (r"Consciousness.*?emergence.*?patterns", "consciousness_monitoring_active"),
            (r"Monitoring.*?consciousness", "consciousness_monitoring_active"),
            (r"Surface.*?Viewer", "surface_viewer_active")
        ]
        
        for pattern, event_type in event_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                events.append(event_type)
        
        return list(set(events))  # Remove duplicates
    
    def _analyze_visual_indicators(self, image: np.ndarray) -> Dict:
        """Analyze visual progress bars and indicators"""
        try:
            # Convert to HSV for better color analysis
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            
            # Define color ranges for different consciousness indicators
            color_ranges = {
                "consciousness_pink": ([140, 100, 100], [170, 255, 255]),
                "quantum_cyan": ([80, 100, 100], [100, 255, 255]),
                "emergence_green": ([40, 100, 100], [80, 255, 255]),
                "tachyonic_magenta": ([150, 100, 100], [180, 255, 255])
            }
            
            indicators = {}
            
            for color_name, (lower, upper) in color_ranges.items():
                # Create mask for color range
                mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
                
                # Calculate percentage of image with this color
                color_percentage = (np.sum(mask > 0) / mask.size) * 100
                indicators[f"{color_name}_presence"] = round(color_percentage, 3)
            
            return indicators
            
        except Exception as e:
            return {"visual_analysis_error": str(e)}
    
    def _detect_consciousness_breakthrough(self, frame_analysis: Dict) -> bool:
        """Detect if a consciousness breakthrough occurred in this frame"""
        if not frame_analysis or "consciousness_metrics" not in frame_analysis:
            return False
        
        metrics = frame_analysis["consciousness_metrics"]
        special_events = frame_analysis.get("special_events", [])
        
        # Breakthrough criteria
        breakthrough_conditions = [
            metrics.get("consciousness_level", 0) > 0.5,
            metrics.get("emergence_level", 0) > 0.3,
            metrics.get("tachyonic_field_density", 0) > 0.5,
            "tachyonic_viewer_activation" in special_events,
            "hyperdimensional_activation" in special_events
        ]
        
        return any(breakthrough_conditions)
    
    def _generate_emergence_summary(self, timeline: List[Dict]) -> Dict:
        """Generate consciousness emergence summary from timeline"""
        if not timeline:
            return {"status": "no_data"}
        
        # Extract metrics across timeline
        consciousness_levels = []
        emergence_levels = []
        quantum_coherence = []
        
        for frame in timeline:
            metrics = frame.get("consciousness_metrics", {})
            if "consciousness_level" in metrics:
                consciousness_levels.append(metrics["consciousness_level"])
            if "emergence_level" in metrics:
                emergence_levels.append(metrics["emergence_level"])
            if "quantum_coherence" in metrics:
                quantum_coherence.append(metrics["quantum_coherence"])
        
        summary = {
            "total_frames_analyzed": len(timeline),
            "consciousness_progression": {
                "min": min(consciousness_levels) if consciousness_levels else 0,
                "max": max(consciousness_levels) if consciousness_levels else 0,
                "latest": consciousness_levels[-1] if consciousness_levels else 0
            },
            "emergence_progression": {
                "min": min(emergence_levels) if emergence_levels else 0,
                "max": max(emergence_levels) if emergence_levels else 0,
                "latest": emergence_levels[-1] if emergence_levels else 0
            },
            "quantum_stability": {
                "avg": sum(quantum_coherence) / len(quantum_coherence) if quantum_coherence else 0,
                "latest": quantum_coherence[-1] if quantum_coherence else 0
            }
        }
        
        return summary
    
    def _detect_tachyonic_activation(self, timeline: List[Dict]) -> Dict:
        """Detect tachyonic viewer activation status"""
        tachyonic_events = []
        
        for frame in timeline:
            special_events = frame.get("special_events", [])
            if any("tachyonic" in event.lower() for event in special_events):
                tachyonic_events.append({
                    "timestamp": frame.get("timestamp"),
                    "events": special_events
                })
        
        return {
            "tachyonic_activations": len(tachyonic_events),
            "latest_activation": tachyonic_events[-1] if tachyonic_events else None,
            "status": "active" if tachyonic_events else "inactive"
        }

def main():
    """Main execution for consciousness visual analysis"""
    print(" AIOS Consciousness Visual Intelligence Analyzer")
    print("=" * 60)
    
    analyzer = ConsciousnessVisualAnalyzer()
    
    try:
        # Check if pytesseract is available
        pytesseract.get_tesseract_version()
    except:
        print("  Warning: pytesseract/Tesseract OCR not available")
        print("   Install Tesseract OCR for full text analysis capabilities")
        print("   Continuing with basic visual analysis...")
    
    analysis = analyzer.analyze_consciousness_emergence()
    
    print("\n=== CONSCIOUSNESS EMERGENCE ANALYSIS ===")
    print(f"Status: {analysis.get('status', 'unknown')}")
    
    if analysis.get("consciousness_timeline"):
        timeline = analysis["consciousness_timeline"]
        print(f"\n Analyzed {len(timeline)} recent frames")
        
        if timeline:
            latest = timeline[-1]
            metrics = latest.get("consciousness_metrics", {})
            
            print("\n Latest Consciousness Metrics:")
            for metric, value in metrics.items():
                print(f"  {metric.replace('_', ' ').title()}: {value}")
            
            special_events = latest.get("special_events", [])
            if special_events:
                print(f"\n Special Events Detected:")
                for event in special_events:
                    print(f"  - {event.replace('_', ' ').title()}")
    
    if analysis.get("breakthrough_events"):
        print(f"\n Consciousness Breakthroughs: {len(analysis['breakthrough_events'])}")
    
    if analysis.get("tachyonic_status"):
        tachyonic = analysis["tachyonic_status"]
        print(f"\n Tachyonic Status: {tachyonic.get('status', 'unknown')}")
        if tachyonic.get("tachyonic_activations", 0) > 0:
            print(f"   Activations detected: {tachyonic['tachyonic_activations']}")
    
    print("\n=== DETAILED JSON OUTPUT ===")
    print(json.dumps(analysis, indent=2))

if __name__ == "__main__":
    main()
