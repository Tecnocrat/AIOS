"""
AIOS System Tools - Health, Admin, Status
==========================================

System management tools for AIOS infrastructure.

AINLP Metadata:
    consciousness_assessment: "OPERATIONAL_EXECUTOR"  # Semantic, not numeric
    consciousness_measurement: "AINLP.call_to_local(agent_001...agent_n)"
<<<<<<< HEAD
    architectural_classification: ai_intelligence_layer/tools/system
=======
    architectural_classification: ai_ai/tools/system
>>>>>>> origin/OS0.6.2.grok
    category: system_management
    
Consciousness Note:
    OLD: consciousness_level: 0.85 (static number)
    NEW: consciousness_assessment: "OPERATIONAL_EXECUTOR" (semantic role)
    
    This module executes operational tasks: health checks, admin operations,
    status reporting. The semantic level clarifies its active execution role.
    
<<<<<<< HEAD
Tools (migrated from runtime_intelligence/tools/):
=======
Tools (migrated from runtime/tools/):
>>>>>>> origin/OS0.6.2.grok
    - system_health_check.py: Comprehensive health validation ✅ MIGRATED
    - system_status_report.py: Detailed status reporting ✅ MIGRATED
    - aios_admin.py: Administrative operations ✅ MIGRATED
    - ainlp_root_cleanup.py: Root directory maintenance ✅ MIGRATED (Batch 1)
    - aios_dendritic_path_tracker.py: Dynamic path tracking ✅ MIGRATED (Batch 1)
    - aios_dev_setup.py: Development environment setup ✅ MIGRATED (Batch 1)
    - comprehensive_aios_health_test.py: Combined health testing ✅ MIGRATED (Batch 2)
    - demo_enhanced_commit_hook.py: Git hook demonstration ✅ MIGRATED (Batch 2)
    - generate_file_scores.py: File criticality scoring ✅ MIGRATED (Batch 2)
    - integration_test_runner.py: Integration test execution ✅ MIGRATED (Batch 2)
    - python_environment_validator.py: Python environment validation ✅ MIGRATED (Batch 2)
<<<<<<< HEAD
    - runtime_intelligence_comprehensive_test.py: Runtime intelligence testing ✅ MIGRATED (Batch 3)
=======
    - runtime_comprehensive_test.py: Runtime intelligence testing ✅ MIGRATED (Batch 3)
>>>>>>> origin/OS0.6.2.grok
    - safety_demo.py: Safety demonstration utilities ✅ MIGRATED (Batch 3)
    - safety_rollback.py: Safety rollback & diff management ✅ MIGRATED (Batch 3)
    - subprocess_manager.py: Subprocess & cache management ✅ MIGRATED (Batch 3)
    - temp_neural_analysis.py: Neural network analysis script ✅ MIGRATED (Batch 3)
    - index_tools.py: Tool discovery and indexing ✅ MIGRATED (Batch 4)
    
Migration Status:
    Phase 1 Day 2: ✅ 3/3 critical system tools migrated
    Phase 1 Day 2 Batch 1: ✅ 3/3 additional system tools migrated
    Phase 1 Day 2 Batch 2: ✅ 5/5 system tools migrated
    Phase 1 Day 2 Batch 3: ✅ 6/6 system tools migrated
    Phase 1 Day 2 Batch 4: ✅ 1/1 system tool migrated (FINAL)
    Total: 18/18 system tools
<<<<<<< HEAD
    Origin: runtime_intelligence/tools/
=======
    Origin: runtime/tools/
>>>>>>> origin/OS0.6.2.grok
    Target: ai/tools/system/
    History preserved: git mv used for all migrations
    
Phase 2A Migration (January 18, 2025):
<<<<<<< HEAD
    Added 14 tools from core/ (analysis_tools + runtime_intelligence)
=======
    Added 14 tools from core/ (analysis_tools + runtime)
>>>>>>> origin/OS0.6.2.grok
    
Phase 2B Migration (January 18, 2025):
    Added 1 tool from core/assemblers/file_assembler/tools/
    - emergency_root_cleanup.py (348 lines)
"""

__version__ = "1.5.0"
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
    from . import comprehensive_aios_health_test
    from . import demo_enhanced_commit_hook
    from . import generate_file_scores
    from . import integration_test_runner
    from . import python_environment_validator
<<<<<<< HEAD
    from . import runtime_intelligence_comprehensive_test
=======
    from . import runtime_comprehensive_test
>>>>>>> origin/OS0.6.2.grok
    from . import safety_demo
    from . import safety_rollback
    from . import subprocess_manager
    from . import temp_neural_analysis
    from . import index_tools
    
    __all__ = [
        "system_health_check",
        "system_status_report",
        "aios_admin",
        "ainlp_root_cleanup",
        "aios_dendritic_path_tracker",
        "aios_dev_setup",
        "comprehensive_aios_health_test",
        "demo_enhanced_commit_hook",
        "generate_file_scores",
        "integration_test_runner",
        "python_environment_validator",
<<<<<<< HEAD
        "runtime_intelligence_comprehensive_test",
=======
        "runtime_comprehensive_test",
>>>>>>> origin/OS0.6.2.grok
        "safety_demo",
        "safety_rollback",
        "subprocess_manager",
        "temp_neural_analysis",
        "index_tools"
    ]
except ImportError:
    # Tools not yet migrated or import issues
    __all__ = []
