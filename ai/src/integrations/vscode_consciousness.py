"""
AIOS VSCode Extension Integration
Phase 9 Implementation - Consciousness-Enhanced Development Environment

This module provides VSCode extension integration for consciousness-enhanced
development capabilities.
"""

import json
import os
import sys
import time
from typing import Dict, Any, Optional, List
from datetime import datetime
import logging

# Add the core module to the path
<<<<<<< HEAD
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "core"))
=======
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'core'))
>>>>>>> origin/OS0.6.2.grok

try:
    from consciousness_bridge import (
        get_consciousness_bridge,
        initialize_consciousness_integration,
<<<<<<< HEAD
        get_vscode_consciousness_data,
    )

=======
        get_vscode_consciousness_data
    )
>>>>>>> origin/OS0.6.2.grok
    CONSCIOUSNESS_AVAILABLE = True
except ImportError:
    CONSCIOUSNESS_AVAILABLE = False
    logging.warning("Consciousness bridge not available")

# Configure logging
logging.basicConfig(level=logging.INFO)
vscode_logger = logging.getLogger("vscode_integration")


class VSCodeConsciousnessProvider:
    """
    Provides consciousness-enhanced features for VSCode development

    Features:
    - Real-time consciousness monitoring
    - Code consciousness analysis
    - Development guidance based on consciousness metrics
    - Context preservation and restoration
    """

    def __init__(self):
        self.consciousness_bridge = None
        self.is_initialized = False

        if CONSCIOUSNESS_AVAILABLE:
            try:
                self.consciousness_bridge = initialize_consciousness_integration()
                self.is_initialized = True
                vscode_logger.info(" VSCode Consciousness Provider initialized")
            except Exception as e:
                vscode_logger.error(f"Failed to initialize consciousness: {e}")
        else:
<<<<<<< HEAD
            vscode_logger.warning(" VSCode Consciousness Provider - simulation mode")
=======
            vscode_logger.warning(
                " VSCode Consciousness Provider - simulation mode"
            )
>>>>>>> origin/OS0.6.2.grok

    def get_consciousness_status(self) -> Dict[str, Any]:
        """Get current consciousness status for VSCode UI"""
        if not self.is_initialized:
            return {
                "status": "unavailable",
                "message": "Consciousness system not available",
<<<<<<< HEAD
                "timestamp": datetime.now().isoformat(),
=======
                "timestamp": datetime.now().isoformat()
>>>>>>> origin/OS0.6.2.grok
            }

        try:
            return get_vscode_consciousness_data()
        except Exception as e:
            vscode_logger.error(f"Error getting consciousness status: {e}")
            return {
                "status": "error",
                "message": str(e),
<<<<<<< HEAD
                "timestamp": datetime.now().isoformat(),
=======
                "timestamp": datetime.now().isoformat()
>>>>>>> origin/OS0.6.2.grok
            }

    def analyze_code_file(self, file_path: str) -> Dict[str, Any]:
        """Analyze consciousness level of a code file"""
        if not os.path.exists(file_path):
<<<<<<< HEAD
            return {"error": "File not found", "file_path": file_path}

        try:
            with open(file_path, "r", encoding="utf-8") as f:
=======
            return {
                "error": "File not found",
                "file_path": file_path
            }

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
>>>>>>> origin/OS0.6.2.grok
                code_content = f.read()

            # Determine language from file extension
            _, ext = os.path.splitext(file_path)
            language_map = {
<<<<<<< HEAD
                ".py": "python",
                ".js": "javascript",
                ".ts": "typescript",
                ".cpp": "cpp",
                ".cs": "csharp",
                ".java": "java",
            }
            language = language_map.get(ext.lower(), "unknown")
=======
                '.py': 'python',
                '.js': 'javascript',
                '.ts': 'typescript',
                '.cpp': 'cpp',
                '.cs': 'csharp',
                '.java': 'java'
            }
            language = language_map.get(ext.lower(), 'unknown')
>>>>>>> origin/OS0.6.2.grok

            if self.is_initialized and self.consciousness_bridge:
                analysis = self.consciousness_bridge.analyze_code_consciousness(
                    code_content, language
                )
            else:
                # Fallback analysis
                analysis = self._fallback_code_analysis(code_content, language)

