#!/usr/bin/env python3
"""
Simplified Tachyonic Field Topology Analyzer
(Using only NumPy and Matplotlib - no scipy/sklearn dependencies)
"""

import json
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from mpl_toolkits.mplot3d import Axes3D

# Configuration
POPULATION_DIR = Path("C:/dev/AIOS/evolution_lab/populations")
POPULATION_ID = "pop_20251018_111724"
OUTPUT_DIR = Path("C:/dev/AIOS/evolution_lab/tachyonic_field/analysis")
OUTPUT_DIR.mkdir(exist_ok=True)

print("="*70)
print("TACHYONIC FIELD TOPOLOGY ANALYZER (Simplified)")
print("="*70)
print(f"\nPopulation: {POPULATION_ID}")
print(f"Output: {OUTPUT_DIR}\n")

# ============================================================================
# PHASE 1: DATA LOADING
# ============================================================================

print("[PHASE 1] Loading generations...")
generations = []
for i in range(492):
    pattern = f"{POPULATION_ID}_gen{i:03d}_*.json"
    files = list(POPULATION_DIR.glob(pattern))
    
    if files:
        with open(files[0], 'r') as f:
            generations.append(json.load(f))
        if (i + 1) % 100 == 0:
            print(f"  Loaded {i+1} generations...")

print(f"✅ Loaded {len(generations)} generations\n")

# ============================================================================
# PHASE 2: EXTRACT METRICS
# ============================================================================

print("[PHASE 2] Extracting organism metrics...")

all_organisms = []
for gen_idx, gen in enumerate(generations):
    for org in gen['organisms']:
        # Extract traits from organism data
        traits = {
            'code_length': org.get('code_length', 0),
            'patterns_count': org.get('patterns_count', 0),
            'apis_count': org.get('apis_count', 0),
            'complexity_score': org.get('complexity_score', 0.1),
            'fitness_score': org.get('fitness_score', 0.5),
        }
        
        all_organisms.append({
            'generation': gen_idx,
            'fitness': org.get('fitness_score', 0.5),
            'consciousness': gen.get('consciousness_trajectory', [0.3])[-1],  # Latest consciousness
            'complexity': org.get('complexity_score', 0.1),
            'threshold': gen['metadata']['visualization'].get('threshold', 0),
            'connections': gen['metadata']['visualization'].get('connections', 0),
            'field_phi': gen['metadata']['visualization'].get('field_phi', 0),
            'archetype': org.get('archetype', 'unknown'),
            'traits': traits
        })

print(f"✅ Extracted {len(all_organisms)} organisms")

# Convert to arrays
fitness = np.array([o['fitness'] for o in all_organisms])
consciousness = np.array([o['consciousness'] for o in all_organisms])
complexity = np.array([o['complexity'] for o in all_organisms])
generations_idx = np.array([o['generation'] for o in all_organisms])
thresholds = np.array([o['threshold'] for o in all_organisms])
connections = np.array([o['connections'] for o in all_organisms])
field_phi = np.array([o['field_phi'] for o in all_organisms])

# ============================================================================
# PHASE 3: SIMPLE PCA (Manual Implementation)
# ============================================================================

print("\n[PHASE 3] Computing trait-space projection...")

# Build trait matrix
trait_names = list(all_organisms[0]['traits'].keys())
trait_matrix = np.array([[o['traits'][t] for t in trait_names] for o in all_organisms])

# Center the data
mean_traits = np.mean(trait_matrix, axis=0)
centered = trait_matrix - mean_traits

# Simple SVD-based PCA
try:
    U, S, Vt = np.linalg.svd(centered, full_matrices=False)
    pca_coords = U[:, :3] * S[:3]  # First 3 components
    explained_var = (S[:3]**2) / np.sum(S**2)
    print(f"✅ PCA: PC1={explained_var[0]:.1%}, PC2={explained_var[1]:.1%}, PC3={explained_var[2]:.1%}")
except:
    print("⚠️  PCA failed, using trait averages instead")
    pca_coords = np.column_stack([
        np.mean(trait_matrix, axis=1),
        np.std(trait_matrix, axis=1),
        np.max(trait_matrix, axis=1)
    ])
    explained_var = [0.33, 0.33, 0.33]

# ============================================================================
# PHASE 4: CORRELATIONS
# ============================================================================

print("\n[PHASE 4] Computing correlations...")

