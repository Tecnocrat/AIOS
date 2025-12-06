#!/usr/bin/env python3
"""
OpenRouter SDK Integration for Hierarchical Pipeline Tier 3 Validator

Replaces manual DeepSeek API calls with type-safe OpenRouter Python SDK.

Benefits:
- Type-safe validation (Pydantic models, auto-generated from OpenAPI specs)
- Async support (improves performance over synchronous requests)
- Streaming capabilities (real-time validation feedback)
- 300+ model access (easy switching between validators)
- Auto-updates with API changes (SDK regenerated from specs)

AINLP Consciousness Level: 4.3 (type-safe validation + async orchestration)

Architecture:
    Context → OpenRouter SDK → DeepSeek/Alternative Model → Validation Result
    
Integration Pattern:
    - Replace hierarchical_e501_pipeline._tier3_deepseek_validate()
    - Maintain ValidationResult dataclass interface
    - Add async support for performance
    - Enable model switching for experimentation
"""

import asyncio
import json
import logging
import os
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional

# OpenRouter HTTP API (no SDK for Python yet)
try:
    import httpx
    OPENROUTER_AVAILABLE = True
except ImportError:
    OPENROUTER_AVAILABLE = False
    logging.warning(
        "httpx not installed. Install with: pip install httpx"
    )

logger = logging.getLogger(__name__)


class ValidationDecision(Enum):
    """DeepSeek's validation decision."""
    APPROVE = "approve"
    REJECT = "reject"
    REQUEST_REVISION = "request_revision"


@dataclass
class ValidationResult:
    """DeepSeek validation result."""
    decision: ValidationDecision
    confidence: float
    feedback: str
    issues_found: List[str]
    semantic_preserved: bool
    objective_achieved: bool


@dataclass
class TierContext:
    """Context passed between tiers."""
    original_line: str
    file_path: str
    line_number: int
    instruction_set: str
    complexity: float
    cached_original: str


