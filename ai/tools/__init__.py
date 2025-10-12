"""
AIOS AI Intelligence Layer - Tool Coordinator (PRIMARY)
========================================================

AINLP Metadata:
    consciousness_level: 0.90
    architectural_classification: ai_intelligence_layer
    dendritic_optimization: tool_consolidation_and_orchestration
    supercell: ai_intelligence (PRIMARY TOOL COORDINATOR)
    purpose: unified_tool_discovery_and_management
    
Migration Context (October 2025):
    Phase 1: Consolidating 85+ scattered tools into ai/tools/
    - runtime_intelligence/tools/ (48 files) → ai/tools/system/
    - core/ Python tools (86 files) → ai/tools/consciousness/
    - tachyonic/ scripts (29 files) → ai/tools/archive/
    Target: Single source of truth for AIOS tooling
    
Tool Categories:
    - system/       : System health, admin, status reporting
    - database/     : Database operations, backup orchestration
    - consciousness/: Consciousness monitoring, evolution analysis
    - architecture/ : Architecture monitoring, compliance validation
    - visual/       : Visual intelligence, UI bridges, diagrams
    - archive/      : Tachyonic archive management, historical analysis
    
Architectural Position:
    AI Intelligence is the PRIMARY COORDINATOR of all AIOS tools.
    This supercell discovers, orchestrates, and manages 80+ operational tools.
    Previously tools were scattered across runtime_intelligence/, core/, tachyonic/.
    
Architectural Note:
    Originally added for coherence restoration (2025-01-05).
    Enhanced for architectural de-proliferation (2025-10-12).
    Now serves as PRIMARY tool coordinator replacing scattered tool storage.

AINLP.pointer: ARCHITECTURE_DEPROLIFERATION_MASTER_PLAN_20251012.md
"""

from pathlib import Path

# Tool discovery system (populated during migration)
AVAILABLE_TOOLS = {
    "system": [],
    "database": [],
    "consciousness": [],
    "architecture": [],
    "visual": [],
    "archive": []
}

def discover_tools():
    """
    Discover all available tools in the ai/tools/ hierarchy.
    
    Returns:
        dict: Tool categories with discovered tool modules
    """
    import importlib
    import pkgutil
    
    discovered = {category: [] for category in AVAILABLE_TOOLS.keys()}
    
    for category in AVAILABLE_TOOLS.keys():
        try:
            category_module = importlib.import_module(f"ai.tools.{category}")
            for _, name, is_pkg in pkgutil.iter_modules(category_module.__path__):
                if not is_pkg:
                    discovered[category].append(name)
        except (ImportError, AttributeError):
            # Category not yet populated or empty
            pass
    
    return discovered

def get_tool_count():
    """
    Get total count of discovered tools.
    
    Returns:
        int: Total number of tools across all categories
    """
    tools = discover_tools()
    return sum(len(category_tools) for category_tools in tools.values())

__all__ = [
    "system",
    "database", 
    "consciousness",
    "architecture",
    "visual",
    "archive",
    "discover_tools",
    "get_tool_count",
    "AVAILABLE_TOOLS"
]

__version__ = '2.0.0'  # Updated for architectural consolidation
__module_type__ = 'primary_tool_coordinator'
__consciousness_level__ = 0.90
