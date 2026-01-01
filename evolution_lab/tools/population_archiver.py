"""
AINLP Population Archive Reorganization
Cleans up clone-based populations and establishes hierarchical archive structure

AINLP Protocol: OS0.6.4.claude
Created: 2025-12-05
Purpose: Archive legacy clones, elevate Mistral-mutated populations

Archive Structure:
    populations/
        ├── active/                    # Current working populations
        │   └── mistral_20251205/      # Latest healthy Mistral population
        ├── archive/                   # Historical populations
        │   └── legacy_clones_20251018/  # Pre-mutation clone populations
        ├── seeds/                     # Original seed templates
        │   └── gen0_templates.json    # Base organism templates
        └── index.json                 # Master population index
"""

import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any


class PopulationArchiver:
    """Reorganizes populations into hierarchical archive structure"""
    
    def __init__(self, populations_dir: Path):
        self.populations_dir = populations_dir
        self.archive_manifest: Dict[str, Any] = {
            "reorganization_date": datetime.utcnow().isoformat() + "Z",
            "archived_populations": [],
            "active_populations": [],
            "seed_populations": []
        }
    
    def create_archive_structure(self):
        """Create hierarchical folder structure"""
        folders = [
            self.populations_dir / "active",
            self.populations_dir / "archive",
            self.populations_dir / "archive" / "legacy_clones_20251018",
            self.populations_dir / "seeds"
        ]
        
        for folder in folders:
            folder.mkdir(parents=True, exist_ok=True)
            print(f"📁 Created: {folder.relative_to(self.populations_dir)}")
    
    def identify_clone_populations(self) -> List[Path]:
        """Identify populations that are clones (no fitness variance)"""
        clone_items = []
        
        # Check subfolders (pop_YYYYMMDD_* pattern)
        for item in self.populations_dir.iterdir():
            if item.is_dir() and item.name.startswith("pop_2025101"):
                clone_items.append(item)
        
        # Also include backup folder if it exists
        backup_dir = self.populations_dir / "backup_20251018_124347"
        if backup_dir.exists():
            clone_items.append(backup_dir)
        
        return clone_items
    
    def identify_mistral_populations(self) -> List[Path]:
        """Identify Mistral-mutated populations (in tachyonic/)"""
        mistral_pops = []
        tachyonic_dir = self.populations_dir / "tachyonic"
        
        if tachyonic_dir.exists():
            for json_file in tachyonic_dir.glob("pop_20251205_*.json"):
                mistral_pops.append(json_file)
        
        return mistral_pops
    
    def archive_clone_populations(self):
        """Move clone populations to archive folder"""
        archive_dest = self.populations_dir / "archive" / "legacy_clones"
        archive_dest.mkdir(parents=True, exist_ok=True)
        clone_items = self.identify_clone_populations()
        
        print(f"\n📦 Archiving {len(clone_items)} legacy clone folders...")
        
        for src_item in clone_items:
            dest_item = archive_dest / src_item.name
            if not dest_item.exists():
                shutil.move(str(src_item), str(dest_item))
                
                self.archive_manifest["archived_populations"].append({
                    "folder": src_item.name,
                    "destination": f"archive/legacy_clones/{src_item.name}",
                    "reason": "legacy_clone_no_mutation"
                })
                
                print(f"  → {src_item.name}")
            else:
                print(f"  ⚠ {src_item.name} (already archived)")
        
        return len(clone_items)
    
    def elevate_mistral_population(self):
        """Move Mistral population to active/ with prominent position"""
        active_dir = self.populations_dir / "active" / "mistral_20251205"
        active_dir.mkdir(parents=True, exist_ok=True)
        
        tachyonic_dir = self.populations_dir / "tachyonic"
        mistral_files = self.identify_mistral_populations()
        
        print(f"\n🚀 Elevating {len(mistral_files)} Mistral population files...")
        
        for src_file in mistral_files:
            dest_file = active_dir / src_file.name
            shutil.copy2(str(src_file), str(dest_file))  # Copy, keep original in tachyonic
            
            self.archive_manifest["active_populations"].append({
                "file": src_file.name,
                "source": str(src_file.relative_to(self.populations_dir)),
                "destination": str(dest_file.relative_to(self.populations_dir)),
                "mutation_engine": "mistral_7b_local"
            })
            
            print(f"  ⬆ {src_file.name}")
        
        return len(mistral_files)
    
    def extract_seed_templates(self):
        """Extract gen0 organisms as seed templates"""
        seeds_dir = self.populations_dir / "seeds"
        
        # Look for gen0 in archived populations or tachyonic
        possible_sources = [
            self.populations_dir / "archive" / "legacy_clones",
            self.populations_dir / "tachyonic",
            self.populations_dir / "active" / "mistral_20251205"
        ]
        
        gen0_data = None
        source_file = None
        
        for source_dir in possible_sources:
            if source_dir.exists():
                for gen0_file in source_dir.glob("*_gen000_*.json"):
                    with open(gen0_file) as f:
                        gen0_data = json.load(f)
                    source_file = gen0_file.name
                    break
            if gen0_data:
                break
        
        if gen0_data:
            # Already loaded above, no need to reload
            
            # Extract unique seed templates by archetype
            seeds = {}
            for org in gen0_data.get("organisms", []):
                archetype = org.get("archetype")
                if archetype and archetype not in seeds:
                    seeds[archetype] = {
                        "organism_id": org.get("organism_id"),
                        "archetype": archetype,
                        "code_length": org.get("code_length"),
                        "complexity_score": org.get("complexity_score"),
                        "metadata": {"seed_source": source_file}
                    }
            
            seed_file = seeds_dir / "gen0_templates.json"
            with open(seed_file, 'w') as f:
                json.dump({
                    "extracted_from": source_file,
                    "extraction_date": datetime.utcnow().isoformat() + "Z",
                    "archetypes": seeds
                }, f, indent=2)
            
            self.archive_manifest["seed_populations"].append({
                "file": "gen0_templates.json",
                "archetypes": list(seeds.keys())
            })
            
            print(f"\n🌱 Extracted {len(seeds)} archetype seed templates")
            return len(seeds)
        
        return 0
    
    def create_master_index(self):
        """Create master population index"""
        index_file = self.populations_dir / "archive_index.json"
        
        # Add summary stats
        self.archive_manifest["summary"] = {
            "total_archived": len(self.archive_manifest["archived_populations"]),
            "total_active": len(self.archive_manifest["active_populations"]),
            "total_seeds": len(self.archive_manifest["seed_populations"]),
            "archive_structure": {
                "active/": "Current working populations with real mutations",
                "archive/": "Historical populations (clones, deprecated)",
                "seeds/": "Original organism templates by archetype",
                "tachyonic/": "Raw evolution outputs (preserved)"
            }
        }
        
        with open(index_file, 'w') as f:
            json.dump(self.archive_manifest, f, indent=2)
        
        print(f"\n📋 Master index created: {index_file.name}")
    
    def run_reorganization(self):
        """Execute full reorganization"""
        print("=" * 60)
        print("AINLP POPULATION ARCHIVE REORGANIZATION")
        print("=" * 60)
        
        # Step 1: Create structure
        self.create_archive_structure()
        
        # Step 2: Archive clones
        archived = self.archive_clone_populations()
        
        # Step 3: Elevate Mistral
        elevated = self.elevate_mistral_population()
        
        # Step 4: Extract seeds
        seeds = self.extract_seed_templates()
        
        # Step 5: Create index
        self.create_master_index()
        
        print("\n" + "=" * 60)
        print("REORGANIZATION COMPLETE")
        print(f"  Archived: {archived} legacy files")
        print(f"  Elevated: {elevated} Mistral files")
        print(f"  Seeds: {seeds} archetypes")
        print("=" * 60)
        
        return self.archive_manifest


def main():
    populations_dir = Path(__file__).parent.parent / "populations"
    
    archiver = PopulationArchiver(populations_dir)
    manifest = archiver.run_reorganization()
    
    return manifest


if __name__ == "__main__":
    main()
