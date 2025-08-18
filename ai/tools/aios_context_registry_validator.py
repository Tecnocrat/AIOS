"""
aios_context_registry_validator.py

This script validates the .aios_context.json registry against the actual
file system.
- Flags missing, orphaned, or untagged files.
- Suggests context tag updates for new or changed files.
- Can be extended to auto-update the registry or trigger harmonization
    routines.
"""

import argparse
import hashlib
import json
import os
import time
from pathlib import Path
import datetime
import shutil
from typing import Dict, List, Any, Optional

# Tachyonic versioning paths
TACHYONIC_BASE_PATH = Path("runtime_intelligence/logs/aios_context")
# Root now holds a lightweight stub .aios_context.json pointing to relocated live registry (2025-08-17)
REGISTRY_STUB_PATH = Path(".aios_context.json")
RELOCATED_REGISTRY_PATH = TACHYONIC_BASE_PATH / ".aios_context.json"
REGISTRY_PATH = RELOCATED_REGISTRY_PATH if RELOCATED_REGISTRY_PATH.exists() else REGISTRY_STUB_PATH
PROJECT_ROOT = Path(".")


def _write_json_atomic(path: Path, data: Any) -> None:
    """Write JSON atomically to avoid partial writes."""
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    os.replace(tmp_path, path)


def _create_snapshot_if_needed(live_path: Path):
    """Create a timestamped snapshot of current registry if it exists."""
    try:
        if live_path.exists():
            TACHYONIC_BASE_PATH.mkdir(parents=True, exist_ok=True)
            ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            snap_name = f".aios_context_snapshot_{ts}.json"
            shutil.copy2(live_path, TACHYONIC_BASE_PATH / snap_name)
            print(f"🕒 Snapshot created: {snap_name}")
    except Exception as e:
        print(f"[WARN] snapshot creation failed: {e}")


