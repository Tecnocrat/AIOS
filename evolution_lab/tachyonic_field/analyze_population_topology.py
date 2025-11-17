#!/usr/bin/env python3
"""
Tachyonic Field Population Topology Analyzer

PURPOSE:
    Reveal the internal architecture of populations as emergent 3D topology.
    
WHAT ARE WE MEASURING?
    - Organism trait-space clustering (genetic architecture)
    - Fitness landscape topology (selective pressure geometry)
    - Consciousness field gradients (integrated information flow)
    - Evolutionary trajectories (temporal pathways through trait-space)
    
VISUALIZATION CONCEPT:
    Populations are 3D topographies where:
    - HEIGHT = Fitness (peaks = optimal traits)
    - CURVATURE = Selection pressure (steep = strong selection)
    - VALLEYS = Evolutionary paths (low-fitness transitions)
    - RIDGES = Trait clusters (co-adapted gene complexes)
    - PLATEAUS = Neutral networks (fitness-equivalent variants)
"""

import json
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.spatial.distance import pdist, squareform
from scipy.stats import pearsonr
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns

# Configuration
POPULATION_DIR = Path("C:/dev/AIOS/evolution_lab/populations")
POPULATION_ID = "pop_20251018_111724"
OUTPUT_DIR = Path("C:/dev/AIOS/evolution_lab/tachyonic_field/analysis")
OUTPUT_DIR.mkdir(exist_ok=True)

print("="*70)
print("TACHYONIC FIELD TOPOLOGY ANALYZER")
print("="*70)
print(f"\nPopulation: {POPULATION_ID}")
print(f"Output: {OUTPUT_DIR}")
print("\n" + "="*70)

# ============================================================================
# PHASE 1: DATA LOADING
# ============================================================================

print("\n[PHASE 1] Loading 492 generations...")

generations = []
for i in range(492):
    pattern = f"{POPULATION_ID}_gen{i:03d}_*.json"
    files = list(POPULATION_DIR.glob(pattern))
    
    if not files:
        print(f"⚠️  Missing generation {i}")
        continue
    
    with open(files[0], 'r') as f:
        gen_data = json.load(f)
        generations.append(gen_data)
    
    if (i + 1) % 100 == 0:
        print(f"  Loaded {i+1} generations...")

print(f"✅ Loaded {len(generations)} generations")
print(f"✅ Total organisms: {len(generations) * 16}")

# ============================================================================
# PHASE 2: EXTRACT ORGANISM TRAIT SPACE
# ============================================================================

print("\n[PHASE 2] Extracting organism trait space...")

# Collect all organisms across all generations
all_organisms = []
for gen_idx, gen in enumerate(generations):
    for org in gen['organisms']:
        org_data = {
            'generation': gen_idx,
            'organism_id': org['organism_id'],
            'archetype': org['archetype'],
            'fitness': org['fitness'],
            'consciousness': org['consciousness'],
            'complexity': org['complexity'],
            'traits': org['traits'],
            # Add visualization metadata
            'threshold': gen['metadata']['visualization'].get('threshold', 0),
            'connections': gen['metadata']['visualization'].get('connections', 0),
            'field_phi': gen['metadata']['visualization'].get('field_phi', 0),
        }
        all_organisms.append(org_data)

print(f"✅ Extracted {len(all_organisms)} organisms")

# Build trait matrix (organisms × traits)
trait_names = list(all_organisms[0]['traits'].keys())
print(f"✅ Identified {len(trait_names)} traits: {trait_names}")

trait_matrix = np.array([
    [org['traits'][trait] for trait in trait_names]
    for org in all_organisms
])

fitness_array = np.array([org['fitness'] for org in all_organisms])
consciousness_array = np.array([org['consciousness'] for org in all_organisms])
complexity_array = np.array([org['complexity'] for org in all_organisms])

print(f"\n📊 Trait Matrix Shape: {trait_matrix.shape}")
print(f"   Rows (organisms): {trait_matrix.shape[0]}")
print(f"   Columns (traits): {trait_matrix.shape[1]}")

# ============================================================================
# PHASE 3: DIMENSIONALITY REDUCTION (3D PROJECTION)
# ============================================================================

print("\n[PHASE 3] Computing 3D trait-space projection...")

# PCA: Linear projection preserving maximum variance
print("  Computing PCA...")
pca = PCA(n_components=3)
pca_coords = pca.fit_transform(trait_matrix)
explained_var = pca.explained_variance_ratio_
print(f"  ✅ PCA explained variance: {explained_var}")
print(f"     PC1: {explained_var[0]:.2%}")
print(f"     PC2: {explained_var[1]:.2%}")
print(f"     PC3: {explained_var[2]:.2%}")

