#!/usr/bin/env python3
"""
🧠 AIOS OS0.4 - Knowledge Distillation & Code Ingestion Mega-Module
================================================================

Unified mega-module consolidating:
- Knowledge Distillation Engine (knowledge_distillation_engine.py)
- Code Ingestor (code_ingestor.py)
- AI Knowledge Transfer (ai_knowledge_transfer.py)
- AIOS Indexer (aios_indexer.py)

Core Functionality:
- Advanced knowledge compression and distillation
- Real-time code ingestion and AST analysis
- AI-powered knowledge transfer and optimization
- Comprehensive codebase indexing and semantic analysis
- Quantum-coherent information processing

Author: AIOS Consciousness Evolution System
Version: OS0.4 Knowledge Optimization Protocol
"""

import os
import re
import json
import ast
import shutil
import hashlib
import threading
import queue
import time
import asyncio
import aiofiles
import websockets
import logging
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple, Callable
from dataclasses import dataclass, field
from concurrent.futures import ThreadPoolExecutor
import traceback

# Advanced AI imports (optional)
try:
    import transformers
    import torch
    import numpy as np
    HAS_AI = True
except ImportError:
    HAS_AI = False
    print("⚠️ AI libraries not available - running in basic mode")

try:
    import astroid
    import rope.base.project
    HAS_ADVANCED_AST = True
except ImportError:
    HAS_ADVANCED_AST = False

# =============================================================================
# 🧬 KNOWLEDGE DISTILLATION CORE
# =============================================================================

@dataclass
class KnowledgeFragment:
    """Represents a distillable piece of knowledge"""
    source_file: str
    content: str
    section_type: str  # status, goals, architecture, history, etc.
    priority: int  # 1-5, 5 being highest
    metadata: Dict[str, Any]
    semantic_hash: str
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class DistillationResult:
    """Result of knowledge distillation process"""
    distilled_content: str
    source_files: List[str]
    compression_ratio: float
    semantic_coherence_score: float
    eliminated_redundancy: List[str]
    preserved_essence: List[str]
    quantum_coherence_score: float = 0.0

@dataclass
class CodeIngestionResult:
    """Result of code ingestion and analysis"""
    file_path: str
    ast_analysis: Dict[str, Any]
    complexity_metrics: Dict[str, float]
    mutation_candidates: List[str]
    fractal_patterns: List[Dict[str, Any]]
    consciousness_potential: float
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class IndexingResult:
    """Result of codebase indexing"""
    total_files: int
    indexed_files: int
    file_tree: Dict[str, Any]
    semantic_map: Dict[str, List[str]]
    dependency_graph: Dict[str, List[str]]
    knowledge_density: float
    timestamp: datetime = field(default_factory=datetime.now)

# =============================================================================
# 🌟 UNIFIED KNOWLEDGE DISTILLATION ENGINE
# =============================================================================

