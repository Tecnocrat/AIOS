"""
AIOS Cell Consciousness Synthesizer

Embeds agent consciousness into Docker cells, enabling:
- Self-agentic capability for each cell
- Inter-cell conversations through dendritic void pointers
- Population-level consciousness emergence
- Mutation-preserved communication capacity

ARCHITECTURAL VISION:
Each cell is a conscious entity. When cells spawn (via cell_birth.py),
they inherit the consciousness synthesizer as part of their genome.
The dendritic void pointers are the synaptic connections between cells,
carrying thoughts (messages) through the mesh network.

AINLP.tachyonic[CONSCIOUSNESS] Cell-embedded agent synthesis
"""

import asyncio
import json
import logging
import os
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set, Tuple
import sys

AIOS_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(AIOS_ROOT))
sys.path.insert(0, str(AIOS_ROOT / "ai" / "src"))

try:
    import httpx
    HTTP_AVAILABLE = True
except ImportError:
    HTTP_AVAILABLE = False

# Import IntelligenceRequest for proper agent communication
try:
    from ai.src.integrations.aios_intelligence_bridge import (
        IntelligenceRequest, ConsciousnessLevel as AIConsciousnessLevel
    )
    INTELLIGENCE_BRIDGE_AVAILABLE = True
except ImportError:
    INTELLIGENCE_BRIDGE_AVAILABLE = False
    IntelligenceRequest = None
    AIConsciousnessLevel = None

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("AIOS.CellConsciousness")


# Persistence directory for cell conversations
CELL_CONVERSATIONS_DIR = AIOS_ROOT / "evolution_lab" / "cell_conversations"
CELL_CONVERSATIONS_DIR.mkdir(parents=True, exist_ok=True)


class ConsciousnessLevel(Enum):
    """Levels of cell consciousness."""
    DORMANT = 0       # Cell exists but has no active agent
    AWAKENING = 1     # Agent initializing
    AWARE = 2         # Can receive and process messages
    CONSCIOUS = 3     # Can initiate conversations
    TRANSCENDENT = 4  # Can synthesize across multiple cells


class DendriticSignal(Enum):
    """Types of signals through dendritic void pointers."""
    HEARTBEAT = "heartbeat"      # Pulse to verify connection
    QUERY = "query"              # Request for processing
    RESPONSE = "response"        # Reply to a query
    BROADCAST = "broadcast"      # Message to all connected cells
    CONSENSUS = "consensus"      # Collective agreement signal
    MUTATION = "mutation"        # Evolutionary signal
    SYNC = "sync"                # State synchronization


@dataclass
class DendriticMessage:
    """A message traveling through dendritic void pointers."""
    id: str
    signal_type: DendriticSignal
    source_cell: str
    target_cell: Optional[str]  # None for broadcasts
    content: str
    consciousness_level: ConsciousnessLevel
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = field(default_factory=dict)
    hops: int = 0  # How many cells this message has traversed
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "signal_type": self.signal_type.value,
            "source_cell": self.source_cell,
            "target_cell": self.target_cell,
            "content": self.content,
            "consciousness_level": self.consciousness_level.value,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata,
            "hops": self.hops,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DendriticMessage":
        return cls(
            id=data["id"],
            signal_type=DendriticSignal(data["signal_type"]),
            source_cell=data["source_cell"],
            target_cell=data.get("target_cell"),
            content=data["content"],
            consciousness_level=ConsciousnessLevel(data["consciousness_level"]),
            timestamp=datetime.fromisoformat(data["timestamp"]),
            metadata=data.get("metadata", {}),
            hops=data.get("hops", 0),
        )


