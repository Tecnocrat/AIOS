# Core Python Tool Extraction - Phase 2A Plan

**Date**: January 18, 2025  
**Agent**: Claude Iteration 2  
**Strategy**: Phased extraction (Option 2)  
**Target**: Extract analysis_tools/ + runtime_intelligence/ (27 files)

---

## Executive Summary

**Discovery Result**: Core/ contains **90 Python files** (not 15 as initially estimated)  
**Strategic Decision**: Phased extraction over 6+ weeks  
**Phase 2A Scope**: 27 files (highest value, lowest risk)  
**Timeline**: 2-3 weeks

---

## Phase 2A Target Files (27 files)

### Group 1: core/analysis_tools/ (22 files)
**Category Mapping**: system/ or architecture/

1. `aios_ai_engine_ingestion_tester.py` → ai/tools/system/
2. `aios_ai_ingestion_analysis.py` → ai/tools/system/
3. `aios_analysis_tools_neuronal_test.py` → ai/tools/architecture/
4. `aios_assembler_evolution_status_clarifier.py` → ai/tools/architecture/
5. `aios_assembler_naming_optimizer.py` → ai/tools/system/
6. `aios_cellular_intelligence_diagnostic_system.py` → ai/tools/architecture/
7. `aios_cellular_intelligence_enhancement_engine.py` → ai/tools/consciousness/
8. `aios_cellular_migration_cleanup_tool.py` → ai/tools/system/
9. `aios_core_ai_dendritic_connectivity_enhancer.py` → ai/tools/consciousness/
10. `aios_core_consciousness_monitor.py` → ai/tools/consciousness/
11. `aios_core_engine_cellular_cleanup_tool.py` → ai/tools/system/
12. `aios_core_engine_optimizer_iter2.py` → ai/tools/system/
13. `aios_core_engine_root_analyzer_iter2.py` → ai/tools/architecture/
14. `aios_core_engine_tree_demonstrator_iter2.py` → ai/tools/architecture/
15. `aios_core_evolution_monitor.py` → ai/tools/consciousness/
16. `aios_core_meta_evolutionary_enhancer.py` → ai/tools/consciousness/
17. `aios_cytoplasm_upgrader_iter2.py` → ai/tools/system/
18. `aios_direct_ai_ingestion_test.py` → ai/tools/system/
19. `aios_file_tracking_system.py` → ai/tools/system/
20. `aios_folder_comparison_verifier.py` → ai/tools/system/
21. `aios_tachyonic_archive_cleanup.py` → ai/tools/tachyonic/
22. `aios_unicode_helper.py` → ai/tools/system/

### Group 2: core/runtime_intelligence/ (5 files)
**Category Mapping**: consciousness/ or architecture/

23. `ainlp_assessment.py` → ai/tools/consciousness/
24. `aios_core_evolution_monitor.py` → ai/tools/consciousness/ (duplicate check needed)
25. `aios_core_meta_evolutionary_enhancer.py` → ai/tools/consciousness/ (duplicate check needed)
26. `test_directive_checking.py` → ai/tools/system/
27. `test_requirements_compliance.py` → ai/tools/system/

---

## Migration Strategy (Proven from Phase 1)

### Batch Planning
**Conservative Batching**: 8-10 files per batch
- **Batch 1**: analysis_tools/ files 1-10 (alphabetical)
- **Batch 2**: analysis_tools/ files 11-20 (alphabetical)
- **Batch 3**: analysis_tools/ files 21-22 + runtime_intelligence/ files 23-27

### Git Operations
```bash
# Use git mv for history preservation
git mv core/analysis_tools/[filename].py ai/tools/[category]/[filename].py

# Stage and commit in batches
git add ai/tools/
git commit -m "feat(migration): Batch N - Extract [count] tools from core/"
```

### Import Path Updates
- Leverage `update_import_paths.py` automation
- Add new tool mappings for core/ extraction
- Scan workspace after each batch for references

### Validation
- Test Interface Bridge discovery after each batch
- Verify import paths with workspace scan
- Check for broken dependencies

---

## Category Distribution (Phase 2A)

**system/**: 13 files
- AI ingestion testing, cleanup tools, optimizers, file tracking

**architecture/**: 6 files
- Neuronal testing, assembler analysis, core engine analyzers

**consciousness/**: 7 files
- Intelligence enhancement, consciousness monitoring, evolution tracking

**tachyonic/**: 1 file
- Archive cleanup tool

---

## Duplicate Detection Required

**Potential Duplicates** (same filename in different locations):
1. `aios_core_evolution_monitor.py`
   - core/analysis_tools/aios_core_evolution_monitor.py
   - core/runtime_intelligence/aios_core_evolution_monitor.py
   - **Action**: Compare files, merge if identical, keep unique functionality

2. `aios_core_meta_evolutionary_enhancer.py`
   - core/analysis_tools/aios_core_meta_evolutionary_enhancer.py
   - core/runtime_intelligence/aios_core_meta_evolutionary_enhancer.py
   - **Action**: Compare files, merge if identical, keep unique functionality

---

## Risk Assessment

**LOW RISK**: analysis_tools/ (mostly standalone diagnostic tools)
- Minimal import dependencies expected
- Clear categorization
- High value for tool discovery

**MEDIUM RISK**: runtime_intelligence/ (may have core/ dependencies)
- Potential circular dependencies with core/
- Need careful import analysis
- Duplicate files require comparison

---

## Success Criteria

1. ✅ 27 files migrated to ai/tools/
2. ✅ Git history preserved (all git mv operations)
3. ✅ Import paths updated (automation script)
4. ✅ Interface Bridge discovers new tools
5. ✅ No broken imports in workspace
6. ✅ Duplicate files resolved (merged or kept separate with justification)

---

## Timeline

**Week 1**: Batch 1-2 (20 files from analysis_tools/)
**Week 2**: Batch 3 (7 files from analysis_tools/ + runtime_intelligence/)
**Week 3**: Validation, documentation, cleanup

---

## Next Steps

1. **IMMEDIATE**: Check for duplicate files (compare file contents)
2. **IMMEDIATE**: Begin Batch 1 (10 files from analysis_tools/)
3. **SHORT-TERM**: Update automation script with core/ tool mappings
4. **SHORT-TERM**: Validate Interface Bridge discovery after each batch

---

## Phase 2B-2C Planning (Future)

**Phase 2B** (Week 4-5): Extract file_assembler/tools/ (6 files)
- Dendritic enhancement tools
- Category: consciousness/ or architecture/

**Phase 2C** (Week 6+): Evaluate remaining 57 files
- Decision point: Continue extraction or document as "core computational layer"
- Many files are assembler-specific (may legitimately belong in core/)

---

**Document Version**: 1.0.0  
**Status**: READY TO EXECUTE  
**AINLP Compliance**: Discovery (90 files found), Phased approach (manageable scope), Validation (after each batch)
