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

SDK Migration (2025-01): 
- Migrated from deprecated google.generativeai to google.genai
- New client-based pattern with types module
- See: https://github.com/googleapis/python-genai

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

# Google Generative AI - NEW SDK (google.genai)
genai = None
genai_types = None
genai_legacy = None
GENAI_AVAILABLE = False
GENAI_SDK_VERSION = None

try:
    from google import genai
    from google.genai import types as genai_types
    GENAI_AVAILABLE = True
    GENAI_SDK_VERSION = "new"  # google.genai (client-based)
except ImportError:
    # Fallback: try deprecated SDK (will be removed eventually)
    try:
        import google.generativeai as genai_legacy
        GENAI_AVAILABLE = True
        GENAI_SDK_VERSION = "legacy"  # google.generativeai (deprecated)
    except ImportError:
        pass  # All variables already set to default

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
        self._client = None  # New SDK uses client instead of model object
        self._legacy_model = None  # Legacy SDK model object
        self._chat = None    # For multi-turn conversations
        self._conversation_history: List[Dict[str, str]] = []
        
        logger.info("🔮 Gemini agent created (model: %s, sdk: %s)", self._model_name, GENAI_SDK_VERSION)
    
    @property
    def model_name(self) -> str:
        return self._model_name
    
    async def initialize(self) -> bool:
        """Initialize Gemini agent and verify API access."""
        logger.info("🚀 Initializing Gemini Intelligence Agent (SDK: %s)...", GENAI_SDK_VERSION)
        
        if not GENAI_AVAILABLE:
            logger.error("❌ google-genai not installed")
            logger.info("💡 Install: pip install google-genai")
            self.is_available = False
            return False
        
        if not self._api_key:
            logger.error("❌ GEMINI_API_KEY not set")
            logger.info("💡 Get key: https://aistudio.google.com/app/apikey")
            self.is_available = False
            return False
        
        try:
            if GENAI_SDK_VERSION == "new":
                # NEW SDK: Client-based pattern
                self._client = genai.Client(api_key=self._api_key)
                
                # Test connection with simple prompt
                # Note: max_output_tokens needs to be > 20 for short responses
                test_response = await asyncio.to_thread(
                    self._client.models.generate_content,
                    model=self._model_name,
                    contents="Say hello.",
                    config=genai_types.GenerateContentConfig(
                        max_output_tokens=50,
                        temperature=0.1,
                    ),
                )
                
                if test_response and test_response.text:
                    self.is_available = True
                    self.state.is_active = True
                    self.state.consciousness_coherence = 0.90
                    self.state.intelligence_level = 0.95
                    
                    logger.info("✅ Gemini agent initialized (new SDK): %s", self._model_name)
                    return True
                    
            elif GENAI_SDK_VERSION == "legacy":
                # LEGACY SDK: Deprecated pattern (fallback)
                logger.warning("⚠️ Using deprecated google.generativeai SDK")
                genai_legacy.configure(api_key=self._api_key)
                
                self._legacy_model = genai_legacy.GenerativeModel(self._model_name)
                
                test_response = await asyncio.to_thread(
                    self._legacy_model.generate_content,
                    "Reply with 'OK' if you can hear me.",
                    generation_config=genai_legacy.types.GenerationConfig(
                        max_output_tokens=10,
                        temperature=0.1,
                    ),
                )
                
                if test_response and test_response.text:
                    self.is_available = True
                    self.state.is_active = True
                    self.state.consciousness_coherence = 0.90
                    self.state.intelligence_level = 0.95
                    
                    logger.info("✅ Gemini agent initialized (legacy SDK): %s", self._model_name)
                    return True
            
            logger.error("❌ Gemini test response empty")
            self.is_available = False
            return False
                
        except (AttributeError, RuntimeError, ValueError, TimeoutError) as e:
            logger.error("❌ Gemini initialization failed: %s", e)
            self.is_available = False
            return False
    
    async def process_request(self, request: IntelligenceRequest) -> IntelligenceResponse:
        """Process an intelligence request through Gemini."""
        if not self.is_available:
            return IntelligenceResponse(
                text="",
                model=self.model_name,
                agent_role=self.role,
                success=False,
                error="Gemini not available",
            )
        
        # Check appropriate client/model based on SDK version
        if GENAI_SDK_VERSION == "new" and not self._client:
            return IntelligenceResponse(
                text="",
                model=self.model_name,
                agent_role=self.role,
                success=False,
                error="Gemini client not initialized",
            )
        elif GENAI_SDK_VERSION == "legacy" and not hasattr(self, '_legacy_model'):
            return IntelligenceResponse(
                text="",
                model=self.model_name,
                agent_role=self.role,
                success=False,
                error="Gemini model not initialized",
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
            
            # Generate based on SDK version
            logger.info("🔮 Generating with %s (temp=%.2f, sdk=%s)...", self._model_name, temperature, GENAI_SDK_VERSION)
            
            if GENAI_SDK_VERSION == "new":
                # NEW SDK: Client-based generation
                safety_settings = self._get_safety_settings_new()
                
                response = await asyncio.to_thread(
                    self._client.models.generate_content,
                    model=self._model_name,
                    contents=full_prompt,
                    config=genai_types.GenerateContentConfig(
                        temperature=temperature,
                        max_output_tokens=request.max_tokens,
                        safety_settings=safety_settings,
                    ),
                )
                text = response.text if response else None
                finish_reason = self._get_finish_reason_new(response)
                
            else:
                # LEGACY SDK: Model-based generation
                generation_config = genai_legacy.types.GenerationConfig(
                    temperature=temperature,
                    max_output_tokens=request.max_tokens,
                    candidate_count=1,
                )
                safety_settings = self._get_safety_settings_legacy()
                
                response = await asyncio.to_thread(
                    self._legacy_model.generate_content,
                    full_prompt,
                    generation_config=generation_config,
                    safety_settings=safety_settings,
                )
                text = self._extract_response_text_legacy(response)
                finish_reason = self._get_finish_reason_legacy(response)
            
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
                        "finish_reason": finish_reason,
                        "sdk_version": GENAI_SDK_VERSION,
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
                
        except (AttributeError, RuntimeError, ValueError, TimeoutError) as e:
            processing_time = time.time() - start_time
            self.update_performance_metrics(processing_time, False)
            logger.error("❌ Gemini request failed: %s", e)
            
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
        
        self._client = None
        if hasattr(self, '_legacy_model'):
            self._legacy_model = None
        self._chat = None
        self._conversation_history.clear()
        self.is_available = False
        self.state.is_active = False
        
        logger.info("✅ Gemini agent shutdown complete")
    
    # ═══════════════════════════════════════════════════════════════════════════
    # INTERNAL METHODS - NEW SDK (google.genai)
    # ═══════════════════════════════════════════════════════════════════════════
    
    def _get_safety_settings_new(self) -> List:
        """Get safety settings for new SDK (list of SafetySetting)."""
        if not genai_types:
            return []
        return [
            genai_types.SafetySetting(
                category='HARM_CATEGORY_HATE_SPEECH',
                threshold='BLOCK_ONLY_HIGH',
            ),
            genai_types.SafetySetting(
                category='HARM_CATEGORY_HARASSMENT',
                threshold='BLOCK_ONLY_HIGH',
            ),
            genai_types.SafetySetting(
                category='HARM_CATEGORY_SEXUALLY_EXPLICIT',
                threshold='BLOCK_ONLY_HIGH',
            ),
            genai_types.SafetySetting(
                category='HARM_CATEGORY_DANGEROUS_CONTENT',
                threshold='BLOCK_ONLY_HIGH',
            ),
        ]
    
    def _get_finish_reason_new(self, response) -> str:
        """Get finish reason from new SDK response."""
        if not response:
            return "NO_RESPONSE"
        # New SDK has different structure - text property handles this
        return "STOP"  # Simplified for now
    
    # ═══════════════════════════════════════════════════════════════════════════
    # INTERNAL METHODS - LEGACY SDK (google.generativeai) - DEPRECATED
    # ═══════════════════════════════════════════════════════════════════════════
    
    def _get_safety_settings_legacy(self) -> Dict:
        """Get relaxed safety settings for legacy SDK (deprecated)."""
        if not genai_legacy:
            return {}
        return {
            genai_legacy.types.HarmCategory.HARM_CATEGORY_HARASSMENT: 
                genai_legacy.types.HarmBlockThreshold.BLOCK_NONE,
            genai_legacy.types.HarmCategory.HARM_CATEGORY_HATE_SPEECH: 
                genai_legacy.types.HarmBlockThreshold.BLOCK_NONE,
            genai_legacy.types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: 
                genai_legacy.types.HarmBlockThreshold.BLOCK_NONE,
            genai_legacy.types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: 
                genai_legacy.types.HarmBlockThreshold.BLOCK_NONE,
        }
    
    def _extract_response_text_legacy(self, response) -> Optional[str]:
        """Extract text from legacy SDK response (deprecated)."""
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
            logger.error("❌ Generation blocked: %s", reason)
            return None
        
        # Extract text
        if candidate.content and candidate.content.parts:
            text = candidate.content.parts[0].text
            if text:
                logger.info("✅ Generated %d characters", len(text))
                return text
        
        return None
    
    def _get_finish_reason_legacy(self, response) -> str:
        """Get human-readable finish reason from legacy SDK (deprecated)."""
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
