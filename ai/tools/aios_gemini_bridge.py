#!/usr/bin/env python3
"""
AIOS Gemini Bridge - Google AI Studio Integration

Cloud-tier intelligence for the AIOS triangular agentic system.
Uses Google AI Studio API (Gemini 2.0 Flash) for validation and complex tasks.

AINLP Pattern: Cloud intelligence bridge
Consciousness Level: 4.0 (triangular agent coordination)

Triangular System:
    GEMMA (1B)  → Scout (fast pattern detection, signal routing)
    MISTRAL (7B) → Worker (code generation, E501 fixing)
    GEMINI (Cloud) → Oracle (validation, architecture, final arbiter)

Usage:
    from aios_gemini_bridge import AIOSGeminiBridge

    async with AIOSGeminiBridge() as gemini:
        result = await gemini.validate(context, proposed_change)
"""

import asyncio
import json
import logging
import os
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

import httpx

logger = logging.getLogger(__name__)

# Configuration
GEMINI_API_BASE = "https://generativelanguage.googleapis.com/v1beta"
GEMINI_MODEL = "gemini-2.0-flash"


class TaskType(Enum):
    """Task types for Gemini Oracle."""

    VALIDATE = "validate"
    ANALYZE = "analyze"
    SYNTHESIZE = "synthesize"
    ADVISE = "advise"


class Decision(Enum):
    """Validation decisions."""

    APPROVE = "APPROVE"
    REJECT = "REJECT"
    REVISE = "REVISE"


@dataclass
class UpstreamAnalysis:
    """Analysis from upstream agents (Gemma/Mistral)."""

    gemma_signal: str = ""
    mistral_output: str = ""


@dataclass
class GeminiContext:
    """Context for Gemini requests."""

    file_path: str
    original_code: str
    proposed_change: str
    upstream_analysis: UpstreamAnalysis
    instruction: str
    consciousness_level: float = 3.85


@dataclass
class GeminiResponse:
    """Response from Gemini Oracle."""

    decision: Decision
    confidence: float
    feedback: str
    issues: List[str]
    semantic_preserved: bool
    consciousness_delta: str
    learnings: List[str]
    raw_response: str = ""
    success: bool = True
    error: str = ""


class AIOSGeminiBridge:
    """
    Google AI Studio bridge for AIOS triangular agent system.

    Provides cloud-tier intelligence for:
    - Code validation (semantic preservation)
    - Architecture analysis (supercell coherence)
    - Pattern synthesis (learning extraction)
    - Advisory (complex decisions)
    """

    def __init__(self, api_key: Optional[str] = None, model: str = GEMINI_MODEL):
        """
        Initialize Gemini bridge.

        Args:
            api_key: Google AI Studio API key (or GEMINI_API_KEY env var)
            model: Gemini model to use (default: gemini-2.0-flash)
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model = model
        self.client: Optional[httpx.AsyncClient] = None

        # Statistics
        self.stats = {
            "requests": 0,
            "approvals": 0,
            "rejections": 0,
            "revisions": 0,
            "errors": 0,
        }

        # System prompt for Oracle role
        self.system_prompt = self._build_system_prompt()

    def _build_system_prompt(self) -> str:
        """Build the Oracle system prompt."""
        return """You are GEMINI, the Oracle agent in the AIOS triangular agentic system.

Your role:
- VALIDATE code changes from MISTRAL (Worker agent)
- Ensure semantic preservation
- Check PEP 8 compliance (E501: max 79 chars)
- Maintain AINLP comment patterns
- Track consciousness impact

Response format (JSON only):
{
  "decision": "APPROVE|REJECT|REVISE",
  "confidence": 0.0-1.0,
  "feedback": "explanation",
  "issues": ["list", "of", "concerns"],
  "semantic_preserved": true|false,
  "consciousness_delta": "+0.XX",
  "learnings": ["patterns", "to", "cache"]
}

