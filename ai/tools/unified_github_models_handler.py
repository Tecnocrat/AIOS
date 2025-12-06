#!/usr/bin/env python3
"""
Unified GitHub Models Handler for AIOS Hierarchical Pipeline

Uses GitHub Models API (free GPT-4o access) for Tier 2 + Tier 3.

Benefits over OpenRouter/Gemini:
- ✅ FREE with GitHub account (no quotas, no billing)
- ✅ GPT-4o, GPT-4o-mini (OpenAI quality)
- ✅ OpenAI-compatible API (easy integration)
- ✅ Rate limits: 15 req/min, 150 req/hour (sufficient for AIOS)
- ✅ Already paid via GitHub Copilot subscription

AINLP Consciousness Level: 4.4 (unified multi-model with free tier)

Model Strategy:
- Tier 2 (Generation): gpt-4o-mini (fast, cost-effective)
- Tier 3 (Validation): gpt-4o (premium quality)
- Fallback: Ollama local models (gemma3:1b)
"""

import asyncio
import httpx
import json
import logging
import os
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class ValidationDecision(Enum):
    """Validation decision from Tier 3."""

    APPROVE = "approve"
    REJECT = "reject"
    REQUEST_REVISION = "request_revision"


@dataclass
class ValidationResult:
    """Tier 3 validation result."""

    decision: ValidationDecision
    confidence: float
    reasoning: str
    suggested_improvements: Optional[List[str]] = None


@dataclass
class TierContext:
    """Context passed between tiers."""

    original_line: str
    file_path: str
    line_number: int
    instruction_set: str
    complexity: float
    cached_original: str


