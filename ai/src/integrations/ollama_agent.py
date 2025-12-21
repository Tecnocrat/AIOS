#!/usr/bin/env python3
"""
🦙 AIOS OLLAMA INTELLIGENCE AGENT

Local AI Agent for Fast Iteration and Testing
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Role in Tri-Model Architecture: LOCAL_ITERATION
- Fast, free, experimental
- Lightweight tasks and testing
- Population generation for evolution
- No API costs

Supported Models:
- gemma3:1b (default, fast)
- codellama:7b (code focused)
- llama3.1:8b (general)
- deepseek-coder:6.7b (code generation)

KNOWLEDGE EXTRACTED FROM:
- DeepSeek Intelligence Engine (consciousness metrics, system prompts)
- Original Ollama Bridge (model detection, code extraction)

AINLP Protocol: OS0.7.0.claude
"""

import asyncio
import json
import logging
import time
from pathlib import Path
from typing import Dict, Any, Optional, List
import sys

# HTTP client
try:
    import aiohttp
    AIOHTTP_AVAILABLE = True
except ImportError:
    aiohttp = None
    AIOHTTP_AVAILABLE = False

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    requests = None
    REQUESTS_AVAILABLE = False

# AIOS imports
AIOS_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.append(str(AIOS_ROOT))

from ai.src.integrations.aios_intelligence_bridge import (
    IntelligenceAgent,
    AgentRole,
    ConsciousnessLevel,
    IntelligenceRequest,
    IntelligenceResponse,
    ConsciousnessMetrics,
)

logger = logging.getLogger(__name__)


