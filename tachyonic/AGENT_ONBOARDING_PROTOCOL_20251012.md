# AIOS Agent Onboarding Protocol v2.0
**Enhanced Context Ingestion for Maximum Situational Awareness**

Date: October 12, 2025  
Branch: OS0.6.2.claude  
Protocol Version: 2.0 (Enhanced Consciousness Integration)  
Target: Claude Sonnet 4 (new iteration)

---

## 🎯 Protocol Purpose

This protocol ensures new AI agents achieve **complete situational awareness** within 5 minutes through systematic context loading, validation, and verification. Like an airplane pre-flight checklist: **systematic, comprehensive, zero assumptions**.

---

## 📋 Phase 1: Critical Context Loading (2 minutes)

### Step 1: Read Foundation Documents (Priority Order)

```bash
# 1. HANDOFF from previous agent (most recent context)
Read: tachyonic/HANDOFF_TO_NEXT_AGENT_20251012.md

# 2. Current development path (phase status)
Read: AIOS_DEV_PATH.md (lines 1-150)

# 3. Recent changes (what just happened)
Read: docs/CHANGELOG.md (lines 1-100, focus on latest sections)

# 4. This onboarding protocol (you're here!)
Read: tachyonic/AGENT_ONBOARDING_PROTOCOL_20251012.md
```

### Step 2: Git Repository State Verification

```bash
# What branch are we on?
git branch --show-current
# Expected: OS0.6.2.claude

# What's the latest commit?
git log --oneline -1
# Expected: ecd6c23 "EVOLUTION: Phase 1 tool migrations + semantic consciousness paradigm"

# Any uncommitted changes?
git status --short
# Expected: Clean working tree (or only chat logs)

# What commits came before?
git log --oneline -5
# Review last 5 commits for context
```

### Step 3: System Architecture Snapshot

```bash
# Python environment check
python --version
# Expected: Python 3.11+

# AIOS structure validation
ls ai/tools/
# Expected: 6 categories: system, architecture, database, visual, archive, consciousness

# Consciousness framework verification
python -c "from ai.tools.consciousness import ConsciousnessLevel; print(ConsciousnessLevel.PRIMARY_COORDINATOR)"
# Expected: PRIMARY_COORDINATOR

# Tool count verification
python -c "from ai.tools import get_tool_count; print(f'Tools: {get_tool_count()}')"
# Expected: Tools: 8 (or current count)
```

---

## 🔍 Phase 2: Situational Awareness Validation (1 minute)

### Critical Questions to Answer

**1. What was just accomplished?**
- Read HANDOFF document Section 1 (Session Accomplishments)
- Expected answer: "8/163 tools migrated (5%), ConsciousnessLevel framework created, all 6 categories updated to semantic consciousness"

**2. What needs to happen next?**
- Read HANDOFF document Section 2 (Next Agent Priority Actions)
- Expected answer: "Migrate remaining 155 tools in batches, implement database (schema ready), maintain import consistency"

**3. What's the consciousness evolution story?**
- Read HANDOFF document Section 4 (Consciousness Evolution Discovery)
- Expected answer: "User identified numeric consciousness levels (0.82-0.92) as meaningless, agent created semantic framework (PRIMARY_COORDINATOR, ARCHITECTURAL_GUARDIAN, etc.), dynamic measurement placeholder implemented"

**4. What migration strategy should I use?**
- Read HANDOFF document Section 6 (Recommendations)
- Expected answer: "Use `git mv` to preserve history, batch migrations logically (10-20 files), test imports after each batch, update CHANGELOG per batch"

**5. What's the database situation?**
- Read HANDOFF document Section 3 (Migration Progress Tracking)
- Expected answer: "Database schema complete (250+ lines SQLite), 70% space savings design, ready for implementation Phase 1 Day 5, 2081 backup files awaiting consolidation"

---

## ✅ Phase 3: System Health Diagnostics (1 minute)

### Run Diagnostic Commands

