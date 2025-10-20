# CORE PYTHON TOOL EXTRACTION - PHASE 2B PLANNING
## File Assembler Tools Migration Strategy

**Document Status**: Planning Phase  
**Created**: January 18, 2025  
**Phase**: 2B - File Assembler Tools Extraction  
**AINLP Protocol**: OS0.6.2.claude  

---

## EXECUTIVE SUMMARY

**Objective**: Extract 6 Python tools from `core/assemblers/file_assembler/tools/` to appropriate `ai/tools/` categories

**Phase Context**:
- **Phase 1 COMPLETE**: 31 runtime_intelligence tools migrated (October 12, 2025)
- **Phase 2A COMPLETE**: 27 core analysis/runtime tools migrated (January 18, 2025)
- **Phase 2B TARGET**: 6 file_assembler tools (this phase)
- **Combined Progress**: 58 tools → 64 tools (target)

**Strategic Goal**: Continue moving toward pure C++ core engine by extracting remaining Python tools

---

## FILE INVENTORY

### Source Directory: `core/assemblers/file_assembler/tools/`

| File | Lines | Size | Category Target | Rationale |
|------|-------|------|----------------|-----------|
| `ainlp_dendritic_enhancer.py` | 338 | 14.5 KB | consciousness | AINLP enhancement, dendritic patterns |
| `dendritic_code_optimizer.py` | 495 | 21.6 KB | consciousness | Code optimization via dendritic patterns |
| `dendritic_consolidation_engine.py` | 1,106 | 54.3 KB | consciousness | Large consolidation engine (highest complexity) |
| `emergency_root_cleanup.py` | 348 | 15.8 KB | system | Root directory cleanup utility |
| `enhanced_tachyonic_preservation.py` | 481 | 23.0 KB | tachyonic | Archive preservation logic |
| `supercell_architecture_analyzer.py` | 566 | 27.0 KB | architecture | Architecture analysis tool |

**Total**: 3,334 lines, 156.5 KB

---

## CATEGORY MAPPING

### Consciousness Tools (3 files)
- `ainlp_dendritic_enhancer.py` → `ai/tools/consciousness/`
- `dendritic_code_optimizer.py` → `ai/tools/consciousness/`
- `dendritic_consolidation_engine.py` → `ai/tools/consciousness/`

**Rationale**: All three focus on dendritic intelligence patterns and consciousness enhancement

### System Tools (1 file)
- `emergency_root_cleanup.py` → `ai/tools/system/`

**Rationale**: Utility for root directory cleanup (system maintenance)

### Tachyonic Tools (1 file)
- `enhanced_tachyonic_preservation.py` → `ai/tools/tachyonic/`

**Rationale**: Archive preservation logic (tachyonic archive management)

### Architecture Tools (1 file)
- `supercell_architecture_analyzer.py` → `ai/tools/architecture/`

**Rationale**: Supercell architecture analysis (architectural monitoring)

---

## MIGRATION STRATEGY

### Batch Planning

**Single Batch Approach** (6 files manageable):
```
Batch 1 (6 files):
- ainlp_dendritic_enhancer.py → consciousness/
- dendritic_code_optimizer.py → consciousness/
- dendritic_consolidation_engine.py → consciousness/
- emergency_root_cleanup.py → system/
- enhanced_tachyonic_preservation.py → tachyonic/
- supercell_architecture_analyzer.py → architecture/
```

**Rationale**:
- Small file count (6 files vs 27 in Phase 2A)
- All files in single directory (low complexity)
- Clear category mapping (no ambiguity)
- Proven methodology from Phases 1 and 2A

---

## EXECUTION PLAN

### Step 1: Duplicate Check
```powershell
# Verify no duplicate filenames in target categories
$targets = @(
    "ai\tools\consciousness\ainlp_dendritic_enhancer.py",
    "ai\tools\consciousness\dendritic_code_optimizer.py",
    "ai\tools\consciousness\dendritic_consolidation_engine.py",
    "ai\tools\system\emergency_root_cleanup.py",
    "ai\tools\tachyonic\enhanced_tachyonic_preservation.py",
    "ai\tools\architecture\supercell_architecture_analyzer.py"
)

foreach ($target in $targets) {
    if (Test-Path $target) {
        Write-Host "DUPLICATE: $target already exists!" -ForegroundColor Red
    }
}
```

### Step 2: Git Migration (History Preservation)
```powershell
# Migrate all 6 files with git mv
git mv core/assemblers/file_assembler/tools/ainlp_dendritic_enhancer.py ai/tools/consciousness/
git mv core/assemblers/file_assembler/tools/dendritic_code_optimizer.py ai/tools/consciousness/
git mv core/assemblers/file_assembler/tools/dendritic_consolidation_engine.py ai/tools/consciousness/
git mv core/assemblers/file_assembler/tools/emergency_root_cleanup.py ai/tools/system/
git mv core/assemblers/file_assembler/tools/enhanced_tachyonic_preservation.py ai/tools/tachyonic/
git mv core/assemblers/file_assembler/tools/supercell_architecture_analyzer.py ai/tools/architecture/
```