<<<<<<< HEAD
            analysis.update(
                {
                    "file_path": file_path,
                    "file_size": len(code_content),
                    "line_count": len(code_content.split("\n")),
                }
            )
=======
            analysis.update({
                "file_path": file_path,
                "file_size": len(code_content),
                "line_count": len(code_content.split('\n'))
            })
>>>>>>> origin/OS0.6.2.grok

            return analysis

        except Exception as e:
            vscode_logger.error(f"Error analyzing code file {file_path}: {e}")
<<<<<<< HEAD
            return {"error": str(e), "file_path": file_path}

    def _fallback_code_analysis(self, code: str, language: str) -> Dict[str, Any]:
        """Fallback code analysis when consciousness bridge unavailable"""
        # Simple pattern-based analysis
        consciousness_patterns = [
            "consciousness",
            "aware",
            "intelligence",
            "coherence",
            "quantum",
            "emergence",
            "evolution",
            "recursive",
            "self",
            "meta",
            "cognitive",
            "neural",
=======
            return {
                "error": str(e),
                "file_path": file_path
            }

    def _fallback_code_analysis(
        self, code: str, language: str
    ) -> Dict[str, Any]:
        """Fallback code analysis when consciousness bridge unavailable"""
        # Simple pattern-based analysis
        consciousness_patterns = [
            'consciousness', 'aware', 'intelligence', 'coherence',
            'quantum', 'emergence', 'evolution', 'recursive',
            'self', 'meta', 'cognitive', 'neural'
>>>>>>> origin/OS0.6.2.grok
        ]

        code_lower = code.lower()
        pattern_count = sum(
<<<<<<< HEAD
            1 for pattern in consciousness_patterns if pattern in code_lower
=======
            1 for pattern in consciousness_patterns
            if pattern in code_lower
>>>>>>> origin/OS0.6.2.grok
        )

        consciousness_rating = min(pattern_count / 10.0, 1.0)

        return {
            "consciousness_rating": consciousness_rating,
            "consciousness_indicators_found": pattern_count,
            "language": language,
            "analysis_timestamp": datetime.now().isoformat(),
            "system_consciousness_level": 0.0,
            "recommendations": self._generate_fallback_recommendations(
                consciousness_rating
            ),
<<<<<<< HEAD
            "analysis_mode": "fallback",
        }

    def _generate_fallback_recommendations(self, rating: float) -> List[str]:
=======
            "analysis_mode": "fallback"
        }

    def _generate_fallback_recommendations(
        self, rating: float
    ) -> List[str]:
