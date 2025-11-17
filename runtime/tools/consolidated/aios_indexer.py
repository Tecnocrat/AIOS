# ============================================================
#  aios_indexer.py
# Enhanced with AIOS Library Ingestion Protocol Integration
# 
# Parses C++/C#/Python modules and generates:
# - docs/dependency_graph.dot (and .svg)
# - docs/services_registry.json
# - Harmonized AI-ingestible summaries
# - Multi-language library knowledge base
# - Semantic network and dendritic connections
# ============================================================

import os
import sys
import json
import asyncio
from pathlib import Path
from graphviz import Digraph

# Add AI core modules to path for library ingestion protocol
AIOS_ROOT = Path(__file__).parent.parent
sys.path.append(str(AIOS_ROOT / "ai" / "src" / "core"))

# Import AIOS Library Ingestion Protocol (optional - graceful degradation)
try:
    from library_learning_integration_hub import (
        LibraryLearningIntegrationHub,
        ProgrammingLanguage
    )
    INGESTION_PROTOCOL_AVAILABLE = True
except ImportError:
    INGESTION_PROTOCOL_AVAILABLE = False
    print("⚠️  AIOS Library Ingestion Protocol not available - using basic mode")

MODULE_DIRS = ['orchestrator', 'director', 'scripts', 'ai/src', 'core']
SERVICE_KEYWORDS = ['IService', 'register', 'Plugin', 'load']

def extract_includes(content):
    """
    Extract include dependencies from C++ source code.
    
    Analyzes C++ content to identify #include directives and extract
    the included file names for dependency mapping.
    
    Args:
        content (str): C++ source code content to analyze
        
    Returns:
        list[str]: List of included file names
        
    Example:
        >>> content = '#include "myheader.h"\\n#include <iostream>'
        >>> extract_includes(content)
        ['myheader.h']
    """
    try:
        return [line.strip().split('"')[1] for line in content.splitlines()
                if line.strip().startswith('#include') and '"' in line]
    except (IndexError, AttributeError) as e:
        print(f"Warning: Error parsing includes: {e}")
        return []


def discover_services(base_path: str) -> list[dict]:
    """
    Discover and catalog service modules across AIOS architecture layers.
    
    Scans the AIOS codebase for service implementations and plugins,
    building a comprehensive registry for dependency analysis.
    
    Args:
        base_path (str): Root path of AIOS project to scan
        
    Returns:
        list[dict]: Registry of discovered services with metadata
        
    AIOS Architecture Integration:
        - Supports multi-language service discovery (C++, C#, Python)
        - Identifies service patterns across all AIOS layers
        - Provides harmonized context for AI processing
    """
    registry = []
    for module_dir in MODULE_DIRS:
        abs_dir = os.path.join(base_path, module_dir)
        if not os.path.exists(abs_dir):
            print(f"Warning: Module directory not found: {abs_dir}")
            continue
            
        for root, _, files in os.walk(abs_dir):
            for f in files:
                if f.endswith(('.cpp', '.cs', '.py')):
                    path = os.path.join(root, f)
                    try:
                        with open(path, 'r', encoding='utf-8') as file:
                            content = file.read()
                            if any(kw in content for kw in SERVICE_KEYWORDS):
                                # Enhanced service metadata for AIOS context
                                service_info = {
                                    'name': os.path.splitext(f)[0],
                                    'path': os.path.relpath(path, base_path),
                                    'language': f.split('.')[-1],
                                    'summary': f"Service module: {f}",
                                    'dependencies': extract_includes(content),
                                    'size_bytes': os.path.getsize(path),
                                    'last_modified': os.path.getmtime(path)
                                }
                                registry.append(service_info)
                    except Exception as e:
                        print(f"Error reading {path}: {e}")
    return registry


def build_graph(registry: list[dict], 
                out_dot: str = 'docs/dependency_graph.dot', 
                out_svg: str = 'docs/dependency_graph.svg') -> None:
    """
    Generate AIOS dependency visualization using intelligent graph analysis.
    
    Creates both DOT and SVG representations of service dependencies
    for architectural understanding and AI context harmonization.
    
    Args:
        registry (list[dict]): Service registry from discover_services()
        out_dot (str): Output path for DOT file
        out_svg (str): Output path for SVG visualization
        
    AIOS Integration:
        - Provides visual context for AI-driven architectural decisions
        - Supports real-time dependency analysis
        - Enhances AIOS pattern recognition capabilities
    """
    try:
        dot = Digraph(comment='AIOS Dependency Graph')
        dot.attr(rankdir='TB', size='12,8')
        dot.attr('node', shape='box', style='rounded,filled', 
                 fillcolor='lightblue')
        
        for svc in registry:
            # Enhanced node with service metadata
            label = f"{svc['name']}\\n({svc['language']})"
            dot.node(svc['name'], label=label)
            
            for dep in svc['dependencies']:
                dot.edge(svc['name'], dep.replace('.h', '').replace('.hpp', ''))
                
        # Ensure output directory exists
        os.makedirs(os.path.dirname(out_dot), exist_ok=True)
        dot.render(out_dot, format='svg', cleanup=True)
        print(f" AIOS dependency graph generated: {out_dot} and {out_svg}")
        
    except Exception as e:
        print(f" Error generating dependency graph: {e}")


