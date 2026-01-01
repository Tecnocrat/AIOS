#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AIOS Agentic Instruction Generator
=================================
Location: ai/laboratory/scripts/agentic_instruction_generator.py
Purpose: Convert quality analysis results into AI-actionable instructions
Architecture: LABORATORY supercell → AI agent communication bridge

This component transforms emoji detection and quality analysis results into
structured instructions that AI chat agents can execute autonomously for
code refactoring and improvement.
"""

import json
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List


class TaskPriority(Enum):
    """Priority levels for agentic tasks"""

    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class TaskType(Enum):
    """Types of agentic refactoring tasks"""

    UNICODE_CLEANUP = "unicode_cleanup"
    CODE_FORMATTING = "code_formatting"
    IMPORT_OPTIMIZATION = "import_optimization"
    DOCUMENTATION_UPDATE = "documentation_update"
    QUALITY_IMPROVEMENT = "quality_improvement"


@dataclass
class AgenticTask:
    """Structured task for AI agent execution"""

    task_id: str
    task_type: TaskType
    priority: TaskPriority
    title: str
    description: str
    instructions: List[str]
    target_files: List[str]
    success_criteria: str
    rollback_plan: str
    estimated_changes: int
    risk_level: str
    ai_prompt: str
    metadata: Dict[str, Any]
    created_at: str


class AgenticInstructionGenerator:
    """Main generator for AI-actionable instructions"""

    def __init__(self, workspace_root: Path = None):
        self.workspace_root = workspace_root or Path.cwd()

    def generate_from_emoji_analysis(
        self, emoji_results: Dict[str, Any]
    ) -> AgenticTask:
        """Generate agentic task from emoji detection results"""

        # Extract key metrics
        total_emojis = emoji_results.get("total_emojis", 0)
        files_affected = len(emoji_results.get("emoji_by_file", {}))
        emoji_frequency = emoji_results.get("emoji_frequency", {})

        # Determine priority based on severity
        priority = self._calculate_priority(total_emojis, files_affected)

        # Generate replacement instructions
        replacement_map = self._generate_replacement_map(emoji_frequency)

        # Create detailed instructions
        instructions = self._generate_unicode_cleanup_instructions(
            emoji_results, replacement_map
        )

        # Generate AI prompt
        ai_prompt = self._generate_ai_prompt(
            total_emojis, files_affected, replacement_map, instructions
        )

        return AgenticTask(
            task_id=f"unicode_cleanup_{uuid.uuid4().hex[:8]}",
            task_type=TaskType.UNICODE_CLEANUP,
            priority=priority,
            title=(
                f"Unicode Emoji Cleanup - {total_emojis} emojis in "
                f"{files_affected} files"
            ),
            description=(
                f"Systematic cleanup of {total_emojis} Unicode emoji "
                f"characters causing Windows terminal encoding "
                f"failures across {files_affected} files in the "
                f"GitHooks system."
            ),
            instructions=instructions,
            target_files=list(emoji_results.get("emoji_by_file", {}).keys()),
            success_criteria=(
                "Zero Unicode emojis in Windows-incompatible "
                "ranges (U+1F300-U+1F9FF, U+2600-U+27BF)"
            ),
            rollback_plan=(
                "Git revert all changes if encoding tests fail or "
                "functionality breaks"
            ),
            estimated_changes=total_emojis,
            risk_level="LOW" if total_emojis < 100 else "MEDIUM",
            ai_prompt=ai_prompt,
            metadata={
                "emoji_frequency": emoji_frequency,
                "replacement_map": replacement_map,
                "analysis_timestamp": emoji_results.get(
                    "analysis_timestamp", datetime.now().isoformat()
                ),
                "quality_grade": emoji_results.get(
                    "overall_quality_score", {}
                ).get("grade", "Unknown"),
            },
            created_at=datetime.now().isoformat(),
        )

    def generate_from_quality_analysis(
        self, quality_results: Dict[str, Any]
    ) -> List[AgenticTask]:
        """Generate multiple agentic tasks from comprehensive analysis"""
        tasks = []

        # Unicode cleanup task from emoji analysis
        if "emoji_analysis" in quality_results:
            emoji_task = self.generate_from_emoji_analysis(
                quality_results["emoji_analysis"]
            )
            tasks.append(emoji_task)

        # Additional quality improvement tasks
        overall_score = quality_results.get("overall_quality_score", {}).get(
            "overall_score", 1.0
        )
        if overall_score < 0.7:
            quality_task = self._generate_quality_improvement_task(
                quality_results
            )
            tasks.append(quality_task)

        return tasks

    def _calculate_priority(
        self, emoji_count: int, file_count: int
    ) -> TaskPriority:
        """Calculate task priority based on severity"""
        if emoji_count > 500 or file_count > 25:
            return TaskPriority.CRITICAL
        elif emoji_count > 100 or file_count > 10:
            return TaskPriority.HIGH
        elif emoji_count > 20 or file_count > 3:
            return TaskPriority.MEDIUM
        else:
            return TaskPriority.LOW

    def _generate_replacement_map(
        self, emoji_frequency: Dict[str, int]
    ) -> Dict[str, str]:
        """Generate emoji to text replacement mapping"""
        replacement_map = {
            # Status indicators
            "": "[COMPLETED]",
            "": "[FAILED]",
            "": "[WARNING]",
            "": "[IN-PROGRESS]",
            # Functional symbols
            "": "TARGET:",
            "": "SUPERCELL:",
            "": "LAUNCH:",
            "": "METRICS:",
            "": "ANALYSIS:",
            "": "FOLDER:",
            "": "DOCS:",
            "": "TOOL:",
            # Architecture symbols
            "": "CORE:",
            "": "RUNTIME:",
            "": "ARCHIVE:",
            "": "AI:",
            "": "INTERFACE:",
            "": "LIBRARY:",
            # Process symbols
            "": "SUCCESS:",
            "": "IDEA:",
            "": "FEATURE:",
            "": "ENHANCEMENT:",
        }

        # Add generic replacements for any emojis not in map
        for emoji in emoji_frequency.keys():
            if emoji not in replacement_map:
                replacement_map[emoji] = f"[{emoji}]"

        return replacement_map

    def _generate_unicode_cleanup_instructions(
        self, emoji_results: Dict[str, Any], replacement_map: Dict[str, str]
    ) -> List[str]:
        """Generate detailed cleanup instructions"""
        instructions = [
            "AUTOMATED UNICODE EMOJI CLEANUP TASK",
            "====================================",
            "",
            "OBJECTIVE: Replace all Unicode emoji characters with ASCII",
            "SCOPE: GitHooks system files (.md, .py, .ps1, .txt, .json)",
            "",
            "REPLACEMENT STRATEGY:",
        ]

        # Add specific replacement mappings
        for emoji, replacement in replacement_map.items():
            if emoji in emoji_results.get("emoji_frequency", {}):
                count = emoji_results["emoji_frequency"][emoji]
                instructions.append(
                    f"  '{emoji}' → '{replacement}' ({count} occurrences)"
                )

        instructions.extend(
            [
                "",
                "EXECUTION REQUIREMENTS:",
                "- Process files individually to enable incremental rollback",
                "- Preserve all surrounding formatting and context exactly",
                "- Maintain markdown structure and indentation",
                "- Test each file after replacement to ensure no corruption",
                "- Use exact string replacement to avoid unintended changes",
                "",
                "VALIDATION CRITERIA:",
                "- No Unicode characters in ranges U+1F300-U+1F9FF (emojis)",
                "- No Unicode characters in ranges U+2600-U+27BF (symbols)",
                "- All existing functionality preserved",
                "- No changes to code logic, only cosmetic emoji replacement",
                "",
                "SAFETY PROTOCOLS:",
                "- Create git branch before starting changes",
                "- Commit each file individually for granular rollback",
                "- Run encoding tests after each file modification",
                "- Stop immediately if any file corruption detected",
            ]
        )

        return instructions

    def _generate_ai_prompt(
        self,
        total_emojis: int,
        files_affected: int,
        replacement_map: Dict[str, str],
        instructions: List[str],
    ) -> str:
        """Generate structured AI prompt for autonomous execution"""

        # Create condensed replacement map for prompt
        common_replacements = {
            k: v
            for k, v in replacement_map.items()
            if k in ["", "", "", "", "", "", "", ""]
        }

        replacement_text = chr(10).join(
            f"  {emoji} → {replacement}"
            for emoji, replacement in common_replacements.items()
        )

        return f"""
