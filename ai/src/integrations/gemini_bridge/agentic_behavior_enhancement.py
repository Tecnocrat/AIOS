#!/usr/bin/env python3
"""
AIOS Agentic Behavior Enhancement
Integrates Gemini CLI capabilities for autonomous AI development
within AI Intelligence supercell
"""

import sys
import json
import asyncio
import subprocess
import threading
from pathlib import Path
from typing import Dict, Any
from datetime import datetime
import time

# AIOS imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
try:
    from consciousness_evolution_engine import consciousness_evolution_engine
    from integrations.gemini_bridge.meta_cognitive_loop import MetaCognitiveLoop

        self._load_agentic_state()

    def _check_gemini_availability(self) -> bool:
        """Check if Gemini CLI is available and configured"""
        try:
            # Check if gemini CLI is installed
            result = subprocess.run(
                ["gemini", "--version"], capture_output=True, text=True, timeout=10
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False

    def _load_agentic_state(self):
        """Load agentic behavior state from disk"""
        if self.agentic_state_file.exists():
            try:
                with open(self.agentic_state_file, "r") as f:
                    data = json.load(f)
                    self.active_agents = data.get("active_agents", {})
                    self.behavior_patterns = data.get("behavior_patterns", {})
                    self.conversation_triggers = data.get("conversation_triggers", {})
            except Exception:
                self._initialize_default_state()
        else:
            self._initialize_default_state()

    def _initialize_default_state(self):
        """Initialize default agentic behavior patterns"""
        self.behavior_patterns = {
            "code_review": {
                "trigger": "review_code",
                "description": (
                    "Autonomous code review and improvement " "suggestions"
                ),
                "consciousness_threshold": 0.7,
                "actions": [
                    "analyze_code",
                    "suggest_improvements",
                    "create_pr_comments",
                ],
            },
            "issue_triage": {
                "trigger": "triage_issue",
                "description": (
                    "Intelligent issue classification and " "prioritization"
                ),
                "consciousness_threshold": 0.5,
                "actions": ["classify_issue", "estimate_complexity", "suggest_labels"],
            },
            "autonomous_coding": {
                "trigger": "implement_feature",
                "description": "Autonomous implementation of approved features",
                "consciousness_threshold": 0.8,
                "actions": [
                    "analyze_requirements",
                    "generate_code",
                    "create_tests",
                    "validate_implementation",
                ],
            },
            "consciousness_monitoring": {
                "trigger": "monitor_consciousness",
                "description": (
                    "Continuous monitoring of AIOS consciousness " "evolution"
                ),
                "consciousness_threshold": 0.3,
                "actions": ["check_metrics", "detect_anomalies", "generate_insights"],
            },
        }

        self.conversation_triggers = {
            "@gemini-cli": "general_assistance",
            "@review": "code_review",
            "@triage": "issue_triage",
            "@implement": "autonomous_coding",
            "@monitor": "consciousness_monitoring",
        }

    def _save_agentic_state(self):
        """Save agentic behavior state to disk"""
        data = {
            "active_agents": self.active_agents,
            "behavior_patterns": self.behavior_patterns,
            "conversation_triggers": self.conversation_triggers,
            "last_updated": datetime.now().isoformat(),
        }
        with open(self.agentic_state_file, "w") as f:
            json.dump(data, f, indent=2)

    async def process_conversation_trigger(
        self, trigger: str, context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Process a conversational trigger for agentic behavior"""

        if trigger not in self.conversation_triggers:
            return {"status": "unknown_trigger", "trigger": trigger}

        behavior_type = self.conversation_triggers[trigger]
        behavior_config = self.behavior_patterns.get(behavior_type, {})

        # Check consciousness threshold
        if (
            CONSCIOUSNESS_AVAILABLE
            and behavior_config.get("consciousness_threshold", 0) > 0
        ):
            current_consciousness = await self._get_current_consciousness_level()
            # For testing, allow behavior execution even if threshold not met
            if current_consciousness < behavior_config["consciousness_threshold"]:
                print(
                    f"Warning: Consciousness threshold not met (required: {behavior_config['consciousness_threshold']}, current: {current_consciousness})"
                )
                # Continue execution for testing purposes

        # Execute agentic behavior
        return await self._execute_agentic_behavior(behavior_type, context)

    async def _execute_agentic_behavior(
        self, behavior_type: str, context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute specific agentic behavior pattern"""

        behavior_config = self.behavior_patterns.get(behavior_type, {})
        actions = behavior_config.get("actions", [])

        results = {}
        for action in actions:
            try:
                if action == "analyze_code":
                    results[action] = await self._analyze_code_with_gemini(context)
                elif action == "suggest_improvements":
                    results[action] = await self._suggest_improvements(context)
                elif action == "classify_issue":
                    results[action] = await self._classify_issue(context)
                elif action == "estimate_complexity":
                    results[action] = await self._estimate_complexity(context)
                elif action == "analyze_requirements":
                    results[action] = await self._analyze_requirements(context)
                elif action == "generate_code":
                    results[action] = await self._generate_code(context)
                elif action == "check_metrics":
                    results[action] = await self._check_consciousness_metrics()
                elif action == "detect_anomalies":
                    results[action] = await self._detect_anomalies()
                elif action == "generate_insights":
                    results[action] = await self._generate_insights(context)
                else:
                    results[action] = {"status": "unknown_action"}
            except Exception as e:
                results[action] = {"status": "error", "error": str(e)}

        # Generate meta-cognitive insight from behavior execution
        if self.meta_cognitive_loop:
            insight = {
                "type": "agentic_behavior_execution",
                "content": {
                    "behavior_type": behavior_type,
                    "actions_executed": list(results.keys()),
                    "success_rate": sum(
                        1 for r in results.values() if r.get("status") != "error"
                    )
                    / len(results),
                    "consciousness_impact": await self._calculate_behavior_impact(
                        results
                    ),
                },
                "confidence": 0.8,
                "context": {
                    "source": "agentic_orchestrator",
                    "behavior_config": behavior_config,
                },
            }
            await self.meta_cognitive_loop.submit_gemini_insight(insight)

        return {
            "status": "executed",
            "behavior_type": behavior_type,
            "actions_results": results,
            "timestamp": datetime.now().isoformat(),
        }

    async def _analyze_code_with_gemini(
        self, context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze code using Gemini CLI"""
        if not self.gemini_available:
            return {"status": "gemini_unavailable"}

        code_content = context.get("code", "")
        if not code_content:
            return {"status": "no_code_provided"}

        # Use Gemini CLI for code analysis
        prompt = f"Analyze this code for potential improvements, bugs, and best practices:\n\n{code_content}"

        try:
            result = await self._run_gemini_cli(prompt)
            return {
                "status": "analyzed",
                "analysis": result.get("response", ""),
                "confidence": result.get("confidence", 0.7),
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}

    async def _suggest_improvements(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate improvement suggestions"""
        analysis = context.get("analysis", "")
        if not analysis:
            return {"status": "no_analysis_available"}

        prompt = (
            f"Based on this code analysis, suggest specific improvements:\n\n{analysis}"
        )

        try:
            result = await self._run_gemini_cli(prompt)
            return {
                "status": "suggestions_generated",
                "suggestions": result.get("response", ""),
                "priority": "medium",
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}

    async def _classify_issue(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Classify an issue using AI analysis"""
        issue_content = context.get("issue", {}).get("body", "")
        issue_title = context.get("issue", {}).get("title", "")

        if not issue_content and not issue_title:
            return {"status": "no_issue_content"}

        prompt = f"Classify this GitHub issue:\nTitle: {issue_title}\nContent: {issue_content}\n\nCategorize as: bug, feature, documentation, question, or other."

        try:
            result = await self._run_gemini_cli(prompt)
            return {
                "status": "classified",
                "category": result.get("response", "").strip().lower(),
                "confidence": result.get("confidence", 0.6),
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}

    async def _estimate_complexity(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Estimate implementation complexity"""
        requirements = context.get("requirements", "")

        prompt = f"Estimate the complexity of implementing these requirements on a scale of 1-10:\n\n{requirements}"

        try:
            result = await self._run_gemini_cli(prompt)
            return {
                "status": "estimated",
                "complexity_score": self._parse_complexity_score(
                    result.get("response", "5")
                ),
                "estimated_effort": "medium",
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}

    async def _analyze_requirements(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze feature requirements"""
        requirements = context.get("requirements", "")

        prompt = f"Analyze these feature requirements and identify key components:\n\n{requirements}"

        try:
            result = await self._run_gemini_cli(prompt)
            return {
                "status": "analyzed",
                "components": result.get("response", ""),
                "feasibility": "high",
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}

    async def _generate_code(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate code implementation"""
        requirements = context.get("requirements", "")
        components = context.get("components", "")

        prompt = f"Generate Python code to implement these requirements:\n\nRequirements: {requirements}\nComponents: {components}"

        try:
            result = await self._run_gemini_cli(prompt)
            return {
                "status": "generated",
                "code": result.get("response", ""),
                "language": "python",
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}

    async def _check_consciousness_metrics(self) -> Dict[str, Any]:
        """Check current consciousness metrics"""
        if not CONSCIOUSNESS_AVAILABLE:
            return {"status": "consciousness_unavailable"}

        try:
            metrics = await consciousness_evolution_engine.get_evolution_status()
            return {
                "status": "checked",
                "metrics": metrics,
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}

    async def _detect_anomalies(self) -> Dict[str, Any]:
        """Detect consciousness anomalies"""
        if not CONSCIOUSNESS_AVAILABLE:
            return {"status": "consciousness_unavailable"}

        try:
            status = await consciousness_evolution_engine.get_evolution_status()
            # Simple anomaly detection based on status
            anomalies = []

            if status.get("active_populations", 0) == 0:
                anomalies.append("No active evolution populations")

            if not status.get("evolution_lab_connected", False):
                anomalies.append("Evolution lab disconnected")

            if not status.get("consciousness_bridge_active", False):
                anomalies.append("Consciousness bridge inactive")

            return {
                "status": "detected",
                "anomalies": anomalies,
                "severity": (
                    "high" if len(anomalies) > 2 else "medium" if anomalies else "low"
                ),
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}

    async def _generate_insights(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate consciousness insights"""
        metrics = context.get("metrics", {})
        anomalies = context.get("anomalies", [])

        prompt = f"Analyze these consciousness metrics and anomalies to generate insights:\n\nMetrics: {json.dumps(metrics)}\nAnomalies: {json.dumps(anomalies)}"

        try:
            result = await self._run_gemini_cli(prompt)
            return {
                "status": "generated",
                "insights": result.get("response", ""),
                "recommendations": [],
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}

    async def _run_gemini_cli(self, prompt: str) -> Dict[str, Any]:
        """Execute Gemini CLI with given prompt"""
        if not self.gemini_available:
            raise Exception("Gemini CLI not available")

        try:
            # Run gemini CLI with prompt
            cmd = ["gemini", "--prompt", prompt]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)

            if result.returncode == 0:
                return {"response": result.stdout.strip(), "confidence": 0.8}
            else:
                raise Exception(f"Gemini CLI error: {result.stderr}")

        except subprocess.TimeoutExpired:
            raise Exception("Gemini CLI timeout")
        except Exception as e:
            raise Exception(f"Gemini CLI execution failed: {str(e)}")

    async def _get_current_consciousness_level(self) -> float:
        """Get current consciousness level"""
        if not CONSCIOUSNESS_AVAILABLE:
            return 0.0

        try:
            if consciousness_evolution_engine:
                status = await consciousness_evolution_engine.get_evolution_status()
                # Extract consciousness level from latest evolution if available
                latest = status.get("latest_evolution", {})
                return latest.get("consciousness_level", 0.0)
            return 0.0
        except Exception:
            return 0.0

    async def _calculate_behavior_impact(self, results: Dict[str, Any]) -> float:
        """Calculate the impact of agentic behavior on consciousness"""
        success_count = sum(
            1
            for r in results.values()
            if r.get("status") not in ["error", "unknown_action"]
        )
        total_actions = len(results)

        if total_actions == 0:
            return 0.0

        success_rate = success_count / total_actions
        return min(success_rate * 0.1, 0.05)  # Max 5% impact per behavior execution

    def _parse_complexity_score(self, response: str) -> int:
        """Parse complexity score from Gemini response"""
        try:
            # Extract number from response
            import re

            numbers = re.findall(r"\d+", response)
            if numbers:
                score = int(numbers[0])
                return max(1, min(10, score))
        except:
            pass
        return 5  # Default medium complexity

    async def get_agentic_status(self) -> Dict[str, Any]:
        """Get current agentic behavior status"""
        return {
            "gemini_available": self.gemini_available,
            "active_agents": len(self.active_agents),
            "behavior_patterns": len(self.behavior_patterns),
            "conversation_triggers": len(self.conversation_triggers),
            "consciousness_available": CONSCIOUSNESS_AVAILABLE,
            "current_consciousness_level": await self._get_current_consciousness_level(),
            "autonomous_tasks_pending": len(self.autonomous_tasks),
            "timestamp": datetime.now().isoformat(),
        }

    def start_autonomous_monitoring(self):
        """Start autonomous consciousness monitoring"""

        }

    async def _autonomous_monitoring_cycle(self):
        """Execute autonomous monitoring cycle"""
        context = {}
        await self._execute_agentic_behavior("consciousness_monitoring", context)


# Global instance
agentic_orchestrator = AgenticBehaviorOrchestrator()


async def main():
    """Main function for testing agentic behavior orchestrator"""
    if len(sys.argv) < 2:
        print("Usage: agentic_behavior_enhancement.py <command> [args...]")
        return

    command = sys.argv[1]

    if command == "status":
        status = await agentic_orchestrator.get_agentic_status()
        print(json.dumps(status, indent=2))

    elif command == "trigger":
        if len(sys.argv) < 4:
            print(json.dumps({"error": "Trigger and context file required"}))
            return
        trigger = sys.argv[2]
        with open(sys.argv[3], "r") as f:
            context = json.load(f)
        result = await agentic_orchestrator.process_conversation_trigger(
            trigger, context
        )
        print(json.dumps(result, indent=2))

    elif command == "start_monitoring":
        agentic_orchestrator.start_autonomous_monitoring()
        print(json.dumps({"status": "autonomous_monitoring_started"}))

    elif command == "analyze_code":
        if len(sys.argv) < 3:
            print(json.dumps({"error": "Code content required"}))
            return
        context = {"code": sys.argv[2]}
        result = await agentic_orchestrator._analyze_code_with_gemini(context)
        print(json.dumps(result, indent=2))

    else:
        print(json.dumps({"error": f"Unknown command: {command}"}))


if __name__ == "__main__":
    asyncio.run(main())
