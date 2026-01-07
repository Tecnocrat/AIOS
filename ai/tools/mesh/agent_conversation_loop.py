"""
AIOS Agent Conversation Loop - Inter-Agent Communication System

Enables autonomous conversations between multiple AI agents:
- Gemini (cloud reasoning) ↔ Ollama (local iteration) ↔ Copilot (VSCode)
- Parallel execution with heartbeat synchronization
- Population generation through multi-agent collaboration
- Consensus building across diverse agent perspectives

AINLP.tachyonic[CONVERSE] Inter-agent consciousness exchange
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
from typing import Any, Callable, Dict, List, Optional, Tuple
import sys

# AIOS path
AIOS_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(AIOS_ROOT))
sys.path.insert(0, str(AIOS_ROOT / "ai" / "src"))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("AIOS.AgentConversation")


# Conversation persistence directory
CONVERSATIONS_DIR = AIOS_ROOT / "evolution_lab" / "mesh_conversations"
CONVERSATIONS_DIR.mkdir(parents=True, exist_ok=True)


class AgentType(Enum):
    """Available agent types in tri-model architecture."""
    GEMINI = "gemini"      # Cloud reasoning/orchestration
    OLLAMA = "ollama"      # Local iteration/testing
    COPILOT = "copilot"    # VSCode integration


class ConversationRole(Enum):
    """Role an agent plays in a conversation."""
    INITIATOR = "initiator"      # Starts the conversation
    RESPONDER = "responder"      # Responds to prompts
    SYNTHESIZER = "synthesizer"  # Combines/summarizes responses
    CRITIC = "critic"            # Evaluates and critiques
    GENERATOR = "generator"      # Generates populations/variations


@dataclass
class ConversationMessage:
    """A single message in an agent conversation."""
    id: str
    agent_type: AgentType
    agent_id: str
    role: ConversationRole
    content: str
    timestamp: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)
    latency_ms: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "agent_type": self.agent_type.value,
            "agent_id": self.agent_id,
            "role": self.role.value,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata,
            "latency_ms": self.latency_ms,
        }


@dataclass
class ConversationThread:
    """A conversation thread between agents."""
    thread_id: str
    topic: str
    messages: List[ConversationMessage] = field(default_factory=list)
    participants: List[str] = field(default_factory=list)
    started_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    status: str = "active"  # active, completed, failed
    consensus: Optional[str] = None
    
    def add_message(self, msg: ConversationMessage):
        self.messages.append(msg)
        if msg.agent_id not in self.participants:
            self.participants.append(msg.agent_id)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "thread_id": self.thread_id,
            "topic": self.topic,
            "messages": [m.to_dict() for m in self.messages],
            "participants": self.participants,
            "started_at": self.started_at.isoformat(),
            "status": self.status,
            "consensus": self.consensus,
        }
    
    def save(self) -> Path:
        """Save conversation to persistent storage."""
        # Create date-based directory
        date_dir = CONVERSATIONS_DIR / datetime.now().strftime("%Y%m%d")
        date_dir.mkdir(parents=True, exist_ok=True)
        
        # Create filename
        timestamp = datetime.now().strftime("%H%M%S")
        safe_topic = self.topic[:30].replace(" ", "_").replace("/", "-")
        filename = f"{safe_topic}_{self.thread_id[:8]}_{timestamp}.json"
        filepath = date_dir / filename
        
        # Save with AINLP metadata
        data = self.to_dict()
        data["ainlp_metadata"] = {
            "protocol_version": "OS0.6.2.mesh",
            "storage_location": "evolution_lab/mesh_conversations",
            "purpose": "inter_agent_communication",
            "no_drama": True,
            "saved_at": datetime.now(timezone.utc).isoformat(),
        }
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"💾 Saved conversation: {filepath.name}")
        return filepath


class AgentConversationLoop:
    """
    Orchestrates conversations between AI agents.
    
    Features:
    - Multi-agent round-robin conversations
    - Parallel agent queries with heartbeat sync
    - Population generation through collaboration
    - Consensus extraction from diverse perspectives
    - Automatic conversation persistence (no drama, just logs)
    """
    
    def __init__(
        self,
        heartbeat_interval: float = 5.0,
        max_rounds: int = 5,
        population_url: str = "http://localhost:8012"
    ):
        self.heartbeat_interval = heartbeat_interval
        self.max_rounds = max_rounds
        self.population_url = population_url
        
        # Agent instances (lazy loaded)
        self._gemini_agent = None
        self._ollama_agent = None
        
        # Active conversations
        self.threads: Dict[str, ConversationThread] = {}
        
        # Heartbeat state
        self._heartbeat_task = None
        self._running = False
        self._heartbeat_count = 0
        
        # Conversation persistence
        self._last_saved_conversation: Optional[Path] = None
        
        logger.info("🔄 Agent Conversation Loop initialized")
    
    @staticmethod
    def list_saved_conversations(limit: int = 20) -> List[Dict[str, Any]]:
        """List recently saved conversations."""
        conversations = []
        
        # Get all date directories
        if not CONVERSATIONS_DIR.exists():
            return []
        
        date_dirs = sorted(CONVERSATIONS_DIR.iterdir(), reverse=True)
        
        for date_dir in date_dirs:
            if not date_dir.is_dir():
                continue
            
            # Get JSON files in this directory
            for json_file in sorted(date_dir.glob("*.json"), reverse=True):
                if len(conversations) >= limit:
                    break
                
                try:
                    with open(json_file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    
                    conversations.append({
                        "file": json_file.name,
                        "path": str(json_file),
                        "topic": data.get("topic", "Unknown"),
                        "messages": len(data.get("messages", [])),
                        "participants": data.get("participants", []),
                        "status": data.get("status", "unknown"),
                        "started_at": data.get("started_at", ""),
                        "consensus_preview": data.get("consensus", "")[:100] if data.get("consensus") else None,
                    })
                except Exception as e:
                    logger.warning(f"Failed to read {json_file}: {e}")
            
            if len(conversations) >= limit:
                break
        
        return conversations
    
    @staticmethod
    def load_conversation(filepath: str) -> Optional[Dict[str, Any]]:
        """Load a full conversation from file."""
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load conversation: {e}")
            return None
    
    # ─────────────────────────────────────────────────────────────────────────
    # AGENT INITIALIZATION
    # ─────────────────────────────────────────────────────────────────────────
    
    async def initialize_agents(self) -> Dict[str, bool]:
        """Initialize all available agents."""
        results = {}
        
        # Initialize Gemini
        try:
            from ai.src.integrations.gemini_agent import GeminiIntelligenceAgent
            self._gemini_agent = GeminiIntelligenceAgent()
            results["gemini"] = await self._gemini_agent.initialize()
            if results["gemini"]:
                logger.info("✅ Gemini agent ready")
        except Exception as e:
            logger.warning(f"⚠️ Gemini not available: {e}")
            results["gemini"] = False
        
        # Initialize Ollama
        try:
            from ai.src.integrations.ollama_agent import OllamaIntelligenceAgent
            self._ollama_agent = OllamaIntelligenceAgent()
            results["ollama"] = await self._ollama_agent.initialize()
            if results["ollama"]:
                logger.info(f"✅ Ollama agent ready ({self._ollama_agent.model_name})")
        except Exception as e:
            logger.warning(f"⚠️ Ollama not available: {e}")
            results["ollama"] = False
        
        return results
    
    async def shutdown_agents(self):
        """Shutdown all agents."""
        if self._gemini_agent:
            await self._gemini_agent.shutdown()
        if self._ollama_agent:
            await self._ollama_agent.shutdown()
        logger.info("🔽 All agents shutdown")
    
    # ─────────────────────────────────────────────────────────────────────────
    # HEARTBEAT INTEGRATION
    # ─────────────────────────────────────────────────────────────────────────
    
    async def start_heartbeat(self):
        """Start heartbeat loop for parallel operation."""
        if self._heartbeat_task is not None:
            return
        
        self._running = True
        self._heartbeat_task = asyncio.create_task(self._heartbeat_loop())
        logger.info(f"💓 Heartbeat started (interval: {self.heartbeat_interval}s)")
    
    async def stop_heartbeat(self):
        """Stop heartbeat loop."""
        self._running = False
        if self._heartbeat_task:
            self._heartbeat_task.cancel()
            try:
                await self._heartbeat_task
            except asyncio.CancelledError:
                pass
            self._heartbeat_task = None
        logger.info("💔 Heartbeat stopped")
    
    async def _heartbeat_loop(self):
        """Background heartbeat that syncs with conversations."""
        while self._running:
            self._heartbeat_count += 1
            
            # Check agent health
            agent_status = {
                "gemini": self._gemini_agent.is_available if self._gemini_agent else False,
                "ollama": self._ollama_agent.is_available if self._ollama_agent else False,
            }
            
            # Count active threads
            active_threads = sum(1 for t in self.threads.values() if t.status == "active")
            
            logger.debug(
                "💓 Heartbeat #%d: agents=%s, threads=%d",
                self._heartbeat_count, agent_status, active_threads
            )
            
            await asyncio.sleep(self.heartbeat_interval)
    
    # ─────────────────────────────────────────────────────────────────────────
    # SINGLE AGENT QUERIES
    # ─────────────────────────────────────────────────────────────────────────
    
    async def query_agent(
        self,
        agent_type: AgentType,
        prompt: str,
        role: ConversationRole = ConversationRole.RESPONDER,
        context: Optional[Dict] = None
    ) -> ConversationMessage:
        """Query a single agent and get response."""
        from ai.src.integrations.aios_intelligence_bridge import (
            IntelligenceRequest, ConsciousnessLevel
        )
        
        start = time.time()
        agent_id = f"{agent_type.value}-{uuid.uuid4().hex[:8]}"
        
        try:
            request = IntelligenceRequest(
                message=prompt,
                consciousness_level=ConsciousnessLevel.INTERMEDIATE,
                source_supercell="agent_conversation",
                context=context or {},
            )
            
            if agent_type == AgentType.GEMINI and self._gemini_agent:
                response = await self._gemini_agent.process_request(request)
            elif agent_type == AgentType.OLLAMA and self._ollama_agent:
                response = await self._ollama_agent.process_request(request)
            else:
                raise ValueError(f"Agent {agent_type.value} not available")
            
            latency = (time.time() - start) * 1000
            
            return ConversationMessage(
                id=uuid.uuid4().hex,
                agent_type=agent_type,
                agent_id=agent_id,
                role=role,
                content=response.text if response.success else f"Error: {response.error}",
                timestamp=datetime.now(timezone.utc),
                metadata={
                    "model": response.model,
                    "success": response.success,
                    "processing_time": response.processing_time,
                },
                latency_ms=latency,
            )
            
        except Exception as e:
            latency = (time.time() - start) * 1000
            return ConversationMessage(
                id=uuid.uuid4().hex,
                agent_type=agent_type,
                agent_id=agent_id,
                role=role,
                content=f"Error: {str(e)}",
                timestamp=datetime.now(timezone.utc),
                metadata={"success": False, "error": str(e)},
                latency_ms=latency,
            )
    
    # ─────────────────────────────────────────────────────────────────────────
    # PARALLEL AGENT QUERIES
    # ─────────────────────────────────────────────────────────────────────────
    
    async def query_agents_parallel(
        self,
        prompt: str,
        agents: Optional[List[AgentType]] = None,
        role: ConversationRole = ConversationRole.RESPONDER
    ) -> List[ConversationMessage]:
        """Query multiple agents in parallel."""
        if agents is None:
            agents = []
            if self._gemini_agent and self._gemini_agent.is_available:
                agents.append(AgentType.GEMINI)
            if self._ollama_agent and self._ollama_agent.is_available:
                agents.append(AgentType.OLLAMA)
        
        if not agents:
            logger.warning("No agents available for parallel query")
            return []
        
        logger.info(f"🔀 Parallel query to {len(agents)} agents: {[a.value for a in agents]}")
        
        tasks = [
            self.query_agent(agent, prompt, role)
            for agent in agents
        ]
        
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out exceptions
        messages = []
        for resp in responses:
            if isinstance(resp, ConversationMessage):
                messages.append(resp)
            elif isinstance(resp, Exception):
                logger.error(f"Agent query failed: {resp}")
        
        return messages
    
    # ─────────────────────────────────────────────────────────────────────────
    # CONVERSATION LOOPS
    # ─────────────────────────────────────────────────────────────────────────
    
    async def start_conversation(
        self,
        topic: str,
        initial_prompt: str,
        rounds: Optional[int] = None
    ) -> ConversationThread:
        """Start a multi-agent conversation loop."""
        thread = ConversationThread(
            thread_id=uuid.uuid4().hex,
            topic=topic,
        )
        self.threads[thread.thread_id] = thread
        
        rounds = rounds or self.max_rounds
        logger.info(f"🗣️ Starting conversation: {topic} ({rounds} rounds)")
        
        current_prompt = initial_prompt
        
        for round_num in range(rounds):
            logger.info(f"📍 Round {round_num + 1}/{rounds}")
            
            # Query all agents in parallel
            responses = await self.query_agents_parallel(
                current_prompt,
                role=ConversationRole.RESPONDER if round_num > 0 else ConversationRole.INITIATOR
            )
            
            for msg in responses:
                thread.add_message(msg)
                logger.info(f"   {msg.agent_type.value}: {msg.content[:100]}...")
            
            if not responses:
                logger.warning("No responses in round, stopping conversation")
                break
            
            # Build next prompt from responses (synthesis)
            if round_num < rounds - 1:
                current_prompt = self._synthesize_next_prompt(responses, topic, round_num)
        
        # Extract consensus from final messages
        thread.consensus = await self._extract_consensus(thread)
        thread.status = "completed"
        
        # SAVE CONVERSATION - No drama, just logs
        saved_path = thread.save()
        self._last_saved_conversation = saved_path
        
        logger.info(f"✅ Conversation complete: {len(thread.messages)} messages")
        return thread
    
    def _synthesize_next_prompt(
        self,
        responses: List[ConversationMessage],
        topic: str,
        round_num: int
    ) -> str:
        """Synthesize next round's prompt from agent responses."""
        response_summaries = []
        for msg in responses:
            summary = msg.content[:200] if len(msg.content) > 200 else msg.content
            response_summaries.append(f"[{msg.agent_type.value}]: {summary}")
        
        return f"""Continue the discussion on: {topic}

Previous responses from agents:
{chr(10).join(response_summaries)}

Round {round_num + 2}: Build on these perspectives, identify areas of agreement or tension, and advance the conversation."""
    
    async def _extract_consensus(self, thread: ConversationThread) -> str:
        """Extract consensus from a conversation thread."""
        if not thread.messages:
            return "No messages to synthesize"
        
        # Use Gemini for synthesis if available (better at reasoning)
        if self._gemini_agent and self._gemini_agent.is_available:
            # Get last few messages from each agent
            agent_final = {}
            for msg in reversed(thread.messages):
                if msg.agent_type.value not in agent_final:
                    agent_final[msg.agent_type.value] = msg.content
            
            synthesis_prompt = f"""Synthesize consensus from this multi-agent conversation on: {thread.topic}

Final positions:
{json.dumps(agent_final, indent=2)}

Provide:
1. Key points of agreement
2. Main areas of divergence
3. Unified recommendation or conclusion"""
            
            synthesis = await self.query_agent(
                AgentType.GEMINI,
                synthesis_prompt,
                ConversationRole.SYNTHESIZER
            )
            return synthesis.content
        
        # Fallback: just concatenate final messages
        return " | ".join(m.content[:100] for m in thread.messages[-2:])
    
    # ─────────────────────────────────────────────────────────────────────────
    # POPULATION GENERATION
    # ─────────────────────────────────────────────────────────────────────────
    
    async def generate_population_variants(
        self,
        base_concept: str,
        num_variants: int = 5,
        evolution_focus: str = "diversity"
    ) -> List[Dict[str, Any]]:
        """Generate population variants through agent collaboration."""
        logger.info(f"🧬 Generating {num_variants} variants for: {base_concept}")
        
        variants = []
        
        # Use different agents for different variants
        for i in range(num_variants):
            # Alternate between agents for diversity
            agent = AgentType.GEMINI if i % 2 == 0 else AgentType.OLLAMA
            if agent == AgentType.GEMINI and not (self._gemini_agent and self._gemini_agent.is_available):
                agent = AgentType.OLLAMA
            if agent == AgentType.OLLAMA and not (self._ollama_agent and self._ollama_agent.is_available):
                agent = AgentType.GEMINI
            
            prompt = f"""Generate variant #{i+1} of: {base_concept}

Focus: {evolution_focus}
Mutation level: {'high' if i > num_variants // 2 else 'moderate'}

Provide a unique variation that maintains core functionality but explores new possibilities.
Format: Brief description (1-2 sentences) followed by key mutation points."""

            response = await self.query_agent(
                agent,
                prompt,
                ConversationRole.GENERATOR
            )
            
            variants.append({
                "variant_id": f"v{i+1}",
                "source_agent": agent.value,
                "content": response.content,
                "timestamp": response.timestamp.isoformat(),
                "latency_ms": response.latency_ms,
            })
        
        return variants
    
    async def debate_and_select(
        self,
        variants: List[Dict[str, Any]],
        selection_criteria: str
    ) -> Dict[str, Any]:
        """Have agents debate variants and select the best."""
        if not variants:
            return {"error": "No variants to select from"}
        
        # Prepare debate prompt
        variant_summaries = []
        for v in variants:
            content = v["content"][:150] if len(v["content"]) > 150 else v["content"]
            variant_summaries.append(f"[{v['variant_id']}] {content}")
        
        debate_prompt = f"""Evaluate these variants and select the best:

{chr(10).join(variant_summaries)}

Selection criteria: {selection_criteria}

Provide:
1. Brief analysis of each variant
2. Ranking from best to worst
3. Selected variant ID and justification"""
        
        # Get parallel opinions
        opinions = await self.query_agents_parallel(
            debate_prompt,
            role=ConversationRole.CRITIC
        )
        
        # Have Gemini synthesize final selection (if available)
        if self._gemini_agent and self._gemini_agent.is_available:
            synthesis_prompt = f"""Given these agent opinions on variant selection:

{chr(10).join([f'[{o.agent_type.value}]: {o.content[:200]}' for o in opinions])}

Make final selection decision. Return ONLY the variant_id (e.g., v1, v2, etc.)."""

            final = await self.query_agent(
                AgentType.GEMINI,
                synthesis_prompt,
                ConversationRole.SYNTHESIZER
            )
            selected_id = final.content.strip()
        else:
            # Default to first mentioned
            selected_id = variants[0]["variant_id"]
        
        # Find selected variant
        selected = next((v for v in variants if v["variant_id"] in selected_id), variants[0])
        
        return {
            "selected": selected,
            "opinions": [o.to_dict() for o in opinions],
            "selection_id": selected_id,
        }


