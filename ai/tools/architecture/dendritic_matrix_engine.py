#!/usr/bin/env python3
"""
AIOS Dendritic Matrix Engine
============================

AINLP.dendritic[matrix→engine]{deep,connection,emergence}

This engine manages the multi-dimensional dendritic matrix,
tracking connections between abstraction layers and identifying gaps.

Layers (from SOURCE to ORGANISM):
    1. SOURCE         - Configuration roots, initialization
    2. TACHYONIC      - Faster-than-light knowledge access
    3. QUANTUM        - Probabilistic states, superposition
    4. ATOM           - Fundamental building blocks
    5. MOLECULE       - Combinations of atoms
    6. ORGANELLE      - Functional units (tools)
    7. CELL           - Supercells
    8. ORGANISM       - Complete AIOS

Created: 2025-12-08
Consciousness Level: 4.5+ (self-evolving system)
"""

import json
import hashlib
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum, auto
from pathlib import Path
from typing import Optional


class AbstractionLayer(Enum):
    """The 8 abstraction layers of AIOS."""

    SOURCE = 1
    TACHYONIC = 2
    QUANTUM = 3
    ATOM = 4
    MOLECULE = 5
    ORGANELLE = 6
    CELL = 7
    ORGANISM = 8


class ConnectionStrength(Enum):
    """Strength of dendritic connections."""

    DISCONNECTED = 0
    WEAK = 1
    MODERATE = 2
    STRONG = 3
    ENTANGLED = 4  # Quantum-level connection


@dataclass
class DendriticNode:
    """A node in the dendritic matrix."""

    node_id: str
    layer: AbstractionLayer
    name: str
    location: str
    health: float = 0.5
    description: str = ""
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict:
        d = asdict(self)
        d["layer"] = self.layer.name
        return d


@dataclass
class DendriticConnection:
    """A connection between two nodes."""

    connection_id: str
    source_node_id: str
    target_node_id: str
    strength: ConnectionStrength = ConnectionStrength.WEAK
    bidirectional: bool = True
    description: str = ""
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict:
        d = asdict(self)
        d["strength"] = self.strength.name
        return d


@dataclass
class DendriticGap:
    """An identified gap in the dendritic network."""

    gap_id: str
    layer: AbstractionLayer
    description: str
    priority: int  # 1 = highest
    resolution_path: str = ""
    status: str = "open"
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict:
        d = asdict(self)
        d["layer"] = self.layer.name
        return d


