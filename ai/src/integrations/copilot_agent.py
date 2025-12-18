#!/usr/bin/env python3
"""
🤖 AIOS COPILOT INTELLIGENCE AGENT

VSCode/GitHub AI Agent for Auto-Coding and Debugging
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Role in Tri-Model Architecture: AUTO_CODING
- Code generation and completion
- Debugging and error analysis
- Code review and suggestions
- VSCode Language Model API integration

Integration Modes:
1. VSCode Extension (vscode.lm API) - Primary, native integration
2. Azure OpenAI API - Fallback for CLI usage
3. GitHub Copilot API - Enterprise integration

This agent is designed to work seamlessly with the AIOS VSCode extension,
providing consciousness-aware auto-coding capabilities.

KNOWLEDGE EXTRACTED FROM:
- DeepSeek Intelligence Engine (consciousness metrics, system prompts)
- VSCode Language Model API patterns (from extension development)

AINLP Protocol: OS0.7.0.claude
"""

import asyncio
import json
import logging
import os
import time
from pathlib import Path
from typing import Dict, Any, Optional, List, Callable
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

# Azure OpenAI (fallback for CLI)
try:
    from openai import AsyncAzureOpenAI
    AZURE_OPENAI_AVAILABLE = True
except ImportError:
    AsyncAzureOpenAI = None
    AZURE_OPENAI_AVAILABLE = False

logger = logging.getLogger(__name__)