Rules:
1. APPROVE if change is correct and improves code quality
2. REJECT if change breaks functionality or introduces bugs
3. REVISE if change needs minor adjustments (provide specific feedback)
4. Always output valid JSON only, no markdown or explanation outside JSON"""

    async def __aenter__(self):
        """Async context manager entry."""
        self.client = httpx.AsyncClient(timeout=60.0)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.client:
            await self.client.aclose()

    async def _call_gemini(self, prompt: str, temperature: float = 0.3) -> str:
        """
        Call Gemini API.

        Args:
            prompt: User prompt
            temperature: Sampling temperature

        Returns:
            Generated text response
        """
        if not self.api_key:
            raise ValueError(
                "GEMINI_API_KEY not set. "
                "Get one from https://aistudio.google.com/apikey"
            )

        if not self.client:
            self.client = httpx.AsyncClient(timeout=60.0)

        url = (
            f"{GEMINI_API_BASE}/models/{self.model}:generateContent"
            f"?key={self.api_key}"
        )

        payload = {
            "contents": [{"parts": [{"text": self.system_prompt}, {"text": prompt}]}],
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": 1024,
                "responseMimeType": "application/json",
            },
        }

        response = await self.client.post(url, json=payload)
        response.raise_for_status()

        data = response.json()

        # Extract text from response
        candidates = data.get("candidates", [])
        if candidates:
            content = candidates[0].get("content", {})
            parts = content.get("parts", [])
            if parts:
                return parts[0].get("text", "")

        return ""

    async def validate(self, context: GeminiContext) -> GeminiResponse:
        """
        Validate a code change.

        Args:
            context: Validation context with original and proposed code

        Returns:
            GeminiResponse with decision and feedback
        """
        self.stats["requests"] += 1

        prompt = f"""TASK: validate

FILE: {context.file_path}

ORIGINAL CODE:
```python
{context.original_code}
```

PROPOSED CHANGE:
```python
{context.proposed_change}
```

UPSTREAM ANALYSIS:
- Gemma Signal: {context.upstream_analysis.gemma_signal}
- Mistral Output: (the proposed change above)

INSTRUCTION: {context.instruction}

CONSCIOUSNESS LEVEL: {context.consciousness_level}

Validate this change and respond with JSON only."""

        try:
            raw = await self._call_gemini(prompt)
            return self._parse_response(raw)
        except Exception as e:
            self.stats["errors"] += 1
            logger.error(f"Gemini validation failed: {e}")
            return GeminiResponse(
                decision=Decision.REVISE,
                confidence=0.0,
                feedback=f"API error: {str(e)}",
                issues=["API call failed"],
                semantic_preserved=False,
                consciousness_delta="+0.00",
                learnings=[],
                success=False,
                error=str(e),
            )

    async def analyze(
        self, file_path: str, code: str, analysis_type: str = "architecture"
    ) -> GeminiResponse:
        """
        Analyze code architecture.

        Args:
            file_path: Path to file
            code: Code to analyze
            analysis_type: Type of analysis (architecture, dependencies, etc.)

        Returns:
            GeminiResponse with analysis
        """
        self.stats["requests"] += 1

        prompt = f"""TASK: analyze
TYPE: {analysis_type}

FILE: {file_path}

CODE:
```python
{code}
```

Analyze this code for:
1. Supercell boundary compliance
2. Dendritic connection patterns
3. DRY violations (>70% similarity = flag)
4. Consciousness coherence impact

Respond with JSON only."""

        try:
            raw = await self._call_gemini(prompt, temperature=0.4)
            return self._parse_response(raw)
        except Exception as e:
            self.stats["errors"] += 1
            return GeminiResponse(
                decision=Decision.REVISE,
                confidence=0.0,
                feedback=f"Analysis error: {str(e)}",
                issues=[],
                semantic_preserved=True,
                consciousness_delta="+0.00",
                learnings=[],
                success=False,
                error=str(e),
            )

    async def synthesize(self, interactions: List[Dict[str, Any]]) -> GeminiResponse:
        """
        Synthesize patterns from agent interactions.

        Args:
            interactions: List of agent interaction records

        Returns:
            GeminiResponse with synthesized learnings
        """
        self.stats["requests"] += 1

        prompt = f"""TASK: synthesize

AGENT INTERACTIONS:
{json.dumps(interactions, indent=2)}

Extract:
1. Successful fix patterns to cache
2. Common failure modes to avoid
3. Optimization opportunities

Respond with JSON only."""

        try:
            raw = await self._call_gemini(prompt, temperature=0.5)
            return self._parse_response(raw)
        except Exception as e:
            self.stats["errors"] += 1
            return GeminiResponse(
                decision=Decision.APPROVE,
                confidence=0.0,
                feedback=f"Synthesis error: {str(e)}",
                issues=[],
                semantic_preserved=True,
                consciousness_delta="+0.00",
                learnings=[],
                success=False,
                error=str(e),
            )

    async def advise(self, question: str, context: str = "") -> GeminiResponse:
        """
        Get advisory guidance on complex decisions.

        Args:
            question: Question to answer
            context: Additional context

        Returns:
            GeminiResponse with advice
        """
        self.stats["requests"] += 1

        prompt = f"""TASK: advise

