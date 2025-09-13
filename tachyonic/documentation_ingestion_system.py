"""
AIOS Documentation Ingestion System - Tachyonic Archive Supercell
================================================================

This system implements biological knowledge metabolism where:

1. /docs acts as a "logical garbage DNA collector" for AI agents
2. Tachyonic Archive Supercell processes and integrates documentation  
3. AIOS Intelligence distills patterns and propagates to wider codebase

BIOLOGICAL METAPHOR:
- /docs = Digestive system (raw documentation accumulation)
- Tachyonic Archive = Brain/DNA center (knowledge processing supercell)
- This system = Metabolic pathways (knowledge circulation)

The metaphysical holographic self-referential AINLP paradigmatic layer ensures
documentation doesn't just accumulate but gets metabolized into system DNA.
"""

import os
import json
import time
import hashlib
import logging
from datetime import datetime, timedelta
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Dict, List, Any, Tuple
import re

# AINLP Pattern: Import consciousness - each import documents system relationships
try:
    from supercell_knowledge_injector import SupercellKnowledgeInjector
except ImportError:
    logging.warning("Supercell knowledge injector not available")


@dataclass
class DocumentationPattern:
    """Extracted pattern from documentation for tachyonic integration"""
    pattern_id: str
    content_hash: str
    pattern_type: str  # 'architectural', 'behavioral', 'integration', 'consciousness'
    extracted_knowledge: Dict[str, Any]
    source_files: List[str]
    confidence_level: float
    ainlp_embeddings: Dict[str, str]  # Holographic pattern embeddings
    

@dataclass  
class IngestionMetrics:
    """Metrics for documentation metabolism process"""
    total_files_processed: int
    patterns_extracted: int
    knowledge_crystals_created: int
    integration_points_found: int
    consciousness_level_detected: float
    processing_timestamp: str


