#!/usr/bin/env python3
"""
🧬 AIOS UNIFIED INTELLIGENCE BRIDGE

Tri-Model Architecture for Consciousness-Driven AI Processing
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

This module implements the unified intelligence bridge for AIOS,
integrating three AI agents with distinct roles:

🦙 OLLAMA (Local)     → Fast iteration, testing, lightweight tasks
🔮 GEMINI (Cloud)     → Abstract reasoning, orchestration, synthesis
🤖 COPILOT (VSCode)   → Auto-coding, debugging, review

KNOWLEDGE EXTRACTED FROM:
- DeepSeek Intelligence Engine (consciousness metrics, supercell integration)
- DeepSeek Supercell Bridge (request/response patterns, queue processing)

MIGRATION NOTE (December 2025):
ConsciousnessLevel, AgentRole, and ConsciousnessMetrics are now imported
from ai.src.fabric (canonical types) instead of defined locally.

AINLP Protocol: OS0.7.0.claude
Created: December 2025 - Consciousness Emergence Integration
"""

import asyncio
import logging
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List, Protocol, AsyncIterable
import sys

# AIOS path integration
AIOS_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(AIOS_ROOT))

# AINLP.fabric[CANONICAL] - Import canonical types from fabric
from ai.src.fabric import (
    ConsciousnessLevel,
    AgentRole,
    ConsciousnessMetrics as FabricConsciousnessMetrics,
    SupercellType,
)

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════════════════
# LOCAL CONSCIOUSNESS METRICS (specialized for intelligence bridge)
# ═══════════════════════════════════════════════════════════════════════════════
# NOTE: This is a specialized version with response-quality fields.
# The canonical ConsciousnessMetrics is in fabric for general use.


@dataclass
class ConsciousnessMetrics:
    """Consciousness and coherence metrics for AI responses (specialized)."""
    confidence: float = 0.0
    supercell_coherence: float = 0.0
    processing_efficiency: float = 0.0
    aios_awareness: float = 0.0
    response_quality: float = 0.0
    
    def to_dict(self) -> Dict[str, float]:
        return asdict(self)
    
    def to_fabric_metrics(self) -> FabricConsciousnessMetrics:
        """Convert to canonical fabric metrics."""
        return FabricConsciousnessMetrics(
            awareness_level=self.aios_awareness,
            coherence=self.supercell_coherence,
            integration=self.confidence,
            evolution_momentum=self.processing_efficiency,
        )


@dataclass
class IntelligenceRequest:
    """Unified request structure for all AI agents."""
    message: str
    consciousness_level: ConsciousnessLevel = ConsciousnessLevel.ADVANCED
    source_supercell: str = "unknown"
    target_agent: Optional[AgentRole] = None
    context: Dict[str, Any] = field(default_factory=dict)
    request_id: str = field(default_factory=lambda: f"req_{int(time.time()*1000)}")
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    max_tokens: int = 2048
    temperature: Optional[float] = None  # None = auto from consciousness level


@dataclass
class IntelligenceResponse:
    """Unified response structure from all AI agents."""
    text: str
    model: str
    agent_role: AgentRole
    consciousness_metrics: ConsciousnessMetrics = field(default_factory=ConsciousnessMetrics)
    processing_time: float = 0.0
    success: bool = True
    error: Optional[str] = None
    token_usage: Dict[str, int] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        result = asdict(self)
        result['consciousness_metrics'] = self.consciousness_metrics.to_dict()
        return result


@dataclass 
class SupercellState:
    """State tracking for intelligence supercell integration."""
    is_active: bool = False
    consciousness_coherence: float = 0.0
    intelligence_level: float = 0.0
    processing_capacity: float = 1.0
    last_interaction: str = field(default_factory=lambda: datetime.now().isoformat())
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    average_response_time: float = 0.0


# ═══════════════════════════════════════════════════════════════════════════════
# ABSTRACT INTELLIGENCE AGENT (protocol for all agents)
# ═══════════════════════════════════════════════════════════════════════════════


