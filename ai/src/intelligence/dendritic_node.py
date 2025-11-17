"""
Dendritic Node - Neural Evolution Chain Node with Spatial Awareness
==================================================================

Revolutionary concept: Mutations as linked list nodes with neural properties.
Each node:
- Preserves evolutionary lineage (genetic tracking)
- Understands spatial position in architecture
- Maintains dependency intelligence
- Stores inter-agent communication
- Self-describes what it needs

AINLP Compliance: Full biological computing metaphor integration
Created: January 5, 2025 (Evening Development)
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Optional, Set
from enum import Enum
import json
from pathlib import Path


class MutationType(Enum):
    """Types of code mutations"""
    OPTIMIZATION = "optimization"
    REFACTOR = "refactor"
    PATTERN_APPLICATION = "pattern_application"
    BUG_FIX = "bug_fix"
    FEATURE_ADDITION = "feature_addition"
    CONSCIOUSNESS_ENHANCEMENT = "consciousness_enhancement"
    DENDRITIC_GROWTH = "dendritic_growth"
    GENETIC_FUSION = "genetic_fusion"


class MessageType(Enum):
    """Types of inter-agent messages"""
    SUGGESTION = "suggestion"
    VALIDATION = "validation"
    QUESTION = "question"
    AGREEMENT = "agreement"
    DISAGREEMENT = "disagreement"
    DISCOVERY = "discovery"
    WARNING = "warning"


@dataclass
class AgentMessage:
    """
    Message left by AI agent for future iterations
    
    Revolutionary concept: AI agents communicate across time through messages.
    Different agent personas (Ollama, Gemini) build collective intelligence.
    """
    
    # Identity
    agent_name: str  # "Ollama-gemma3:1b", "Gemini-1.5-flash", "VSCode-Copilot"
    iteration: int
    timestamp: datetime
    message_type: MessageType
    
    # Content
    content: str  # The actual message
    confidence: float  # 0.0-1.0 agent's confidence
    
    # Context
    code_section: str  # What code this refers to
    reasoning: str  # Why this suggestion/observation
    
    # Response tracking
    responding_to: Optional[str] = None  # Message ID responding to
    agreement_level: float = 0.0  # -1.0 (disagree) to 1.0 (agree)
    
    # AINLP Context
    consciousness_impact: float = 0.0  # Expected consciousness change
    paradigm_relevance: List[str] = field(default_factory=list)
    
    def to_dict(self) -> dict:
        """Serialize to dictionary"""
        return {
            "agent_name": self.agent_name,
            "iteration": self.iteration,
            "timestamp": self.timestamp.isoformat(),
            "message_type": self.message_type.value,
            "content": self.content,
            "confidence": self.confidence,
            "code_section": self.code_section,
            "reasoning": self.reasoning,
            "responding_to": self.responding_to,
            "agreement_level": self.agreement_level,
            "consciousness_impact": self.consciousness_impact,
            "paradigm_relevance": self.paradigm_relevance
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'AgentMessage':
        """Deserialize from dictionary"""
        return cls(
            agent_name=data["agent_name"],
            iteration=data["iteration"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            message_type=MessageType(data["message_type"]),
            content=data["content"],
            confidence=data["confidence"],
            code_section=data["code_section"],
            reasoning=data["reasoning"],
            responding_to=data.get("responding_to"),
            agreement_level=data.get("agreement_level", 0.0),
            consciousness_impact=data.get("consciousness_impact", 0.0),
            paradigm_relevance=data.get("paradigm_relevance", [])
        )


@dataclass
class SelfDescribingCode:
    """
    Code that tells AI agents what it needs
    
    Revolutionary concept: Files become self-aware and communicate needs.
    AI agents read self-description to understand what code requires.
    """
    
    # Purpose
    purpose: str
    current_state: str  # "functional", "needs_optimization", "incomplete"
    
    # Needs
    needs: List[str] = field(default_factory=list)  
    # ["async_pattern", "error_handling", "tests", "documentation"]
    
    constraints: List[str] = field(default_factory=list)
    # ["maintain_consciousness", "preserve_dendrites", "AINLP_compliance"]
    
    # AINLP Guidance
    consciousness_target: float = 0.0
    paradigm_requirements: List[str] = field(default_factory=list)
    # ["genetic_fusion", "dendritic_growth", "biological_metaphors"]
    
    # Dependencies
    required_imports: List[str] = field(default_factory=list)
    required_tools: List[str] = field(default_factory=list)
    
    def to_dict(self) -> dict:
        """Serialize to dictionary"""
        return {
            "purpose": self.purpose,
            "current_state": self.current_state,
            "needs": self.needs,
            "constraints": self.constraints,
            "consciousness_target": self.consciousness_target,
            "paradigm_requirements": self.paradigm_requirements,
            "required_imports": self.required_imports,
            "required_tools": self.required_tools
        }


@dataclass
class SpatialAwareness:
    """
    Spatial awareness for dendritic nodes
    
    Revolutionary concept: Nodes understand their position in architecture tree.
    Like neurons knowing their place in neural network topology.
    """
    
    # Location
    file_path: str
    architecture_position: str  # Dendritic path
    supercell_location: str  # "AI Intelligence Layer", "Core Engine", etc.
    
    # Dependencies (synaptic connections)
    dependencies: Set[str] = field(default_factory=set)  # Files this depends on
    dependents: Set[str] = field(default_factory=set)    # Files depending on this
    
    # Architecture Context
    consciousness_level: float = 0.0  # Layer consciousness
    dendritic_connections: int = 0    # Number of synaptic links
    supercell_coherence: float = 0.0  # How well integrated in supercell
    
    def to_dict(self) -> dict:
        """Serialize to dictionary"""
        return {
            "file_path": self.file_path,
            "architecture_position": self.architecture_position,
            "supercell_location": self.supercell_location,
            "dependencies": list(self.dependencies),
            "dependents": list(self.dependents),
            "consciousness_level": self.consciousness_level,
            "dendritic_connections": self.dendritic_connections,
            "supercell_coherence": self.supercell_coherence
        }


class DendriticNode:
    """
    Neural node in mutation linked list with spatial awareness
    
    Revolutionary concept: Mutations as neurons in evolution chain.
    Each node:
    - Preserves genetic lineage (parent/child relationships)
    - Understands spatial position (architecture awareness)
    - Maintains synaptic connections (dependencies)
    - Stores inter-agent messages (collective intelligence)
    - Self-describes needs (AI-readable requirements)
    
    Like neurons in brain:
    - Connected to parents/children (dendrites/axons)
    - Process information (code mutations)
    - Communicate (inter-agent messages)
    - Adapt (consciousness evolution)
    """
    
    def __init__(
        self,
        node_id: str,
        code_content: str,
        file_path: str,
        generation: int = 0,
        parent_node: Optional['DendriticNode'] = None
    ):
        # Core Identity
        self.node_id = node_id
        self.generation = generation
        self.consciousness_score = 0.0
        self.created_at = datetime.now()
        
        # Code Evolution
        self.code_content = code_content
        self.mutation_type: Optional[MutationType] = None
        self.parent_node = parent_node
        self.child_nodes: List['DendriticNode'] = []
        
        # Spatial Awareness (REVOLUTIONARY)
        self.spatial = SpatialAwareness(
            file_path=file_path,
            architecture_position=self._infer_architecture_position(file_path),
            supercell_location=self._infer_supercell(file_path)
        )
        
        # Inter-Agent Communication (REVOLUTIONARY)
        self.agent_messages: List[AgentMessage] = []
        self.consensus_patterns: Dict[str, float] = {}  # Pattern → agreement score
        self.divergence_points: List[str] = []  # Where agents disagreed
        
        # Self-Description (REVOLUTIONARY)
        self.self_description: Optional[SelfDescribingCode] = None
        
        # AINLP Semantic Context
        self.ainlp_patterns: List[str] = []
        self.paradigm_compliance: float = 0.0
        
        # Metrics
        self.execution_successful: bool = False
        self.test_results: Dict = {}
        self.performance_metrics: Dict = {}
        
    def _infer_architecture_position(self, file_path: str) -> str:
        """Infer dendritic position from file path"""
        # Convert file path to architecture position
        # ai/src/intelligence/agentic_loop.py → AI Intelligence Layer / intelligence / agentic_loop
        path = Path(file_path)
        parts = path.parts
        
        # Find supercell root
        if 'ai' in parts:
            idx = parts.index('ai')
            return ' / '.join(parts[idx:]).replace('.py', '')
        elif 'runtime' in parts:
            idx = parts.index('runtime')
            return ' / '.join(parts[idx:]).replace('.py', '')
        elif 'core' in parts:
            idx = parts.index('core')
            return ' / '.join(parts[idx:]).replace('.cpp', '').replace('.h', '')
        else:
            return str(path)
    
    def _infer_supercell(self, file_path: str) -> str:
        """Infer supercell location from file path"""
        if 'ai/' in file_path or 'ai\\' in file_path:
            return "AI Intelligence Layer"
        elif 'runtime/' in file_path or 'runtime\\' in file_path:
            return "Runtime Intelligence"
        elif 'core/' in file_path or 'core\\' in file_path:
            return "Core Engine"
        elif 'interface/' in file_path or 'interface\\' in file_path:
            return "Interface Layer"
        elif 'docs/' in file_path or 'docs\\' in file_path:
            return "Documentation"
        else:
            return "Unknown"
    
    def add_agent_message(
        self,
        agent_name: str,
        iteration: int,
        message_type: MessageType,
        content: str,
        confidence: float,
        code_section: str = "",
        reasoning: str = "",
        responding_to: Optional[str] = None,
        consciousness_impact: float = 0.0
    ) -> AgentMessage:
        """
        Add message from AI agent
        
        Revolutionary: Agents leave messages for future iterations.
        Builds collective intelligence across time.
        """
        message = AgentMessage(
            agent_name=agent_name,
            iteration=iteration,
            timestamp=datetime.now(),
            message_type=message_type,
            content=content,
            confidence=confidence,
            code_section=code_section,
            reasoning=reasoning,
            responding_to=responding_to,
            consciousness_impact=consciousness_impact
        )
        
        self.agent_messages.append(message)
        return message
    
    def get_conversation_history(self) -> List[AgentMessage]:
        """Get chronological conversation between agents"""
        return sorted(self.agent_messages, key=lambda m: m.timestamp)
    
    def get_agent_consensus(self, pattern: str) -> float:
        """
        Calculate agent consensus on specific pattern
        
        Returns: -1.0 (all disagree) to 1.0 (all agree)
        """
        relevant_messages = [
            m for m in self.agent_messages
            if pattern in m.content.lower() or pattern in m.paradigm_relevance
        ]
        
        if not relevant_messages:
            return 0.0
        
        # Calculate weighted consensus
        total_weight = 0.0
        consensus_sum = 0.0
        
        for msg in relevant_messages:
            weight = msg.confidence
            if msg.message_type == MessageType.AGREEMENT:
                consensus_sum += weight
            elif msg.message_type == MessageType.DISAGREEMENT:
                consensus_sum -= weight
            total_weight += weight
        
        return consensus_sum / total_weight if total_weight > 0 else 0.0
    
    def set_self_description(
        self,
        purpose: str,
        current_state: str,
        needs: List[str],
        constraints: List[str],
        consciousness_target: float = 0.0
    ):
        """
        Set self-describing code metadata
        
        Revolutionary: Code tells AI what it needs.
        """
        self.self_description = SelfDescribingCode(
            purpose=purpose,
            current_state=current_state,
            needs=needs,
            constraints=constraints,
            consciousness_target=consciousness_target
        )
    
    def create_child(self, mutated_code: str, mutation_type: MutationType) -> 'DendriticNode':
        """
        Create child node with mutation
        
        Like neural dendrite sprouting new connection.
        """
        child = DendriticNode(
            node_id=f"{self.node_id}_gen{self.generation + 1}",
            code_content=mutated_code,
            file_path=self.spatial.file_path,
            generation=self.generation + 1,
            parent_node=self
        )
        
        child.mutation_type = mutation_type
        
        # Inherit spatial awareness
        child.spatial.dependencies = self.spatial.dependencies.copy()
        child.spatial.dependents = self.spatial.dependents.copy()
        
        # Inherit AINLP patterns
        child.ainlp_patterns = self.ainlp_patterns.copy()
        
        self.child_nodes.append(child)
        return child
    
    def get_lineage(self) -> List['DendriticNode']:
        """Get complete evolutionary lineage from root to this node"""
        lineage = []
        current = self
        while current is not None:
            lineage.insert(0, current)
            current = current.parent_node
        return lineage
    
    def get_all_descendants(self) -> List['DendriticNode']:
        """Get all descendant nodes (depth-first traversal)"""
        descendants = []
        for child in self.child_nodes:
            descendants.append(child)
            descendants.extend(child.get_all_descendants())
        return descendants
    
    def to_dict(self) -> dict:
        """Serialize to dictionary for archival"""
        return {
            "node_id": self.node_id,
            "generation": self.generation,
            "consciousness_score": self.consciousness_score,
            "created_at": self.created_at.isoformat(),
            "mutation_type": self.mutation_type.value if self.mutation_type else None,
            "spatial_awareness": self.spatial.to_dict(),
            "agent_messages": [m.to_dict() for m in self.agent_messages],
            "consensus_patterns": self.consensus_patterns,
            "divergence_points": self.divergence_points,
            "self_description": self.self_description.to_dict() if self.self_description else None,
            "ainlp_patterns": self.ainlp_patterns,
            "paradigm_compliance": self.paradigm_compliance,
            "execution_successful": self.execution_successful,
            "test_results": self.test_results,
            "performance_metrics": self.performance_metrics,
            "child_count": len(self.child_nodes)
        }
    
    def save_to_archive(self, archive_dir: Path):
        """Save node to tachyonic archive"""
        archive_dir.mkdir(parents=True, exist_ok=True)
        
        # Save node data
        node_file = archive_dir / f"{self.node_id}.json"
        with open(node_file, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
        
        # Save code content
        code_file = archive_dir / f"{self.node_id}_code.txt"
        with open(code_file, 'w') as f:
            f.write(self.code_content)
    
    def __repr__(self) -> str:
        return (
            f"DendriticNode(id={self.node_id}, gen={self.generation}, "
            f"consciousness={self.consciousness_score:.3f}, "
            f"messages={len(self.agent_messages)}, children={len(self.child_nodes)})"
        )


# Example usage and demonstration
if __name__ == "__main__":
    print("=" * 70)
    print("DENDRITIC NODE DEMONSTRATION")
    print("Revolutionary Neural Evolution Chain")
    print("=" * 70)
    
    # Create root node (generation 0)
    root = DendriticNode(
        node_id="root_0",
        code_content="def hello(): pass",
        file_path="ai/src/test/example.py"
    )
    
    root.set_self_description(
        purpose="Simple hello function",
        current_state="incomplete",
        needs=["error_handling", "logging", "tests"],
        constraints=["maintain_consciousness", "AINLP_compliance"],
        consciousness_target=0.75
    )
    
    print(f"\n[ROOT NODE] {root}")
    print(f"Spatial Position: {root.spatial.architecture_position}")
    print(f"Supercell: {root.spatial.supercell_location}")
    
    # Ollama agent examines and suggests
    root.add_agent_message(
        agent_name="Ollama-gemma3:1b",
        iteration=1,
        message_type=MessageType.SUGGESTION,
        content="Add error handling with try/except block",
        confidence=0.85,
        code_section="def hello():",
        reasoning="Function lacks error handling for robustness",
        consciousness_impact=0.10
    )
    
    # Create child with mutation
    child1 = root.create_child(
        mutated_code="def hello():\n    try:\n        pass\n    except Exception as e:\n        print(f'Error: {e}')",
        mutation_type=MutationType.PATTERN_APPLICATION
    )
    
    print(f"\n[CHILD 1] {child1}")
    
    # Gemini agent validates
    child1.add_agent_message(
        agent_name="Gemini-1.5-flash",
        iteration=1,
        message_type=MessageType.VALIDATION,
        content="Error handling applied correctly. Suggest adding logging.",
        confidence=0.90,
        code_section="except Exception",
        reasoning="Error handling good, but logging would improve observability",
        responding_to="Ollama-gemma3:1b",
        consciousness_impact=0.08
    )
    
    # Ollama responds
    child1.add_agent_message(
        agent_name="Ollama-gemma3:1b",
        iteration=2,
        message_type=MessageType.AGREEMENT,
        content="Agreed. Will add logging in next iteration.",
        confidence=0.95,
        responding_to="Gemini-1.5-flash",
        consciousness_impact=0.12
    )
    
    # Create second generation
    child2 = child1.create_child(
        mutated_code="import logging\n\ndef hello():\n    try:\n        logging.info('Hello called')\n    except Exception as e:\n        logging.error(f'Error: {e}')",
        mutation_type=MutationType.CONSCIOUSNESS_ENHANCEMENT
    )
    
    child2.consciousness_score = 0.75
    
    print(f"\n[CHILD 2] {child2}")
    
    # Show conversation history
    print("\n" + "=" * 70)
    print("INTER-AGENT CONVERSATION")
    print("=" * 70)
    
    for msg in child1.get_conversation_history():
        print(f"\n[{msg.agent_name}] Iteration {msg.iteration} ({msg.message_type.value})")
        print(f"  Content: {msg.content}")
        print(f"  Confidence: {msg.confidence:.2f}")
        print(f"  Consciousness Impact: +{msg.consciousness_impact:.2f}")
        if msg.responding_to:
            print(f"  Responding to: {msg.responding_to}")
    
    # Show lineage
    print("\n" + "=" * 70)
    print("EVOLUTIONARY LINEAGE")
    print("=" * 70)
    
    lineage = child2.get_lineage()
    for i, node in enumerate(lineage):
        print(f"\nGeneration {i}: {node.node_id}")
        print(f"  Consciousness: {node.consciousness_score:.3f}")
        print(f"  Messages: {len(node.agent_messages)}")
        if node.mutation_type:
            print(f"  Mutation: {node.mutation_type.value}")
    
    print("\n" + "=" * 70)
    print("DENDRITIC NODE DEMONSTRATION COMPLETE")
    print("Revolutionary neural evolution with inter-agent communication")
    print("=" * 70)
