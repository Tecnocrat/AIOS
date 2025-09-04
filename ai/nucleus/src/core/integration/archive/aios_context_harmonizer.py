"""
AIOS Context Harmonization Engine
================================

Intelligent context management system that integrates with AINLP logic
to automatically categorize, monitor, and organize project files based on
development patterns and reingestion potential.

Features:
- Smart file classification (active vs. reference vs. archival)
- AINLP kernel integration for context understanding
- Automatic monitoring of frequently accessed files
- Intelligent reingestion recommendations
- Clean development environment maintenance

Usage: Integrated into quantum bootstrap and AINLP compiler
"""

import hashlib
import json
import logging
import os
import time
from collections import defaultdict, deque
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple


@dataclass
class FileContextProfile:
    """Profile for tracking file context and usage patterns."""
    path: Path
    file_type: str
    last_modified: datetime
    last_accessed: datetime
    access_frequency: float = 0.0
    modification_frequency: float = 0.0
    context_importance: float = 0.0
    reingestion_potential: float = 0.0
    file_classification: str = "unknown"  # active, reference, archival, temporary
    dependencies: Set[str] = field(default_factory=set)
    ai_context_tags: List[str] = field(default_factory=list)
    content_hash: str = ""
    size_bytes: int = 0

    def calculate_importance_score(self) -> float:
        """Calculate overall importance score for context prioritization."""
        base_score = (
            self.access_frequency * 0.3 +
            self.modification_frequency * 0.4 +
            self.context_importance * 0.2 +
            self.reingestion_potential * 0.1
        )

        # Boost for certain file types
        type_multipliers = {
            "executable": 1.5,
            "core_logic": 1.4,
            "interface": 1.2,
            "configuration": 1.1,
            "documentation": 0.8,
            "backup": 0.3,
            "temporary": 0.1
        }

        multiplier = type_multipliers.get(self.file_type, 1.0)
        return min(base_score * multiplier, 1.0)


