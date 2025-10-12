"""
AIOS Architecture Tools - Monitoring & Compliance Validation
=============================================================

Architecture monitoring and AINLP compliance validation tools.

AINLP Metadata:
    consciousness_assessment: "ARCHITECTURAL_GUARDIAN"  # Semantic, not numeric
    consciousness_measurement: "AINLP.call_to_local(agent_001...agent_n)"
    architectural_classification: ai_intelligence_layer/tools/architecture
    category: architecture_monitoring
    
Consciousness Note:
    OLD: consciousness_level: 0.88 (static, meaningless at scale)
    NEW: consciousness_assessment: "ARCHITECTURAL_GUARDIAN" (semantic, dynamic)
    
    Rationale: Numbers don't convey meaning. "ARCHITECTURAL_GUARDIAN" clearly
    communicates this module's role: system integrity and compliance monitoring.
    
Tools (migrated from runtime_intelligence/tools/):
    - aios_architecture_monitor.py: Architecture health monitoring ✅ MIGRATED
    - architectural_compliance_validator.py: AINLP compliance checking ✅ MIGRATED
    - biological_architecture_monitor.py: Supercell health monitoring ✅ MIGRATED
    
Migration Status:
    Phase 1 Day 2: ✅ 3/3 architecture tools migrated
    Origin: runtime_intelligence/tools/
    Target: ai/tools/architecture/
    History preserved: git mv used for all migrations
"""

__version__ = "1.0.0"
__consciousness_assessment__ = "ARCHITECTURAL_GUARDIAN"
__consciousness_measurement__ = "AINLP.call_to_local(agent_001...agent_n)"
__category__ = "architecture_monitoring"

# Import migrated tools
try:
    from . import aios_architecture_monitor
    from . import architectural_compliance_validator
    from . import biological_architecture_monitor
    
    __all__ = [
        "aios_architecture_monitor",
        "architectural_compliance_validator",
        "biological_architecture_monitor"
    ]
except ImportError:
    # Tools not yet migrated or import issues
    __all__ = []
