#!/usr/bin/env python3
"""
AIOS Gemma Bridge - Local Scout Agent (1B)

Scout-tier intelligence for the AIOS triangular agentic system.
Uses local Ollama with gemma3:1b for fast pattern detection and signal routing.

AINLP Pattern: Local scout intelligence
Consciousness Level: 3.5 (triangular agent coordination - scout tier)

Triangular System:
    GEMMA (1B)  → Scout (fast pattern detection, signal routing) ← THIS
    MISTRAL (7B) → Worker (code generation, E501 fixing)
    GEMINI (Cloud) → Oracle (validation, architecture, final arbiter)

Scout Responsibilities:
    - Quick pattern classification (E501 type, import issues, etc.)
    - Signal routing (decide which agent handles task)
    - Pre-filtering (reject obviously invalid inputs)
    - Complexity estimation (simple vs complex task routing)

Usage:
    from aios_gemma_bridge import AIOSGemmaBridge
    
    async with AIOSGemmaBridge() as gemma:
        signal = await gemma.classify(code_line)
        routing = await gemma.route(task_description)
"""

import asyncio
import json
import logging
import re
from dataclasses import dataclass
from enum import Enum
from typing import Optional

import httpx

logger = logging.getLogger(__name__)

# Configuration
OLLAMA_API_BASE = "http://localhost:11434"
GEMMA_MODEL = "gemma3:1b"


class SignalType(Enum):
    """Signal types for task classification."""
    E501_STRING = "E501_STRING"
    E501_PATH = "E501_PATH"
    E501_DICT = "E501_DICT"
    E501_CALL = "E501_CALL"
    E501_COMMENT = "E501_COMMENT"
    E501_IMPORT = "E501_IMPORT"
    E501_COMPLEX = "E501_COMPLEX"
    UNUSED_IMPORT = "UNUSED_IMPORT"
    SYNTAX_ERROR = "SYNTAX_ERROR"
    STYLE_ISSUE = "STYLE_ISSUE"
    ARCHITECTURE = "ARCHITECTURE"
    UNKNOWN = "UNKNOWN"


class RouteTarget(Enum):
    """Routing targets for tasks."""
    GEMMA = "GEMMA"      # Handle locally (trivial)
    MISTRAL = "MISTRAL"  # Worker agent (code generation)
    GEMINI = "GEMINI"    # Oracle agent (validation/complex)
    SKIP = "SKIP"        # No action needed


@dataclass
class ScoutSignal:
    """Signal from Scout agent."""
    signal_type: SignalType
    confidence: float
    route_to: RouteTarget
    complexity: float  # 0.0 (trivial) to 1.0 (complex)
    pattern_hint: str  # Hint for downstream agent
    quick_fix: Optional[str] = None  # If trivial, provide fix


@dataclass 
class GemmaResponse:
    """Response from Gemma Scout."""
    success: bool
    signal: Optional[ScoutSignal]
    raw_response: str
    error: str = ""