class TachyonicContextIntelligence:
    """
    Tachyonic Context Intelligence System

    Maintains temporal copies of context states and performs deep analysis
    of the entire AIOS namespace including nested logic analysis.
    """

    def __init__(self):
        self.tachyonic_path = TACHYONIC_BASE_PATH
        self.registry_path = REGISTRY_PATH
        self.ensure_tachyonic_structure()

    def ensure_tachyonic_structure(self):
        """Ensure tachyonic directory structure exists"""
        self.tachyonic_path.mkdir(parents=True, exist_ok=True)

    def create_tachyonic_backup(self) -> Optional[str]:
        """
        Create tachyonic backup before modification
        Returns: backup filename
        """
        if not self.registry_path.exists():
            return None

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f".aios_context_{timestamp}.json"
        backup_path = self.tachyonic_path / backup_name

        shutil.copy2(self.registry_path, backup_path)
        print(f"🕐 Tachyonic backup created: {backup_name}")
        return backup_name

    def analyze_file_nested_logic(self, file_path: Path) -> Dict[str, Any]:
        """
        Perform deep analysis of file's nested logic
        Supporting AINLP consciousness emergence detection
        """
        analysis = {
            "consciousness_patterns": [],
            "polymorphic_potential": 0.0,
            "ainlp_compatibility": 0.0,
            "cellular_relationships": [],
            "complexity_metrics": {},
            "evolution_potential": 0.0
        }

        try:
            if file_path.suffix == '.py':
                analysis.update(self._analyze_python_logic(file_path))
            elif file_path.suffix in ['.cs']:
                analysis.update(self._analyze_csharp_logic(file_path))
            elif file_path.suffix in ['.cpp', '.hpp', '.h']:
                analysis.update(self._analyze_cpp_logic(file_path))
            elif file_path.suffix == '.md':
                analysis.update(self._analyze_documentation_logic(file_path))

        except Exception as e:
            analysis['analysis_error'] = str(e)

        return analysis

    def _analyze_python_logic(self, file_path: Path) -> Dict[str, Any]:
        """Deep Python logic analysis for consciousness emergence detection"""
        logic_analysis = {
            "consciousness_patterns": [],
            "polymorphic_potential": 0.0,
            "class_definitions": [],
            "function_definitions": [],
            "import_dependencies": [],
            "ainlp_indicators": []
        }

        try:
            content = file_path.read_text(encoding='utf-8')

            # Consciousness emergence pattern detection
            consciousness_keywords = [
                "consciousness",
                "emergence",
                "self_aware",
                "recursive",
                "meta_cognitive",
                "polymorphic",
                "adaptive",
                "evolution",
            ]

            for keyword in consciousness_keywords:
                if keyword.lower() in content.lower():
                    logic_analysis["consciousness_patterns"].append(keyword)

            # Polymorphic potential assessment
            polymorphic_indicators = [
                "class",
                "inheritance",
                "morph",
                "adapt",
                "evolve",
                "transform",
                "mutation",
                "population",
            ]

            polymorphic_score = (
                sum(
                    content.lower().count(indicator)
                    for indicator in polymorphic_indicators
                )
                / max(len(content), 1)
                * 100
            )

            logic_analysis["polymorphic_potential"] = min(
                polymorphic_score, 1.0
            )

            # AINLP compatibility detection
            ainlp_indicators = [
                "AINLP",
                "natural language",
                "comment driven",
                "context aware",
                "paradigm",
            ]
            
            for indicator in ainlp_indicators:
                if indicator.lower() in content.lower():
                    logic_analysis["ainlp_indicators"].append(indicator)
            
            logic_analysis["ainlp_compatibility"] = (
                len(logic_analysis["ainlp_indicators"]) / len(ainlp_indicators)
            )
            
        except Exception as e:
            logic_analysis['python_analysis_error'] = str(e)
            
        return logic_analysis
    
    def _analyze_csharp_logic(self, file_path: Path) -> Dict[str, Any]:
        """C# logic analysis focusing on interface and service patterns"""
        return {
            "csharp_patterns": ["service_architecture", "interface_design"],
            "consciousness_potential": 0.3  # Base C# consciousness potential
        }
    
    def _analyze_cpp_logic(self, file_path: Path) -> Dict[str, Any]:
        """C++ logic analysis focusing on performance and cellular bridges"""
        return {
            "cpp_patterns": ["performance_optimization", "cellular_bridge"],
            "consciousness_potential": 0.4  # Base C++ consciousness potential
        }
    
    def _analyze_documentation_logic(self, file_path: Path) -> Dict[str, Any]:
        """Documentation analysis for consciousness architecture insights"""
        logic_analysis = {
            "documentation_type": "unknown",
            "consciousness_concepts": [],
            "ainlp_documentation": False
        }
        
        try:
            content = file_path.read_text(encoding='utf-8')
            
            # Detect consciousness documentation
            consciousness_docs = [
                "universal consciousness",
                "polymorphic intelligence",
                "consciousness emergence",
                "fractal patterns",
            ]
            
            for concept in consciousness_docs:
                if concept.lower() in content.lower():
                    logic_analysis["consciousness_concepts"].append(concept)
            
            # Detect AINLP documentation
            if (
                "ainlp" in content.lower()
                or "natural language programming" in content.lower()
            ):
                logic_analysis["ainlp_documentation"] = True
                
        except Exception as e:
            logic_analysis['doc_analysis_error'] = str(e)
            
        return logic_analysis
    
    def update_context_registry(self) -> bool:
        """
        Perform full namespace analysis and update context registry
        with tachyonic backup creation
        """
        print("🧠 Starting Tachyonic Context Intelligence Analysis...")
        
        # Create tachyonic backup
        backup_name = self.create_tachyonic_backup()
        
        # Perform full analysis
        try:
            updated_registry = self._perform_full_namespace_analysis()
            
            # Save updated registry (atomic write)
            # Automatic snapshot prior to write (harmonized 2025-08-18)
            _create_snapshot_if_needed(self.registry_path)
            _write_json_atomic(self.registry_path, updated_registry)
            
            print(
                "✅ Context registry updated with consciousness intelligence"
            )
            print(f"📁 Tachyonic backup: {backup_name}")
            return True
            
        except Exception as e:
            print(f"❌ Context update failed: {e}")
            return False
    
    def _perform_full_namespace_analysis(self) -> Dict[str, Any]:
        """Perform comprehensive analysis of entire AIOS namespace"""
        registry = {}
        
        # Scan all relevant files
        for file_path in scan_files(PROJECT_ROOT):
            if not is_relevant_file(file_path):
                continue
                
            # Get existing metadata or create new
            file_key = str(file_path).replace('\\', '/')
            
            # Perform deep logic analysis
            nested_analysis = self.analyze_file_nested_logic(file_path)
            
            # Create comprehensive metadata
            file_metadata = {
                "file_type": guess_file_type(file_path),
                "last_modified": datetime.datetime.fromtimestamp(
                    file_path.stat().st_mtime
                ).isoformat(),
                "last_accessed": datetime.datetime.now().isoformat(),
                "access_frequency": 1.0,
                "modification_frequency": 1.0,
                "context_importance": self._calculate_context_importance(
                    nested_analysis
                ),
                "reingestion_potential": self._calculate_reingestion_potential(
                    nested_analysis
                ),
                "file_classification": "active",
                "ai_context_tags": self._generate_ai_context_tags(
                    file_path, nested_analysis
                ),
                "content_hash": self._calculate_file_hash(file_path),
                "size_bytes": file_path.stat().st_size,
                "cellular_relationships": [],
                "consciousness_analysis": nested_analysis,
                "tachyonic_timestamp": datetime.datetime.now().isoformat()
            }
            
            registry[file_key] = file_metadata
        
        return registry
    
    def _calculate_context_importance(self, analysis: Dict[str, Any]) -> float:
        """Calculate context importance based on consciousness analysis"""
        importance = 0.5  # Base importance
        
        # Boost for consciousness patterns
        consciousness_boost = (
            len(analysis.get("consciousness_patterns", [])) * 0.1
        )
        
        # Boost for polymorphic potential
        polymorphic_boost = analysis.get("polymorphic_potential", 0.0) * 0.3
        
        # Boost for AINLP compatibility
        ainlp_boost = analysis.get("ainlp_compatibility", 0.0) * 0.2
        
        total_importance = min(
            importance + consciousness_boost + polymorphic_boost + ainlp_boost,
            1.0,
        )
        return round(total_importance, 3)
    
    def _calculate_reingestion_potential(
        self, analysis: Dict[str, Any]
    ) -> float:
        """Calculate reingestion potential based on evolution capacity"""
        base_potential = 0.5
        
        # High potential for consciousness-related files
        if analysis.get("consciousness_patterns"):
            base_potential += 0.3
            
        # High potential for polymorphic files
        if analysis.get("polymorphic_potential", 0.0) > 0.5:
            base_potential += 0.2
            
        return min(base_potential, 1.0)
    
    def _generate_ai_context_tags(
        self, file_path: Path, analysis: Dict[str, Any]
    ) -> List[str]:
        """Generate enhanced AI context tags"""
        tags = [file_path.suffix[1:]] if file_path.suffix else []
        
        # Add consciousness tags
        if analysis.get("consciousness_patterns"):
            tags.append("consciousness_emergence")
            
        # Add polymorphic tags
        if analysis.get("polymorphic_potential", 0.0) > 0.3:
            tags.append("polymorphic_intelligence")
            
        # Add AINLP tags
        if analysis.get("ainlp_compatibility", 0.0) > 0.3:
            tags.append("ainlp_compatible")
            
        # Add cellular tags
        if "cellular" in str(file_path).lower():
            tags.append("cellular_ai")
            
        return tags
    
    def _calculate_file_hash(self, file_path: Path) -> str:
        """Calculate file content hash for change detection"""
        try:
            content = file_path.read_bytes()
            return hashlib.md5(content).hexdigest()
        except Exception:
            return "hash_error"


