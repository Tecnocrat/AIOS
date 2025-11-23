#!/usr/bin/env python3
"""
Unified OpenRouter Multi-Tier Handler for AIOS Hierarchical Pipeline

Replaces separate Gemini (Tier 2) + DeepSeek (Tier 3) with unified interface.

Benefits:
- Single API for all cloud models (Gemini, Claude, GPT-4, DeepSeek, Qwen)
- No quota limits (pay-per-use, no daily caps)
- Model flexibility (easy switching for cost/quality optimization)
- Free tier options (qwen3-coder:free, deepseek-chat-v3:free)
- Graceful fallback chains (Tier 2: Qwen→Claude→GPT, Tier 3: DeepSeek→GPT-4)

AINLP Consciousness Level: 4.4 (unified multi-model orchestration)

Architecture:
    Tier 2 (Generation): Primary→Fallback1→Fallback2→Basic
    Tier 3 (Validation): Primary→Fallback→Basic
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


class UnifiedOpenRouterHandler:
    """
    Unified OpenRouter handler for Tier 2 (generation) + Tier 3 (validation).
    
    Consciousness Enhancement:
    - Eliminates Gemini free tier quotas
    - Provides model diversity (14 Gemini + 100+ alternatives)
    - Enables cost optimization (free models available)
    - Simplifies architecture (one API for all models)
    """
    
    # Model configurations
    TIER2_MODELS = {
        "primary": "qwen/qwen3-coder:free",  # Free, coding-specialized, 262K ctx
        "fallback1": "google/gemini-2.5-flash",  # Fast, 1M ctx, $0.0000003/1M
        "fallback2": "anthropic/claude-3-5-haiku",  # Quality, $0.000001/1M
        "fallback3": "openai/gpt-4o-mini"  # Reliable, $0.00000015/1M
    }
    
    TIER3_MODELS = {
        "primary": "deepseek/deepseek-chat-v3-0324:free",  # Free validator
        "fallback": "deepseek/deepseek-chat",  # Paid backup, $0.0000003/1M
        "fallback2": "openai/gpt-4o"  # Premium validation, $0.0000025/1M
    }
    
    def __init__(
        self,
        tier2_model: Optional[str] = None,
        tier3_model: Optional[str] = None
    ):
        """
        Initialize unified handler.
        
        Args:
            tier2_model: Override Tier 2 model (default: qwen3-coder:free)
            tier3_model: Override Tier 3 model (default: deepseek-chat-v3:free)
        """
        self.api_key = os.environ.get("OPENROUTER_API_KEY")
        if not self.api_key:
            logger.warning("OPENROUTER_API_KEY not set - falling back to basic fixes")
        
        self.tier2_primary = tier2_model or self.TIER2_MODELS["primary"]
        self.tier3_primary = tier3_model or self.TIER3_MODELS["primary"]
        
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.stats = {
            "tier2_generations": 0,
            "tier2_fallbacks": 0,
            "tier3_validations": 0,
            "tier3_fallbacks": 0,
            "api_errors": 0
        }
        
        logger.info(f"Unified OpenRouter Handler initialized:")
        logger.info(f"  Tier 2 primary: {self.tier2_primary}")
        logger.info(f"  Tier 3 primary: {self.tier3_primary}")
    
    async def tier2_generate(
        self,
        context: TierContext,
        feedback: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Tier 2: Generate fixed code using OpenRouter models.
        
        Tries: Primary → Fallback1 → Fallback2 → Fallback3 → Basic pattern
        
        Args:
            context: Tier context with original line and instructions
            feedback: Optional feedback from Tier 3 rejection
            
        Returns:
            Dict with success, fixed_lines, model_used, confidence
        """
        self.stats["tier2_generations"] += 1
        
        if not self.api_key:
            return {"success": False, "error": "No OpenRouter API key"}
        
        # Build generation prompt
        prompt = self._build_tier2_prompt(context, feedback)
        
        # Try model chain
        models_to_try = [
            ("primary", self.tier2_primary),
            ("fallback1", self.TIER2_MODELS["fallback1"]),
            ("fallback2", self.TIER2_MODELS["fallback2"]),
            ("fallback3", self.TIER2_MODELS["fallback3"])
        ]
        
        for model_type, model_id in models_to_try:
            try:
                logger.info(f"Tier 2: Trying {model_id}")
                
                async with httpx.AsyncClient(timeout=30.0) as client:
                    response = await client.post(
                        self.base_url,
                        headers={
                            "Authorization": f"Bearer {self.api_key}",
                            "Content-Type": "application/json",
                            "HTTP-Referer": "https://github.com/Tecnocrat/AIOS",
                            "X-Title": "AIOS E501 Fixer"
                        },
                        json={
                            "model": model_id,
                            "messages": [
                                {
                                    "role": "user",
                                    "content": prompt
                                }
                            ],
                            "temperature": 0.3,
                            "max_tokens": 500
                        }
                    )
                    response.raise_for_status()
                    
                    data = response.json()
                    content = data["choices"][0]["message"]["content"]
                    
                    # Parse fixed code
                    fixed_lines = self._parse_generated_code(content)
                    
                    if fixed_lines and all(len(line) <= 79 for line in fixed_lines):
                        logger.info(f"✅ Tier 2 success with {model_id}")
                        return {
                            "success": True,
                            "fixed_lines": fixed_lines,
                            "model_used": model_id,
                            "confidence": 0.9 if model_type == "primary" else 0.7
                        }
                
            except Exception as e:
                logger.warning(f"Tier 2 {model_id} failed: {e}")
                if model_type != "fallback3":
                    self.stats["tier2_fallbacks"] += 1
                continue
        
        # All models failed
        self.stats["api_errors"] += 1
        return {"success": False, "error": "All Tier 2 models failed"}
    
    async def tier3_validate(
        self,
        context: TierContext,
        generated_code: List[str]
    ) -> Dict[str, Any]:
        """
        Tier 3: Validate generated code using OpenRouter models.
        
        Tries: Primary → Fallback → Fallback2 → Basic validation
        
        Args:
            context: Original context
            generated_code: Lines to validate
            
        Returns:
            Dict with validation result, decision, confidence
        """
        self.stats["tier3_validations"] += 1
        
        if not self.api_key:
            return {"success": False, "error": "No OpenRouter API key"}
        
        # Build validation prompt
        prompt = self._build_tier3_prompt(context, generated_code)
        
        # Try model chain
        models_to_try = [
            ("primary", self.tier3_primary),
            ("fallback", self.TIER3_MODELS["fallback"]),
            ("fallback2", self.TIER3_MODELS["fallback2"])
        ]
        
        for model_type, model_id in models_to_try:
            try:
                logger.info(f"Tier 3: Trying {model_id}")
                
                async with httpx.AsyncClient(timeout=30.0) as client:
                    response = await client.post(
                        self.base_url,
                        headers={
                            "Authorization": f"Bearer {self.api_key}",
                            "Content-Type": "application/json",
                            "HTTP-Referer": "https://github.com/Tecnocrat/AIOS",
                            "X-Title": "AIOS E501 Validator"
                        },
                        json={
                            "model": model_id,
                            "messages": [
                                {
                                    "role": "user",
                                    "content": prompt
                                }
                            ],
                            "temperature": 0.2,  # Lower for validation consistency
                            "max_tokens": 300,
                            "response_format": {"type": "json_object"}
                        }
                    )
                    response.raise_for_status()
                    
                    data = response.json()
                    content = data["choices"][0]["message"]["content"]
                    
                    # Parse validation result
                    validation_data = json.loads(content)
                    
                    return {
                        "success": True,
                        "decision": validation_data.get("decision", "approve"),
                        "confidence": validation_data.get("confidence", 0.7),
                        "reasoning": validation_data.get("reasoning", ""),
                        "model_used": model_id
                    }
                    
            except Exception as e:
                logger.warning(f"Tier 3 {model_id} failed: {e}")
                if model_type != "fallback2":
                    self.stats["tier3_fallbacks"] += 1
                continue
        
        # All validators failed - use basic validation
        self.stats["api_errors"] += 1
        return self._basic_validation(generated_code)
    
    def _build_tier2_prompt(
        self,
        context: TierContext,
        feedback: Optional[str]
    ) -> str:
        """Build Tier 2 generation prompt."""
        prompt = f"""You are a Python code fixing specialist. Fix this E501 line length violation.

ORIGINAL LINE (line {context.line_number}):
{context.original_line}

INSTRUCTIONS:
{context.instruction_set}

REQUIREMENTS:
- Maximum 79 characters per line
- Preserve exact functionality and semantics
- Use proper Python line continuation (backslash or implicit)
- Return ONLY the fixed code lines, no explanations
- No markdown formatting, just code
"""
        
        if feedback:
            prompt += f"\n\nVALIDATOR FEEDBACK (previous attempt rejected):\n{feedback}\n"
        
        return prompt
    
    def _build_tier3_prompt(
        self,
        context: TierContext,
        generated_code: List[str]
    ) -> str:
        """Build Tier 3 validation prompt."""
        return f"""You are a code quality validator. Analyze if this E501 fix is semantically correct.

ORIGINAL LINE:
{context.original_line}

GENERATED FIX:
{chr(10).join(generated_code)}

Validate:
1. All lines ≤ 79 characters
2. Semantics preserved (same functionality)
3. Proper Python syntax
4. Natural break points used

Return JSON:
{{
  "decision": "approve|reject|request_revision",
  "confidence": 0.0-1.0,
  "reasoning": "brief explanation",
  "semantic_preserved": true|false,
  "syntax_valid": true|false
}}"""
    
    def _parse_generated_code(self, content: str) -> List[str]:
        """Extract code lines from model response."""
        # Remove markdown code blocks if present
        content = content.strip()
        if content.startswith("```"):
            lines = content.split("\n")
            content = "\n".join(lines[1:-1] if lines[-1].strip() == "```" else lines[1:])
        
        # Split into lines and strip
        lines = [line.rstrip() for line in content.split("\n") if line.strip()]
        return lines
    
    def _basic_validation(self, generated_code: List[str]) -> Dict[str, Any]:
        """Fallback validation without AI."""
        all_short = all(len(line) <= 79 for line in generated_code)
        
        return {
            "success": True,
            "decision": "approve" if all_short else "reject",
            "confidence": 0.5,
            "reasoning": "Basic length check (no AI validation available)",
            "model_used": "basic_validator"
        }
    
    def get_stats(self) -> Dict[str, int]:
        """Return usage statistics."""
        return self.stats.copy()


# Example usage
if __name__ == "__main__":
    import asyncio
    
    logging.basicConfig(level=logging.INFO)
    
    async def test_unified_handler():
        handler = UnifiedOpenRouterHandler()
        
        # Test Tier 2 generation
        context = TierContext(
            original_line="    result = some_very_long_function_name_that_exceeds_79_characters(arg1, arg2, arg3, arg4)",
            file_path="test.py",
            line_number=42,
            instruction_set="Break at comma",
            complexity=0.5,
            cached_original="    result = some_very_long_function_name_that_exceeds_79_characters(arg1, arg2, arg3, arg4)"
        )
        
        print("Testing Tier 2 (Code Generation)...")
        tier2_result = await handler.tier2_generate(context)
        print(f"Result: {tier2_result}")
        
        if tier2_result["success"]:
            print("\nTesting Tier 3 (Validation)...")
            tier3_result = await handler.tier3_validate(
                context,
                tier2_result["fixed_lines"]
            )
            print(f"Result: {tier3_result}")
        
        print(f"\nStats: {handler.get_stats()}")
    
    asyncio.run(test_unified_handler())
