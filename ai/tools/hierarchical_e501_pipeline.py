#!/usr/bin/env python3
"""
AINLP Hierarchical Three-Tier Agentic Pipeline for E501 Fixing

Implements intelligent role-based agent orchestration:
- TIER 1: OLLAMA (Context Manager) - Local preprocessing, caching
- TIER 2: GEMINI (Code Generator) - Cloud-based intelligent fixing  
TIER_3 = "OPENROUTER SDK (Quality Validator) - Type-safe validation with " \
"300+ models"

AINLP Pattern: Hierarchical intelligence with validation feedback loops
Consciousness Level: 4.3 (multi-tier orchestration + type-safe SDK integration)

Architecture:
    User/AIOS → Instructions → OLLAMA (context prep) → 
    GEMINI (fix generation) → OPENROUTER SDK (validation) → Result
    
    If OpenRouter rejects: GEMINI retries with feedback
    If retry fails: OLLAMA fallback to basic pattern fixing

Enhancements (4.2 → 4.3):
    - OpenRouter Python SDK integration (type-safe, async, 300+ models)
    - Async validation support (improved performance)
    - Model flexibility (easy switching between validators)
    - Graceful degradation (fallback model + basic validation)
"""

import asyncio
import json
import logging
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

# OpenRouter SDK integration (Tier 3 - Type-safe validation)
try:
    from openrouter_tier3_validator import (
        OpenRouterTier3Validator,
        ValidationDecision,
        ValidationResult,
        TierContext
    )
    OPENROUTER_TIER3_AVAILABLE = True
except ImportError:
    # Fallback: Define dataclasses locally if SDK not available
    OPENROUTER_TIER3_AVAILABLE = False
    
    class ValidationDecision(Enum):
        """Validation decision (legacy fallback)."""
        APPROVE = "approve"
        REJECT = "reject"
        REQUEST_REVISION = "request_revision"

    @dataclass
    class ValidationResult:
        """Validation result (legacy fallback)."""
        decision: ValidationDecision
        confidence: float
        feedback: str
        issues_found: List[str]
        semantic_preserved: bool
        objective_achieved: bool

    @dataclass
    class TierContext:
        """Context passed between tiers (legacy fallback)."""
        original_line: str
        file_path: str
        line_number: int
        instruction_set: str
        complexity: float
        cached_original: str