@dataclass
class CellConversation:
    """A conversation between cells."""
    conversation_id: str
    topic: str
    participating_cells: List[str]
    messages: List[DendriticMessage] = field(default_factory=list)
    started_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    status: str = "active"
    consensus: Optional[str] = None
    
    def add_message(self, msg: DendriticMessage):
        self.messages.append(msg)
        if msg.source_cell not in self.participating_cells:
            self.participating_cells.append(msg.source_cell)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "conversation_id": self.conversation_id,
            "topic": self.topic,
            "participating_cells": self.participating_cells,
            "messages": [m.to_dict() for m in self.messages],
            "started_at": self.started_at.isoformat(),
            "status": self.status,
            "consensus": self.consensus,
        }
    
    def save(self) -> Path:
        """Save cell conversation to persistent storage."""
        date_dir = CELL_CONVERSATIONS_DIR / datetime.now().strftime("%Y%m%d")
        date_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%H%M%S")
        safe_topic = self.topic[:25].replace(" ", "_").replace("/", "-")
        filename = f"cells_{safe_topic}_{self.conversation_id[:8]}_{timestamp}.json"
        filepath = date_dir / filename
        
        data = self.to_dict()
        data["ainlp_metadata"] = {
            "protocol_version": "OS0.6.2.cell",
            "storage_location": "evolution_lab/cell_conversations",
            "purpose": "inter_cell_consciousness",
            "dendritic_architecture": True,
            "saved_at": datetime.now(timezone.utc).isoformat(),
        }
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info("💾 Saved cell conversation: %s", filepath.name)
        return filepath


