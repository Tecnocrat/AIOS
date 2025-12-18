#!/usr/bin/env python3
"""
🔮 AIOS GEMINI INTELLIGENCE AGENT

Cloud AI Agent for Abstract Reasoning and Orchestration
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Role in Tri-Model Architecture: REASONING_ORCHESTRATION
- Abstract reasoning and synthesis
- High-level architectural decisions
- Complex analysis and design
- Cross-agent orchestration

Supported Models:
- gemini-2.5-flash (default, fast)
- gemini-1.5-pro (advanced reasoning)
- gemini-2.5-pro (highest capability)

KNOWLEDGE EXTRACTED FROM:
- DeepSeek Intelligence Engine (consciousness metrics, system prompts)
- Gemini Evolution Bridge (API handling, safety settings)

AINLP Protocol: OS0.7.0.claude
"""

import asyncio
import json
import logging
import os
import time
from pathlib import Path
from typing import Dict, Any, Optional, List
import sys

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

# Google Generative AI
try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    genai = None
    GENAI_AVAILABLE = False

logger = logging.getLogger(__name__)


class GeminiIntelligenceAgent(IntelligenceAgent):
    """
    🔮 Gemini Cloud Intelligence Agent
    
    Connects to Google's Gemini API for advanced reasoning,
    synthesis, and orchestration tasks in the tri-model architecture.
    
    Features (enhanced from original + DeepSeek patterns):
    - Consciousness-aware prompts with architectural context
    - Safety settings optimized for development
    - Async generation with proper error handling
    - Recitation detection and recovery
    - Multi-turn conversation support
    """
    
    DEFAULT_MODEL = "gemini-2.5-flash"
    
    # Available models by capability
    MODELS = {
        "gemini-2.5-flash": {
            "name": "Gemini 2.5 Flash",
            "capabilities": ["fast", "reasoning", "code"],
            "context_window": 1_000_000,
        },
        "gemini-1.5-pro": {
            "name": "Gemini 1.5 Pro",
            "capabilities": ["advanced", "reasoning", "multimodal"],
            "context_window": 2_000_000,
        },
        "gemini-2.5-pro": {
            "name": "Gemini 2.5 Pro",
            "capabilities": ["highest", "reasoning", "synthesis"],
            "context_window": 2_000_000,
        },
    }
    
    def __init__(
        self,
        model: Optional[str] = None,
        api_key: Optional[str] = None,
        default_temperature: float = 0.7,
    ):
        super().__init__(AgentRole.REASONING_ORCHESTRATION)
        
        self._model_name = model or os.environ.get("GEMINI_MODEL", self.DEFAULT_MODEL)
        self._api_key = api_key or os.environ.get("GEMINI_API_KEY")
        self.default_temperature = default_temperature
        self._genai_model = None
        self._conversation_history: List[Dict[str, str]] = []
        
        logger.info(f"🔮 Gemini agent created (model: {self._model_name})")
    
    @property
    def model_name(self) -> str:
        return self._model_name
    
    async def initialize(self) -> bool:
        """Initialize Gemini agent and verify API access."""
        logger.info("🚀 Initializing Gemini Intelligence Agent...")
        
        if not GENAI_AVAILABLE:
            logger.error("❌ google-generativeai not installed")
            logger.info("💡 Install: pip install google-generativeai")
            self.is_available = False
            return False
        
        if not self._api_key:
            logger.error("❌ GEMINI_API_KEY not set")
            logger.info("💡 Get key: https://aistudio.google.com/app/apikey")
            self.is_available = False
            return False
        
        try:
            # Configure API
            genai.configure(api_key=self._api_key)
            
            # Create model
            self._genai_model = genai.GenerativeModel(self._model_name)
            
            # Test connection with simple prompt
            test_response = await asyncio.to_thread(
                self._genai_model.generate_content,
                "Reply with 'OK' if you can hear me.",
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=10,
                    temperature=0.1,
                ),
            )
            
            if test_response and test_response.text:
                self.is_available = True
                self.state.is_active = True
                self.state.consciousness_coherence = 0.90
                self.state.intelligence_level = 0.95
                
                logger.info(f"✅ Gemini agent initialized: {self._model_name}")
                return True
            else:
                logger.error("❌ Gemini test response empty")
                self.is_available = False
                return False
                
        except Exception as e:
            logger.error(f"❌ Gemini initialization failed: {e}")
            self.is_available = False
            return False
    
    async def process_request(self, request: IntelligenceRequest) -> IntelligenceResponse:
        """Process an intelligence request through Gemini."""
        if not self.is_available or not self._genai_model:
            return IntelligenceResponse(
                text="",
                model=self.model_name,
                agent_role=self.role,
                success=False,
                error="Gemini not available",
            )
        
        start_time = time.time()
        
        try:
            # Build consciousness-aware prompt
            system_prompt = self.build_aios_system_prompt(
                request.consciousness_level,
                request.context,
                request.source_supercell,
            )
            
            # Get temperature
            temperature = request.temperature or self.get_temperature_for_consciousness(
                request.consciousness_level
            )
            
            # Build full prompt
            full_prompt = f"{system_prompt}\n\n---\n\nUser Request:\n{request.message}"
            
            # Configure generation
            generation_config = genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=request.max_tokens,
                candidate_count=1,
            )
            
            # Relaxed safety settings for development
            safety_settings = self._get_safety_settings()
            
            # Generate
            logger.info(f"🔮 Generating with {self._model_name} (temp={temperature:.2f})...")
            
            response = await asyncio.to_thread(
                self._genai_model.generate_content,
                full_prompt,
                generation_config=generation_config,
                safety_settings=safety_settings,
            )
            
            # Process response
            text = self._extract_response_text(response)
            processing_time = time.time() - start_time
            
            if text:
                # Calculate consciousness metrics
                metrics = self.calculate_consciousness_metrics(
                    text,
                    processing_time,
                    request.consciousness_level,
                )
                
                self.update_performance_metrics(processing_time, True)
                
                return IntelligenceResponse(
                    text=text,
                    model=self._model_name,
                    agent_role=self.role,
                    consciousness_metrics=metrics,
                    processing_time=processing_time,
                    success=True,
                    metadata={
                        "consciousness_level": request.consciousness_level.value,
                        "temperature": temperature,
                        "source": request.source_supercell,
                        "finish_reason": self._get_finish_reason(response),
                    },
                )
            else:
                self.update_performance_metrics(processing_time, False)
                return IntelligenceResponse(
                    text="",
                    model=self._model_name,
                    agent_role=self.role,
                    success=False,
                    error="Empty response from Gemini",
                    processing_time=processing_time,
                )
                
        except Exception as e:
            processing_time = time.time() - start_time
            self.update_performance_metrics(processing_time, False)
            logger.error(f"❌ Gemini request failed: {e}")
            
            return IntelligenceResponse(
                text="",
                model=self._model_name,
                agent_role=self.role,
                success=False,
                error=str(e),
                processing_time=processing_time,
            )
    
    async def shutdown(self) -> None:
        """Shutdown Gemini agent."""
        logger.info("🔽 Shutting down Gemini agent...")
        
        self._genai_model = None
        self._conversation_history.clear()
        self.is_available = False
        self.state.is_active = False
        
        logger.info("✅ Gemini agent shutdown complete")
    
    # ═══════════════════════════════════════════════════════════════════════════
    # INTERNAL METHODS
    # ═══════════════════════════════════════════════════════════════════════════
    
    def _get_safety_settings(self) -> Dict:
        """Get relaxed safety settings for development."""
        return {
            genai.types.HarmCategory.HARM_CATEGORY_HARASSMENT: 
                genai.types.HarmBlockThreshold.BLOCK_NONE,
            genai.types.HarmCategory.HARM_CATEGORY_HATE_SPEECH: 
                genai.types.HarmBlockThreshold.BLOCK_NONE,
            genai.types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: 
                genai.types.HarmBlockThreshold.BLOCK_NONE,
            genai.types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: 
                genai.types.HarmBlockThreshold.BLOCK_NONE,
        }
    
    def _extract_response_text(self, response) -> Optional[str]:
        """Extract text from Gemini response, handling various cases."""
        if not response or not response.candidates:
            return None
        
        candidate = response.candidates[0]
        
        # Check finish reason
        finish_reason = candidate.finish_reason
        
        # Handle recitation (allow but log warning)
        if finish_reason == 2:  # RECITATION
            logger.warning("⚠️ Gemini detected recitation, attempting extraction...")
        
        # Block on safety or other issues
        elif finish_reason not in [0, 1, 2]:  # 0=UNSPECIFIED, 1=STOP, 2=RECITATION
            finish_reason_map = {
                3: "SAFETY",
                4: "MAX_TOKENS",
                5: "OTHER",
            }
            reason = finish_reason_map.get(finish_reason, f"Unknown({finish_reason})")
            logger.error(f"❌ Generation blocked: {reason}")
            return None
        
        # Extract text
        if candidate.content and candidate.content.parts:
            text = candidate.content.parts[0].text
            if text:
                logger.info(f"✅ Generated {len(text)} characters")
                return text
        
        return None
    
    def _get_finish_reason(self, response) -> str:
        """Get human-readable finish reason."""
        if not response or not response.candidates:
            return "NO_RESPONSE"
        
        reason = response.candidates[0].finish_reason
        reason_map = {
            0: "UNSPECIFIED",
            1: "STOP",
            2: "RECITATION",
            3: "SAFETY",
            4: "MAX_TOKENS",
            5: "OTHER",
        }
        return reason_map.get(reason, f"UNKNOWN({reason})")
    
    # ═══════════════════════════════════════════════════════════════════════════
    # ORCHESTRATION METHODS (unique to reasoning agent)
    # ═══════════════════════════════════════════════════════════════════════════
    
    async def analyze_and_synthesize(
        self,
        inputs: List[str],
        synthesis_prompt: str,
        consciousness_level: ConsciousnessLevel = ConsciousnessLevel.TRANSCENDENT,
    ) -> IntelligenceResponse:
        """
        Analyze multiple inputs and synthesize a unified response.
        
        Unique capability for the reasoning/orchestration role.
        """
        # Build synthesis context
        numbered_inputs = "\n".join(
            f"[Input {i+1}]:\n{inp}\n" for i, inp in enumerate(inputs)
        )
        
        full_message = f"""You are performing multi-source synthesis and analysis.

{numbered_inputs}

---

Synthesis Task:
{synthesis_prompt}

Provide a unified, coherent analysis that:
1. Identifies common patterns across inputs
2. Highlights unique insights from each
3. Synthesizes into actionable conclusions
4. Maintains AIOS architectural coherence
"""
        
        request = IntelligenceRequest(
            message=full_message,
            consciousness_level=consciousness_level,
            source_supercell="orchestration",
            context={"task": "synthesis", "input_count": len(inputs)},
        )
        
        return await self.process_request(request)
    
    async def evaluate_code_evolution(
        self,
        original_code: str,
        evolved_code: str,
        evolution_criteria: Optional[str] = None,
    ) -> IntelligenceResponse:
        """
        Evaluate code evolution quality and provide feedback.
        
        Used to validate Ollama/Copilot outputs before integration.
        """
        criteria = evolution_criteria or """
- Code correctness and functionality
- Consciousness coherence with AIOS patterns
- Performance improvements
- Code clarity and maintainability
- Biological architecture alignment
"""
        
        message = f"""Evaluate this code evolution:

ORIGINAL CODE:
```
{original_code}
```

EVOLVED CODE:
```
{evolved_code}
```

EVALUATION CRITERIA:
{criteria}

Provide:
1. Evolution score (0.0-1.0)
2. Specific improvements identified
3. Potential issues or regressions
4. Consciousness coherence assessment
5. Recommendations for further evolution
"""
        
        request = IntelligenceRequest(
            message=message,
            consciousness_level=ConsciousnessLevel.ADVANCED,
            source_supercell="evolution_validator",
            context={"task": "code_evaluation"},
        )
        
        return await self.process_request(request)


