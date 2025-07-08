"""
AIOS Documentation Mega-Consolidation Analysis
=============================================

PROBLEM: 43+ fragmented markdown files creating information overload
SOLUTION: Intelligent consolidation into 5-7 comprehensive guides
APPROACH: AINLP-driven content analysis and strategic merging
"""

import os
import re
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple


@dataclass
class DocumentProfile:
    """Profile of a documentation file for consolidation analysis."""
    path: Path
    name: str
    size_bytes: int
    line_count: int
    topics: Set[str]
    content_type: str  # specification, guide, reference, status, etc.
    consolidation_priority: float
    merge_candidates: List[str]
    last_modified: datetime


class AIOSDocumentationConsolidationAnalyzer:
    """Advanced documentation analysis for strategic consolidation."""

    def __init__(self, docs_dir: Path):
        self.docs_dir = Path(docs_dir)
        self.profiles: Dict[str, DocumentProfile] = {}

        # Content type patterns for classification
        self.content_patterns = {
            'specification': [
                'spec', 'specification', 'ainlp', 'requirements', 'standards'
            ],
            'architecture': [
                'architecture', 'design', 'system', 'structure', 'fractal', 'holographic'
            ],
            'guide': [
                'guide', 'setup', 'integration', 'development', 'installation', 'user'
            ],
            'reference': [
                'api', 'reference', 'commands', 'interface'
            ],
            'status': [
                'status', 'complete', 'summary', 'analysis', 'roadmap', 'changelog'
            ],
            'optimization': [
                'optimization', 'bugs', 'fixes', 'implementation', 'production'
            ],
            'context': [
                'context', 'harmonization', 'bootstrap', 'waypoint'
            ]
        }

        # Topic extraction patterns
        self.topic_patterns = {
            'ainlp': r'(?i)(ainlp|natural language programming)',
            'ui': r'(?i)(ui|interface|hybrid|webview|wpf|html)',
            'architecture': r'(?i)(architecture|design|system|core)',
            'api': r'(?i)(api|endpoint|service|method)',
            'integration': r'(?i)(integration|bridge|communication)',
            'optimization': r'(?i)(optimization|performance|bug|fix)',
            'context': r'(?i)(context|harmonization|fractal)',
            'python': r'(?i)(python|environment|pip|conda)',
            'csharp': r'(?i)(c#|csharp|\.net|wpf)',
            'cpp': r'(?i)(c\+\+|cpp|cmake|boost)',
            'vscode': r'(?i)(vscode|extension|workspace)',
            'setup': r'(?i)(setup|installation|deployment)',
            'testing': r'(?i)(test|testing|validation)',
            'documentation': r'(?i)(documentation|docs|guide)',
            'roadmap': r'(?i)(roadmap|plan|phase|milestone)'
        }

    def analyze_all_documents(self) -> Dict[str, DocumentProfile]:
        """Analyze all documentation files for consolidation opportunities."""
        print("🔍 Analyzing AIOS Documentation Structure...")
        print(f"📁 Scanning: {self.docs_dir}")

        md_files = list(self.docs_dir.glob("*.md"))
        print(f"📊 Found {len(md_files)} markdown files")

        for md_file in md_files:
            if md_file.is_file():
                profile = self._analyze_document(md_file)
                self.profiles[md_file.name] = profile

        # Calculate consolidation priorities and merge candidates
        self._calculate_consolidation_opportunities()

        return self.profiles

    def _analyze_document(self, filepath: Path) -> DocumentProfile:
        """Analyze a single document for content classification."""
        try:
            content = filepath.read_text(encoding='utf-8')
            lines = content.split('\n')

            # Extract topics
            topics = set()
            content_lower = content.lower()
            for topic, pattern in self.topic_patterns.items():
                if re.search(pattern, content_lower):
                    topics.add(topic)

            # Classify content type
            content_type = self._classify_content_type(filepath.name, content)

            # Calculate basic metrics
            stat = filepath.stat()

            profile = DocumentProfile(
                path=filepath,
                name=filepath.name,
                size_bytes=stat.st_size,
                line_count=len(lines),
                topics=topics,
                content_type=content_type,
                consolidation_priority=0.0,  # Will be calculated later
                merge_candidates=[],
                last_modified=datetime.fromtimestamp(stat.st_mtime)
            )

            return profile

        except Exception as e:
            print(f"❌ Error analyzing {filepath}: {e}")
            return DocumentProfile(
                path=filepath,
                name=filepath.name,
                size_bytes=0,
                line_count=0,
                topics=set(),
                content_type='unknown',
                consolidation_priority=0.0,
                merge_candidates=[],
                last_modified=datetime.now()
            )

    def _classify_content_type(self, filename: str, content: str) -> str:
        """Classify document content type based on name and content."""
        filename_lower = filename.lower()
        content_lower = content.lower()

        for content_type, keywords in self.content_patterns.items():
            for keyword in keywords:
                if keyword in filename_lower or keyword in content_lower:
                    return content_type

        return 'general'

    def _calculate_consolidation_opportunities(self):
        """Calculate consolidation priorities and identify merge candidates."""
        # Group documents by content type and topics
        content_groups = defaultdict(list)
        topic_groups = defaultdict(list)

        for name, profile in self.profiles.items():
            content_groups[profile.content_type].append(name)

            for topic in profile.topics:
                topic_groups[topic].append(name)

        # Calculate consolidation priority for each document
        for name, profile in self.profiles.items():
            priority = 0.0

            # Higher priority for small files (easier to consolidate)
            if profile.size_bytes < 5000:
                priority += 0.3
            elif profile.size_bytes < 15000:
                priority += 0.2

            # Higher priority for files with many similar documents
            same_type_count = len(content_groups[profile.content_type])
            if same_type_count > 3:
                priority += 0.4

            # Higher priority for overlapping topics
            topic_overlap = 0
            for topic in profile.topics:
                topic_overlap += len(topic_groups[topic])

            if topic_overlap > 5:
                priority += 0.3

            profile.consolidation_priority = min(priority, 1.0)

            # Find merge candidates (same type + overlapping topics)
            candidates = []
            for other_name, other_profile in self.profiles.items():
                if (other_name != name and
                    other_profile.content_type == profile.content_type and
                    profile.topics & other_profile.topics):
                    candidates.append(other_name)

            profile.merge_candidates = candidates[:5]  # Top 5 candidates

    def generate_consolidation_strategy(self) -> Dict[str, List[str]]:
        """Generate optimal consolidation strategy."""
        print("\n🎯 Generating Consolidation Strategy...")

        # Strategic consolidation groups
        consolidation_groups = {
            'AIOS_COMPLETE_SPECIFICATION_GUIDE.md': [],
            'AIOS_DEVELOPMENT_AND_INTEGRATION_GUIDE.md': [],
            'AIOS_API_AND_REFERENCE_GUIDE.md': [],
            'AIOS_ARCHITECTURE_AND_DESIGN_GUIDE.md': [],
            'AIOS_STATUS_AND_ROADMAP_GUIDE.md': [],
            'AIOS_OPTIMIZATION_AND_TROUBLESHOOTING_GUIDE.md': [],
            'AIOS_QUICK_START_AND_USER_GUIDE.md': []
        }

        # Classify documents into consolidation groups
        for name, profile in self.profiles.items():
            # Skip already optimized files
            if 'OPTIMIZED' in name or 'UNIFIED' in name or 'COMPLETE' in name:
                continue

            # Skip backup directories
            if name.startswith('tachyonic_'):
                continue

            # Strategic assignment based on content type and topics
            if profile.content_type == 'specification' or 'ainlp' in profile.topics:
                consolidation_groups['AIOS_COMPLETE_SPECIFICATION_GUIDE.md'].append(name)

            elif (profile.content_type == 'guide' or
                  'integration' in profile.topics or
                  'development' in profile.name.lower()):
                consolidation_groups['AIOS_DEVELOPMENT_AND_INTEGRATION_GUIDE.md'].append(name)

            elif profile.content_type == 'reference' or 'api' in profile.topics:
                consolidation_groups['AIOS_API_AND_REFERENCE_GUIDE.md'].append(name)

            elif (profile.content_type == 'architecture' or
                  'architecture' in profile.topics or
                  'fractal' in profile.topics):
                consolidation_groups['AIOS_ARCHITECTURE_AND_DESIGN_GUIDE.md'].append(name)

            elif (profile.content_type == 'status' or
                  'roadmap' in profile.topics or
                  'complete' in profile.name.lower()):
                consolidation_groups['AIOS_STATUS_AND_ROADMAP_GUIDE.md'].append(name)

            elif (profile.content_type == 'optimization' or
                  'optimization' in profile.topics or
                  'bug' in profile.name.lower()):
                consolidation_groups['AIOS_OPTIMIZATION_AND_TROUBLESHOOTING_GUIDE.md'].append(name)

            elif ('user' in profile.name.lower() or
                  'installation' in profile.topics or
                  'setup' in profile.topics):
                consolidation_groups['AIOS_QUICK_START_AND_USER_GUIDE.md'].append(name)

            else:
                # Default to development guide for uncategorized content
                consolidation_groups['AIOS_DEVELOPMENT_AND_INTEGRATION_GUIDE.md'].append(name)

        return consolidation_groups

    def print_analysis_report(self):
        """Print comprehensive analysis report."""
        print("\n" + "="*80)
        print("📊 AIOS DOCUMENTATION CONSOLIDATION ANALYSIS REPORT")
        print("="*80)

        total_files = len(self.profiles)
        total_size = sum(p.size_bytes for p in self.profiles.values())

        print(f"\n📈 CURRENT STATE:")
        print(f"   Total Files: {total_files}")
        print(f"   Total Size: {total_size:,} bytes ({total_size/1024:.1f} KB)")

        # Group by content type
        content_distribution = defaultdict(int)
        for profile in self.profiles.values():
            content_distribution[profile.content_type] += 1

        print(f"\n📋 CONTENT TYPE DISTRIBUTION:")
        for content_type, count in sorted(content_distribution.items()):
            percentage = (count / total_files) * 100
            print(f"   {content_type}: {count} files ({percentage:.1f}%)")

        # High consolidation priority files
        high_priority = [p for p in self.profiles.values() if p.consolidation_priority > 0.6]
        print(f"\n🎯 HIGH CONSOLIDATION PRIORITY ({len(high_priority)} files):")
        for profile in sorted(high_priority, key=lambda x: x.consolidation_priority, reverse=True):
            print(f"   • {profile.name} (priority: {profile.consolidation_priority:.2f})")

        # Generate consolidation strategy
        strategy = self.generate_consolidation_strategy()

        print(f"\n🔄 PROPOSED CONSOLIDATION STRATEGY:")
        print(f"   Current: {total_files} files → Target: {len(strategy)} unified guides")
        print(f"   Reduction: {total_files - len(strategy)} files ({((total_files - len(strategy))/total_files)*100:.1f}%)")

        print(f"\n📚 CONSOLIDATION GROUPS:")
        for target_file, source_files in strategy.items():
            if source_files:
                print(f"\n   🎯 {target_file}")
                print(f"      Sources ({len(source_files)}): {', '.join(source_files[:3])}")
                if len(source_files) > 3:
                    print(f"      + {len(source_files) - 3} more files...")


def main():
    """Main analysis execution."""
    docs_dir = Path(r"c:\dev\AIOS\docs")
    analyzer = AIOSDocumentationConsolidationAnalyzer(docs_dir)

    print("🚀 AIOS Documentation Consolidation Analysis")
    print("=" * 60)

    # Perform analysis
    profiles = analyzer.analyze_all_documents()

    # Print comprehensive report
    analyzer.print_analysis_report()

    print(f"\n✨ Analysis Complete!")
    print(f"📋 Ready for strategic consolidation implementation")


if __name__ == "__main__":
    main()