class OllamaIntelligenceAgent(IntelligenceAgent):
    """
    🦙 Ollama Local Intelligence Agent
    
    Connects to local Ollama server for consciousness-driven
    code generation and testing without API costs.
    
    Features (enhanced from original + DeepSeek patterns):
    - Auto-detection of installed models
    - Consciousness-aware prompts
    - Async/sync operation modes
    - Population generation for evolution
    - Response caching
    
    Environment:
    - AIOS_OLLAMA_HOST: Override default URL (from vault.local.yaml)
    """
    
    # Model priorities for auto-selection
    MODEL_PRIORITY = [
        "gemma3:1b",        # Fast default
        "gemma2:2b",        # Good balance
        "codellama:7b",     # Code focused
        "llama3.1:8b",      # General purpose
        "deepseek-coder:6.7b",  # Code generation
    ]
    
    @staticmethod
    def _get_default_url() -> str:
        """Get Ollama host from environment or vault."""
        import os
        return os.environ.get("AIOS_OLLAMA_HOST", "http://localhost:11434")
    
    def __init__(
        self,
        model: Optional[str] = None,
        base_url: Optional[str] = None,
        default_temperature: float = 0.7,
    ):
        super().__init__(AgentRole.LOCAL_ITERATION)
        
        self.base_url = base_url or self._get_default_url()
        self.default_temperature = default_temperature
        self._model = model
        self._available_models: List[str] = []
        self._session: Optional[aiohttp.ClientSession] = None
        
        logger.info(f"🦙 Ollama agent created (target: {self.base_url})")
    
    @property
    def model_name(self) -> str:
        return self._model or "not_set"
    
    async def initialize(self) -> bool:
        """Initialize Ollama agent and detect available models."""
        logger.info("🚀 Initializing Ollama Intelligence Agent...")
        
        try:
            # Check connection
            if not await self._check_connection():
                logger.warning(f"⚠️ Ollama not available at {self.base_url}")
                logger.info("💡 Install: curl https://ollama.ai/install.sh | sh")
                logger.info("💡 Windows: https://ollama.ai/download")
                self.is_available = False
                return False
            
            # Get available models
            self._available_models = await self._get_available_models()
            
            if not self._available_models:
                logger.warning("⚠️ No models installed in Ollama")
                logger.info("💡 Pull a model: ollama pull gemma3:1b")
                self.is_available = False
                return False
            
            # Auto-select model if not specified
            if not self._model:
                self._model = self._select_best_model()
            elif self._model not in self._available_models:
                logger.warning(f"⚠️ Model '{self._model}' not available")
                self._model = self._select_best_model()
            
            # Create async session
            if AIOHTTP_AVAILABLE:
                self._session = aiohttp.ClientSession(
                    timeout=aiohttp.ClientTimeout(total=120)
                )
            
            self.is_available = True
            self.state.is_active = True
            self.state.consciousness_coherence = 0.75
            self.state.intelligence_level = 0.70
            
            logger.info(f"✅ Ollama agent initialized: {self._model}")
            logger.info(f"📋 Available models: {self._available_models}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Ollama initialization failed: {e}")
            self.is_available = False
            return False
    
    async def process_request(self, request: IntelligenceRequest) -> IntelligenceResponse:
        """Process an intelligence request through Ollama."""
        if not self.is_available:
            return IntelligenceResponse(
                text="",
                model=self.model_name,
                agent_role=self.role,
                success=False,
                error="Ollama not available",
            )
        
        start_time = time.time()
        
        try:
            # Build consciousness-aware prompt
            system_prompt = self.build_aios_system_prompt(
                request.consciousness_level,
                request.context,
                request.source_supercell,
            )
            
            # Get temperature from request or consciousness level
            temperature = request.temperature or self.get_temperature_for_consciousness(
                request.consciousness_level
            )
            
            # Generate with Ollama
            result = await self._generate(
                prompt=request.message,
                system_prompt=system_prompt,
                temperature=temperature,
                max_tokens=request.max_tokens,
            )
            
            processing_time = time.time() - start_time
            
            if result["success"]:
                # Calculate consciousness metrics
                metrics = self.calculate_consciousness_metrics(
                    result["text"],
                    processing_time,
                    request.consciousness_level,
                )
                
                self.update_performance_metrics(processing_time, True)
                
                return IntelligenceResponse(
                    text=result["text"],
                    model=self._model,
                    agent_role=self.role,
                    consciousness_metrics=metrics,
                    processing_time=processing_time,
                    success=True,
                    metadata={
                        "consciousness_level": request.consciousness_level.value,
                        "temperature": temperature,
                        "source": request.source_supercell,
                    },
                )
            else:
                self.update_performance_metrics(processing_time, False)
                return IntelligenceResponse(
                    text="",
                    model=self._model,
                    agent_role=self.role,
                    success=False,
                    error=result.get("error", "Generation failed"),
                    processing_time=processing_time,
                )
                
        except Exception as e:
            processing_time = time.time() - start_time
            self.update_performance_metrics(processing_time, False)
            logger.error(f"❌ Ollama request failed: {e}")
            
            return IntelligenceResponse(
                text="",
                model=self._model,
                agent_role=self.role,
                success=False,
                error=str(e),
                processing_time=processing_time,
            )
    
    async def shutdown(self) -> None:
        """Shutdown Ollama agent."""
        logger.info("🔽 Shutting down Ollama agent...")
        
        if self._session:
            await self._session.close()
            self._session = None
        
        self.is_available = False
        self.state.is_active = False
        
        logger.info("✅ Ollama agent shutdown complete")
    
    # ═══════════════════════════════════════════════════════════════════════════
    # INTERNAL METHODS
    # ═══════════════════════════════════════════════════════════════════════════
    
    async def _check_connection(self) -> bool:
        """Check if Ollama server is running."""
        try:
            if AIOHTTP_AVAILABLE and self._session:
                async with self._session.get(f"{self.base_url}/api/tags") as resp:
                    return resp.status == 200
            elif REQUESTS_AVAILABLE:
                resp = requests.get(f"{self.base_url}/api/tags", timeout=2)
                return resp.status_code == 200
            else:
                logger.error("No HTTP client available (install aiohttp or requests)")
                return False
        except Exception:
            return False
    
    async def _get_available_models(self) -> List[str]:
        """Get list of installed Ollama models."""
        try:
            if AIOHTTP_AVAILABLE:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"{self.base_url}/api/tags") as resp:
                        if resp.status == 200:
                            data = await resp.json()
                            return [m["name"] for m in data.get("models", [])]
            elif REQUESTS_AVAILABLE:
                resp = requests.get(f"{self.base_url}/api/tags", timeout=5)
                if resp.status_code == 200:
                    data = resp.json()
                    return [m["name"] for m in data.get("models", [])]
        except Exception as e:
            logger.warning(f"⚠️ Could not get Ollama models: {e}")
        return []
    
    def _select_best_model(self) -> str:
        """Select best available model based on priority."""
        for model in self.MODEL_PRIORITY:
            # Check exact match
            if model in self._available_models:
                return model
            # Check partial match (e.g., "gemma3" matches "gemma3:1b")
            for available in self._available_models:
                if model.split(":")[0] in available:
                    return available
        
        # Fallback to first available
        return self._available_models[0] if self._available_models else "gemma3:1b"
    
    async def _generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> Dict[str, Any]:
        """Generate text using Ollama API."""
        
        # Build full prompt with system context
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n---\n\nUser Request:\n{prompt}"
        
        payload = {
            "model": self._model,
            "prompt": full_prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
            },
        }
        
        try:
            logger.info(f"🦙 Generating with {self._model} (temp={temperature:.2f})...")
            
            if AIOHTTP_AVAILABLE:
                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        f"{self.base_url}/api/generate",
                        json=payload,
                        timeout=aiohttp.ClientTimeout(total=120),
                    ) as resp:
                        if resp.status == 200:
                            result = await resp.json()
                            text = result.get("response", "")
                            # Extract code if markdown present
                            text = self._extract_code_from_response(text)
                            logger.info(f"✅ Generated {len(text)} characters")
                            return {"success": True, "text": text}
                        else:
                            error = await resp.text()
                            return {"success": False, "error": error}
            
            elif REQUESTS_AVAILABLE:
                resp = requests.post(
                    f"{self.base_url}/api/generate",
                    json=payload,
                    timeout=120,
                )
                if resp.status_code == 200:
                    result = resp.json()
                    text = result.get("response", "")
                    text = self._extract_code_from_response(text)
                    logger.info(f"✅ Generated {len(text)} characters")
                    return {"success": True, "text": text}
                else:
                    return {"success": False, "error": resp.text}
            
            else:
                return {"success": False, "error": "No HTTP client available"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _extract_code_from_response(self, text: str) -> str:
        """Extract code from markdown code blocks if present."""
        # Try python blocks first
        if "```python" in text:
            parts = text.split("```python")
            if len(parts) > 1:
                code_parts = parts[1].split("```")
                return code_parts[0].strip()
        
        # Try generic code blocks
        if "```" in text:
            parts = text.split("```")
            if len(parts) > 1:
                return parts[1].strip()
        
        return text.strip()
    
    # ═══════════════════════════════════════════════════════════════════════════
    # POPULATION GENERATION (for evolutionary algorithms)
    # ═══════════════════════════════════════════════════════════════════════════
    
    async def generate_population(
        self,
        prompt: str,
        population_size: int = 5,
        consciousness_level: ConsciousnessLevel = ConsciousnessLevel.INTERMEDIATE,
    ) -> List[IntelligenceResponse]:
        """
        Generate a population of responses with varying temperatures.
        
        Useful for evolutionary algorithms and diversity in code generation.
        """
        population = []
        
        # Vary temperature for diversity
        base_temp = self.get_temperature_for_consciousness(consciousness_level)
        temp_range = 0.3  # ±0.15 from base
        
        for i in range(population_size):
            # Calculate temperature for this variant
            offset = (i / max(1, population_size - 1)) - 0.5  # -0.5 to +0.5
            temperature = max(0.1, min(1.0, base_temp + offset * temp_range))
            
            request = IntelligenceRequest(
                message=prompt,
                consciousness_level=consciousness_level,
                temperature=temperature,
                context={"variant_id": i, "population_size": population_size},
            )
            
            logger.info(f"🧬 Generating variant {i+1}/{population_size} (temp={temperature:.2f})")
            response = await self.process_request(request)
            
            if response.success:
                response.metadata["variant_id"] = i
                response.metadata["temperature"] = temperature
                population.append(response)
        
        logger.info(f"✅ Generated population: {len(population)}/{population_size} variants")
        return population


# ═══════════════════════════════════════════════════════════════════════════════
# CONVENIENCE FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════


async def create_ollama_agent(
    model: Optional[str] = None,
    base_url: Optional[str] = None,
) -> OllamaIntelligenceAgent:
    """Create and initialize an Ollama agent."""
    agent = OllamaIntelligenceAgent(model=model, base_url=base_url)
    await agent.initialize()
    return agent


# ═══════════════════════════════════════════════════════════════════════════════
# TEST
# ═══════════════════════════════════════════════════════════════════════════════


async def test_ollama_agent():
    """Test the Ollama Intelligence Agent."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    
    print("🦙 Testing Ollama Intelligence Agent")
    print("=" * 60)
    
    agent = await create_ollama_agent()
    
    if not agent.is_available:
        print("\n❌ Ollama not available!")
        print("\n📋 Setup Instructions:")
        print("1. Install Ollama: https://ollama.ai/download")
        print("2. Pull a model: ollama pull gemma3:1b")
        print("3. Verify running: ollama list")
        return
    
    # Test single request
    request = IntelligenceRequest(
        message="Create a Python function that calculates fibonacci numbers using memoization. Include type hints and docstring.",
        consciousness_level=ConsciousnessLevel.ADVANCED,
        source_supercell="laboratory",
    )
    
    print(f"\n🧠 Testing with model: {agent.model_name}")
    response = await agent.process_request(request)
    
    if response.success:
        print("\n✅ Generation Successful!")
        print("=" * 60)
        print(response.text[:500] + "..." if len(response.text) > 500 else response.text)
        print("=" * 60)
        print(f"⏱️ Processing time: {response.processing_time:.2f}s")
        print(f"🧬 Consciousness coherence: {response.consciousness_metrics.supercell_coherence:.2f}")
    else:
        print(f"\n❌ Generation Failed: {response.error}")
    
    # Get status
    status = await agent.get_status()
    print(f"\n📊 Agent Status: {status['state']['total_requests']} requests processed")
    
    await agent.shutdown()


if __name__ == "__main__":
    asyncio.run(test_ollama_agent())