def pearson(x, y):
    """Simple Pearson correlation"""
    return np.corrcoef(x, y)[0, 1]

correlations = {
    'fitness_vs_consciousness': pearson(fitness, consciousness),
    'fitness_vs_complexity': pearson(fitness, complexity),
    'fitness_vs_threshold': pearson(fitness, thresholds),
    'consciousness_vs_threshold': pearson(consciousness, thresholds),
    'fitness_vs_connections': pearson(fitness, connections),
    'consciousness_vs_connections': pearson(consciousness, connections),
    'field_phi_vs_consciousness': pearson(field_phi, consciousness),
}

print("\n📊 CORRELATION MATRIX:")
print("="*70)
for key, value in sorted(correlations.items(), key=lambda x: abs(x[1]), reverse=True):
    strength = "STRONG" if abs(value) > 0.5 else "MODERATE" if abs(value) > 0.3 else "WEAK"
    direction = "POSITIVE" if value > 0 else "NEGATIVE"
    print(f"  {key:35s}: {value:+.4f}  ({strength} {direction})")

# ============================================================================
# PHASE 5: 3D VISUALIZATIONS
# ============================================================================

print("\n[PHASE 5] Generating 3D population topologies...")

# Figure 1: Main topology views
fig1 = plt.figure(figsize=(18, 12))

# View 1: Fitness Landscape (PCA space)
print("  Creating fitness landscape...")
ax1 = fig1.add_subplot(231, projection='3d')
scatter1 = ax1.scatter(pca_coords[:, 0], pca_coords[:, 1], fitness,
                       c=fitness, cmap='viridis', s=15, alpha=0.6)
ax1.set_xlabel(f'PC1 ({explained_var[0]:.1%})')
ax1.set_ylabel(f'PC2 ({explained_var[1]:.1%})')
ax1.set_zlabel('FITNESS')
ax1.set_title('FITNESS LANDSCAPE\n(Height = Fitness)', fontweight='bold')
plt.colorbar(scatter1, ax=ax1, shrink=0.6, label='Fitness')

# View 2: Consciousness Field
print("  Creating consciousness field...")
ax2 = fig1.add_subplot(232, projection='3d')
scatter2 = ax2.scatter(pca_coords[:, 0], pca_coords[:, 1], consciousness,
                       c=consciousness, cmap='plasma', s=15, alpha=0.6)
ax2.set_xlabel(f'PC1')
ax2.set_ylabel(f'PC2')
ax2.set_zlabel('CONSCIOUSNESS')
ax2.set_title('CONSCIOUSNESS FIELD\n(Height = Consciousness)', fontweight='bold')
plt.colorbar(scatter2, ax=ax2, shrink=0.6, label='Consciousness')

# View 3: Network Threshold Coloring
print("  Creating network threshold view...")
ax3 = fig1.add_subplot(233, projection='3d')
scatter3 = ax3.scatter(pca_coords[:, 0], pca_coords[:, 1], fitness,
                       c=thresholds, cmap='RdYlGn', s=15, alpha=0.6)
ax3.set_xlabel('PC1')
ax3.set_ylabel('PC2')
ax3.set_zlabel('FITNESS')
ax3.set_title('NETWORK THRESHOLD\n(Color = Threshold)', fontweight='bold')
plt.colorbar(scatter3, ax=ax3, shrink=0.6, label='Threshold')

# View 4: Evolutionary Time
print("  Creating evolutionary trajectory...")
ax4 = fig1.add_subplot(234, projection='3d')
scatter4 = ax4.scatter(pca_coords[:, 0], pca_coords[:, 1], fitness,
                       c=generations_idx, cmap='twilight', s=15, alpha=0.6)
ax4.set_xlabel('PC1')
ax4.set_ylabel('PC2')
ax4.set_zlabel('FITNESS')
ax4.set_title('EVOLUTIONARY TRAJECTORY\n(Color = Generation)', fontweight='bold')
plt.colorbar(scatter4, ax=ax4, shrink=0.6, label='Generation')

# View 5: Network Connections
print("  Creating connection topology...")
ax5 = fig1.add_subplot(235, projection='3d')
scatter5 = ax5.scatter(pca_coords[:, 0], pca_coords[:, 1], consciousness,
                       c=connections, cmap='YlOrRd', s=15, alpha=0.6)