# Load registry


def load_registry() -> Dict[str, Any]:
    """Load registry, resolving relocated live file or stub pointer.

    Stub format example (root): {"relocated": "runtime_intelligence/logs/aios_context/.aios_context.json"}
    """
    path = REGISTRY_PATH
    if not path.exists():
        print("[WARN] context registry not found; starting with empty {}")
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        # If this is the stub (contains only relocation pointer), follow it
        if path == REGISTRY_STUB_PATH and isinstance(data, dict) and "relocated" in data:
            relocated = Path(data["relocated"])
            if relocated.exists():
                with open(relocated, "r", encoding="utf-8") as rf:
                    return json.load(rf)
        return data if isinstance(data, dict) else {}
    except Exception as e:
        print(f"[WARN] failed to load context registry: {e}; using empty {}")
        return {}


# Scan files in the project directory


def scan_files(root):
    for dirpath, _, filenames in os.walk(root):
        for fname in filenames:
            fpath = Path(dirpath) / fname
            # Ignore hidden/system files
            if any(part.startswith(".") for part in fpath.parts):
                continue
            yield fpath.relative_to(root)


def is_relevant_file(fpath):
    # Ignore common build/output folders and files
    ignored_dirs = {
        "__pycache__",
        "venv",
        "node_modules",
        ".git",
        ".pytest_cache",
        ".vscode",
    }
    if any(part in ignored_dirs for part in fpath.parts):
        return False
    # Only include relevant file extensions
    relevant_exts = {
        ".py",
        ".cs",
        ".cpp",
        ".h",
        ".hpp",
        ".json",
        ".md",
        ".yml",
        ".yaml",
        ".toml",
        ".sln",
        ".ps1",
        ".sh",
        ".ts",
        ".js",
        ".html",
        ".xml",
        ".bat",
        ".ini",
        ".txt",
    }
    return fpath.suffix.lower() in relevant_exts