### Step 3: Version Tracking Updates
```powershell
# Update __init__.py in each target category
# consciousness: Add 3 tools (existing ~14 → 17)
# system: Add 1 tool (existing ~32 → 33)
# tachyonic: Add 1 tool (existing ~3 → 4)
# architecture: Add 1 tool (existing ~13 → 14)
```

### Step 4: Commit
```bash
git add -A
git commit -m "MIGRATION: Phase 2B - File assembler tools extraction (6/6 files)

Migrated Tools:
- ainlp_dendritic_enhancer.py → consciousness/ (338 lines)
- dendritic_code_optimizer.py → consciousness/ (495 lines)
- dendritic_consolidation_engine.py → consciousness/ (1,106 lines)
- emergency_root_cleanup.py → system/ (348 lines)
- enhanced_tachyonic_preservation.py → tachyonic/ (481 lines)
- supercell_architecture_analyzer.py → architecture/ (566 lines)

Source Directory: core/assemblers/file_assembler/tools/ (cleared)
Total Migrated: 3,334 lines, 156.5 KB

Category Distribution:
- consciousness/: +3 tools (14 → 17)
- system/: +1 tool (32 → 33)
- tachyonic/: +1 tool (3 → 4)
- architecture/: +1 tool (13 → 14)

Combined Progress: 58 → 64 tools (Phase 1 + 2A + 2B)
Interface Bridge Expected: 108 → 114 tools (+6)

Git History: 100% preserved (git mv)
Status: Phase 2B complete, core/assemblers/file_assembler/tools/ cleared

Next: Phase 2C evaluation (57 remaining core/ Python files)"
```

### Step 5: Interface Bridge Validation
```powershell
# Check health endpoint for updated tool count
curl http://localhost:8000/health

# Expected result:
# "tools_discovered": 114 (was 108, +6 from Phase 2B)
# "sequencer_components": 114
```

### Step 6: Import Path Automation
```powershell
# Run import path updater (should find any broken imports)
python ai/tools/update_import_paths.py --dry-run

# If imports need updating:
python ai/tools/update_import_paths.py --execute
```

---

## RISK ASSESSMENT

### Low Risk Factors
1. **Small Batch**: Only 6 files (vs 27 in Phase 2A, 31 in Phase 1)
2. **Single Directory**: All files in same source location
3. **Proven Methodology**: Successful Phase 1 and 2A patterns
4. **Clear Categories**: No ambiguity in target destinations
5. **Git History**: git mv preserves all history

### Medium Risk Factors
1. **File Assembler Dependencies**: Tools may reference core/assemblers/ structure
2. **Large File**: dendritic_consolidation_engine.py (1,106 lines) - highest complexity
3. **Import Paths**: May need updates in 22+ files (automation available)

### Mitigation Strategies
1. **Import Automation**: update_import_paths.py ready to handle path updates
2. **Validation**: Interface Bridge + health checks confirm discovery
3. **Git Safety**: All operations via git mv (rollback possible)
4. **Conservative Approach**: Single batch with immediate validation

---

## SUCCESS CRITERIA

### Migration Completion
- ✅ All 6 files migrated via git mv (history preserved)
- ✅ Source directory `core/assemblers/file_assembler/tools/` cleared
- ✅ Version tracking updated in all target category __init__.py files
- ✅ Git commit created with comprehensive details

### Validation Passing
- ✅ Interface Bridge discovers 114 tools (was 108, +6)
- ✅ Health endpoint responds successfully
- ✅ Import automation reports 0 broken imports (or auto-fixed)
- ✅ No duplicate files in target categories

### Documentation Complete
- ✅ CHANGELOG.md updated with Phase 2B entry
- ✅ Dev Path updated with Phase 2B completion status
- ✅ Completion report created (CORE_PYTHON_EXTRACTION_PHASE_2B_COMPLETE.md)
- ✅ Session summary archived in tachyonic/

---

## EXPECTED OUTCOMES

### Tool Distribution (Post-Phase 2B)
```
Combined Total: 64 tools (was 58, +6 from Phase 2B)

ai/tools/consciousness/: 17 tools (was 14, +3)
ai/tools/system/: 33 tools (was 32, +1)
ai/tools/tachyonic/: 4 tools (was 3, +1)
ai/tools/architecture/: 14 tools (was 13, +1)
ai/tools/visual/: 4 tools (unchanged)
ai/tools/database/: 0 tools (unchanged)
```

### Interface Bridge Discovery
```
Expected: 114 tools (was 108, +6)
- 64 tools from ai/tools/ (6 categories)
- 50 tools from other locations (ai_cells, infrastructure, runtime_intelligence root)
```