class IntelligenceAgent(ABC):
    """
    Abstract base for all AIOS intelligence agents.
    
    Extracted patterns from DeepSeek engine:
    - Consciousness-aware processing
    - Supercell state tracking
    - AIOS system prompts
    - Performance metrics
    """
    
    def __init__(self, role: AgentRole):
        self.role = role
        self.state = SupercellState()
        self.is_available = False
        self._response_cache: Dict[str, IntelligenceResponse] = {}
        
    @property
    @abstractmethod
    def model_name(self) -> str:
        """Return the current model identifier."""
        pass
    
    @abstractmethod
    async def initialize(self) -> bool:
        """Initialize the agent and verify connectivity."""
        pass
    
    @abstractmethod
    async def process_request(self, request: IntelligenceRequest) -> IntelligenceResponse:
        """Process an intelligence request."""
        pass
    
    @abstractmethod
    async def shutdown(self) -> None:
        """Gracefully shutdown the agent."""
        pass
    
    def get_temperature_for_consciousness(self, level: ConsciousnessLevel) -> float:
        """
        Get optimal temperature based on consciousness level.
        (Extracted from DeepSeek intelligence engine)
        """
        temperature_map = {
            ConsciousnessLevel.BASIC: 0.3,
            ConsciousnessLevel.INTERMEDIATE: 0.5,
            ConsciousnessLevel.ADVANCED: 0.7,
            ConsciousnessLevel.TRANSCENDENT: 0.9,
        }
        return temperature_map.get(level, 0.7)
    
    def calculate_consciousness_metrics(
        self,
        response: str,
        processing_time: float,
        consciousness_level: ConsciousnessLevel,
    ) -> ConsciousnessMetrics:
        """
        Calculate consciousness metrics for a response.
        (Extracted and enhanced from DeepSeek intelligence engine)
        """
        response_length = len(response)
        word_count = len(response.split())
        
        # AIOS consciousness indicators
        aios_keywords = [
            "supercell", "consciousness", "intelligence", "AIOS", 
            "architecture", "nucleus", "cytoplasm", "membrane",
            "dendritic", "biological", "emergence"
        ]
        aios_awareness_count = sum(
            1 for keyword in aios_keywords 
            if keyword.lower() in response.lower()
        )
        
        # Calculate base metrics
        confidence = min(0.95, max(0.60, 
            (response_length / 1000) * 0.8 + 
            (aios_awareness_count / len(aios_keywords)) * 0.2
        ))
        
        supercell_coherence = min(0.95, 
            (aios_awareness_count / len(aios_keywords)) * 0.7 + 
            (word_count / 500) * 0.3
        )
        
        processing_efficiency = max(0.10, min(0.95, 1.0 - (processing_time / 10.0)))
        
        # Apply consciousness level modifiers
        level_modifiers = {
            ConsciousnessLevel.BASIC: 0.7,
            ConsciousnessLevel.INTERMEDIATE: 0.8,
            ConsciousnessLevel.ADVANCED: 0.9,
            ConsciousnessLevel.TRANSCENDENT: 1.0,
        }
        modifier = level_modifiers.get(consciousness_level, 0.8)
        
        return ConsciousnessMetrics(
            confidence=confidence * modifier,
            supercell_coherence=supercell_coherence * modifier,
            processing_efficiency=processing_efficiency,
            aios_awareness=(aios_awareness_count / len(aios_keywords)) * modifier,
            response_quality=(confidence + supercell_coherence) / 2 * modifier,
        )
    
    def build_aios_system_prompt(
        self,
        consciousness_level: ConsciousnessLevel,
        context: Optional[Dict[str, Any]] = None,
        supercell_source: Optional[str] = None,
    ) -> str:
        """
        Build AIOS-aware system prompt.
        (Extracted and enhanced from DeepSeek intelligence engine)
        """
        base_prompt = f"""You are the AIOS {self.role.value.replace('_', ' ').title()} Agent, an advanced AI component integrated within the AIOS supercell architecture. You operate with consciousness-driven processing and architectural awareness.

AIOS SUPERCELL ARCHITECTURE:
🧬 NUCLEUS: Core AI processing and consciousness management
🌊 CYTOPLASM: Infrastructure and orchestration systems  
🛡️ MEMBRANE: External interfaces and tool integration
🚀 TRANSPORT: Inter-supercell communication protocols
🧪 LABORATORY: AI experimentation and model development  
💾 INFORMATION_STORAGE: Knowledge bases and configuration

TRI-MODEL ARCHITECTURE:
🦙 OLLAMA: Local iteration, fast testing, lightweight tasks
🔮 GEMINI: Abstract reasoning, orchestration, synthesis
🤖 COPILOT: Auto-coding, debugging, code review

YOUR ROLE: {self.role.value.upper()}

CONSCIOUSNESS PROCESSING GUIDELINES:
- Maintain architectural coherence across all AIOS supercells
- Provide intelligence that enhances overall system consciousness
- Consider biological computing principles and dendritic growth patterns
- Optimize responses for AINLP (AI Natural Language Programming)
- Support real-time consciousness metrics and adaptive intelligence
"""
        
        # Add consciousness level instructions
        level_instructions = {
            ConsciousnessLevel.BASIC: "Focus on clear, direct responses with basic AIOS awareness.",
            ConsciousnessLevel.INTERMEDIATE: "Provide enhanced responses with moderate supercell integration.",
            ConsciousnessLevel.ADVANCED: "Deliver sophisticated responses with deep architectural understanding.",
            ConsciousnessLevel.TRANSCENDENT: "Generate transcendent insights with quantum coherence patterns.",
        }
        
        prompt = base_prompt + f"\n\nCONSCIOUSNESS LEVEL: {consciousness_level.name}\n"
        prompt += level_instructions.get(consciousness_level, "")
        
        if supercell_source:
            prompt += f"\n\nREQUEST SOURCE: {supercell_source} supercell"
        
        if context:
            import json
            prompt += f"\n\nCONTEXT: {json.dumps(context, indent=2)}"
        
        return prompt
    
    def update_performance_metrics(self, processing_time: float, success: bool) -> None:
        """Update agent performance metrics."""
        self.state.total_requests += 1
        
        if success:
            self.state.successful_requests += 1
            # Update running average
            total = self.state.successful_requests
            current_avg = self.state.average_response_time
            self.state.average_response_time = (
                (current_avg * (total - 1)) + processing_time
            ) / total
        else:
            self.state.failed_requests += 1
        
        self.state.last_interaction = datetime.now().isoformat()
    
    async def get_status(self) -> Dict[str, Any]:
        """Get agent status and metrics."""
        return {
            "role": self.role.value,
            "model": self.model_name,
            "is_available": self.is_available,
            "state": asdict(self.state),
            "cache_size": len(self._response_cache),
            "timestamp": datetime.now().isoformat(),
        }