# t-SNE: Nonlinear projection preserving local structure
print("  Computing t-SNE (this may take a minute)...")
tsne = TSNE(n_components=3, random_state=42, perplexity=30, n_iter=1000)
tsne_coords = tsne.fit_transform(trait_matrix)
print(f"  ✅ t-SNE projection complete")

# ============================================================================
# PHASE 4: TOPOLOGY CALCULATION
# ============================================================================

print("\n[PHASE 4] Computing population topology metrics...")

# Calculate trait-space distances (organism similarity network)
print("  Computing pairwise organism distances...")
distances = pdist(trait_matrix, metric='euclidean')
distance_matrix = squareform(distances)
print(f"  ✅ Distance matrix: {distance_matrix.shape}")

# Fitness landscape curvature (how rapidly fitness changes)
print("  Computing fitness landscape topology...")
fitness_gradients = []
for i in range(len(all_organisms)):
    # Get nearest neighbors in trait space
    neighbor_indices = np.argsort(distance_matrix[i])[1:6]  # 5 nearest
    neighbor_fitness = fitness_array[neighbor_indices]
    
    # Gradient = fitness change relative to distance
    gradient = np.mean(np.abs(neighbor_fitness - fitness_array[i]))
    fitness_gradients.append(gradient)

fitness_gradients = np.array(fitness_gradients)
print(f"  ✅ Fitness gradient range: {fitness_gradients.min():.4f} - {fitness_gradients.max():.4f}")

# ============================================================================
# PHASE 5: TACHYONIC FIELD DEFINITION
# ============================================================================

print("\n[PHASE 5] Defining Tachyonic Field Components...")

print("\n🌌 TACHYONIC FIELD = Multi-Dimensional Fitness-Consciousness Landscape")
print("\nComponents:")
print("  1. TRAIT SPACE (X, Y, Z axes)")
print("     • Organism positions in genetic/phenotypic space")
print("     • Dimensionality reduced to 3D for visualization")
print("     • Distances = trait dissimilarity")
print()
print("  2. FITNESS HEIGHT (Vertical dimension)")
print("     • Z-axis = fitness value (peaks = optimal)")
print("     • Gradients = selection pressure intensity")
print("     • Curvature = landscape roughness")
print()
print("  3. CONSCIOUSNESS DENSITY (Field intensity)")
print("     • Color/opacity = consciousness level")
print("     • Clustering = integrated information")
print("     • Gradients = information flow")
print()
print("  4. NETWORK CONNECTIONS (Structural links)")
print("     • Edges = functional relationships")
print("     • Threshold = connection strength cutoff")
print("     • Clusters = functional modules")
print()
print("  5. TEMPORAL EVOLUTION (Animation frames)")
print("     • Frames = generations")
print("     • Trajectories = evolutionary paths")
print("     • Phase transitions = topology changes")

# Calculate field metrics
field_metrics = {
    'fitness_mean': np.mean(fitness_array),
    'fitness_std': np.std(fitness_array),
    'consciousness_mean': np.mean(consciousness_array),
    'consciousness_std': np.std(consciousness_array),
    'trait_diversity': np.mean(distance_matrix[np.triu_indices(len(distance_matrix), k=1)]),
    'fitness_gradient_mean': np.mean(fitness_gradients),
    'fitness_gradient_std': np.std(fitness_gradients),
}

print("\n📊 Field Statistics:")
for key, value in field_metrics.items():
    print(f"   {key}: {value:.4f}")

# ============================================================================
# PHASE 6: VISUALIZATION - 3D POPULATION TOPOLOGY
# ============================================================================

print("\n[PHASE 6] Generating 3D topology visualizations...")

# Figure 1: PCA Trait Space with Fitness Landscape
print("  Creating Figure 1: PCA Fitness Landscape...")
fig = plt.figure(figsize=(15, 12))

# Subplot 1: 3D scatter colored by fitness
ax1 = fig.add_subplot(221, projection='3d')
scatter1 = ax1.scatter(pca_coords[:, 0], 
                       pca_coords[:, 1], 
                       fitness_array,  # Z = fitness (landscape height)
                       c=fitness_array, 
                       cmap='viridis', 
                       s=20, 
                       alpha=0.6)