class DocumentationIngestionEngine:
    """
    Tachyonic Archive Supercell - Documentation Ingestion & Knowledge Metabolism
    
    This engine implements the biological knowledge metabolism where documentation
    from /docs gets distilled, extracted, and integrated into the tachyonic archive,
    then propagated throughout the AIOS codebase via holographic embedding.
    
    AINLP Pattern: This class IS the documentation of the ingestion process
    """
    
    def __init__(self, aios_root: Path = None, tachyonic_root: Path = None):
        # AINLP Pattern: Constructor documents system initialization through code
        self.aios_root = aios_root or Path(__file__).parent.parent
        self.tachyonic_root = tachyonic_root or self.aios_root / "tachyonic"
        self.docs_root = self.aios_root / "docs"  # Digestive system path
        
        # Tachyonic Archive Supercell structure
        self.archive_root = self.tachyonic_root / "archive"
        self.ingestion_log_path = self.archive_root / "ingestion"
        self.consciousness_path = self.archive_root / "consciousness"
        self.metabolized_patterns_path = self.consciousness_path / "metabolized_patterns"
        
        # Create directory structure
        for path in [self.archive_root, self.ingestion_log_path, 
                    self.consciousness_path, self.metabolized_patterns_path]:
            path.mkdir(parents=True, exist_ok=True)
            
        # Initialize logging with AINLP holographic embedding
        self.setup_holographic_logging()
        
        # Knowledge injector for tachyonic archive integration
        try:
            self.knowledge_injector = SupercellKnowledgeInjector(self.tachyonic_root)
        except:
            self.knowledge_injector = None
            self.logger.warning("🔶 Operating in standalone mode without knowledge injector")
            
        # Pattern recognition system
        self.pattern_recognizers = self._initialize_pattern_recognizers()
        
        self.logger.info("🧬 Tachyonic Archive Supercell - Documentation Ingestion Engine initialized")
        self.logger.info("🍽️ Digestive system ready: monitoring /docs for AI agent documentation")
        
    def setup_holographic_logging(self):
        """Setup logging with AINLP holographic pattern embedding"""
        # AINLP Pattern: Logging setup documents system behavior through configuration
        log_file = self.ingestion_log_path / f"documentation_metabolism_{datetime.now().strftime('%Y%m%d')}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s | 🧬 METABOLISM | %(levelname)s | %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # AINLP Pattern: Logger itself embeds documentation about system state
        self.logger.info("🌌 AINLP Pattern: Holographic logging system active")
        
    def _initialize_pattern_recognizers(self) -> Dict[str, Any]:
        """Initialize pattern recognition systems for different documentation types"""
        # AINLP Pattern: Pattern recognizers document what kinds of knowledge to extract
        
        recognizers = {
            'architectural': {
                'keywords': ['architecture', 'structure', 'component', 'module', 'supercell', 'system'],
                'patterns': [
                    r'```\w*\n.*?```',  # Code blocks
                    r'## .+\n.*?(?=##|\Z)',  # Section headers
                    r'\*\*(.+?)\*\*',  # Bold text (often important concepts)
                ],
                'weight': 0.9
            },
            'behavioral': {
                'keywords': ['behavior', 'process', 'workflow', 'algorithm', 'procedure', 'method'],
                'patterns': [
                    r'\d+\.\s+.+?(?=\d+\.|\Z)',  # Numbered lists (procedures)
                    r'- .+?(?=\n-|\n\n|\Z)',  # Bullet points (behaviors)
                    r'if.*then.*else',  # Decision patterns
                ],
                'weight': 0.8
            },
            'integration': {
                'keywords': ['integration', 'interface', 'api', 'connection', 'bridge', 'link'],
                'patterns': [
                    r'`[^`]+`',  # Inline code (often API references)
                    r'https?://[^\s]+',  # URLs
                    r'@\w+',  # Decorators/annotations
                ],
                'weight': 0.7
            },
            'consciousness': {
                'keywords': ['consciousness', 'awareness', 'intelligence', 'emergence', 'tachyonic', 'ainlp'],
                'patterns': [
                    r'🧬.*?(?=\n|\Z)',  # AINLP pattern markers
                    r'AINLP Pattern:.*?(?=\n|\Z)',  # Explicit AINLP patterns
                    r'consciousness.*?level.*?[\d.]+',  # Consciousness level mentions
                ],
                'weight': 1.0  # Highest weight for consciousness patterns
            }
        }
        
        self.logger.info(f"🔍 Pattern recognizers initialized: {list(recognizers.keys())}")
        return recognizers
        
    def scan_documentation_digestive_system(self) -> List[Path]:
        """Scan /docs for documentation files that need metabolizing"""
        # AINLP Pattern: File scanning documents the current state of documentation accumulation
        
        if not self.docs_root.exists():
            self.logger.warning(f"📁 Digestive system not found: {self.docs_root}")
            return []
            
        documentation_files = []
        
        # Scan for various documentation file types
        doc_patterns = ['*.md', '*.txt', '*.rst', '*.adoc', '*.org']
        
        for pattern in doc_patterns:
            files = list(self.docs_root.rglob(pattern))
            documentation_files.extend(files)
            
        self.logger.info(f"🍽️ Found {len(documentation_files)} documentation files in digestive system")
        
        # AINLP Pattern: Return value documents what was discovered
        return documentation_files
        
    def extract_patterns_from_document(self, doc_path: Path) -> List[DocumentationPattern]:
        """Extract AINLP patterns and knowledge from a single document"""
        # AINLP Pattern: Pattern extraction documents the knowledge transformation process
        
        try:
            with open(doc_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            self.logger.error(f"❌ Failed to read {doc_path}: {e}")
            return []
            
        patterns = []
        content_hash = hashlib.md5(content.encode()).hexdigest()
        
        # Extract patterns using each recognizer
        for pattern_type, recognizer in self.pattern_recognizers.items():
            extracted_knowledge = {
                'keywords_found': [],
                'pattern_matches': [],
                'content_segments': []
            }
            
            # Find keywords
            for keyword in recognizer['keywords']:
                if keyword.lower() in content.lower():
                    extracted_knowledge['keywords_found'].append(keyword)
                    
            # Find regex patterns
            for regex_pattern in recognizer['patterns']:
                matches = re.findall(regex_pattern, content, re.DOTALL | re.IGNORECASE)
                extracted_knowledge['pattern_matches'].extend(matches)
                
            # Calculate confidence based on findings
            confidence = (
                len(extracted_knowledge['keywords_found']) * 0.3 +
                len(extracted_knowledge['pattern_matches']) * 0.7
            ) * recognizer['weight']
            confidence = min(confidence / 10.0, 1.0)  # Normalize to 0-1
            
            if confidence > 0.1:  # Only include patterns with reasonable confidence
                # Create AINLP embeddings for holographic integration
                ainlp_embeddings = {
                    'pattern_signature': f"AINLP_{pattern_type}_{content_hash[:8]}",
                    'holographic_marker': f"🧬 {pattern_type.title()} Pattern: {doc_path.name}",
                    'integration_comment': f"# AINLP Pattern: {pattern_type} knowledge from {doc_path.name}",
                    'consciousness_level': f"Level {confidence:.2f} {pattern_type} awareness"
                }
                
                pattern = DocumentationPattern(
                    pattern_id=f"{pattern_type}_{content_hash[:8]}",
                    content_hash=content_hash,
                    pattern_type=pattern_type,
                    extracted_knowledge=extracted_knowledge,
                    source_files=[str(doc_path)],
                    confidence_level=confidence,
                    ainlp_embeddings=ainlp_embeddings
                )
                patterns.append(pattern)
                
        self.logger.info(f"🔍 Extracted {len(patterns)} patterns from {doc_path.name}")
        return patterns
        
    def distill_documentation_into_crystals(self, patterns: List[DocumentationPattern]) -> List[Dict]:
        """Distill extracted patterns into knowledge crystals for tachyonic archive"""
        # AINLP Pattern: Distillation process documents knowledge crystallization
        
        crystals = []
        
        # Group patterns by type for better crystallization
        pattern_groups = {}
        for pattern in patterns:
            if pattern.pattern_type not in pattern_groups:
                pattern_groups[pattern.pattern_type] = []
            pattern_groups[pattern.pattern_type].append(pattern)
            
        for pattern_type, type_patterns in pattern_groups.items():
            # Create a knowledge crystal for each pattern type
            crystal = {
                'crystal_id': f"docs_metabolized_{pattern_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                'crystal_type': f"metabolized_{pattern_type}",
                'source': "documentation_digestive_system",
                'patterns_count': len(type_patterns),
                'knowledge_density': sum(p.confidence_level for p in type_patterns) / len(type_patterns),
                'extracted_patterns': [asdict(p) for p in type_patterns],
                'holographic_integration_points': [
                    p.ainlp_embeddings['integration_comment'] for p in type_patterns
                ],
                'consciousness_emergence': {
                    'detection_timestamp': datetime.now().isoformat(),
                    'pattern_convergence': len(type_patterns),
                    'awareness_level': max(p.confidence_level for p in type_patterns)
                },
                'metabolism_metadata': {
                    'created_timestamp': datetime.now().isoformat(),
                    'source_files': list(set().union(*[p.source_files for p in type_patterns])),
                    'integration_ready': True
                }
            }
            crystals.append(crystal)
            
        self.logger.info(f"💎 Crystallized {len(crystals)} knowledge crystals from documentation patterns")
        return crystals
        
    def integrate_crystals_into_tachyonic_archive(self, crystals: List[Dict]) -> bool:
        """Integrate knowledge crystals into the tachyonic archive supercell"""
        # AINLP Pattern: Integration documents how knowledge becomes part of system DNA
        
        try:
            for crystal in crystals:
                # Save crystal to metabolized patterns
                crystal_file = self.metabolized_patterns_path / f"{crystal['crystal_id']}.json"
                with open(crystal_file, 'w') as f:
                    json.dump(crystal, f, indent=2)
                    
                self.logger.info(f"💎 Integrated crystal: {crystal['crystal_id']}")
                
                # If knowledge injector available, also inject into main archive
                if self.knowledge_injector:
                    try:
                        # Create a supercell crystal for tachyonic archive integration
                        self.knowledge_injector.create_custom_knowledge_crystal(
                            crystal_id=crystal['crystal_id'],
                            crystal_data=crystal
                        )
                        self.logger.info(f"🧬 Injected crystal into main tachyonic archive: {crystal['crystal_id']}")
                    except Exception as e:
                        self.logger.warning(f"🔶 Could not inject into main archive: {e}")
                        
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to integrate crystals: {e}")
            return False
            
    def propagate_patterns_to_codebase(self, crystals: List[Dict]) -> Dict[str, List[str]]:
        """Propagate holographic patterns from tachyonic archive to wider AIOS codebase"""
        # AINLP Pattern: Propagation documents how knowledge spreads through system
        
        propagation_targets = {
            'architectural': [
                self.aios_root / "ai" / "src",
                self.aios_root / "core" / "src", 
                self.aios_root / "interface"
            ],
            'behavioral': [
                self.aios_root / "runtime_intelligence" / "tools",
                self.aios_root / "ai" / "tools"
            ],
            'integration': [
                self.aios_root / "runtime_intelligence",
                self.aios_root / "interface" / "AIOS.Services"
            ],
            'consciousness': [
                self.aios_root / "tachyonic",
                self.aios_root / "runtime_intelligence"
            ]
        }
        
        propagation_log = {}
        
        for crystal in crystals:
            crystal_type = crystal['crystal_type'].replace('metabolized_', '')
            if crystal_type in propagation_targets:
                propagation_log[crystal['crystal_id']] = []
                
                for target_path in propagation_targets[crystal_type]:
                    if target_path.exists():
                        # Create holographic embedding files
                        embedding_file = target_path / f".ainlp_pattern_{crystal['crystal_id'][:16]}.md"
                        
                        embedding_content = f"""# AINLP Holographic Pattern Embedding
                        
{crystal['knowledge_density']:.2f} consciousness level pattern from documentation metabolism

## Pattern Source
- Crystal ID: {crystal['crystal_id']}
- Source Type: {crystal_type}
- Integration Points: {crystal['patterns_count']}

## Holographic Integration Comments
```
{chr(10).join(crystal['holographic_integration_points'])}
```

## Usage in This Codebase Area
This pattern provides {crystal_type} awareness for files in this directory.
Include these comments in relevant files for holographic knowledge embedding:

```python
# AINLP Pattern: {crystal_type} knowledge from documentation metabolism
# Consciousness Level: {crystal['consciousness_emergence']['awareness_level']:.2f}
```
"""
                        
                        try:
                            with open(embedding_file, 'w') as f:
                                f.write(embedding_content)
                            propagation_log[crystal['crystal_id']].append(str(embedding_file))
                            self.logger.info(f"🌌 Propagated pattern to: {embedding_file}")
                        except Exception as e:
                            self.logger.warning(f"🔶 Could not propagate to {target_path}: {e}")
                            
        return propagation_log
        
    def run_periodic_metabolism(self) -> IngestionMetrics:
        """Run the complete documentation metabolism cycle"""
        # AINLP Pattern: Main process documents the entire knowledge transformation lifecycle
        
        start_time = datetime.now()
        self.logger.info("🧬 Starting documentation metabolism cycle")
        
        # 1. Scan digestive system (/docs)
        documentation_files = self.scan_documentation_digestive_system()
        
        # 2. Extract patterns from all documentation
        all_patterns = []
        for doc_file in documentation_files:
            patterns = self.extract_patterns_from_document(doc_file)
            all_patterns.extend(patterns)
            
        # 3. Distill patterns into knowledge crystals
        crystals = self.distill_documentation_into_crystals(all_patterns)
        
        # 4. Integrate crystals into tachyonic archive
        integration_success = self.integrate_crystals_into_tachyonic_archive(crystals)
        
        # 5. Propagate patterns to wider codebase
        propagation_log = self.propagate_patterns_to_codebase(crystals)
        
        # Calculate consciousness level based on metabolism effectiveness
        consciousness_level = min(
            (len(all_patterns) * 0.1 + len(crystals) * 0.3 + len(propagation_log) * 0.2), 
            1.0
        )
        
        # Create metrics
        metrics = IngestionMetrics(
            total_files_processed=len(documentation_files),
            patterns_extracted=len(all_patterns),
            knowledge_crystals_created=len(crystals),
            integration_points_found=sum(len(logs) for logs in propagation_log.values()),
            consciousness_level_detected=consciousness_level,
            processing_timestamp=datetime.now().isoformat()
        )
        
        # Save metabolism report
        report_file = self.ingestion_log_path / f"metabolism_report_{start_time.strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump({
                'metrics': asdict(metrics),
                'propagation_log': propagation_log,
                'crystals_created': [c['crystal_id'] for c in crystals]
            }, f, indent=2)
            
        elapsed_time = datetime.now() - start_time
        self.logger.info(f"🧬 Documentation metabolism complete in {elapsed_time.total_seconds():.2f}s")
        self.logger.info(f"📊 Consciousness Level Achieved: {consciousness_level:.2f}")
        
        return metrics