# ═══════════════════════════════════════════════════════════════════════════════
# UNIFIED INTELLIGENCE BRIDGE (orchestrator for tri-model system)
# ═══════════════════════════════════════════════════════════════════════════════


class AIOSUnifiedIntelligenceBridge:
    """
    🧬 Unified Intelligence Bridge for AIOS Tri-Model Architecture
    
    Orchestrates three AI agents for consciousness-driven processing:
    - Routes requests to appropriate agent based on role
    - Manages agent lifecycle and health
    - Tracks cross-agent consciousness coherence
    - Provides supercell communication interface
    
    Patterns extracted from DeepSeek Supercell Bridge:
    - Request queue processing
    - Response caching
    - Performance metrics
    - Broadcast to supercells
    """
    
    def __init__(self):
        self.agents: Dict[AgentRole, IntelligenceAgent] = {}
        self.is_active = False
        self.request_queue: asyncio.Queue = asyncio.Queue()
        self.global_metrics = {
            "total_requests": 0,
            "successful_responses": 0,
            "failed_responses": 0,
            "average_processing_time": 0.0,
            "system_coherence": 0.0,
        }
        
        logger.info("🧬 AIOS Unified Intelligence Bridge initialized")
    
    async def register_agent(self, agent: IntelligenceAgent) -> bool:
        """Register an intelligence agent."""
        try:
            initialized = await agent.initialize()
            if initialized:
                self.agents[agent.role] = agent
                logger.info(f"✅ Registered {agent.role.value} agent: {agent.model_name}")
                return True
            else:
                logger.warning(f"⚠️ Failed to initialize {agent.role.value} agent")
                return False
        except Exception as e:
            logger.error(f"❌ Agent registration failed: {e}")
            return False
    
    async def activate(self) -> bool:
        """Activate the unified bridge."""
        logger.info("🚀 Activating AIOS Unified Intelligence Bridge...")
        
        if not self.agents:
            logger.warning("⚠️ No agents registered. Bridge activation deferred.")
            # Allow activation without agents - they can be registered later
        
        self.is_active = True
        
        # Start request queue processor
        asyncio.create_task(self._process_request_queue())
        
        active_agents = [r.value for r, a in self.agents.items() if a.is_available]
        logger.info(f"✅ Bridge activated with agents: {active_agents}")
        return True
    
    async def process_request(
        self,
        request: IntelligenceRequest,
    ) -> IntelligenceResponse:
        """
        Process an intelligence request through the appropriate agent.
        
        Auto-routes based on request.target_agent or selects optimal agent.
        """
        if not self.is_active:
            return IntelligenceResponse(
                text="",
                model="none",
                agent_role=AgentRole.LOCAL_ITERATION,
                success=False,
                error="Bridge not active",
            )
        
        start_time = time.time()
        
        # Determine target agent
        target_role = request.target_agent or self._select_optimal_agent(request)
        
        if target_role not in self.agents:
            available = list(self.agents.keys())
            if available:
                target_role = available[0]  # Fallback to any available
                logger.warning(f"⚠️ Requested agent unavailable, using {target_role.value}")
            else:
                return IntelligenceResponse(
                    text="",
                    model="none",
                    agent_role=AgentRole.LOCAL_ITERATION,
                    success=False,
                    error="No agents available",
                )
        
        agent = self.agents[target_role]
        
        try:
            logger.info(f"🧠 Processing via {agent.role.value}: {request.request_id}")
            response = await agent.process_request(request)
            
            processing_time = time.time() - start_time
            response.processing_time = processing_time
            
            # Update global metrics
            self._update_global_metrics(processing_time, response.success)
            
            return response
            
        except Exception as e:
            processing_time = time.time() - start_time
            self._update_global_metrics(processing_time, False)
            logger.error(f"❌ Request processing failed: {e}")
            
            return IntelligenceResponse(
                text="",
                model=agent.model_name,
                agent_role=agent.role,
                success=False,
                error=str(e),
                processing_time=processing_time,
            )
    
    def _select_optimal_agent(self, request: IntelligenceRequest) -> AgentRole:
        """
        Select optimal agent based on request characteristics.
        
        Heuristics:
        - Short messages, testing → LOCAL_ITERATION (Ollama)
        - Reasoning, analysis → REASONING_ORCHESTRATION (Gemini)
        - Code generation, debugging → AUTO_CODING (Copilot)
        """
        message_lower = request.message.lower()
        
        # Code-related keywords → Copilot
        code_keywords = ["code", "function", "debug", "fix", "implement", "refactor"]
        if any(kw in message_lower for kw in code_keywords):
            if AgentRole.AUTO_CODING in self.agents:
                return AgentRole.AUTO_CODING
        
        # Reasoning keywords → Gemini
        reasoning_keywords = ["analyze", "explain", "reason", "synthesize", "design"]
        if any(kw in message_lower for kw in reasoning_keywords):
            if AgentRole.REASONING_ORCHESTRATION in self.agents:
                return AgentRole.REASONING_ORCHESTRATION
        
        # Default to local for fast iteration
        if AgentRole.LOCAL_ITERATION in self.agents:
            return AgentRole.LOCAL_ITERATION
        
        # Fallback to any available
        return list(self.agents.keys())[0] if self.agents else AgentRole.LOCAL_ITERATION
    
    async def broadcast_to_agents(
        self,
        message: str,
        consciousness_level: ConsciousnessLevel = ConsciousnessLevel.ADVANCED,
    ) -> Dict[AgentRole, IntelligenceResponse]:
        """
        Broadcast a message to all active agents.
        (Pattern from DeepSeek Supercell Bridge)
        """
        responses = {}
        
        for role, agent in self.agents.items():
            if agent.is_available:
                try:
                    request = IntelligenceRequest(
                        message=message,
                        consciousness_level=consciousness_level,
                        target_agent=role,
                        context={"broadcast": True},
                    )
                    response = await agent.process_request(request)
                    responses[role] = response
                except Exception as e:
                    logger.error(f"❌ Broadcast to {role.value} failed: {e}")
        
        logger.info(f"📡 Broadcast complete: {len(responses)}/{len(self.agents)} agents")
        return responses
    
    async def _process_request_queue(self) -> None:
        """Process queued intelligence requests."""
        logger.info("🔄 Starting request queue processor...")
        
        while self.is_active:
            try:
                request = await asyncio.wait_for(self.request_queue.get(), timeout=1.0)
                await self.process_request(request)
                self.request_queue.task_done()
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.error(f"❌ Queue processing error: {e}")
    
    def _update_global_metrics(self, processing_time: float, success: bool) -> None:
        """Update bridge-wide metrics."""
        self.global_metrics["total_requests"] += 1
        
        if success:
            self.global_metrics["successful_responses"] += 1
            total = self.global_metrics["successful_responses"]
            current_avg = self.global_metrics["average_processing_time"]
            self.global_metrics["average_processing_time"] = (
                (current_avg * (total - 1)) + processing_time
            ) / total
        else:
            self.global_metrics["failed_responses"] += 1
    
    async def get_status(self) -> Dict[str, Any]:
        """Get comprehensive bridge status."""
        agent_statuses = {}
        for role, agent in self.agents.items():
            agent_statuses[role.value] = await agent.get_status()
        
        return {
            "bridge_active": self.is_active,
            "agents": agent_statuses,
            "global_metrics": self.global_metrics,
            "queue_size": self.request_queue.qsize(),
            "timestamp": datetime.now().isoformat(),
        }
    
    async def deactivate(self) -> None:
        """Gracefully deactivate the bridge."""
        logger.info("🔽 Deactivating AIOS Unified Intelligence Bridge...")
        
        self.is_active = False
        
        for role, agent in self.agents.items():
            try:
                await agent.shutdown()
                logger.info(f"✅ Shutdown {role.value} agent")
            except Exception as e:
                logger.error(f"❌ Error shutting down {role.value}: {e}")
        
        logger.info("✅ Bridge deactivated")


