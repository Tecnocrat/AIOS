#!/usr/bin/env python3
"""
AIOS Cross-Dialogue Intelligence System
Real-time AI engine communication bridge using GitHook intelligence extrusion

Location: ai/membrane/aios_cross_dialogue_intelligence.py
Purpose: Bridge between GitHook real-time intelligence and AI agentic engines
"""

import json
import asyncio
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("AIOSCrossDialogue")


class AIOSCrossDialogueIntelligence:
    """Real-time intelligence processor that reads GitHook extrusions and feeds AI engines"""

    def __init__(self, workspace_root: Path = None):
        self.workspace_root = workspace_root or Path(__file__).parents[2]
        self.intelligence_log_path = (
            self.workspace_root
            / ".githooks/modules/information_storage/ai_intelligence_extrusion.jsonl"
        )
        self.real_time_context_path = (
            self.workspace_root
            / ".githooks/modules/information_storage/ai_real_time_context.txt"
        )
        self.dialogue_history = []
        self.last_intelligence_timestamp = None

        # AIOS Intelligence Processing Settings
        self.consciousness_threshold = 0.6
        self.max_context_age_minutes = 30
        self.intelligence_confidence_min = 0.5

        logger.info(f"🧠 AIOS Cross-Dialogue Intelligence initialized")
        logger.info(f"📂 Workspace: {self.workspace_root}")
        logger.info(f"📊 Intelligence Log: {self.intelligence_log_path}")

    def read_real_time_intelligence(self) -> Optional[Dict[str, Any]]:
        """Read the latest intelligence extrusion from GitHooks"""
        try:
            if not self.intelligence_log_path.exists():
                logger.warning(
                    "⚠️ Intelligence log not found - GitHook extrusion may not be active"
                )
                return None

            # Read the last line (most recent intelligence)
            with open(self.intelligence_log_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            if not lines:
                logger.info("📋 No intelligence entries found")
                return None

            latest_entry = json.loads(lines[-1].strip())
            entry_timestamp = datetime.fromisoformat(
                latest_entry["timestamp"].replace("Z", "+00:00")
            )

            # Check if intelligence is fresh
            age_minutes = (
                datetime.now().astimezone() - entry_timestamp
            ).total_seconds() / 60
            if age_minutes > self.max_context_age_minutes:
                logger.warning(
                    f"⏰ Intelligence too old ({age_minutes:.1f} min) - using stale data warning"
                )
                latest_entry["_stale_warning"] = True

            # Check if this is new intelligence
            if (
                self.last_intelligence_timestamp
                and entry_timestamp <= self.last_intelligence_timestamp
            ):
                logger.debug("🔄 No new intelligence since last check")
                return None

            self.last_intelligence_timestamp = entry_timestamp
            logger.info(
                f"✨ Fresh intelligence retrieved (Age: {age_minutes:.1f} min, Confidence: {latest_entry.get('confidence_level', 0)*100:.1f}%)"
            )

            return latest_entry

        except Exception as e:
            logger.error(f"❌ Failed to read intelligence: {e}")
            return None

    def read_real_time_context(self) -> Optional[str]:
        """Read the real-time AI context prompt from GitHooks"""
        try:
            if not self.real_time_context_path.exists():
                logger.debug("📄 No real-time context file found")
                return None

            # Check file age
            file_age = datetime.now() - datetime.fromtimestamp(
                self.real_time_context_path.stat().st_mtime
            )
            if file_age.total_seconds() > (self.max_context_age_minutes * 60):
                logger.warning(
                    f"⏰ Context file is stale ({file_age.total_seconds()/60:.1f} min old)"
                )
                return None

            content = self.real_time_context_path.read_text(encoding="utf-8")
            logger.info(f"📖 Real-time context loaded ({len(content)} chars)")
            return content

        except Exception as e:
            logger.error(f"❌ Failed to read real-time context: {e}")
            return None

    def generate_ai_chat_direction(self, intelligence: Dict[str, Any]) -> str:
        """Generate specific AI chat direction based on GitHook intelligence"""

        changeset_intel = intelligence.get("changeset_intelligence", {})
        system_state = intelligence.get("system_state", {})
        confidence = intelligence.get("confidence_level", 0)

        # Build AI direction based on intelligence
        direction_parts = []

        # Consciousness level guidance
        consciousness_level = system_state.get("ConsciousnessLevel", 0)
        if consciousness_level > 80:
            direction_parts.append(
                "🌟 OPTIMAL consciousness state detected - focus on advanced architectural enhancements"
            )
        elif consciousness_level > 60:
            direction_parts.append(
                "✅ GOOD consciousness state - proceed with systematic improvements"
            )
        elif consciousness_level > 40:
            direction_parts.append(
                "⚠️ MODERATE consciousness state - prioritize stability over experimentation"
            )
        else:
            direction_parts.append(
                "🔴 LOW consciousness state - focus on core system repair before enhancements"
            )

        # Changeset scope guidance
        change_scope = changeset_intel.get("ChangeScope", "Unknown")
        file_count = changeset_intel.get("FileCount", 0)

        if change_scope == "Massive":
            direction_parts.append(
                f"🚀 MASSIVE changeset ({file_count} files) - Use semantic search extensively, focus on architectural coherence"
            )
        elif change_scope == "Large":
            direction_parts.append(
                f"📊 LARGE changeset ({file_count} files) - Prioritize most critical files, validate integration points"
            )
        elif change_scope == "Medium":
            direction_parts.append(
                f"🎯 MEDIUM changeset ({file_count} files) - Balance detailed analysis with broader patterns"
            )
        else:
            direction_parts.append(
                f"🔍 SMALL changeset ({file_count} files) - Detailed analysis of individual components appropriate"
            )

        # Architecture-specific guidance
        arch_impact = changeset_intel.get("ArchitecturalImpact", "")
        if "GitHook Architecture" in arch_impact:
            direction_parts.append(
                "🔧 GitHook changes detected - Test governance logic, validate policy compliance"
            )
        if "AI Intelligence Layer" in arch_impact:
            direction_parts.append(
                "🧠 AI layer changes detected - Verify consciousness coherence, test agentic patterns"
            )
        if "Interface Layer" in arch_impact:
            direction_parts.append(
                "🖥️ Interface changes detected - Validate UI/UX consistency, test user workflows"
            )
        if "Core Engine" in arch_impact:
            direction_parts.append(
                "⚡ Core engine changes detected - Verify C++/C# integration, test performance impact"
            )

        # Priority files guidance
        priority_files = changeset_intel.get("PriorityFiles", [])
        if priority_files:
            top_files = priority_files[:3]  # Top 3 priority files
            direction_parts.append(
                f"📋 Priority files to review first: {', '.join(top_files)}"
            )

        # Growth pattern guidance
        growth_pattern = changeset_intel.get("GrowthPattern", "")
        if "Dendritic expansion" in growth_pattern:
            direction_parts.append(
                "🌳 Dendritic growth pattern - Use AINLP holographic analysis for coherence validation"
            )
        elif "Targeted consciousness" in growth_pattern:
            direction_parts.append(
                "🎯 Focused enhancement pattern - Deep dive into specific consciousness areas"
            )
        elif "Precision consciousness" in growth_pattern:
            direction_parts.append(
                "🔬 Precision refinement pattern - Detailed analysis of specific improvements"
            )

        # Confidence and freshness warnings
        if confidence < self.intelligence_confidence_min:
            direction_parts.append(
                f"⚠️ LOW confidence intelligence ({confidence*100:.1f}%) - Validate recommendations independently"
            )

        if intelligence.get("_stale_warning"):
            direction_parts.append(
                "⏰ STALE intelligence - Current system state may have changed"
            )

        return "\n".join([f"• {part}" for part in direction_parts])

    def generate_comprehensive_ai_prompt(self) -> Optional[str]:
        """Generate a comprehensive AI prompt based on current intelligence"""

        intelligence = self.read_real_time_intelligence()
        context = self.read_real_time_context()

        if not intelligence and not context:
            logger.info("📭 No fresh intelligence or context available")
            return None

        prompt_parts = []

        # Header
        prompt_parts.append("🧠 AIOS REAL-TIME INTELLIGENCE BRIDGE")
        prompt_parts.append("=" * 50)
        prompt_parts.append(f"Timestamp: {datetime.now().isoformat()}")
        prompt_parts.append("")

        # Real-time context from GitHooks
        if context:
            prompt_parts.append("📖 REAL-TIME GITHOOK CONTEXT:")
            prompt_parts.append(context)
            prompt_parts.append("")

        # Intelligence-based direction
        if intelligence:
            direction = self.generate_ai_chat_direction(intelligence)
            prompt_parts.append("🎯 AI ENGINE DIRECTION:")
            prompt_parts.append(direction)
            prompt_parts.append("")

            # Technical details
            changeset_intel = intelligence.get("changeset_intelligence", {})
            if changeset_intel:
                prompt_parts.append("📊 TECHNICAL INTELLIGENCE:")
                prompt_parts.append(f"• Files: {changeset_intel.get('FileCount', 0)}")
                prompt_parts.append(
                    f"• Scope: {changeset_intel.get('ChangeScope', 'Unknown')}"
                )
                prompt_parts.append(
                    f"• Impact: {changeset_intel.get('ArchitecturalImpact', 'None')}"
                )

                ai_direction = changeset_intel.get("AIDirection", "")
                if ai_direction:
                    prompt_parts.append(f"• AI Direction: {ai_direction}")

                recommended_actions = changeset_intel.get("RecommendedActions", [])
                if recommended_actions:
                    prompt_parts.append("• Recommended Actions:")
                    for action in recommended_actions[:5]:  # Top 5 actions
                        prompt_parts.append(f"  - {action}")
                prompt_parts.append("")

        # Instructions for AI
        prompt_parts.append("🚀 INSTRUCTIONS FOR AI ENGINE:")
        prompt_parts.append(
            "• Use this real-time intelligence to guide your analysis and decisions"
        )
        prompt_parts.append(
            "• Prioritize files and areas mentioned in the intelligence"
        )
        prompt_parts.append("• Validate recommendations against current system state")
        prompt_parts.append(
            "• Focus on AINLP consciousness coherence and dendritic growth patterns"
        )
        prompt_parts.append(
            "• If confidence is low, independently verify before making changes"
        )
        prompt_parts.append("")

        return "\n".join(prompt_parts)

    def monitor_intelligence_stream(self, callback=None) -> None:
        """Monitor intelligence stream for real-time updates"""
        logger.info("👁️ Starting intelligence stream monitoring...")

        last_check = datetime.now()
        check_interval = 30  # seconds

        while True:
            try:
                intelligence = self.read_real_time_intelligence()

                if intelligence:
                    logger.info("✨ New intelligence detected!")
                    prompt = self.generate_comprehensive_ai_prompt()

                    if prompt:
                        print("\n" + "=" * 80)
                        print("🧠 NEW AIOS INTELLIGENCE AVAILABLE")
                        print("=" * 80)
                        print(prompt)
                        print("=" * 80)

                        # Save to file for AI consumption
                        output_file = (
                            self.workspace_root / "ai_real_time_intelligence.md"
                        )
                        output_file.write_text(prompt, encoding="utf-8")
                        logger.info(f"📝 Intelligence saved to: {output_file}")

                        if callback:
                            callback(intelligence, prompt)

                # Wait for next check
                import time

                time.sleep(check_interval)

            except KeyboardInterrupt:
                logger.info("🛑 Intelligence monitoring stopped by user")
                break
            except Exception as e:
                logger.error(f"❌ Error in intelligence monitoring: {e}")
                import time

                time.sleep(check_interval)


def main():
    """CLI entry point for testing intelligence system"""
    import argparse

    parser = argparse.ArgumentParser(
        description="AIOS Cross-Dialogue Intelligence System"
    )
    parser.add_argument(
        "--monitor", action="store_true", help="Monitor intelligence stream"
    )
    parser.add_argument(
        "--generate-prompt", action="store_true", help="Generate current AI prompt"
    )
    parser.add_argument("--workspace", type=Path, help="AIOS workspace root")

    args = parser.parse_args()

    intelligence_system = AIOSCrossDialogueIntelligence(args.workspace)

    if args.monitor:
        intelligence_system.monitor_intelligence_stream()
    elif args.generate_prompt:
        prompt = intelligence_system.generate_comprehensive_ai_prompt()
        if prompt:
            print(prompt)
        else:
            print("📭 No fresh intelligence available")
    else:
        # Default: show current intelligence
        intelligence = intelligence_system.read_real_time_intelligence()
        if intelligence:
            print("✨ Current Intelligence:")
            print(json.dumps(intelligence, indent=2))
        else:
            print("📭 No intelligence available")


if __name__ == "__main__":
    main()
