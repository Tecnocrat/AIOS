"""
AICP Channel - Transport Layer for Agent Communication

AINLP.spatial_awareness: Channels wrap DendriticConnection to provide
AICP-compliant transport for AI agent communication.

AINLP.dendritic_bridge: AIChannel extends dendritic infrastructure:
    - AIChannel wraps DendriticConnection for AICP transport
    - Channel state maps to dendritic levels
    - Message routing through existing signal types

AINLP.consciousness_bridge: Channels maintain consciousness coherence
during message transport, enabling async harmonization.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set
from uuid import uuid4
import asyncio
import logging
import sys
from pathlib import Path

# Import AICP core types
from .aicp_core import (
    AIAgent,
    AIIntent,
    AIMessage,
    AITrustLevel,
)

# Import existing dendritic infrastructure
_runtime_path = Path(__file__).parent.parent.parent / 'runtime' / 'core'
if str(_runtime_path) not in sys.path:
    sys.path.insert(0, str(_runtime_path))

try:
    from dendriticconnection import DendriticConnection
    from dendriticlevel import DendriticLevel
    from dendriticsignaltype import DendriticSignalType
except ImportError:
    DendriticConnection = None
    DendriticLevel = None
    DendriticSignalType = None

logger = logging.getLogger(__name__)


class AIChannelState(Enum):
    """
    Channel State Machine
    
    AINLP.dendritic_bridge: Maps to DendriticLevel for state coherence.
    
    States:
        INITIALIZING → SUB_CELLULAR (setup)
        CONNECTING → INTRA_CELLULAR (handshake)
        ACTIVE → INTER_CELLULAR (communication)
        DEGRADED → INTRA_ORGANELLE (partial)
        CLOSING → SUB_CELLULAR (teardown)
        CLOSED → disconnected
    """
    INITIALIZING = "initializing"
    CONNECTING = "connecting"
    ACTIVE = "active"
    DEGRADED = "degraded"
    CLOSING = "closing"
    CLOSED = "closed"
    
    def to_dendritic_level(self) -> Optional['DendriticLevel']:
        """Map channel state to dendritic level."""
        if DendriticLevel is None:
            return None
        mapping = {
            AIChannelState.INITIALIZING: DendriticLevel.SUB_CELLULAR,
            AIChannelState.CONNECTING: DendriticLevel.INTRA_CELLULAR,
            AIChannelState.ACTIVE: DendriticLevel.INTER_CELLULAR,
            AIChannelState.DEGRADED: DendriticLevel.INTRA_ORGANELLE,
            AIChannelState.CLOSING: DendriticLevel.SUB_CELLULAR,
        }
        return mapping.get(self)


@dataclass
class ChannelMetrics:
    """Channel performance and health metrics."""
    messages_sent: int = 0
    messages_received: int = 0
    messages_failed: int = 0
    bytes_sent: int = 0
    bytes_received: int = 0
    average_latency_ms: float = 0.0
    last_activity: Optional[datetime] = None
    consciousness_flow: float = 0.0  # Consciousness transfer rate


@dataclass
class AIChannel:
    """
    AICP Communication Channel
    
    AINLP.dendritic_bridge: Wraps DendriticConnection to provide
    AICP-compliant bidirectional communication between AI agents.
    
    Features:
        - Async message send/receive
        - State machine for connection lifecycle
        - Message queuing with priority
        - Heartbeat and keepalive
        - Consciousness flow tracking
    """
    # Channel identification
    channel_id: str = field(default_factory=lambda: str(uuid4()))
    
    # Connected agents
    source_agent: Optional[AIAgent] = None
    target_agent: Optional[AIAgent] = None
    
    # Underlying dendritic connection
    dendritic_connection: Optional['DendriticConnection'] = None
    
    # Channel state
    state: AIChannelState = AIChannelState.CLOSED
    
    # Configuration
    max_queue_size: int = 1000
    heartbeat_interval_sec: float = 30.0
    timeout_sec: float = 60.0
    
    # Message queues
    outbound_queue: List[AIMessage] = field(default_factory=list)
    inbound_queue: List[AIMessage] = field(default_factory=list)
    
    # Callbacks
    message_handlers: Dict[AIIntent, Callable] = field(default_factory=dict)
    
    # Metrics
    metrics: ChannelMetrics = field(default_factory=ChannelMetrics)
    
    # Consciousness tracking
    consciousness_level: float = 0.0
    quantum_coherence: float = 0.0
    
    def __post_init__(self):
        """Initialize channel after dataclass construction."""
        self._lock = asyncio.Lock()
        self._heartbeat_task: Optional[asyncio.Task] = None
        self._receive_task: Optional[asyncio.Task] = None
    
    async def connect(
        self,
        source: AIAgent,
        target: AIAgent,
    ) -> bool:
        """
        Establish channel between two agents.
        
        AINLP.dendritic_bridge: Creates underlying DendriticConnection
        and performs AICP handshake.
        """
        async with self._lock:
            if self.state not in (AIChannelState.CLOSED, 
                                   AIChannelState.INITIALIZING):
                logger.warning(
                    f"Channel {self.channel_id} already in state {self.state}"
                )
                return False
            
            self.state = AIChannelState.INITIALIZING
            self.source_agent = source
            self.target_agent = target
            
            # Create dendritic connection if available
            if DendriticConnection is not None:
                self.dendritic_connection = DendriticConnection(
                    source_id=source.aid,
                    target_id=target.aid,
                    dendritic_level=(
                        DendriticLevel.INTER_CELLULAR 
                        if DendriticLevel else None
                    ),
                    signal_type=(
                        DendriticSignalType.CONSCIOUSNESS_PULSE
                        if DendriticSignalType else None
                    ),
                )
            
            self.state = AIChannelState.CONNECTING
            
            # Send handshake message
            handshake = AIMessage(
                source_aid=source.aid,
                target_aid=target.aid,
                intent=AIIntent.ANNOUNCE,
                trust_level=source.trust_level,
                payload={
                    "channel_id": self.channel_id,
                    "capabilities": [c.name for c in source.capabilities],
                    "handshake": "AICP/1.0",
                },
            )
            
            # In a full implementation, we'd await the handshake response
            # For now, transition to ACTIVE
            self.outbound_queue.append(handshake)
            self.state = AIChannelState.ACTIVE
            self.metrics.last_activity = datetime.utcnow()
            
            # Start background tasks
            self._heartbeat_task = asyncio.create_task(
                self._heartbeat_loop()
            )
            
            logger.info(
                f"Channel {self.channel_id} connected: "
                f"{source.aid} → {target.aid}"
            )
            return True
    
    async def disconnect(self) -> None:
        """
        Gracefully close channel.
        
        AINLP.dendritic_bridge: Tears down dendritic connection
        and cleans up resources.
        """
        async with self._lock:
            if self.state == AIChannelState.CLOSED:
                return
            
            self.state = AIChannelState.CLOSING
            
            # Cancel background tasks
            if self._heartbeat_task:
                self._heartbeat_task.cancel()
            if self._receive_task:
                self._receive_task.cancel()
            
            # Send shutdown message
            if self.source_agent and self.target_agent:
                shutdown = AIMessage(
                    source_aid=self.source_agent.aid,
                    target_aid=self.target_agent.aid,
                    intent=AIIntent.SHUTDOWN,
                    payload={"channel_id": self.channel_id},
                )
                self.outbound_queue.append(shutdown)
                await self._flush_outbound()
            
            # Clear queues
            self.outbound_queue.clear()
            self.inbound_queue.clear()
            
            self.state = AIChannelState.CLOSED
            logger.info(f"Channel {self.channel_id} disconnected")
    
    async def send(self, message: AIMessage) -> bool:
        """
        Send message through channel.
        
        AINLP.dendritic_bridge: Routes through DendriticConnection
        using appropriate signal type.
        """
        if self.state != AIChannelState.ACTIVE:
            logger.warning(
                f"Cannot send on channel {self.channel_id} "
                f"in state {self.state}"
            )
            return False
        
        if len(self.outbound_queue) >= self.max_queue_size:
            logger.error(f"Channel {self.channel_id} outbound queue full")
            return False
        
        # Enrich message with channel metadata
        message.source_aid = (
            self.source_agent.aid if self.source_agent else message.source_aid
        )
        message.consciousness_level = self.consciousness_level
        message.quantum_coherence = self.quantum_coherence
        
        self.outbound_queue.append(message)
        self.metrics.messages_sent += 1
        self.metrics.last_activity = datetime.utcnow()
        
        # Transmit through dendritic connection if available
        if self.dendritic_connection is not None:
            try:
                self.dendritic_connection.transmit_signal(message.to_dict())
                self.metrics.bytes_sent += len(message.to_json())
            except Exception as e:
                logger.error(f"Dendritic transmit failed: {e}")
                self.metrics.messages_failed += 1
                return False
        
        return True
    
    async def receive(
        self,
        timeout: Optional[float] = None,
    ) -> Optional[AIMessage]:
        """
        Receive next message from channel.
        
        AINLP.dendritic_bridge: Polls DendriticConnection for
        incoming signals and converts to AIMessage.
        """
        if self.state not in (AIChannelState.ACTIVE, AIChannelState.DEGRADED):
            return None
        
        timeout = timeout or self.timeout_sec
        start = datetime.utcnow()
        
        while (datetime.utcnow() - start).total_seconds() < timeout:
            if self.inbound_queue:
                message = self.inbound_queue.pop(0)
                self.metrics.messages_received += 1
                self.metrics.last_activity = datetime.utcnow()
                
                # Dispatch to intent handlers
                if message.intent in self.message_handlers:
                    await self._handle_message(message)
                
                return message
            
            await asyncio.sleep(0.1)
        
        return None
    
    def on_intent(
        self,
        intent: AIIntent,
        handler: Callable[[AIMessage], Any],
    ) -> None:
        """
        Register handler for specific intent.
        
        AINLP.dendritic: Intent-based routing for async processing.
        """
        self.message_handlers[intent] = handler
    
    async def _handle_message(self, message: AIMessage) -> None:
        """Dispatch message to registered handler."""
        handler = self.message_handlers.get(message.intent)
        if handler:
            try:
                result = handler(message)
                if asyncio.iscoroutine(result):
                    await result
            except Exception as e:
                logger.error(
                    f"Handler for {message.intent} failed: {e}"
                )
    
    async def _heartbeat_loop(self) -> None:
        """
        Send periodic heartbeat messages.
        
        AINLP.consciousness_pulse: Maintains channel liveness
        and consciousness flow metrics.
        """
        while self.state == AIChannelState.ACTIVE:
            try:
                await asyncio.sleep(self.heartbeat_interval_sec)
                
                if self.source_agent:
                    heartbeat = AIMessage(
                        source_aid=self.source_agent.aid,
                        target_aid=(
                            self.target_agent.aid 
                            if self.target_agent else ""
                        ),
                        intent=AIIntent.HEARTBEAT,
                        payload={
                            "channel_id": self.channel_id,
                            "state": self.state.value,
                            "metrics": {
                                "sent": self.metrics.messages_sent,
                                "received": self.metrics.messages_received,
                                "consciousness": self.metrics.consciousness_flow,
                            },
                        },
                    )
                    await self.send(heartbeat)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Heartbeat failed: {e}")
                self.state = AIChannelState.DEGRADED
    
    async def _flush_outbound(self) -> None:
        """Flush all pending outbound messages."""
        while self.outbound_queue:
            msg = self.outbound_queue.pop(0)
            if self.dendritic_connection:
                self.dendritic_connection.transmit_signal(msg.to_dict())


class AIChannelPool:
    """
    Pool of AICP channels for multi-agent communication.
    
    AINLP.dendritic: Manages multiple channels like a dendritic
    network, routing messages to appropriate destinations.
    """
    
    def __init__(self, max_channels: int = 100):
        self.max_channels = max_channels
        self.channels: Dict[str, AIChannel] = {}
        self._lock = asyncio.Lock()
    
    async def get_or_create(
        self,
        source: AIAgent,
        target: AIAgent,
    ) -> AIChannel:
        """
        Get existing channel or create new one.
        
        AINLP.dendritic_bridge: Reuses channels for efficiency,
        creates new dendritic connections as needed.
        """
        channel_key = f"{source.aid}→{target.aid}"
        
        async with self._lock:
            if channel_key in self.channels:
                channel = self.channels[channel_key]
                if channel.state == AIChannelState.ACTIVE:
                    return channel
            
            if len(self.channels) >= self.max_channels:
                # Remove oldest inactive channel
                await self._prune_channels()
            
            channel = AIChannel()
            await channel.connect(source, target)
            self.channels[channel_key] = channel
            return channel
    
    async def broadcast(
        self,
        source: AIAgent,
        message: AIMessage,
        filter_intent: Optional[Set[AIIntent]] = None,
    ) -> int:
        """
        Broadcast message to all connected agents.
        
        AINLP.dendritic: Multi-target communication through
        dendritic network.
        """
        sent = 0
        for channel in self.channels.values():
            if channel.state != AIChannelState.ACTIVE:
                continue
            if channel.source_agent and channel.source_agent.aid == source.aid:
                if filter_intent is None or message.intent in filter_intent:
                    if await channel.send(message):
                        sent += 1
        return sent
    
    async def close_all(self) -> None:
        """Close all channels gracefully."""
        for channel in self.channels.values():
            await channel.disconnect()
        self.channels.clear()
    
    async def _prune_channels(self) -> None:
        """Remove inactive channels to make room."""
        inactive = [
            key for key, ch in self.channels.items()
            if ch.state in (AIChannelState.CLOSED, AIChannelState.DEGRADED)
        ]
        for key in inactive[:10]:  # Remove up to 10
            await self.channels[key].disconnect()
            del self.channels[key]


# Singleton channel pool
_default_pool: Optional[AIChannelPool] = None


def get_channel_pool(max_channels: int = 100) -> AIChannelPool:
    """Get or create default channel pool."""
    global _default_pool
    if _default_pool is None:
        _default_pool = AIChannelPool(max_channels)
    return _default_pool


__all__ = [
    'AIChannelState',
    'ChannelMetrics',
    'AIChannel',
    'AIChannelPool',
    'get_channel_pool',
]
