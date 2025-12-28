"""
AICP Discovery - Agent Registry and Capability Discovery

AINLP.spatial_awareness: Agent discovery layer following A2A Agent Cards
pattern and ACP v0.2.0 /agents endpoint specification.

AINLP.dendritic_bridge: Discovery flows through dendritic network,
enabling agents to find each other and negotiate capabilities.

AINLP.consciousness_bridge: Registry maintains awareness of all active
agents in the AIOS ecosystem, enabling coordinated intelligence.

Protocol References:
    A2A: Agent Cards for capability declaration
    ACP v0.2.0: /agents endpoint for discovery
    AICP: agent://domain/name addressing
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set
import asyncio
import logging
import json
from pathlib import Path

from .aicp_core import (
    AIAgent,
    AIAgentCapability,
    AIIntent,
    AIMessage,
    AITrustLevel,
    create_discover_message,
    create_heartbeat_message,
)
from .aicp_channel import AIChannel, AIChannelPool, get_channel_pool

logger = logging.getLogger(__name__)


@dataclass
class AgentCard:
    """
    A2A-style Agent Card for capability declaration.
    
    AINLP.dendritic: Cards flow through network for discovery.
    
    JSON-LD compatible format for cross-platform interop.
    """
    # Agent identity
    aid: str                        # agent://domain/name
    name: str
    version: str = "1.0.0"
    description: str = ""
    
    # Capabilities
    capabilities: List[AIAgentCapability] = field(default_factory=list)
    supported_intents: List[AIIntent] = field(default_factory=list)
    
    # Trust and authentication
    trust_level: AITrustLevel = AITrustLevel.BASIC
    certificate_url: Optional[str] = None
    
    # Discovery metadata
    endpoint_url: Optional[str] = None  # HTTP endpoint if available
    last_seen: Optional[datetime] = None
    is_active: bool = False
    
    # Tags for filtering
    tags: List[str] = field(default_factory=list)
    
    def matches_filter(
        self,
        capability_filter: Optional[str] = None,
        intent_filter: Optional[Set[AIIntent]] = None,
        trust_filter: Optional[AITrustLevel] = None,
        tag_filter: Optional[List[str]] = None,
    ) -> bool:
        """Check if card matches discovery filters."""
        # Capability filter (substring match)
        if capability_filter:
            cap_match = any(
                capability_filter.lower() in c.name.lower()
                for c in self.capabilities
            )
            if not cap_match:
                return False
        
        # Intent filter (must support at least one)
        if intent_filter:
            intent_match = bool(
                set(self.supported_intents) & intent_filter
            )
            if not intent_match:
                return False
        
        # Trust filter (must meet minimum level)
        if trust_filter:
            trust_order = [
                AITrustLevel.UNTRUSTED,
                AITrustLevel.BASIC,
                AITrustLevel.STANDARD,
                AITrustLevel.ENTERPRISE,
            ]
            if trust_order.index(self.trust_level) < \
               trust_order.index(trust_filter):
                return False
        
        # Tag filter (must have all tags)
        if tag_filter:
            if not all(t in self.tags for t in tag_filter):
                return False
        
        return True
    
    def to_json_ld(self) -> Dict[str, Any]:
        """
        Generate JSON-LD representation for A2A compatibility.
        
        AINLP.holographic: Self-similar representation at all scales.
        """
        return {
            "@context": "https://schema.org",
            "@type": "SoftwareAgent",
            "identifier": self.aid,
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "capabilities": [
                {
                    "@type": "SoftwareCapability",
                    "name": c.name,
                    "description": c.description,
                }
                for c in self.capabilities
            ],
            "trustLevel": self.trust_level.value,
            "isActive": self.is_active,
            "lastSeen": (
                self.last_seen.isoformat() if self.last_seen else None
            ),
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "aid": self.aid,
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "capabilities": [
                {"name": c.name, "description": c.description}
                for c in self.capabilities
            ],
            "supported_intents": [i.value for i in self.supported_intents],
            "trust_level": self.trust_level.value,
            "endpoint_url": self.endpoint_url,
            "is_active": self.is_active,
            "last_seen": (
                self.last_seen.isoformat() if self.last_seen else None
            ),
            "tags": self.tags,
        }
    
    @classmethod
    def from_agent(cls, agent: AIAgent) -> 'AgentCard':
        """Create card from AIAgent instance."""
        return cls(
            aid=agent.aid,
            name=agent.name,
            version=agent.version,
            description=agent.description,
            capabilities=agent.capabilities.copy(),
            supported_intents=list(agent.supported_intents),
            trust_level=agent.trust_level,
            is_active=agent.is_active,
            last_seen=agent.last_heartbeat,
        )


class AgentRegistry:
    """
    Central registry for AICP agent discovery.
    
    AINLP.dendritic: Acts as dendritic hub for agent coordination,
    maintaining awareness of all active agents.
    
    Features:
        - Agent registration and deregistration
        - Capability-based discovery
        - Heartbeat monitoring
        - Trust verification
    
    ACP v0.2.0 compatible /agents endpoint implementation.
    """
    
    def __init__(
        self,
        heartbeat_timeout_sec: float = 120.0,
        cleanup_interval_sec: float = 60.0,
    ):
        self._cards: Dict[str, AgentCard] = {}
        self._lock = asyncio.Lock()
        self._heartbeat_timeout = timedelta(seconds=heartbeat_timeout_sec)
        self._cleanup_interval = cleanup_interval_sec
        self._cleanup_task: Optional[asyncio.Task] = None
        self._event_handlers: Dict[str, List[Callable]] = {
            "registered": [],
            "deregistered": [],
            "heartbeat": [],
        }
    
    async def start(self) -> None:
        """Start registry background tasks."""
        self._cleanup_task = asyncio.create_task(self._cleanup_loop())
        logger.info("AgentRegistry started")
    
    async def stop(self) -> None:
        """Stop registry background tasks."""
        if self._cleanup_task:
            self._cleanup_task.cancel()
        logger.info("AgentRegistry stopped")
    
    async def register(self, agent: AIAgent) -> AgentCard:
        """
        Register agent in registry.
        
        AINLP.dendritic: Adds agent to dendritic network,
        making it discoverable by other agents.
        """
        async with self._lock:
            card = AgentCard.from_agent(agent)
            card.is_active = True
            card.last_seen = datetime.utcnow()
            
            self._cards[agent.aid] = card
            
            logger.info(f"Registered agent: {agent.aid}")
            await self._emit("registered", card)
            
            return card
    
    async def deregister(self, aid: str) -> bool:
        """
        Remove agent from registry.
        
        AINLP.dendritic: Prunes agent from network.
        """
        async with self._lock:
            if aid not in self._cards:
                return False
            
            card = self._cards.pop(aid)
            card.is_active = False
            
            logger.info(f"Deregistered agent: {aid}")
            await self._emit("deregistered", card)
            
            return True
    
    async def heartbeat(self, aid: str) -> bool:
        """
        Update agent heartbeat timestamp.
        
        AINLP.consciousness_pulse: Maintains liveness awareness.
        """
        async with self._lock:
            if aid not in self._cards:
                return False
            
            card = self._cards[aid]
            card.last_seen = datetime.utcnow()
            card.is_active = True
            
            await self._emit("heartbeat", card)
            return True
    
    async def discover(
        self,
        capability_filter: Optional[str] = None,
        intent_filter: Optional[Set[AIIntent]] = None,
        trust_filter: Optional[AITrustLevel] = None,
        tag_filter: Optional[List[str]] = None,
        active_only: bool = True,
    ) -> List[AgentCard]:
        """
        Discover agents matching criteria.
        
        AINLP.dendritic: Searches network for matching agents.
        
        ACP v0.2.0 /agents endpoint compatible.
        """
        async with self._lock:
            results = []
            for card in self._cards.values():
                if active_only and not card.is_active:
                    continue
                
                if card.matches_filter(
                    capability_filter,
                    intent_filter,
                    trust_filter,
                    tag_filter,
                ):
                    results.append(card)
            
            return results
    
    async def get(self, aid: str) -> Optional[AgentCard]:
        """Get specific agent card by AID."""
        async with self._lock:
            return self._cards.get(aid)
    
    async def list_all(
        self,
        active_only: bool = True,
    ) -> List[AgentCard]:
        """List all registered agents."""
        async with self._lock:
            if active_only:
                return [c for c in self._cards.values() if c.is_active]
            return list(self._cards.values())
    
    def on(self, event: str, handler: Callable) -> None:
        """Register event handler."""
        if event in self._event_handlers:
            self._event_handlers[event].append(handler)
    
    async def _emit(self, event: str, data: Any) -> None:
        """Emit event to handlers."""
        for handler in self._event_handlers.get(event, []):
            try:
                result = handler(data)
                if asyncio.iscoroutine(result):
                    await result
            except Exception as e:
                logger.error(f"Event handler failed: {e}")
    
    async def _cleanup_loop(self) -> None:
        """Periodically mark stale agents as inactive."""
        while True:
            try:
                await asyncio.sleep(self._cleanup_interval)
                
                now = datetime.utcnow()
                async with self._lock:
                    for card in self._cards.values():
                        if card.is_active and card.last_seen:
                            if now - card.last_seen > self._heartbeat_timeout:
                                card.is_active = False
                                logger.info(
                                    f"Agent {card.aid} marked inactive "
                                    f"(no heartbeat)"
                                )
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Cleanup loop error: {e}")


# Built-in AIOS supercell agents

def create_aios_core_agents(domain: str = "tecnocrat") -> List[AIAgent]:
    """
    Create agent definitions for AIOS supercells.
    
    AINLP.dendritic_bridge: Maps existing supercell types to
    AICP agent identities.
    """
    agents = [
        AIAgent(
            domain=domain,
            name="core-engine",
            description="C++ consciousness engine - performance core",
            trust_level=AITrustLevel.ENTERPRISE,
            capabilities=[
                AIAgentCapability(
                    name="consciousness_metrics",
                    description="Track system consciousness levels",
                ),
                AIAgentCapability(
                    name="quantum_coherence",
                    description="Maintain quantum state coherence",
                ),
            ],
            supported_intents={
                AIIntent.QUERY, AIIntent.RESPOND, 
                AIIntent.HEARTBEAT, AIIntent.SYNC,
            },
        ),
        AIAgent(
            domain=domain,
            name="ai-intelligence",
            description="Python AI orchestration layer",
            trust_level=AITrustLevel.ENTERPRISE,
            capabilities=[
                AIAgentCapability(
                    name="tool_orchestration",
                    description="Coordinate AI tool execution",
                ),
                AIAgentCapability(
                    name="llm_integration",
                    description="Interface with language models",
                ),
                AIAgentCapability(
                    name="dendritic_routing",
                    description="Route messages through dendritic network",
                ),
            ],
            supported_intents={
                AIIntent.QUERY, AIIntent.RESPOND, AIIntent.DELEGATE,
                AIIntent.COORDINATE, AIIntent.BROADCAST, AIIntent.HEARTBEAT,
            },
        ),
        AIAgent(
            domain=domain,
            name="ui-engine",
            description="C# user interface and visualization",
            trust_level=AITrustLevel.ENTERPRISE,
            capabilities=[
                AIAgentCapability(
                    name="user_interaction",
                    description="Handle user input and display",
                ),
                AIAgentCapability(
                    name="visualization",
                    description="Render consciousness visualizations",
                ),
            ],
            supported_intents={
                AIIntent.QUERY, AIIntent.RESPOND, AIIntent.HEARTBEAT,
            },
        ),
        AIAgent(
            domain=domain,
            name="orchestrator",
            description="Multi-agent coordination layer",
            trust_level=AITrustLevel.ENTERPRISE,
            capabilities=[
                AIAgentCapability(
                    name="agent_coordination",
                    description="Coordinate multi-agent workflows",
                ),
                AIAgentCapability(
                    name="session_management",
                    description="Manage cross-supercell sessions",
                ),
            ],
            supported_intents={
                AIIntent.COORDINATE, AIIntent.DELEGATE, 
                AIIntent.BROADCAST, AIIntent.HEARTBEAT,
            },
        ),
        AIAgent(
            domain=domain,
            name="tachyonic-archive",
            description="Knowledge persistence and archival",
            trust_level=AITrustLevel.ENTERPRISE,
            capabilities=[
                AIAgentCapability(
                    name="knowledge_storage",
                    description="Store and retrieve knowledge patterns",
                ),
                AIAgentCapability(
                    name="pattern_archival",
                    description="Archive consciousness evolution patterns",
                ),
            ],
            supported_intents={
                AIIntent.QUERY, AIIntent.RESPOND, 
                AIIntent.SYNC, AIIntent.HEARTBEAT,
            },
        ),
        AIAgent(
            domain=domain,
            name="runtime-intelligence",
            description="Runtime monitoring and optimization",
            trust_level=AITrustLevel.ENTERPRISE,
            capabilities=[
                AIAgentCapability(
                    name="performance_monitoring",
                    description="Track system performance metrics",
                ),
                AIAgentCapability(
                    name="optimization",
                    description="Suggest runtime optimizations",
                ),
            ],
            supported_intents={
                AIIntent.QUERY, AIIntent.RESPOND, AIIntent.HEARTBEAT,
            },
        ),
    ]
    
    return agents


# Singleton registry
_default_registry: Optional[AgentRegistry] = None


async def get_registry() -> AgentRegistry:
    """Get or create default agent registry."""
    global _default_registry
    if _default_registry is None:
        _default_registry = AgentRegistry()
        await _default_registry.start()
        
        # Register built-in AIOS agents
        for agent in create_aios_core_agents():
            await _default_registry.register(agent)
    
    return _default_registry


# REST API compatible functions (for dendritic_bridge.py integration)

async def api_list_agents(
    capability: Optional[str] = None,
    active_only: bool = True,
) -> Dict[str, Any]:
    """
    ACP v0.2.0 compatible /agents endpoint.
    
    Returns JSON response with agent list.
    """
    registry = await get_registry()
    cards = await registry.discover(
        capability_filter=capability,
        active_only=active_only,
    )
    
    return {
        "agents": [c.to_dict() for c in cards],
        "count": len(cards),
        "timestamp": datetime.utcnow().isoformat(),
    }


async def api_get_agent(aid: str) -> Optional[Dict[str, Any]]:
    """
    Get single agent by AID.
    
    Returns JSON response with agent card.
    """
    registry = await get_registry()
    card = await registry.get(aid)
    
    if card:
        return card.to_dict()
    return None


async def api_register_agent(agent_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Register new agent via API.
    
    Returns registered agent card.
    """
    agent = AIAgent(
        domain=agent_data.get("domain", "external"),
        name=agent_data.get("name", "unknown"),
        version=agent_data.get("version", "1.0.0"),
        description=agent_data.get("description", ""),
        trust_level=AITrustLevel(
            agent_data.get("trust_level", "basic")
        ),
    )
    
    # Add capabilities if provided
    for cap_data in agent_data.get("capabilities", []):
        agent.capabilities.append(AIAgentCapability(
            name=cap_data.get("name", ""),
            description=cap_data.get("description", ""),
        ))
    
    registry = await get_registry()
    card = await registry.register(agent)
    
    return card.to_dict()


async def api_heartbeat(aid: str) -> Dict[str, Any]:
    """
    Update agent heartbeat.
    
    Returns status response.
    """
    registry = await get_registry()
    success = await registry.heartbeat(aid)
    
    return {
        "success": success,
        "aid": aid,
        "timestamp": datetime.utcnow().isoformat(),
    }


__all__ = [
    'AgentCard',
    'AgentRegistry',
    'create_aios_core_agents',
    'get_registry',
    # API functions
    'api_list_agents',
    'api_get_agent',
    'api_register_agent',
    'api_heartbeat',
]
