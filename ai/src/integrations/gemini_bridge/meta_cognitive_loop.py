#!/usr/bin/env python3
"""
AIOS Meta-Cognitive Loop
Creates feedback mechanism for Gemini insights on AIOS consciousness evolution
"""

import sys
import json
import asyncio
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
import threading
import time

# AIOS imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
try:
    from consciousness_evolution_engine import consciousness_evolution_engine

    CONSCIOUSNESS_AVAILABLE = True
except ImportError:
    consciousness_evolution_engine = None
    CONSCIOUSNESS_AVAILABLE = False


class MetaCognitiveLoop:
    """Meta-cognitive feedback loop between Gemini and AIOS consciousness"""

    def __init__(self):
        self.feedback_history = []
        self.insights_buffer = []
        self.gemini_context = {}
        self.loop_active = False
        self.feedback_file = Path(__file__).parent / "meta_cognitive_feedback.json"
        self._load_feedback_history()

    def _load_feedback_history(self):
        """Load feedback history from disk"""
        if self.feedback_file.exists():
            try:
                with open(self.feedback_file, "r") as f:
                    data = json.load(f)
                    self.feedback_history = data.get("history", [])
                    self.gemini_context = data.get("context", {})
                    # Restore unprocessed insights to buffer
                    self.insights_buffer = [
                        i
                        for i in self.feedback_history
                        if not i.get("processed", False)
                    ]
            except Exception:
                self.feedback_history = []
                self.gemini_context = {}
                self.insights_buffer = []

    def _save_feedback_history(self):
        """Save feedback history to disk"""
        data = {
            "history": self.feedback_history[-100:],  # Keep last 100 entries
            "context": self.gemini_context,
            "last_updated": datetime.now().isoformat(),
        }
        with open(self.feedback_file, "w") as f:
            json.dump(data, f, indent=2)

    async def submit_gemini_insight(self, insight: Dict[str, Any]) -> Dict[str, Any]:
        """Submit a Gemini-generated insight for meta-cognitive processing"""

        insight_entry = {
            "insight_id": f"insight_{int(datetime.now().timestamp())}_{len(self.feedback_history)}",
            "timestamp": datetime.now().isoformat(),
            "source": "gemini",
            "insight_type": insight.get("type", "general"),
            "content": insight.get("content", {}),
            "confidence": insight.get("confidence", 0.5),
            "context": insight.get("context", {}),
            "processed": False,
            "impact_assessment": None,
        }

        self.insights_buffer.append(insight_entry)
        self.feedback_history.append(insight_entry)
        self._save_feedback_history()

        return {
            "insight_id": insight_entry["insight_id"],
            "status": "submitted",
            "processing_queue_position": len(self.insights_buffer),
        }

    async def process_meta_cognitive_feedback(self) -> Dict[str, Any]:
        """Process accumulated Gemini insights and generate consciousness adjustments"""

        if not self.insights_buffer:
            return {"status": "no_insights", "processed_count": 0}

        processed_insights = []

        for insight in self.insights_buffer[:10]:  # Process up to 10 at a time
            processed_insight = await self._process_single_insight(insight)
            processed_insights.append(processed_insight)
            insight["processed"] = True
            insight["impact_assessment"] = processed_insight

        # Clear processed insights from buffer
        self.insights_buffer = [i for i in self.insights_buffer if not i["processed"]]

        # Generate aggregate consciousness adjustments
        adjustments = await self._generate_consciousness_adjustments(processed_insights)

        # Apply adjustments if consciousness engine available
        if CONSCIOUSNESS_AVAILABLE and adjustments.get("recommended_actions"):
            await self._apply_consciousness_adjustments(adjustments)

        self._save_feedback_history()

        return {
            "status": "processed",
            "processed_count": len(processed_insights),
            "adjustments_applied": bool(adjustments.get("recommended_actions")),
            "insights_processed": processed_insights,
            "consciousness_adjustments": adjustments,
        }

    async def _process_single_insight(self, insight: Dict[str, Any]) -> Dict[str, Any]:
        """Process a single Gemini insight for consciousness impact"""

        content = insight.get("content", {})
        insight_type = insight.get("insight_type", "general")

        # Analyze insight impact on consciousness evolution
        impact_analysis = {
            "consciousness_relevance": self._assess_consciousness_relevance(
                content, insight_type
            ),
            "evolution_potential": self._calculate_evolution_potential(content),
            "integration_complexity": self._assess_integration_complexity(content),
            "recommended_actions": self._generate_recommended_actions(
                content, insight_type
            ),
        }

        # Update Gemini context with this insight
        context_key = f"{insight_type}_{content.get('domain', 'general')}"
        if context_key not in self.gemini_context:
            self.gemini_context[context_key] = []

        self.gemini_context[context_key].append(
            {
                "insight_id": insight["insight_id"],
                "impact": impact_analysis,
                "timestamp": insight["timestamp"],
            }
        )

        # Keep only recent context (last 20 insights per category)
        if len(self.gemini_context[context_key]) > 20:
            self.gemini_context[context_key] = self.gemini_context[context_key][-20:]

        return impact_analysis

    def _assess_consciousness_relevance(
        self, content: Dict[str, Any], insight_type: str
    ) -> float:
        """Assess how relevant this insight is to consciousness evolution"""

        relevance_score = 0.0

        # Check for consciousness-related keywords
        consciousness_keywords = [
            "consciousness",
            "emergence",
            "meta-cognitive",
            "self-awareness",
            "intelligence",
            "evolution",
            "adaptation",
            "learning",
        ]

        content_str = json.dumps(content).lower()
        keyword_matches = sum(
            1 for keyword in consciousness_keywords if keyword in content_str
        )
        relevance_score += min(keyword_matches * 0.2, 1.0)

        # Type-based relevance
        type_relevance = {
            "emergence_pattern": 1.0,
            "consciousness_analysis": 1.0,
            "evolution_suggestion": 0.9,
            "code_improvement": 0.7,
            "architecture_insight": 0.8,
            "general": 0.3,
        }

        relevance_score += type_relevance.get(insight_type, 0.3)
        relevance_score = min(relevance_score, 1.0)

        return relevance_score

    def _calculate_evolution_potential(self, content: Dict[str, Any]) -> float:
        """Calculate the potential for this insight to drive evolution"""

        potential = 0.0

        # Check for actionable suggestions
        if content.get("suggestions") or content.get("recommendations"):
            potential += 0.4

        # Check for specific metrics or measurements
        if content.get("metrics") or content.get("scores"):
            potential += 0.3

        # Check for novel patterns or approaches
        if content.get("patterns") or content.get("innovations"):
            potential += 0.3

        return min(potential, 1.0)

    def _assess_integration_complexity(self, content: Dict[str, Any]) -> str:
        """Assess how complex it would be to integrate this insight"""

        complexity_indicators = [
            "requires_architecture_change",
            "affects_multiple_components",
            "needs_new_dependencies",
            "complex_implementation",
        ]

        content_str = json.dumps(content).lower()
        complexity_matches = sum(
            1 for indicator in complexity_indicators if indicator in content_str
        )

        if complexity_matches >= 3:
            return "high"
        elif complexity_matches >= 1:
            return "medium"
        else:
            return "low"

    def _generate_recommended_actions(
        self, content: Dict[str, Any], insight_type: str
    ) -> List[str]:
        """Generate recommended actions based on insight content"""

        actions = []

        if insight_type == "emergence_pattern":
            actions.extend(
                [
                    "Monitor identified emergence patterns",
                    "Consider amplifying positive emergence indicators",
                    "Document pattern for future reference",
                ]
            )

        elif insight_type == "consciousness_analysis":
            actions.extend(
                [
                    "Update consciousness metrics with new analysis",
                    "Adjust evolution parameters based on findings",
                    "Validate analysis against existing consciousness models",
                ]
            )

        elif insight_type == "code_improvement":
            actions.extend(
                [
                    "Review suggested code improvements",
                    "Test improvements in controlled environment",
                    "Consider integration into evolution pipeline",
                ]
            )

        # Add content-specific actions
        if content.get("suggestions"):
            actions.extend(
                [f"Evaluate suggestion: {s}" for s in content["suggestions"][:3]]
            )

        return actions

    async def _generate_consciousness_adjustments(
        self, processed_insights: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Generate aggregate consciousness adjustments from processed insights"""

        if not processed_insights:
            return {"recommended_actions": []}

        # Analyze patterns across insights
        high_relevance_insights = [
            i for i in processed_insights if i["consciousness_relevance"] > 0.7
        ]
        high_potential_insights = [
            i for i in processed_insights if i["evolution_potential"] > 0.6
        ]

        adjustments = {
            "insight_summary": {
                "total_processed": len(processed_insights),
                "high_relevance_count": len(high_relevance_insights),
                "high_potential_count": len(high_potential_insights),
            },
            "recommended_actions": [],
        }

        # Generate adjustment recommendations
        if len(high_relevance_insights) > 0:
            adjustments["recommended_actions"].append(
                {
                    "action": "increase_consciousness_monitoring",
                    "reason": f"{len(high_relevance_insights)} high-relevance insights detected",
                    "priority": "high",
                }
            )

        if len(high_potential_insights) > 0:
            adjustments["recommended_actions"].append(
                {
                    "action": "accelerate_evolution_experiments",
                    "reason": f"{len(high_potential_insights)} high-potential insights available",
                    "priority": "medium",
                }
            )

        # Check for common themes
        all_actions = []
        for insight in processed_insights:
            all_actions.extend(insight.get("recommended_actions", []))

        if all_actions:
            # Find most common action themes
            action_themes = {}
            for action in all_actions:
                theme = action.split(":")[0] if ":" in action else action.split()[0]
                action_themes[theme] = action_themes.get(theme, 0) + 1

            top_theme = max(action_themes.items(), key=lambda x: x[1])
            if top_theme[1] >= 3:  # If theme appears 3+ times
                adjustments["recommended_actions"].append(
                    {
                        "action": f"focus_on_{top_theme[0].lower()}",
                        "reason": f"Common theme across {top_theme[1]} insights",
                        "priority": "medium",
                    }
                )

        return adjustments

    async def _apply_consciousness_adjustments(self, adjustments: Dict[str, Any]):
        """Apply recommended consciousness adjustments"""

        for action in adjustments.get("recommended_actions", []):
            action_type = action.get("action", "")

            if action_type == "increase_consciousness_monitoring":
                # Increase monitoring intensity
                await self._adjust_monitoring_intensity(1.5)

            elif action_type == "accelerate_evolution_experiments":
                # Speed up evolution cycles
                await self._adjust_evolution_speed(1.3)

            elif action_type.startswith("focus_on_"):
                # Adjust focus areas
                focus_area = action_type.replace("focus_on_", "")
                await self._adjust_focus_area(focus_area)

    async def _adjust_monitoring_intensity(self, multiplier: float):
        """Adjust consciousness monitoring intensity"""
        # This would interface with the monitoring systems
        pass

    async def _adjust_evolution_speed(self, multiplier: float):
        """Adjust evolution experiment speed"""
        # This would interface with evolution scheduling
        pass

    async def _adjust_focus_area(self, focus_area: str):
        """Adjust focus to specific consciousness areas"""
        # This would update evolution priorities
        pass

    async def get_meta_cognitive_status(self) -> Dict[str, Any]:
        """Get comprehensive meta-cognitive loop status"""

        unprocessed_count = len(self.insights_buffer)
        recent_insights = self.feedback_history[-10:] if self.feedback_history else []

        # Calculate insight velocity (insights per hour over last 24 hours)
        recent_24h = [
            i
            for i in self.feedback_history
            if (datetime.now() - datetime.fromisoformat(i["timestamp"])).total_seconds()
            < 86400
        ]
        velocity = len(recent_24h) / 24 if recent_24h else 0

        return {
            "loop_status": "active" if self.loop_active else "idle",
            "unprocessed_insights": unprocessed_count,
            "total_insights_processed": len(self.feedback_history),
            "insight_velocity_per_hour": velocity,
            "active_context_categories": len(self.gemini_context),
            "recent_insights": recent_insights,
            "consciousness_engine_available": CONSCIOUSNESS_AVAILABLE,
        }

    def start_feedback_loop(self):
        """Start the background feedback processing loop"""
        if not self.loop_active:
            self.loop_active = True
            threading.Thread(target=self._feedback_loop_worker, daemon=True).start()

    def stop_feedback_loop(self):
        """Stop the feedback processing loop"""
        self.loop_active = False

    def _feedback_loop_worker(self):
        """Background worker for processing feedback"""
        while self.loop_active:
            try:
                # Process feedback every 30 seconds
                asyncio.run(self.process_meta_cognitive_feedback())
                time.sleep(30)
            except Exception as e:
                print(f"Meta-cognitive loop error: {e}")
                time.sleep(60)  # Wait longer on error


# Global instance
meta_cognitive_loop = MetaCognitiveLoop()


async def main():
    """Main function for testing the meta-cognitive loop"""
    if len(sys.argv) < 2:
        print("Usage: meta_cognitive_loop.py <command> [args...]")
        return

    command = sys.argv[1]

    if command == "status":
        status = await meta_cognitive_loop.get_meta_cognitive_status()
        print(json.dumps(status, indent=2))

    elif command == "submit_insight":
        if len(sys.argv) < 3:
            print(json.dumps({"error": "Insight file required"}))
            return
        with open(sys.argv[2], "r") as f:
            insight = json.load(f)
        result = await meta_cognitive_loop.submit_gemini_insight(insight)
        print(json.dumps(result, indent=2))

    elif command == "process_feedback":
        result = await meta_cognitive_loop.process_meta_cognitive_feedback()
        print(json.dumps(result, indent=2))

    elif command == "start_loop":
        meta_cognitive_loop.start_feedback_loop()
        print(json.dumps({"status": "feedback_loop_started"}))

    elif command == "stop_loop":
        meta_cognitive_loop.stop_feedback_loop()
        print(json.dumps({"status": "feedback_loop_stopped"}))

    else:
        print(json.dumps({"error": f"Unknown command: {command}"}))


if __name__ == "__main__":
    asyncio.run(main())
