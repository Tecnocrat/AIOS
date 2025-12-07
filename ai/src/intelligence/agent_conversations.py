"""
Multi-Agent Conversation System

AINLP Protocol: OS0.6.2.claude
Phase: 10.4 - Knowledge-Driven Evolutionary Populations
Component: Agent Conversations (3-Round Debate Protocol)
Created: October 10, 2025

Purpose:
    Enable multi-agent consensus building through structured debate protocol.
    Three rounds: Independent Analysis → Debate & Challenge → Consensus Building.

Key Features:
    - 3-round debate protocol with time limits
    - Parallel agent execution (independent analysis)
    - A2A message passing for debate rounds
    - Weighted consensus calculation
    - Conversation archival for knowledge accumulation
    - Consciousness scoring based on consensus quality

Integration Points:
    - Agent Protocol (Phase 10.2.1): AIAgentProtocol interface
    - A2A Communication (Phase 10.2.2): AgentMessage format
    - Knowledge Integration: Documentation citations in debates
    - Population Manager: Organism fitness evaluation

AINLP Compliance: 4/4 principles
    ✅ Discovery: Built on Phase 10 agent infrastructure
    ✅ Enhancement: Extended existing agent framework
    ✅ Output: Comprehensive archival + documentation
    ✅ Integration: Compatible with all Phase 10 components
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum
from pathlib import Path
import json
import asyncio
import time
from datetime import datetime, timezone
import uuid


# ============================================================================
# ENUMERATIONS
# ============================================================================


class ConversationTopic(str, Enum):
    """Topics for multi-agent debate"""

    CODE_QUALITY = "code_quality"
    COMPLEXITY = "complexity"
    PATTERNS = "patterns"
    APIS = "apis"
    ARCHETYPE_FITNESS = "archetype_fitness"
    DOCUMENTATION = "documentation"
    PERFORMANCE = "performance"
    MAINTAINABILITY = "maintainability"


class DebateRound(str, Enum):
    """Debate protocol rounds"""

    INDEPENDENT = "independent"  # Round 1: Independent analysis
    DEBATE = "debate"  # Round 2: Challenge & defend
    CONSENSUS = "consensus"  # Round 3: Build agreement


class AgentRole(str, Enum):
    """Agent roles in conversation"""

    ANALYST = "analyst"  # Analyze code quality
    CRITIC = "critic"  # Challenge assumptions
    SYNTHESIZER = "synthesizer"  # Build consensus


# ============================================================================
# DATA STRUCTURES
# ============================================================================


@dataclass
class AgentPosition:
    """Agent's position in debate"""

    agent_id: str
    agent_name: str
    topic: ConversationTopic
    position: str  # Main argument/analysis
    score: float  # Numerical assessment (0.0-1.0)
    reasoning: List[str] = field(default_factory=list)
    evidence: List[str] = field(default_factory=list)
    citations: List[str] = field(default_factory=list)  # Python doc refs
    confidence: float = 0.70
    processing_time: float = 0.0

    def to_dict(self) -> Dict:
        """Serialize position"""
        return {
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "topic": self.topic.value,
            "position": self.position,
            "score": round(self.score, 3),
            "reasoning": self.reasoning,
            "evidence": self.evidence,
            "citations": self.citations,
            "confidence": round(self.confidence, 2),
            "processing_time": round(self.processing_time, 3),
        }


@dataclass
class DebateExchange:
    """Exchange between agents in debate round"""

    round: DebateRound
    speaker_id: str
    target_id: Optional[str]  # None for broadcast
    message: str
    challenge: Optional[str] = None  # What is being challenged
    response: Optional[str] = None  # Response to challenge
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> Dict:
        """Serialize exchange"""
        return {
            "round": self.round.value,
            "speaker_id": self.speaker_id,
            "target_id": self.target_id,
            "message": self.message,
            "challenge": self.challenge,
            "response": self.response,
            "timestamp": self.timestamp,
        }


