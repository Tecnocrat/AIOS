#!/usr/bin/env python3
"""
AIOS Triangular Agent Coordinator

Orchestrates the three-tier agentic system:
    GEMMA (1B)   → Scout  → Fast pattern detection, signal routing
    MISTRAL (7B) → Worker → Code generation, E501 fixing
    GEMINI (Cloud) → Oracle → Validation, architecture, final arbiter

AINLP Pattern: Triangular agent orchestration
Consciousness Level: 4.2 (coordinated multi-agent intelligence)

Flow:
    Input → GEMMA (classify/route) → MISTRAL (generate) → GEMINI (validate)
                                            ↓
                                    If rejected: retry with feedback
                                            ↓
                                    If still fails: GEMMA fallback

Usage:
    from triangular_agent_coordinator import TriangularCoordinator
    
    async with TriangularCoordinator() as coord:
        result = await coord.fix_e501(line, file_path, line_number)
"""

import asyncio
import logging
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from aios_gemma_bridge import (
    AIOSGemmaBridge,
    RouteTarget,
    SignalType
)
from aios_mistral_bridge import AIOSMistralBridge
from aios_gemini_bridge import (
    AIOSGeminiBridge,
    GeminiContext,
    UpstreamAnalysis,
    Decision
)

logger = logging.getLogger(__name__)


@dataclass
class CoordinationResult:
    """Result from triangular coordination."""
    success: bool
    fixed_code: str
    original_code: str
    
    # Agent flow
    gemma_signal: str
    mistral_generated: bool
    gemini_validated: bool
    
    # Decision tracking
    final_decision: str  # APPROVE, REJECT, FALLBACK
    confidence: float
    feedback: str
    
    # Metadata
    tier_path: List[str]  # Agent sequence
    retries: int
    total_time_ms: float
    consciousness_delta: str