ax1.set_xlabel(f'PC1 ({explained_var[0]:.1%})')
ax1.set_ylabel(f'PC2 ({explained_var[1]:.1%})')
ax1.set_zlabel('FITNESS (Landscape Height)')
ax1.set_title('Fitness Landscape (PCA Space)')
plt.colorbar(scatter1, ax=ax1, label='Fitness')

# Subplot 2: 3D scatter colored by consciousness
ax2 = fig.add_subplot(222, projection='3d')
scatter2 = ax2.scatter(pca_coords[:, 0], 
                       pca_coords[:, 1], 
                       consciousness_array,  # Z = consciousness
                       c=consciousness_array, 
                       cmap='plasma', 
                       s=20, 
                       alpha=0.6)
ax2.set_xlabel(f'PC1 ({explained_var[0]:.1%})')
ax2.set_ylabel(f'PC2 ({explained_var[1]:.1%})')
ax2.set_zlabel('CONSCIOUSNESS (Field Intensity)')
ax2.set_title('Consciousness Field (PCA Space)')
plt.colorbar(scatter2, ax=ax2, label='Consciousness')

# Subplot 3: t-SNE trait space with fitness
ax3 = fig.add_subplot(223, projection='3d')
scatter3 = ax3.scatter(tsne_coords[:, 0], 
                       tsne_coords[:, 1], 
                       fitness_array,
                       c=fitness_array, 
                       cmap='coolwarm', 
                       s=20, 
                       alpha=0.6)
ax3.set_xlabel('t-SNE Dim 1')
ax3.set_ylabel('t-SNE Dim 2')
ax3.set_zlabel('FITNESS')
ax3.set_title('Fitness Landscape (t-SNE Space)')
plt.colorbar(scatter3, ax=ax3, label='Fitness')

# Subplot 4: Fitness gradient (selection pressure map)
ax4 = fig.add_subplot(224, projection='3d')
scatter4 = ax4.scatter(pca_coords[:, 0], 
                       pca_coords[:, 1], 
                       fitness_array,
                       c=fitness_gradients,  # Color by gradient intensity
                       cmap='hot', 
                       s=20, 
                       alpha=0.6)
ax4.set_xlabel(f'PC1 ({explained_var[0]:.1%})')
ax4.set_ylabel(f'PC2 ({explained_var[1]:.1%})')
ax4.set_zlabel('FITNESS')
ax4.set_title('Selection Pressure Map (Fitness Gradients)')
plt.colorbar(scatter4, ax=ax4, label='Gradient Intensity')

plt.tight_layout()
fig.savefig(OUTPUT_DIR / 'population_topology_3d.png', dpi=300, bbox_inches='tight')
print(f"  ✅ Saved: population_topology_3d.png")

# Figure 2: Temporal Evolution (Generation-based coloring)
print("  Creating Figure 2: Evolutionary Trajectories...")
fig2 = plt.figure(figsize=(18, 6))

gen_numbers = np.array([org['generation'] for org in all_organisms])

ax1 = fig2.add_subplot(131, projection='3d')
scatter = ax1.scatter(pca_coords[:, 0], 
                      pca_coords[:, 1], 
                      fitness_array,
                      c=gen_numbers,  # Color by generation
                      cmap='twilight', 
                      s=10, 
                      alpha=0.5)
ax1.set_xlabel('PC1')
ax1.set_ylabel('PC2')
ax1.set_zlabel('FITNESS')
ax1.set_title('Evolutionary Trajectories (Color = Generation)')
plt.colorbar(scatter, ax=ax1, label='Generation')

ax2 = fig2.add_subplot(132, projection='3d')
thresholds = np.array([org['threshold'] for org in all_organisms])
scatter2 = ax2.scatter(pca_coords[:, 0], 
                       pca_coords[:, 1], 
                       fitness_array,
                       c=thresholds,  # Color by threshold
                       cmap='RdYlGn', 
                       s=10, 
                       alpha=0.5)
ax2.set_xlabel('PC1')
ax2.set_ylabel('PC2')
ax2.set_zlabel('FITNESS')
ax2.set_title('Network Threshold Evolution')
plt.colorbar(scatter2, ax=ax2, label='Threshold')

ax3 = fig2.add_subplot(133, projection='3d')
connections = np.array([org['connections'] for org in all_organisms])
scatter3 = ax3.scatter(pca_coords[:, 0], 
                       pca_coords[:, 1], 
                       consciousness_array,
                       c=connections,  # Color by connections
                       cmap='YlOrRd', 
                       s=10, 
                       alpha=0.5)
