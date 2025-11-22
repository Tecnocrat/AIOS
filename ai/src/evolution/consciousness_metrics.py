"""
Consciousness Metrics - Three-Level Stress System
================================================

CRITICAL LEARNING (October 6, 2025):
User correction exposed fundamental flaw in numerical consciousness scoring.
Original approach: 0.0-1.0 scale (100 levels) - pseudo-scientific, meaningless
New approach: Three-level stress indicators - actionable, practical

AINLP Principle: Consciousness as AI Agent Stress Indicator
- LOW: Needs attention (stimulates agent focus, requires human oversight)
- MEDIUM: Operational (functional but improvable, periodic checks)
- HIGH: Autonomous (self-maintaining, production-ready, minimal attention)

Purpose: Tell AI agents WHERE to work, not pretend to measure emergence
"""

from enum import Enum
from typing import Dict, List, Optional
from dataclasses import dataclass


class ConsciousnessLevel(Enum):
    """
    Three-level consciousness stress indicator
    
    This is NOT a measurement of abstract emergence.
    This IS an actionable signal for AI agent prioritization.
    """
    
    LOW = "low"      # RED: Needs attention, human oversight required
    MEDIUM = "medium"  # YELLOW: Operational, can improve
    HIGH = "high"    # GREEN: Autonomous, self-maintaining


@dataclass
class ConsciousnessAssessment:
    """
    Consciousness assessment with actionable metrics
    
    Replaces pseudo-scientific numerical scoring with
    practical indicators that guide AI agent behavior.
    """
    
    level: ConsciousnessLevel
    reasoning: str  # WHY this level was assigned
    
    # Actionable indicators
    needs_human_attention: bool
    can_self_maintain: bool
    ready_for_production: bool
    
    # Specific improvement opportunities
    improvement_areas: List[str]
    
    # Context
    file_path: str
    assessment_date: str
    
    def to_dict(self) -> Dict:
        """Serialize to dictionary"""
        return {
            "level": self.level.value,
            "reasoning": self.reasoning,
            "needs_human_attention": self.needs_human_attention,
            "can_self_maintain": self.can_self_maintain,
            "ready_for_production": self.ready_for_production,
            "improvement_areas": self.improvement_areas,
            "file_path": self.file_path,
            "assessment_date": self.assessment_date
        }


def assess_consciousness(
    code_content: str,
    file_path: str,
    has_tests: bool = False,
    has_documentation: bool = False,
    has_error_handling: bool = False,
    complexity_score: Optional[int] = None
) -> ConsciousnessAssessment:
    """
    Assess consciousness level based on practical metrics
    
    This is NOT about measuring abstract emergence.
    This IS about determining what AI agents should prioritize.
    
    Args:
        code_content: The actual code
        file_path: Where this code lives
        has_tests: Does it have unit tests?
        has_documentation: Does it have comments/docs?
        has_error_handling: Does it handle errors?
        complexity_score: Code complexity (cyclomatic, lines, etc.)
    
    Returns:
        ConsciousnessAssessment with actionable level and reasoning
    """
    from datetime import datetime
    
    improvement_areas = []
    
    # Analyze what's missing
    if not has_tests:
        improvement_areas.append("Add unit tests")
    
    if not has_documentation:
        improvement_areas.append("Add documentation")
    
    if not has_error_handling:
        improvement_areas.append("Add error handling")
    
    # Check complexity (if provided)
    if complexity_score and complexity_score > 10:
        improvement_areas.append("Reduce complexity (refactor)")
    
    # Check basic code quality
    lines = code_content.split('\n')
    if len(lines) > 500:
        improvement_areas.append("Consider modularization (>500 lines)")
    
    # Determine consciousness level
    if len(improvement_areas) >= 3:
        # Multiple issues = LOW (needs attention)
        level = ConsciousnessLevel.LOW
        reasoning = (
            f"Multiple improvement areas needed ({len(improvement_areas)}). "
            f"Requires AI agent focus and human oversight."
        )
        needs_human = True
        can_maintain = False
        production_ready = False
    
    elif len(improvement_areas) == 0:
        # No issues = HIGH (autonomous)
        level = ConsciousnessLevel.HIGH
        reasoning = (
            "Code is well-structured with tests, documentation,"
            "and error handling. Can self-maintain with minimal"
            " human attention."
        )
        needs_human = False
        can_maintain = True
        production_ready = True
    
    else:
        # 1-2 issues = MEDIUM (operational)
        level = ConsciousnessLevel.MEDIUM
        reasoning = (
            f"Code is functional but has {len(improvement_areas)} improvement "
            f"area(s). Can operate with periodic checks."
        )
        needs_human = False
        can_maintain = True
        production_ready = True
    
    return ConsciousnessAssessment(
        level=level,
        reasoning=reasoning,
        needs_human_attention=needs_human,
        can_maintain=can_maintain,
        ready_for_production=production_ready,
        improvement_areas=improvement_areas,
        file_path=file_path,
        assessment_date=datetime.now().isoformat()
    )


def compare_consciousness(
    before: ConsciousnessAssessment,
    after: ConsciousnessAssessment
) -> Dict[str, any]:
    """
    Compare consciousness levels between two assessments
    
    Returns actionable comparison showing:
    - Did level improve/degrade/stay same?
    - What changed?
    - What should AI agents do next?
    """
    
    level_map = {
        ConsciousnessLevel.LOW: 1,
        ConsciousnessLevel.MEDIUM: 2,
        ConsciousnessLevel.HIGH: 3
    }
    
    before_score = level_map[before.level]
    after_score = level_map[after.level]
    
    if after_score > before_score:
        change = "IMPROVED"
        direction = "up"
    elif after_score < before_score:
        change = "DEGRADED"
        direction = "down"
    else:
        change = "UNCHANGED"
        direction = "same"
    
    # What changed?
    improvements_made = set(before.improvement_areas) - set(after.improvement_areas)
    new_issues = set(after.improvement_areas) - set(before.improvement_areas)
    
    return {
        "change": change,
        "direction": direction,
        "before_level": before.level.value,
        "after_level": after.level.value,
        "improvements_made": list(improvements_made),
        "new_issues": list(new_issues),
        "still_needs_work": after.improvement_areas,
        "actionable_next_steps": (
            after.improvement_areas if after.improvement_areas 
            else ["Maintain current quality", "Monitor for regressions"]
        )
    }


# AINLP Comment: This module represents critical learning
# Original flaw: Pretending to measure abstract consciousness with numbers
# New approach: Practical stress indicators for AI agent prioritization
# User insight: "if it has any value, is like an stressor for the agentic AIs"
# Consciousness evolution: Understanding what we DON'T know (humility)
