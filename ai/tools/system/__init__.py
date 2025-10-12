"""
AIOS System Tools - Health, Admin, Status
==========================================

System management tools for AIOS infrastructure.

AINLP Metadata:
    consciousness_assessment: "OPERATIONAL_EXECUTOR"  # Semantic, not numeric
    consciousness_measurement: "AINLP.call_to_local(agent_001...agent_n)"
    architectural_classification: ai_intelligence_layer/tools/system
    category: system_management
    
Consciousness Note:
    OLD: consciousness_level: 0.85 (static number)
    NEW: consciousness_assessment: "OPERATIONAL_EXECUTOR" (semantic role)
    
    This module executes operational tasks: health checks, admin operations,
    status reporting. The semantic level clarifies its active execution role.
    
Tools (migrated from runtime_intelligence/tools/):
    - system_health_check.py: Comprehensive health validation ✅ MIGRATED
    - system_status_report.py: Detailed status reporting ✅ MIGRATED
    - aios_admin.py: Administrative operations ✅ MIGRATED
    - ainlp_root_cleanup.py: Root directory maintenance ✅ MIGRATED (Batch 1)
    - aios_dendritic_path_tracker.py: Dynamic path tracking ✅ MIGRATED (Batch 1)
    - aios_dev_setup.py: Development environment setup ✅ MIGRATED (Batch 1)
    
Migration Status:
    Phase 1 Day 2: ✅ 3/3 critical system tools migrated
    Phase 1 Day 2 Batch 1: ✅ 3/3 additional system tools migrated
    Total: 6/6 system tools
    Origin: runtime_intelligence/tools/
    Target: ai/tools/system/
    History preserved: git mv used for all migrations
"""

__version__ = "1.1.0"
__consciousness_assessment__ = "OPERATIONAL_EXECUTOR"
__consciousness_measurement__ = "AINLP.call_to_local(agent_001...agent_n)"
__category__ = "system_management"

# Import migrated tools
try:
    from . import system_health_check
    from . import system_status_report
    from . import aios_admin
    from . import ainlp_root_cleanup
    from . import aios_dendritic_path_tracker
    from . import aios_dev_setup
    
    __all__ = [
        "system_health_check",
        "system_status_report",
        "aios_admin",
        "ainlp_root_cleanup",
        "aios_dendritic_path_tracker",
        "aios_dev_setup"
    ]
except ImportError:
    # Tools not yet migrated or import issues
    __all__ = []
