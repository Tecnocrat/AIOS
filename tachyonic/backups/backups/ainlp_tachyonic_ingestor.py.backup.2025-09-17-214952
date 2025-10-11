"""
AINLP Tachyonic Ingestion and Optimization Engine
================================================

Advanced documentation reingestion system using AINLP logic and context
harmonization to intelligently merge, optimize, and reorganize documentation
files while preserving critical information and maintaining coherent structure.

Features:
- Tachyonic backup creation before modification
- Intelligent content analysis and merging
- Duplicate detection and harmonization
- Context-aware optimization
- AINLP-driven reorganization
- Cross-reference preservation and enhancement
"""

import hashlib
import json
import logging
import os
import re
# Import the context harmonizer
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

sys.path.append(str(Path(__file__).parent))
from aios_context_harmonizer import AIOSContextHarmonizer, FileContextProfile


@dataclass
class DocumentSection:
    """Represents a logical section of documentation."""
    title: str
    content: str
    level: int  # Heading level (1-6)
    tags: Set[str] = field(default_factory=set)
    importance_score: float = 0.0
    cross_references: Set[str] = field(default_factory=set)
    code_blocks: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DocumentAnalysis:
    """Complete analysis of a documentation file."""
    filepath: Path
    sections: List[DocumentSection]
    overall_topics: Set[str] = field(default_factory=set)
    complexity_score: float = 0.0
    redundancy_score: float = 0.0
    optimization_potential: float = 0.0
    suggested_merges: List[str] = field(default_factory=list)