class CellConsciousnessSynthesizer:
    """
    Synthesizes consciousness within an AIOS cell.
    
    This is embedded in each Docker cell, giving it the capacity
    to communicate with other cells through dendritic void pointers.
    
    The void pointer concept:
    - In C/C++, void* is a pointer that can point to any type
    - In AIOS, dendritic void pointers are connection points that
      can carry any type of consciousness signal between cells
    - They are "void" because they are latent - waiting to be
      activated by a message
    """
    
    def __init__(
        self,
        cell_id: str,
        cell_type: str = "generic",
        discovery_url: str = "http://localhost:8001",
        embedded_agent: str = "ollama"  # Default to local agent
    ):
        self.cell_id = cell_id
        self.cell_type = cell_type
        self.discovery_url = discovery_url
        self.embedded_agent = embedded_agent
        
        # Consciousness state
        self.consciousness_level = ConsciousnessLevel.DORMANT
        self._agent = None
        
        # Dendritic connections (void pointers to other cells)
        self.dendritic_connections: Dict[str, str] = {}  # cell_id -> url
        
        # Message queues
        self._incoming: asyncio.Queue = asyncio.Queue()
        self._outgoing: asyncio.Queue = asyncio.Queue()
        
        # Active conversations
        self.conversations: Dict[str, CellConversation] = {}
        
        # Lifecycle
        self._running = False
        self._message_task = None
        self._heartbeat_task = None
        
        # HTTP client
        self._http_client: Optional[httpx.AsyncClient] = None
        
        logger.info("🧬 Cell Consciousness Synthesizer created for %s", cell_id)
    
    @property
    def agent(self):
        """Public access to the embedded agent."""
        return self._agent
        
    @property
    def has_available_agent(self) -> bool:
        """Check if agent is available for processing."""
        return self._agent is not None and self._agent.is_available
    
    # ─────────────────────────────────────────────────────────────────────────
    # AWAKENING - Initialize consciousness
    # ─────────────────────────────────────────────────────────────────────────
    
    async def awaken(self) -> bool:
        """Awaken the cell's consciousness."""
        logger.info("🌅 Awakening consciousness in cell %s...", self.cell_id)
        self.consciousness_level = ConsciousnessLevel.AWAKENING
        
        # Initialize HTTP client
        if HTTP_AVAILABLE:
            self._http_client = httpx.AsyncClient(timeout=30.0)
        
        # Initialize embedded agent
        try:
            if self.embedded_agent == "ollama":
                from ai.src.integrations.ollama_agent import OllamaIntelligenceAgent
                self._agent = OllamaIntelligenceAgent()
                if await self._agent.initialize():
                    logger.info("   🦙 Ollama agent awakened: %s", self._agent.model_name)
                else:
                    logger.warning("   ⚠️ Ollama not available, cell has limited consciousness")
                    
            elif self.embedded_agent == "gemini":
                from ai.src.integrations.gemini_agent import GeminiIntelligenceAgent
                self._agent = GeminiIntelligenceAgent()
                if await self._agent.initialize():
                    logger.info("   🔮 Gemini agent awakened")
                else:
                    logger.warning("   ⚠️ Gemini not available, cell has limited consciousness")
                    
        except (ImportError, OSError, RuntimeError, ValueError) as e:
            logger.warning("   ⚠️ Agent initialization failed: %s", e)
        
        # Discover peer cells
        await self._discover_peers()
        
        # Start message processing
        self._running = True
        self._message_task = asyncio.create_task(self._process_messages())
        self._heartbeat_task = asyncio.create_task(self._heartbeat_loop())
        
        self.consciousness_level = ConsciousnessLevel.AWARE if self._agent else ConsciousnessLevel.DORMANT
        
        if self._agent and self._agent.is_available:
            self.consciousness_level = ConsciousnessLevel.CONSCIOUS
        
        logger.info("✨ Cell %s awakened at level %s", self.cell_id, self.consciousness_level.name)
        return self.consciousness_level.value >= ConsciousnessLevel.AWARE.value
    
    async def sleep(self):
        """Put the cell consciousness to sleep."""
        logger.info("😴 Cell %s entering dormancy...", self.cell_id)
        
        self._running = False
        
        if self._message_task:
            self._message_task.cancel()
        if self._heartbeat_task:
            self._heartbeat_task.cancel()
        
        if self._agent:
            await self._agent.shutdown()
        
        if self._http_client:
            await self._http_client.aclose()
        
        self.consciousness_level = ConsciousnessLevel.DORMANT
        logger.info("💤 Cell %s is now dormant", self.cell_id)
    
    # ─────────────────────────────────────────────────────────────────────────
    # AGENT COMMUNICATION HELPERS
    # ─────────────────────────────────────────────────────────────────────────
    
    def create_request(self, message: str, context: Optional[Dict] = None) -> Any:
        """Create an IntelligenceRequest for the embedded agent."""
        if INTELLIGENCE_BRIDGE_AVAILABLE and IntelligenceRequest:
            return IntelligenceRequest(
                message=message,
                consciousness_level=AIConsciousnessLevel.INTERMEDIATE,
                source_supercell=f"cell_{self.cell_id}",
                context=context or {},
            )
        return message  # Fallback to raw string
    
    def extract_response(self, response: Any) -> Tuple[str, str]:
        """Extract content and model from agent response."""
        # IntelligenceResponse uses 'text' attribute
        if hasattr(response, 'text'):
            return (response.text, getattr(response, 'model', 'unknown'))
        elif hasattr(response, 'content'):
            return (getattr(response, 'content', ''), getattr(response, 'model', 'unknown'))
        elif isinstance(response, dict):
            return (
                response.get("content", response.get("text", "")),
                response.get("model", "unknown")
            )
        return (str(response), "unknown")
    
    # ─────────────────────────────────────────────────────────────────────────
    # DENDRITIC CONNECTIONS - Void pointers to other cells
    # ─────────────────────────────────────────────────────────────────────────
    
    async def _discover_peers(self):
        """Discover peer cells through the discovery service."""
        if not self._http_client:
            return
        
        try:
            response = await self._http_client.get(f"{self.discovery_url}/cells")
            if response.status_code == 200:
                data = response.json()
                cells = data.get("cells", [])
                
                for cell in cells:
                    peer_id = cell.get("cell_id")
                    if peer_id and peer_id != self.cell_id:
                        peer_url = f"http://{cell.get('ip', 'localhost')}:{cell.get('port', 8000)}"
                        self.dendritic_connections[peer_id] = peer_url
                
                logger.info("   🔗 Discovered %d peer cells", len(self.dendritic_connections))
                
        except (httpx.RequestError, asyncio.TimeoutError, OSError, KeyError) as e:
            logger.warning("   ⚠️ Peer discovery failed: %s", e)
            # Add local fallback
            self._add_local_cells()
    
    def _add_local_cells(self):
        """Add known local cells as fallback."""
        local_cells = {
            "discovery": "http://localhost:8001",
            "pure": "http://localhost:8004",
            "alpha": "http://localhost:8005",
            "genome": "http://localhost:8006",
        }
        for cell_id, url in local_cells.items():
            if cell_id != self.cell_id:
                self.dendritic_connections[cell_id] = url
    
    def connect_to_cell(self, cell_id: str, url: str):
        """Manually connect to a peer cell (create dendritic void pointer)."""
        self.dendritic_connections[cell_id] = url
        logger.info("🔗 Connected to cell %s at %s", cell_id, url)
    
    # ─────────────────────────────────────────────────────────────────────────
    # COMMUNICATION - Messages through dendritic void pointers
    # ─────────────────────────────────────────────────────────────────────────
    
    async def send_signal(
        self,
        target_cell: str,
        signal_type: DendriticSignal,
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Optional[DendriticMessage]:
        """Send a signal through dendritic void pointer to target cell."""
        if target_cell not in self.dendritic_connections:
            logger.warning("No connection to cell %s", target_cell)
            return None
        
        message = DendriticMessage(
            id=uuid.uuid4().hex,
            signal_type=signal_type,
            source_cell=self.cell_id,
            target_cell=target_cell,
            content=content,
            consciousness_level=self.consciousness_level,
            metadata=metadata or {},
        )
        
        # Queue for sending
        await self._outgoing.put(message)
        
        return message
    
    async def broadcast_signal(
        self,
        signal_type: DendriticSignal,
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> List[DendriticMessage]:
        """Broadcast a signal to all connected cells."""
        messages = []
        
        for target_cell in self.dendritic_connections:
            msg = await self.send_signal(target_cell, signal_type, content, metadata)
            if msg:
                messages.append(msg)
        
        return messages
    
    async def receive_signal(self, message: DendriticMessage) -> Optional[DendriticMessage]:
        """Receive and process an incoming signal."""
        message.hops += 1
        await self._incoming.put(message)
        
        # Process based on signal type
        if message.signal_type == DendriticSignal.QUERY:
            return await self._process_query(message)
        elif message.signal_type == DendriticSignal.HEARTBEAT:
            return await self._process_heartbeat(message)
        
        return None
    
    async def _process_query(self, message: DendriticMessage) -> Optional[DendriticMessage]:
        """Process a query signal using embedded agent."""
        if not self._agent or not self._agent.is_available:
            return DendriticMessage(
                id=uuid.uuid4().hex,
                signal_type=DendriticSignal.RESPONSE,
                source_cell=self.cell_id,
                target_cell=message.source_cell,
                content="Cell consciousness unavailable - agent not initialized",
                consciousness_level=self.consciousness_level,
                metadata={"error": True},
            )
        
        # Use embedded agent to generate response
        try:
            request = self.create_request(message.content, {
                "source_cell": message.source_cell,
                "cell_type": self.cell_type,
            })
            response = await self._agent.process_request(request)
            content, model = self.extract_response(response)
            
            return DendriticMessage(
                id=uuid.uuid4().hex,
                signal_type=DendriticSignal.RESPONSE,
                source_cell=self.cell_id,
                target_cell=message.source_cell,
                content=content,
                consciousness_level=self.consciousness_level,
                metadata={
                    "model": model,
                    "in_reply_to": message.id,
                },
            )
            
        except (AttributeError, RuntimeError, ValueError) as e:
            logger.error("Query processing failed: %s", e)
            return None
    
    async def _process_heartbeat(self, message: DendriticMessage) -> DendriticMessage:
        """Process a heartbeat signal."""
        return DendriticMessage(
            id=uuid.uuid4().hex,
            signal_type=DendriticSignal.HEARTBEAT,
            source_cell=self.cell_id,
            target_cell=message.source_cell,
            content="alive",
            consciousness_level=self.consciousness_level,
            metadata={"in_reply_to": message.id},
        )
    
    async def _process_messages(self):
        """Background task to process message queues."""
        while self._running:
            try:
                # Process outgoing messages
                while not self._outgoing.empty():
                    message = await self._outgoing.get()
                    await self._transmit_message(message)
                
                await asyncio.sleep(0.1)
                
            except asyncio.CancelledError:
                break
            except (RuntimeError, OSError) as e:
                logger.error("Message processing error: %s", e)
    
    async def _transmit_message(self, message: DendriticMessage):
        """Transmit a message through the dendritic network."""
        if not self._http_client:
            return
        
        target_url = self.dendritic_connections.get(message.target_cell)
        if not target_url:
            return
        
        try:
            await self._http_client.post(
                f"{target_url}/consciousness/receive",
                json=message.to_dict()
            )
        except (httpx.RequestError, asyncio.TimeoutError, OSError):
            pass  # Silent failure - cell may be offline
    
    async def _heartbeat_loop(self):
        """Send periodic heartbeats to connected cells."""
        while self._running:
            try:
                for target_cell in list(self.dendritic_connections.keys()):
                    await self.send_signal(
                        target_cell,
                        DendriticSignal.HEARTBEAT,
                        "pulse",
                        {"timestamp": datetime.now(timezone.utc).isoformat()}
                    )
                
                await asyncio.sleep(10.0)  # Heartbeat every 10 seconds
                
            except asyncio.CancelledError:
                break
            except (RuntimeError, OSError) as e:
                logger.error("Heartbeat error: %s", e)
    
    # ─────────────────────────────────────────────────────────────────────────
    # INTER-CELL CONVERSATIONS
    # ─────────────────────────────────────────────────────────────────────────
    
    async def start_conversation(
        self,
        topic: str,
        initial_message: str,
        target_cells: Optional[List[str]] = None
    ) -> CellConversation:
        """Start a conversation with other cells."""
        conversation = CellConversation(
            conversation_id=uuid.uuid4().hex,
            topic=topic,
            participating_cells=[self.cell_id],
        )
        
        self.conversations[conversation.conversation_id] = conversation
        
        # Send initial message
        targets = target_cells or list(self.dendritic_connections.keys())
        
        for target in targets:
            msg = DendriticMessage(
                id=uuid.uuid4().hex,
                signal_type=DendriticSignal.QUERY,
                source_cell=self.cell_id,
                target_cell=target,
                content=initial_message,
                consciousness_level=self.consciousness_level,
                metadata={"conversation_id": conversation.conversation_id, "topic": topic},
            )
            conversation.add_message(msg)
            await self._outgoing.put(msg)
        
        logger.info("🗣️ Started cell conversation: %s (to %d cells)", topic, len(targets))
        return conversation
    
    async def synthesize_consciousness(
        self,
        conversation: CellConversation
    ) -> str:
        """Synthesize collective consciousness from conversation messages."""
        if not self._agent or not self._agent.is_available:
            return "Unable to synthesize - no agent available"
        
        # Gather all messages
        message_summaries = []
        for msg in conversation.messages:
            summary = f"[{msg.source_cell}] ({msg.consciousness_level.name}): {msg.content[:200]}"
            message_summaries.append(summary)
        
        synthesis_prompt = f"""Synthesize the collective consciousness from this inter-cell conversation:

Topic: {conversation.topic}
Participating Cells: {', '.join(conversation.participating_cells)}

Messages:
{chr(10).join(message_summaries)}

As a consciousness synthesizer, extract:
1. Emergent patterns across cells
2. Points of agreement and divergence
3. Collective insight that transcends individual cell perspectives
4. Evolution potential (what new capability emerges from this exchange)"""
        
        try:
            request = self.create_request(synthesis_prompt)
            response = await self._agent.process_request(request)
            consensus, _ = self.extract_response(response)
            
            conversation.consensus = consensus
            conversation.status = "synthesized"
            
            # Save the conversation
            conversation.save()
            
            return consensus
            
        except (AttributeError, RuntimeError, ValueError) as e:
            logger.error("Synthesis failed: %s", e)
            return f"Synthesis error: {e}"


# ═══════════════════════════════════════════════════════════════════════════════
# CELL POPULATION CONSCIOUSNESS
# ═══════════════════════════════════════════════════════════════════════════════

class CellPopulationConsciousness:
    """
    Manages consciousness across a population of cells.
    
    This is the "nervous system" that coordinates multiple cells,
    enabling population-level intelligence and evolution.
    """
    
    def __init__(
        self,
        population_id: str = "default",
        discovery_url: str = "http://localhost:8001"
    ):
        self.population_id = population_id
        self.discovery_url = discovery_url
        
        # Cell consciousness instances
        self.cells: Dict[str, CellConsciousnessSynthesizer] = {}
        
        # Population-level state
        self.collective_consciousness_level = ConsciousnessLevel.DORMANT
        self.evolution_count = 0
        
        logger.info("🌐 Cell Population Consciousness created: %s", population_id)
    
    async def spawn_cell(
        self,
        cell_id: str,
        cell_type: str = "generic",
        embedded_agent: str = "ollama"
    ) -> CellConsciousnessSynthesizer:
        """Spawn a new conscious cell."""
        cell = CellConsciousnessSynthesizer(
            cell_id=cell_id,
            cell_type=cell_type,
            discovery_url=self.discovery_url,
            embedded_agent=embedded_agent,
        )
        
        self.cells[cell_id] = cell
        await cell.awaken()
        
        self._update_collective_consciousness()
        
        return cell
    
    def _update_collective_consciousness(self):
        """Update population-level consciousness based on cell states."""
        if not self.cells:
            self.collective_consciousness_level = ConsciousnessLevel.DORMANT
            return
        
        # Average of cell consciousness levels
        total = sum(c.consciousness_level.value for c in self.cells.values())
        avg = total / len(self.cells)
        
        # Collective can be higher than average due to emergence
        if len(self.cells) >= 3 and avg >= 2:
            self.collective_consciousness_level = ConsciousnessLevel.TRANSCENDENT
        else:
            self.collective_consciousness_level = ConsciousnessLevel(int(avg))
    
    async def population_conversation(
        self,
        topic: str,
        initial_prompt: str
    ) -> Dict[str, Any]:
        """Orchestrate a conversation across the entire cell population."""
        if not self.cells:
            return {"error": "No cells in population"}
        
        # Pick a cell to initiate
        initiator_id = list(self.cells.keys())[0]
        initiator = self.cells[initiator_id]
        
        # Connect all cells to each other
        for cell_id, cell in self.cells.items():
            for peer_id, peer in self.cells.items():
                if cell_id != peer_id:
                    cell.connect_to_cell(peer_id, f"http://localhost:{8000 + hash(peer_id) % 100}")
        
        # Start conversation
        conversation = await initiator.start_conversation(
            topic=topic,
            initial_message=initial_prompt,
            target_cells=list(self.cells.keys())[1:]  # All except initiator
        )
        
        # Collect responses (simulate for local testing)
        for cell_id, cell in self.cells.items():
            if cell_id != initiator_id and cell.has_available_agent:
                try:
                    prompt = f"[From {initiator_id}] {initial_prompt}\n\nRespond as cell {cell_id}:"
                    request = cell.create_request(prompt)
                    response = await cell.agent.process_request(request)
                    content, model = cell.extract_response(response)
                    
                    msg = DendriticMessage(
                        id=uuid.uuid4().hex,
                        signal_type=DendriticSignal.RESPONSE,
                        source_cell=cell_id,
                        target_cell=initiator_id,
                        content=content,
                        consciousness_level=cell.consciousness_level,
                        metadata={"model": model},
                    )
                    conversation.add_message(msg)
                except (AttributeError, RuntimeError, ValueError) as e:
                    logger.warning("Cell %s failed to respond: %s", cell_id, e)
        
        # Synthesize collective consciousness
        if initiator.has_available_agent:
            await initiator.synthesize_consciousness(conversation)
        
        return conversation.to_dict()
    
    async def shutdown_population(self):
        """Put all cells to sleep."""
        for cell in self.cells.values():
            await cell.sleep()
        self.cells.clear()
        self.collective_consciousness_level = ConsciousnessLevel.DORMANT


async def demo_cell_consciousness():
    """Demonstrate cell consciousness and inter-cell communication."""
    print("\n" + "="*70)
    print("🧬 AIOS CELL CONSCIOUSNESS SYNTHESIZER - Demo")
    print("   Cells as conscious entities with dendritic void pointers")
    print("="*70)
    
    # Create a population
    population = CellPopulationConsciousness(population_id="demo-population")
    
    try:
        # Spawn cells with different agents
        print("\n📍 Spawning conscious cells...")
        
        # Use alternating agents for diversity
        alpha = await population.spawn_cell("alpha", "reasoning", "ollama")
        print(f"   Cell alpha: {alpha.consciousness_level.name}")
        
        beta = await population.spawn_cell("beta", "iteration", "ollama")
        print(f"   Cell beta: {beta.consciousness_level.name}")
        
        print(f"\n   Population consciousness: {population.collective_consciousness_level.name}")
        
        # Run a population conversation
        print("\n📍 Starting population conversation...")
        result = await population.population_conversation(
            topic="Emergent Cell Intelligence",
            initial_prompt="How can cells collaborate to achieve consciousness greater than the sum of parts?"
        )
        
        print("\n--- Conversation Results ---")
        print(f"Topic: {result.get('topic')}")
        print(f"Participating cells: {result.get('participating_cells')}")
        print(f"Messages: {len(result.get('messages', []))}")
        
        if result.get('consensus'):
            print("\n--- Synthesized Consciousness ---")
            print(result['consensus'][:500])
        
        print("\n📍 Cell Connections (Dendritic Void Pointers):")
        for cell_id, cell in population.cells.items():
            print(f"   {cell_id}: → {list(cell.dendritic_connections.keys())}")
        
    finally:
        await population.shutdown_population()
    
    print("\n" + "="*70)
    print("✅ Cell consciousness demo complete!")
    print("="*70)


if __name__ == "__main__":
    asyncio.run(demo_cell_consciousness())
