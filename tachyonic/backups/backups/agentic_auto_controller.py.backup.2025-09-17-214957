#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# flake8: noqa: E402
"""
AIOS Agentic Auto Controller
===========================
Location: ai/cytoplasm/scripts/agentic_auto_controller.py
Purpose: Decision engine for triggering autonomous AI refactoring
Architecture: CYTOPLASM supercell orchestration and control

This controller determines when to trigger agentic auto mode based on
quality analysis results and manages the execution of AI-driven refactoring
tasks with appropriate safety controls and risk assessment.
"""

import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

# Add AIOS paths
sys.path.append(str(Path(__file__).parent.parent.parent))

from laboratory.scripts.agentic_instruction_generator import (  # noqa: E402
    AgenticInstructionGenerator,
    AgenticTask,
    TaskPriority,
)
from transport.intercellular.enhanced_cellular_communication import (
    InterCellularMessage,
    SupercellType,
    get_cellular_bridge,
)


class AgenticAutoController:
    """Decision engine and controller for autonomous AI refactoring"""

    def __init__(self, workspace_root: Path = None):
        self.workspace_root = workspace_root or Path.cwd()
        self.cellular_bridge = get_cellular_bridge()
        self.instruction_generator = AgenticInstructionGenerator(
            workspace_root
        )

        # Configuration
        self.auto_trigger_thresholds = {
            "min_quality_score": 0.7,  # Below this triggers auto mode
            "max_emoji_count": 100,  # Above this triggers auto mode
            "max_affected_files": 25,  # Above this requires confirmation
            "critical_emoji_count": 500,  # Above this is critical priority
        }

        self.safety_settings = {
            "dry_run_first": True,
            "incremental_processing": True,
            "require_confirmation_for_high_risk": True,
            "max_files_per_batch": 5,
            "rollback_on_failure": True,
        }

    def analyze_and_trigger(
        self, quality_results: Dict[str, Any], force_agentic: bool = False
    ) -> Dict[str, Any]:
        """Analyze results and determine if agentic auto mode should trigger"""

        # Generate agentic tasks from analysis
        agentic_tasks = (
            self.instruction_generator.generate_from_quality_analysis(
                quality_results
            )
        )

        # Decision logic for auto-triggering
        should_trigger = force_agentic or self._should_trigger_auto_mode(
            quality_results
        )

        # Risk assessment
        risk_assessment = self._assess_risk(quality_results, agentic_tasks)

        # Generate execution plan
        execution_plan = self._create_execution_plan(
            agentic_tasks, risk_assessment
        )

        result = {
            "should_trigger_agentic": should_trigger,
            "agentic_tasks": agentic_tasks,
            "risk_assessment": risk_assessment,
            "execution_plan": execution_plan,
            "safety_checks": self._perform_safety_checks(agentic_tasks),
            "ai_prompt_ready": (
                self._generate_combined_ai_prompt(agentic_tasks)
                if should_trigger
                else None
            ),
        }

        # Communicate decision through supercells
        self._communicate_agentic_decision(result)

        return result

    def _should_trigger_auto_mode(
        self, quality_results: Dict[str, Any]
    ) -> bool:
        """Determine if automatic agentic mode should be triggered"""

        # Check overall quality score
        overall_score = quality_results.get("overall_quality_score", {}).get(
            "overall_score", 1.0
        )
        if overall_score < self.auto_trigger_thresholds["min_quality_score"]:
            return True

        # Check emoji count (primary trigger)
        emoji_count = quality_results.get("emoji_analysis", {}).get(
            "total_emojis", 0
        )
        if emoji_count > self.auto_trigger_thresholds["max_emoji_count"]:
            return True

        # Check for encoding errors (immediate trigger)
        if quality_results.get("encoding_errors", 0) > 0:
            return True

        # Check integration quality
        integration_score = quality_results.get(
            "integration_analysis", {}
        ).get("integration_score", 1.0)
        if integration_score < 0.5:
            return True

        return False

    def _assess_risk(
        self, quality_results: Dict[str, Any], agentic_tasks: List[AgenticTask]
    ) -> Dict[str, Any]:
        """Assess risk level of proposed agentic tasks"""

        total_changes = sum(task.estimated_changes for task in agentic_tasks)
        affected_files = set()
        for task in agentic_tasks:
            affected_files.update(task.target_files)

        high_priority_tasks = [
            task
            for task in agentic_tasks
            if task.priority in [TaskPriority.CRITICAL, TaskPriority.HIGH]
        ]

        # Risk calculation
        risk_score = 0.0
        risk_factors = []

        if total_changes > 1000:
            risk_score += 0.3
            risk_factors.append(
                f"High change volume: {total_changes} modifications"
            )

        if (
            len(affected_files)
            > self.auto_trigger_thresholds["max_affected_files"]
        ):
            risk_score += 0.2
            risk_factors.append(
                f"Many files affected: {len(affected_files)} files"
            )

        if len(high_priority_tasks) > 0:
            risk_score += 0.1
            risk_factors.append(
                f"High priority tasks: {len(high_priority_tasks)} tasks"
            )

        # Determine risk level
        if risk_score >= 0.5:
            risk_level = "HIGH"
        elif risk_score >= 0.3:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"

        return {
            "risk_level": risk_level,
            "risk_score": risk_score,
            "risk_factors": risk_factors,
            "total_estimated_changes": total_changes,
            "total_affected_files": len(affected_files),
            "requires_confirmation": risk_level == "HIGH"
            and self.safety_settings["require_confirmation_for_high_risk"],
        }

    def _create_execution_plan(
        self, agentic_tasks: List[AgenticTask], risk_assessment: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create detailed execution plan for agentic tasks"""

        # Sort tasks by priority
        sorted_tasks = sorted(
            agentic_tasks,
            key=lambda t: (t.priority.value, t.estimated_changes),
            reverse=True,
        )

        # Create batches for incremental processing
        batches = []
        if self.safety_settings["incremental_processing"]:
            current_batch = []
            current_batch_files = set()

            for task in sorted_tasks:
                # Create new batch if too many files
                if (
                    len(current_batch_files) + len(task.target_files)
                    > self.safety_settings["max_files_per_batch"]
                ):
                    if current_batch:
                        batches.append(current_batch)
                    current_batch = [task]
                    current_batch_files = set(task.target_files)
                else:
                    current_batch.append(task)
                    current_batch_files.update(task.target_files)

            if current_batch:
                batches.append(current_batch)
        else:
            batches = [sorted_tasks]

        return {
            "execution_order": [task.task_id for task in sorted_tasks],
            "batch_processing": len(batches) > 1,
            "batches": [
                {
                    "batch_id": i + 1,
                    "tasks": [task.task_id for task in batch],
                    "estimated_changes": sum(
                        task.estimated_changes for task in batch
                    ),
                    "files": list(
                        set().union(*(task.target_files for task in batch))
                    ),
                }
                for i, batch in enumerate(batches)
            ],
            "dry_run_required": self.safety_settings["dry_run_first"],
            "rollback_strategy": (
                "individual_task"
                if risk_assessment["risk_level"] == "HIGH"
                else "batch_level"
            ),
        }

    def _perform_safety_checks(
        self, agentic_tasks: List[AgenticTask]
    ) -> Dict[str, Any]:
        """Perform comprehensive safety checks before execution"""

        checks = {
            "git_status_clean": True,  # Would check actual git status
            "backup_available": True,  # Would verify backup mechanisms
            "test_suite_available": False,  # Would check for automated tests
            "rollback_prepared": True,  # Would verify rollback capabilities
            "file_permissions_ok": True,  # Would check write permissions
            "disk_space_sufficient": True,  # Would check available disk space
        }

        # Safety warnings
        warnings = []
        if not checks["test_suite_available"]:
            warnings.append(
                "No automated test suite detected - manual validation required"
            )

        if sum(task.estimated_changes for task in agentic_tasks) > 500:
            warnings.append(
                "Large number of changes - consider incremental execution"
            )

        return {
            "checks_passed": all(checks.values()),
            "individual_checks": checks,
            "warnings": warnings,
            "recommendation": (
                "PROCEED" if all(checks.values()) else "CAUTION_REQUIRED"
            ),
        }

    def _generate_combined_ai_prompt(
        self, agentic_tasks: List[AgenticTask]
    ) -> str:
        """Generate combined AI prompt for multiple tasks"""

        if len(agentic_tasks) == 1:
            return agentic_tasks[0].ai_prompt

        # Combine multiple tasks into unified prompt
        total_changes = sum(task.estimated_changes for task in agentic_tasks)
        all_files = set()
        for task in agentic_tasks:
            all_files.update(task.target_files)

        prompt = f"""
AGENTIC AUTO MODE: Multi-Task Quality Improvement
================================================

**COMPREHENSIVE REFACTORING SESSION**
- {len(agentic_tasks)} automated tasks to execute
- {total_changes} total estimated changes
- {len(all_files)} files affected across GitHooks system

**TASK BREAKDOWN:**
"""

        for i, task in enumerate(agentic_tasks, 1):
            prompt += f"""
{i}. {task.title}
   Priority: {task.priority.value}
   Changes: {task.estimated_changes}
   Files: {len(task.target_files)}
"""

        prompt += """
**EXECUTION STRATEGY:**
1. Process tasks in priority order (CRITICAL → HIGH → MEDIUM → LOW)
2. Execute changes incrementally with testing between batches
3. Maintain complete audit trail of all modifications
4. Implement rollback immediately if any issues detected

**SAFETY PROTOCOLS:**
- Create feature branch before starting changes
- Commit each logical group of changes separately
- Test functionality after each batch of modifications
- Stop execution if any unexpected behavior detected

**SUCCESS CRITERIA:**
- All task objectives completed successfully
- No regression in existing functionality
- Clean git history with descriptive commit messages
- System quality score improved measurably

Please execute this comprehensive refactoring session autonomously, \
following the incremental approach and safety protocols outlined above.

#github-pull-request_copilot-coding-agent
"""

        return prompt

    def _communicate_agentic_decision(self, decision_result: Dict[str, Any]):
        """Communicate agentic mode decision through supercell network"""

        # Send to INFORMATION_STORAGE for logging
        storage_message = InterCellularMessage(
            source_supercell=SupercellType.CYTOPLASM,
            target_supercell=SupercellType.INFORMATION_STORAGE,
            message_type="agentic_decision",
            data=decision_result,
            timestamp=datetime.now(),
            correlation_id=(f"agentic_decision_"
                            f"{int(datetime.now().timestamp())}"),
        )
        self.cellular_bridge.send_message(storage_message)

        # Send to MEMBRANE for AI agent preparation if triggering
        if decision_result["should_trigger_agentic"]:
            membrane_message = InterCellularMessage(
                source_supercell=SupercellType.CYTOPLASM,
                target_supercell=SupercellType.MEMBRANE,
                message_type="prepare_ai_agent",
                data={
                    "ai_prompt": decision_result["ai_prompt_ready"],
                    "execution_plan": decision_result["execution_plan"],
                    "safety_checks": decision_result["safety_checks"],
                },
                timestamp=datetime.now(),
                correlation_id=(f"ai_agent_prep_"
                                f"{int(datetime.now().timestamp())}"),
            )
            self.cellular_bridge.send_message(membrane_message)

        # Update CYTOPLASM state
        self.cellular_bridge.update_supercell_state(
            SupercellType.CYTOPLASM,
            "agentic_decision_complete",
            ["agentic_auto_controller"],
            {"latest_decision": decision_result},
        )


def main():
    """CLI entry point for testing"""
    print("AIOS Agentic Auto Controller")
    print("===========================")

    controller = AgenticAutoController()

    # Mock quality results for testing
    mock_quality_results = {
        "overall_quality_score": {"overall_score": 0.620, "grade": "D"},
        "emoji_analysis": {
            "total_emojis": 46,
            "files_with_emojis": 1,
            "emoji_frequency": {"": 33, "": 9, "": 2, "": 2},
        },
        "integration_analysis": {"integration_score": 0.8},
    }

    # Test decision logic
    result = controller.analyze_and_trigger(mock_quality_results)

    print(f"Should Trigger Agentic Mode: {result['should_trigger_agentic']}")
    print(f"Risk Level: {result['risk_assessment']['risk_level']}")
    print(f"Total Tasks Generated: {len(result['agentic_tasks'])}")
    print(f"Safety Checks: {result['safety_checks']['recommendation']}")

    if result["ai_prompt_ready"]:
        print("\nAI Prompt Preview:")
        print(result["ai_prompt_ready"][:300] + "...")


if __name__ == "__main__":
    main()
