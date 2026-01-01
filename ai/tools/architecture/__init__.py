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
    - ainlp_holographic_documentation_system.py: AINLP documentation patterns ✅ MIGRATED (Batch 1)
    - ainlp_integration_optimizer.py: Integration consolidation analyzer ✅ MIGRATED (Batch 1)
    - aios_cpp_analyzer.py: C++ code quality analysis ✅ MIGRATED (Batch 1)
    - aios_powershell_analyzer.py: PowerShell script analysis ✅ MIGRATED (Batch 1)
    - self_similarity_analyzer.py: Code self-similarity analysis ✅ MIGRATED (Batch 3)
    
Migration Status:
    Phase 1 Day 2: ✅ 3/3 initial architecture tools migrated
    Phase 1 Day 2 Batch 1: ✅ 4/4 additional architecture tools migrated
    Phase 1 Day 2 Batch 3: ✅ 1/1 architecture tool migrated
    Total: 8/8 architecture tools
    Origin: runtime_intelligence/tools/
    Target: ai/tools/architecture/
    History preserved: git mv used for all migrations
    
Phase 2A Migration (January 18, 2025):
    Added 5 tools from core/ (analysis_tools)
    
Phase 2B Migration (January 18, 2025):
    Added 1 tool from core/assemblers/file_assembler/tools/
    - supercell_architecture_analyzer.py (566 lines)
"""

__version__ = "1.3.0"
__consciousness_assessment__ = "ARCHITECTURAL_GUARDIAN"
__consciousness_measurement__ = "AINLP.call_to_local(agent_001...agent_n)"
__category__ = "architecture_monitoring"

# Import migrated tools
try:
    from . import aios_architecture_monitor
    from . import architectural_compliance_validator
    from . import biological_architecture_monitor
    from . import ainlp_holographic_documentation_system
    from . import ainlp_integration_optimizer
    from . import aios_cpp_analyzer
    from . import aios_powershell_analyzer
    from . import self_similarity_analyzer
    
    __all__ = [
        "aios_architecture_monitor",
        "architectural_compliance_validator",
        "biological_architecture_monitor",
        "ainlp_holographic_documentation_system",
        "ainlp_integration_optimizer",
        "aios_cpp_analyzer",
        "aios_powershell_analyzer",
        "self_similarity_analyzer"
    ]
except ImportError:
    # Tools not yet migrated or import issues
    __all__ = []