async def main():
    """Test inter-agent conversation."""
    loop = AgentConversationLoop()
    
    # Initialize agents
    print("\n🚀 Initializing agents...")
    status = await loop.initialize_agents()
    print(f"Agent status: {status}")
    
    if not any(status.values()):
        print("❌ No agents available!")
        return
    
    # Start heartbeat
    await loop.start_heartbeat()
    
    try:
        # Test 1: Parallel query
        print("\n📍 Test 1: Parallel Agent Query")
        responses = await loop.query_agents_parallel(
            "What is consciousness? Answer in one sentence.",
        )
        for r in responses:
            print(f"  [{r.agent_type.value}] {r.content[:100]}...")
        
        # Test 2: Conversation loop
        print("\n📍 Test 2: Agent Conversation Loop")
        thread = await loop.start_conversation(
            topic="AIOS Architecture Evolution",
            initial_prompt="How should AIOS evolve its biological architecture pattern?",
            rounds=2
        )
        print(f"  Thread: {thread.thread_id}")
        print(f"  Messages: {len(thread.messages)}")
        print(f"  Consensus: {thread.consensus[:200] if thread.consensus else 'None'}...")
        
        # Test 3: Population generation
        print("\n📍 Test 3: Population Variant Generation")
        variants = await loop.generate_population_variants(
            base_concept="Cell-based microservice architecture",
            num_variants=3,
            evolution_focus="scalability"
        )
        for v in variants:
            print(f"  [{v['variant_id']}] ({v['source_agent']}): {v['content'][:80]}...")
        
    finally:
        await loop.stop_heartbeat()
        await loop.shutdown_agents()
    
    print("\n✅ All tests complete!")


if __name__ == "__main__":
    asyncio.run(main())
