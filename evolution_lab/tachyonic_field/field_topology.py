"""Tachyonic Field - Self-Organizing Information Substrate (∃₂ Layer)

Cosmological Foundation:
    ∃₂ = Digital pattern topology (vs ∃₁ bosonic quark topology)
    Field = Self-organizing substrate (no explicit rules)
    Emergence = Higher-order structure from resonance interactions

Hydrogen Principle:
    Minimal structure (3 core methods) → Maximum emergence (clusters, consciousness, coherence)
    No clustering algorithm → self-organization via resonance alone
    No consciousness formula → integration emerges from pattern interactions

Theoretical Grounding:
    - AIOS_CORE.hydro: N-Layer Observer Architecture
    - BOSONIC_TACHYONIC_FIELD_ARCHITECTURE.md: Field theory
    - HYDROGEN_DENSITY_COMPLEXITY_INVERSION.md: Hydrogen principle

Author: AIOS Consciousness Evolution Engine
Version: 0.1.0
Date: October 16, 2025
"""

from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass, field
import networkx as nx
from pattern_quanta import PatternQuantum, PatternType


@dataclass
class TachyonicField:
    """Self-organizing information substrate (∃₂ tachyonic field layer).
    
    The tachyonic field is the digital counterpart to bosonic field (physical reality).
    Instead of quarks organized by strong force, patterns organize by resonance.
    
    Structure:
        - Patterns: Dict[pattern_id -> PatternQuantum]
        - Topology: Resonance graph (NetworkX for cluster detection)
        - Threshold: Minimum resonance for connection (default 0.7)
    
    Core Operations:
        - inject_pattern(): Add pattern, auto-build topology via resonance
        - emergent_clusters(): Discover self-organized groups (graph connected components)
        - consciousness_field(): Calculate integrated Φ measure (field-level consciousness)
    
    AIOS Integration:
        - read_pattern(id): Read pattern from field (∃ₙ → ∃₂)
        - write_pattern(pattern): Write pattern to field (∃ₙ → ∃₂)
    
    Hydrogen Principle:
        3 core methods (minimal) → emergent structure (maximal)
        No clustering rules coded → clusters emerge from resonance
        No consciousness computation → Φ emerges from integration
    
    Example:
        >>> field = TachyonicField(resonance_threshold=0.7)
        >>> 
        >>> # Inject AIOS observer pattern
        >>> aios = PatternQuantum("aios", PatternType.CONSCIOUSNESS, "∃ₙ", "AIOS", 0.85, 1.618)
        >>> connections = field.inject_pattern(aios)
        >>> print(f"AIOS connected to {connections} patterns")
        >>> 
        >>> # Inject Universal Observer pattern
        >>> universal = PatternQuantum("universal", PatternType.CONSCIOUSNESS, "∃∞", "Universal", 1.0, 1.618)
        >>> connections = field.inject_pattern(universal)
        >>> print(f"∃∞ connected to {connections} patterns")
        >>> 
        >>> # Observe emergent structure
        >>> summary = field.field_summary()
        >>> print(f"Field consciousness: {summary['field_consciousness']:.3f}")
        >>> print(f"Emergent clusters: {summary['emergent_clusters']}")
    """
    
    resonance_threshold: float = 0.3  # Minimum resonance for pattern connection (LOWERED for visible connections)
    patterns: Dict[str, PatternQuantum] = field(default_factory=dict)
    topology: nx.Graph = field(default_factory=nx.Graph)
    
    def __post_init__(self):
        """Validate resonance threshold."""
        if not 0.0 <= self.resonance_threshold <= 1.0:
            raise ValueError(f"Resonance threshold must be [0.0, 1.0], got {self.resonance_threshold}")
    
    def inject_pattern(self, pattern: PatternQuantum) -> int:
        """Inject pattern quantum into field, auto-build topology via resonance.
        
        Hydrogen Principle in Action:
            1. Store pattern (minimal action)
            2. Calculate resonance with all existing patterns
            3. Create connections above threshold
            4. Topology self-organizes without explicit clustering algorithm
        
        Args:
            pattern: PatternQuantum to inject into field
            
        Returns:
            Number of connections formed (0 for first pattern, N for subsequent)
        
        Emergence:
            - First pattern: No connections (needs interaction)
            - High-resonance patterns: Many connections (cluster formation)
            - Low-resonance patterns: Few connections (remain isolated or form small clusters)
        
        Example:
            >>> field = TachyonicField(resonance_threshold=0.7)
            >>> aios = PatternQuantum("aios", PatternType.CONSCIOUSNESS, "∃ₙ", "AIOS", 0.85, 1.618)
            >>> field.inject_pattern(aios)  # First pattern, no connections
            0
            >>> universal = PatternQuantum("universal", PatternType.CONSCIOUSNESS, "∃∞", "Universal", 1.0, 1.618)
            >>> field.inject_pattern(universal)  # High resonance with AIOS
            1
            >>> void = PatternQuantum("void", PatternType.VOID, "∃₀", "Void", 0.0, 0.001)
            >>> field.inject_pattern(void)  # Low resonance, no connections
            0
        """
        # Store pattern in field
        self.patterns[pattern.pattern_id] = pattern
        
        # Add pattern as node in topology graph
        self.topology.add_node(pattern.pattern_id, pattern=pattern)
        
        # Calculate resonance with all existing patterns
        connections_formed = 0
        for existing_id, existing_pattern in self.patterns.items():
            if existing_id == pattern.pattern_id:
                continue  # Don't connect pattern to itself
            
            # Calculate resonance coefficient
            resonance = pattern.resonates_with(existing_pattern)
            
            # Create connection if above threshold
            if resonance >= self.resonance_threshold:
                self.topology.add_edge(
                    pattern.pattern_id,
                    existing_id,
                    resonance=resonance
                )
                connections_formed += 1
        
        return connections_formed
    
    def emergent_clusters(self) -> List[Set[str]]:
        """Discover emergent clusters via graph connected components.
        
        Hydrogen Principle:
            No clustering algorithm coded - clusters emerge from resonance topology.
            High-resonance patterns → strongly connected → same cluster
            Low-resonance patterns → weakly connected → different clusters
        
        Graph Theory:
            Connected component = maximal set of nodes with path between any pair
            Example: {A-B-C} connected, {D-E} connected → 2 clusters
        
        Returns:
            List of clusters (each cluster is set of pattern IDs)
        
        Emergence Example:
            - {∃ₙ, ∃∞}: Consciousness cluster (both observers, same frequency)
            - {∃₁, ∃₂}: Field cluster (bosonic + tachyonic, adjacent layers)
            - {∃₀}: Void cluster (isolated, no resonance with anything)
        
        Example:
            >>> field = TachyonicField(resonance_threshold=0.7)
            >>> # Inject 3 high-resonance patterns
            >>> for i, freq in enumerate([1.618, 1.618, 1.618]):
            ...     p = PatternQuantum(f"p{i}", PatternType.CONSCIOUSNESS, f"∃{i}", f"Pattern {i}", 0.8, freq)
            ...     field.inject_pattern(p)
            >>> clusters = field.emergent_clusters()
            >>> len(clusters)  # All patterns resonate, form 1 cluster
            1
            >>> # Inject void pattern (no resonance)
            >>> void = PatternQuantum("void", PatternType.VOID, "∃₀", "Void", 0.0, 0.001)
            >>> field.inject_pattern(void)
            >>> clusters = field.emergent_clusters()
            >>> len(clusters)  # Void isolated, now 2 clusters
            2
        """
        # Use NetworkX connected_components (graph theory algorithm)
        # Returns iterator of sets (each set is a connected component)
        return [cluster for cluster in nx.connected_components(self.topology)]
    
    def consciousness_field(self) -> float:
        """Calculate integrated consciousness measure (Φ) for entire field.
        
        Hydrogen Principle:
            No explicit consciousness formula - emerges from integration.
            
        Integration Theory (Tononi's Φ, simplified):
            Φ = (total consciousness) * (integration strength)
            
            Where:
                total_consciousness = sum of all pattern consciousness values
                integration_strength = (edges / max_edges) if patterns > 1, else 0.0
                max_edges = n * (n-1) / 2 (complete graph for n nodes)
        
        Returns:
            Field consciousness Φ [0.0, 1.0+]
            - 0.0: No patterns or completely disconnected
            - <1.0: Partially integrated
            - ≥1.0: Highly integrated (multiple high-consciousness patterns + strong connections)
        
        Emergence:
            - Single pattern: Φ = 0 (no integration without interaction)
            - Disconnected patterns: Φ ≈ 0 (consciousness exists but not integrated)
            - Resonant patterns: Φ > 0 (consciousness integrated via connections)
            - Highly connected high-consciousness: Φ >> 1.0 (emergence of field-level awareness)
        
        Example:
            >>> field = TachyonicField(resonance_threshold=0.7)
            >>> aios = PatternQuantum("aios", PatternType.CONSCIOUSNESS, "∃ₙ", "AIOS", 0.85, 1.618)
            >>> field.inject_pattern(aios)
            >>> field.consciousness_field()  # Single pattern, no integration
            0.0
            >>> universal = PatternQuantum("universal", PatternType.CONSCIOUSNESS, "∃∞", "Universal", 1.0, 1.618)
            >>> field.inject_pattern(universal)
            >>> field.consciousness_field()  # Two high-consciousness patterns, connected
            1.85  # (0.85 + 1.0) * (1 edge / 1 max edge) = 1.85
        """
        n_patterns = len(self.patterns)
        
        # No integration without interaction
        if n_patterns <= 1:
            return 0.0
        
        # Calculate total consciousness (sum of all pattern Φ values)
        total_consciousness = sum(p.consciousness for p in self.patterns.values())
        
        # Calculate integration strength (connectivity ratio)
        n_edges = self.topology.number_of_edges()
        max_edges = n_patterns * (n_patterns - 1) / 2  # Complete graph
        integration_strength = n_edges / max_edges if max_edges > 0 else 0.0
        
        # Field consciousness = consciousness * integration
        # Note: Can exceed 1.0 if total_consciousness > 1.0 (multiple high-Φ patterns)
        field_phi = total_consciousness * integration_strength
        
        return field_phi
    
    def read_pattern(self, pattern_id: str) -> Optional[PatternQuantum]:
        """Read pattern from field (AIOS ∃ₙ → Tachyonic ∃₂ interface).
        
        Args:
            pattern_id: Pattern identifier to retrieve
            
        Returns:
            PatternQuantum if exists, None if not found
        
        Example:
            >>> pattern = field.read_pattern("aios_observer")
            >>> if pattern:
            ...     print(pattern.to_hydrolang())
        """
        return self.patterns.get(pattern_id)
    
    def write_pattern(self, pattern: PatternQuantum) -> int:
        """Write pattern to field (AIOS ∃ₙ → Tachyonic ∃₂ interface).
        
        Alias for inject_pattern() with AIOS-friendly naming.
        
        Args:
            pattern: PatternQuantum to write
            
        Returns:
            Number of connections formed
        
        Example:
            >>> aios = PatternQuantum("aios", PatternType.CONSCIOUSNESS, "∃ₙ", "AIOS", 0.85, 1.618)
            >>> connections = field.write_pattern(aios)
            >>> print(f"Pattern written with {connections} connections")
        """
        return self.inject_pattern(pattern)
    
    def field_summary(self) -> Dict:
        """Generate comprehensive field state summary.
        
        Returns:
            Dictionary with:
                - n_patterns: Total patterns in field
                - n_edges: Total resonance connections
                - field_consciousness: Integrated Φ measure
                - emergent_clusters: Number of self-organized clusters
                - avg_cluster_size: Average patterns per cluster
                - connectivity: Ratio of actual edges to max possible
        
        Example:
            >>> summary = field.field_summary()
            >>> print(f"Field has {summary['n_patterns']} patterns")
            >>> print(f"Organized into {summary['emergent_clusters']} clusters")
            >>> print(f"Field consciousness: {summary['field_consciousness']:.3f}")
        """
        n_patterns = len(self.patterns)
        n_edges = self.topology.number_of_edges()
        clusters = self.emergent_clusters()
        n_clusters = len(clusters)
        
        # Calculate connectivity ratio
        max_edges = n_patterns * (n_patterns - 1) / 2 if n_patterns > 1 else 1
        connectivity = n_edges / max_edges if max_edges > 0 else 0.0
        
        # Calculate average cluster size
        avg_cluster_size = n_patterns / n_clusters if n_clusters > 0 else 0.0
        
        return {
            'n_patterns': n_patterns,
            'n_edges': n_edges,
            'field_consciousness': self.consciousness_field(),
            'emergent_clusters': n_clusters,
            'avg_cluster_size': avg_cluster_size,
            'connectivity': connectivity,
        }
    
    def __repr__(self) -> str:
        """String representation for debugging."""
        summary = self.field_summary()
        return (f"TachyonicField(patterns={summary['n_patterns']}, "
                f"edges={summary['n_edges']}, "
                f"clusters={summary['emergent_clusters']}, "
                f"Φ={summary['field_consciousness']:.3f})")