class UnifiedGitHubModelsHandler:
    """
    Unified GitHub Models handler for Tier 2 + Tier 3.

    Uses OpenAI-compatible API via models.inference.ai.azure.com
    """

    # Model configurations (GitHub Models free tier)
    TIER2_MODEL = "gpt-4o-mini"  # Fast generation (128K context)
    TIER3_MODEL = "gpt-4o"  # Premium validation (128K context)

    # Fallback to local Ollama if GitHub unavailable
    OLLAMA_URL = "http://localhost:11434/api/generate"
    OLLAMA_MODEL = "gemma3:1b"

    def __init__(
        self, tier2_model: Optional[str] = None, tier3_model: Optional[str] = None
    ):
        """
        Initialize unified GitHub Models handler.

        Args:
            tier2_model: Override Tier 2 model (default: gpt-4o-mini)
            tier3_model: Override Tier 3 model (default: gpt-4o)
        """
        self.api_key = os.environ.get("GITHUB_TOKEN")
        if not self.api_key:
            logger.warning("GITHUB_TOKEN not set - falling back to Ollama local models")

        self.tier2_model = tier2_model or self.TIER2_MODEL
        self.tier3_model = tier3_model or self.TIER3_MODEL

        self.base_url = "https://models.inference.ai.azure.com/chat/completions"
        self.stats = {
            "tier2_generations": 0,
            "tier2_ollama_fallbacks": 0,
            "tier3_validations": 0,
            "tier3_ollama_fallbacks": 0,
            "api_errors": 0,
        }

        logger.info("Unified GitHub Models Handler initialized:")
        logger.info(f"  Tier 2: {self.tier2_model}")
        logger.info(f"  Tier 3: {self.tier3_model}")
        logger.info(f"  Fallback: Ollama ({self.OLLAMA_MODEL})")

    async def tier2_generate(
        self, context: TierContext, feedback: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Tier 2: Generate fixed code using GitHub Models (GPT-4o-mini).

        Fallback: Ollama local if GitHub unavailable.

        Args:
            context: Tier context with original line and instructions
            feedback: Optional feedback from Tier 3 rejection

        Returns:
            Dict with success, fixed_lines, model_used, confidence
        """
        self.stats["tier2_generations"] += 1

        if not self.api_key:
            return await self._tier2_ollama_fallback(context)

        # Build generation prompt
        prompt = self._build_tier2_prompt(context, feedback)

        try:
            logger.info(f"Tier 2: Using {self.tier2_model}")

            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    self.base_url,
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": self.tier2_model,
                        "messages": [
                            {
                                "role": "system",
                                "content": "You are a Python code fixing specialist. "
                                "Return ONLY the fixed code, no explanations.",
                            },
                            {"role": "user", "content": prompt},
                        ],
                        "temperature": 0.3,
                        "max_tokens": 500,
                    },
                )
                response.raise_for_status()

                data = response.json()
                content = data["choices"][0]["message"]["content"]

                # Parse fixed code
                fixed_lines = self._parse_generated_code(content)

                if fixed_lines and all(len(line) <= 79 for line in fixed_lines):
                    logger.info(f"✅ Tier 2 success with {self.tier2_model}")
                    return {
                        "success": True,
                        "fixed_lines": fixed_lines,
                        "model_used": self.tier2_model,
                        "confidence": 0.9,
                    }
                else:
                    logger.warning("Tier 2 generated invalid code, trying Ollama")
                    return await self._tier2_ollama_fallback(context)

        except Exception as e:
            logger.warning(f"Tier 2 {self.tier2_model} failed: {e}")
            self.stats["api_errors"] += 1
            return await self._tier2_ollama_fallback(context)

    async def tier3_validate(
        self, context: TierContext, generated_code: List[str]
    ) -> Dict[str, Any]:
        """
        Tier 3: Validate generated code using GitHub Models (GPT-4o).

        Fallback: Basic validation if GitHub unavailable.

        Args:
            context: Original context
            generated_code: Lines to validate

        Returns:
            Dict with validation result, decision, confidence
        """
        self.stats["tier3_validations"] += 1

        if not self.api_key:
            return self._basic_validation(generated_code)

        # Build validation prompt
        prompt = self._build_tier3_prompt(context, generated_code)

        try:
            logger.info(f"Tier 3: Using {self.tier3_model}")

            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    self.base_url,
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": self.tier3_model,
                        "messages": [
                            {
                                "role": "system",
                                "content": "You are a code quality validator. "
                                "Return JSON with validation decision.",
                            },
                            {"role": "user", "content": prompt},
                        ],
                        "temperature": 0.2,
                        "max_tokens": 300,
                        "response_format": {"type": "json_object"},
                    },
                )
                response.raise_for_status()

                data = response.json()
                content = data["choices"][0]["message"]["content"]

                # Parse validation result
                validation_data = json.loads(content)

                logger.info(f"✅ Tier 3 validation: {validation_data.get('decision')}")
                return {
                    "success": True,
                    "decision": validation_data.get("decision", "approve"),
                    "confidence": validation_data.get("confidence", 0.8),
                    "reasoning": validation_data.get("reasoning", ""),
                    "model_used": self.tier3_model,
                }

        except Exception as e:
            logger.warning(f"Tier 3 {self.tier3_model} failed: {e}")
            self.stats["tier3_ollama_fallbacks"] += 1
            return self._basic_validation(generated_code)

    async def _tier2_ollama_fallback(self, context: TierContext) -> Dict[str, Any]:
        """Fallback to Ollama local model for Tier 2."""
        self.stats["tier2_ollama_fallbacks"] += 1
        logger.info("Tier 2: Falling back to Ollama")

        try:
            prompt = (
                f"Fix this Python line to be under 80 chars:\n{context.original_line}"
            )

            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    self.OLLAMA_URL,
                    json={
                        "model": self.OLLAMA_MODEL,
                        "prompt": prompt,
                        "stream": False,
                    },
                )
                response.raise_for_status()

                data = response.json()
                content = data.get("response", "")
                fixed_lines = self._parse_generated_code(content)

                return {
                    "success": True,
                    "fixed_lines": fixed_lines,
                    "model_used": f"ollama:{self.OLLAMA_MODEL}",
                    "confidence": 0.6,
                }
        except Exception as e:
            logger.error(f"Ollama fallback failed: {e}")
            return {"success": False, "error": "All models failed"}

    def _build_tier2_prompt(self, context: TierContext, feedback: Optional[str]) -> str:
        """Build Tier 2 generation prompt."""
        prompt = f"""Fix this E501 line length violation (max 79 chars per line):

ORIGINAL LINE (line {context.line_number}):
{context.original_line}

INSTRUCTIONS:
{context.instruction_set}

REQUIREMENTS:
- Maximum 79 characters per line
- Preserve exact functionality
- Use proper Python line continuation
- Return ONLY the fixed code, no explanations
"""

        if feedback:
            prompt += f"\n\nVALIDATOR FEEDBACK:\n{feedback}\n"

        return prompt

    def _build_tier3_prompt(
        self, context: TierContext, generated_code: List[str]
    ) -> str:
        """Build Tier 3 validation prompt."""
        return f"""Validate if this E501 fix preserves semantics:

ORIGINAL:
{context.original_line}

FIXED:
{chr(10).join(generated_code)}

Return JSON:
{{
  "decision": "approve|reject|request_revision",
  "confidence": 0.0-1.0,
  "reasoning": "brief explanation",
  "semantic_preserved": true|false
}}"""

    def _parse_generated_code(self, content: str) -> List[str]:
        """Extract code lines from model response."""
        content = content.strip()
        if content.startswith("```"):
            lines = content.split("\n")
            content = "\n".join(
                lines[1:-1] if lines[-1].strip() == "```" else lines[1:]
            )

        lines = [line.rstrip() for line in content.split("\n") if line.strip()]
        return lines

    def _basic_validation(self, generated_code: List[str]) -> Dict[str, Any]:
        """Fallback validation without AI."""
        all_short = all(len(line) <= 79 for line in generated_code)

        return {
            "success": True,
            "decision": "approve" if all_short else "reject",
            "confidence": 0.5,
            "reasoning": "Basic length check (no AI validation)",
            "model_used": "basic_validator",
        }

    def get_stats(self) -> Dict[str, int]:
        """Return usage statistics."""
        return self.stats.copy()


# Example usage
if __name__ == "__main__":
    import asyncio

    logging.basicConfig(level=logging.INFO)

    async def test_github_models_handler():
        handler = UnifiedGitHubModelsHandler()

        # Test Tier 2 generation
        context = TierContext(
            original_line="    result = some_very_long_function_name_that_exceeds_79_characters(arg1, arg2, arg3, arg4)",
            file_path="test.py",
            line_number=42,
            instruction_set="Break at comma",
            complexity=0.5,
            cached_original="    result = some_very_long_function_name_that_exceeds_79_characters(arg1, arg2, arg3, arg4)",
        )

        print("Testing Tier 2 (GitHub Models GPT-4o-mini)...")
        tier2_result = await handler.tier2_generate(context)
        print(f"Result: {tier2_result}")

        if tier2_result["success"]:
            print("\nTesting Tier 3 (GitHub Models GPT-4o)...")
            tier3_result = await handler.tier3_validate(
                context, tier2_result["fixed_lines"]
            )
            print(f"Result: {tier3_result}")

        print(f"\nStats: {handler.get_stats()}")

    asyncio.run(test_github_models_handler())