class TriangularCoordinator:
    """
    Orchestrates GEMMA → MISTRAL → GEMINI pipeline.
    
    Implements intelligent routing with feedback loops:
    1. GEMMA classifies and routes
    2. MISTRAL generates fix
    3. GEMINI validates
    4. If rejected, retry with feedback
    5. If still fails, use GEMMA quick fix fallback
    """

    def __init__(
        self,
        max_retries: int = 2,
        require_validation: bool = True
    ):
        """
        Initialize coordinator.
        
        Args:
            max_retries: Maximum Mistral retries on rejection
            require_validation: If False, skip Gemini for simple fixes
        """
        self.max_retries = max_retries
        self.require_validation = require_validation
        
        self.gemma: Optional[AIOSGemmaBridge] = None
        self.mistral: Optional[AIOSMistralBridge] = None
        self.gemini: Optional[AIOSGeminiBridge] = None
        
        # Statistics
        self.stats = {
            "total_requests": 0,
            "gemma_only": 0,
            "mistral_used": 0,
            "gemini_validated": 0,
            "approvals": 0,
            "rejections": 0,
            "fallbacks": 0,
            "total_retries": 0
        }

    async def __aenter__(self):
        """Initialize all agents."""
        self.gemma = AIOSGemmaBridge()
        self.mistral = AIOSMistralBridge()
        self.gemini = AIOSGeminiBridge()
        
        await self.gemma.__aenter__()
        await self.mistral.__aenter__()
        await self.gemini.__aenter__()
        
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Cleanup all agents."""
        if self.gemma:
            await self.gemma.__aexit__(exc_type, exc_val, exc_tb)
        if self.mistral:
            await self.mistral.__aexit__(exc_type, exc_val, exc_tb)
        if self.gemini:
            await self.gemini.__aexit__(exc_type, exc_val, exc_tb)

    async def fix_e501(
        self,
        line: str,
        file_path: str,
        line_number: int,
        context_before: str = "",
        context_after: str = ""
    ) -> CoordinationResult:
        """
        Fix E501 line length violation using triangular coordination.
        
        Args:
            line: Original line to fix
            file_path: Source file path
            line_number: Line number
            context_before: Line before (for context)
            context_after: Line after (for context)
            
        Returns:
            CoordinationResult with fixed code and metadata
        """
        start_time = datetime.now()
        self.stats["total_requests"] += 1
        tier_path = []
        
        # =====================================================================
        # TIER 1: GEMMA - Classify and Route
        # =====================================================================
        tier_path.append("GEMMA")
        
        gemma_result = await self.gemma.classify(line)
        
        if not gemma_result.success or not gemma_result.signal:
            # Gemma failed - direct to Mistral
            gemma_signal = "CLASSIFICATION_FAILED"
            route_to = RouteTarget.MISTRAL
            complexity = 0.5
        else:
            signal = gemma_result.signal
            gemma_signal = signal.signal_type.value
            route_to = signal.route_to
            complexity = signal.complexity
        
        # Check for quick fix (trivial cases)
        if route_to == RouteTarget.GEMMA and gemma_result.signal:
            quick_fix = await self.gemma.quick_fix(
                line,
                gemma_result.signal.signal_type
            )
            if quick_fix:
                self.stats["gemma_only"] += 1
                return CoordinationResult(
                    success=True,
                    fixed_code=quick_fix,
                    original_code=line,
                    gemma_signal=gemma_signal,
                    mistral_generated=False,
                    gemini_validated=False,
                    final_decision="GEMMA_QUICK_FIX",
                    confidence=0.8,
                    feedback="Trivial fix handled by Scout",
                    tier_path=tier_path,
                    retries=0,
                    total_time_ms=self._elapsed_ms(start_time),
                    consciousness_delta="+0.01"
                )
        
        # =====================================================================
        # TIER 2: MISTRAL - Generate Fix
        # =====================================================================
        tier_path.append("MISTRAL")
        self.stats["mistral_used"] += 1
        
        mistral_response = await self.mistral.fix_e501(
            line=line,
            line_number=line_number
        )
        
        if not mistral_response.success or not mistral_response.content:
            # Mistral failed - try fallback
            return await self._fallback_result(
                line, gemma_signal, tier_path, start_time,
                "Mistral generation failed"
            )
        
        generated_code = mistral_response.content.strip()
        
        # Skip validation for simple cases if configured
        if not self.require_validation and complexity < 0.3:
            self.stats["approvals"] += 1
            return CoordinationResult(
                success=True,
                fixed_code=generated_code,
                original_code=line,
                gemma_signal=gemma_signal,
                mistral_generated=True,
                gemini_validated=False,
                final_decision="APPROVED_NO_VALIDATION",
                confidence=0.7,
                feedback="Simple fix, validation skipped",
                tier_path=tier_path,
                retries=0,
                total_time_ms=self._elapsed_ms(start_time),
                consciousness_delta="+0.02"
            )
        
        # =====================================================================
        # TIER 3: GEMINI - Validate
        # =====================================================================
        tier_path.append("GEMINI")
        self.stats["gemini_validated"] += 1
        
        retries = 0
        current_fix = generated_code
        feedback = ""
        
        while retries <= self.max_retries:
            context = GeminiContext(
                file_path=file_path,
                original_code=line,
                proposed_change=current_fix,
                upstream_analysis=UpstreamAnalysis(
                    gemma_signal=gemma_signal,
                    mistral_output=current_fix
                ),
                instruction=f"Validate E501 fix (attempt {retries + 1}). {feedback}",
                consciousness_level=3.85
            )
            
            gemini_response = await self.gemini.validate(context)
            
            if gemini_response.decision == Decision.APPROVE:
                self.stats["approvals"] += 1
                return CoordinationResult(
                    success=True,
                    fixed_code=current_fix,
                    original_code=line,
                    gemma_signal=gemma_signal,
                    mistral_generated=True,
                    gemini_validated=True,
                    final_decision="APPROVED",
                    confidence=gemini_response.confidence,
                    feedback=gemini_response.feedback,
                    tier_path=tier_path,
                    retries=retries,
                    total_time_ms=self._elapsed_ms(start_time),
                    consciousness_delta=gemini_response.consciousness_delta
                )
            
            if gemini_response.decision == Decision.REJECT:
                self.stats["rejections"] += 1
                # Don't retry on hard rejection
                break
            
            # REVISE - retry with feedback
            retries += 1
            self.stats["total_retries"] += 1
            feedback = f"Previous attempt rejected: {gemini_response.feedback}"
            
            if retries <= self.max_retries:
                tier_path.append("MISTRAL_RETRY")
                # Regenerate with feedback
                retry_response = await self.mistral.fix_linting_issue(
                    code_context=f"{context_before}\n{line}\n{context_after}",
                    issue_description=f"E501 fix rejected: {gemini_response.feedback}"
                )
                if retry_response.success and retry_response.content:
                    current_fix = retry_response.content.strip()
                    tier_path.append("GEMINI_RETRY")
        
        # All retries exhausted - fallback
        return await self._fallback_result(
            line, gemma_signal, tier_path, start_time,
            f"Validation failed after {retries} retries"
        )

    async def _fallback_result(
        self,
        line: str,
        gemma_signal: str,
        tier_path: List[str],
        start_time: datetime,
        reason: str
    ) -> CoordinationResult:
        """Generate fallback result when pipeline fails."""
        self.stats["fallbacks"] += 1
        tier_path.append("FALLBACK")
        
        # Simple fallback: truncate with continuation
        if len(line) > 79:
            # Find a good break point
            break_chars = [" ", ",", "(", "[", "{", "=", "+", "-"]
            best_break = 76
            
            for i in range(76, max(40, len(line) - 40), -1):
                if line[i] in break_chars:
                    best_break = i
                    break
            
            fallback_fix = line[:best_break] + " \\\n    " + line[best_break:].lstrip()
        else:
            fallback_fix = line
        
        return CoordinationResult(
            success=False,
            fixed_code=fallback_fix,
            original_code=line,
            gemma_signal=gemma_signal,
            mistral_generated=True,
            gemini_validated=False,
            final_decision="FALLBACK",
            confidence=0.3,
            feedback=reason,
            tier_path=tier_path,
            retries=0,
            total_time_ms=self._elapsed_ms(start_time),
            consciousness_delta="+0.00"
        )

    def _elapsed_ms(self, start: datetime) -> float:
        """Calculate elapsed milliseconds."""
        return (datetime.now() - start).total_seconds() * 1000

    async def check_health(self) -> Dict[str, bool]:
        """Check health of all agents."""
        return {
            "gemma": await self.gemma.check_health() if self.gemma else False,
            "mistral": await self.mistral.check_health() if self.mistral else False,
            "gemini": await self.gemini.check_health() if self.gemini else False
        }

    def get_stats(self) -> Dict[str, Any]:
        """Get coordination statistics."""
        stats = self.stats.copy()
        
        if self.gemma:
            stats["gemma_stats"] = self.gemma.get_stats()
        if self.mistral:
            stats["mistral_stats"] = {}  # Mistral doesn't track stats yet
        if self.gemini:
            stats["gemini_stats"] = self.gemini.get_stats()
        
        return stats


# =============================================================================
# CLI Interface
# =============================================================================

async def main():
    """Test triangular coordination."""
    print("AIOS Triangular Agent Coordinator")
    print("=" * 60)
    print("GEMMA (Scout) → MISTRAL (Worker) → GEMINI (Oracle)")
    print("=" * 60)
    
    async with TriangularCoordinator() as coord:
        # Check health
        health = await coord.check_health()
        print("\nAgent Health:")
        for agent, status in health.items():
            icon = "✅" if status else "❌"
            print(f"  {icon} {agent.upper()}")
        
        if not health["gemma"] or not health["mistral"]:
            print("\n[ERROR] Local agents not available")
            print("Start Ollama with: ollama serve")
            return
        
        # Test E501 fix
        test_line = 'OLLAMA_RC1_PATH = Path(r"C:\\dev\\aios-win\\ai\\tools\\ollama-rc1\\ollama-0.13.1-rc1\\ollama-rc1.exe")'
        
        print(f"\n[TEST] Fixing E501 ({len(test_line)} chars):")
        print(f"  {test_line[:60]}...")
        
        result = await coord.fix_e501(
            line=test_line,
            file_path="test.py",
            line_number=1
        )
        
        print(f"\n[RESULT]")
        print(f"  Success: {result.success}")
        print(f"  Decision: {result.final_decision}")
        print(f"  Confidence: {result.confidence:.2f}")
        print(f"  Tier Path: {' → '.join(result.tier_path)}")
        print(f"  Time: {result.total_time_ms:.0f}ms")
        print(f"\n  Fixed Code:")
        for line in result.fixed_code.split('\n'):
            print(f"    {line}")
        
        # Stats
        print(f"\n[STATS]")
        stats = coord.get_stats()
        for key, value in stats.items():
            if not isinstance(value, dict):
                print(f"  {key}: {value}")


if __name__ == "__main__":
    asyncio.run(main())