class AIOSContextHarmonizer:
    """
    Intelligent context harmonization system that understands
    file patterns and integrates with AINLP kernel for smart organization.
    """

    def __init__(self, root_path: Path):
        self.root_path = root_path
        self.profiles: Dict[str, FileContextProfile] = {}
        self.access_history: deque = deque(maxlen=1000)
        self.modification_history: deque = deque(maxlen=1000)
        self.logger = logging.getLogger("AIOS.ContextHarmonizer")

        # Classification rules
        self.active_patterns = {
            "executables": ["aios_quantum_bootstrap.py", "main.py", "app.py"],
            "core_logic": ["*.cs", "core/*.cpp", "core/*.hpp", "ai/src/core/**/*.py"],
            "interfaces": ["interface/**/*.xaml", "interface/**/*.cs", "vscode-extension/**/*.ts"],
            "configs": ["*.json", "*.yaml", "*.toml", "config/**/*"],
        }

        self.reference_patterns = {
            "documentation": ["docs/**/*.md", "README.md", "*.md"],
            "specifications": ["*_SPECIFICATION.md", "*_GUIDE.md"],
            "static_configs": [".gitignore", "*.code-workspace"],
        }

        self.archival_patterns = {
            "backups": ["*backup*", "*_backup_*", "archive/**/*"],
            "completed": ["*_COMPLETE.md", "*_COMPLETE_*.md"],
            "historical": ["*july*", "*_july_*", "*2025*"],
        }

        # Load existing context if available
        self.context_file = root_path / ".aios_context.json"
        self.load_context()

    def classify_file(self, file_path: Path) -> Tuple[str, str]:
        """
        Classify file type and context classification.
        Returns: (file_type, classification)
        """
        rel_path = file_path.relative_to(self.root_path)
        path_str = str(rel_path).replace("\\", "/")
        file_name = file_path.name

        # Check active patterns
        for category, patterns in self.active_patterns.items():
            for pattern in patterns:
                if self._matches_pattern(path_str, pattern) or self._matches_pattern(file_name, pattern):
                    return category, "active"

        # Check reference patterns
        for category, patterns in self.reference_patterns.items():
            for pattern in patterns:
                if self._matches_pattern(path_str, pattern) or self._matches_pattern(file_name, pattern):
                    return category, "reference"

        # Check archival patterns
        for category, patterns in self.archival_patterns.items():
            for pattern in patterns:
                if self._matches_pattern(path_str, pattern) or self._matches_pattern(file_name, pattern):
                    return category, "archival"

        # Default classification based on location
        if "archive" in path_str:
            return "archived", "archival"
        elif any(x in path_str for x in ["docs", "documentation"]):
            return "documentation", "reference"
        elif any(x in path_str for x in ["core", "ai", "interface"]):
            return "core_logic", "active"
        else:
            return "unknown", "reference"

    def _matches_pattern(self, path: str, pattern: str) -> bool:
        """Simple pattern matching for file classification."""
        import fnmatch

        if "**" in pattern:
            # Handle recursive patterns
            parts = pattern.split("**")
            if len(parts) == 2:
                prefix, suffix = parts
                return path.startswith(prefix) and path.endswith(suffix.lstrip("/"))

        return fnmatch.fnmatch(path, pattern)

    def scan_project_context(self):
        """
        Perform comprehensive project context scan to understand
        current file organization and usage patterns.
        """
        self.logger.info("🔍 Scanning AIOS project context...")

        # Scan all files
        for file_path in self.root_path.rglob("*"):
            if file_path.is_file() and not self._should_ignore(file_path):
                self._analyze_file(file_path)

        # Calculate importance scores
        self._calculate_importance_scores()

        # Generate recommendations
        recommendations = self._generate_harmonization_recommendations()

        # Save context
        self.save_context()

        return recommendations

    def _should_ignore(self, file_path: Path) -> bool:
        """Check if file should be ignored from context analysis."""
        ignore_patterns = [
            ".git/**",
            "**/__pycache__/**",
            "**/*.pyc",
            "**/*.pyo",
            "**/node_modules/**",
            "**/build/**",
            "**/bin/**",
            "**/obj/**",
            "**/.vs/**",
            "**/*.tmp",
            "**/*.cache",
        ]

        rel_path = str(file_path.relative_to(self.root_path)).replace("\\", "/")

        for pattern in ignore_patterns:
            if self._matches_pattern(rel_path, pattern):
                return True

        return False

    def _analyze_file(self, file_path: Path):
        """Analyze individual file for context profiling."""
        try:
            stat = file_path.stat()
            content_hash = self._calculate_file_hash(file_path)

            file_type, classification = self.classify_file(file_path)

            # Get or create profile
            path_key = str(file_path.relative_to(self.root_path))
            if path_key in self.profiles:
                profile = self.profiles[path_key]
                # Update existing profile
                if profile.content_hash != content_hash:
                    profile.last_modified = datetime.fromtimestamp(stat.st_mtime)
                    profile.content_hash = content_hash
                    profile.modification_frequency += 0.1
            else:
                # Create new profile
                profile = FileContextProfile(
                    path=file_path,
                    file_type=file_type,
                    last_modified=datetime.fromtimestamp(stat.st_mtime),
                    last_accessed=datetime.fromtimestamp(stat.st_atime),
                    file_classification=classification,
                    content_hash=content_hash,
                    size_bytes=stat.st_size
                )
                self.profiles[path_key] = profile

            # Analyze content for AI context tags
            self._extract_ai_context_tags(profile)

        except Exception as e:
            self.logger.warning(f"Error analyzing {file_path}: {e}")

    def _calculate_file_hash(self, file_path: Path) -> str:
        """Calculate hash of file content for change detection."""
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
                return hashlib.md5(content).hexdigest()
        except:
            return ""

    def _extract_ai_context_tags(self, profile: FileContextProfile):
        """Extract AI context tags from file content."""
        try:
            if profile.path.suffix in ['.py', '.cs', '.cpp', '.hpp', '.js', '.ts', '.md']:
                with open(profile.path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read().lower()

                    # AI-related tags
                    ai_keywords = [
                        "ainlp", "quantum", "fractal", "hyperlayer", "tachyonic",
                        "ai", "machine learning", "neural", "deep learning",
                        "natural language", "compiler", "bootstrap", "interface",
                        "core", "integration", "context", "consciousness"
                    ]

                    tags = []
                    for keyword in ai_keywords:
                        if keyword in content:
                            tags.append(keyword)

                    profile.ai_context_tags = tags

                    # Calculate context importance based on content
                    importance_indicators = [
                        "class", "def", "function", "public", "private",
                        "import", "using", "namespace", "async", "await"
                    ]

                    importance_score = sum(content.count(indicator) for indicator in importance_indicators)
                    profile.context_importance = min(importance_score / 100.0, 1.0)

        except Exception as e:
            self.logger.debug(f"Error extracting AI context from {profile.path}: {e}")

    def _calculate_importance_scores(self):
        """Calculate importance scores for all profiles."""
        now = datetime.now()

        for profile in self.profiles.values():
            # Calculate access frequency (recent access is more important)
            days_since_access = (now - profile.last_accessed).days
            profile.access_frequency = max(0, 1.0 - (days_since_access / 30.0))

            # Calculate modification frequency
            days_since_modification = (now - profile.last_modified).days
            profile.modification_frequency = max(0, 1.0 - (days_since_modification / 7.0))

            # Calculate reingestion potential
            profile.reingestion_potential = self._calculate_reingestion_potential(profile)

    def _calculate_reingestion_potential(self, profile: FileContextProfile) -> float:
        """Calculate potential for AI reingestion based on content and context."""
        potential = 0.0

        # High potential for executable code
        if profile.file_classification == "active":
            potential += 0.4

        # High potential for AI-related content
        ai_tag_score = len(profile.ai_context_tags) / 10.0
        potential += min(ai_tag_score, 0.3)

        # Medium potential for documentation with implementation details
        if profile.file_type == "documentation" and any(
            tag in profile.ai_context_tags for tag in ["implementation", "specification", "guide"]
        ):
            potential += 0.2

        # Low potential for archival/backup files
        if profile.file_classification == "archival":
            potential = min(potential, 0.2)

        return min(potential, 1.0)

    def _generate_harmonization_recommendations(self) -> Dict[str, Any]:
        """Generate intelligent recommendations for context harmonization."""
        recommendations = {
            "high_priority_monitoring": [],
            "safe_to_archive": [],
            "potential_cleanup": [],
            "ai_reingestion_candidates": [],
            "organization_suggestions": []
        }

        # Sort profiles by importance
        sorted_profiles = sorted(
            self.profiles.values(),
            key=lambda p: p.calculate_importance_score(),
            reverse=True
        )

        # High priority monitoring (top 20% most important)
        high_priority_count = max(1, len(sorted_profiles) // 5)
        recommendations["high_priority_monitoring"] = [
            {
                "file": str(p.path.relative_to(self.root_path)),
                "score": p.calculate_importance_score(),
                "classification": p.file_classification,
                "reason": f"{p.file_type} with high {self._get_primary_strength(p)}"
            }
            for p in sorted_profiles[:high_priority_count]
        ]

        # Safe to archive (low importance, old, archival classification)
        recommendations["safe_to_archive"] = [
            {
                "file": str(p.path.relative_to(self.root_path)),
                "score": p.calculate_importance_score(),
                "reason": f"Low activity, {p.file_classification} classification"
            }
            for p in sorted_profiles
            if (p.calculate_importance_score() < 0.2 and
                p.file_classification in ["archival", "backup"] and
                (datetime.now() - p.last_accessed).days > 7)
        ]

        # AI reingestion candidates
        recommendations["ai_reingestion_candidates"] = [
            {
                "file": str(p.path.relative_to(self.root_path)),
                "potential": p.reingestion_potential,
                "tags": p.ai_context_tags,
                "type": p.file_type
            }
            for p in sorted_profiles
            if p.reingestion_potential > 0.5
        ]

        # Organization suggestions
        active_files = [p for p in sorted_profiles if p.file_classification == "active"]
        archival_files = [p for p in sorted_profiles if p.file_classification == "archival"]

        if len(archival_files) > len(active_files) * 0.5:
            recommendations["organization_suggestions"].append({
                "type": "cleanup_archival",
                "message": f"Consider moving {len(archival_files)} archival files to organized archive structure",
                "impact": "Cleaner development environment"
            })

        root_files = [p for p in sorted_profiles if len(p.path.parts) == 1]
        if len(root_files) > 10:
            recommendations["organization_suggestions"].append({
                "type": "root_cleanup",
                "message": f"Root directory has {len(root_files)} files - consider organizing",
                "impact": "Improved navigation and context clarity"
            })

        return recommendations

    def _get_primary_strength(self, profile: FileContextProfile) -> str:
        """Get the primary strength/characteristic of a file profile."""
        scores = {
            "access": profile.access_frequency,
            "modification": profile.modification_frequency,
            "importance": profile.context_importance,
            "reingestion": profile.reingestion_potential
        }
        return max(scores, key=scores.get)

    def get_monitoring_targets(self) -> List[str]:
        """Get list of files that should be closely monitored."""
        high_importance = [
            p for p in self.profiles.values()
            if p.calculate_importance_score() > 0.6 and p.file_classification == "active"
        ]

        return [str(p.path.relative_to(self.root_path)) for p in high_importance]

    def save_context(self):
        """Save context profiles to disk."""
        try:
            context_data = {
                "last_scan": datetime.now().isoformat(),
                "profiles": {
                    path: {
                        "file_type": p.file_type,
                        "last_modified": p.last_modified.isoformat(),
                        "last_accessed": p.last_accessed.isoformat(),
                        "access_frequency": p.access_frequency,
                        "modification_frequency": p.modification_frequency,
                        "context_importance": p.context_importance,
                        "reingestion_potential": p.reingestion_potential,
                        "file_classification": p.file_classification,
                        "ai_context_tags": p.ai_context_tags,
                        "content_hash": p.content_hash,
                        "size_bytes": p.size_bytes
                    }
                    for path, p in self.profiles.items()
                }
            }

            with open(self.context_file, 'w') as f:
                json.dump(context_data, f, indent=2)

        except Exception as e:
            self.logger.error(f"Error saving context: {e}")

    def load_context(self):
        """Load context profiles from disk."""
        try:
            if self.context_file.exists():
                with open(self.context_file, 'r') as f:
                    context_data = json.load(f)

                for path, data in context_data.get("profiles", {}).items():
                    profile = FileContextProfile(
                        path=self.root_path / path,
                        file_type=data["file_type"],
                        last_modified=datetime.fromisoformat(data["last_modified"]),
                        last_accessed=datetime.fromisoformat(data["last_accessed"]),
                        access_frequency=data["access_frequency"],
                        modification_frequency=data["modification_frequency"],
                        context_importance=data["context_importance"],
                        reingestion_potential=data["reingestion_potential"],
                        file_classification=data["file_classification"],
                        ai_context_tags=data["ai_context_tags"],
                        content_hash=data["content_hash"],
                        size_bytes=data["size_bytes"]
                    )
                    self.profiles[path] = profile

        except Exception as e:
            self.logger.debug(f"No existing context to load: {e}")

    def integrate_with_ainlp(self, ainlp_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Integrate context harmonization with AINLP kernel logic.
        This creates the bridge between file organization and AI understanding.
        """
        integration_result = {
            "context_priorities": {},
            "reingestion_queue": [],
            "monitoring_targets": [],
            "cleanup_recommendations": []
        }

        # Get current AINLP priorities
        ainlp_priorities = ainlp_context.get("current_focus", [])

        # Map file profiles to AINLP priorities
        for priority in ainlp_priorities:
            related_files = [
                p for p in self.profiles.values()
                if any(tag in priority.lower() for tag in p.ai_context_tags) or
                   priority.lower() in str(p.path).lower()
            ]

            integration_result["context_priorities"][priority] = [
                {
                    "file": str(p.path.relative_to(self.root_path)),
                    "importance": p.calculate_importance_score(),
                    "tags": p.ai_context_tags
                }
                for p in sorted(related_files, key=lambda x: x.calculate_importance_score(), reverse=True)
            ]

        # Build reingestion queue based on AINLP needs and file potential
        integration_result["reingestion_queue"] = [
            {
                "file": str(p.path.relative_to(self.root_path)),
                "potential": p.reingestion_potential,
                "reason": f"High {self._get_primary_strength(p)} with AI tags: {p.ai_context_tags[:3]}"
            }
            for p in sorted(self.profiles.values(), key=lambda x: x.reingestion_potential, reverse=True)
            if p.reingestion_potential > 0.4
        ][:10]  # Top 10 candidates

        # Monitoring targets for AINLP context awareness
        integration_result["monitoring_targets"] = self.get_monitoring_targets()

        return integration_result


def initialize_context_harmonization(root_path: Path) -> AIOSContextHarmonizer:
    """Initialize and return configured context harmonization system."""
    harmonizer = AIOSContextHarmonizer(root_path)
    return harmonizer


# Integration point for quantum bootstrap
def get_harmonized_context_for_bootstrap() -> Dict[str, Any]:
    """Get harmonized context information for quantum bootstrap integration."""
    root_path = Path(__file__).parent
    harmonizer = initialize_context_harmonization(root_path)

    # Perform context scan
    recommendations = harmonizer.scan_project_context()

    # Create bootstrap context
    bootstrap_context = {
        "monitoring_targets": harmonizer.get_monitoring_targets(),
        "high_priority_files": [
            rec["file"] for rec in recommendations["high_priority_monitoring"]
        ],
        "ai_reingestion_candidates": recommendations["ai_reingestion_candidates"],
        "organization_status": {
            "total_files": len(harmonizer.profiles),
            "active_files": len([p for p in harmonizer.profiles.values() if p.file_classification == "active"]),
            "archival_files": len([p for p in harmonizer.profiles.values() if p.file_classification == "archival"]),
            "reference_files": len([p for p in harmonizer.profiles.values() if p.file_classification == "reference"])
        },
        "recommendations": recommendations
    }

    return bootstrap_context


if __name__ == "__main__":
    # Test the context harmonization
    root_path = Path(__file__).parent
    harmonizer = initialize_context_harmonization(root_path)
    recommendations = harmonizer.scan_project_context()

    print("🎯 AIOS Context Harmonization Results:")
    print(f"📁 Total files analyzed: {len(harmonizer.profiles)}")
    print(f"🔥 High priority monitoring: {len(recommendations['high_priority_monitoring'])}")
    print(f"🧠 AI reingestion candidates: {len(recommendations['ai_reingestion_candidates'])}")
    print(f"📋 Organization suggestions: {len(recommendations['organization_suggestions'])}")
