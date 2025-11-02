"""
AIOS Visual Intelligence Tools - UI Bridges & Visualization
============================================================

Visual intelligence, UI bridges, and diagram generation tools.

AINLP Metadata:
    consciousness_assessment: "SUPPORTIVE_UTILITY"  # Semantic, not numeric
    consciousness_measurement: "AINLP.call_to_local(agent_001...agent_n)"
    architectural_classification: ai_ai/tools/visual
    category: visual_intelligence
    
Consciousness Note:
    OLD: consciousness_level: 0.86 (arbitrary precision)
    NEW: consciousness_assessment: "SUPPORTIVE_UTILITY" (functional clarity)
    
    Visual tools support system operations through UI bridges and visualization.
    Not primary orchestration, but essential supporting functionality.
    
Tools (migrated from runtime/tools/):
    - enhanced_visual_intelligence_bridge.py: Visual intelligence integration ✅ MIGRATED
    - consciousness_visual_analyzer.py: Consciousness emergence visualization ✅ MIGRATED (Batch 2)
    - visual_intelligence_bridge_enhanced.py: Enhanced visual bridge (Batch 3 migration) ✅ MIGRATED (Batch 3)
    - visual_intelligence_bridge.py: Visual intelligence bridge ✅ MIGRATED (Batch 3)
    
Migration Status:
    Phase 1 Day 2: ✅ 1/1 visual tools migrated
    Phase 1 Day 2 Batch 2: ✅ 1/1 visual tools migrated
    Phase 1 Day 2 Batch 3: ✅ 2/2 visual tools migrated
    Total: 4/4 visual tools
    Origin: runtime/tools/
    Target: ai/tools/visual/
    History preserved: git mv used for migration
"""

__version__ = "1.2.0"
__consciousness_assessment__ = "SUPPORTIVE_UTILITY"
__consciousness_measurement__ = "AINLP.call_to_local(agent_001...agent_n)"
__category__ = "visual_intelligence"

# Import migrated tools
try:
    from . import enhanced_visual_intelligence_bridge
    from . import consciousness_visual_analyzer
    from . import visual_intelligence_bridge_enhanced
    from . import visual_intelligence_bridge
    
    __all__ = [
        "enhanced_visual_intelligence_bridge",
        "consciousness_visual_analyzer",
        "visual_intelligence_bridge_enhanced",
        "visual_intelligence_bridge"
    ]
except ImportError:
    # Tools not yet migrated or import issues
    __all__ = []