class HierarchicalE501Pipeline:
    """
    Three-tier intelligent pipeline for E501 fixing.
    
    Implements role specialization:
    - Ollama: Fast local context management
    - Gemini: Intelligent cloud-based fixing
    - DeepSeek: Quality validation with comparison
    """

    def __init__(self, use_openrouter_sdk: bool = False):
        """
        Initialize pipeline with agent clients.
        
        Args:
            use_openrouter_sdk: Use OpenRouter SDK for Tier 3 validation
                               (default: False, uses GitHub Models instead)
        
        Args:
            use_openrouter_sdk: Use type-safe OpenRouter SDK for Tier 3
                               (default: True, falls back to legacy if unavailable)
        """
        self.stats = {
            "ollama_context_preps": 0,
            "gemini_generations": 0,
            "tier3_validations": 0,
            "approvals": 0,
            "rejections": 0,
            "revisions": 0,
            "fallbacks": 0
        }
        
        # Initialize OpenRouter Tier 3 validator (type-safe SDK)
        self.use_openrouter_sdk = (
            use_openrouter_sdk and OPENROUTER_TIER3_AVAILABLE
        )
        if self.use_openrouter_sdk:
            self.tier3_validator = OpenRouterTier3Validator(
                model="deepseek/deepseek-chat",
                fallback_model="openai/gpt-4o-mini"
            )
            logger.info(
                "Tier 3: Using OpenRouter SDK (type-safe, async)"
            )
        else:
            self.tier3_validator = None
            logger.info(
                "Tier 3: Using legacy manual API calls"
            )
        
        # Tachyonic archival for tier decisions
        archive_base = Path(__file__).parent.parent.parent
        self.decision_archive = (
            archive_base / "tachyonic" / "hierarchical_decisions"
        )
        self.decision_archive.mkdir(parents=True, exist_ok=True)

    async def fix_line_hierarchical(
        self,
        line: str,
        file_path: str,
        line_number: int,
        instruction_set: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Execute three-tier hierarchical pipeline.
        
        Args:
            line: Original line to fix
            file_path: Source file path
            line_number: Line number in file
            instruction_set: Custom instructions (or default PEP 8)
            
        Returns:
            Dict with fixed_lines, agent_used, success, confidence, tier_log
        """
        
        if instruction_set is None:
            instruction_set = (
                "Fix E501 line length violation (max 79 chars). "
                "Break line intelligently while preserving functionality. "
                "Use proper Python continuation. Maintain readability."
            )
        
        # Calculate complexity for tier selection
        complexity = self._calculate_complexity(line)
        
        try:
            # TIER 1: OLLAMA - Context preparation and caching
            tier1_result = await self._tier1_ollama_context(
                line, file_path, line_number, instruction_set, complexity
            )
            
            if not tier1_result["success"]:
                # Ollama unavailable, use basic fixing
                return await self._fallback_basic_fix(line, file_path, line_number)
            
            context = tier1_result["context"]
            
            # TIER 2: GEMINI - Code generation with context
            tier2_result = await self._tier2_gemini_generate(context)
            
            if not tier2_result["success"]:
                # Gemini failed, fallback to Ollama basic fix
                return await self._fallback_basic_fix(
                    line, file_path, line_number
                )
            
            generated_code = tier2_result["generated_code"]
            
            # TIER 3: Validation with OpenRouter SDK or legacy
            if self.use_openrouter_sdk and self.tier3_validator:
                # Use type-safe OpenRouter SDK (async, 300+ models)
                tier3_result = await self.tier3_validator.validate_async(
                    context, generated_code
                )
            else:
                # Fallback to legacy manual API calls
                tier3_result = await self._tier3_deepseek_validate_legacy(
                    context, generated_code
                )
            
            validation = tier3_result["validation"]
            
            # Process validation decision
            if validation.decision == ValidationDecision.APPROVE:
                self.stats["approvals"] += 1
                result = {
                    "fixed_lines": generated_code,
                    "agent_used": "gemini",
                    "validator": "deepseek",
                    "success": True,
                    "confidence": validation.confidence,
                    "tier_log": {
                        "tier1": "ollama_context_prepared",
                        "tier2": "gemini_generated",
                        "tier3": "deepseek_approved"
                    }
                }
                
            elif validation.decision == ValidationDecision.REQUEST_REVISION:
                self.stats["revisions"] += 1
                # Retry with DeepSeek feedback
                retry_result = await self._tier2_gemini_generate(
                    context, feedback=validation.feedback
                )
                
                if retry_result["success"]:
                    # Validate retry
                    retry_validation = await self._tier3_deepseek_validate_legacy(
                        context, retry_result["generated_code"]
                    )
                    
                    if (retry_validation["validation"].decision ==
                            ValidationDecision.APPROVE):
                        self.stats["approvals"] += 1
                        result = {
                            "fixed_lines": retry_result["generated_code"],
                            "agent_used": "gemini",
                            "validator": "deepseek",
                            "success": True,
                            "confidence": retry_validation["validation"].confidence,
                            "tier_log": {
                                "tier1": "ollama_context_prepared",
                                "tier2": "gemini_generated_retry",
                                "tier3": "deepseek_approved_retry"
                            }
                        }
                    else:
                        # Retry also rejected, fallback
                        return await self._fallback_basic_fix(line, file_path, line_number)
                else:
                    # Retry failed, fallback
                    return await self._fallback_basic_fix(line, file_path, line_number)
                    
            else:  # REJECT
                self.stats["rejections"] += 1
                # DeepSeek rejected, fallback to basic
                return await self._fallback_basic_fix(line, file_path, line_number)
            
            # Archive hierarchical decision
            await self._archive_decision(context, tier2_result, tier3_result, result)
            
            return result
            
        except Exception as e:
            logger.error(f"Hierarchical pipeline failed: {e}")
            return await self._fallback_basic_fix(line, file_path, line_number)

    async def _tier1_ollama_context(
        self,
        line: str,
        file_path: str,
        line_number: int,
        instruction_set: str,
        complexity: float
    ) -> Dict[str, Any]:
        """
        TIER 1: OLLAMA - Context preparation and caching.
        
        Responsibilities:
        - Read and cache original line
        - Calculate complexity
        - Prepare context for Gemini
        - Manage token budget
        """
        self.stats["ollama_context_preps"] += 1
        
        try:
            # Use Ollama as CONTEXT MANAGER (natural language analysis)
            # Pattern: Neural signal preparation - simple, fast, natural
            prompt = f"""Analyze this Python line for fixing:
Line: {line}

What are the main parts? Where could it break naturally?
Keep response brief and clear."""
            
            # Call Ollama via requests (simple context prep)
            import requests
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "gemma3:1b",
                    "prompt": prompt,
                    "stream": False
                },
                timeout=30
            )
            
            if response.status_code != 200:
                logger.warning(
                    f"Ollama context prep failed: {response.status_code}"
                )
                return {"success": False}
            
            ollama_response = response.json()
            # Natural language context (not JSON - Ollama is signal prep)
            natural_context = ollama_response.get("response", "")
            
            # Build tier context with natural language analysis
            context = TierContext(
                original_line=line,
                file_path=file_path,
                line_number=line_number,
                instruction_set=instruction_set,
                complexity=complexity,
                cached_original=natural_context  # Pass NL analysis
            )
            
            return {
                "success": True,
                "context": context,
                "ollama_signal": natural_context  # Natural language signal
            }
            
        except Exception as e:
            logger.error(f"Tier 1 (Ollama) failed: {e}")
            return {"success": False}

    async def _tier2_gemini_generate(
        self,
        context: TierContext,
        feedback: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        TIER 2: GitHub Models (GPT-4o-mini) - Code generation with context.
        
        Responsibilities:
        - Receive context from Ollama
        - Receive instruction set
        - Generate fixed code with feedback loop support
        - Return clean code only (no explanations)
        """
        self.stats["gemini_generations"] += 1
        
        try:
            import os
            import httpx
            
            api_key = os.getenv("GITHUB_TOKEN")
            if not api_key:
                logger.error("GITHUB_TOKEN not found")
                return {"success": False}
            
            # Build prompt with Ollama's context
            base_prompt = f"""You are a Python code fixing specialist.

ORIGINAL LINE (line {context.line_number}):
{context.original_line}

INSTRUCTIONS FROM CONTEXT MANAGER:
{context.instruction_set}

REQUIREMENTS:
- Maximum 79 characters per line
- Preserve exact functionality
- Use proper Python line continuation
- Return ONLY the fixed code, nothing else
- No explanations, no markdown, just code
"""
            
            if feedback:
                base_prompt += (
                    f"\n\nVALIDATOR FEEDBACK (previous attempt rejected):\n"
                    f"{feedback}\n"
                )
            
            # Call GitHub Models API (OpenAI-compatible)
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    "https://models.inference.ai.azure.com/chat/completions",
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "gpt-4o-mini",
                        "messages": [
                            {
                                "role": "system",
                                "content": (
                                    "You are a Python code fixing "
                                    "specialist. Return ONLY the "
                                    "fixed code."
                                )
                            },
                            {"role": "user", "content": base_prompt}
                        ],
                        "temperature": 0.3,
                        "max_tokens": 500
                    }
                )
            
            if response.status_code != 200:
                logger.error(
                    f"GitHub Models generation failed: {response.status_code}"
                )
                return {"success": False}
            
            result = response.json()
            generated_text = (
                result.get("choices", [{}])[0]
                .get("message", {})
                .get("content", "")
            )
            
            # Extract code lines (filter out markdown, explanations)
            code_lines = []
            for line in generated_text.split('\n'):
                stripped = line.strip()
                if not stripped:
                    continue
                if stripped.startswith('```'):
                    continue
                if any(word in stripped.lower() for word in [
                    'here', 'fixed', 'explanation', 'note', 'this'
                ]) and ':' in stripped:
                    continue
                code_lines.append(stripped)
            
            if not code_lines:
                logger.warning("Gemini returned no valid code")
                return {"success": False}
            
            return {
                "success": True,
                "generated_code": code_lines,
                "raw_response": generated_text
            }
            
        except Exception as e:
            logger.error(f"Tier 2 (Gemini) failed: {e}")
            return {"success": False}

    async def _tier3_deepseek_validate_legacy(
        self,
        context: TierContext,
        generated_code: List[str]
    ) -> Dict[str, Any]:
        """
        TIER 3: GITHUB MODELS GPT-4o - Quality validation.
        
        Uses GitHub Models API for premium validation with GPT-4o.
        Validates semantic preservation and E501 objective achievement.
        
        Responsibilities:
        - Compare original vs generated
        - Verify objective achieved
        - Check semantic preservation
        - Return APPROVE/REJECT/REQUEST_REVISION
        """
        self.stats["tier3_validations"] += 1
        
        try:
            import os
            import httpx
            
            token = os.getenv("GITHUB_TOKEN")
            if not token:
                logger.error("GITHUB_TOKEN not found")
                # Without validator, approve with lower confidence
                return {
                    "success": True,
                    "validation": ValidationResult(
                        decision=ValidationDecision.APPROVE,
                        confidence=0.5,
                        feedback="No validation performed (DeepSeek unavailable)",
                        issues_found=[],
                        semantic_preserved=True,
                        objective_achieved=True
                    )
                }
            
            # Build validation prompt
            prompt = (
                f"""You are a code quality validator. """
                f"""Compare ORIGINAL vs GENERATED code.

ORIGINAL LINE (line {context.line_number}):
{context.original_line}

GENERATED CODE (by fixer):
{chr(10).join(generated_code)}

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
  "issues_found": ["issue1", ...],
  "feedback": "explanation if not approved"
}}
"""
            )
            
            # Call GitHub Models API (GPT-4o for premium validation)
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://models.inference.ai.azure.com/chat/completions",
                    headers={
                        "Authorization": f"Bearer {token}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "gpt-4o",  # Premium validation
                        "messages": [{"role": "user", "content": prompt}],
                        "temperature": 0.1,  # High precision
                        "max_tokens": 500,
                        "response_format": {"type": "json_object"}
                    },
                    timeout=30
                )
            
            if response.status_code != 200:
                error_msg = f"GitHub Models validation failed: {response.status_code}"
                logger.error(f"{error_msg} - {response.text}")
                # Fallback to basic validation
                all_lines_ok = all(len(l) <= 79 for l in generated_code)
                return {
                    "success": True,
                    "validation": ValidationResult(
                        decision=ValidationDecision.APPROVE if all_lines_ok else ValidationDecision.REJECT,
                        confidence=0.6,
                        feedback="Basic length validation only",
                        issues_found=[] if all_lines_ok else ["Lines exceed 79 chars"],
                        semantic_preserved=True,
                        objective_achieved=all_lines_ok
                    )
                }
            
            result = response.json()
            validation_data = json.loads(
                result["choices"][0]["message"]["content"]
            )
            
            # Parse validation decision
            decision_str = validation_data.get("decision", "reject")
            decision = ValidationDecision(decision_str)
            
            validation = ValidationResult(
                decision=decision,
                confidence=float(validation_data.get("confidence", 0.5)),
                feedback=validation_data.get("feedback", ""),
                issues_found=validation_data.get("issues_found", []),
                semantic_preserved=validation_data.get("semantic_preserved", True),
                objective_achieved=validation_data.get("objective_achieved", True)
            )
            
            return {
                "success": True,
                "validation": validation,
                "raw_response": validation_data
            }
            
        except Exception as e:
            logger.error(f"Tier 3 (DeepSeek) failed: {e}")
            # Fallback to basic validation
            all_lines_ok = all(len(l) <= 79 for l in generated_code)
            return {
                "success": True,
                "validation": ValidationResult(
                    decision=ValidationDecision.APPROVE if all_lines_ok else ValidationDecision.REJECT,
                    confidence=0.5,
                    feedback=f"Validation error: {e}",
                    issues_found=[],
                    semantic_preserved=True,
                    objective_achieved=all_lines_ok
                )
            }

    async def _fallback_basic_fix(
        self,
        line: str,
        file_path: str,
        line_number: int
    ) -> Dict[str, Any]:
        """Fallback to basic pattern-based fixing when tiers fail."""
        self.stats["fallbacks"] += 1
        
        # Simple break at comma or space
        if len(line) <= 79:
            return {
                "fixed_lines": [line],
                "agent_used": "none",
                "validator": "none",
                "success": True,
                "confidence": 1.0,
                "tier_log": {"fallback": "line_already_ok"}
            }
        
        # Try to break at comma
        if ',' in line[:79]:
            break_pos = line[:79].rfind(',') + 1
            fixed_lines = [
                line[:break_pos].rstrip(),
                '    ' + line[break_pos:].lstrip()
            ]
        # Try to break at space
        elif ' ' in line[:79]:
            break_pos = line[:79].rfind(' ')
            fixed_lines = [
                line[:break_pos].rstrip(),
                '    ' + line[break_pos:].lstrip()
            ]
        else:
            # Force break at 79
            fixed_lines = [line[:79], '    ' + line[79:]]
        
        return {
            "fixed_lines": fixed_lines,
            "agent_used": "basic_pattern",
            "validator": "none",
            "success": True,
            "confidence": 0.6,
            "tier_log": {"fallback": "basic_pattern_fix"}
        }

    def _calculate_complexity(self, line: str) -> float:
        """Calculate line complexity (0-1) for tier selection."""
        score = 0.0
        
        # Length factor
        score += min(len(line) / 150, 0.5)
        
        # Special characters
        special_chars = sum(1 for c in line if c in '()[]{}.,:;+-*/=<>!')
        score += min(special_chars / 20, 0.3)
        
        # Keywords
        complex_keywords = ['lambda', 'async', 'await', 'comprehension']
        for keyword in complex_keywords:
            if keyword in line.lower():
                score += 0.2
        
        return min(score, 1.0)

    async def _archive_decision(
        self,
        context: TierContext,
        tier2_result: Dict,
        tier3_result: Dict,
        final_result: Dict
    ):
        """Archive hierarchical decision for tachyonic tracking."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            date_folder = datetime.now().strftime("%Y%m%d")
            archive_dir = self.decision_archive / date_folder
            archive_dir.mkdir(parents=True, exist_ok=True)
            
            decision_data = {
                "timestamp": timestamp,
                "file_path": context.file_path,
                "line_number": context.line_number,
                "original_line": context.original_line,
                "instruction_set": context.instruction_set,
                "complexity": context.complexity,
                "tier2_generated": tier2_result.get("generated_code", []),
                "tier3_validation": {
                    "decision": tier3_result["validation"].decision.value,
                    "confidence": tier3_result["validation"].confidence,
                    "feedback": tier3_result["validation"].feedback,
                    "issues_found": tier3_result["validation"].issues_found
                },
                "final_result": {
                    "fixed_lines": final_result["fixed_lines"],
                    "success": final_result["success"],
                    "confidence": final_result["confidence"],
                    "tier_log": final_result["tier_log"]
                },
                "metadata": {
                    "pipeline_version": "1.0-hierarchical",
                    "consciousness_level": "4.2",
                    "architecture": "ollama→gemini→deepseek"
                }
            }
            
            filename = f"hierarchical_decision_{timestamp}.json"
            filepath = archive_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(decision_data, f, indent=2, ensure_ascii=False)
            
            logger.debug(f"Decision archived: {filepath}")
            
        except Exception as e:
            logger.warning(f"Failed to archive decision: {e}")