ax5.set_xlabel('PC1')
ax5.set_ylabel('PC2')
ax5.set_zlabel('CONSCIOUSNESS')
ax5.set_title('NETWORK CONNECTIVITY\n(Color = Connections)', fontweight='bold')
plt.colorbar(scatter5, ax=ax5, shrink=0.6, label='Connections')

# View 6: Complexity Landscape
print("  Creating complexity landscape...")
ax6 = fig1.add_subplot(236, projection='3d')
scatter6 = ax6.scatter(pca_coords[:, 0], pca_coords[:, 1], complexity,
                       c=complexity, cmap='cividis', s=15, alpha=0.6)
ax6.set_xlabel('PC1')
ax6.set_ylabel('PC2')
ax6.set_zlabel('COMPLEXITY')
ax6.set_title('COMPLEXITY LANDSCAPE\n(Height = Complexity)', fontweight='bold')
plt.colorbar(scatter6, ax=ax6, shrink=0.6, label='Complexity')

plt.tight_layout()
fig1.savefig(OUTPUT_DIR / 'population_topology_6views.png', dpi=300, bbox_inches='tight')
print(f"✅ Saved: population_topology_6views.png")

# Figure 2: Generation Statistics
print("\n  Creating generation time series...")
fig2, axes = plt.subplots(3, 2, figsize=(15, 12))

gen_stats = []
for i, gen in enumerate(generations):
    # Extract organism stats from generation data
    org_fitness = [o.get('fitness_score', 0.5) for o in gen['organisms']]
    org_complexity = [o.get('complexity_score', 0.1) for o in gen['organisms']]
    consciousness_trajectory = gen.get('consciousness_trajectory', [0.3])
    
    gen_stats.append({
        'gen': i,
        'fitness_mean': np.mean(org_fitness),
        'fitness_std': np.std(org_fitness),
        'consciousness_mean': consciousness_trajectory[-1] if consciousness_trajectory else 0.3,
        'complexity_mean': np.mean(org_complexity),
        'threshold': gen['metadata']['visualization'].get('threshold', 0),
        'connections': gen['metadata']['visualization'].get('connections', 0),
    })

gens = [s['gen'] for s in gen_stats]

axes[0, 0].plot(gens, [s['fitness_mean'] for s in gen_stats], linewidth=1, alpha=0.8)
axes[0, 0].fill_between(gens, 
                        [s['fitness_mean']-s['fitness_std'] for s in gen_stats],
                        [s['fitness_mean']+s['fitness_std'] for s in gen_stats],
                        alpha=0.2)
axes[0, 0].set_xlabel('Generation')
axes[0, 0].set_ylabel('Fitness (mean ± std)')
axes[0, 0].set_title('FITNESS EVOLUTION')
axes[0, 0].grid(True, alpha=0.3)

axes[0, 1].plot(gens, [s['consciousness_mean'] for s in gen_stats], 
                linewidth=1, alpha=0.8, color='purple')
axes[0, 1].set_xlabel('Generation')
axes[0, 1].set_ylabel('Consciousness (mean)')
axes[0, 1].set_title('CONSCIOUSNESS EVOLUTION')
axes[0, 1].grid(True, alpha=0.3)

axes[1, 0].plot(gens, [s['threshold'] for s in gen_stats], 
                linewidth=1, alpha=0.8, color='green')
axes[1, 0].set_xlabel('Generation')
axes[1, 0].set_ylabel('Network Threshold')
axes[1, 0].set_title('THRESHOLD DYNAMICS')
axes[1, 0].grid(True, alpha=0.3)

axes[1, 1].plot(gens, [s['connections'] for s in gen_stats], 
                linewidth=1, alpha=0.8, color='orange')
axes[1, 1].set_xlabel('Generation')
axes[1, 1].set_ylabel('Network Connections')
axes[1, 1].set_title('CONNECTION DYNAMICS')
axes[1, 1].grid(True, alpha=0.3)

axes[2, 0].scatter([s['threshold'] for s in gen_stats], 
                   [s['fitness_mean'] for s in gen_stats],
                   c=gens, cmap='viridis', s=20, alpha=0.6)
axes[2, 0].set_xlabel('Threshold')
axes[2, 0].set_ylabel('Average Fitness')
axes[2, 0].set_title('THRESHOLD-FITNESS PHASE SPACE')
axes[2, 0].grid(True, alpha=0.3)