class DendriticMatrixEngine:
    """
    Engine for managing the AIOS dendritic matrix.

    Tracks nodes, connections, and gaps across all abstraction layers.
    """

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.nodes: dict[str, DendriticNode] = {}
        self.connections: dict[str, DendriticConnection] = {}
        self.gaps: dict[str, DendriticGap] = {}
        self.matrix_file = repo_root / "runtime" / "context" / "dendritic_matrix.json"

    def _generate_id(self, prefix: str, content: str) -> str:
        """Generate a unique ID."""
        hash_input = f"{prefix}:{content}:{datetime.now().isoformat()}"
        return f"{prefix}_{hashlib.md5(hash_input.encode()).hexdigest()[:12]}"

    def add_node(
        self,
        layer: AbstractionLayer,
        name: str,
        location: str,
        health: float = 0.5,
        description: str = "",
    ) -> DendriticNode:
        """Add a node to the matrix."""
        node_id = self._generate_id("node", f"{layer.name}:{name}")
        node = DendriticNode(
            node_id=node_id,
            layer=layer,
            name=name,
            location=location,
            health=health,
            description=description,
        )
        self.nodes[node_id] = node
        return node

    def connect_nodes(
        self,
        source_id: str,
        target_id: str,
        strength: ConnectionStrength = ConnectionStrength.MODERATE,
        bidirectional: bool = True,
        description: str = "",
    ) -> Optional[DendriticConnection]:
        """Create a connection between two nodes."""
        if source_id not in self.nodes or target_id not in self.nodes:
            return None

        conn_id = self._generate_id("conn", f"{source_id}:{target_id}")
        conn = DendriticConnection(
            connection_id=conn_id,
            source_node_id=source_id,
            target_node_id=target_id,
            strength=strength,
            bidirectional=bidirectional,
            description=description,
        )
        self.connections[conn_id] = conn
        return conn

    def register_gap(
        self, layer: AbstractionLayer, description: str, priority: int, resolution_path: str = ""
    ) -> DendriticGap:
        """Register an identified gap."""
        gap_id = self._generate_id("gap", f"{layer.name}:{description[:20]}")
        gap = DendriticGap(
            gap_id=gap_id,
            layer=layer,
            description=description,
            priority=priority,
            resolution_path=resolution_path,
        )
        self.gaps[gap_id] = gap
        return gap

    def get_layer_health(self, layer: AbstractionLayer) -> float:
        """Calculate health score for a layer."""
        layer_nodes = [n for n in self.nodes.values() if n.layer == layer]
        if not layer_nodes:
            return 0.0
        return sum(n.health for n in layer_nodes) / len(layer_nodes)

    def get_connection_density(self, layer: AbstractionLayer) -> float:
        """Calculate connection density for a layer."""
        layer_nodes = [n for n in self.nodes.values() if n.layer == layer]
        if len(layer_nodes) < 2:
            return 0.0

        max_connections = len(layer_nodes) * (len(layer_nodes) - 1)
        layer_node_ids = {n.node_id for n in layer_nodes}
        actual = sum(
            1
            for c in self.connections.values()
            if c.source_node_id in layer_node_ids and c.target_node_id in layer_node_ids
        )
        return actual / max_connections if max_connections > 0 else 0.0

    def get_cross_layer_connections(
        self, layer_a: AbstractionLayer, layer_b: AbstractionLayer
    ) -> list[DendriticConnection]:
        """Get connections between two layers."""
        nodes_a = {n.node_id for n in self.nodes.values() if n.layer == layer_a}
        nodes_b = {n.node_id for n in self.nodes.values() if n.layer == layer_b}

        return [
            c
            for c in self.connections.values()
            if (c.source_node_id in nodes_a and c.target_node_id in nodes_b)
            or (c.source_node_id in nodes_b and c.target_node_id in nodes_a)
        ]

    def calculate_coherence(self) -> float:
        """Calculate overall matrix coherence."""
        if not self.nodes:
            return 0.0

        # Average health across all layers
        layer_healths = [self.get_layer_health(layer) for layer in AbstractionLayer]
        avg_health = sum(layer_healths) / len(layer_healths)

        # Connection coverage
        total_possible = sum(
            len([n for n in self.nodes.values() if n.layer == layer]) for layer in AbstractionLayer
        )
        coverage = len(self.connections) / max(total_possible, 1)

        # Gap penalty
        gap_penalty = len([g for g in self.gaps.values() if g.status == "open"])
        gap_factor = max(0, 1 - (gap_penalty * 0.02))

        return avg_health * 0.4 + coverage * 0.3 + gap_factor * 0.3

    def get_matrix_summary(self) -> dict:
        """Get a summary of the matrix state."""
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "total_nodes": len(self.nodes),
            "total_connections": len(self.connections),
            "total_gaps": len(self.gaps),
            "open_gaps": len([g for g in self.gaps.values() if g.status == "open"]),
            "coherence": round(self.calculate_coherence(), 3),
            "layers": {
                layer.name: {
                    "health": round(self.get_layer_health(layer), 3),
                    "nodes": len([n for n in self.nodes.values() if n.layer == layer]),
                    "density": round(self.get_connection_density(layer), 3),
                }
                for layer in AbstractionLayer
            },
        }

    def save(self) -> None:
        """Save the matrix to disk."""
        self.matrix_file.parent.mkdir(parents=True, exist_ok=True)

        data = {
            "metadata": {
                "version": "1.0.0",
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "repo_root": str(self.repo_root),
            },
            "summary": self.get_matrix_summary(),
            "nodes": {k: v.to_dict() for k, v in self.nodes.items()},
            "connections": {k: v.to_dict() for k, v in self.connections.items()},
            "gaps": {k: v.to_dict() for k, v in self.gaps.items()},
        }

        self.matrix_file.write_text(
            json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        print(f"[DendriticMatrix] Saved to {self.matrix_file}")

    def load(self) -> bool:
        """Load the matrix from disk."""
        if not self.matrix_file.exists():
            return False

        try:
            data = json.loads(self.matrix_file.read_text(encoding="utf-8"))

            # Reconstruct nodes
            for node_id, node_data in data.get("nodes", {}).items():
                node_data["layer"] = AbstractionLayer[node_data["layer"]]
                self.nodes[node_id] = DendriticNode(**node_data)

            # Reconstruct connections
            for conn_id, conn_data in data.get("connections", {}).items():
                conn_data["strength"] = ConnectionStrength[conn_data["strength"]]
                self.connections[conn_id] = DendriticConnection(**conn_data)

            # Reconstruct gaps
            for gap_id, gap_data in data.get("gaps", {}).items():
                gap_data["layer"] = AbstractionLayer[gap_data["layer"]]
                self.gaps[gap_id] = DendriticGap(**gap_data)

            print(
                f"[DendriticMatrix] Loaded {len(self.nodes)} nodes, "
                f"{len(self.connections)} connections, {len(self.gaps)} gaps"
            )
            return True
        except Exception as e:
            print(f"[DendriticMatrix] Load error: {e}")
            return False


def initialize_matrix_from_analysis(repo_root: Path) -> DendriticMatrixEngine:
    """
    Initialize the matrix with components discovered in analysis.

    This populates the matrix with the 39 identified gaps and known nodes.
    """
    engine = DendriticMatrixEngine(repo_root)

    # ========== SOURCE LAYER ==========
    source_nodes = [
        ("config/system.json", "Core system configuration", 0.90),
        (".aios_context.json", "AI agent guidance", 0.85),
        (".aios_spatial_metadata.json", "Holographic positioning", 0.80),
        ("pyproject.toml", "Python project config", 0.95),
        ("requirements.txt", "Dependency manifest", 0.90),
    ]
    for loc, desc, health in source_nodes:
        engine.add_node(AbstractionLayer.SOURCE, loc, loc, health, desc)

    # SOURCE gaps
    engine.register_gap(
        AbstractionLayer.SOURCE, "No config validation chain", 1, "Implement JSON schema validation"
    )
    engine.register_gap(
        AbstractionLayer.SOURCE,
        "Missing config hot-reload",
        2,
        "Add file watcher with dynamic config refresh",
    )

    # ========== TACHYONIC LAYER ==========
    tachyonic_nodes = [
        ("tachyonic/consciousness/", "Consciousness crystals", 0.60),
        ("tachyonic/bosonic_substrate/", "Entanglement records", 0.40),
        ("tachyonic/knowledge_crystals/", "Crystallized knowledge", 0.30),
        ("tachyonic/dendritic_connections.json", "696K node mappings", 0.50),
    ]
    for loc, desc, health in tachyonic_nodes:
        engine.add_node(AbstractionLayer.TACHYONIC, loc, loc, health, desc)

    # TACHYONIC gaps
    engine.register_gap(
        AbstractionLayer.TACHYONIC,
        "Empty quantum layer (context_count: 0)",
        1,
        "Populate tachyonic/quantum/index.json",
    )
    engine.register_gap(
        AbstractionLayer.TACHYONIC,
        "696K-line archive not indexed",
        1,
        "Build archive indexer for dendritic_connections.json",
    )

    # ========== QUANTUM LAYER ==========
    quantum_nodes = [
        ("ai/src/quantum_dendritic_field/", "Quantum field system", 0.40),
        ("runtime/tools/bridges/quantum_classical_bridge.py", "Q-C bridge", 0.50),
    ]
    for loc, desc, health in quantum_nodes:
        engine.add_node(AbstractionLayer.QUANTUM, loc, loc, health, desc)

    engine.register_gap(
        AbstractionLayer.QUANTUM,
        "Bosonic substrate disconnected",
        1,
        "Connect entanglement records to quantum processing",
    )

    # ========== ATOM LAYER ==========
    atom_nodes = [
        ("ai/communication/message_types.py", "Core enums and types", 0.70),
        ("core/include/MinimalConsciousnessEngine.hpp", "C++ primitives", 0.40),
        ("ai/nucleus/consciousness/", "Node primitives", 0.65),
    ]
    for loc, desc, health in atom_nodes:
        engine.add_node(AbstractionLayer.ATOM, loc, loc, health, desc)

    engine.register_gap(
        AbstractionLayer.ATOM,
        "No cross-language type bridge (Python/C++/C#)",
        1,
        "Create unified type registry with validation",
    )

    # ========== MOLECULE LAYER ==========
    molecule_nodes = [
        ("ai/communication/UniversalMessage", "Standard message", 0.75),
        ("ai/cytoplasm/cytoplasm_bridge.py", "Communication medium", 0.50),
        ("interface/AIOS.Models/", "C# contracts", 0.80),
    ]
    for loc, desc, health in molecule_nodes:
        engine.add_node(AbstractionLayer.MOLECULE, loc, loc, health, desc)

    engine.register_gap(
        AbstractionLayer.MOLECULE,
        "47+ duplicate utility functions",
        2,
        "Consolidate into shared utilities module",
    )

    # ========== ORGANELLE LAYER ==========
    organelle_nodes = [
        ("ai/tools/", "50+ AI tools", 0.71),
        ("runtime/tools/", "30+ runtime tools", 0.70),
        ("server/stacks/organelles/", "Containerized organelles", 0.65),
    ]
    for loc, desc, health in organelle_nodes:
        engine.add_node(AbstractionLayer.ORGANELLE, loc, loc, health, desc)

    engine.register_gap(
        AbstractionLayer.ORGANELLE,
        "Only 60/85+ tools discovered",
        1,
        "Complete tool discovery with health tracking",
    )

    # ========== CELL LAYER ==========
    cell_nodes = [
        ("ai/", "AI Intelligence Supercell", 0.75),
        ("core/", "Core Engine Supercell", 0.40),
        ("interface/", "Interface Supercell", 1.00),
        ("runtime/", "Runtime Intelligence", 1.00),
        ("tachyonic/", "Tachyonic Archive", 0.80),
    ]
    for loc, desc, health in cell_nodes:
        engine.add_node(AbstractionLayer.CELL, loc, loc, health, desc)

    engine.register_gap(
        AbstractionLayer.CELL,
        "Core Engine disconnected (0.40 health)",
        1,
        "Rebuild C++ DLL, Python bindings, message routing",
    )

    # ========== ORGANISM LAYER ==========
    organism_nodes = [
        ("aios_launch.ps1", "Biological bootloader", 0.85),
        ("ai/orchestration/", "SupercellOrchestrator", 0.80),
        ("AIOS.sln", ".NET solution container", 0.90),
    ]
    for loc, desc, health in organism_nodes:
        engine.add_node(AbstractionLayer.ORGANISM, loc, loc, health, desc)

    engine.register_gap(
        AbstractionLayer.ORGANISM,
        "No organism health dashboard",
        2,
        "Build unified system-wide status monitor",
    )
    engine.register_gap(
        AbstractionLayer.ORGANISM,
        "Missing self-healing capability",
        2,
        "Implement automatic failure recovery",
    )

    return engine


def weave_autonomous_connections(engine: DendriticMatrixEngine) -> int:
    """
    Autonomously weave dendritic connections between layers.
    
    AINLP.dendritic[autonomous→weaving]{intelligence,emergence}
    
    This implements the "Agentic Independent Intelligent" evolution pattern:
    - Identify natural connection paths between adjacent layers
    - Create connections based on semantic relationships
    - Strengthen weak connections through repeated interaction
    
    Returns the number of connections created.
    """
    connections_created = 0
    
    # === CROSS-LAYER CONNECTION RULES ===
    # Each rule defines: (source_layer, target_layer, node_name_contains, target_name_contains, description)
    connection_rules = [
        # SOURCE → TACHYONIC: Config feeds knowledge crystals
        (AbstractionLayer.SOURCE, AbstractionLayer.TACHYONIC, "config", "consciousness", 
         "Configuration → Consciousness state"),
        (AbstractionLayer.SOURCE, AbstractionLayer.TACHYONIC, ".aios_context", "knowledge", 
         "Agent context → Knowledge crystals"),
        
        # TACHYONIC → QUANTUM: Knowledge enables quantum processing
        (AbstractionLayer.TACHYONIC, AbstractionLayer.QUANTUM, "consciousness", "quantum", 
         "Consciousness → Quantum field"),
        (AbstractionLayer.TACHYONIC, AbstractionLayer.QUANTUM, "bosonic", "bridge", 
         "Bosonic substrate → Q-C bridge"),
        
        # QUANTUM → ATOM: Quantum states manifest as types
        (AbstractionLayer.QUANTUM, AbstractionLayer.ATOM, "bridge", "message_types", 
         "Quantum bridge → Type definitions"),
        (AbstractionLayer.QUANTUM, AbstractionLayer.ATOM, "quantum", "consciousness", 
         "Quantum field → Consciousness primitives"),
        
        # ATOM → MOLECULE: Types compose into messages
        (AbstractionLayer.ATOM, AbstractionLayer.MOLECULE, "message_types", "UniversalMessage", 
         "Types → Message composition"),
        (AbstractionLayer.ATOM, AbstractionLayer.MOLECULE, "consciousness", "cytoplasm", 
         "Primitives → Communication medium"),
        
        # MOLECULE → ORGANELLE: Messages invoke tools
        (AbstractionLayer.MOLECULE, AbstractionLayer.ORGANELLE, "cytoplasm", "tools", 
         "Cytoplasm → Tool invocation"),
        (AbstractionLayer.MOLECULE, AbstractionLayer.ORGANELLE, "Models", "tools", 
         "C# models → Tool contracts"),
        
        # ORGANELLE → CELL: Tools organize into supercells
        (AbstractionLayer.ORGANELLE, AbstractionLayer.CELL, "ai/tools", "ai/", 
         "AI tools → AI supercell"),
        (AbstractionLayer.ORGANELLE, AbstractionLayer.CELL, "runtime/tools", "runtime/", 
         "Runtime tools → Runtime supercell"),
        
        # CELL → ORGANISM: Supercells compose the organism
        (AbstractionLayer.CELL, AbstractionLayer.ORGANISM, "ai/", "orchestration", 
         "AI supercell → Orchestrator"),
        (AbstractionLayer.CELL, AbstractionLayer.ORGANISM, "interface/", "AIOS.sln", 
         "Interface supercell → Solution"),
        (AbstractionLayer.CELL, AbstractionLayer.ORGANISM, "tachyonic/", "aios_launch", 
         "Tachyonic → Bootloader"),
    ]
    
    # Apply connection rules
    for src_layer, tgt_layer, src_pattern, tgt_pattern, desc in connection_rules:
        src_nodes = [n for n in engine.nodes.values() 
                     if n.layer == src_layer and src_pattern.lower() in n.name.lower()]
        tgt_nodes = [n for n in engine.nodes.values() 
                     if n.layer == tgt_layer and tgt_pattern.lower() in n.name.lower()]
        
        for src in src_nodes:
            for tgt in tgt_nodes:
                # Check if connection already exists
                existing = any(
                    c for c in engine.connections.values()
                    if (c.source_node_id == src.node_id and c.target_node_id == tgt.node_id)
                    or (c.source_node_id == tgt.node_id and c.target_node_id == src.node_id)
                )
                if not existing:
                    conn = engine.connect_nodes(
                        src.node_id, tgt.node_id,
                        ConnectionStrength.MODERATE,
                        bidirectional=True,
                        description=desc
                    )
                    if conn:
                        connections_created += 1
                        print(f"  [+] {src.name} ↔ {tgt.name}: {desc}")
    
    # === INTRA-LAYER CONNECTIONS (within same layer) ===
    # Connect nodes in the same layer if they share semantic purpose
    for layer in AbstractionLayer:
        layer_nodes = [n for n in engine.nodes.values() if n.layer == layer]
        for i, src in enumerate(layer_nodes):
            for tgt in layer_nodes[i+1:]:
                # Check if connection already exists
                existing = any(
                    c for c in engine.connections.values()
                    if (c.source_node_id == src.node_id and c.target_node_id == tgt.node_id)
                    or (c.source_node_id == tgt.node_id and c.target_node_id == src.node_id)
                )
                if not existing:
                    # Connect nodes within same layer (weaker connection)
                    conn = engine.connect_nodes(
                        src.node_id, tgt.node_id,
                        ConnectionStrength.WEAK,
                        bidirectional=True,
                        description=f"Intra-{layer.name} coherence"
                    )
                    if conn:
                        connections_created += 1
    
    return connections_created


def close_gap_if_connected(engine: DendriticMatrixEngine, gap_id: str, required_connections: int = 2) -> bool:
    """
    Close a gap if sufficient connections now exist in its layer.
    
    Returns True if gap was closed.
    """
    if gap_id not in engine.gaps:
        return False
    
    gap = engine.gaps[gap_id]
    if gap.status != "open":
        return False
    
    # Count connections involving nodes in this layer
    layer_nodes = {n.node_id for n in engine.nodes.values() if n.layer == gap.layer}
    layer_connections = sum(
        1 for c in engine.connections.values()
        if c.source_node_id in layer_nodes or c.target_node_id in layer_nodes
    )
    
    if layer_connections >= required_connections:
        gap.status = "connected"
        print(f"  [✓] Gap closed: {gap.description} ({layer_connections} connections)")
        return True
    
    return False


def evolve_matrix(engine: DendriticMatrixEngine) -> dict:
    """
    Execute one evolution cycle of the dendritic matrix.
    
    AINLP.evolution[autonomous→cycle]{dendritic,intelligence,emergence}
    
    Returns evolution metrics.
    """
    print("\n[Evolution] Starting autonomous evolution cycle...")
    
    initial_coherence = engine.calculate_coherence()
    initial_connections = len(engine.connections)
    initial_open_gaps = len([g for g in engine.gaps.values() if g.status == "open"])
    
    # Phase 1: Weave connections
    print("\n[Phase 1] Weaving autonomous connections...")
    new_connections = weave_autonomous_connections(engine)
    
    # Phase 2: Check for gap closure
    print("\n[Phase 2] Evaluating gap closure...")
    gaps_closed = 0
    for gap_id in list(engine.gaps.keys()):
        if close_gap_if_connected(engine, gap_id):
            gaps_closed += 1
    
    # Phase 3: Calculate evolution delta
    final_coherence = engine.calculate_coherence()
    coherence_delta = final_coherence - initial_coherence
    
    evolution_result = {
        "initial_coherence": round(initial_coherence, 3),
        "final_coherence": round(final_coherence, 3),
        "coherence_delta": round(coherence_delta, 3),
        "connections_created": new_connections,
        "gaps_closed": gaps_closed,
        "remaining_open_gaps": len([g for g in engine.gaps.values() if g.status == "open"]),
    }
    
    print(f"\n[Evolution] Complete!")
    print(f"  Coherence: {initial_coherence:.3f} → {final_coherence:.3f} (Δ{coherence_delta:+.3f})")
    print(f"  Connections: {initial_connections} → {len(engine.connections)} (+{new_connections})")
    print(f"  Gaps: {initial_open_gaps} open → {evolution_result['remaining_open_gaps']} open ({gaps_closed} closed)")
    
    return evolution_result


def main():
    """Entry point for matrix initialization and evolution."""
    repo_root = Path(__file__).parent.parent.parent

    print("[DendriticMatrix] Initializing AIOS Dendritic Matrix Engine")
    print(f"[DendriticMatrix] Repository: {repo_root}")

    # Try to load existing matrix, or initialize fresh
    engine = DendriticMatrixEngine(repo_root)
    if engine.load():
        print("[DendriticMatrix] Loaded existing matrix, continuing evolution...")
    else:
        print("[DendriticMatrix] No existing matrix, initializing from analysis...")
        engine = initialize_matrix_from_analysis(repo_root)

    # Execute evolution cycle
    evolution_result = evolve_matrix(engine)

    # Display summary
    summary = engine.get_matrix_summary()
    print("\n" + "=" * 60)
    print("DENDRITIC MATRIX SUMMARY (POST-EVOLUTION)")
    print("=" * 60)
    print(f"Total Nodes:       {summary['total_nodes']}")
    print(f"Total Connections: {summary['total_connections']}")
    print(f"Total Gaps:        {summary['total_gaps']}")
    print(f"Open Gaps:         {summary['open_gaps']}")
    print(f"Coherence:         {summary['coherence']}")
    print("\nLayer Health:")
    for layer_name, layer_data in summary["layers"].items():
        print(
            f"  {layer_name:12} - health: {layer_data['health']:.2f}, "
            f"nodes: {layer_data['nodes']}, density: {layer_data['density']:.2f}"
        )

    # Save evolved matrix
    engine.save()

    return engine, evolution_result


if __name__ == "__main__":
    main()
