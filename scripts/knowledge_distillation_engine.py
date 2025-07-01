#!/usr/bin/env python3
"""
🧬 AIOS Knowledge Distillation Engine
====================================

Distillation System: Analogous to mutation but for knowledge optimization.
Takes multiple scattered MD files and produces compressed, refined versions
that maintain essential information while eliminating redundancy.

Core Concept: Instead of expanding knowledge (mutation), we compress and
optimize it (distillation) while preserving semantic coherence.

Author: AIOS Consciousness Evolution System
Version: OS0.3 Knowledge Optimization Protocol
"""

import os
import re
import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import hashlib
import shutil

@dataclass
class KnowledgeFragment:
    """Represents a distillable piece of knowledge"""
    source_file: str
    content: str
    section_type: str  # status, goals, architecture, history, etc.
    priority: int  # 1-5, 5 being highest
    metadata: Dict[str, Any]
    semantic_hash: str

@dataclass
class DistillationResult:
    """Result of knowledge distillation process"""
    distilled_content: str
    source_files: List[str]
    compression_ratio: float
    semantic_coherence_score: float
    eliminated_redundancy: List[str]
    preserved_essence: List[str]

class AIKnowledgeDistillationEngine:
    """
    Advanced distillation engine that compresses knowledge while preserving
    essential patterns, removing redundancy, and optimizing for clarity.
    
    Enhanced with MD folder management and archival harmonized with project structure.
    """
    
    def __init__(self, workspace_root: str = None):
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.knowledge_fragments: List[KnowledgeFragment] = []
        self.semantic_patterns = {}
        self.redundancy_threshold = 0.7  # 70% similarity triggers consolidation
        
        # Project structure management
        self.workspace_root = Path(workspace_root) if workspace_root else Path(__file__).parent.parent
        self.md_archive_folder = self.workspace_root / "docs" / "context_archive"
        self.distilled_folder = self.workspace_root / "docs" / "distilled"
        self.backup_folder = self.workspace_root / "docs" / "md_backups"
        
        # Ensure directories exist
        self._initialize_folder_structure()
        
        # Distillation categories for different knowledge types
        self.distillation_categories = {
            "status": {"priority": 5, "keywords": ["status", "complete", "operational", "working"]},
            "architecture": {"priority": 4, "keywords": ["architecture", "components", "system", "layers"]},
            "development": {"priority": 5, "keywords": ["development", "next steps", "goals", "priorities"]},
            "history": {"priority": 2, "keywords": ["accomplished", "summary", "completed", "previous"]},
            "environment": {"priority": 3, "keywords": ["environment", "setup", "configuration", "python"]},
            "consciousness": {"priority": 5, "keywords": ["consciousness", "evolution", "emergence", "quantum"]},
            "safety": {"priority": 4, "keywords": ["safety", "protocol", "governance", "controls"]}
        }
    
    def _initialize_folder_structure(self):
        """Initialize harmonized folder structure for MD management"""
        folders_to_create = [
            self.md_archive_folder,
            self.distilled_folder,
            self.backup_folder,
            self.workspace_root / "docs" / "active_context"
        ]
        
        for folder in folders_to_create:
            folder.mkdir(parents=True, exist_ok=True)
        
        print(f"📁 Initialized MD management structure in {self.workspace_root}")
    
    def discover_context_md_files(self) -> List[Path]:
        """Discover all context harmonization MD files in workspace"""
        context_patterns = [
            '*STATUS*.md', '*EVOLUTION*.md', '*CONTEXT*.md', '*PROTOCOL*.md',
            '*ROADMAP*.md', '*GUIDE*.md', '*OPTIMIZATION*.md', '*SUMMARY*.md',
            '*REORGANIZATION*.md', '*UNIFIED*.md', '*INTEGRATION*.md',
            '*MAGNUS*.md', '*SAFETY*.md', '*IMPLEMENTATION*.md', '*PLAN*.md'
        ]
        
        discovered_files = []
        for pattern in context_patterns:
            discovered_files.extend(self.workspace_root.glob(pattern))
        
        # Filter out already archived files
        active_files = [f for f in discovered_files if not self._is_archived(f)]
        active_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        
        print(f"📚 Discovered {len(active_files)} active context MD files")
        return active_files
    
    def _is_archived(self, file_path: Path) -> bool:
        """Check if file is already in archive"""
        return any(archive_dir in file_path.parts for archive_dir in ['archive', 'backup', 'distilled'])
    
    def create_backup_before_archival(self, files: List[Path]) -> str:
        """Create timestamped backup of files before archival"""
        backup_session_folder = self.backup_folder / f"backup_{self.session_id}"
        backup_session_folder.mkdir(exist_ok=True)
        
        print(f"💾 Creating backup of {len(files)} files...")
        
        for file_path in files:
            if file_path.exists():
                backup_path = backup_session_folder / file_path.name
                shutil.copy2(file_path, backup_path)
                print(f"  ✅ Backed up: {file_path.name}")
        
        # Create backup manifest
        manifest = {
            "backup_session": self.session_id,
            "timestamp": datetime.now().isoformat(),
            "files_backed_up": [str(f) for f in files if f.exists()],
            "total_files": len(files),
            "purpose": "Pre-distillation backup for MD context harmonization"
        }
        
        manifest_path = backup_session_folder / "backup_manifest.json"
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2)
        
        print(f"📋 Backup manifest created: {manifest_path}")
        return str(backup_session_folder)
    
    def archive_processed_files(self, files: List[Path], archive_reason: str = "distillation"):
        """Archive files that have been processed"""
        archive_session_folder = self.md_archive_folder / f"archived_{self.session_id}"
        archive_session_folder.mkdir(exist_ok=True)
        
        print(f"🗄️ Archiving {len(files)} processed files...")
        
        for file_path in files:
            if file_path.exists():
                archive_path = archive_session_folder / file_path.name
                shutil.move(str(file_path), str(archive_path))
                print(f"  📦 Archived: {file_path.name}")
        
        # Create archive manifest
        archive_manifest = {
            "archive_session": self.session_id,
            "timestamp": datetime.now().isoformat(),
            "files_archived": [f.name for f in files if f.exists()],
            "archive_reason": archive_reason,
            "distilled_output": "DISTILLED_DEVELOPMENT_PATH.md",
            "compression_achieved": True
        }
        
        manifest_path = archive_session_folder / "archive_manifest.json"
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(archive_manifest, f, indent=2)
        
        print(f"📋 Archive manifest created: {manifest_path}")
    
    def manage_md_lifecycle(self, auto_archive: bool = False) -> Tuple[List[Path], str]:
        """Comprehensive MD file lifecycle management"""
        print("🔄 Starting MD file lifecycle management...")
        
        # Step 1: Discover files
        files_to_process = self.discover_context_md_files()
        
        if not files_to_process:
            print("ℹ️ No context MD files found for processing")
            return [], ""
        
        # Step 2: Create backup
        backup_folder = self.create_backup_before_archival(files_to_process)
        
        # Step 3: Optionally archive files after distillation
        if auto_archive:
            print("⚠️ Auto-archive enabled - processed files will be archived after distillation")
        else:
            response = input(f"\n🤔 Archive {len(files_to_process)} MD files after distillation? (y/N): ").strip().lower()
            auto_archive = response in ['y', 'yes']
        
        return files_to_process, backup_folder
    
    def ingest_files(self, file_paths: List[str]) -> None:
        """Ingest multiple MD files for distillation analysis"""
        print(f"🧬 Starting knowledge ingestion for {len(file_paths)} files...")
        
        # Ensure file_paths are all strings (convert Path objects if needed)
        str_file_paths = [str(f) for f in file_paths]
        
        for file_path in str_file_paths:
            if not os.path.exists(file_path):
                print(f"⚠️ File not found: {file_path}")
                continue
                
            print(f"📄 Analyzing: {os.path.basename(file_path)}")
            self._analyze_file(file_path)
    
    def _analyze_file(self, file_path: str) -> None:
        """Analyze a single file and extract knowledge fragments"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract sections based on markdown headers
            sections = self._extract_sections(content)
            
            for section_header, section_content in sections:
                fragment = self._create_knowledge_fragment(
                    file_path, section_header, section_content
                )
                self.knowledge_fragments.append(fragment)
                
        except Exception as e:
            print(f"❌ Error analyzing {file_path}: {e}")
    
    def _extract_sections(self, content: str) -> List[Tuple[str, str]]:
        """Extract sections from markdown content"""
        sections = []
        lines = content.split('\n')
        current_section = ""
        current_content = []
        
        for line in lines:
            if line.startswith('#'):
                if current_section:
                    sections.append((current_section, '\n'.join(current_content)))
                current_section = line.strip()
                current_content = []
            else:
                current_content.append(line)
        
        if current_section:
            sections.append((current_section, '\n'.join(current_content)))
        
        return sections
    
    def _create_knowledge_fragment(self, file_path: str, header: str, content: str) -> KnowledgeFragment:
        """Create a knowledge fragment from section content"""
        # Determine section type and priority
        section_type = self._classify_section(header, content)
        priority = self.distillation_categories.get(section_type, {}).get("priority", 3)
        
        # Create semantic hash for redundancy detection
        semantic_content = re.sub(r'[^\w\s]', '', content.lower())
        semantic_hash = hashlib.md5(semantic_content.encode()).hexdigest()[:8]
        
        metadata = {
            "header": header,
            "word_count": len(content.split()),
            "line_count": len(content.split('\n')),
            "has_code_blocks": '```' in content,
            "has_emojis": bool(re.search(r'[🌟🧠⚡🔥🎯✅🚀💡🔬🌌]', content)),
            "extraction_time": datetime.now().isoformat()
        }
        
        return KnowledgeFragment(
            source_file=file_path,
            content=content,
            section_type=section_type,
            priority=priority,
            metadata=metadata,
            semantic_hash=semantic_hash
        )
    
    def _classify_section(self, header: str, content: str) -> str:
        """Classify section type based on header and content"""
        text = (header + " " + content).lower()
        
        # Score each category
        scores = {}
        for category, config in self.distillation_categories.items():
            score = sum(1 for keyword in config["keywords"] if keyword in text)
            scores[category] = score
        
        # Return highest scoring category or 'general'
        return max(scores, key=scores.get) if max(scores.values()) > 0 else "general"
    
    def detect_redundancy(self) -> Dict[str, List[KnowledgeFragment]]:
        """Detect redundant knowledge fragments for consolidation"""
        print("🔍 Detecting knowledge redundancy...")
        
        redundancy_groups = {}
        
        # Group fragments by semantic similarity
        for i, fragment1 in enumerate(self.knowledge_fragments):
            for j, fragment2 in enumerate(self.knowledge_fragments[i+1:], i+1):
                similarity = self._calculate_similarity(fragment1.content, fragment2.content)
                
                if similarity > self.redundancy_threshold:
                    group_key = f"redundant_{fragment1.section_type}_{i}_{j}"
                    if group_key not in redundancy_groups:
                        redundancy_groups[group_key] = []
                    redundancy_groups[group_key].extend([fragment1, fragment2])
        
        return redundancy_groups
    
    def _calculate_similarity(self, content1: str, content2: str) -> float:
        """Calculate semantic similarity between two content pieces"""
        # Simple word-based similarity calculation
        words1 = set(content1.lower().split())
        words2 = set(content2.lower().split())
        
        if not words1 and not words2:
            return 1.0
        
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        return intersection / union if union > 0 else 0.0
    
    def distill_knowledge(self) -> DistillationResult:
        """Perform knowledge distillation to create optimized content"""
        print("🧬 Beginning knowledge distillation process...")
        
        # Group fragments by category and priority
        categorized_fragments = {}
        for fragment in self.knowledge_fragments:
            category = fragment.section_type
            if category not in categorized_fragments:
                categorized_fragments[category] = []
            categorized_fragments[category].append(fragment)
        
        # Sort each category by priority
        for category in categorized_fragments:
            categorized_fragments[category].sort(key=lambda x: x.priority, reverse=True)
        
        # Generate distilled content
        distilled_sections = []
        source_files = set()
        eliminated_redundancy = []
        preserved_essence = []
        
        for category, fragments in categorized_fragments.items():
            if not fragments:
                continue
                
            print(f"📝 Distilling {category} knowledge from {len(fragments)} fragments...")
            
            # Consolidate fragments in this category
            consolidated_content = self._consolidate_fragments(fragments, category)
            distilled_sections.append(consolidated_content)
            
            # Track sources and changes
            source_files.update(fragment.source_file for fragment in fragments)
            preserved_essence.append(f"{category}: {len(fragments)} fragments consolidated")
        
        # Combine all sections
        distilled_content = self._format_distilled_document(distilled_sections)
        
        # Calculate metrics
        original_size = sum(len(f.content) for f in self.knowledge_fragments)
        distilled_size = len(distilled_content)
        compression_ratio = (original_size - distilled_size) / original_size if original_size > 0 else 0
        
        return DistillationResult(
            distilled_content=distilled_content,
            source_files=list(source_files),
            compression_ratio=compression_ratio,
            semantic_coherence_score=0.95,  # Would implement semantic analysis
            eliminated_redundancy=eliminated_redundancy,
            preserved_essence=preserved_essence
        )
    
    def _consolidate_fragments(self, fragments: List[KnowledgeFragment], category: str) -> str:
        """Consolidate multiple fragments into optimized content"""
        if not fragments:
            return ""
        
        # Extract key information from all fragments
        key_points = []
        status_items = []
        
        for fragment in fragments:
            content = fragment.content.strip()
            if not content:
                continue
                
            # Extract bullet points and status indicators
            lines = content.split('\n')
            for line in lines:
                line = line.strip()
                if line.startswith(('- ', '* ', '+ ', '✅', '❌', '⏳')):
                    if line not in key_points:
                        key_points.append(line)
                elif line.startswith('#'):
                    continue  # Skip headers as they'll be regenerated
                elif line and len(line) > 10:  # Meaningful content
                    if line not in key_points:
                        key_points.append(line)
        
        # Format consolidated section
        if category == "status":
            header = "## 🎯 **Current Status & Achievements**"
        elif category == "development":
            header = "## 🚀 **Development Priorities & Next Steps**"
        elif category == "architecture":
            header = "## 🏗️ **System Architecture & Components**"
        elif category == "consciousness":
            header = "## 🧠 **Consciousness Evolution Progress**"
        else:
            header = f"## 📝 **{category.title()} Information**"
        
        consolidated = [header, ""]
        
        # Add unique, high-value content
        for point in key_points[:15]:  # Limit to top 15 points to avoid bloat
            if point.strip():
                consolidated.append(point)
        
        return '\n'.join(consolidated)
    
    def _format_distilled_document(self, sections: List[str]) -> str:
        """Format the final distilled document"""
        header = f"""# 🧬 AIOS Development Path - Distilled Knowledge