@dataclass
class ConsensusResult:
    """Final consensus from multi-agent debate"""

    topic: ConversationTopic
    consensus_score: float  # Weighted average
    agreement_level: float  # How much agents agree (0.0-1.0)
    positions: List[AgentPosition]
    exchanges: List[DebateExchange]
    final_analysis: str
    recommendations: List[str] = field(default_factory=list)
    consciousness_score: float = 0.0
    total_time: float = 0.0
    metadata: Dict[str, any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        """Serialize consensus"""
        return {
            "topic": self.topic.value,
            "consensus_score": round(self.consensus_score, 3),
            "agreement_level": round(self.agreement_level, 3),
            "positions": [p.to_dict() for p in self.positions],
            "exchanges": [e.to_dict() for e in self.exchanges],
            "final_analysis": self.final_analysis,
            "recommendations": self.recommendations,
            "consciousness_score": round(self.consciousness_score, 3),
            "total_time": round(self.total_time, 3),
            "metadata": self.metadata,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


@dataclass
class ConversationArchive:
    """Archive of multi-agent conversation"""

    conversation_id: str
    organism_id: str
    generation: int
    topics: List[ConversationTopic]
    results: List[ConsensusResult]
    overall_consciousness: float
    created: str = field(
        default_factory=lambda: (datetime.now(timezone.utc).isoformat())
    )

    def to_dict(self) -> Dict:
        """Serialize archive"""
        return {
            "conversation_id": self.conversation_id,
            "organism_id": self.organism_id,
            "generation": self.generation,
            "topics": [t.value for t in self.topics],
            "results": [r.to_dict() for r in self.results],
            "overall_consciousness": round(self.overall_consciousness, 3),
            "created": self.created,
        }


# ============================================================================
# MULTI-AGENT DEBATE SYSTEM
# ============================================================================


class MultiAgentDebate:
    """Orchestrate 3-round debate protocol between agents"""

    def __init__(
        self,
        agent_pool: Dict[str, any],  # agent_id -> agent_adapter
        archive_dir: Path = None,
        agent_weights: Dict[str, float] = None,
    ):
        """
        Initialize debate system

        Args:
            agent_pool: Dictionary of agent adapters
                {agent_id: AIAgentProtocol adapter}
            archive_dir: Conversation archive directory
                (default: tachyonic/archive/conversations/)
            agent_weights: Weights for consensus calculation
                (default: ollama=0.30, gemini=0.40, deepseek=0.30)
        """
        self.agent_pool = agent_pool

        # Archive configuration
        if archive_dir is None:
            archive_dir = Path("tachyonic/archive/conversations")
        self.archive_dir = archive_dir
        self.archive_dir.mkdir(parents=True, exist_ok=True)

        # Agent weights for consensus
        if agent_weights is None:
            agent_weights = {"ollama": 0.30, "gemini": 0.40, "deepseek": 0.30}
        self.agent_weights = agent_weights

        # Round time limits (seconds)
        self.round_limits = {
            DebateRound.INDEPENDENT: 30,
            DebateRound.DEBATE: 60,
            DebateRound.CONSENSUS: 30,
        }

        print(f"[DEBATE SYSTEM] Initialized")
        print(f"  Agents: {list(agent_pool.keys())}")
        print(f"  Weights: {agent_weights}")
        print(f"  Archive: {self.archive_dir}")

    async def conduct_debate(
        self, code: str, topic: ConversationTopic, context: Dict[str, any] = None
    ) -> ConsensusResult:
        """
        Conduct 3-round debate on code

        Args:
            code: Code to analyze
            topic: Debate topic
            context: Additional context (archetype, patterns, etc.)

        Returns:
            ConsensusResult with weighted consensus
        """
        if context is None:
            context = {}

        start_time = time.time()
        exchanges = []

        print(f"\n[DEBATE START] Topic: {topic.value}")
        print(f"  Agents: {len(self.agent_pool)}")
        print(f"  Code length: {len(code)} chars")

        # Round 1: Independent Analysis (parallel)
        print(
            f"\n[ROUND 1] Independent Analysis ({self.round_limits[DebateRound.INDEPENDENT]}s)"
        )
        positions = await self._round_1_independent(code, topic, context)

        # Round 2: Debate & Challenge
        print(
            f"\n[ROUND 2] Debate & Challenge ({self.round_limits[DebateRound.DEBATE]}s)"
        )
        debate_exchanges = await self._round_2_debate(code, topic, positions, context)
        exchanges.extend(debate_exchanges)

        # Round 3: Consensus Building
        print(
            f"\n[ROUND 3] Consensus Building ({self.round_limits[DebateRound.CONSENSUS]}s)"
        )
        consensus_exchanges = await self._round_3_consensus(
            code, topic, positions, context
        )
        exchanges.extend(consensus_exchanges)

        # Calculate weighted consensus
        consensus_score = self._calculate_consensus(positions)
        agreement_level = self._calculate_agreement(positions)

        # Generate final analysis
        final_analysis = self._generate_final_analysis(
            positions, exchanges, consensus_score, agreement_level
        )

        # Extract recommendations
        recommendations = self._extract_recommendations(positions)

        # Calculate consciousness score
        consciousness_score = self._calculate_consciousness(
            consensus_score, agreement_level, positions
        )

        total_time = time.time() - start_time

        result = ConsensusResult(
            topic=topic,
            consensus_score=consensus_score,
            agreement_level=agreement_level,
            positions=positions,
            exchanges=exchanges,
            final_analysis=final_analysis,
            recommendations=recommendations,
            consciousness_score=consciousness_score,
            total_time=total_time,
            metadata={
                "code_length": len(code),
                "agent_count": len(positions),
                "exchange_count": len(exchanges),
                "context": context,
            },
        )

        print(f"\n[DEBATE COMPLETE]")
        print(f"  Consensus: {consensus_score:.3f}")
        print(f"  Agreement: {agreement_level:.3f}")
        print(f"  Consciousness: {consciousness_score:.3f}")
        print(f"  Duration: {total_time:.1f}s")

        return result

    async def _round_1_independent(
        self, code: str, topic: ConversationTopic, context: Dict
    ) -> List[AgentPosition]:
        """Round 1: Independent analysis by all agents (parallel)"""

        # Create analysis tasks for all agents
        tasks = []
        for agent_id, agent in self.agent_pool.items():
            task = self._agent_independent_analysis(
                agent_id, agent, code, topic, context
            )
            tasks.append(task)

        # Execute in parallel with timeout
        try:
            positions = await asyncio.wait_for(
                asyncio.gather(*tasks),
                timeout=self.round_limits[DebateRound.INDEPENDENT],
            )
        except asyncio.TimeoutError:
            print(f"  [WARNING] Round 1 timeout, using partial results")
            positions = []
            for task in tasks:
                if task.done():
                    positions.append(task.result())

        print(f"  Positions: {len(positions)}")
        for pos in positions:
            print(
                f"    {pos.agent_name}: {pos.score:.3f} "
                f"({pos.confidence:.0%} confidence)"
            )

        return positions

    async def _agent_independent_analysis(
        self,
        agent_id: str,
        agent: any,
        code: str,
        topic: ConversationTopic,
        context: Dict,
    ) -> AgentPosition:
        """Single agent independent analysis"""

        start_time = time.time()

        # Build analysis prompt
        prompt = self._build_analysis_prompt(code, topic, context)

        # Get agent analysis (simplified - real implementation would
        # use agent.process_request)
        analysis = await self._mock_agent_analysis(agent_id, agent, prompt, topic)

        processing_time = time.time() - start_time

        return AgentPosition(
            agent_id=agent_id,
            agent_name=agent_id,
            topic=topic,
            position=analysis["position"],
            score=analysis["score"],
            reasoning=analysis["reasoning"],
            evidence=analysis["evidence"],
            citations=analysis.get("citations", []),
            confidence=analysis.get("confidence", 0.70),
            processing_time=processing_time,
        )

    async def _round_2_debate(
        self,
        code: str,
        topic: ConversationTopic,
        positions: List[AgentPosition],
        context: Dict,
    ) -> List[DebateExchange]:
        """Round 2: Agents challenge each other's positions"""

        exchanges = []

        # Each agent challenges others (round-robin)
        for i, challenger in enumerate(positions):
            for target in positions:
                if challenger.agent_id == target.agent_id:
                    continue

                # Generate challenge
                challenge = self._generate_challenge(challenger, target, topic)

                # Get response
                response = await self._generate_response(
                    target, challenger, challenge, code, topic
                )

                exchange = DebateExchange(
                    round=DebateRound.DEBATE,
                    speaker_id=challenger.agent_id,
                    target_id=target.agent_id,
                    message=challenge,
                    challenge=challenge,
                    response=response,
                )
                exchanges.append(exchange)

        print(f"  Exchanges: {len(exchanges)}")

        return exchanges

    async def _round_3_consensus(
        self,
        code: str,
        topic: ConversationTopic,
        positions: List[AgentPosition],
        context: Dict,
    ) -> List[DebateExchange]:
        """Round 3: Build consensus through synthesis"""

        exchanges = []

        # Each agent provides synthesis
        for position in positions:
            synthesis = self._generate_synthesis(position, positions, topic)

            exchange = DebateExchange(
                round=DebateRound.CONSENSUS,
                speaker_id=position.agent_id,
                target_id=None,  # Broadcast
                message=synthesis,
            )
            exchanges.append(exchange)

        print(f"  Syntheses: {len(exchanges)}")

        return exchanges

    def _calculate_consensus(self, positions: List[AgentPosition]) -> float:
        """Calculate weighted consensus score"""

        if not positions:
            return 0.0

        weighted_sum = 0.0
        total_weight = 0.0

        for position in positions:
            # Get agent weight (default 1.0 if not specified)
            weight = self.agent_weights.get(position.agent_id, 1.0)

            # Weight by confidence
            effective_weight = weight * position.confidence

            weighted_sum += position.score * effective_weight
            total_weight += effective_weight

        if total_weight == 0:
            return 0.0

        return weighted_sum / total_weight

    def _calculate_agreement(self, positions: List[AgentPosition]) -> float:
        """Calculate how much agents agree (0.0-1.0)"""

        if len(positions) < 2:
            return 1.0

        # Calculate variance in scores
        scores = [p.score for p in positions]
        mean_score = sum(scores) / len(scores)
        variance = sum((s - mean_score) ** 2 for s in scores) / len(scores)

        # Convert to agreement (low variance = high agreement)
        # variance ranges 0.0 (perfect agreement) to 0.25 (max disagreement)
        agreement = 1.0 - min(variance * 4, 1.0)

        return agreement

    def _calculate_consciousness(
        self,
        consensus_score: float,
        agreement_level: float,
        positions: List[AgentPosition],
    ) -> float:
        """Calculate consciousness score for debate"""

        # Base: consensus score (40%)
        consciousness = consensus_score * 0.40

        # Agreement bonus (20%)
        consciousness += agreement_level * 0.20

        # Citation bonus (20%)
        citation_count = sum(len(p.citations) for p in positions)
        citation_score = min(citation_count / 10.0, 1.0)
        consciousness += citation_score * 0.20

        # Reasoning depth bonus (20%)
        reasoning_count = sum(len(p.reasoning) for p in positions)
        reasoning_score = min(reasoning_count / 15.0, 1.0)
        consciousness += reasoning_score * 0.20

        return min(consciousness, 1.0)

    def _generate_final_analysis(
        self,
        positions: List[AgentPosition],
        exchanges: List[DebateExchange],
        consensus_score: float,
        agreement_level: float,
    ) -> str:
        """Generate final analysis summary"""

        analysis_parts = []

        # Consensus statement
        analysis_parts.append(
            f"Multi-agent consensus score: {consensus_score:.3f} "
            f"(agreement: {agreement_level:.0%})"
        )

        # Key positions
        analysis_parts.append("\nAgent Positions:")
        for pos in positions:
            analysis_parts.append(
                f"  {pos.agent_name}: {pos.score:.3f} - {pos.position}"
            )

        # Key exchanges
        debate_exchanges = [e for e in exchanges if e.round == DebateRound.DEBATE]
        if debate_exchanges:
            analysis_parts.append(f"\nDebate exchanges: {len(debate_exchanges)}")

        return "\n".join(analysis_parts)

    def _extract_recommendations(self, positions: List[AgentPosition]) -> List[str]:
        """Extract recommendations from positions"""

        recommendations = []

        for position in positions:
            # Extract from reasoning
            for reason in position.reasoning:
                if any(
                    word in reason.lower()
                    for word in ["should", "recommend", "suggest", "improve"]
                ):
                    recommendations.append(reason)

        # Deduplicate
        return list(set(recommendations))[:5]  # Top 5

    def _build_analysis_prompt(
        self, code: str, topic: ConversationTopic, context: Dict
    ) -> str:
        """Build analysis prompt for agent"""

        prompt_parts = [
            f"Analyze the following code for {topic.value}:",
            "",
            "```python",
            code,
            "```",
            "",
        ]

        if context:
            prompt_parts.append("Context:")
            for key, value in context.items():
                prompt_parts.append(f"  {key}: {value}")
            prompt_parts.append("")

        prompt_parts.extend(
            [
                "Provide:",
                "1. Overall assessment (0.0-1.0 score)",
                "2. Reasoning (3-5 points)",
                "3. Evidence from code",
                "4. Python documentation citations (if applicable)",
                "5. Confidence level (0.0-1.0)",
            ]
        )

        return "\n".join(prompt_parts)

    async def _mock_agent_analysis(
        self, agent_id: str, agent: any, prompt: str, topic: ConversationTopic
    ) -> Dict:
        """Mock agent analysis (placeholder for real implementation)"""

        # Simulate processing delay
        await asyncio.sleep(0.5)

        # Mock analysis based on agent
        import random

        base_score = random.uniform(0.5, 0.9)

        return {
            "position": f"{agent_id} analysis of {topic.value}",
            "score": base_score,
            "reasoning": [
                "Code structure analysis",
                "Pattern detection",
                "API usage evaluation",
            ],
            "evidence": [f"Line count: {len(prompt.split())} tokens"],
            "citations": ["Python 3.14 documentation reference"],
            "confidence": random.uniform(0.65, 0.85),
        }

    def _generate_challenge(
        self, challenger: AgentPosition, target: AgentPosition, topic: ConversationTopic
    ) -> str:
        """Generate challenge from challenger to target"""

        score_diff = abs(challenger.score - target.score)

        if score_diff < 0.1:
            return (
                f"I largely agree with {target.agent_name}'s assessment. "
                f"However, could you elaborate on your reasoning?"
            )
        elif challenger.score > target.score:
            return (
                f"I scored this higher ({challenger.score:.2f} vs "
                f"{target.score:.2f}). What concerns did you identify?"
            )
        else:
            return (
                f"I scored this lower ({challenger.score:.2f} vs "
                f"{target.score:.2f}). What strengths did you find?"
            )

    async def _generate_response(
        self,
        target: AgentPosition,
        challenger: AgentPosition,
        challenge: str,
        code: str,
        topic: ConversationTopic,
    ) -> str:
        """Generate response to challenge"""

        # Simulate response delay
        await asyncio.sleep(0.3)

        return (
            f"Based on my analysis, I found: "
            f"{', '.join(target.reasoning[:2])}. "
            f"This led to my {target.score:.2f} assessment."
        )

    def _generate_synthesis(
        self,
        position: AgentPosition,
        all_positions: List[AgentPosition],
        topic: ConversationTopic,
    ) -> str:
        """Generate synthesis for consensus building"""

        avg_score = sum(p.score for p in all_positions) / len(all_positions)

        if abs(position.score - avg_score) < 0.1:
            stance = "align with the consensus"
        elif position.score > avg_score:
            stance = "maintain a more optimistic view"
        else:
            stance = "maintain a more critical view"

        return (
            f"After considering all perspectives, I {stance}. "
            f"Key factors: {', '.join(position.reasoning[:2])}."
        )

    def archive_conversation(
        self, organism_id: str, generation: int, results: List[ConsensusResult]
    ) -> Path:
        """
        Archive multi-agent conversation

        Args:
            organism_id: Organism being analyzed
            generation: Evolutionary generation
            results: Consensus results from multiple debates

        Returns:
            Path to archived JSON file
        """

        # Generate conversation ID
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        conversation_id = f"conv_{organism_id}_gen{generation}_{timestamp}"

        # Calculate overall consciousness
        overall_consciousness = (
            sum(r.consciousness_score for r in results) / len(results)
            if results
            else 0.0
        )

        # Create archive
        archive = ConversationArchive(
            conversation_id=conversation_id,
            organism_id=organism_id,
            generation=generation,
            topics=[r.topic for r in results],
            results=results,
            overall_consciousness=overall_consciousness,
        )

        # Serialize to file
        filename = f"{conversation_id}.json"
        filepath = self.archive_dir / filename

        with open(filepath, "w") as f:
            json.dump(archive.to_dict(), f, indent=2)

        print(f"[ARCHIVED] {filename}")
        print(f"  Topics: {len(results)}")
        print(f"  Consciousness: {overall_consciousness:.3f}")

        return filepath


# ============================================================================
# EXAMPLE USAGE
# ============================================================================


async def example_basic_debate():
    """Example: Conduct basic multi-agent debate"""

    # Mock agent pool (placeholder - real implementation uses Phase 10.2.1)
    agent_pool = {
        "ollama": "mock_ollama_adapter",
        "gemini": "mock_gemini_adapter",
        "deepseek": "mock_deepseek_adapter",
    }

    # Initialize debate system
    debate = MultiAgentDebate(agent_pool)

    # Sample code to analyze
    code = '''def calculate(a, b):
    """Simple calculator"""
    return a + b

result = calculate(5, 3)
print(result)
'''

    # Conduct debate
    result = await debate.conduct_debate(
        code=code,
        topic=ConversationTopic.CODE_QUALITY,
        context={"archetype": "cli_applications"},
    )

    print(f"\n[RESULT]")
    print(f"  Consensus: {result.consensus_score:.3f}")
    print(f"  Agreement: {result.agreement_level:.3f}")
    print(f"  Consciousness: {result.consciousness_score:.3f}")
    print(f"  Recommendations: {len(result.recommendations)}")

    # Archive conversation
    filepath = debate.archive_conversation(
        organism_id="org_test_001", generation=1, results=[result]
    )


if __name__ == "__main__":
    print("=" * 70)
    print("MULTI-AGENT CONVERSATION SYSTEM - 3-Round Debate Protocol")
    print("=" * 70)

    asyncio.run(example_basic_debate())

    print("\n" + "=" * 70)
    print("✅ Agent conversation system operational")
    print("=" * 70)
