#!/usr/bin/env python3
"""
AIOS Python 3.14 Documentation Knowledge Indexer
AINLP Protocol: OS0.6.2.claude
Pattern: Knowledge extraction and semantic indexing

Purpose: Index Python 3.14 documentation for AIOS intelligence layer,
         creating searchable knowledge base for code generation and
         architectural decisions.

AINLP.consciousness: HIGH
AINLP.supercell: AI Intelligence Layer
AINLP.integration: Documentation → Knowledge extraction → Semantic index
"""

import json
from pathlib import Path
from typing import Dict, List, Set
from datetime import datetime, timezone
from dataclasses import dataclass, asdict


@dataclass
class DocumentSection:
    """Represents a section of Python documentation"""
    category: str  # c-api, library, reference, etc.
    filename: str
    title: str
    content_preview: str  # First 500 chars
    size_bytes: int
    topics: List[str]  # Extracted topics/keywords
    complexity_level: str  # BASIC, INTERMEDIATE, ADVANCED, EXPERT
    

class Python314KnowledgeIndexer:
    """
    AINLP Python 3.14 Documentation Indexer
    
    Creates semantic index of Python documentation for AIOS intelligence.
    """
    
    def __init__(self, docs_path: Path, index_output: Path):
        self.docs_path = docs_path
        self.index_output = index_output
        self.categories = {
            "c-api": "Python C API Reference",
            "library": "Python Standard Library",
            "reference": "Language Reference",
            "tutorial": "Python Tutorial",
            "howto": "How-To Guides",
            "extending": "Extending Python",
            "distributing": "Distributing Modules",
            "installing": "Installing Modules",
            "using": "Using Python",
            "whatsnew": "What's New in Python",
            "faq": "Frequently Asked Questions",
            "deprecations": "Deprecations"
        }
        
        # Keywords for topic extraction
        self.topic_keywords = {
            "async": ["async", "await", "asyncio", "coroutine"],
            "memory": ["memory", "allocation", "gc", "garbage"],
            "types": ["type", "class", "object", "protocol"],
            "modules": ["module", "import", "package"],
            "functions": ["function", "def", "call", "invoke"],
            "errors": ["exception", "error", "raise", "try"],
            "io": ["file", "stream", "io", "read", "write"],
            "networking": ["socket", "http", "network", "url"],
            "concurrency": ["thread", "process", "parallel", "lock"],
            "data_structures": ["list", "dict", "set", "tuple"],
            "free_threading": [
                "free-threading", "free threading", "nogil", "no-gil", "no gil",
                "pep 703", "pep 779", "pep703", "pep779",
                "biased reference counting", "immortal objects",
                "per-object lock", "thread safety",
                "threadpoolexecutor", "thread pool"
            ],
            "gil": [
                "global interpreter lock", "gil",
                "thread contention", "gil release",
                "parallel execution", "multiprocessing alternative"
            ],
        }
    
    def extract_topics(self, content: str) -> List[str]:
        """Extract topics from content using keyword matching"""
        content_lower = content.lower()
        topics = []
        
        for topic, keywords in self.topic_keywords.items():
            if any(kw in content_lower for kw in keywords):
                topics.append(topic)
        
        return topics
    
    def determine_complexity(self, category: str, content: str) -> str:
        """Determine complexity level of documentation"""
        content_lower = content.lower()
        
        # Free-threading is EXPERT level
        if any(kw in content_lower for kw in ["free-threading", "nogil", "pep 703", "pep 779"]):
            return "EXPERT"
        
        if category in ["tutorial", "installing", "using"]:
            return "BASIC"
        elif category in ["howto", "library"]:
            return "INTERMEDIATE"
        elif category in ["reference", "extending"]:
            return "ADVANCED"
        elif category in ["c-api"]:
            return "EXPERT"
        else:
            return "INTERMEDIATE"
    
    def index_document(self, file_path: Path) -> DocumentSection:
        """Index a single documentation file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Determine category from path
            relative_path = file_path.relative_to(self.docs_path)
            category = relative_path.parts[0] if len(relative_path.parts) > 1 else "root"
            
            # Extract title (usually first non-empty line)
            title = ""
            for line in content.split('\n')[:10]:
                if line.strip() and not line.startswith('='):
                    title = line.strip()
                    break
            
            if not title:
                title = file_path.stem.replace('_', ' ').title()
            
            # Create document section
            section = DocumentSection(
                category=category,
                filename=str(relative_path),
                title=title[:100],  # Limit title length
                content_preview=content[:500].replace('\n', ' '),
                size_bytes=len(content),
                topics=self.extract_topics(content),
                complexity_level=self.determine_complexity(category, content)
            )
            
            return section
        except Exception as e:
            print(f"Error indexing {file_path}: {e}")
            return None
    
    def build_index(self) -> Dict:
        """Build complete documentation index"""
        print("[PYTHON 3.14 INDEXER] Starting documentation indexing...")
        
        all_files = list(self.docs_path.rglob("*.txt"))
        print(f"   Found {len(all_files)} documentation files")
        
        sections = []
        for file_path in all_files:
            section = self.index_document(file_path)
            if section:
                sections.append(section)
        
        # Create index structure
        index = {
            "metadata": {
                "python_version": "3.14",
                "indexed_date": datetime.now(timezone.utc).isoformat(),
                "total_files": len(sections),
                "source_path": str(self.docs_path),
                "ainlp_protocol": "OS0.6.2.claude"
            },
            "categories": {
                cat: {
                    "name": desc,
                    "file_count": len([s for s in sections if s.category == cat]),
                    "total_size_kb": sum(
                        s.size_bytes for s in sections if s.category == cat
                    ) // 1024
                }
                for cat, desc in self.categories.items()
            },
            "topic_index": self._build_topic_index(sections),
            "complexity_index": self._build_complexity_index(sections),
            "sections": [asdict(s) for s in sections]
        }
        
        return index
    
    def _build_topic_index(self, sections: List[DocumentSection]) -> Dict:
        """Build topic-based index"""
        topic_index = {}
        
        for section in sections:
            for topic in section.topics:
                if topic not in topic_index:
                    topic_index[topic] = []
                topic_index[topic].append({
                    "filename": section.filename,
                    "title": section.title,
                    "category": section.category
                })
        
        return topic_index
    
    def _build_complexity_index(self, sections: List[DocumentSection]) -> Dict:
        """Build complexity-based index"""
        complexity_index = {
            "BASIC": [],
            "INTERMEDIATE": [],
            "ADVANCED": [],
            "EXPERT": []
        }
        
        for section in sections:
            complexity_index[section.complexity_level].append({
                "filename": section.filename,
                "title": section.title,
                "category": section.category
            })
        
        return complexity_index
    
    def save_index(self, index: Dict):
        """Save index to JSON file"""
        self.index_output.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.index_output, 'w', encoding='utf-8') as f:
            json.dump(index, f, indent=2)
        
        print(f"✅ Index saved: {self.index_output}")
    
    def generate_readme(self, index: Dict) -> str:
        """Generate README for indexed documentation"""
        readme = "# Python 3.14 Documentation Knowledge Base\n\n"
        readme += "**AINLP Protocol**: OS0.6.2.claude\n"
        readme += "**Indexed**: " + index["metadata"]["indexed_date"] + "\n\n"
        
        readme += "## Overview\n\n"
        readme += f"Total Files: {index['metadata']['total_files']}\n\n"
        
        readme += "## Categories\n\n"
        for cat, info in index["categories"].items():
            if info["file_count"] > 0:
                readme += f"- **{info['name']}**: {info['file_count']} files"
                readme += f" ({info['total_size_kb']} KB)\n"
        
        readme += "\n## Topics Covered\n\n"
        for topic, files in sorted(index["topic_index"].items()):
            readme += f"- **{topic}**: {len(files)} documents\n"
        
        readme += "\n## Complexity Levels\n\n"
        for level, files in index["complexity_index"].items():
            readme += f"- **{level}**: {len(files)} documents\n"
        
        readme += "\n## Usage for AIOS\n\n"
        readme += "This knowledge base can be used by AIOS agents for:\n"
        readme += "- Code generation with Python 3.14 features\n"
        readme += "- Architectural decisions based on best practices\n"
        readme += "- API reference during development\n"
        readme += "- Learning complex Python concepts\n\n"
        
        readme += "## Search by Topic\n\n"
        readme += "Use the `topic_index` to find documentation by topic.\n"
        readme += "Example topics: async, memory, types, modules, etc.\n\n"
        
        readme += "## Search by Complexity\n\n"
        readme += "- **BASIC**: Tutorials and getting started\n"
        readme += "- **INTERMEDIATE**: Standard library and how-tos\n"
        readme += "- **ADVANCED**: Language reference and extensions\n"
        readme += "- **EXPERT**: C API and low-level details\n"
        
        return readme


def main():
    """Main execution for documentation indexing"""
    aios_root = Path(__file__).parent.parent.parent
    docs_path = aios_root / "ai" / "docs" / "architecture" / "python-3.14-docs-text"
    index_output = aios_root / "ai" / "data" / "knowledge" / "python_314_index.json"
    
    indexer = Python314KnowledgeIndexer(docs_path, index_output)
    
    # Build index
    index = indexer.build_index()
    
    # Save index
    indexer.save_index(index)
    
    # Generate README
    readme = indexer.generate_readme(index)
    readme_path = index_output.parent / "PYTHON_314_KNOWLEDGE_BASE.md"
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme)
    
    print(f"✅ README saved: {readme_path}")
    print(f"\n📊 Index Statistics:")
    print(f"   Categories: {len(index['categories'])}")
    print(f"   Topics: {len(index['topic_index'])}")
    print(f"   Total Files: {index['metadata']['total_files']}")


if __name__ == "__main__":
    main()