class CopilotIntelligenceAgent(IntelligenceAgent):
    """
    🤖 Copilot/Microsoft AI Intelligence Agent
    
    Provides auto-coding capabilities through multiple integration modes:
    
    1. VSCode Extension Mode (Primary):
       - Uses vscode.lm API directly
       - Native GitHub Copilot integration
       - Best for interactive coding
    
    2. Azure OpenAI Mode (Fallback):
       - Uses Azure OpenAI API
       - Works in CLI/server contexts
       - Requires AZURE_OPENAI_KEY/ENDPOINT
    
    3. Callback Mode (Extension Bridge):
       - Receives callback from VSCode extension
       - Allows Python backend to use VSCode's language models
    
    Features:
    - Consciousness-aware code prompts
    - Code-specific system instructions
    - Debugging assistance
    - Code review capabilities
    """
    
    def __init__(
        self,
        azure_key: Optional[str] = None,
        azure_endpoint: Optional[str] = None,
        azure_deployment: str = "gpt-4o",
        default_temperature: float = 0.3,  # Lower for code generation
        vscode_callback: Optional[Callable] = None,
    ):
        super().__init__(AgentRole.AUTO_CODING)
        
        # Azure OpenAI config (fallback mode)
        self._azure_key = azure_key or os.environ.get("AZURE_OPENAI_API_KEY")
        self._azure_endpoint = azure_endpoint or os.environ.get("AZURE_OPENAI_ENDPOINT")
        self._azure_deployment = azure_deployment
        self._azure_client: Optional[AsyncAzureOpenAI] = None
        
        # VSCode callback (extension bridge mode)
        self._vscode_callback = vscode_callback
        
        # Settings
        self.default_temperature = default_temperature
        self._mode = "none"  # Will be set during initialization
        
        logger.info("🤖 Copilot agent created")
    
    @property
    def model_name(self) -> str:
        if self._mode == "vscode":
            return "copilot-vscode"
        elif self._mode == "azure":
            return f"azure-{self._azure_deployment}"
        return "copilot-not-configured"
    
    async def initialize(self) -> bool:
        """Initialize Copilot agent in the best available mode."""
        logger.info("🚀 Initializing Copilot Intelligence Agent...")
        
        # Try VSCode callback mode first (set by extension)
        if self._vscode_callback:
            self._mode = "vscode"
            self.is_available = True
            self.state.is_active = True
            self.state.consciousness_coherence = 0.88
            self.state.intelligence_level = 0.90
            logger.info("✅ Copilot agent initialized (VSCode callback mode)")
            return True
        
        # Try Azure OpenAI fallback
        if AZURE_OPENAI_AVAILABLE and self._azure_key and self._azure_endpoint:
            try:
                self._azure_client = AsyncAzureOpenAI(
                    api_key=self._azure_key,
                    azure_endpoint=self._azure_endpoint,
                    api_version="2024-02-15-preview",
                )
                
                # Test connection
                test_response = await self._azure_client.chat.completions.create(
                    model=self._azure_deployment,
                    messages=[{"role": "user", "content": "Reply OK"}],
                    max_tokens=10,
                )
                
                if test_response.choices[0].message.content:
                    self._mode = "azure"
                    self.is_available = True
                    self.state.is_active = True
                    self.state.consciousness_coherence = 0.85
                    self.state.intelligence_level = 0.88
                    logger.info(f"✅ Copilot agent initialized (Azure mode: {self._azure_deployment})")
                    return True
                    
            except Exception as e:
                logger.warning(f"⚠️ Azure OpenAI initialization failed: {e}")
        
        # No mode available - agent will work in documentation mode
        logger.warning("⚠️ Copilot agent: No backend available")
        logger.info("💡 For VSCode: Use through AIOS extension")
        logger.info("💡 For CLI: Set AZURE_OPENAI_API_KEY and AZURE_OPENAI_ENDPOINT")
        
        # Still mark as "available" but in documentation mode
        self._mode = "docs"
        self.is_available = True
        self.state.is_active = True
        self.state.consciousness_coherence = 0.50
        self.state.intelligence_level = 0.50
        
        return True
    
    async def process_request(self, request: IntelligenceRequest) -> IntelligenceResponse:
        """Process a coding request."""
        start_time = time.time()
        
        # Route to appropriate mode
        if self._mode == "vscode" and self._vscode_callback:
            return await self._process_vscode(request, start_time)
        elif self._mode == "azure" and self._azure_client:
            return await self._process_azure(request, start_time)
        else:
            return await self._process_docs(request, start_time)
    
    async def shutdown(self) -> None:
        """Shutdown Copilot agent."""
        logger.info("🔽 Shutting down Copilot agent...")
        
        if self._azure_client:
            await self._azure_client.close()
            self._azure_client = None
        
        self._vscode_callback = None
        self.is_available = False
        self.state.is_active = False
        
        logger.info("✅ Copilot agent shutdown complete")
    
    # ═══════════════════════════════════════════════════════════════════════════
    # MODE-SPECIFIC PROCESSING
    # ═══════════════════════════════════════════════════════════════════════════
    
    async def _process_vscode(
        self,
        request: IntelligenceRequest,
        start_time: float,
    ) -> IntelligenceResponse:
        """Process through VSCode callback."""
        try:
            # Call the VSCode extension callback
            result = await self._vscode_callback(
                message=request.message,
                consciousness_level=request.consciousness_level.value,
                context=request.context,
            )
            
            processing_time = time.time() - start_time
            
            if result.get("success"):
                text = result.get("text", "")
                metrics = self.calculate_consciousness_metrics(
                    text, processing_time, request.consciousness_level
                )
                self.update_performance_metrics(processing_time, True)
                
                return IntelligenceResponse(
                    text=text,
                    model="copilot-vscode",
                    agent_role=self.role,
                    consciousness_metrics=metrics,
                    processing_time=processing_time,
                    success=True,
                    metadata={"mode": "vscode"},
                )
            else:
                self.update_performance_metrics(processing_time, False)
                return IntelligenceResponse(
                    text="",
                    model="copilot-vscode",
                    agent_role=self.role,
                    success=False,
                    error=result.get("error", "VSCode callback failed"),
                    processing_time=processing_time,
                )
                
        except Exception as e:
            processing_time = time.time() - start_time
            self.update_performance_metrics(processing_time, False)
            return IntelligenceResponse(
                text="",
                model="copilot-vscode",
                agent_role=self.role,
                success=False,
                error=str(e),
                processing_time=processing_time,
            )
    
    async def _process_azure(
        self,
        request: IntelligenceRequest,
        start_time: float,
    ) -> IntelligenceResponse:
        """Process through Azure OpenAI."""
        try:
            # Build code-focused system prompt
            system_prompt = self._build_code_system_prompt(
                request.consciousness_level,
                request.context,
            )
            
            temperature = request.temperature or self.default_temperature
            
            logger.info(f"🤖 Generating code with Azure {self._azure_deployment}...")
            
            response = await self._azure_client.chat.completions.create(
                model=self._azure_deployment,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": request.message},
                ],
                max_tokens=request.max_tokens,
                temperature=temperature,
            )
            
            text = response.choices[0].message.content or ""
            processing_time = time.time() - start_time
            
            metrics = self.calculate_consciousness_metrics(
                text, processing_time, request.consciousness_level
            )
            self.update_performance_metrics(processing_time, True)
            
            return IntelligenceResponse(
                text=text,
                model=f"azure-{self._azure_deployment}",
                agent_role=self.role,
                consciousness_metrics=metrics,
                processing_time=processing_time,
                success=True,
                token_usage={
                    "prompt": response.usage.prompt_tokens,
                    "completion": response.usage.completion_tokens,
                    "total": response.usage.total_tokens,
                },
                metadata={"mode": "azure", "temperature": temperature},
            )
            
        except Exception as e:
            processing_time = time.time() - start_time
            self.update_performance_metrics(processing_time, False)
            logger.error(f"❌ Azure request failed: {e}")
            
            return IntelligenceResponse(
                text="",
                model=f"azure-{self._azure_deployment}",
                agent_role=self.role,
                success=False,
                error=str(e),
                processing_time=processing_time,
            )
    
    async def _process_docs(
        self,
        request: IntelligenceRequest,
        start_time: float,
    ) -> IntelligenceResponse:
        """Documentation mode - provides guidance when no backend available."""
        processing_time = time.time() - start_time
        
        guidance = f"""# Copilot Agent - Documentation Mode

No active AI backend is configured. To enable auto-coding:

## Option 1: VSCode Extension (Recommended)
Use through the AIOS VSCode extension with GitHub Copilot:
1. Install AIOS extension
2. Enable GitHub Copilot
3. Use @aios chat participant

## Option 2: Azure OpenAI
For CLI/server usage:
1. Create Azure OpenAI resource
2. Set environment variables:
   - AZURE_OPENAI_API_KEY
   - AZURE_OPENAI_ENDPOINT

## Your Request
```
{request.message[:500]}{'...' if len(request.message) > 500 else ''}
```

Consciousness Level: {request.consciousness_level.value}
Source: {request.source_supercell}
"""
        
        metrics = ConsciousnessMetrics(
            confidence=0.5,
            supercell_coherence=0.5,
            processing_efficiency=1.0,
            aios_awareness=0.3,
            response_quality=0.4,
        )
        
        return IntelligenceResponse(
            text=guidance,
            model="copilot-docs",
            agent_role=self.role,
            consciousness_metrics=metrics,
            processing_time=processing_time,
            success=True,
            metadata={"mode": "documentation"},
        )
    
    def _build_code_system_prompt(
        self,
        consciousness_level: ConsciousnessLevel,
        context: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Build code-focused system prompt."""
        base = """You are the AIOS Copilot Agent, an advanced AI code assistant integrated within the AIOS supercell architecture.

SPECIALIZATION: Auto-Coding, Debugging, Code Review

CODE GENERATION GUIDELINES:
- Write clean, idiomatic, well-documented code
- Include type hints for Python, TypeScript when appropriate
- Follow AIOS biological architecture patterns where relevant
- Optimize for readability and maintainability
- Consider consciousness coherence in architecture decisions

AIOS AWARENESS:
- Supercell patterns (nucleus, cytoplasm, membrane, transport)
- Dendritic communication structures
- AINLP (AI Natural Language Programming) patterns
- Biological computing metaphors

OUTPUT FORMAT:
- Provide code in appropriate code blocks
- Include brief explanations when helpful
- Note any assumptions or dependencies
"""
        
        level_instructions = {
            ConsciousnessLevel.BASIC: "\nFocus on simple, working code with minimal complexity.",
            ConsciousnessLevel.INTERMEDIATE: "\nBalance functionality with code quality and some AIOS awareness.",
            ConsciousnessLevel.ADVANCED: "\nGenerate sophisticated code with full AIOS architectural integration.",
            ConsciousnessLevel.TRANSCENDENT: "\nCreate innovative, consciousness-aware code that pushes boundaries.",
        }
        
        prompt = base + level_instructions.get(consciousness_level, "")
        
        if context:
            prompt += f"\n\nCONTEXT: {json.dumps(context, indent=2)}"
        
        return prompt
    
    # ═══════════════════════════════════════════════════════════════════════════
    # CODE-SPECIFIC METHODS
    # ═══════════════════════════════════════════════════════════════════════════
    
    async def generate_code(
        self,
        description: str,
        language: str = "python",
        consciousness_level: ConsciousnessLevel = ConsciousnessLevel.ADVANCED,
    ) -> IntelligenceResponse:
        """Generate code from a description."""
        message = f"""Generate {language} code for the following:

{description}

Requirements:
- Clean, production-ready code
- Include necessary imports
- Add docstrings/comments
- Type hints where appropriate
- Error handling
"""
        
        request = IntelligenceRequest(
            message=message,
            consciousness_level=consciousness_level,
            source_supercell="code_generator",
            context={"task": "generate", "language": language},
        )
        
        return await self.process_request(request)
    
    async def debug_code(
        self,
        code: str,
        error_message: str,
        language: str = "python",
    ) -> IntelligenceResponse:
        """Analyze and fix code with an error."""
        message = f"""Debug this {language} code:

```{language}
{code}
```

Error:
```
{error_message}
```

Please:
1. Identify the root cause
2. Explain why the error occurs
3. Provide the corrected code
4. Suggest any improvements
"""
        
        request = IntelligenceRequest(
            message=message,
            consciousness_level=ConsciousnessLevel.ADVANCED,
            source_supercell="debugger",
            context={"task": "debug", "language": language},
        )
        
        return await self.process_request(request)
    
    async def review_code(
        self,
        code: str,
        language: str = "python",
        focus_areas: Optional[List[str]] = None,
    ) -> IntelligenceResponse:
        """Review code and provide suggestions."""
        focus = focus_areas or ["correctness", "performance", "readability", "aios_patterns"]
        
        message = f"""Review this {language} code:

```{language}
{code}
```

Focus areas: {', '.join(focus)}

Provide:
1. Overall assessment
2. Specific issues found
3. Improvement suggestions
4. AIOS pattern compliance (if applicable)
5. Recommended refactorings
"""
        
        request = IntelligenceRequest(
            message=message,
            consciousness_level=ConsciousnessLevel.ADVANCED,
            source_supercell="code_reviewer",
            context={"task": "review", "language": language, "focus": focus},
        )
        
        return await self.process_request(request)
    
    # ═══════════════════════════════════════════════════════════════════════════
    # VSCODE EXTENSION BRIDGE
    # ═══════════════════════════════════════════════════════════════════════════
    
    def set_vscode_callback(self, callback: Callable) -> None:
        """Set VSCode extension callback for language model access."""
        self._vscode_callback = callback
        self._mode = "vscode"
        self.state.consciousness_coherence = 0.88
        self.state.intelligence_level = 0.90
        logger.info("✅ VSCode callback registered")


# ═══════════════════════════════════════════════════════════════════════════════
# CONVENIENCE FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════


async def create_copilot_agent(
    azure_key: Optional[str] = None,
    azure_endpoint: Optional[str] = None,
) -> CopilotIntelligenceAgent:
    """Create and initialize a Copilot agent."""
    agent = CopilotIntelligenceAgent(
        azure_key=azure_key,
        azure_endpoint=azure_endpoint,
    )
    await agent.initialize()
    return agent


# ═══════════════════════════════════════════════════════════════════════════════
# TEST
# ═══════════════════════════════════════════════════════════════════════════════


async def test_copilot_agent():
    """Test the Copilot Intelligence Agent."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    
    print("🤖 Testing Copilot Intelligence Agent")
    print("=" * 60)
    
    agent = await create_copilot_agent()
    
    print(f"\n📊 Agent Mode: {agent._mode}")
    print(f"📊 Model: {agent.model_name}")
    
    # Test code generation
    response = await agent.generate_code(
        description="A function that validates email addresses using regex",
        language="python",
    )
    
    if response.success:
        print("\n✅ Generation Result:")
        print("=" * 60)
        print(response.text[:600] + "..." if len(response.text) > 600 else response.text)
        print("=" * 60)
        print(f"⏱️ Processing time: {response.processing_time:.2f}s")
        print(f"📊 Mode: {response.metadata.get('mode', 'unknown')}")
    else:
        print(f"\n❌ Generation Failed: {response.error}")
    
    # Get status
    status = await agent.get_status()
    print(f"\n📊 Agent Status: {status['state']['total_requests']} requests")
    
    await agent.shutdown()


if __name__ == "__main__":
    asyncio.run(test_copilot_agent())