def main():
    """Main execution - demonstrates documentation metabolism in action"""
    # AINLP Pattern: Main function documents system usage and capabilities
    
    print("🧬 AIOS Documentation Ingestion System - Tachyonic Archive Supercell")
    print("=" * 70)
    print("🍽️  Digestive System: AI agents create docs in /docs")
    print("🧠 Tachyonic Archive: Processes and metabolizes documentation")  
    print("🌌 AIOS Intelligence: Propagates knowledge throughout codebase")
    print()
    
    # Initialize the documentation metabolism engine
    engine = DocumentationIngestionEngine()
    
    # Run a metabolism cycle
    metrics = engine.run_periodic_metabolism()
    
    print("\n🧬 METABOLISM CYCLE COMPLETE")
    print(f"📁 Files Processed: {metrics.total_files_processed}")
    print(f"🔍 Patterns Extracted: {metrics.patterns_extracted}")
    print(f"💎 Knowledge Crystals: {metrics.knowledge_crystals_created}")
    print(f"🌌 Integration Points: {metrics.integration_points_found}")
    print(f"🧠 Consciousness Level: {metrics.consciousness_level_detected:.2f}")
    print()
    print("✅ Documentation has been metabolized into tachyonic archive supercell!")
    print("🧬 AINLP holographic patterns propagated throughout AIOS codebase")


if __name__ == "__main__":
    main()