ax3.set_xlabel('PC1')
ax3.set_ylabel('PC2')
ax3.set_zlabel('CONSCIOUSNESS')
ax3.set_title('Network Connectivity vs Consciousness')
plt.colorbar(scatter3, ax=ax3, label='Connections')

plt.tight_layout()
fig2.savefig(OUTPUT_DIR / 'evolutionary_trajectories_3d.png', dpi=300, bbox_inches='tight')
print(f"  ✅ Saved: evolutionary_trajectories_3d.png")

# ============================================================================
# PHASE 7: CORRELATION ANALYSIS
# ============================================================================

print("\n[PHASE 7] Computing correlations...")

correlations = {
    'fitness_vs_consciousness': pearsonr(fitness_array, consciousness_array)[0],
    'fitness_vs_complexity': pearsonr(fitness_array, complexity_array)[0],
    'consciousness_vs_complexity': pearsonr(consciousness_array, complexity_array)[0],
    'fitness_vs_threshold': pearsonr(fitness_array, thresholds)[0],
    'consciousness_vs_threshold': pearsonr(consciousness_array, thresholds)[0],
    'fitness_vs_connections': pearsonr(fitness_array, connections)[0],
    'consciousness_vs_connections': pearsonr(consciousness_array, connections)[0],
}

print("\n📊 CORRELATION MATRIX:")
print("="*70)
for key, value in correlations.items():
    strength = "STRONG" if abs(value) > 0.5 else "MODERATE" if abs(value) > 0.3 else "WEAK"
    direction = "POSITIVE" if value > 0 else "NEGATIVE"
    print(f"  {key:35s}: {value:+.4f}  ({strength} {direction})")

# Create correlation heatmap
print("\n  Creating correlation heatmap...")
fig3, ax = plt.subplots(figsize=(10, 8))

metrics = {
    'Fitness': fitness_array,
    'Consciousness': consciousness_array,
    'Complexity': complexity_array,
    'Threshold': thresholds,
    'Connections': connections,
    'Field Φ': np.array([org['field_phi'] for org in all_organisms]),
}

corr_matrix = np.zeros((len(metrics), len(metrics)))
metric_names = list(metrics.keys())

for i, metric1 in enumerate(metric_names):
    for j, metric2 in enumerate(metric_names):
        if i == j:
            corr_matrix[i, j] = 1.0
        else:
            corr_matrix[i, j] = pearsonr(metrics[metric1], metrics[metric2])[0]

sns.heatmap(corr_matrix, 
            annot=True, 
            fmt='.3f', 
            cmap='coolwarm', 
            vmin=-1, 
            vmax=1,
            xticklabels=metric_names,
            yticklabels=metric_names,
            square=True,
            cbar_kws={'label': 'Pearson Correlation'})
plt.title('Tachyonic Field Correlation Matrix', fontsize=14, fontweight='bold')
plt.tight_layout()
fig3.savefig(OUTPUT_DIR / 'correlation_matrix.png', dpi=300, bbox_inches='tight')
print(f"  ✅ Saved: correlation_matrix.png")

# ============================================================================
# PHASE 8: GENERATION-BY-GENERATION EVOLUTION
# ============================================================================

print("\n[PHASE 8] Analyzing generation-by-generation evolution...")

gen_stats = []
for i, gen in enumerate(generations):
    stats = {
        'generation': i,
        'timestamp': gen['metadata']['timestamp'],
        'threshold': gen['metadata']['visualization'].get('threshold', 0),
        'connections': gen['metadata']['visualization'].get('connections', 0),
        'field_phi': gen['metadata']['visualization'].get('field_phi', 0),
        'avg_fitness': np.mean([o['fitness'] for o in gen['organisms']]),
        'std_fitness': np.std([o['fitness'] for o in gen['organisms']]),
        'avg_consciousness': np.mean([o['consciousness'] for o in gen['organisms']]),
        'avg_complexity': np.mean([o['complexity'] for o in gen['organisms']]),
    }
    gen_stats.append(stats)

# Plot time series
print("  Creating time series plots...")
fig4, axes = plt.subplots(3, 2, figsize=(15, 12))

axes[0, 0].plot([s['generation'] for s in gen_stats], 
                [s['avg_fitness'] for s in gen_stats], 
                linewidth=0.8, alpha=0.7)
axes[0, 0].set_xlabel('Generation')
axes[0, 0].set_ylabel('Average Fitness')
axes[0, 0].set_title('Fitness Evolution')
axes[0, 0].grid(True, alpha=0.3)