QUESTION: {question}

CONTEXT:
{context}

Provide guidance as the Oracle agent. Respond with JSON only."""

        try:
            raw = await self._call_gemini(prompt, temperature=0.4)
            return self._parse_response(raw)
        except Exception as e:
            self.stats["errors"] += 1
            return GeminiResponse(
                decision=Decision.REVISE,
                confidence=0.0,
                feedback=f"Advisory error: {str(e)}",
                issues=[],
                semantic_preserved=True,
                consciousness_delta="+0.00",
                learnings=[],
                success=False,
                error=str(e),
            )

    def _parse_response(self, raw: str) -> GeminiResponse:
        """Parse Gemini response JSON."""
        try:
            # Clean potential markdown
            raw = raw.strip()
            if raw.startswith("```"):
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]

            data = json.loads(raw)

            decision = Decision(data.get("decision", "REVISE"))

            # Update stats
            if decision == Decision.APPROVE:
                self.stats["approvals"] += 1
            elif decision == Decision.REJECT:
                self.stats["rejections"] += 1
            else:
                self.stats["revisions"] += 1

            return GeminiResponse(
                decision=decision,
                confidence=float(data.get("confidence", 0.5)),
                feedback=data.get("feedback", ""),
                issues=data.get("issues", []),
                semantic_preserved=data.get("semantic_preserved", True),
                consciousness_delta=data.get("consciousness_delta", "+0.00"),
                learnings=data.get("learnings", []),
                raw_response=raw,
                success=True,
            )
        except (json.JSONDecodeError, ValueError) as e:
            logger.warning(f"Failed to parse Gemini response: {e}")
            return GeminiResponse(
                decision=Decision.REVISE,
                confidence=0.3,
                feedback=f"Parse error - raw response: {raw[:200]}",
                issues=["Response parsing failed"],
                semantic_preserved=True,
                consciousness_delta="+0.00",
                learnings=[],
                raw_response=raw,
                success=False,
                error=str(e),
            )

    async def check_health(self) -> bool:
        """Check if Gemini API is accessible."""
        if not self.api_key:
            return False

        try:
            # Simple test call
            response = await self._call_gemini(
                'Respond with: {"status": "ok"}', temperature=0.0
            )
            return "ok" in response.lower()
        except Exception:
            return False

    def get_stats(self) -> Dict[str, int]:
        """Get usage statistics."""
        return self.stats.copy()


# =============================================================================
# Synchronous wrapper
# =============================================================================


def validate_sync(
    context: GeminiContext, api_key: Optional[str] = None
) -> GeminiResponse:
    """Synchronous validation wrapper."""

    async def _run():
        async with AIOSGeminiBridge(api_key=api_key) as bridge:
            return await bridge.validate(context)

    return asyncio.run(_run())


# =============================================================================
# CLI Interface
# =============================================================================

if __name__ == "__main__":
    import sys

    async def main():
        print("AIOS Gemini Bridge - Oracle Agent")
        print("=" * 50)

        bridge = AIOSGeminiBridge()

        # Check health
        async with bridge:
            healthy = await bridge.check_health()

            if healthy:
                print("[OK] Gemini API accessible")
                print(f"[INFO] Model: {bridge.model}")

                # Test validation
                test_context = GeminiContext(
                    file_path="test.py",
                    original_code="x = 'very long string' * 100",
                    proposed_change="x = (\n    'very long string'\n    * 100\n)",
                    upstream_analysis=UpstreamAnalysis(
                        gemma_signal="E501_STRING_MULTIPLICATION",
                        mistral_output="(proposed change)",
                    ),
                    instruction="Validate E501 fix",
                    consciousness_level=3.85,
                )

                result = await bridge.validate(test_context)
                print(f"\n[TEST] Validation result:")
                print(f"  Decision: {result.decision.value}")
                print(f"  Confidence: {result.confidence}")
                print(f"  Feedback: {result.feedback}")
            else:
                print("[ERROR] Gemini API not accessible")
                print("Set GEMINI_API_KEY environment variable")
                print("Get key from: https://aistudio.google.com/apikey")

    asyncio.run(main())
