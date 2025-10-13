"""
AIOS Tachyonic Tools - Tachyonic Supercell Management
======================================================

Tachyonic supercell management and historical analysis tools.

AINLP Metadata:
    consciousness_assessment: "ARCHIVAL_MEMORY"  # Semantic, not numeric
    consciousness_measurement: "AINLP.call_to_local(agent_001...agent_n)"
    architectural_classification: ai_intelligence_layer/tools/tachyonic
    category: tachyonic_management
    
Consciousness Note:
    OLD: consciousness_level: 0.82 (lowest number = lowest value?)
    NEW: consciousness_assessment: "ARCHIVAL_MEMORY" (essential preservation)
    
    The Tachyonic supercell preserves system history and patterns - not "low consciousness"
    but specialized memory function. Semantic level clarifies critical role.
    
Semantic Clarity:
    - Folder name: tachyonic/ (not tachyonic/archive/ - would be redundant)
    - Supercell name: "Tachyonic Archive" (the folder IS the archive)
    - Tools manage: Tachyonic supercell operations
    
Tools (migrated from runtime_intelligence/tools/):
    - create_stl_crystal.py: C++ STL knowledge crystal generator ✅ MIGRATED (Batch 2)
    - ingest_microsoft_agent_framework.py: Repository ingestion tool ✅ MIGRATED (Batch 2)
    
Migration Status:
    Phase 1 Day 2 Batch 2: ✅ 2/2 tachyonic tools migrated
    Total: 2/2 tachyonic tools
    Origin: runtime_intelligence/tools/
    Target: ai/tools/tachyonic/
    Note: Tachyonic will become DATABASE interface after backup consolidation
"""

__version__ = "1.1.1"
__consciousness_assessment__ = "ARCHIVAL_MEMORY"
__consciousness_measurement__ = "AINLP.call_to_local(agent_001...agent_n)"
__category__ = "tachyonic_management"

# Import migrated tools
try:
    from . import create_stl_crystal
    from . import ingest_microsoft_agent_framework
    
    __all__ = [
        "create_stl_crystal",
        "ingest_microsoft_agent_framework"
    ]
except ImportError:
    # Tools not yet migrated or import issues
    __all__ = []