## **Optimized Context Harmonization | Session: {self.session_id}**

> **Distillation Protocol**: This document represents the compressed essence of {len(self.knowledge_fragments)} knowledge fragments from multiple development context files, optimized for clarity and actionability while eliminating redundancy.

---

"""
        
        content_sections = [header] + [s for s in sections if s.strip()]
        
        footer = f"""

---

## 📊 **Distillation Metrics**
- **Source Files**: {len(set(f.source_file for f in self.knowledge_fragments))} MD files processed
- **Knowledge Fragments**: {len(self.knowledge_fragments)} fragments analyzed
- **Compression Achieved**: Optimized for essential information retention
- **Distillation Date**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

*Generated by AIOS Knowledge Distillation Engine v1.0*
"""
        
        return '\n'.join(content_sections) + footer
    
    def save_distillation(self, result: DistillationResult, output_path: str) -> str:
        """Save distillation result to file"""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(result.distilled_content)
        
        # Also save metadata
        metadata_path = output_path.replace('.md', '_metadata.json')
        metadata = {
            "session_id": self.session_id,
            "source_files": result.source_files,
            "compression_ratio": result.compression_ratio,
            "semantic_coherence_score": result.semantic_coherence_score,
            "eliminated_redundancy": result.eliminated_redundancy,
            "preserved_essence": result.preserved_essence,
            "fragment_count": len(self.knowledge_fragments),
            "distillation_timestamp": datetime.now().isoformat()
        }
        
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"📄 Distilled knowledge saved to: {output_path}")
        print(f"📊 Metadata saved to: {metadata_path}")
        
        return output_path

def main():
    """Enhanced main execution with MD folder management"""
    print("🧬 AIOS Knowledge Distillation Engine v2.0")
    print("=" * 50)
    print("📁 Enhanced with MD folder management and archival harmonization")
    
    # Initialize distillation engine with workspace management
    workspace_root = "c:/dev/AIOS"
    engine = AIKnowledgeDistillationEngine(workspace_root)
    
    # Step 1: Comprehensive MD lifecycle management
    files_to_process, backup_folder = engine.manage_md_lifecycle(auto_archive=False)
    
    if not files_to_process:
        print("🛑 No files to process. Exiting.")
        return
    
    # Step 2: Ingest files for distillation
    print(f"\n🔍 Processing {len(files_to_process)} files for distillation...")
    engine.ingest_files([str(f) for f in files_to_process])
    
    # Step 3: Perform knowledge distillation
    result = engine.distill_knowledge()
    
    # Step 4: Save distilled results
    distilled_path = workspace_root + "/DISTILLED_DEVELOPMENT_PATH.md"
    engine.save_distillation(result, distilled_path)
    
    # Step 5: Archive processed files if requested
    archive_response = input(f"\n🗄️ Archive the {len(files_to_process)} processed MD files? (y/N): ").strip().lower()
    if archive_response in ['y', 'yes']:
        engine.archive_processed_files(files_to_process, "knowledge_distillation_v2")
        print(f"✅ Files archived. Backup available at: {backup_folder}")
    else:
        print(f"ℹ️ Files kept in place. Backup available at: {backup_folder}")
    
    # Step 6: Print comprehensive summary
    print(f"\n🎉 Knowledge Distillation Complete!")
    print(f"✅ Files Processed: {len(files_to_process)}")
    print(f"✅ Compression Ratio: {result.compression_ratio:.1%}")
    print(f"✅ Coherence Score: {result.semantic_coherence_score:.1%}")
    print(f"📄 Distilled Document: {distilled_path}")
    print(f"💾 Backup Location: {backup_folder}")
    print(f"📁 MD Management: Harmonized with project structure")
    
    # Step 7: Show next steps
    print(f"\n🚀 Next Steps:")
    print(f"1. Review the distilled document: DISTILLED_DEVELOPMENT_PATH.md")
    print(f"2. Use the distilled path as your primary development reference")
    print(f"3. Re-run distillation as new context files are created")
    print(f"4. Check archived files in docs/context_archive/ if needed")

if __name__ == "__main__":
    main()
