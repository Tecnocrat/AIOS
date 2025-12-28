
"""
AIOS Runtime Intelligence - Visual Data Bridge
Enhanced with AI Intelligence Engine integration through Cytoplasm communication
Collects visual data and processes it through AI Intelligence for advanced analysis
"""

import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Add AI cytoplasm to path for communication
ai_cytoplasm_path = Path(__file__).parent.parent.parent / "ai" / "cytoplasm"
sys.path.insert(0, str(ai_cytoplasm_path))

try:
    from ui_interaction_bridge import get_ui_bridge
    AI_INTELLIGENCE_AVAILABLE = True
except ImportError:
    AI_INTELLIGENCE_AVAILABLE = False
    print("Warning: AI Intelligence bridge not available, running in data-only mode")


class AIOSVisualIntelligence:
    """
    Runtime Intelligence component enhanced with AI Intelligence engine
    - Collects visual data (Runtime Intelligence function)
    - Processes through AI Intelligence via cytoplasm communication
    - Provides comprehensive analysis results
    """
    
    def __init__(self, aios_root: str = "C:/dev/AIOS"):
        self.aios_root = Path(aios_root)
        self.visual_feedback_dir = self.aios_root / "visual_interface" / "bin" / "Debug" / "net9.0-windows" / "ai_visual_feedback"
        self.state_dir = self.visual_feedback_dir / "state"
        self.screenshots_dir = self.visual_feedback_dir / "screenshots"
        
        # Initialize AI Intelligence connection through cytoplasm
        self.ai_bridge = None
        if AI_INTELLIGENCE_AVAILABLE:
            try:
                self.ai_bridge = get_ui_bridge()
                print(" Runtime Intelligence connected to AI Intelligence via cytoplasm")
            except Exception as e:
                print(f" AI Intelligence connection failed: {e}")
    
    def get_current_visual_state(self) -> Dict:
        """Get visual state data and process through AI Intelligence if available"""
        try:
            # Step 1: Extract raw visual data (Runtime Intelligence function)
            raw_data = self._extract_raw_visual_data()
            
            if raw_data.get("status") != "active":
                return raw_data
            
            # Step 2: Process through AI Intelligence engine via cytoplasm
            if self.ai_bridge:
                enhanced_data = self._process_through_ai_intelligence(raw_data)
                raw_data.update(enhanced_data)
            
            return raw_data
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def _extract_raw_visual_data(self) -> Dict:
        """Extract pure visual data (Runtime Intelligence core function)"""
        # Check if AIOS visual feedback is active
        if not self.state_dir.exists():
            return {"status": "inactive", "message": "AIOS visual feedback not running"}
        
        # Extract pure data without interpretation
        session_info = self._extract_session_data()
        latest_frame = self._extract_latest_frame_data()
        screenshot_activity = self._extract_screenshot_activity()
        objectives = self._extract_ai_objectives()
        
        # Return structured data
        return {
            "timestamp": datetime.now().isoformat(),
            "status": "active",
            "session": session_info,
            "latest_frame": latest_frame,
            "activity_analysis": screenshot_activity,
            "ai_objectives": objectives,
            "extraction_summary": self._generate_extraction_summary(
                session_info, latest_frame, screenshot_activity, objectives
            )
        }
    
    def _process_through_ai_intelligence(self, raw_data: Dict) -> Dict:
        """Process raw visual data through AI Intelligence engine via cytoplasm"""
        try:
            print(" Cytoplasm: Processing visual data through AI Intelligence...")
            
            # Use AI Intelligence visual processing through cytoplasm bridge
            ai_result = self.ai_bridge.execute_ai_function("process_visual_intelligence", {
                "analysis_depth": "enhanced",
                "data": raw_data
            })
            
            # Get consciousness analysis
            consciousness_result = self.ai_bridge.execute_ai_function("analyze_consciousness_patterns", {
                "data": raw_data,
                "temporal_window": 300
            })
            
            # Get enhanced cellular analysis
            enhanced_result = self.ai_bridge.execute_ai_function("enhanced_visual_analysis", {
                "data": raw_data,
                "cellular_integration": True
            })
            
            return {
                "ai_intelligence": {
                    "visual_processing": ai_result,
                    "consciousness_analysis": consciousness_result,
                    "enhanced_analysis": enhanced_result,
                    "processed_by": "cytoplasm_bridge",
                    "processing_timestamp": datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            return {
                "ai_intelligence": {
                    "status": "error",
                    "error": str(e),
                    "fallback_mode": True
                }
            }
    
    def _extract_session_data(self) -> Optional[Dict]:
        """Extract current session data"""
        session_file = self.state_dir / "current_session.json"
        if session_file.exists():
            with open(session_file, 'r') as f:
                return json.load(f)
        return None
    
    def _extract_latest_frame_data(self) -> Optional[Dict]:
        """Extract metadata for the most recent captured frame"""
        metadata_files = list(self.state_dir.glob("frame_*_metadata.json"))
        if not metadata_files:
            return None
        
        # Get the most recent metadata file
        latest_metadata = max(metadata_files, key=lambda x: x.stat().st_mtime)
        
        with open(latest_metadata, 'r') as f:
            return json.load(f)
    
    def _extract_screenshot_activity(self) -> Dict:
        """Extract screenshot capture activity data"""
        if not self.screenshots_dir.exists():
            return {"status": "no_screenshots", "count": 0}
        
        screenshots = list(self.screenshots_dir.glob("*.png"))
        if not screenshots:
            return {"status": "no_screenshots", "count": 0}
        
        # Analyze recent activity (last 5 minutes)
        recent_screenshots = [s for s in screenshots 
                            if (datetime.now().timestamp() - s.stat().st_mtime) < 300]
        
        # Calculate file statistics
        total_size = sum(s.stat().st_size for s in screenshots)
        
        return {
            "status": "active",
            "total_screenshots": len(screenshots),
            "recent_screenshots": len(recent_screenshots),
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "latest_screenshot": max(screenshots, key=lambda x: x.stat().st_mtime).name if screenshots else None,
            "capture_rate": len(recent_screenshots) / 5  # per minute
        }
    
    def _extract_ai_objectives(self) -> Optional[Dict]:
        """Extract AI objectives data"""
        objectives_file = self.state_dir / "ai_objectives.json"
        if objectives_file.exists():
            with open(objectives_file, 'r') as f:
                return json.load(f)
        return None
    
    def _generate_extraction_summary(self, session: Dict, frame: Dict, activity: Dict, objectives: Dict) -> Dict:
        """Generate extraction summary for AI Intelligence processing"""
        return {
            "has_session": session is not None,
            "has_latest_frame": frame is not None,
            "screenshot_activity_level": activity.get("capture_rate", 0),
            "has_objectives": objectives is not None,
            "extraction_quality": self._assess_extraction_quality(session, frame, activity, objectives),
            "ready_for_ai_processing": all([session, frame, activity.get("status") == "active"])
        }
    
    def _assess_extraction_quality(self, session: Dict, frame: Dict, activity: Dict, objectives: Dict) -> str:
        """Assess the quality of extracted data"""
        quality_score = 0
        
        if session:
            quality_score += 25
        if frame:
            quality_score += 25
        if activity.get("status") == "active":
            quality_score += 25
        if objectives:
            quality_score += 25
        
        if quality_score >= 75:
            return "excellent"
        elif quality_score >= 50:
            return "good"
        elif quality_score >= 25:
            return "fair"
        else:
            return "poor"


def main():
    """Main function for standalone testing"""
    print(" AIOS Runtime Intelligence - Visual Data Bridge")
    print("Enhanced with AI Intelligence Engine via Cytoplasm")
    print("=" * 60)
    
    intelligence = AIOSVisualIntelligence()
    
    # Test data extraction and AI processing
    result = intelligence.get_current_visual_state()
    
    print(f"Status: {result.get('status')}")
    print(f"Timestamp: {result.get('timestamp')}")
    
    if result.get("status") == "active":
        print(f"Extraction Quality: {result.get('extraction_summary', {}).get('extraction_quality')}")
        print(f"Ready for AI Processing: {result.get('extraction_summary', {}).get('ready_for_ai_processing')}")
        
        # Show AI Intelligence results if available
        if "ai_intelligence" in result:
            ai_data = result["ai_intelligence"]
            print(f"AI Processing Status: {ai_data.get('visual_processing', {}).get('status', 'unknown')}")
            print(f"Consciousness Analysis: {ai_data.get('consciousness_analysis', {}).get('status', 'unknown')}")
            print(f"Enhanced Analysis: {ai_data.get('enhanced_analysis', {}).get('status', 'unknown')}")
            print(f"Processed By: {ai_data.get('processed_by', 'unknown')}")
    
    print(f"\n Runtime Intelligence → AI Intelligence communication {'active' if intelligence.ai_bridge else 'inactive'}")


if __name__ == "__main__":
    main()