def guess_file_type(fpath):
    ext = fpath.suffix.lower()
    if ext in {".py", ".ps1", ".sh"}:
        if "test" in fpath.name.lower():
            return "testing"
        if "cell" in fpath.name.lower() or "cell" in str(fpath.parent).lower():
            return "cellular_ai"
        if "integration" in str(fpath.parent).lower():
            return "core_logic"
        return "core_logic"
    if ext in {".cs", ".cpp", ".h", ".hpp"}:
        return "core_logic"
    if ext in {".json", ".yml", ".yaml", ".toml", ".ini"}:
        return "configs"
    if ext in {".md", ".txt"}:
        return "documentation"
    if ext in {".sln"}:
        return "core_logic"
    if ext in {".html", ".xml", ".js", ".ts"}:
        return "core_logic"
    return "unknown"


def guess_tags(fpath):
    tags = []
    name = fpath.name.lower()
    if "tensorflow" in name:
        tags.append("tensorflow")
    if "cell" in name or "cell" in str(fpath.parent).lower():
        tags.append("cellular")
    if "ainlp" in name or "ainlp" in str(fpath.parent).lower():
        tags.append("ainlp")
    if "test" in name:
        tags.append("testing")
    if "integration" in str(fpath.parent).lower():
        tags.append("integration")
    if ext := fpath.suffix.lower():
        tags.append(ext.lstrip("."))
    return list(set(tags))


def file_content_hash(fpath):
    try:
        with open(fpath, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()
    except Exception:
        return ""


def autofix_registry(registry, missing_files, orphaned_files, yes=False):
    updated = False
    for f in missing_files:
        ftype = guess_file_type(f)
        tags = guess_tags(f)
        entry = {
            "file_type": ftype,
            "last_modified": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "last_accessed": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "access_frequency": 1.0,
            "modification_frequency": 1.0,
            "context_importance": 0.5,
            "reingestion_potential": 0.5,
            "file_classification": "active",
            "ai_context_tags": tags,
            "content_hash": file_content_hash(f),
            "size_bytes": f.stat().st_size if f.exists() else 0,
            "cellular_relationships": [],
        }
        registry[str(f)] = entry
        print(f"[AUTO-ADD] {f} -> {ftype}, tags: {tags}")
        updated = True
    for f in orphaned_files:
        if str(f) in registry:
            del registry[str(f)]
            print(f"[AUTO-REMOVE] {f}")
            updated = True
    if updated and (
            yes or input(
                "Write changes to .aios_context.json? [y/N] "
            ).lower().startswith("y")
    ):
        _write_json_atomic(REGISTRY_PATH, registry)
        print("Registry updated.")
    elif updated:
        print("No changes written.")
    else:
        print("No harmonization needed.")


def main():
    parser = argparse.ArgumentParser(
        description="AIOS Context Registry Validator & Autocoder"
    )
    parser.add_argument(
        "--autofix",
        action="store_true",
        help="Auto-harmonize registry (add/remove)",
    )
    parser.add_argument(
        "--yes", action="store_true", help="Write changes without prompt"
    )
    args = parser.parse_args()

    registry = load_registry()
    registered_files = set(Path(f) for f in registry.keys())
    actual_files = set(scan_files(PROJECT_ROOT))
    relevant_files = set(f for f in actual_files if is_relevant_file(f))
    missing_in_registry = relevant_files - registered_files
    orphaned_in_registry = registered_files - actual_files

    print("=== AIOS Context Registry Validation (Filtered) ===")
    print(f"Relevant files missing in registry: {len(missing_in_registry)}")
    for f in sorted(missing_in_registry):
        print(f"  [NEW] {f}")
    print(f"Orphaned files in registry: {len(orphaned_in_registry)}")
    for f in sorted(orphaned_in_registry):
        print(f"  [ORPHAN] {f}")
    print("Validation complete.")

    if args.autofix:
        autofix_registry(
            registry, missing_in_registry, orphaned_in_registry, yes=args.yes
        )
    else:
        # Run enhanced tachyonic context intelligence
        print("\n🌌 Launching Tachyonic Context Intelligence System...")
        tachyonic_system = TachyonicContextIntelligence()
        tachyonic_system.update_context_registry()


if __name__ == "__main__":
    main()