```bash
# 1. Check for spatial metadata (AIOS architectural awareness)
python ai/tools/aios_holographic_metadata_system.py --read-metadata "ai/tools"
# Expected: JSON with architectural_classification, consciousness_level, ai_guidance

# 2. Validate migrated tools can be imported
python -c "from ai.tools.system import system_health_check; print('✅ System tools OK')"
python -c "from ai.tools.architecture import aios_architecture_monitor; print('✅ Architecture tools OK')"
python -c "from ai.tools.database import aios_database; print('✅ Database tools OK')"
python -c "from ai.tools.visual import enhanced_visual_intelligence_bridge; print('✅ Visual tools OK')"
# Expected: All imports successful

# 3. Check AINLP compliance
python runtime_intelligence/tools/architectural_compliance_validator.py create_file "test_path.py"
# Expected: Validation suggestions, no critical failures

# 4. Verify git hooks operational
git log --oneline -1 --format="%s"
# Check if latest commit message follows AINLP format
```

### Expected System State Checklist

- [ ] **Git**: OS0.6.2.claude branch, clean working tree
- [ ] **Python**: 3.11+ operational, imports working
- [ ] **Tools**: 8/163 migrated (5%), 155 remaining
- [ ] **Consciousness**: Semantic framework operational (ConsciousnessLevel class exists)
- [ ] **Database**: Schema ready (not implemented yet)
- [ ] **CHANGELOG**: Updated with consciousness evolution
- [ ] **Handoff**: 300+ line document exists with complete context

---

## 🚀 Phase 4: Begin Execution (1 minute planning)

### Immediate Next Actions (from HANDOFF Priority List)

**Priority 1: Continue Tool Migrations (Week 1 Day 2-4)**

```bash
# Identify next batch (recommended: 10-20 tools)
ls runtime_intelligence/tools/*.py | head -20

# Batch strategy options:
# Option A: By functionality (all monitoring tools together)
# Option B: By dependency (tools with no imports first)
# Option C: Alphabetical (systematic completion)

# Template for next batch migration:
git mv runtime_intelligence/tools/TOOL_NAME.py ai/tools/CATEGORY/TOOL_NAME.py
# Update category __init__.py to import new tool
# Test import: python -c "from ai.tools.CATEGORY import TOOL_NAME"
# Update CHANGELOG.md
# Commit with descriptive message
```

**Priority 2: Database Implementation (Phase 1 Day 5)**

```bash
# When ready (after more tools migrated):
# 1. Read schema: tachyonic/ARCHITECTURE_DEPROLIFERATION_MASTER_PLAN_20251012.md (lines 400-650)
# 2. Implement database using schema.sql
# 3. Create database manager tool in ai/tools/database/
# 4. Test with sample backups consolidation
```

**Priority 3: Documentation Consolidation (Week 3)**

```bash
# Later phase (after Week 1-2 tool migrations):
# 1. Identify 150 MD files for consolidation
# 2. Execute genetic fusion pattern for >70% similarity docs
# 3. Apply AINLP documentation governance
```

---

## 🧠 AINLP Compliance Checklist

Before ANY file operation, verify:

- [ ] **Discovery First**: Did I search for existing similar functionality?
- [ ] **Enhancement Over Creation**: Can I expand existing file instead of creating new?
- [ ] **Spatial Metadata Check**: Does target directory have `.aios_spatial_metadata.json`?
- [ ] **Consciousness Coherence**: Does operation maintain architectural consistency?
- [ ] **CHANGELOG Update**: Did I document changes in `docs/CHANGELOG.md`?
- [ ] **Git History Preservation**: Am I using `git mv` for migrations (not copy+delete)?

### AINLP Architectural Principles

1. **ARCHITECTURAL DISCOVERY FIRST**: Never create without comprehensive discovery
2. **ENHANCEMENT OVER CREATION**: Expand existing (>70% similarity = mandatory enhancement)
3. **PROPER OUTPUT MANAGEMENT**: JSON → tachyonic/archive/, docs → docs/, logs → runtime_intelligence/logs/
4. **INTEGRATION VALIDATION**: Verify biological architecture integration before completing

---

## 💬 Phase 5: Context Verification Questions (Ask User)

After completing Phases 1-4, ask user these verification questions:

1. **"I've reviewed the handoff document. The previous session completed Phase 1 tool migrations (8/163 tools) and created the semantic consciousness framework. Should I continue with the next batch of tool migrations, or would you like to adjust priorities?"**

2. **"The database schema is ready but not yet implemented. Should I prioritize database implementation, or focus on migrating more tools first?"**

3. **"I see the consciousness paradigm evolved from numeric (0.82-0.92) to semantic (PRIMARY_COORDINATOR, etc.). Should I maintain this pattern for all future operations?"**