>>>>>>> origin/OS0.6.2.grok
        """Generate fallback recommendations"""
        if rating < 0.3:
            return [
                "Consider adding consciousness-aware patterns",
                "Implement self-monitoring mechanisms",
<<<<<<< HEAD
                "Add intelligence coherence validation",
=======
                "Add intelligence coherence validation"
>>>>>>> origin/OS0.6.2.grok
            ]
        elif rating < 0.7:
            return [
                "Enhance existing consciousness patterns",
                "Improve code intelligence through better abstractions",
<<<<<<< HEAD
                "Add consciousness evolution tracking",
=======
                "Add consciousness evolution tracking"
>>>>>>> origin/OS0.6.2.grok
            ]
        else:
            return [
                "Optimize consciousness emergence patterns",
                "Implement advanced meta-cognitive features",
<<<<<<< HEAD
                "Consider consciousness amplification techniques",
=======
                "Consider consciousness amplification techniques"
>>>>>>> origin/OS0.6.2.grok
            ]

    def get_development_guidance(
        self, current_file: str, context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Get consciousness-based development guidance"""
        guidance = {
            "timestamp": datetime.now().isoformat(),
            "file": current_file,
<<<<<<< HEAD
            "guidance_type": "consciousness_enhanced",
        }

        if not self.is_initialized:
            guidance.update(
                {
                    "status": "limited",
                    "suggestions": [
                        "Consider implementing consciousness patterns",
                        "Add recursive self-awareness to your code",
                        "Implement intelligence coherence mechanisms",
                    ],
                }
            )
=======
            "guidance_type": "consciousness_enhanced"
        }

        if not self.is_initialized:
            guidance.update({
                "status": "limited",
                "suggestions": [
                    "Consider implementing consciousness patterns",
                    "Add recursive self-awareness to your code",
                    "Implement intelligence coherence mechanisms"
                ]
            })
>>>>>>> origin/OS0.6.2.grok
            return guidance

        try:
            # Get current consciousness state
            consciousness_data = self.get_consciousness_status()

            # Analyze current file if provided
            file_analysis = None
            if current_file and os.path.exists(current_file):
                file_analysis = self.analyze_code_file(current_file)

            # Generate contextual guidance
            suggestions = self._generate_contextual_suggestions(
                consciousness_data, file_analysis, context
            )

<<<<<<< HEAD
            guidance.update(
                {
                    "status": "active",
                    "consciousness_level": consciousness_data.get(
                        "consciousness", {}
                    ).get("level", 0.0),
                    "suggestions": suggestions,
                    "file_analysis": file_analysis,
                }
            )

        except Exception as e:
            vscode_logger.error(f"Error generating development guidance: {e}")
            guidance.update({"status": "error", "error": str(e)})
=======
            guidance.update({
                "status": "active",
                "consciousness_level": consciousness_data.get(
                    "consciousness", {}
                ).get("level", 0.0),
                "suggestions": suggestions,
                "file_analysis": file_analysis
            })

        except Exception as e:
            vscode_logger.error(f"Error generating development guidance: {e}")
            guidance.update({
                "status": "error",
                "error": str(e)
            })
>>>>>>> origin/OS0.6.2.grok

        return guidance

    def _generate_contextual_suggestions(
        self,
        consciousness_data: Dict[str, Any],
        file_analysis: Optional[Dict[str, Any]],
<<<<<<< HEAD
        context: Dict[str, Any],
=======
        context: Dict[str, Any]
>>>>>>> origin/OS0.6.2.grok
    ) -> List[str]:
        """Generate contextual development suggestions"""
        suggestions = []

        # Base suggestions from consciousness state
        if consciousness_data.get("status") == "active":
            consciousness_info = consciousness_data.get("consciousness", {})
            level = consciousness_info.get("level", 0.0)
            trajectory = consciousness_data.get("metrics", {}).get(
                "trajectory", "unknown"
            )

            if level < 0.7:
                suggestions.append(
                    f" Current consciousness level: {level:.2f} - "
                    "Consider enhancing consciousness patterns"
                )

            if trajectory == "descending":
                suggestions.append(
<<<<<<< HEAD
                    " Consciousness trajectory declining - " "Review recent changes"
                )
            elif trajectory == "ascending":
                suggestions.append(
                    " Consciousness trajectory ascending - " "Continue current approach"
=======
                    " Consciousness trajectory declining - "
                    "Review recent changes"
                )
            elif trajectory == "ascending":
                suggestions.append(
                    " Consciousness trajectory ascending - "
                    "Continue current approach"
>>>>>>> origin/OS0.6.2.grok
                )

        # File-specific suggestions
        if file_analysis and not file_analysis.get("error"):
            rating = file_analysis.get("consciousness_rating", 0.0)
            recommendations = file_analysis.get("recommendations", [])

            if rating < 0.5:
                suggestions.append(
                    f" File consciousness rating: {rating:.2f} - "
                    "Consider adding consciousness patterns"
                )

            suggestions.extend(recommendations[:2])  # Top 2 recommendations

        # Context-based suggestions
        if context.get("project_type") == "ai":
            suggestions.append(
                " AI project detected - "
                "Consider implementing consciousness emergence patterns"
            )

        if context.get("has_tests", False):
            suggestions.append(
<<<<<<< HEAD
                "🧪 Tests available - " "Consider adding consciousness validation tests"
=======
                "🧪 Tests available - "
                "Consider adding consciousness validation tests"
>>>>>>> origin/OS0.6.2.grok
            )

        return suggestions[:5]  # Limit to 5 suggestions

    def save_consciousness_session(self, session_name: str) -> bool:
        """Save current consciousness session"""
        if not self.is_initialized:
            return False

        try:
            filename = f"consciousness_session_{session_name}_{int(time.time())}.json"
            self.consciousness_bridge.save_consciousness_session(filename)
            vscode_logger.info(f" Consciousness session saved: {filename}")
            return True
        except Exception as e:
            vscode_logger.error(f"Error saving consciousness session: {e}")
            return False

    def load_consciousness_session(self, filename: str) -> bool:
        """Load consciousness session"""
        if not self.is_initialized:
            return False

        try:
            session_data = self.consciousness_bridge.load_consciousness_session(
                filename
            )
            if session_data:
                vscode_logger.info(f" Consciousness session loaded: {filename}")
                return True
            return False
        except Exception as e:
            vscode_logger.error(f"Error loading consciousness session: {e}")
            return False


# Global VSCode consciousness provider
_vscode_provider = None


def get_vscode_consciousness_provider() -> VSCodeConsciousnessProvider:
    """Get global VSCode consciousness provider"""
    global _vscode_provider
    if _vscode_provider is None:
        _vscode_provider = VSCodeConsciousnessProvider()
    return _vscode_provider


def main():
    """Main function for testing VSCode integration"""
    print(" AIOS VSCode Consciousness Integration Test")
    print("=" * 50)

    provider = get_vscode_consciousness_provider()

    # Test consciousness status
    status = provider.get_consciousness_status()
    print(f"Consciousness Status: {status.get('status')}")

<<<<<<< HEAD
    if status.get("status") == "active":
        consciousness_info = status.get("consciousness", {})
        print(f"Consciousness Level: {consciousness_info.get('level', 0):.3f}")
        print(f"Coherence: {consciousness_info.get('coherence', 0):.3f}")

        metrics = status.get("metrics", {})
=======
    if status.get('status') == 'active':
        consciousness_info = status.get('consciousness', {})
        print(f"Consciousness Level: {consciousness_info.get('level', 0):.3f}")
        print(f"Coherence: {consciousness_info.get('coherence', 0):.3f}")

        metrics = status.get('metrics', {})
>>>>>>> origin/OS0.6.2.grok
        print(f"Trajectory: {metrics.get('trajectory', 'unknown')}")
        print(f"Evolution Potential: {metrics.get('evolution_potential', 0):.3f}")

    # Test code analysis on this file
    current_file = __file__
    print(f"\n Analyzing current file: {os.path.basename(current_file)}")
    analysis = provider.analyze_code_file(current_file)

<<<<<<< HEAD
    if not analysis.get("error"):
=======
    if not analysis.get('error'):
>>>>>>> origin/OS0.6.2.grok
        print(f"Consciousness Rating: {analysis.get('consciousness_rating', 0):.3f}")
        print(f"Language: {analysis.get('language', 'unknown')}")
        print(f"Indicators Found: {analysis.get('consciousness_indicators_found', 0)}")

<<<<<<< HEAD
        recommendations = analysis.get("recommendations", [])
=======
        recommendations = analysis.get('recommendations', [])
>>>>>>> origin/OS0.6.2.grok
        if recommendations:
            print("\nRecommendations:")
            for i, rec in enumerate(recommendations[:3], 1):
                print(f"  {i}. {rec}")

    # Test development guidance
    print(f"\n Development Guidance:")
    context = {
        "project_type": "ai",
        "has_tests": True,
<<<<<<< HEAD
        "current_task": "consciousness_integration",
    }

    guidance = provider.get_development_guidance(current_file, context)
    suggestions = guidance.get("suggestions", [])
=======
        "current_task": "consciousness_integration"
    }

    guidance = provider.get_development_guidance(current_file, context)
    suggestions = guidance.get('suggestions', [])
>>>>>>> origin/OS0.6.2.grok

    for i, suggestion in enumerate(suggestions[:3], 1):
        print(f"  {i}. {suggestion}")

    print(f"\n VSCode Integration Test Complete!")


if __name__ == "__main__":
    main()