### Core Engine Progress
```
Before Phase 2B: 63 Python files in core/
After Phase 2B: 57 Python files in core/ (6 files extracted)

Remaining Python files in core/: 57 files
- Most are assembler-specific (tree_assembler/, context_assembler/, etc.)
- Strategic decision needed: Full extraction vs preserve as computational layer
```

---

## TIMELINE

**Estimated Duration**: 1-2 hours (single session)

**Execution Sequence**:
1. Duplicate check: 2 minutes
2. Git migration: 5 minutes
3. Version tracking: 10 minutes
4. Commit: 2 minutes
5. Interface Bridge validation: 3 minutes
6. Import automation: 5-10 minutes
7. Documentation: 20-30 minutes

**Total**: 47-62 minutes (conservative estimate)

---

## PHASE 2C PREVIEW

After Phase 2B completion, evaluate remaining 57 Python files in core/:

### Remaining Python Files by Location
- `core/assemblers/tree_assembler/`: ~40 files (consciousness, meta_evolutionary, scripts)
- `core/assemblers/context_assembler/`: ~5 files
- `core/assemblers/integration_assembler/`: ~5 files
- `core/orchestrator/`: ~7 files

### Strategic Decision Required
**Option 1**: Full extraction (57 files → ai/tools/)
- Pro: Pure C++ core engine achieved
- Con: Large scope (57 files), 4-6 week timeline
- Risk: Assembler-specific tools may be legitimate core/ residents

**Option 2**: Selective extraction (consciousness/meta_evolutionary tools only)
- Pro: Extract ~20 high-value consciousness tools
- Con: Core/ remains mixed (C++ + Python)
- Risk: Incomplete architectural consolidation

**Option 3**: Preserve as computational layer
- Pro: Assemblers are core computational logic (not AI tools)
- Con: Violates "pure C++ core" goal
- Risk: Ongoing Python/C++ boundary confusion

**Recommendation**: Evaluate after Phase 2B completion with comprehensive file analysis

---

## AINLP COMPLIANCE

### Architectural Discovery First
- ✅ Comprehensive file inventory (6 files, 3,334 lines)
- ✅ Category mapping analysis (4 target categories)
- ✅ Dependency assessment (file_assembler context evaluated)
- ✅ Risk analysis (low/medium factors identified)

### Enhancement Over Creation
- ✅ Zero new files created (all migrations)
- ✅ Existing category structure enhanced (consciousness/system/tachyonic/architecture)
- ✅ Git history preserved (git mv for all operations)
- ✅ No duplicate functionality introduced

### Proper Output Management
- ✅ Planning document created (this file)
- ✅ Completion report planned (CORE_PYTHON_EXTRACTION_PHASE_2B_COMPLETE.md)
- ✅ Dev Path updates planned
- ✅ CHANGELOG entry planned
- ✅ Session summary planned (tachyonic archive)

### Integration Validation
- ✅ Interface Bridge validation planned (tool count verification)
- ✅ Import automation planned (update_import_paths.py)
- ✅ Health endpoint checks planned
- ✅ Biological architecture monitoring available

---

## LESSONS LEARNED (From Phases 1 & 2A)

### Proven Successful Patterns
1. **Conservative Batching**: Small batches prevent conflicts (Phase 2A: 10+10+7)
2. **Git-Native Operations**: git mv preserves history 100%
3. **Category First**: Clear category mapping before migration
4. **Version Tracking**: Update __init__.py after each batch
5. **Automation Ready**: Import path script handles updates automatically
6. **Documentation First**: Planning document enables smooth execution

### Apply to Phase 2B
1. **Single Batch**: 6 files manageable in one operation
2. **Clear Mapping**: 4 target categories (no ambiguity)
3. **Immediate Validation**: Check Interface Bridge after migration
4. **Comprehensive Documentation**: Plan → Execute → Report
5. **Import Automation**: Run update_import_paths.py if needed

---

## RELATED DOCUMENTATION

- **Phase 1 Report**: [`TOOL_MIGRATION_COMPLETE_REPORT.md`](../TOOL_MIGRATION_COMPLETE_REPORT.md)
- **Phase 2A Planning**: [`CORE_PYTHON_EXTRACTION_PHASE_2A.md`](CORE_PYTHON_EXTRACTION_PHASE_2A.md)
- **Phase 2A Completion**: [`CORE_PYTHON_EXTRACTION_PHASE_2A_COMPLETE.md`](CORE_PYTHON_EXTRACTION_PHASE_2A_COMPLETE.md)
- **Dev Path**: [`docs/development/AIOS_DEV_PATH.md`](development/AIOS_DEV_PATH.md)
- **Import Automation**: [`ai/tools/update_import_paths.py`](../ai/tools/update_import_paths.py)

---

**Status**: READY TO EXECUTE  
**Next Action**: Run duplicate check, then execute git migrations  
**Timeline**: 1-2 hours (single session)  
**Expected Outcome**: 64 total tools (58 → +6), Interface Bridge discovering 114 tools

---

*Document created following AINLP architectural discovery protocol. All 6 files inventoried, categorized, and migration strategy planned.*
