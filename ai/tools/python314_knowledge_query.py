#!/usr/bin/env python3
"""
Python 3.14 Knowledge Base Query Tool
AINLP Protocol: OS0.6.2.claude

Demonstrates how to query the indexed Python 3.14 documentation.
"""

import json
from pathlib import Path
from typing import List, Dict


class Python314KnowledgeQuery:
    """Query interface for Python 3.14 documentation knowledge base"""
    
    def __init__(self, index_path: Path):
        with open(index_path, 'r', encoding='utf-8') as f:
            self.index = json.load(f)
        
        self.metadata = self.index['metadata']
        self.sections = self.index['sections']
        self.topic_index = self.index['topic_index']
        self.complexity_index = self.index['complexity_index']
    
    def search_by_topic(self, topic: str) -> List[Dict]:
        """Find all documents related to a topic"""
        if topic not in self.topic_index:
            return []
        return self.topic_index[topic]
    
    def search_by_complexity(self, level: str) -> List[Dict]:
        """Find documents by complexity level (BASIC, INTERMEDIATE, ADVANCED, EXPERT)"""
        if level not in self.complexity_index:
            return []
        return self.complexity_index[level]
    
    def search_by_keyword(self, keyword: str) -> List[Dict]:
        """Search for keyword in titles and content previews"""
        results = []
        keyword_lower = keyword.lower()
        
        for section in self.sections:
            if (keyword_lower in section['title'].lower() or 
                keyword_lower in section['content_preview'].lower()):
                results.append({
                    'filename': section['filename'],
                    'title': section['title'],
                    'category': section['category'],
                    'topics': section['topics']
                })
        
        return results
    
    def get_free_threading_docs(self) -> List[Dict]:
        """Get all free-threading related documentation"""
        return self.search_by_topic('free_threading')
    
    def get_gil_docs(self) -> List[Dict]:
        """Get all GIL-related documentation"""
        return self.search_by_topic('gil')
    
    def print_summary(self):
        """Print knowledge base summary"""
        print("=" * 70)
        print("Python 3.14 Documentation Knowledge Base")
        print("=" * 70)
        print(f"Total Files: {self.metadata['total_files']}")
        print(f"Indexed: {self.metadata['indexed_date']}")
        print(f"Python Version: {self.metadata['python_version']}")
        print(f"AINLP Protocol: {self.metadata['ainlp_protocol']}")
        print()
        
        print("Topics Available:")
        for topic, docs in sorted(self.topic_index.items()):
            print(f"  • {topic}: {len(docs)} documents")
        print()
        
        print("Complexity Levels:")
        for level, docs in self.complexity_index.items():
            print(f"  • {level}: {len(docs)} documents")
        print("=" * 70)


def main():
    """Demonstrate knowledge base querying"""
    aios_root = Path(__file__).parent.parent.parent
    index_path = aios_root / "ai" / "data" / "knowledge" / "python_314_index.json"
    
    # Load knowledge base
    kb = Python314KnowledgeQuery(index_path)
    
    # Print summary
    kb.print_summary()
    print()
    
    # Example queries
    print("🔍 Example Queries:")
    print()
    
    # 1. Free-threading documentation
    print("1️⃣  Free-Threading Documentation (Python 3.14's biggest feature):")
    free_threading_docs = kb.get_free_threading_docs()
    print(f"   Found {len(free_threading_docs)} documents")
    if free_threading_docs:
        print("   First 3:")
        for i, doc in enumerate(free_threading_docs[:3], 1):
            print(f"     {i}. {doc['title'][:60]}")
            print(f"        → {doc['filename']}")
    print()
    
    # 2. GIL documentation
    print("2️⃣  GIL Documentation:")
    gil_docs = kb.get_gil_docs()
    print(f"   Found {len(gil_docs)} documents")
    if gil_docs:
        print("   First 3:")
        for i, doc in enumerate(gil_docs[:3], 1):
            print(f"     {i}. {doc['title'][:60]}")
            print(f"        → {doc['filename']}")
    print()
    
    # 3. Async programming
    print("3️⃣  Async Programming Documentation:")
    async_docs = kb.search_by_topic('async')
    print(f"   Found {len(async_docs)} documents")
    print()
    
    # 4. Expert-level documentation
    print("4️⃣  Expert-Level Documentation:")
    expert_docs = kb.search_by_complexity('EXPERT')
    print(f"   Found {len(expert_docs)} documents")
    if expert_docs:
        print("   Sample topics:")
        for i, doc in enumerate(expert_docs[:5], 1):
            print(f"     {i}. {doc['title'][:60]}")
    print()
    
    # 5. Search by keyword
    print("5️⃣  Search for 'thread safety':")
    safety_docs = kb.search_by_keyword('thread safety')
    print(f"   Found {len(safety_docs)} documents")
    if safety_docs:
        for i, doc in enumerate(safety_docs[:3], 1):
            print(f"     {i}. {doc['title'][:60]}")
    print()
    
    print("=" * 70)
    print("✅ Knowledge base is ready for AIOS agent use!")
    print("=" * 70)


if __name__ == "__main__":
    main()