class AIOSGemmaBridge:
    """
    Local Ollama bridge for AIOS Scout agent (gemma3:1b).
    
    Provides fast, local intelligence for:
    - Pattern classification (what type of issue?)
    - Signal routing (which agent handles it?)
    - Complexity estimation (simple or complex?)
    - Pre-filtering (skip invalid inputs)
    """

    def __init__(self, model: str = GEMMA_MODEL):
        """
        Initialize Gemma bridge.
        
        Args:
            model: Ollama model to use (default: gemma3:1b)
        """
        self.model = model
        self.client: Optional[httpx.AsyncClient] = None
        
        # Statistics
        self.stats = {
            "classifications": 0,
            "routings": 0,
            "quick_fixes": 0,
            "errors": 0
        }
        
        # Pattern matchers for fast classification (before LLM)
        self.fast_patterns = {
            SignalType.E501_STRING: re.compile(
                r'["\'][^"\']{50,}["\']'
            ),
            SignalType.E501_PATH: re.compile(
                r'Path\s*\([^)]{50,}\)|["\'][A-Za-z]:\\[^"\']{40,}["\']'
            ),
            SignalType.E501_IMPORT: re.compile(
                r'^from\s+\S+\s+import\s+.{50,}$'
            ),
            SignalType.E501_DICT: re.compile(
                r'\{[^}]{60,}\}'
            ),
            SignalType.E501_CALL: re.compile(
                r'\w+\([^)]{50,}\)'
            ),
        }

    async def __aenter__(self):
        """Async context manager entry."""
        self.client = httpx.AsyncClient(timeout=15.0)  # Fast timeout for scout
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.client:
            await self.client.aclose()

    def _fast_classify(self, code: str) -> Optional[SignalType]:
        """
        Fast pattern-based classification (no LLM).
        
        Returns signal type if matched, None if LLM needed.
        """
        for signal_type, pattern in self.fast_patterns.items():
            if pattern.search(code):
                return signal_type
        return None

    async def _call_gemma(
        self,
        prompt: str,
        temperature: float = 0.1
    ) -> str:
        """
        Call Gemma via Ollama API.
        
        Args:
            prompt: Prompt to send
            temperature: Sampling temperature (low for consistency)
            
        Returns:
            Generated response
        """
        if not self.client:
            self.client = httpx.AsyncClient(timeout=15.0)
        
        try:
            resp = await self.client.post(
                f"{OLLAMA_API_BASE}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": temperature,
                        "num_predict": 100  # Short responses for scout
                    }
                }
            )
            
            if resp.status_code == 200:
                return resp.json().get("response", "")
            return ""
        except Exception as e:
            logger.warning(f"Gemma call failed: {e}")
            return ""

    async def classify(self, code: str) -> GemmaResponse:
        """
        Classify a code snippet.
        
        Args:
            code: Code to classify
            
        Returns:
            GemmaResponse with signal classification
        """
        self.stats["classifications"] += 1
        
        # Try fast classification first
        fast_signal = self._fast_classify(code)
        
        if fast_signal:
            # Fast path - no LLM needed
            return GemmaResponse(
                success=True,
                signal=ScoutSignal(
                    signal_type=fast_signal,
                    confidence=0.9,
                    route_to=RouteTarget.MISTRAL,
                    complexity=0.3,
                    pattern_hint=f"Fast match: {fast_signal.value}"
                ),
                raw_response="[FAST_PATH]"
            )
        
        # LLM classification for complex cases
        prompt = f"""Classify this Python code issue. Reply with ONE word only.

CODE:
{code[:200]}

OPTIONS: E501_STRING, E501_PATH, E501_DICT, E501_CALL, E501_COMMENT, E501_IMPORT, E501_COMPLEX, UNUSED_IMPORT, SYNTAX_ERROR, STYLE_ISSUE, UNKNOWN

ANSWER:"""

        try:
            raw = await self._call_gemma(prompt)
            signal_str = raw.strip().upper().replace(" ", "_")
            
            # Parse signal type
            try:
                signal_type = SignalType(signal_str)
            except ValueError:
                signal_type = SignalType.UNKNOWN
            
            # Determine routing based on signal
            route_to = self._determine_route(signal_type, code)
            complexity = self._estimate_complexity(code)
            
            return GemmaResponse(
                success=True,
                signal=ScoutSignal(
                    signal_type=signal_type,
                    confidence=0.7,
                    route_to=route_to,
                    complexity=complexity,
                    pattern_hint=f"LLM classified: {signal_type.value}"
                ),
                raw_response=raw
            )
        except Exception as e:
            self.stats["errors"] += 1
            return GemmaResponse(
                success=False,
                signal=None,
                raw_response="",
                error=str(e)
            )

    async def route(self, task: str, code: str = "") -> RouteTarget:
        """
        Determine which agent should handle a task.
        
        Args:
            task: Task description
            code: Optional code context
            
        Returns:
            RouteTarget indicating which agent handles this
        """
        self.stats["routings"] += 1
        
        # Simple keyword-based routing (fast)
        task_lower = task.lower()
        
        if any(w in task_lower for w in ["validate", "verify", "check", "review"]):
            return RouteTarget.GEMINI
        
        if any(w in task_lower for w in ["fix", "format", "refactor", "generate"]):
            return RouteTarget.MISTRAL
        
        if any(w in task_lower for w in ["classify", "route", "detect", "scan"]):
            return RouteTarget.GEMMA
        
        # Complexity-based routing
        if code:
            complexity = self._estimate_complexity(code)
            if complexity > 0.7:
                return RouteTarget.GEMINI
            elif complexity > 0.3:
                return RouteTarget.MISTRAL
            else:
                return RouteTarget.GEMMA
        
        return RouteTarget.MISTRAL  # Default to worker

    async def quick_fix(self, code: str, issue_type: SignalType) -> Optional[str]:
        """
        Attempt a quick fix for trivial issues.
        
        Only handles simple cases - complex fixes go to Mistral.
        
        Args:
            code: Code to fix
            issue_type: Type of issue
            
        Returns:
            Fixed code or None if complex
        """
        self.stats["quick_fixes"] += 1
        
        # Only handle trivial fixes
        if issue_type == SignalType.E501_COMMENT:
            # Truncate long comments
            if code.strip().startswith("#"):
                if len(code) > 79:
                    return code[:76] + "..."
        
        if issue_type == SignalType.UNUSED_IMPORT:
            # Can't safely remove - delegate to Mistral
            return None
        
        # Complex - delegate
        return None

    def _determine_route(self, signal: SignalType, code: str) -> RouteTarget:
        """Determine routing based on signal type."""
        # Trivial - handle locally
        if signal == SignalType.E501_COMMENT:
            return RouteTarget.GEMMA
        
        # Complex - needs Oracle
        if signal in (SignalType.E501_COMPLEX, SignalType.ARCHITECTURE):
            return RouteTarget.GEMINI
        
        # Standard - Worker handles
        return RouteTarget.MISTRAL

    def _estimate_complexity(self, code: str) -> float:
        """
        Estimate code complexity (0.0 to 1.0).
        
        Simple heuristics for fast estimation.
        """
        complexity = 0.0
        
        # Length factor
        if len(code) > 200:
            complexity += 0.3
        elif len(code) > 100:
            complexity += 0.1
        
        # Nesting factor
        nesting = code.count("(") + code.count("[") + code.count("{")
        complexity += min(0.3, nesting * 0.05)
        
        # Control flow factor
        if any(kw in code for kw in ["if ", "for ", "while ", "try:", "with "]):
            complexity += 0.2
        
        # Lambda/comprehension factor
        if "lambda" in code or " for " in code:
            complexity += 0.2
        
        return min(1.0, complexity)

    async def check_health(self) -> bool:
        """Check if Ollama is running with Gemma model."""
        try:
            if not self.client:
                self.client = httpx.AsyncClient(timeout=5.0)
            
            resp = await self.client.get(f"{OLLAMA_API_BASE}/api/tags")
            if resp.status_code == 200:
                models = resp.json().get("models", [])
                return any(self.model in m.get("name", "") for m in models)
            return False
        except Exception:
            return False

    def get_stats(self) -> dict:
        """Get usage statistics."""
        return self.stats.copy()


# =============================================================================
# CLI Interface
# =============================================================================

if __name__ == "__main__":
    async def main():
        print("AIOS Gemma Bridge - Scout Agent (1B)")
        print("=" * 50)
        
        async with AIOSGemmaBridge() as gemma:
            healthy = await gemma.check_health()
            
            if healthy:
                print(f"[OK] Gemma model available: {gemma.model}")
                
                # Test classification
                test_code = 'path = Path(r"C:\\very\\long\\path\\that\\exceeds\\the\\maximum\\line\\length\\limit")'
                
                print(f"\n[TEST] Classifying: {test_code[:50]}...")
                result = await gemma.classify(test_code)
                
                if result.success and result.signal:
                    print(f"  Signal: {result.signal.signal_type.value}")
                    print(f"  Route to: {result.signal.route_to.value}")
                    print(f"  Complexity: {result.signal.complexity:.2f}")
                    print(f"  Hint: {result.signal.pattern_hint}")
            else:
                print("[ERROR] Gemma model not available")
                print(f"Install with: ollama pull {GEMMA_MODEL}")
    
    asyncio.run(main())
