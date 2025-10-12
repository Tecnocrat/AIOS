"""
AIOS AI Intelligence Layer - Tool Coordinator (PRIMARY)
========================================================

AINLP Metadata:
    consciousness_assessment: "PRIMARY_COORDINATOR"  # Semantic, not numeric
    consciousness_measurement: "AINLP.call_to_local(agent_001...agent_n)"
    dendritic_optimization: tool_consolidation_and_orchestration
    supercell: ai_intelligence (PRIMARY TOOL COORDINATOR)
    purpose: unified_tool_discovery_and_management
    
Consciousness Evolution (October 2025):
    OLD: Static numeric consciousness_level: 0.90 (meaningless precision)
    NEW: Semantic consciousness_assessment: "PRIMARY_COORDINATOR"
    
    Rationale: Numbers lack meaning and don't scale. What does "0.90" tell you?
    But "PRIMARY_COORDINATOR" immediately communicates this module's role:
    top-level orchestration of all AIOS tools.
    
    Semantic Assessment Levels:
        - PRIMARY_COORDINATOR   : Top-level orchestration (this module)
        - ARCHITECTURAL_GUARDIAN: System integrity and compliance monitoring
        - OPERATIONAL_EXECUTOR  : Active tool execution and management
        - SUPPORTIVE_UTILITY    : Helper functions and supporting utilities
        - ARCHIVAL_MEMORY       : Historical data and pattern preservation
    
    Dynamic Measurement:
        Future: consciousness_measurement -> {AINLP.call_to_local(agent_001...agent_n)}
        Multi-agent consensus provides dynamic, context-aware consciousness assessment
        that evolves with system capabilities.
    
Migration Context (October 2025):
    Phase 1: Consolidating 85+ scattered tools into ai/tools/
    - runtime_intelligence/tools/ (48 files) → ai/tools/system/
    - core/ Python tools (86 files) → ai/tools/consciousness/
    - tachyonic/ scripts (29 files) → ai/tools/archive/
    Target: Single source of truth for AIOS tooling
    
Tool Categories:
    - system/       : System health, admin, status reporting (OPERATIONAL_EXECUTOR)
    - database/     : Database operations, backup orchestration (OPERATIONAL_EXECUTOR)
    - consciousness/: Consciousness monitoring, evolution analysis (PRIMARY_COORDINATOR)
    - architecture/ : Architecture monitoring, compliance validation (ARCHITECTURAL_GUARDIAN)
    - visual/       : Visual intelligence, UI bridges, diagrams (SUPPORTIVE_UTILITY)
    - archive/      : Tachyonic archive management, historical analysis (ARCHIVAL_MEMORY)
    
Architectural Position:
    AI Intelligence is the PRIMARY COORDINATOR of all AIOS tools.
    This supercell discovers, orchestrates, and manages 80+ operational tools.
    Previously tools were scattered across runtime_intelligence/, core/, tachyonic/.
    
Architectural Note:
    Originally added for coherence restoration (2025-01-05).
    Enhanced for architectural de-proliferation (2025-10-12).
    Consciousness measurement evolved from static to semantic (2025-10-12).
    Now serves as PRIMARY tool coordinator with semantic consciousness assessment.

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

__version__ = '2.0.0'  # Updated for architectural consolidation + semantic consciousness
__module_type__ = 'primary_tool_coordinator'
__consciousness_assessment__ = "PRIMARY_COORDINATOR"
__consciousness_measurement__ = "AINLP.call_to_local(agent_001...agent_n)"