def save_registry(registry: list[dict], 
                  out_json: str = 'docs/services_registry.json') -> None:
    """
    Persist AIOS service registry for AI context harmonization.
    
    Saves the discovered service registry in JSON format for use by
    AIOS AI engines and context harmonization systems.
    
    Args:
        registry (list[dict]): Complete service registry
        out_json (str): Output JSON file path
        
    AIOS AI Integration:
        - Provides structured context for GitHub Copilot
        - Enables intelligent code analysis and suggestions
        - Supports automated refactoring workflows
    """
    try:
        # Ensure output directory exists
        os.makedirs(os.path.dirname(out_json), exist_ok=True)
        
        # Enhanced registry with metadata for AI processing
        enhanced_registry = {
            'aios_version': '0.6.1',
            'generated_timestamp': str(os.path.getmtime(__file__)),
            'total_services': len(registry),
            'services': registry,
            'ai_context': {
                'purpose': 'AIOS service discovery for AI harmonization',
                'compatible_engines': ['GitHub Copilot', 'Claude', 'GPT-4'],
                'integration_ready': True
            }
        }
        
        with open(out_json, 'w', encoding='utf-8') as f:
            json.dump(enhanced_registry, f, indent=2)
        print(f" AIOS service registry saved: {out_json}")
        
    except Exception as e:
        print(f" Error saving service registry: {e}")


async def run_enhanced_ingestion(base_path: str, registry: list[dict]):
    """
    Enhanced ingestion using AIOS Library Ingestion Protocol
    
    Performs deep semantic analysis and multi-language library learning
    with consciousness integration and dendritic network expansion.
    
    Args:
        base_path: Base path for AIOS project
        registry: Service registry from basic discovery
    """
    if not INGESTION_PROTOCOL_AVAILABLE:
        print("⚠️  Enhanced ingestion not available - skipping")
        return
    
    print("\n🧬 Enhanced Library Ingestion Protocol")
    print("=" * 50)
    
    try:
        # Initialize library learning integration hub
        hub = LibraryLearningIntegrationHub(consciousness_level=0.85)
        
        # Start learning session
        session = await hub.start_learning_session()
        print(f"🚀 Learning session started: {session.session_id}")
        
        # Learn key AIOS libraries
        key_libraries = [
            ('scripts', ProgrammingLanguage.PYTHON),
            ('ai/src/core', ProgrammingLanguage.PYTHON),
            ('ai/src/engines', ProgrammingLanguage.PYTHON),
            ('core/core_systems', None),  # Mixed languages - auto-detect
        ]
        
        for lib_path, language in key_libraries:
            full_path = Path(base_path) / lib_path
            if full_path.exists():
                try:
                    print(f"\n📚 Learning library: {lib_path}")
                    knowledge = await hub.learn_library(
                        str(full_path),
                        library_name=lib_path.replace('/', '_'),
                        language=language
                    )
                    print(f"   ✅ Learned {len(knowledge.api_elements)} API elements")
                    print(f"   🧠 Consciousness: {knowledge.consciousness_coherence:.2f}")
                    print(f"   🏷️  Tags: {', '.join(knowledge.semantic_tags[:5])}")
                except Exception as e:
                    print(f"   ⚠️  Error learning {lib_path}: {e}")
        
        # Finish learning session
        completed_session = await hub.finish_learning_session()
        
        # Display learning statistics
        stats = hub.get_learning_statistics()
        print(f"\n📊 Enhanced Ingestion Statistics:")
        print(f"   Total libraries: {stats['total_libraries']}")
        print(f"   Total API elements: {stats['total_api_elements']}")
        print(f"   Semantic network size: {stats['semantic_network_size']}")
        print(f"   Dendritic network size: {stats['dendritic_network_size']}")
        print(f"   Final consciousness level: {stats['consciousness_level']:.2f}")
        
        # Save enhanced registry with semantic information
        enhanced_registry_path = os.path.join(base_path, 'docs', 'enhanced_services_registry.json')
        os.makedirs(os.path.dirname(enhanced_registry_path), exist_ok=True)
        
        enhanced_data = {
            'basic_services': registry,
            'learning_statistics': stats,
            'semantic_network': {tag: list(items) for tag, items in hub.semantic_network.items()},
            'session_summary': completed_session.to_dict()
        }
        
        with open(enhanced_registry_path, 'w', encoding='utf-8') as f:
            json.dump(enhanced_data, f, indent=2)
        
        print(f"\n💾 Enhanced registry saved: {enhanced_registry_path}")
        
    except Exception as e:
        print(f"\n⚠️  Enhanced ingestion error: {e}")
        print("   Continuing with basic indexing...")


if __name__ == '__main__':
    """
    AIOS Indexer Main Execution
    
    Orchestrates the complete AIOS service discovery and dependency 
    analysis workflow for AI context harmonization.
    
    Enhanced with AIOS Library Ingestion Protocol for:
    - Multi-language library learning
    - Semantic network construction
    - Consciousness-driven analysis
    - Dendritic knowledge expansion
    """
    print("🧬 AIOS Service Discovery & Dependency Analysis")
    print("=" * 50)
    
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    print(f"📂 Scanning AIOS base path: {base_path}")
    
    # Execute basic AIOS discovery workflow
    registry = discover_services(base_path)
    print(f"✅ Discovered {len(registry)} services")
    
    build_graph(registry)
    save_registry(registry)
    
    # Execute enhanced ingestion with library learning protocol
    if INGESTION_PROTOCOL_AVAILABLE:
        asyncio.run(run_enhanced_ingestion(base_path, registry))
    
    print("\n🎉 AIOS indexing complete - Ready for AI harmonization!")