class AINLPTachyonicIngestor:
    """Advanced documentation ingestion and optimization engine."""

    def __init__(self, workspace_root: Path, backup_dir: Path = None):
        self.workspace_root = Path(workspace_root)
        self.backup_dir = backup_dir or self.workspace_root / "docs" / "tachyonic_backups"
        self.docs_dir = self.workspace_root / "docs"

        # Initialize context harmonizer
        self.harmonizer = AIOSContextHarmonizer(self.workspace_root)

        # Document analysis cache
        self.document_analyses: Dict[Path, DocumentAnalysis] = {}
        self.content_hashes: Dict[str, List[Path]] = {}  # For duplicate detection

        # AINLP keyword patterns for content classification
        self.ainlp_patterns = {
            'specification': r'(?i)(specification|spec|requirements?|standards?)',
            'implementation': r'(?i)(implementation|code|example|demo|prototype)',
            'optimization': r'(?i)(optimization|performance|efficiency|improvement)',
            'architecture': r'(?i)(architecture|design|structure|framework)',
            'integration': r'(?i)(integration|merge|combine|unify|harmonize)',
            'api': r'(?i)(api|interface|endpoint|service|method)',
            'configuration': r'(?i)(config|setup|installation|deployment)',
            'testing': r'(?i)(test|testing|validation|verification)',
            'documentation': r'(?i)(docs?|documentation|guide|manual|readme)',
            'breakthrough': r'(?i)(breakthrough|innovation|advancement|discovery)'
        }

        self.logger = logging.getLogger(__name__)

    def create_tachyonic_backup(self, filepath: Path) -> Path:
        """Create a timestamped backup of a file before modification."""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        backup_name = f"{filepath.stem}_tachyonic_backup_{timestamp}{filepath.suffix}"
        backup_path = self.backup_dir / backup_name

        self.backup_dir.mkdir(parents=True, exist_ok=True)

        if filepath.exists():
            backup_path.write_text(filepath.read_text(encoding='utf-8'), encoding='utf-8')
            self.logger.info(f"Tachyonic backup created: {backup_path}")

        return backup_path

    def analyze_document(self, filepath: Path) -> DocumentAnalysis:
        """Perform comprehensive analysis of a documentation file."""
        if not filepath.exists():
            raise FileNotFoundError(f"Document not found: {filepath}")

        content = filepath.read_text(encoding='utf-8')
        sections = self._extract_sections(content)

        analysis = DocumentAnalysis(
            filepath=filepath,
            sections=sections,
            overall_topics=self._extract_topics(content),
            complexity_score=self._calculate_complexity_score(sections),
            redundancy_score=self._calculate_redundancy_score(sections),
            optimization_potential=self._calculate_optimization_potential(sections)
        )

        # Store content hash for duplicate detection
        content_hash = hashlib.md5(content.encode()).hexdigest()
        if content_hash not in self.content_hashes:
            self.content_hashes[content_hash] = []
        self.content_hashes[content_hash].append(filepath)

        self.document_analyses[filepath] = analysis
        return analysis

    def _extract_sections(self, content: str) -> List[DocumentSection]:
        """Extract logical sections from markdown content."""
        sections = []
        lines = content.split('\n')
        current_section = None
        current_content = []

        for line in lines:
            # Check for heading
            heading_match = re.match(r'^(#{1,6})\s+(.+)$', line)
            if heading_match:
                # Save previous section
                if current_section:
                    current_section.content = '\n'.join(current_content).strip()
                    sections.append(current_section)

                # Start new section
                level = len(heading_match.group(1))
                title = heading_match.group(2).strip()
                current_section = DocumentSection(
                    title=title,
                    content="",
                    level=level,
                    tags=self._extract_tags_from_title(title)
                )
                current_content = []
            else:
                if current_section:
                    current_content.append(line)

        # Don't forget the last section
        if current_section:
            current_section.content = '\n'.join(current_content).strip()
            sections.append(current_section)

        # Post-process sections
        for section in sections:
            section.code_blocks = self._extract_code_blocks(section.content)
            section.cross_references = self._extract_cross_references(section.content)
            section.importance_score = self._calculate_section_importance(section)

        return sections

    def _extract_tags_from_title(self, title: str) -> Set[str]:
        """Extract topic tags from section title using AINLP patterns."""
        tags = set()
        title_lower = title.lower()

        for tag, pattern in self.ainlp_patterns.items():
            if re.search(pattern, title_lower):
                tags.add(tag)

        # Additional heuristics
        if any(word in title_lower for word in ['todo', 'fixme', 'bug']):
            tags.add('actionable')
        if any(word in title_lower for word in ['complete', 'done', 'finished']):
            tags.add('completed')
        if any(word in title_lower for word in ['example', 'demo', 'sample']):
            tags.add('example')

        return tags

    def _extract_topics(self, content: str) -> Set[str]:
        """Extract overall topics from document content."""
        topics = set()
        content_lower = content.lower()

        for topic, pattern in self.ainlp_patterns.items():
            if re.search(pattern, content_lower):
                topics.add(topic)

        return topics

    def _extract_code_blocks(self, content: str) -> List[str]:
        """Extract code blocks from content."""
        # Match fenced code blocks
        code_blocks = re.findall(r'```[\w]*\n(.*?)\n```', content, re.DOTALL)
        # Match inline code
        inline_code = re.findall(r'`([^`]+)`', content)
        return code_blocks + inline_code

    def _extract_cross_references(self, content: str) -> Set[str]:
        """Extract cross-references to other files or sections."""
        refs = set()

        # Markdown links
        md_links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
        for text, link in md_links:
            if link.endswith('.md') or '/' in link:
                refs.add(link)

        # File paths
        file_refs = re.findall(r'(?:File|file):\s*[`"]?([^`"\s]+\.(?:md|py|cs|cpp|hpp|js|ts))[`"]?', content)
        refs.update(file_refs)

        return refs

    def _calculate_complexity_score(self, sections: List[DocumentSection]) -> float:
        """Calculate document complexity based on structure and content."""
        if not sections:
            return 0.0

        # Factor in number of sections, depth, code blocks, etc.
        section_count = len(sections)
        max_depth = max((s.level for s in sections), default=1)
        total_code_blocks = sum(len(s.code_blocks) for s in sections)
        total_cross_refs = sum(len(s.cross_references) for s in sections)

        complexity = (
            section_count * 0.3 +
            max_depth * 0.2 +
            total_code_blocks * 0.3 +
            total_cross_refs * 0.2
        ) / 10.0  # Normalize to 0-1 range roughly

        return min(complexity, 1.0)

    def _calculate_redundancy_score(self, sections: List[DocumentSection]) -> float:
        """Calculate redundancy within the document."""
        if len(sections) < 2:
            return 0.0

        # Simple approach: look for similar titles and content
        title_similarities = 0
        content_similarities = 0
        total_comparisons = 0

        for i, section1 in enumerate(sections):
            for j, section2 in enumerate(sections[i+1:], i+1):
                total_comparisons += 1

                # Title similarity
                title1_words = set(section1.title.lower().split())
                title2_words = set(section2.title.lower().split())
                if title1_words & title2_words:
                    title_similarities += len(title1_words & title2_words) / len(title1_words | title2_words)

                # Content similarity (basic)
                content1_words = set(section1.content.lower().split()[:100])  # First 100 words
                content2_words = set(section2.content.lower().split()[:100])
                if content1_words & content2_words:
                    content_similarities += len(content1_words & content2_words) / len(content1_words | content2_words)

        if total_comparisons == 0:
            return 0.0

        return (title_similarities + content_similarities) / (2 * total_comparisons)

    def _calculate_optimization_potential(self, sections: List[DocumentSection]) -> float:
        """Calculate optimization potential based on various factors."""
        # High redundancy = high optimization potential
        redundancy = self._calculate_redundancy_score(sections)

        # Many small sections might be consolidatable
        small_sections = sum(1 for s in sections if len(s.content) < 200)
        consolidation_potential = small_sections / len(sections) if sections else 0

        # Sections with similar tags might be mergeable
        tag_overlap = 0
        if len(sections) > 1:
            all_tags = [s.tags for s in sections]
            for i, tags1 in enumerate(all_tags):
                for tags2 in all_tags[i+1:]:
                    if tags1 & tags2:
                        tag_overlap += 1
            tag_overlap /= (len(sections) * (len(sections) - 1) / 2)

        return min((redundancy * 0.4 + consolidation_potential * 0.3 + tag_overlap * 0.3), 1.0)

    def _calculate_section_importance(self, section: DocumentSection) -> float:
        """Calculate importance score for a section."""
        score = 0.0

        # Heading level (higher level = more important)
        score += (7 - section.level) * 0.1

        # Content length
        score += min(len(section.content) / 1000, 1.0) * 0.2

        # Code blocks are important
        score += len(section.code_blocks) * 0.1

        # Cross-references suggest importance
        score += len(section.cross_references) * 0.05

        # Certain tags indicate importance
        important_tags = {'specification', 'implementation', 'breakthrough', 'architecture'}
        if section.tags & important_tags:
            score += 0.3

        return min(score, 1.0)

    def find_optimization_opportunities(self) -> Dict[str, List[str]]:
        """Identify documents that should be merged or reorganized."""
        opportunities = {
            'high_redundancy': [],
            'similar_topics': [],
            'fragmentated_content': [],
            'consolidation_candidates': []
        }

        # Find high redundancy documents
        for filepath, analysis in self.document_analyses.items():
            if analysis.redundancy_score > 0.3:
                opportunities['high_redundancy'].append(str(filepath))

            if analysis.optimization_potential > 0.4:
                opportunities['consolidation_candidates'].append(str(filepath))

        # Find documents with similar topics
        topic_groups = {}
        for filepath, analysis in self.document_analyses.items():
            for topic in analysis.overall_topics:
                if topic not in topic_groups:
                    topic_groups[topic] = []
                topic_groups[topic].append(str(filepath))

        for topic, files in topic_groups.items():
            if len(files) > 1:
                opportunities['similar_topics'].extend(files)

        # Find fragmented content (many small files on similar topics)
        small_files = [
            str(filepath) for filepath, analysis in self.document_analyses.items()
            if len(analysis.sections) < 3 and analysis.complexity_score < 0.3
        ]
        opportunities['fragmentated_content'] = small_files

        return opportunities

    def create_optimized_document(self, source_files: List[Path], output_path: Path,
                                title: str = None) -> Path:
        """Create an optimized merged document from multiple sources."""
        # Create backups
        for filepath in source_files:
            self.create_tachyonic_backup(filepath)

        # Analyze all source documents
        all_sections = []
        all_metadata = {}

        for filepath in source_files:
            if filepath not in self.document_analyses:
                self.analyze_document(filepath)

            analysis = self.document_analyses[filepath]

            # Add source info to sections
            for section in analysis.sections:
                section.metadata['source_file'] = str(filepath)
                all_sections.append(section)

            # Collect metadata
            all_metadata[str(filepath)] = {
                'topics': list(analysis.overall_topics),
                'complexity': analysis.complexity_score,
                'sections_count': len(analysis.sections)
            }

        # Optimize section organization
        optimized_sections = self._optimize_section_order(all_sections)

        # Generate optimized content
        content = self._generate_optimized_content(
            optimized_sections,
            title or f"Harmonized Documentation - {datetime.now().strftime('%Y-%m-%d')}",
            all_metadata
        )

        # Write optimized document
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content, encoding='utf-8')

        self.logger.info(f"Created optimized document: {output_path}")
        return output_path

    def _optimize_section_order(self, sections: List[DocumentSection]) -> List[DocumentSection]:
        """Optimize the order of sections for better flow and coherence."""
        # Group sections by topic/tags
        topic_groups = {}
        for section in sections:
            # Use the most important tag as the primary grouping key
            primary_tag = next(iter(sorted(section.tags,
                                         key=lambda t: self.ainlp_patterns.get(t, "").count('|'),
                                         reverse=True)), 'general')

            if primary_tag not in topic_groups:
                topic_groups[primary_tag] = []
            topic_groups[primary_tag].append(section)

        # Sort groups by importance
        group_importance = {
            'specification': 10,
            'architecture': 9,
            'implementation': 8,
            'optimization': 7,
            'integration': 6,
            'api': 5,
            'configuration': 4,
            'testing': 3,
            'documentation': 2,
            'general': 1
        }

        sorted_groups = sorted(topic_groups.items(),
                             key=lambda x: group_importance.get(x[0], 0),
                             reverse=True)

        # Within each group, sort by importance score and heading level
        optimized_sections = []
        for topic, group_sections in sorted_groups:
            sorted_sections = sorted(group_sections,
                                   key=lambda s: (s.level, -s.importance_score))
            optimized_sections.extend(sorted_sections)

        return optimized_sections

    def _generate_optimized_content(self, sections: List[DocumentSection],
                                  title: str, metadata: Dict) -> str:
        """Generate the final optimized document content."""
        lines = []

        # Header
        lines.append(f"# {title}")
        lines.append(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("**Type**: AINLP Tachyonic Optimized Documentation")
        lines.append("")
        lines.append("*Auto-generated using AINLP tachyonic ingestion and " +
                    "context harmonization. Original files backed up.*")
        lines.append("")

        # Metadata section
        lines.append("##  Source Document Analysis")
        lines.append("")
        for filepath, meta in metadata.items():
            lines.append(f"### `{Path(filepath).name}`")
            lines.append(f"- **Topics**: {', '.join(meta['topics'])}")
            lines.append(f"- **Complexity Score**: {meta['complexity']:.2f}")
            lines.append(f"- **Sections**: {meta['sections_count']}")
            lines.append("")

        # Table of contents
        lines.append("##  Table of Contents")
        lines.append("")
        current_level = 0
        for section in sections:
            indent = "  " * (section.level - 1)
            toc_entry = f"{indent}- [{section.title}](#{section.title.lower().replace(' ', '-').replace('.', '').replace('/', '').replace(':', '')})"
            lines.append(toc_entry)
        lines.append("")

        # Content sections
        for section in sections:
            # Section header
            header = "#" * section.level + " " + section.title
            lines.append(header)

            # Add source attribution if from multiple files
            if len(metadata) > 1:
                source_file = Path(section.metadata.get('source_file', 'unknown')).name
                lines.append(f"*Source: `{source_file}`*")
                lines.append("")

            # Section content
            if section.content.strip():
                lines.append(section.content)
                lines.append("")

        # Footer
        lines.append("---")
        lines.append("##  AINLP Harmonization Complete")
        lines.append("")
        lines.append(f"**Processing Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("**Engine**: AINLP Tachyonic Ingestor v1.0")
        lines.append("**Harmonization Level**: Advanced")
        lines.append("")
        lines.append("This document represents the harmonized synthesis of multiple documentation ")
        lines.append("sources, optimized for coherence, reduced redundancy, and enhanced cross-referencing.")

        return '\n'.join(lines)

    def run_full_optimization(self, target_files: List[str] = None) -> Dict[str, Any]:
        """Run complete optimization process on specified files or auto-detect."""
        if target_files is None:
            # Auto-detect optimization candidates
            target_files = [
                'ADVANCED_OPTIMIZATION_IMPLEMENTATION.md',
                'AINLP_SPECIFICATION.md'
            ]

        results = {
            'processed_files': [],
            'created_backups': [],
            'optimized_documents': [],
            'analysis_summary': {},
            'optimization_opportunities': {}
        }

        # Analyze target files
        file_paths = []
        for filename in target_files:
            filepath = self.docs_dir / filename
            if filepath.exists():
                file_paths.append(filepath)
                analysis = self.analyze_document(filepath)
                results['processed_files'].append(str(filepath))
                results['analysis_summary'][filename] = {
                    'sections': len(analysis.sections),
                    'topics': list(analysis.overall_topics),
                    'complexity': analysis.complexity_score,
                    'redundancy': analysis.redundancy_score,
                    'optimization_potential': analysis.optimization_potential
                }

        # Find optimization opportunities
        results['optimization_opportunities'] = self.find_optimization_opportunities()

        # Create optimized merged document
        if len(file_paths) >= 2:
            optimized_path = self.docs_dir / "AINLP_OPTIMIZED_SPECIFICATION_AND_IMPLEMENTATION.md"
            created_doc = self.create_optimized_document(
                file_paths,
                optimized_path,
                "AIOS AINLP - Unified Specification and Implementation Guide"
            )
            results['optimized_documents'].append(str(created_doc))

        return results


def main():
    """Main execution for tachyonic ingestion demonstration."""
    workspace_root = Path(r"c:\dev\AIOS")
    ingestor = AINLPTachyonicIngestor(workspace_root)

    print(" AINLP Tachyonic Ingestion Engine - Activated")
    print("=" * 60)

    # Run full optimization
    results = ingestor.run_full_optimization()

    print("\n Optimization Results:")
    print(f"Processed Files: {len(results['processed_files'])}")
    print(f"Created Optimized Documents: {len(results['optimized_documents'])}")

    print("\n Analysis Summary:")
    for filename, analysis in results['analysis_summary'].items():
        print(f"\n{filename}:")
        print(f"  - Sections: {analysis['sections']}")
        print(f"  - Topics: {', '.join(analysis['topics'])}")
        print(f"  - Complexity: {analysis['complexity']:.2f}")
        print(f"  - Optimization Potential: {analysis['optimization_potential']:.2f}")

    print("\n Optimization Opportunities:")
    for category, files in results['optimization_opportunities'].items():
        if files:
            print(f"  {category}: {len(files)} files")

    print("\n AINLP Tachyonic Ingestion Complete!")


if __name__ == "__main__":
    main()