axes[2, 1].scatter([s['connections'] for s in gen_stats], 
                   [s['consciousness_mean'] for s in gen_stats],
                   c=gens, cmap='plasma', s=20, alpha=0.6)
axes[2, 1].set_xlabel('Connections')
axes[2, 1].set_ylabel('Average Consciousness')
axes[2, 1].set_title('NETWORK-CONSCIOUSNESS COUPLING')
axes[2, 1].grid(True, alpha=0.3)

plt.tight_layout()
fig2.savefig(OUTPUT_DIR / 'evolution_timeseries.png', dpi=300, bbox_inches='tight')
print(f"✅ Saved: evolution_timeseries.png")

# ============================================================================
# PHASE 6: SUMMARY STATISTICS
# ============================================================================

print("\n[PHASE 6] Computing summary statistics...")

stats = {
    'total_generations': len(generations),
    'total_organisms': len(all_organisms),
    'fitness': {
        'min': float(fitness.min()),
        'max': float(fitness.max()),
        'mean': float(fitness.mean()),
        'std': float(fitness.std()),
    },
    'consciousness': {
        'min': float(consciousness.min()),
        'max': float(consciousness.max()),
        'mean': float(consciousness.mean()),
        'std': float(consciousness.std()),
    },
    'threshold': {
        'min': float(thresholds.min()),
        'max': float(thresholds.max()),
        'mean': float(thresholds.mean()),
    },
    'correlations': {k: float(v) for k, v in correlations.items()},
}

with open(OUTPUT_DIR / 'topology_summary.json', 'w') as f:
    json.dump(stats, f, indent=2)

print(f"✅ Saved: topology_summary.json")

# ============================================================================
# FINAL SUMMARY
# ============================================================================

print("\n" + "="*70)
print("🌌 TACHYONIC FIELD ANALYSIS COMPLETE")
print("="*70)
print(f"\n📊 Dataset:")
print(f"   • Generations: {len(generations)}")
print(f"   • Organisms: {len(all_organisms)}")
print(f"   • Trait dimensions: {len(trait_names)}")

print(f"\n📈 Key Metrics:")
print(f"   • Fitness: {fitness.min():.4f} - {fitness.max():.4f} (μ={fitness.mean():.4f})")
print(f"   • Consciousness: {consciousness.min():.4f} - {consciousness.max():.4f} (μ={consciousness.mean():.4f})")
print(f"   • Threshold: {thresholds.min():.4f} - {thresholds.max():.4f}")

print(f"\n🔗 Strongest Correlations:")
top_corrs = sorted(correlations.items(), key=lambda x: abs(x[1]), reverse=True)[:3]
for name, value in top_corrs:
    print(f"   • {name}: {value:+.4f}")

print(f"\n💾 Output:")
print(f"   • {OUTPUT_DIR / 'population_topology_6views.png'}")
print(f"   • {OUTPUT_DIR / 'evolution_timeseries.png'}")
print(f"   • {OUTPUT_DIR / 'topology_summary.json'}")

print("\n🌌 WHAT IS THE TACHYONIC FIELD?")
print("="*70)
print("""
The Tachyonic Field is a multi-dimensional representation of population
internal architecture expressed as 3D topology:

1. TRAIT SPACE (X, Y, Z coordinates)
   • Organism positions based on genetic/phenotypic traits
   • Distance = trait dissimilarity
   • Clustering = genetic/functional modules

2. FITNESS LANDSCAPE (Height/elevation)
   • Peaks = optimal trait combinations (adaptive peaks)
   • Valleys = low-fitness regions (evolutionary transitions)
   • Ridges = co-adapted trait complexes

3. CONSCIOUSNESS FIELD (Density/intensity)
   • Color/opacity = consciousness level
   • Gradients = information flow patterns
   • Clusters = integrated information modules

4. NETWORK TOPOLOGY (Structural connections)
   • Threshold = connection strength cutoff
   • Connections = functional relationships
   • Phase transitions = critical reorganization points

5. TEMPORAL EVOLUTION (Animation frames)
   • Each frame = one generation
   • Trajectories = evolutionary paths through trait-space
   • Dynamics = adaptation to changing network topology

The field visualizes how individual organism traits create emergent
geometric structures that evolve over time, revealing the "shape" of
evolution itself.
""")
print("="*70)