AGENTIC AUTO MODE: Unicode Emoji Cleanup Task
=============================================

**TASK SUMMARY:**
- Replace {total_emojis} Unicode emoji characters across {files_affected} files
- Focus on GitHooks system (.githooks directory and subdirectories)
- Resolve Windows terminal encoding failures

**PRIMARY REPLACEMENTS:**
{replacement_text}

**EXECUTION APPROACH:**
1. Scan each target file for Unicode emoji characters
2. Apply exact string replacements using the provided mapping
3. Preserve all formatting, indentation, and context
4. Test encoding compatibility after each file
5. Commit changes incrementally for rollback capability

**SUCCESS CRITERIA:**
- Zero Unicode emojis in Windows-incompatible ranges
- All file functionality preserved
- No encoding errors in Windows terminal
- Clean git history with descriptive commit messages

**SAFETY REQUIREMENTS:**
- Process files individually, not in bulk
- Test each replacement before proceeding
- Stop if any corruption or unexpected changes detected
- Maintain complete audit trail of all modifications

Please execute this Unicode cleanup task autonomously, following the \
safety protocols and replacement mapping provided. Focus on systematic, \
incremental changes with proper testing at each step.

#github-pull-request_copilot-coding-agent
"""

    def _generate_quality_improvement_task(
        self, quality_results: Dict[str, Any]
    ) -> AgenticTask:
        """Generate general quality improvement task"""
        overall_score = quality_results.get("overall_quality_score", {}).get(
            "overall_score", 1.0
        )
        grade = quality_results.get("overall_quality_score", {}).get(
            "grade", "Unknown"
        )

        return AgenticTask(
            task_id=f"quality_improvement_{uuid.uuid4().hex[:8]}",
            task_type=TaskType.QUALITY_IMPROVEMENT,
            priority=TaskPriority.MEDIUM,
            title=(f"System Quality Improvement - Grade {grade} "
                   f"({overall_score:.3f})"),
            description=(f"Comprehensive quality improvement for system "
                         f"currently graded {grade} with score "
                         f"{overall_score:.3f}"),
            instructions=[
                "Analyze system quality metrics and implement improvements",
                "Focus on measurable quality indicators",
                "Address structural and integration issues",
                "Improve code organization and maintainability",
            ],
            target_files=[],
            success_criteria=(f"Improve overall quality score from "
                              f"{overall_score:.3f} to >0.8 (Grade B+)"),
            rollback_plan=("Revert individual improvements if quality "
                           "score decreases"),
            estimated_changes=0,
            risk_level="MEDIUM",
            ai_prompt=("System quality improvement analysis and "
                       "implementation required."),
            metadata=quality_results,
            created_at=datetime.now().isoformat(),
        )

    def save_task_to_file(
        self, task: AgenticTask, filepath: Path = None
    ) -> Path:
        """Save agentic task to JSON file"""
        if filepath is None:
            filepath = (
                self.workspace_root
                / "ai"
                / "laboratory"
                / "runtime"
                / f"agentic_task_{task.task_id}.json"
            )

        filepath.parent.mkdir(parents=True, exist_ok=True)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(asdict(task), f, indent=2, default=str)

        return filepath

    def load_task_from_file(self, filepath: Path) -> AgenticTask:
        """Load agentic task from JSON file"""
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Convert enums back
        data["task_type"] = TaskType(data["task_type"])
        data["priority"] = TaskPriority(data["priority"])

        return AgenticTask(**data)


def main():
    """CLI entry point for testing"""
    print("AIOS Agentic Instruction Generator")
    print("=================================")

    # Example usage with mock emoji results
    generator = AgenticInstructionGenerator()

    mock_emoji_results = {
        "total_emojis": 46,
        "emoji_by_file": {
            ".githooks/README.md": [
                {"emoji": "", "line": 52, "context": "Real message queuing"},
                {
                    "emoji": "",
                    "line": 75,
                    "context": "43+ files in single directory",
                },
            ]
        },
        "emoji_frequency": {"": 33, "": 9, "": 2, "": 2},
        "analysis_timestamp": datetime.now().isoformat(),
    }

    task = generator.generate_from_emoji_analysis(mock_emoji_results)

    print(f"Generated Task: {task.title}")
    print(f"Priority: {task.priority.value}")
    print(f"Estimated Changes: {task.estimated_changes}")
    print(f"Target Files: {len(task.target_files)}")
    print()
    print("AI Prompt Preview:")
    print(task.ai_prompt[:500] + "...")

    # Save task example
    filepath = generator.save_task_to_file(task)
    print(f"Task saved to: {filepath}")


if __name__ == "__main__":
    main()