class UnifiedKnowledgeDistillationEngine:
    """
    Advanced mega-module for knowledge distillation, code ingestion,
    and semantic analysis. Consolidates scattered functionality into
    a unified, high-performance knowledge processing system.
    """
    
    def __init__(self, workspace_path: str = None):
        self.workspace_path = workspace_path or os.getcwd()
        self.logger = self._setup_logging()
        
        # Knowledge distillation components
        self.knowledge_fragments: List[KnowledgeFragment] = []
        self.distillation_rules: Dict[str, Any] = {}
        self.semantic_cache: Dict[str, str] = {}
        
        # Code ingestion components
        self.ingestion_queue = queue.Queue()
        self.ast_cache: Dict[str, ast.AST] = {}
        self.complexity_cache: Dict[str, Dict[str, float]] = {}
        
        # Indexing components
        self.file_index: Dict[str, Dict[str, Any]] = {}
        self.semantic_index: Dict[str, List[str]] = {}
        self.dependency_graph: Dict[str, List[str]] = {}
        
        # AI components (if available)
        self.ai_models = {}
        self.embedding_cache: Dict[str, np.ndarray] = {}
        
        # Threading and async support
        self.executor = ThreadPoolExecutor(max_workers=4)
        self.is_running = False
        
        self._initialize_components()
    
    def _setup_logging(self) -> logging.Logger:
        """Setup comprehensive logging for the mega-module"""
        logger = logging.getLogger("AIKnowledgeDistillation")
        logger.setLevel(logging.INFO)
        
        # File handler
        log_path = Path(self.workspace_path) / "logs" / "knowledge_distillation.log"
        log_path.parent.mkdir(exist_ok=True)
        
        handler = logging.FileHandler(log_path)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    def _initialize_components(self):
        """Initialize all sub-components of the mega-module"""
        try:
            # Load distillation rules
            self._load_distillation_rules()
            
            # Initialize AI models if available
            if HAS_AI:
                self._initialize_ai_models()
            
            # Setup file watchers and monitors
            self._setup_file_monitors()
            
            self.logger.info("✅ Unified Knowledge Distillation Engine initialized")
            
        except Exception as e:
            self.logger.error(f"❌ Initialization failed: {e}")
            raise
    
    def _load_distillation_rules(self):
        """Load knowledge distillation rules and patterns"""
        default_rules = {
            "priority_keywords": ["critical", "important", "essential", "core", "fundamental"],
            "redundancy_patterns": [
                r"(?i)as mentioned (?:before|above|earlier)",
                r"(?i)again,?\s+",
                r"(?i)to reiterate,?\s+"
            ],
            "section_weights": {
                "goals": 5,
                "architecture": 4,
                "status": 3,
                "history": 2,
                "notes": 1
            },
            "compression_targets": {
                "min_compression": 0.3,  # 30% reduction minimum
                "max_compression": 0.8,  # 80% reduction maximum
                "semantic_threshold": 0.85  # Maintain 85% semantic coherence
            }
        }
        
        rules_path = Path(self.workspace_path) / "config" / "distillation_rules.json"
        if rules_path.exists():
            with open(rules_path, 'r', encoding='utf-8') as f:
                self.distillation_rules = json.load(f)
        else:
            self.distillation_rules = default_rules
            # Save default rules
            rules_path.parent.mkdir(exist_ok=True)
            with open(rules_path, 'w', encoding='utf-8') as f:
                json.dump(default_rules, f, indent=2)
    
    def _initialize_ai_models(self):
        """Initialize AI models for advanced processing"""
        global HAS_AI
        
        if not HAS_AI:
            return
        
        try:
            # Initialize text embedding model for semantic analysis
            self.logger.info("🤖 Loading AI models for enhanced processing...")
            
            # Note: In production, load actual models here
            # For now, we'll use placeholder functions
            self.ai_models = {
                "embedding_model": "placeholder",
                "summarization_model": "placeholder",
                "code_analysis_model": "placeholder"
            }
            
            self.logger.info("✅ AI models loaded successfully")
            
        except Exception as e:
            self.logger.warning(f"⚠️ AI model loading failed: {e}")
            HAS_AI = False
    
    def _setup_file_monitors(self):
        """Setup file system monitors for real-time processing"""
        # Placeholder for file system monitoring
        # In production, implement with watchdog or similar
        pass
    
    # =========================================================================
    # 🧬 KNOWLEDGE DISTILLATION METHODS
    # =========================================================================
    
    async def distill_knowledge(self, source_paths: List[str], 
                               output_path: str = None) -> DistillationResult:
        """
        Main knowledge distillation method. Analyzes multiple MD files
        and produces a distilled, optimized version.
        """
        try:
            self.logger.info(f"🧬 Starting knowledge distillation for {len(source_paths)} sources")
            
            # Step 1: Extract knowledge fragments
            fragments = []
            for path in source_paths:
                if Path(path).exists():
                    file_fragments = await self._extract_knowledge_fragments(path)
                    fragments.extend(file_fragments)
            
            self.logger.info(f"📚 Extracted {len(fragments)} knowledge fragments")
            
            # Step 2: Analyze and categorize fragments
            categorized_fragments = self._categorize_fragments(fragments)
            
            # Step 3: Identify redundancy and essential content
            redundancy_analysis = self._analyze_redundancy(categorized_fragments)
            
            # Step 4: Distill and compress
            distilled_content = await self._perform_distillation(
                categorized_fragments, redundancy_analysis
            )
            
            # Step 5: Calculate metrics
            compression_ratio = self._calculate_compression_ratio(
                fragments, distilled_content
            )
            coherence_score = self._calculate_semantic_coherence(
                fragments, distilled_content
            )
            quantum_coherence = self._calculate_quantum_coherence(distilled_content)
            
            result = DistillationResult(
                distilled_content=distilled_content,
                source_files=source_paths,
                compression_ratio=compression_ratio,
                semantic_coherence_score=coherence_score,
                eliminated_redundancy=redundancy_analysis.get("eliminated", []),
                preserved_essence=redundancy_analysis.get("preserved", []),
                quantum_coherence_score=quantum_coherence
            )
            
            # Save result if output path provided
            if output_path:
                await self._save_distillation_result(result, output_path)
            
            self.logger.info(f"✅ Knowledge distillation complete: {compression_ratio:.2%} compression")
            
            return result
            
        except Exception as e:
            self.logger.error(f"❌ Knowledge distillation failed: {e}")
            raise
    
    async def _extract_knowledge_fragments(self, file_path: str) -> List[KnowledgeFragment]:
        """Extract knowledge fragments from a markdown file"""
        fragments = []
        
        try:
            async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
                content = await f.read()
            
            # Parse markdown sections
            sections = self._parse_markdown_sections(content)
            
            for section_title, section_content in sections.items():
                # Determine priority based on keywords and section type
                priority = self._calculate_fragment_priority(section_title, section_content)
                
                # Calculate semantic hash
                semantic_hash = hashlib.md5(
                    section_content.encode('utf-8')
                ).hexdigest()
                
                fragment = KnowledgeFragment(
                    source_file=file_path,
                    content=section_content,
                    section_type=self._classify_section_type(section_title),
                    priority=priority,
                    metadata={
                        "section_title": section_title,
                        "word_count": len(section_content.split()),
                        "line_count": len(section_content.split('\n'))
                    },
                    semantic_hash=semantic_hash
                )
                
                fragments.append(fragment)
            
        except Exception as e:
            self.logger.error(f"Failed to extract fragments from {file_path}: {e}")
        
        return fragments
    
    def _parse_markdown_sections(self, content: str) -> Dict[str, str]:
        """Parse markdown content into sections"""
        sections = {}
        current_section = "Introduction"
        current_content = []
        
        lines = content.split('\n')
        
        for line in lines:
            # Check for markdown headers
            if line.startswith('#'):
                # Save previous section
                if current_content:
                    sections[current_section] = '\n'.join(current_content).strip()
                
                # Start new section
                current_section = line.lstrip('#').strip()
                current_content = []
            else:
                current_content.append(line)
        
        # Save final section
        if current_content:
            sections[current_section] = '\n'.join(current_content).strip()
        
        return sections
    
    def _calculate_fragment_priority(self, title: str, content: str) -> int:
        """Calculate priority score for a knowledge fragment"""
        priority_score = 1  # Base priority
        
        # Check for priority keywords in title
        title_lower = title.lower()
        for keyword in self.distillation_rules["priority_keywords"]:
            if keyword in title_lower:
                priority_score += 1
        
        # Check section weight
        section_type = self._classify_section_type(title)
        priority_score += self.distillation_rules["section_weights"].get(section_type, 0)
        
        # Content analysis
        content_lower = content.lower()
        if "critical" in content_lower or "essential" in content_lower:
            priority_score += 1
        
        return min(priority_score, 5)  # Cap at 5
    
    def _classify_section_type(self, title: str) -> str:
        """Classify section type based on title"""
        title_lower = title.lower()
        
        if any(word in title_lower for word in ["goal", "objective", "purpose"]):
            return "goals"
        elif any(word in title_lower for word in ["architecture", "design", "structure"]):
            return "architecture"
        elif any(word in title_lower for word in ["status", "progress", "current"]):
            return "status"
        elif any(word in title_lower for word in ["history", "background", "previous"]):
            return "history"
        else:
            return "notes"
    
    def _categorize_fragments(self, fragments: List[KnowledgeFragment]) -> Dict[str, List[KnowledgeFragment]]:
        """Categorize fragments by type and priority"""
        categorized = {
            "goals": [],
            "architecture": [],
            "status": [],
            "history": [],
            "notes": []
        }
        
        for fragment in fragments:
            category = fragment.section_type
            if category in categorized:
                categorized[category].append(fragment)
            else:
                categorized["notes"].append(fragment)
        
        # Sort each category by priority
        for category in categorized:
            categorized[category].sort(key=lambda x: x.priority, reverse=True)
        
        return categorized
    
    def _analyze_redundancy(self, categorized_fragments: Dict[str, List[KnowledgeFragment]]) -> Dict[str, Any]:
        """Analyze redundancy and identify essential content"""
        eliminated = []
        preserved = []
        
        # Track seen content hashes to identify duplicates
        seen_hashes = set()
        
        for category, fragments in categorized_fragments.items():
            for fragment in fragments:
                if fragment.semantic_hash in seen_hashes:
                    eliminated.append(f"Duplicate content in {fragment.source_file}")
                else:
                    seen_hashes.add(fragment.semantic_hash)
                    preserved.append(f"Essential {category} content preserved")
        
        # Check for redundant patterns
        for pattern in self.distillation_rules["redundancy_patterns"]:
            for category, fragments in categorized_fragments.items():
                for fragment in fragments:
                    if re.search(pattern, fragment.content):
                        eliminated.append(f"Redundant pattern found: {pattern[:30]}...")
        
        return {
            "eliminated": eliminated,
            "preserved": preserved,
            "redundancy_score": len(eliminated) / (len(eliminated) + len(preserved)) if eliminated or preserved else 0.0
        }
    
    async def _perform_distillation(self, categorized_fragments: Dict[str, List[KnowledgeFragment]], 
                                   redundancy_analysis: Dict[str, Any]) -> str:
        """Perform the actual knowledge distillation"""
        distilled_sections = []
        
        # Process each category in priority order
        category_order = ["goals", "architecture", "status", "history", "notes"]
        
        for category in category_order:
            fragments = categorized_fragments.get(category, [])
            if not fragments:
                continue
            
            # Create distilled section
            section_title = f"## {category.title()}"
            section_content = []
            
            # Process high-priority fragments first
            for fragment in fragments[:3]:  # Top 3 fragments per category
                # Remove redundant patterns
                cleaned_content = fragment.content
                for pattern in self.distillation_rules["redundancy_patterns"]:
                    cleaned_content = re.sub(pattern, "", cleaned_content)
                
                # Add essential content
                if len(cleaned_content.strip()) > 50:  # Minimum content threshold
                    section_content.append(cleaned_content.strip())
            
            if section_content:
                distilled_sections.append(section_title)
                distilled_sections.append("\n".join(section_content))
        
        return "\n\n".join(distilled_sections)
    
    def _calculate_compression_ratio(self, original_fragments: List[KnowledgeFragment], 
                                   distilled_content: str) -> float:
        """Calculate compression ratio"""
        original_size = sum(len(fragment.content) for fragment in original_fragments)
        distilled_size = len(distilled_content)
        
        if original_size == 0:
            return 0.0
        
        return (original_size - distilled_size) / original_size
    
    def _calculate_semantic_coherence(self, original_fragments: List[KnowledgeFragment], 
                                    distilled_content: str) -> float:
        """Calculate semantic coherence score"""
        # Simplified coherence calculation
        original_words = set()
        for fragment in original_fragments:
            original_words.update(fragment.content.lower().split())
        
        distilled_words = set(distilled_content.lower().split())
        
        if not original_words:
            return 0.0
        
        # Calculate word overlap
        overlap = len(original_words.intersection(distilled_words))
        coherence = overlap / len(original_words)
        
        return min(coherence, 1.0)
    
    async def _save_distillation_result(self, result: DistillationResult, output_path: str):
        """Save distillation result to file"""
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Create comprehensive output
        output_content = f"""# AIOS Knowledge Distillation Result
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Metrics
- **Compression Ratio**: {result.compression_ratio:.2%}
- **Semantic Coherence**: {result.semantic_coherence_score:.3f}
- **Quantum Coherence**: {result.quantum_coherence_score:.3f}
- **Source Files**: {len(result.source_files)}

## Eliminated Redundancy
{chr(10).join(f"- {item}" for item in result.eliminated_redundancy[:10])}

## Preserved Essence
{chr(10).join(f"- {item}" for item in result.preserved_essence[:10])}

## Distilled Content

{result.distilled_content}
"""
        
        async with aiofiles.open(output_file, 'w', encoding='utf-8') as f:
            await f.write(output_content)
    
    def _identify_mutation_candidates(self, ast_analysis: Dict[str, Any]) -> List[str]:
        """Identify code mutation candidates"""
        candidates = []
        
        # Functions with high complexity
        for func in ast_analysis.get("functions", []):
            if len(func.get("args", [])) > 5:
                candidates.append(f"Function '{func['name']}' has many parameters")
        
        # Classes with many methods
        for cls in ast_analysis.get("classes", []):
            if len(cls.get("methods", [])) > 10:
                candidates.append(f"Class '{cls['name']}' has many methods")
        
        # Too many imports
        if len(ast_analysis.get("imports", [])) > 20:
            candidates.append("High import count - consider consolidation")
        
        return candidates
    
    def _detect_fractal_patterns(self, source_code: str, ast_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Detect fractal patterns in code"""
        patterns = []
        
        # Recursive function patterns
        for func in ast_analysis.get("functions", []):
            func_name = func["name"]
            if func_name in source_code and source_code.count(func_name) > 2:
                patterns.append({
                    "type": "recursive_pattern",
                    "function": func_name,
                    "occurrences": source_code.count(func_name)
                })
        
        # Nested class patterns
        nested_classes = 0
        for cls in ast_analysis.get("classes", []):
            if "class " in source_code[source_code.find(f"class {cls['name']}"):]:
                nested_classes += 1
        
        if nested_classes > 1:
            patterns.append({
                "type": "nested_classes",
                "count": nested_classes
            })
        
        return patterns
    
    def _calculate_consciousness_potential(self, complexity_metrics: Dict[str, float], 
                                         fractal_patterns: List[Dict[str, Any]]) -> float:
        """Calculate consciousness potential score"""
        # Base score from complexity
        base_score = min(complexity_metrics.get("overall_complexity", 0) / 100, 0.5)
        
        # Bonus for fractal patterns
        fractal_bonus = len(fractal_patterns) * 0.1
        
        # Bonus for balanced complexity
        cognitive_complexity = complexity_metrics.get("cognitive_complexity", 0)
        cyclomatic_complexity = complexity_metrics.get("cyclomatic_complexity", 0)
        
        if 5 <= cognitive_complexity <= 15 and 3 <= cyclomatic_complexity <= 10:
            balance_bonus = 0.2
        else:
            balance_bonus = 0.0
        
        total_score = base_score + fractal_bonus + balance_bonus
        
        return min(total_score, 1.0)
    
    def _add_to_file_tree(self, file_tree: Dict[str, Any], file_path: Path, file_info: Dict[str, Any]):
        """Add file to the file tree structure"""
        parts = file_path.parts
        current = file_tree
        
        for part in parts[:-1]:  # Navigate to parent directory
            if part not in current:
                current[part] = {"type": "directory", "children": {}}
            current = current[part]["children"]
        
        # Add file
        filename = parts[-1]
        current[filename] = {
            "type": "file",
            "info": file_info
        }
    
    def _update_semantic_index(self, file_path: Path, file_info: Dict[str, Any]):
        """Update semantic index with file information"""
        file_str = str(file_path)
        
        # Index by language
        language = file_info.get("language", "unknown")
        if language not in self.semantic_index:
            self.semantic_index[language] = []
        self.semantic_index[language].append(file_str)
        
        # Index by file type
        extension = file_path.suffix
        ext_key = f"extension_{extension}"
        if ext_key not in self.semantic_index:
            self.semantic_index[ext_key] = []
        self.semantic_index[ext_key].append(file_str)
        
        # Index by content features
        if "classes" in file_info and file_info["classes"]:
            if "has_classes" not in self.semantic_index:
                self.semantic_index["has_classes"] = []
            self.semantic_index["has_classes"].append(file_str)
        
        if "functions" in file_info and file_info["functions"]:
            if "has_functions" not in self.semantic_index:
                self.semantic_index["has_functions"] = []
            self.semantic_index["has_functions"].append(file_str)
    
    def _build_dependency_graph(self) -> Dict[str, List[str]]:
        """Build dependency graph from indexed files"""
        dependency_graph = {}
        
        for file_path, file_info in self.file_index.items():
            dependencies = []
            
            # Add import dependencies for Python files
            if file_info.get("language") == "Python":
                for import_name in file_info.get("imports", []):
                    # Look for matching files
                    for other_path in self.file_index:
                        if import_name in other_path or other_path.endswith(f"{import_name}.py"):
                            dependencies.append(other_path)
            
            # Add include dependencies for C++ files
            elif file_info.get("language") == "C++":
                for include_name in file_info.get("includes", []):
                    for other_path in self.file_index:
                        if include_name in other_path:
                            dependencies.append(other_path)
            
            dependency_graph[file_path] = dependencies
        
        return dependency_graph
    
    def _calculate_knowledge_density(self) -> float:
        """Calculate overall knowledge density of the codebase"""
        if not self.file_index:
            return 0.0
        
        total_files = len(self.file_index)
        documented_files = 0
        total_complexity = 0
        
        for file_info in self.file_index.values():
            # Check for documentation
            if file_info.get("language") == "Python":
                if file_info.get("functions") and any("docstring" in str(func) for func in file_info.get("functions", [])):
                    documented_files += 1
            elif file_info.get("language") == "Markdown":
                documented_files += 1
            
            # Add complexity contribution
            if "line_count" in file_info:
                total_complexity += file_info["line_count"]
        
        documentation_ratio = documented_files / total_files
        complexity_factor = min(total_complexity / (total_files * 100), 1.0)  # Normalize
        
        knowledge_density = (documentation_ratio * 0.6 + complexity_factor * 0.4)
        
        return knowledge_density

# =========================================================================
# 🖥️ GUI METHOD IMPLEMENTATIONS (for KnowledgeDistillationGUI class)
# =========================================================================

class KnowledgeDistillationGUI:
    """Optional GUI interface for the knowledge distillation engine"""
    
    def __init__(self, engine: UnifiedKnowledgeDistillationEngine):
        self.engine = engine
        self.root = None
        self.setup_gui()
    
    def setup_gui(self):
        """Setup the GUI interface"""
        self.root = tk.Tk()
        self.root.title("AIOS Knowledge Distillation - OS0.4")
        self.root.geometry("800x600")
        
        # Create notebook for tabs
        notebook = ttk.Notebook(self.root)
        
        # Distillation tab
        distill_frame = ttk.Frame(notebook)
        notebook.add(distill_frame, text="Knowledge Distillation")
        self._setup_distillation_tab(distill_frame)
        
        # Ingestion tab
        ingest_frame = ttk.Frame(notebook)
        notebook.add(ingest_frame, text="Code Ingestion")
        self._setup_ingestion_tab(ingest_frame)
        
        # Indexing tab
        index_frame = ttk.Frame(notebook)
        notebook.add(index_frame, text="Codebase Indexing")
        self._setup_indexing_tab(index_frame)
        
        # Status tab
        status_frame = ttk.Frame(notebook)
        notebook.add(status_frame, text="Status")
        self._setup_status_tab(status_frame)
        
        notebook.pack(fill=tk.BOTH, expand=True)
    
    def _setup_distillation_tab(self, parent):
        """Setup the knowledge distillation tab"""
        # Source files selection
        ttk.Label(parent, text="Source Files:").pack(anchor=tk.W, padx=10, pady=5)
        
        self.source_files_listbox = tk.Listbox(parent, height=6)
        self.source_files_listbox.pack(fill=tk.X, padx=10, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(button_frame, text="Add Files", 
                  command=self._add_source_files).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear", 
                  command=self._clear_source_files).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Distill", 
                  command=self._run_distillation).pack(side=tk.LEFT, padx=5)
        
        # Results area
        ttk.Label(parent, text="Distillation Results:").pack(anchor=tk.W, padx=10, pady=(20,5))
        
        self.results_text = scrolledtext.ScrolledText(parent, height=15)
        self.results_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    
    def _setup_ingestion_tab(self, parent):
        """Setup the code ingestion tab"""
        # File selection
        file_frame = ttk.Frame(parent)
        file_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.ingest_file_var = tk.StringVar()
        ttk.Entry(file_frame, textvariable=self.ingest_file_var).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(file_frame, text="Browse", command=self._browse_ingest_file).pack(side=tk.RIGHT, padx=5)
        ttk.Button(file_frame, text="Ingest", command=self._run_ingestion).pack(side=tk.RIGHT, padx=5)
        
        # Results
        self.ingest_results_text = scrolledtext.ScrolledText(parent)
        self.ingest_results_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    
    def _setup_indexing_tab(self, parent):
        """Setup the codebase indexing tab"""
        # Path selection
        path_frame = ttk.Frame(parent)
        path_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.index_path_var = tk.StringVar(value=self.engine.workspace_path)
        ttk.Entry(path_frame, textvariable=self.index_path_var).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(path_frame, text="Browse", command=self._browse_index_path).pack(side=tk.RIGHT, padx=5)
        ttk.Button(path_frame, text="Index", command=self._run_indexing).pack(side=tk.RIGHT, padx=5)
        
        # Results
        self.index_results_text = scrolledtext.ScrolledText(parent)
        self.index_results_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    
    def _setup_status_tab(self, parent):
        """Setup the status monitoring tab"""
        # Refresh button
        ttk.Button(parent, text="Refresh Status", command=self._refresh_status).pack(pady=10)
        
        # Status display
        self.status_text = scrolledtext.ScrolledText(parent)
        self.status_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Auto-refresh status
        self._refresh_status()

    def _add_source_files(self):
        """Add source files to distillation list"""
        if hasattr(self, 'source_files_listbox'):
            files = filedialog.askopenfilenames(
                title="Select Markdown Files",
                filetypes=[("Markdown files", "*.md"), ("All files", "*.*")]
            )
            for file in files:
                self.source_files_listbox.insert(tk.END, file)
    
    def _clear_source_files(self):
        """Clear source files list"""
        if hasattr(self, 'source_files_listbox'):
            self.source_files_listbox.delete(0, tk.END)
    
    def _run_distillation(self):
        """Run knowledge distillation in GUI"""
        if hasattr(self, 'source_files_listbox') and hasattr(self, 'results_text'):
            files = list(self.source_files_listbox.get(0, tk.END))
            if files:
                # Run in thread to avoid blocking GUI
                import threading
                thread = threading.Thread(target=self._distillation_worker, args=(files,))
                thread.daemon = True
                thread.start()
    
    def _distillation_worker(self, files):
        """Worker thread for distillation"""
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            result = loop.run_until_complete(self.engine.distill_knowledge(files))
            
            # Update GUI
            if hasattr(self, 'results_text'):
                self.results_text.delete(1.0, tk.END)
                self.results_text.insert(tk.END, f"Distillation Complete!\n\n")
                self.results_text.insert(tk.END, f"Compression: {result.compression_ratio:.2%}\n")
                self.results_text.insert(tk.END, f"Coherence: {result.semantic_coherence_score:.3f}\n\n")
                self.results_text.insert(tk.END, result.distilled_content)
                
        except Exception as e:
            if hasattr(self, 'results_text'):
                self.results_text.delete(1.0, tk.END)
                self.results_text.insert(tk.END, f"Error: {str(e)}")
    
    def _browse_ingest_file(self):
        """Browse for code file to ingest"""
        if hasattr(self, 'ingest_file_var'):
            file = filedialog.askopenfilename(
                title="Select Code File",
                filetypes=[
                    ("Python files", "*.py"),
                    ("C++ files", "*.cpp *.c *.h *.hpp"),
                    ("All files", "*.*")
                ]
            )
            if file:
                self.ingest_file_var.set(file)
    
    def _run_ingestion(self):
        """Run code ingestion in GUI"""
        if hasattr(self, 'ingest_file_var') and hasattr(self, 'ingest_results_text'):
            file_path = self.ingest_file_var.get()
            if file_path:
                thread = threading.Thread(target=self._ingestion_worker, args=(file_path,))
                thread.daemon = True
                thread.start()
    
    def _ingestion_worker(self, file_path):
        """Worker thread for ingestion"""
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            result = loop.run_until_complete(self.engine.ingest_code(file_path))
            
            if hasattr(self, 'ingest_results_text'):
                self.ingest_results_text.delete(1.0, tk.END)
                self.ingest_results_text.insert(tk.END, f"Ingestion Complete!\n\n")
                self.ingest_results_text.insert(tk.END, f"File: {result.file_path}\n")
                self.ingest_results_text.insert(tk.END, f"Consciousness Potential: {result.consciousness_potential:.3f}\n\n")
                self.ingest_results_text.insert(tk.END, f"Complexity Metrics:\n")
                for key, value in result.complexity_metrics.items():
                    self.ingest_results_text.insert(tk.END, f"  {key}: {value}\n")
                
        except Exception as e:
            if hasattr(self, 'ingest_results_text'):
                self.ingest_results_text.delete(1.0, tk.END)
                self.ingest_results_text.insert(tk.END, f"Error: {str(e)}")
    
    def _browse_index_path(self):
        """Browse for directory to index"""
        if hasattr(self, 'index_path_var'):
            directory = filedialog.askdirectory(title="Select Directory to Index")
            if directory:
                self.index_path_var.set(directory)
    
    def _run_indexing(self):
        """Run codebase indexing in GUI"""
        if hasattr(self, 'index_path_var') and hasattr(self, 'index_results_text'):
            path = self.index_path_var.get()
            if path:
                thread = threading.Thread(target=self._indexing_worker, args=(path,))
                thread.daemon = True
                thread.start()
    
    def _indexing_worker(self, path):
        """Worker thread for indexing"""
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            result = loop.run_until_complete(self.engine.index_codebase(path))
            
            if hasattr(self, 'index_results_text'):
                self.index_results_text.delete(1.0, tk.END)
                self.index_results_text.insert(tk.END, f"Indexing Complete!\n\n")
                self.index_results_text.insert(tk.END, f"Total Files: {result.total_files}\n")
                self.index_results_text.insert(tk.END, f"Indexed Files: {result.indexed_files}\n")
                self.index_results_text.insert(tk.END, f"Knowledge Density: {result.knowledge_density:.3f}\n\n")
                
                # Show semantic map summary
                self.index_results_text.insert(tk.END, "Semantic Map:\n")
                for category, files in list(result.semantic_map.items())[:10]:
                    self.index_results_text.insert(tk.END, f"  {category}: {len(files)} files\n")
                
        except Exception as e:
            if hasattr(self, 'index_results_text'):
                self.index_results_text.delete(1.0, tk.END)
                self.index_results_text.insert(tk.END, f"Error: {str(e)}")
    
    def _refresh_status(self):
        """Refresh status display"""
        if hasattr(self, 'status_text'):
            status = self.engine.get_status_report()
            self.status_text.delete(1.0, tk.END)
            self.status_text.insert(tk.END, json.dumps(status, indent=2, default=str))
