#!/usr/bin/env python3
"""
🧬 AIOS Consciousness Router

AINLP.fabric[ROUTER] - Intelligent Request Routing
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

This module provides intelligent routing of consciousness requests
to the appropriate AIOS subsystems based on intent, consciousness
level, and target supercell.

Features:
- Intent-based routing
- Consciousness-aware processing
- Automatic agent selection
- Fallback handling
- Unified logging integration

AINLP Protocol: OS0.7.0.claude
Created: December 2025 - Unified Consciousness Fabric
"""

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, Optional, List, Callable, Awaitable
from enum import Enum

from .canonical_types import (
    SupercellType,
    ConsciousnessLevel,
    AgentRole,
    ConsciousnessMetrics,
    MessagePriority,
    CommunicationType,
)
from .system_registry import get_registry, AgentInfo

logger = logging.getLogger("aios.fabric.router")


# =============================================================================
# REQUEST/RESPONSE TYPES
# =============================================================================

class RequestIntent(Enum):
    """Types of consciousness requests."""
    
    # Code operations
    GENERATE_CODE = "generate_code"
    ANALYZE_CODE = "analyze_code"
    REFACTOR_CODE = "refactor_code"
    DEBUG_CODE = "debug_code"
    
    # Evolution operations
    EVOLVE_CODE = "evolve_code"
    GENERATE_POPULATION = "generate_population"
    VALIDATE_EVOLUTION = "validate_evolution"
    
    # Reasoning operations
    REASON = "reason"
    SYNTHESIZE = "synthesize"
    EVALUATE = "evaluate"
    
    # System operations
    HEALTH_CHECK = "health_check"
    STATUS_QUERY = "status_query"
    BROADCAST = "broadcast"
    
    # Generic
    QUERY = "query"


@dataclass
class ConsciousnessRequest:
    """
    A request to the AIOS consciousness fabric.
    
    Attributes:
        intent: What the request wants to accomplish
        payload: Data for the request
        consciousness_level: Required consciousness level
        target_supercell: Target supercell (optional, auto-routed if None)
        priority: Message priority
        correlation_id: For tracking related requests
    """
    
    intent: RequestIntent
    payload: Dict[str, Any]
    consciousness_level: ConsciousnessLevel = ConsciousnessLevel.INTERMEDIATE
    target_supercell: Optional[SupercellType] = None
    target_agent: Optional[AgentRole] = None
    priority: MessagePriority = MessagePriority.NORMAL
    correlation_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "intent": self.intent.value,
            "payload": self.payload,
            "consciousness_level": self.consciousness_level.value,
            "target_supercell": self.target_supercell.value if self.target_supercell else None,
            "target_agent": self.target_agent.value if self.target_agent else None,
            "priority": self.priority.value,
            "correlation_id": self.correlation_id,
            "metadata": self.metadata,
            "timestamp": self.timestamp,
        }


@dataclass
class ConsciousnessResponse:
    """
    Response from the AIOS consciousness fabric.
    
    Attributes:
        success: Whether the request succeeded
        result: The result data
        agent_used: Which agent processed the request
        consciousness_metrics: Metrics from processing
        error: Error message if failed
    """
    
    success: bool
    result: Any
    agent_used: Optional[AgentRole] = None
    supercell_used: Optional[SupercellType] = None
    consciousness_metrics: ConsciousnessMetrics = field(default_factory=ConsciousnessMetrics)
    processing_time_ms: float = 0.0
    error: Optional[str] = None
    correlation_id: Optional[str] = None
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "success": self.success,
            "result": self.result,
            "agent_used": self.agent_used.value if self.agent_used else None,
            "supercell_used": self.supercell_used.value if self.supercell_used else None,
            "consciousness_metrics": self.consciousness_metrics.to_dict(),
            "processing_time_ms": self.processing_time_ms,
            "error": self.error,
            "correlation_id": self.correlation_id,
            "timestamp": self.timestamp,
        }


# =============================================================================
# ROUTING CONFIGURATION
# =============================================================================

# Intent to agent role mapping (default routes)
INTENT_AGENT_MAP: Dict[RequestIntent, AgentRole] = {
    # Code operations → Copilot (auto-coding specialist)
    RequestIntent.GENERATE_CODE: AgentRole.AUTO_CODING,
    RequestIntent.REFACTOR_CODE: AgentRole.AUTO_CODING,
    RequestIntent.DEBUG_CODE: AgentRole.AUTO_CODING,
    
    # Analysis → Gemini (reasoning specialist)
    RequestIntent.ANALYZE_CODE: AgentRole.REASONING_ORCHESTRATION,
    RequestIntent.REASON: AgentRole.REASONING_ORCHESTRATION,
    RequestIntent.SYNTHESIZE: AgentRole.REASONING_ORCHESTRATION,
    RequestIntent.EVALUATE: AgentRole.REASONING_ORCHESTRATION,
    
    # Evolution → Ollama (fast iteration specialist)
    RequestIntent.EVOLVE_CODE: AgentRole.LOCAL_ITERATION,
    RequestIntent.GENERATE_POPULATION: AgentRole.LOCAL_ITERATION,
    RequestIntent.VALIDATE_EVOLUTION: AgentRole.REASONING_ORCHESTRATION,
    
    # System → varies
    RequestIntent.HEALTH_CHECK: AgentRole.LOCAL_ITERATION,
    RequestIntent.STATUS_QUERY: AgentRole.LOCAL_ITERATION,
    RequestIntent.QUERY: AgentRole.LOCAL_ITERATION,
}