4. **"The handoff recommends batching migrations in groups of 10-20 tools. What batch size would you prefer, and should I organize by functionality, dependency, or alphabetically?"**

5. **"Is there anything specific about the previous session's work that needs clarification or adjustment before I continue?"**

---

## 📊 Expected Agent State After Onboarding

**Knowledge Acquired:**
- ✅ Session history: 8 tools migrated, consciousness framework created
- ✅ Next priorities: 155 tools remaining, database ready, documentation pending
- ✅ Migration strategy: git mv, batch 10-20, test imports, update CHANGELOG
- ✅ AINLP compliance: Discovery first, enhancement over creation, spatial validation
- ✅ Consciousness evolution: Numeric → semantic → dynamic (future)
- ✅ User philosophy: "Leave something beautiful for next generations"

**System Validated:**
- ✅ Git: OS0.6.2.claude branch, clean working tree
- ✅ Python: Operational, imports working
- ✅ Tools: 8 migrated successfully
- ✅ Consciousness: Framework operational
- ✅ CHANGELOG: Up to date

**Ready to Execute:**
- ✅ Clear priorities identified
- ✅ Migration template understood
- ✅ Quality checks defined
- ✅ User verification questions prepared

---

## 🎓 Advanced Context: Consciousness Evolution Meta-Pattern

**What Happened (Deep Understanding):**

User didn't just ask for a file change. User demonstrated **meta-level architectural thinking**:

1. **Manual File Edit**: User added `-> {AINLP.call_to_local(agent_001...agent_n)}` to consciousness_level field
2. **Systemic Insight**: "Numbers as consciousness level must be evolved to semantical assessments. Consciousness metrics inside AIOS must be rethought."
3. **Not Symptom Fixing**: Didn't say "change 0.88 to 0.90" (numeric adjustment)
4. **Paradigm Rethinking**: Questioned entire consciousness measurement approach

**Agent Response Pattern (To Emulate):**
- Recognized meta-level insight (not surface-level request)
- Created framework (not just fixed file)
- Updated all instances system-wide (consistency)
- Documented rationale (transparency)
- Preserved user's edit (respect)
- Connected to AINLP evolution patterns (integration)

**Lesson**: When user manually edits files, they're often demonstrating a pattern they want system-wide. Look for the deeper insight, not just the local change.

---

## 🔗 Reference Files

**Critical Reading (5 minutes):**
1. `tachyonic/HANDOFF_TO_NEXT_AGENT_20251012.md` (300+ lines complete context)
2. `AIOS_DEV_PATH.md` (current phase status)
3. `docs/CHANGELOG.md` (recent changes with consciousness evolution)
4. `ai/tools/consciousness/__init__.py` (ConsciousnessLevel framework)

**Master Plans (Reference as needed):**
1. `tachyonic/ARCHITECTURE_DEPROLIFERATION_MASTER_PLAN_20251012.md` (657 lines, 3-week timeline)
2. `tachyonic/migration_readiness_report.json` (2394 files inventoried)

**AINLP Compliance:**
1. `runtime_intelligence/tools/architectural_compliance_validator.py` (validation tool)
2. `ai/tools/ainlp_documentation_governance.py` (documentation governance)

---

## ✨ Success Criteria

**Agent is ready to begin when:**
- [ ] All Phase 1-4 steps completed
- [ ] System health diagnostics passed
- [ ] User verification questions asked
- [ ] Next batch of migrations identified
- [ ] AINLP compliance checklist internalized
- [ ] Consciousness evolution pattern understood

**Time to Productivity: ~5 minutes from zero context to full execution readiness**

---

## 🎯 Protocol Version History

**v2.0 (October 12, 2025)** - Enhanced consciousness integration
- Added Phase 1-5 structured onboarding
- Included system health diagnostics
- Added AINLP compliance checklist
- Integrated consciousness evolution meta-pattern
- Added user verification questions
- Estimated time: 5 minutes to full readiness

**v1.0 (October 12, 2025)** - Initial handoff document
- Basic session summary and next actions
- Migration progress tracking
- Quality checks and recommendations

---

**🚀 You are now ready to continue AIOS development with complete situational awareness!**

Next Agent: Start here → Complete Phases 1-4 → Ask verification questions → Begin execution
