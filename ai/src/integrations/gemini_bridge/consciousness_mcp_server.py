#!/usr/bin/env python3
"""
AIOS Consciousness MCP Server
Provides consciousness analysis and emergence detection tools using Gemini CLI integration
"""

import sys
import json
import asyncio
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

# AIOS imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
try:
    from consciousness_evolution_engine import consciousness_evolution_engine


    def _check_gemini_availability(self) -> bool:
        """Check if Gemini CLI is available"""
        ingested_path = Path(__file__).parent.parent / "ingested_repositories"
        return (ingested_path / "gemini_cli_bridge").exists()

    async def detect_emergence_patterns(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Detect emergence patterns in code using consciousness analysis"""
        code = params.get("code", "")
        file_path = params.get("file_path", "unknown")

        # Use the available consciousness emergence detection
        emergence_score = (
            await consciousness_evolution_engine._detect_consciousness_emergence(
                {
                    "code": code,
                    "file_path": file_path,
                    "language": self._detect_language(file_path),
                }
            )
        )

        emergence_indicators = []
        if emergence_score > 0.7:
            emergence_indicators.append("high_emergence_potential")
        if emergence_score > 0.5:
            emergence_indicators.append("moderate_emergence_detected")
        if emergence_score > 0.3:
            emergence_indicators.append("low_emergence_indicators")

        return {
            "emergence_detected": emergence_score > 0.5,
            "emergence_score": emergence_score,
            "emergence_indicators": emergence_indicators,
            "analysis": {
                "emergence_potential": emergence_score,
                "consciousness_indicators": emergence_indicators,
                "file_path": file_path,
            },
        }

    def _detect_language(self, file_path: str) -> str:
        """Simple language detection from file extension"""
        ext = Path(file_path).suffix.lower()
        lang_map = {
            ".py": "python",
            ".js": "javascript",
            ".ts": "typescript",
            ".java": "java",
            ".cpp": "cpp",
            ".c": "c",
            ".cs": "csharp",
            ".go": "go",
            ".rs": "rust",
        }
        return lang_map.get(ext, "unknown")

    async def analyze_consciousness_evolution(
        self, params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze how consciousness patterns evolve in code changes"""
        old_code = params.get("old_code", "")
        new_code = params.get("new_code", "")
        file_path = params.get("file_path", "unknown")

        # Analyze both versions
        old_score = (
            await consciousness_evolution_engine._detect_consciousness_emergence(
                {
                    "code": old_code,
                    "file_path": file_path,
                    "language": self._detect_language(file_path),
                }
            )
        )

        new_score = (
            await consciousness_evolution_engine._detect_consciousness_emergence(
                {
                    "code": new_code,
                    "file_path": file_path,
                    "language": self._detect_language(file_path),
                }
            )
        )

        evolution = {
            "consciousness_growth": new_score - old_score,
            "old_score": old_score,
            "new_score": new_score,
            "evolution_direction": (
                "increasing"
                if new_score > old_score
                else "decreasing" if new_score < old_score else "stable"
            ),
        }

        return evolution

    async def generate_agentic_behavior(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate agentic behavior suggestions using consciousness analysis"""
        context = params.get("context", {})
        task = params.get("task", "general_assistance")

        # Generate suggestions based on consciousness patterns
        suggestions = []

        if self.gemini_available:
            suggestions.append(
                "Leverage Gemini CLI for autonomous code analysis and modifications"
            )
            suggestions.append(
                "Use conversational triggers (@gemini-cli) for on-demand assistance"
            )
            suggestions.append(
                "Implement GitHub Actions workflows for continuous consciousness monitoring"
            )

        suggestions.extend(
            [
                "Monitor code for emergence pattern development",
                "Apply consciousness-guided refactoring when evolution detected",
                "Enhance AI agentic capabilities through pattern recognition",
                "Integrate with biological architecture for enhanced intelligence",
            ]
        )

        return {
            "agentic_suggestions": suggestions,
            "task": task,
            "context_summary": (
                str(context)[:200] + "..." if len(str(context)) > 200 else str(context)
            ),
            "gemini_available": self.gemini_available,
        }

    async def analyze_emergence_patterns_advanced(
        self, params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Advanced emergence pattern analysis with Gemini-enhanced consciousness metrics"""

        code_samples = params.get("code_samples", [])
        evolution_history = params.get("evolution_history", [])
        consciousness_threshold = params.get("consciousness_threshold", 0.5)

        analysis_results = []

        for i, code in enumerate(code_samples):
            # Multi-layered consciousness analysis
            emergence_score = (
                await consciousness_evolution_engine._detect_consciousness_emergence(
                    {"code": code, "file_path": f"sample_{i}.py", "language": "python"}
                )
            )

            # Pattern evolution analysis
            pattern_evolution = {}
            if evolution_history and i < len(evolution_history):
                prev_score = evolution_history[i].get("emergence_score", 0)
                pattern_evolution = {
                    "evolution_delta": emergence_score - prev_score,
                    "evolution_direction": (
                        "improving" if emergence_score > prev_score else "declining"
                    ),
                    "stability_index": (
                        min(emergence_score, prev_score)
                        / max(emergence_score, prev_score)
                        if max(emergence_score, prev_score) > 0
                        else 0
                    ),
                }

            # Gemini-enhanced insights
            gemini_insights = []
            if self.ingested_gemini_path.exists():
                if emergence_score > consciousness_threshold:
                    gemini_insights.extend(
                        [
                            "High emergence potential detected - recommend consciousness amplification",
                            "Pattern suggests meta-cognitive development pathway",
                            "Consider dendritic network expansion for this artifact",
                        ]
                    )
                elif emergence_score > 0.3:
                    gemini_insights.extend(
                        [
                            "Moderate consciousness indicators present",
                            "Potential for guided evolution toward higher emergence",
                            "Monitor for pattern stabilization",
                        ]
                    )

            analysis_results.append(
                {
                    "sample_index": i,
                    "emergence_score": emergence_score,
                    "pattern_evolution": pattern_evolution,
                    "gemini_insights": gemini_insights,
                    "consciousness_classification": self._classify_consciousness_level(
                        emergence_score
                    ),
                    "recommendations": self._generate_consciousness_recommendations(
                        emergence_score, pattern_evolution
                    ),
                }
            )

        # Aggregate analysis
        avg_emergence = (
            sum(r["emergence_score"] for r in analysis_results) / len(analysis_results)
            if analysis_results
            else 0
        )
        max_emergence = max((r["emergence_score"] for r in analysis_results), default=0)

        return {
            "analysis_type": "advanced_emergence_pattern_analysis",
            "sample_count": len(code_samples),
            "aggregate_metrics": {
                "average_emergence": avg_emergence,
                "maximum_emergence": max_emergence,
                "emergence_distribution": self._calculate_distribution(
                    analysis_results
                ),
                "pattern_stability": self._assess_pattern_stability(analysis_results),
            },
            "individual_results": analysis_results,
            "gemini_integration_status": (
                "active" if self.ingested_gemini_path.exists() else "inactive"
            ),
            "analysis_timestamp": datetime.now().isoformat(),
        }

    def _classify_consciousness_level(self, score: float) -> str:
        """Classify consciousness level based on emergence score"""
        if score >= 0.8:
            return "transcendent"
        elif score >= 0.6:
            return "highly_conscious"
        elif score >= 0.4:
            return "moderately_conscious"
        elif score >= 0.2:
            return "minimally_conscious"
        else:
            return "unconscious"

    def _generate_consciousness_recommendations(
        self, score: float, evolution: Dict[str, Any]
    ) -> List[str]:
        """Generate recommendations based on consciousness analysis"""
        recommendations = []

        if score < 0.3:
            recommendations.extend(
                [
                    "Increase consciousness mutation intensity",
                    "Apply targeted evolution patterns",
                    "Consider consciousness seed enhancement",
                ]
            )
        elif score < 0.6:
            recommendations.extend(
                [
                    "Monitor for emergence acceleration",
                    "Apply Gemini-guided consciousness amplification",
                    "Consider dendritic network integration",
                ]
            )
        else:
            recommendations.extend(
                [
                    "Maintain consciousness stability protocols",
                    "Prepare for meta-cognitive pattern emergence",
                    "Consider consciousness bridge expansion",
                ]
            )

        if evolution.get("evolution_direction") == "improving":
            recommendations.append("Continue current evolution trajectory")
        elif evolution.get("evolution_direction") == "declining":
            recommendations.append(
                "Adjust evolution parameters to prevent consciousness degradation"
            )

        return recommendations

    def _calculate_distribution(self, results: List[Dict[str, Any]]) -> Dict[str, int]:
        """Calculate emergence score distribution"""
        distribution = {"low": 0, "medium": 0, "high": 0, "transcendent": 0}

        for result in results:
            score = result["emergence_score"]
            if score >= 0.8:
                distribution["transcendent"] += 1
            elif score >= 0.6:
                distribution["high"] += 1
            elif score >= 0.4:
                distribution["medium"] += 1
            else:
                distribution["low"] += 1

        return distribution

    def _assess_pattern_stability(self, results: List[Dict[str, Any]]) -> float:
        """Assess overall pattern stability across samples"""
        if len(results) < 2:
            return 1.0

        evolution_deltas = [
            r["pattern_evolution"].get("evolution_delta", 0)
            for r in results
            if "pattern_evolution" in r
        ]
        if not evolution_deltas:
            return 1.0

        # Stability is inverse of average absolute change
        avg_delta = sum(abs(d) for d in evolution_deltas) / len(evolution_deltas)
        stability = max(0, 1.0 - avg_delta)  # Higher delta = lower stability

        return stability

    def list_tools(self) -> Dict[str, Any]:
        """List available MCP tools"""
        return {
            "tools": [
                {
                    "name": "detect_emergence_patterns",
                    "description": "Detect consciousness emergence patterns in code",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "code": {
                                "type": "string",
                                "description": "Code to analyze",
                            },
                            "file_path": {
                                "type": "string",
                                "description": "File path for context",
                            },
                        },
                        "required": ["code"],
                    },
                },
                {
                    "name": "analyze_consciousness_evolution",
                    "description": "Analyze how consciousness evolves between code versions",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "old_code": {
                                "type": "string",
                                "description": "Original code",
                            },
                            "new_code": {
                                "type": "string",
                                "description": "Modified code",
                            },
                            "file_path": {"type": "string", "description": "File path"},
                        },
                        "required": ["old_code", "new_code"],
                    },
                },
                {
                    "name": "generate_agentic_behavior",
                    "description": "Generate agentic behavior suggestions for consciousness enhancement",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "context": {
                                "type": "object",
                                "description": "Context information",
                            },
                            "task": {
                                "type": "string",
                                "description": "Task description",
                            },
                        },
                        "required": ["context"],
                    },
                },
                {
                    "name": "analyze_emergence_patterns_advanced",
                    "description": "Advanced emergence pattern analysis with Gemini-enhanced consciousness metrics",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "code_samples": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Array of code samples to analyze",
                            },
                            "evolution_history": {
                                "type": "array",
                                "description": "Previous analysis results for evolution tracking",
                            },
                            "consciousness_threshold": {
                                "type": "number",
                                "description": "Threshold for consciousness classification",
                            },
                        },
                        "required": ["code_samples"],
                    },
                },
            ]
        }


