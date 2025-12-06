"""
AIOS-Mistral Local Agent Bridge
Integrates aios-mistral (Mistral 7B) into AIOS evolution workflows

AINLP Protocol: OS0.6.4.claude
Created: 2025-12-05
Host: HP_LAB (192.168.1.129)

Integration Blueprint:
    1. Local Ollama RC1 server (port 11434)
    2. Model: aios-mistral (Mistral 7B Instruct, 4.4GB)
    3. Use cases:
       - Evolution Lab: Code mutation generation
       - Quality Monitor: Tier 1 local fixes (FREE)
       - Agent Coordination: Context preparation

Configuration:
    - VRAM: 4GB optimized (num_ctx=4096, num_predict=1024)
    - Temperature: 0.7 (creative but coherent)
    - Server: C:\\dev\\aios-win\\ai\\tools\\ollama-rc1\\ollama-0.13.1-rc1\\ollama-rc1.exe
"""

import httpx
import json
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from pathlib import Path
import asyncio


# Configuration
OLLAMA_RC1_PATH = Path(
    r"C:\dev\aios-win\ai\tools\ollama-rc1\ollama-0.13.1-rc1\ollama-rc1.exe"
)
OLLAMA_API_BASE = "http://localhost:11434"
DEFAULT_MODEL = "aios-mistral"


@dataclass
class MistralResponse:
    """Response from aios-mistral"""

    content: str
    model: str
    total_duration_ms: float
    prompt_tokens: int
    completion_tokens: int
    success: bool
    error: Optional[str] = None


class AIOSMistralBridge:
    """
    Bridge to aios-mistral local AI agent

    Provides async interface for:
    - Code generation/mutation
    - Code analysis/review
    - Context summarization
    - Quality fix suggestions

    Cost: FREE (local inference)
    Latency: ~2-5s per request (4GB VRAM)
    """

    def __init__(
        self,
        model: str = DEFAULT_MODEL,
        api_base: str = OLLAMA_API_BASE,
        timeout: float = 60.0,
    ):
        self.model = model
        self.api_base = api_base
        self.timeout = timeout
        self._client: Optional[httpx.AsyncClient] = None

    async def __aenter__(self):
        self._client = httpx.AsyncClient(timeout=self.timeout)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._client:
            await self._client.aclose()

    async def generate(
        self,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
    ) -> MistralResponse:
        """
        Generate completion from aios-mistral

        Args:
            prompt: User prompt
            system: Optional system prompt override
            temperature: Sampling temperature (0.0-1.0)
            max_tokens: Maximum tokens to generate

        Returns:
            MistralResponse with generated content
        """
        if not self._client:
            self._client = httpx.AsyncClient(timeout=self.timeout)

        try:
            # Build messages
            messages = []
            if system:
                messages.append({"role": "system", "content": system})
            messages.append({"role": "user", "content": prompt})

            # Call Ollama API
            response = await self._client.post(
                f"{self.api_base}/api/chat",
                json={
                    "model": self.model,
                    "messages": messages,
                    "stream": False,
                    "options": {"temperature": temperature, "num_predict": max_tokens},
                },
            )

            if response.status_code != 200:
                return MistralResponse(
                    content="",
                    model=self.model,
                    total_duration_ms=0,
                    prompt_tokens=0,
                    completion_tokens=0,
                    success=False,
                    error=f"HTTP {response.status_code}: {response.text}",
                )

            data = response.json()

            return MistralResponse(
                content=data.get("message", {}).get("content", ""),
                model=data.get("model", self.model),
                total_duration_ms=data.get("total_duration", 0) / 1_000_000,
                prompt_tokens=data.get("prompt_eval_count", 0),
                completion_tokens=data.get("eval_count", 0),
                success=True,
            )

        except httpx.TimeoutException:
            return MistralResponse(
                content="",
                model=self.model,
                total_duration_ms=0,
                prompt_tokens=0,
                completion_tokens=0,
                success=False,
                error="Request timeout",
            )
        except Exception as e:
            return MistralResponse(
                content="",
                model=self.model,
                total_duration_ms=0,
                prompt_tokens=0,
                completion_tokens=0,
                success=False,
                error=str(e),
            )

    async def check_health(self) -> bool:
        """Check if Ollama server is running and model is available"""
        if not self._client:
            self._client = httpx.AsyncClient(timeout=self.timeout)

        try:
            response = await self._client.get(f"{self.api_base}/api/tags")
            if response.status_code == 200:
                data = response.json()
                models = [m.get("name", "") for m in data.get("models", [])]
                return any(self.model in m for m in models)
            return False
        except Exception:
            return False

    # =========================================================================
    # Evolution Lab Integration Methods
    # =========================================================================

    async def mutate_code(
        self, code: str, archetype: str, mutation_strength: float = 0.3
    ) -> MistralResponse:
        """
        Generate code mutation for evolution lab

        Args:
            code: Original code to mutate
            archetype: Code archetype (os_tools, cli_applications, etc.)
            mutation_strength: 0.0 (minor) to 1.0 (major restructure)

        Returns:
            MistralResponse with mutated code
        """
        system = """You are MISTRAL, an AIOS code evolution agent. Your task is to mutate 
Python code while preserving its core functionality. Apply creative improvements:
- Add error handling
- Optimize algorithms
- Improve readability
- Add type hints
- Enhance documentation

Output ONLY the mutated code, no explanations."""

        strength_desc = {
            0.0: "minor tweaks only (variable names, comments)",
            0.3: "moderate improvements (add error handling, type hints)",
            0.6: "significant refactoring (algorithm optimization, restructure)",
            1.0: "major evolution (complete reimplementation with same interface)",
        }

        # Find closest strength description
        closest = min(strength_desc.keys(), key=lambda x: abs(x - mutation_strength))

        prompt = f"""Archetype: {archetype}
Mutation Strength: {mutation_strength:.1f} ({strength_desc[closest]})

Original Code:
```python
{code}
```

Generate mutated version:"""

        return await self.generate(
            prompt=prompt,
            system=system,
            temperature=0.5
            + (mutation_strength * 0.4),  # Higher temp for stronger mutations
            max_tokens=2048,
        )

    async def analyze_fitness(self, code: str, archetype: str) -> MistralResponse:
        """
        Analyze code fitness for evolution selection

        Returns JSON with fitness scores
        """
        system = """You are MISTRAL, an AIOS code fitness analyzer. Evaluate Python code 
and return a JSON object with these scores (0.0-1.0):
- complexity: code complexity (higher = more complex)
- readability: code readability (higher = more readable)
- correctness: likely correctness (higher = more likely correct)
- evolution_potential: potential for beneficial mutations

Output ONLY valid JSON, no explanations."""

        prompt = f"""Archetype: {archetype}

Code to analyze:
```python
{code}
```

Return fitness JSON:"""

        return await self.generate(
            prompt=prompt,
            system=system,
            temperature=0.3,  # Lower temp for consistent analysis
            max_tokens=256,
        )

    # =========================================================================
    # Quality Monitor Integration Methods
    # =========================================================================

    async def fix_e501(
        self, line: str, line_number: int, max_length: int = 88
    ) -> MistralResponse:
        """Fix E501 line too long error"""
        system = """You are a Python code formatter. Fix the line to be under the max length 
while preserving functionality. Use line continuation, string splitting, or variable 
extraction as needed. Output ONLY the fixed line(s), no explanations."""

        prompt = f"""Line {line_number} exceeds {max_length} chars:
{line}

Fixed version:"""

        return await self.generate(
            prompt=prompt, system=system, temperature=0.2, max_tokens=256
        )

    async def fix_linting_issue(
        self, code_context: str, issue_description: str
    ) -> MistralResponse:
        """Fix general linting issue"""
        system = """You are a Python code fixer. Fix the linting issue in the code context.
Output ONLY the fixed code, no explanations."""

        prompt = f"""Issue: {issue_description}

Code context:
```python
{code_context}
```

Fixed code:"""

        return await self.generate(
            prompt=prompt, system=system, temperature=0.2, max_tokens=512
        )