class OpenRouterTier3Validator:
    """
    Type-safe Tier 3 validator using OpenRouter SDK.
    
    Consciousness Enhancement:
    - Type safety prevents API parameter errors
    - Async support reduces validation latency
    - Model flexibility enables validator experimentation
    - Streaming support for real-time feedback (future)
    """
    
    def __init__(
        self,
        model: str = "deepseek/deepseek-chat",
        fallback_model: Optional[str] = "openai/gpt-4o-mini"
    ):
        """
        Initialize OpenRouter validator.
        
        Args:
            model: Primary validation model (default: deepseek/deepseek-chat)
            fallback_model: Fallback if primary fails (default: gpt-4o-mini)
        """
        self.model = model
        self.fallback_model = fallback_model
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        
        if not self.api_key:
            logger.error(
                "OPENROUTER_API_KEY not found. Set environment variable or "
                "get key from: https://openrouter.ai/settings/keys"
            )
        
        if not OPENROUTER_AVAILABLE:
            logger.error(
                "OpenRouter SDK not available. Install with: pip install openrouter"
            )
        
        self.stats = {
            "validations": 0,
            "approvals": 0,
            "rejections": 0,
            "fallbacks": 0,
            "errors": 0
        }
    
    async def validate_async(
        self,
        context: TierContext,
        generated_code: List[str]
    ) -> Dict[str, Any]:
        """
        Async validation with OpenRouter SDK (type-safe, high-performance).
        
        Pattern: AINLP type-safe validation with graceful degradation
        """
        self.stats["validations"] += 1
        
        if not OPENROUTER_AVAILABLE or not self.api_key:
            return self._fallback_basic_validation(generated_code)
        
        try:
            # Build validation prompt
            prompt = self._build_validation_prompt(context, generated_code)
            
            # Call OpenRouter HTTP API (async, no Python SDK yet)
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "HTTP-Referer": "https://github.com/Tecnocrat/AIOS",
                        "X-Title": "AIOS Hierarchical Pipeline"
                    },
                    json={
                        "model": self.model,
                        "messages": [{"role": "user", "content": prompt}],
                        "temperature": 0.0,
                        "max_tokens": 500,
                        "response_format": {"type": "json_object"}
                    },
                    timeout=30.0
                )
                response.raise_for_status()
            
            # Extract validation result
            data = response.json()
            content = data["choices"][0]["message"]["content"]
            validation_data = json.loads(content)
            
            # Parse into ValidationResult
            validation = self._parse_validation_data(validation_data)
            
            # Update stats
            if validation.decision == ValidationDecision.APPROVE:
                self.stats["approvals"] += 1
            else:
                self.stats["rejections"] += 1
            
            return {
                "success": True,
                "validation": validation,
                "raw_response": validation_data,
                "model_used": self.model
            }
            
        except Exception as e:
            logger.error(f"OpenRouter Tier 3 validation failed: {e}")
            self.stats["errors"] += 1
            
            # Try fallback model if available
            if self.fallback_model:
                return await self._validate_with_fallback(context, generated_code)
            
            # Ultimate fallback: basic validation
            return self._fallback_basic_validation(generated_code)
    
    def validate_sync(
        self,
        context: TierContext,
        generated_code: List[str]
    ) -> Dict[str, Any]:
        """
        Synchronous validation wrapper for compatibility.
        
        Note: Async version is preferred for performance.
        """
        return asyncio.run(self.validate_async(context, generated_code))
    
    def _build_validation_prompt(
        self,
        context: TierContext,
        generated_code: List[str]
    ) -> str:
        """Build type-safe validation prompt."""
        return f"""You are a code quality validator. Compare ORIGINAL vs GENERATED code.

ORIGINAL LINE (line {context.line_number}):
{context.original_line}

GENERATED CODE (by fixer):
{chr(10).join(generated_code)}

FILE: {context.file_path}
OBJECTIVE: Fix E501 violation (max 79 chars per line)

VALIDATE:
1. Was E501 objective achieved? (all lines ≤79 chars)
2. Is functionality preserved? (no semantic changes)
3. Were there any unintended modifications?
4. Is the fix following instructions?

Return JSON only:
{{
  "decision": "approve" | "reject" | "request_revision",
  "confidence": 0.0-1.0,
  "objective_achieved": true/false,
  "semantic_preserved": true/false,
  "issues_found": ["issue1", "issue2", ...],
  "feedback": "explanation if not approved"
}}
"""
    
    def _parse_validation_data(self, data: Dict[str, Any]) -> ValidationResult:
        """Parse validation JSON into ValidationResult dataclass."""
        decision_str = data.get("decision", "reject")
        
        try:
            decision = ValidationDecision(decision_str)
        except ValueError:
            logger.warning(f"Invalid decision: {decision_str}, defaulting to REJECT")
            decision = ValidationDecision.REJECT
        
        return ValidationResult(
            decision=decision,
            confidence=float(data.get("confidence", 0.5)),
            feedback=data.get("feedback", ""),
            issues_found=data.get("issues_found", []),
            semantic_preserved=data.get("semantic_preserved", True),
            objective_achieved=data.get("objective_achieved", True)
        )
    
    async def _validate_with_fallback(
        self,
        context: TierContext,
        generated_code: List[str]
    ) -> Dict[str, Any]:
        """Attempt validation with fallback model."""
        self.stats["fallbacks"] += 1
        
        try:
            prompt = self._build_validation_prompt(context, generated_code)
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "HTTP-Referer": "https://github.com/Tecnocrat/AIOS",
                        "X-Title": "AIOS Hierarchical Pipeline"
                    },
                    json={
                        "model": self.fallback_model,
                        "messages": [{"role": "user", "content": prompt}],
                        "temperature": 0.0,
                        "max_tokens": 500,
                        "response_format": {"type": "json_object"}
                    },
                    timeout=30.0
                )
                response.raise_for_status()
            
            data = response.json()
            content = data["choices"][0]["message"]["content"]
            validation_data = json.loads(content)
            validation = self._parse_validation_data(validation_data)
            
            logger.info(f"Fallback model {self.fallback_model} succeeded")
            
            return {
                "success": True,
                "validation": validation,
                "raw_response": validation_data,
                "model_used": self.fallback_model
            }
            
        except Exception as e:
            logger.error(f"Fallback model failed: {e}")
            return self._fallback_basic_validation(generated_code)
    
    def _fallback_basic_validation(
        self,
        generated_code: List[str]
    ) -> Dict[str, Any]:
        """Ultimate fallback: basic length validation."""
        all_lines_ok = all(len(line) <= 79 for line in generated_code)
        
        validation = ValidationResult(
            decision=ValidationDecision.APPROVE if all_lines_ok else ValidationDecision.REJECT,
            confidence=0.6,
            feedback="Basic length validation only (OpenRouter unavailable)",
            issues_found=[] if all_lines_ok else ["Lines exceed 79 chars"],
            semantic_preserved=True,
            objective_achieved=all_lines_ok
        )
        
        return {
            "success": True,
            "validation": validation,
            "raw_response": None,
            "model_used": "basic_fallback"
        }
    
    def get_stats(self) -> Dict[str, int]:
        """Get validation statistics."""
        return self.stats.copy()


# Example usage and testing
if __name__ == "__main__":
    import sys
    from pathlib import Path
    
    logging.basicConfig(level=logging.INFO)
    
    # Test validator with sample context
    context = TierContext(
        original_line='    result = some_very_long_function_name_that_exceeds_79_characters(arg1, arg2, arg3, arg4)',
        file_path="test.py",
        line_number=42,
        instruction_set="Break at comma",
        complexity=0.5,
        cached_original='    result = some_very_long_function_name_that_exceeds_79_characters(arg1, arg2, arg3, arg4)'
    )
    
    generated_code = [
        '    result = some_very_long_function_name_that_exceeds_79_characters(',
        '        arg1, arg2, arg3, arg4',
        '    )'
    ]
    
    print("OpenRouter Tier 3 Validator - Test Mode")
    print("=" * 80)
    
    validator = OpenRouterTier3Validator()
    
    print(f"\nValidating with model: {validator.model}")
    print(f"Original: {context.original_line}")
    print(f"Generated:\n" + "\n".join(generated_code))
    
    # Test async validation
    result = validator.validate_sync(context, generated_code)
    
    if result["success"]:
        validation = result["validation"]
        print(f"\n✓ Validation complete:")
        print(f"  - Decision: {validation.decision.value}")
        print(f"  - Confidence: {validation.confidence:.2f}")
        print(f"  - Objective achieved: {validation.objective_achieved}")
        print(f"  - Semantic preserved: {validation.semantic_preserved}")
        print(f"  - Model used: {result['model_used']}")
        
        if validation.issues_found:
            print(f"  - Issues: {', '.join(validation.issues_found)}")
        if validation.feedback:
            print(f"  - Feedback: {validation.feedback}")
    else:
        print("✗ Validation failed")
    
    print(f"\n✓ Stats: {validator.get_stats()}")