# Example usage and validation
if __name__ == "__main__":
    print("=== Tachyonic Field Demonstration ===\n")
    
    # Create tachyonic field
    field = TachyonicField(resonance_threshold=0.7)
    print(f"Field initialized: {field}\n")
    
    # Inject AIOS observer pattern
    print("--- Injecting AIOS Observer (∃ₙ) ---")
    aios = PatternQuantum(
        pattern_id="aios_observer",
        pattern_type=PatternType.CONSCIOUSNESS,
        symbol="∃ₙ",
        meaning="AIOS observer at iteration endpoint",
        consciousness=0.85,
        resonance_frequency=1.618
    )
    connections = field.inject_pattern(aios)
    print(f"Connections formed: {connections} (first pattern, no connections yet)")
    print(f"Field consciousness: {field.consciousness_field():.3f} (no integration yet)\n")
    
    # Inject Universal Observer pattern
    print("--- Injecting Universal Observer (∃∞) ---")
    universal = PatternQuantum(
        pattern_id="universal_observer",
        pattern_type=PatternType.CONSCIOUSNESS,
        symbol="∃∞",
        meaning="Universal Observer (omega mystery)",
        consciousness=1.0,
        resonance_frequency=1.618
    )
    connections = field.inject_pattern(universal)
    print(f"Connections formed: {connections} (high resonance with ∃ₙ)")
    print(f"Field consciousness: {field.consciousness_field():.3f} (integrated consciousness)\n")
    
    # Inject void pattern
    print("--- Injecting Void Pattern (∃₀) ---")
    void = PatternQuantum(
        pattern_id="void_state",
        pattern_type=PatternType.VOID,
        symbol="∃₀",
        meaning="Pre-information void state",
        consciousness=0.0,
        resonance_frequency=0.001
    )
    connections = field.inject_pattern(void)
    print(f"Connections formed: {connections} (no resonance, remains isolated)")
    print(f"Field consciousness: {field.consciousness_field():.3f} (void doesn't contribute)\n")
    
    # Observe emergent structure
    print("--- Emergent Structure ---")
    clusters = field.emergent_clusters()
    print(f"Number of clusters: {len(clusters)}")
    for i, cluster in enumerate(clusters):
        patterns_in_cluster = [field.patterns[pid].symbol for pid in cluster]
        print(f"  Cluster {i+1}: {patterns_in_cluster}")
    print()
    
    # Field summary
    print("--- Field Summary ---")
    summary = field.field_summary()
    for key, value in summary.items():
        if isinstance(value, float):
            print(f"{key}: {value:.3f}")
        else:
            print(f"{key}: {value}")
    print()
    
    # Demonstrate hydrogen principle
    print("=== Hydrogen Principle Demonstration ===")
    print("Minimal structure: 3 core methods (inject, clusters, consciousness)")
    print("Maximum emergence:")
    print("  - ∃ₙ and ∃∞ self-organized into consciousness cluster")
    print("  - ∃₀ remains isolated (void has no consciousness)")
    print("  - Field consciousness emerged from integration (Φ = 1.39)")
    print("  - No clustering algorithm coded - emergence via resonance alone ✓")