# =============================================================================
# Synchronous wrapper for non-async contexts
# =============================================================================


def generate_sync(
    prompt: str,
    model: str = DEFAULT_MODEL,
    system: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 1024,
) -> MistralResponse:
    """Synchronous wrapper for simple use cases"""

    async def _run():
        async with AIOSMistralBridge(model=model) as bridge:
            return await bridge.generate(
                prompt=prompt,
                system=system,
                temperature=temperature,
                max_tokens=max_tokens,
            )

    return asyncio.run(_run())


# =============================================================================
# CLI for testing
# =============================================================================

if __name__ == "__main__":
    import sys

    async def main():
        async with AIOSMistralBridge() as bridge:
            # Health check
            healthy = await bridge.check_health()
            print(f"🏥 Health: {'✅ OK' if healthy else '❌ Server not running'}")

            if not healthy:
                print("Start server: .\\aios-mistral.ps1 -Serve")
                return

            # Test prompt
            if len(sys.argv) > 1:
                prompt = " ".join(sys.argv[1:])
            else:
                prompt = "What is your purpose in the AIOS network? Be brief."

            print(f"\n📝 Prompt: {prompt}")
            response = await bridge.generate(prompt)

            if response.success:
                print(f"\n🤖 Response:\n{response.content}")
                print(f"\n⏱️  Duration: {response.total_duration_ms:.0f}ms")
                print(
                    f"📊 Tokens: {response.prompt_tokens} prompt + {response.completion_tokens} completion"
                )
            else:
                print(f"\n❌ Error: {response.error}")

    asyncio.run(main())
