
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
                )
            }
            
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
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
        avg_size = total_size / len(screenshots) if screenshots else 0
        
        return {
            "status": "active",
            "total_screenshots": len(screenshots),
            "recent_screenshots": len(recent_screenshots),
            "avg_file_size": avg_size,
            "total_size_mb": total_size / (1024 * 1024),
            "activity_level": (
                "high" if len(recent_screenshots) > 10
                else "moderate" if len(recent_screenshots) > 0
                else "low"
            )
        }
    
    def _extract_ai_objectives(self) -> List[Dict]:
        """Extract current AI objectives data"""
        objectives = []
        objective_files = list(self.state_dir.glob("objective_*.json"))
        
        for obj_file in objective_files:
            try:
                with open(obj_file, 'r') as f:
                    objectives.append(json.load(f))
            except:
                continue
        
        return objectives
    
    def _generate_extraction_summary(self, session: Optional[Dict], frame: Optional[Dict], 
                                   activity: Dict, objectives: List[Dict]) -> str:
        """Generate summary of extracted data for Runtime Intelligence logs"""
        summary_parts = []
        
        # Session extraction status
        if session:
            summary_parts.append(f"Session Data: Extracted {session.get('SessionId', 'Unknown')[:8]}...")
            summary_parts.append(f"Purpose: {session.get('Purpose', 'Unknown')}")
        else:
            summary_parts.append("Session Data: No active session")
        
        # Frame extraction status
        if frame:
            summary_parts.append(f"Frame Data: Frame {frame.get('FrameNumber', 0)} extracted")
            summary_parts.append(f"Resolution: {frame.get('Resolution', {}).get('Width', 0)}x{frame.get('Resolution', {}).get('Height', 0)}")
        else:
            summary_parts.append("Frame Data: No frame data available")
        
        # Activity extraction status
        activity_status = activity.get('status', 'unknown')
        if activity_status == 'active':
            summary_parts.append(f"Activity Data: {activity['total_screenshots']} screenshots, {activity['total_size_mb']:.1f} MB")
        else:
            summary_parts.append("Activity Data: No screenshot activity")
        
        # Objectives extraction status
        summary_parts.append(f"Objectives Data: {len(objectives)} objectives extracted")
        
        return "\n".join(summary_parts)

def main():
    """Main function for Runtime Intelligence visual data extraction"""
    intelligence = AIOSVisualIntelligence()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--json":
        # JSON output for AI Intelligence consumption
        state = intelligence.get_current_visual_state()
        print(json.dumps(state, indent=2))
    else:
        # Human-readable output for Runtime Intelligence monitoring
        state = intelligence.get_current_visual_state()
        if state.get("status") == "active":
            print("=== RUNTIME INTELLIGENCE VISUAL DATA EXTRACTION ===")
            print(state["extraction_summary"])
            print("\n=== RAW DATA FOR AI INTELLIGENCE ===")
            print(json.dumps(state, indent=2))
        else:
            print(f"Runtime Intelligence Visual Status: {state.get('status')}")
            print(f"Message: {state.get('message', 'No additional information')}")

if __name__ == "__main__":
    main()