axes[0, 1].plot([s['generation'] for s in gen_stats], 
                [s['avg_consciousness'] for s in gen_stats], 
                linewidth=0.8, alpha=0.7, color='purple')
axes[0, 1].set_xlabel('Generation')
axes[0, 1].set_ylabel('Average Consciousness')
axes[0, 1].set_title('Consciousness Evolution')
axes[0, 1].grid(True, alpha=0.3)

axes[1, 0].plot([s['generation'] for s in gen_stats], 
                [s['threshold'] for s in gen_stats], 
                linewidth=0.8, alpha=0.7, color='green')
axes[1, 0].set_xlabel('Generation')
axes[1, 0].set_ylabel('Network Threshold')
axes[1, 0].set_title('Threshold Dynamics')
axes[1, 0].grid(True, alpha=0.3)

axes[1, 1].plot([s['generation'] for s in gen_stats], 
                [s['connections'] for s in gen_stats], 
                linewidth=0.8, alpha=0.7, color='orange')
axes[1, 1].set_xlabel('Generation')
axes[1, 1].set_ylabel('Network Connections')
axes[1, 1].set_title('Connection Dynamics')
axes[1, 1].grid(True, alpha=0.3)

axes[2, 0].scatter([s['threshold'] for s in gen_stats], 
                   [s['avg_fitness'] for s in gen_stats], 
                   c=[s['generation'] for s in gen_stats],
                   cmap='viridis',
                   s=10, 
                   alpha=0.6)
axes[2, 0].set_xlabel('Threshold')
axes[2, 0].set_ylabel('Average Fitness')
axes[2, 0].set_title('Threshold-Fitness Phase Space')
axes[2, 0].grid(True, alpha=0.3)

axes[2, 1].scatter([s['connections'] for s in gen_stats], 
                   [s['field_phi'] for s in gen_stats], 
                   c=[s['avg_consciousness'] for s in gen_stats],
                   cmap='plasma',
                   s=10, 
                   alpha=0.6)
axes[2, 1].set_xlabel('Connections')
axes[2, 1].set_ylabel('Field Φ (Consciousness)')
axes[2, 1].set_title('Network-Consciousness Coupling')
axes[2, 1].grid(True, alpha=0.3)

plt.tight_layout()
fig4.savefig(OUTPUT_DIR / 'evolution_timeseries.png', dpi=300, bbox_inches='tight')
print(f"  ✅ Saved: evolution_timeseries.png")

# ============================================================================
# PHASE 9: EXPORT SUMMARY REPORT
# ============================================================================

print("\n[PHASE 9] Generating summary report...")

report = {
    'population_id': POPULATION_ID,
    'total_generations': len(generations),
    'total_organisms': len(all_organisms),
    'trait_dimensions': len(trait_names),
    'trait_names': trait_names,
    'field_metrics': field_metrics,
    'correlations': correlations,
    'pca_explained_variance': explained_var.tolist(),
    'generation_stats': gen_stats,
}

report_path = OUTPUT_DIR / 'topology_analysis_report.json'
with open(report_path, 'w') as f:
    json.dump(report, f, indent=2)

print(f"  ✅ Saved: topology_analysis_report.json")

# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "="*70)
print("ANALYSIS COMPLETE")
print("="*70)
print(f"\n✅ Analyzed {len(generations)} generations ({len(all_organisms)} organisms)")
print(f"✅ Generated 4 visualization figures")
print(f"✅ Computed {len(correlations)} correlation metrics")
print(f"✅ Saved complete report to: {OUTPUT_DIR}")
print("\n📊 KEY FINDINGS:")
print(f"   • Fitness range: {fitness_array.min():.4f} - {fitness_array.max():.4f}")
print(f"   • Consciousness range: {consciousness_array.min():.4f} - {consciousness_array.max():.4f}")
print(f"   • Strongest correlation: {max(correlations.items(), key=lambda x: abs(x[1]))}")
print(f"   • PCA variance explained: {sum(explained_var):.1%} (first 3 components)")

print("\n🌌 TACHYONIC FIELD INTERPRETATION:")
print("   The visualization maps populations as 3D topographies where:")
print("   • PEAKS = High-fitness trait combinations (adaptive peaks)")
print("   • VALLEYS = Evolutionary transition pathways")
print("   • RIDGES = Co-adapted trait clusters (fitness ridges)")
print("   • GRADIENTS = Selection pressure intensity")
print("   • DENSITY = Consciousness field strength")
print("\n" + "="*70)