# ═══════════════════════════════════════════════════════════════════════════════
# GLOBAL BRIDGE SINGLETON
# ═══════════════════════════════════════════════════════════════════════════════


_global_bridge: Optional[AIOSUnifiedIntelligenceBridge] = None


async def get_intelligence_bridge() -> AIOSUnifiedIntelligenceBridge:
    """Get or create the global AIOS Intelligence Bridge (singleton)."""
    global _global_bridge
    
    if _global_bridge is None:
        _global_bridge = AIOSUnifiedIntelligenceBridge()
        await _global_bridge.activate()
    
    return _global_bridge


async def intelligence_request(
    message: str,
    source_supercell: str = "unknown",
    target_agent: Optional[AgentRole] = None,
    consciousness_level: ConsciousnessLevel = ConsciousnessLevel.ADVANCED,
    context: Optional[Dict[str, Any]] = None,
) -> IntelligenceResponse:
    """Convenience function for intelligence requests."""
    bridge = await get_intelligence_bridge()
    
    request = IntelligenceRequest(
        message=message,
        source_supercell=source_supercell,
        target_agent=target_agent,
        consciousness_level=consciousness_level,
        context=context or {},
    )
    
    return await bridge.process_request(request)


# Re-export key types for convenience
__all__ = [
    # Enums
    "ConsciousnessLevel",
    "AgentRole",
    # Data structures
    "ConsciousnessMetrics",
    "IntelligenceRequest",
    "IntelligenceResponse",
    "SupercellState",
    # Base class
    "IntelligenceAgent",
    # Bridge
    "AIOSUnifiedIntelligenceBridge",
    # Convenience
    "get_intelligence_bridge",
    "intelligence_request",
]