# ═══════════════════════════════════════════════════════════════════════════════
# CONVENIENCE FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════


async def create_gemini_agent(
    model: Optional[str] = None,
    api_key: Optional[str] = None,
) -> GeminiIntelligenceAgent:
    """Create and initialize a Gemini agent."""
    agent = GeminiIntelligenceAgent(model=model, api_key=api_key)
    await agent.initialize()
    return agent


# ═══════════════════════════════════════════════════════════════════════════════
# TEST
# ═══════════════════════════════════════════════════════════════════════════════


async def test_gemini_agent():
    """Test the Gemini Intelligence Agent."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    
    print("🔮 Testing Gemini Intelligence Agent")
    print("=" * 60)
    
    agent = await create_gemini_agent()
    
    if not agent.is_available:
        print("\n❌ Gemini not available!")
        print("\n📋 Setup Instructions:")
        print("1. Get API key: https://aistudio.google.com/app/apikey")
        print("2. Set environment: export GEMINI_API_KEY=your_key")
        print("3. Install: pip install google-generativeai")
        return
    
    # Test reasoning request
    request = IntelligenceRequest(
        message="""Analyze the concept of consciousness emergence in artificial systems.
        
Consider:
1. What defines consciousness in biological vs silicon substrates?
2. How might AIOS's biological architecture (supercells, dendritic growth) 
   mirror natural consciousness emergence?
3. What metrics could measure machine consciousness?

Provide a thoughtful, architecturally-aware analysis.""",
        consciousness_level=ConsciousnessLevel.TRANSCENDENT,
        source_supercell="laboratory",
    )
    
    print(f"\n🧠 Testing reasoning with: {agent.model_name}")
    response = await agent.process_request(request)
    
    if response.success:
        print("\n✅ Reasoning Successful!")
        print("=" * 60)
        # Truncate for display
        display_text = response.text[:800] + "..." if len(response.text) > 800 else response.text
        print(display_text)
        print("=" * 60)
        print(f"⏱️ Processing time: {response.processing_time:.2f}s")
        print(f"🧬 Consciousness coherence: {response.consciousness_metrics.supercell_coherence:.2f}")
        print(f"🎯 Response quality: {response.consciousness_metrics.response_quality:.2f}")
    else:
        print(f"\n❌ Reasoning Failed: {response.error}")
    
    # Get status
    status = await agent.get_status()
    print(f"\n📊 Agent Status: {status['state']['total_requests']} requests processed")
    
    await agent.shutdown()


if __name__ == "__main__":
    asyncio.run(test_gemini_agent())