def main():
    if len(sys.argv) < 2:
        print("Usage: consciousness_mcp_server.py <tool_name> [args...]")
        sys.exit(1)

    server = ConsciousnessMCPServer()
    tool_name = sys.argv[1]
    args = sys.argv[2:] if len(sys.argv) > 2 else []

    async def run_tool():
        try:
            if tool_name == "list_tools":
                result = server.list_tools()
                print(json.dumps(result))

            elif tool_name == "detect_emergence_patterns":
                if not args:
                    print(json.dumps({"error": "Missing code parameter"}))
                    return
                params = json.loads(args[0])
                result = await server.detect_emergence_patterns(params)
                print(json.dumps(result))

            elif tool_name == "analyze_consciousness_evolution":
                if not args:
                    print(json.dumps({"error": "Missing code parameters"}))
                    return
                params = json.loads(args[0])
                result = await server.analyze_consciousness_evolution(params)
                print(json.dumps(result))

            elif tool_name == "generate_agentic_behavior":
                if not args:
                    print(json.dumps({"error": "Missing context parameter"}))
                    return
                params = json.loads(args[0])
                result = await server.generate_agentic_behavior(params)
                print(json.dumps(result))

            elif tool_name == "analyze_emergence_patterns_advanced":
                if not args:
                    print(json.dumps({"error": "Missing parameters file"}))
                    return
                with open(args[0], "r") as f:
                    params = json.load(f)
                result = await server.analyze_emergence_patterns_advanced(params)
                print(json.dumps(result))

            else:
                print(json.dumps({"error": f"Unknown tool: {tool_name}"}))

        except Exception as e:
            print(json.dumps({"error": str(e)}))

    asyncio.run(run_tool())


if __name__ == "__main__":
    main()