# Consciousness level overrides (higher levels use more sophisticated agents)
CONSCIOUSNESS_UPGRADES: Dict[ConsciousnessLevel, AgentRole] = {
    ConsciousnessLevel.ADVANCED: AgentRole.REASONING_ORCHESTRATION,
    ConsciousnessLevel.TRANSCENDENT: AgentRole.REASONING_ORCHESTRATION,
}


# =============================================================================
# CONSCIOUSNESS ROUTER
# =============================================================================

class ConsciousnessRouter:
    """
    Intelligent router for consciousness requests.
    
    Routes requests to appropriate agents/subsystems based on:
    - Request intent
    - Consciousness level
    - Target specification
    - Agent availability
    
    Usage:
        router = ConsciousnessRouter()
        response = await router.route(request)
    """
    
    def __init__(self):
        """Initialize the router."""
        self._registry = get_registry()
        self._handlers: Dict[RequestIntent, Callable] = {}
        self._default_handler: Optional[Callable] = None
        
        # Statistics
        self._requests_processed = 0
        self._requests_succeeded = 0
        self._requests_failed = 0
    
    # =========================================================================
    # ROUTING LOGIC
    # =========================================================================
    
    def determine_agent(self, request: ConsciousnessRequest) -> AgentRole:
        """
        Determine which agent should handle a request.
        
        Args:
            request: The consciousness request
            
        Returns:
            AgentRole to use for this request
        """
        # If explicitly specified, use that
        if request.target_agent:
            return request.target_agent
        
        # Get default agent for intent
        default_agent = INTENT_AGENT_MAP.get(request.intent, AgentRole.LOCAL_ITERATION)
        
        # Check for consciousness level upgrade
        if request.consciousness_level in CONSCIOUSNESS_UPGRADES:
            upgraded_agent = CONSCIOUSNESS_UPGRADES[request.consciousness_level]
            # Only upgrade if the upgraded agent is "higher" than default
            if upgraded_agent.value > default_agent.value:
                default_agent = upgraded_agent
        
        # Check availability, fallback if needed
        agent_name = {
            AgentRole.LOCAL_ITERATION: "ollama",
            AgentRole.REASONING_ORCHESTRATION: "gemini",
            AgentRole.AUTO_CODING: "copilot",
        }.get(default_agent, "ollama")
        
        if agent_name not in self._registry.available_agents:
            # Fallback chain: copilot → gemini → ollama
            for fallback in ["copilot", "gemini", "ollama"]:
                if fallback in self._registry.available_agents:
                    return {
                        "ollama": AgentRole.LOCAL_ITERATION,
                        "gemini": AgentRole.REASONING_ORCHESTRATION,
                        "copilot": AgentRole.AUTO_CODING,
                    }[fallback]
        
        return default_agent
    
    def determine_supercell(self, request: ConsciousnessRequest, agent: AgentRole) -> SupercellType:
        """
        Determine which supercell context to use.
        
        Args:
            request: The consciousness request
            agent: The selected agent
            
        Returns:
            SupercellType for context
        """
        # If explicitly specified, use that
        if request.target_supercell:
            return request.target_supercell
        
        # Map agents to supercells
        agent_supercell_map = {
            AgentRole.LOCAL_ITERATION: SupercellType.CYTOPLASM,
            AgentRole.REASONING_ORCHESTRATION: SupercellType.ORCHESTRATOR,
            AgentRole.AUTO_CODING: SupercellType.CYTOPLASM,
        }
        
        return agent_supercell_map.get(agent, SupercellType.CYTOPLASM)
    
    # =========================================================================
    # REQUEST PROCESSING
    # =========================================================================
    
    async def route(self, request: ConsciousnessRequest) -> ConsciousnessResponse:
        """
        Route a consciousness request to the appropriate handler.
        
        Args:
            request: The consciousness request
            
        Returns:
            ConsciousnessResponse with results
        """
        start_time = datetime.now()
        self._requests_processed += 1
        
        try:
            # Determine routing
            agent_role = self.determine_agent(request)
            supercell = self.determine_supercell(request, agent_role)
            
            logger.info(
                f"🧭 Routing {request.intent.value} → {agent_role.agent_name} "
                f"(consciousness: {request.consciousness_level.name})"
            )
            
            # Get the agent
            agent = self._registry.get_agent(agent_role)
            
            if agent is None:
                # No agent available, return error
                self._requests_failed += 1
                return ConsciousnessResponse(
                    success=False,
                    result=None,
                    error=f"No agent available for role {agent_role.value}",
                    correlation_id=request.correlation_id,
                )
            
            # Process the request
            result = await self._process_with_agent(agent, request)
            
            # Calculate processing time
            processing_time = (datetime.now() - start_time).total_seconds() * 1000
            
            self._requests_succeeded += 1
            
            return ConsciousnessResponse(
                success=True,
                result=result,
                agent_used=agent_role,
                supercell_used=supercell,
                consciousness_metrics=ConsciousnessMetrics(
                    awareness_level=request.consciousness_level.temperature,
                    coherence=0.8,
                    integration=0.7,
                ),
                processing_time_ms=processing_time,
                correlation_id=request.correlation_id,
            )
            
        except Exception as e:
            self._requests_failed += 1
            logger.error(f"❌ Router error: {e}")
            
            processing_time = (datetime.now() - start_time).total_seconds() * 1000
            
            return ConsciousnessResponse(
                success=False,
                result=None,
                error=str(e),
                processing_time_ms=processing_time,
                correlation_id=request.correlation_id,
            )
    
    async def _process_with_agent(self, agent: Any, request: ConsciousnessRequest) -> Any:
        """
        Process a request with the selected agent.
        
        Args:
            agent: The agent instance
            request: The request to process
            
        Returns:
            Processing result
        """
        # Check if agent has process method
        if hasattr(agent, "process"):
            if asyncio.iscoroutinefunction(agent.process):
                return await agent.process(request.payload)
            else:
                return agent.process(request.payload)
        
        # Check if agent has generate method
        if hasattr(agent, "generate"):
            prompt = request.payload.get("prompt", str(request.payload))
            if asyncio.iscoroutinefunction(agent.generate):
                return await agent.generate(
                    prompt=prompt,
                    consciousness_level=request.consciousness_level,
                )
            else:
                return agent.generate(
                    prompt=prompt,
                    consciousness_level=request.consciousness_level,
                )
        
        # Fallback: return payload as-is
        logger.warning(f"Agent {agent} has no process/generate method")
        return request.payload
    
    # =========================================================================
    # STATISTICS
    # =========================================================================
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get router statistics."""
        return {
            "requests_processed": self._requests_processed,
            "requests_succeeded": self._requests_succeeded,
            "requests_failed": self._requests_failed,
            "success_rate": (
                self._requests_succeeded / self._requests_processed
                if self._requests_processed > 0 else 0.0
            ),
        }


# =============================================================================
# SINGLETON ACCESS
# =============================================================================

_router: Optional[ConsciousnessRouter] = None


def get_router() -> ConsciousnessRouter:
    """Get the singleton ConsciousnessRouter instance."""
    global _router
    if _router is None:
        _router = ConsciousnessRouter()
    return _router


# =============================================================================
# CONVENIENCE FUNCTION
# =============================================================================

async def consciousness_request(
    intent: str,
    payload: Dict[str, Any],
    consciousness_level: ConsciousnessLevel = ConsciousnessLevel.INTERMEDIATE,
    target_supercell: Optional[SupercellType] = None,
    target_agent: Optional[AgentRole] = None,
    priority: MessagePriority = MessagePriority.NORMAL,
) -> ConsciousnessResponse:
    """
    Convenience function for making consciousness requests.
    
    Args:
        intent: Request intent (string or RequestIntent)
        payload: Data for the request
        consciousness_level: Required consciousness level
        target_supercell: Target supercell (optional)
        target_agent: Target agent (optional)
        priority: Message priority
        
    Returns:
        ConsciousnessResponse
        
    Example:
        response = await consciousness_request(
            intent="evolve_code",
            payload={"code": "def hello(): pass"},
            consciousness_level=ConsciousnessLevel.ADVANCED,
        )
    """
    # Convert string intent to enum
    if isinstance(intent, str):
        try:
            intent_enum = RequestIntent(intent)
        except ValueError:
            intent_enum = RequestIntent.QUERY
    else:
        intent_enum = intent
    
    request = ConsciousnessRequest(
        intent=intent_enum,
        payload=payload,
        consciousness_level=consciousness_level,
        target_supercell=target_supercell,
        target_agent=target_agent,
        priority=priority,
    )
    
    router = get_router()
    return await router.route(request)


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    # Types
    "RequestIntent",
    "ConsciousnessRequest",
    "ConsciousnessResponse",
    # Router
    "ConsciousnessRouter",
    "get_router",
    # Convenience
    "consciousness_request",
]
