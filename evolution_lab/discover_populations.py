import json
from pathlib import Path

pop_file = Path("evolution_lab/populations/pop_20251018_111724_gen000_20251018_111724.json")
with open(pop_file) as f:
    data = json.load(f)

print("=" * 70)
print("POPULATION STRUCTURE DISCOVERY")
print("=" * 70)
print(f"\nPopulation ID: {data['population_id']}")
print(f"Generation: {data['generation']}")
print(f"Organism Count: {data['organism_count']}")
print(f"Average Fitness: {data['average_fitness']:.4f}")
print(f"Average Complexity: {data['average_complexity']:.4f}")
print(f"Consciousness Trajectory: {len(data.get('consciousness_trajectory', []))} points")

print(f"\n{'=' * 70}")
print("FIRST ORGANISM SAMPLE")
print("=" * 70)
org = data['organisms'][0]
print(f"\nOrganism ID: {org['organism_id']}")
print(f"Archetype: {org['archetype']}")
print(f"Fitness Score: {org['fitness_score']:.4f}")
print(f"Complexity Score: {org['complexity_score']:.4f}")
print(f"Code Length: {org['code_length']} chars")
print(f"Patterns Used: {len(org.get('patterns_used', []))}")
print(f"APIs Used: {len(org.get('apis_used', []))}")
print(f"Generation: {org['generation']}")
print(f"Parent ID: {org.get('parent_id', 'None (initial)')}")

print(f"\n{'=' * 70}")
print("POPULATION ARCHIVE STATISTICS")
print("=" * 70)
pop_dir = Path("evolution_lab/populations")
json_files = list(pop_dir.glob("pop_*.json"))
print(f"\nTotal population files: {len(json_files)}")
print(f"Location: {pop_dir.absolute()}")
print(f"Pattern: pop_YYYYMMDD_HHMMSS_genXXX_YYYYMMDD_HHMMSS.json")
print("\n✅ DISCOVERY COMPLETE - Population visor can read from these JSON files")
