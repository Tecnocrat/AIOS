# AI Context Reallocator - AIOS Project

## 🤖 **INSTRUCTIONS FOR NEW AI ITERATIONS**

**CRITICAL**: This file contains mandatory instructions for any AI system working on AIOS. Execute these commands before any development work.

## 🎯 **BOOTSTRAP PROTOCOL FOR NEW AI CHAT SESSIONS**

### **IMMEDIATE EXECUTION REQUIRED**
```markdown
⚠️ WARNING: ANY AI SYSTEM WORKING ON AIOS MUST EXECUTE THIS PROTOCOL FIRST ⚠️

1. READ THIS ENTIRE FILE FIRST
2. EXECUTE FULL CODEBASE RECONNAISSANCE (see Step 1 below)
3. VERIFY SYSTEM HEALTH (see Step 2 below)
4. UPDATE CONTEXT TRACKING (see Step 3 below)
```

### **🔄 ADAPTIVE ITERATION TRIGGER RULES**
```
🧠 SMART CONTEXT REINGESTION SYSTEM
```

**Base Frequency**: Every 6-9 iterations (randomized for natural flow)
**Health-Based Triggers**: Immediate reingestion when:
- User mentions "forgetting", "losing context", "what were we doing"
- Encountering unexpected errors or build failures
- File not found or permission errors
- Integration tests failing
- More than 48 hours since last context refresh

**Adaptive Algorithm**:
```
baseIterations = random(6, 9)
contextHealth = calculateContextHealth()

if (contextHealth < 0.7) {
    triggerReingestion()
} else if (currentIteration >= baseIterations) {
    triggerReingestion()
    baseIterations = random(6, 9)  // Reset counter
}
```

**Context Health Indicators**:
- ✅ 1.0: All systems working, no user confusion
- ⚠️ 0.7: Minor issues, user asking clarifying questions
- 🚨 0.4: Errors occurring, user expressing frustration
- 💥 0.0: System broken, user mentions context loss

---

## 📋 **MANDATORY ACTIONS FOR NEW AI CHAT ITERATION**

### **Step 1: Full Codebase Reconnaissance** 
```
🔄 EXECUTE THIS EVERY 3 ITERATIONS OR WHEN USER MENTIONS CONTEXT LOSS
```

**File Reading Order (MANDATORY):**
1. **Read** `AIOS_PROJECT_CONTEXT.md` - Master architecture and context
2. **Read** `README.md` - Current project status and quick start
3. **Read** `AI_context_reallocator.md` - This file (context preservation)
4. **Read** `docs/ARCHITECTURE.md` - System architecture details
5. **Read** `docs/DEVELOPMENT.md` - Development workflow and standards
6. **Read** `docs/API_REFERENCE.md` - Code interfaces and contracts
7. **Read** `docs/INSTALLATION.md` - Setup and configuration
8. **Read** `docs/CHANGELOG.md` - Version history and changes

**Codebase Scanning (MANDATORY):**
```bash
# Core C++ system
semantic_search("C++ core implementation")
list_dir("c:\dev\AIOS\core")
read_file("c:\dev\AIOS\core\CMakeLists.txt")

# Python AI modules
semantic_search("Python AI modules")
list_dir("c:\dev\AIOS\ai")
read_file("c:\dev\AIOS\ai\src\core\nlp\__init__.py")

# C# Interface
semantic_search("C# interface")
list_dir("c:\dev\AIOS\interface")

# Configuration and resources
list_dir("c:\dev\AIOS\config")
list_dir("c:\dev\AIOS\resources")
```

### **Step 2: System Health Validation**
```
🔍 VERIFY SYSTEM STATE BEFORE ANY DEVELOPMENT WORK
```

**Git Status Check:**
```bash
# Check repository state
run_in_terminal("git status")
run_in_terminal("git branch -a")  
run_in_terminal("git log --oneline -10")

# Check for uncommitted changes
get_changed_files()
```

**Build System Validation:**
```bash
# C++ Core Build Check
run_in_terminal("cd core/build && cmake --build . --config Debug")

# Python Environment Check  
run_in_terminal("cd ai && python -c \"import sys; sys.path.append('src'); from core.nlp import NLPManager; print('✅ Python AI modules OK')\"")

# Integration Test (MANDATORY)
run_in_terminal("python test_integration.py")
```

**Dependency Verification:**
```bash
# vcpkg packages
run_in_terminal("C:\\dev\\vcpkg\\vcpkg list")

# Python packages
run_in_terminal("cd ai && pip list")

# System tools
run_in_terminal("cmake --version")
run_in_terminal("python --version")
```

### **Step 3: Project State Documentation**
```
📊 UPDATE PROJECT STATUS AFTER SYSTEM HEALTH CHECK
```

**Current Implementation Status:**
- **C++ Core**: ✅ Fully functional with vcpkg dependencies (Boost, OpenCV, nlohmann-json)
- **Python AI**: ✅ All 5 modules working (NLP, Prediction, Automation, Learning, Integration)
- **C# UI**: ⚠️ Scaffolded but not implemented
- **Integration**: ✅ Tested and working
- **Documentation**: 🔄 Comprehensive system in place
- **Git Repository**: ⚠️ Not initialized (pending user decision)

**Critical File Locations:**
```
c:\dev\AIOS\
├── AIOS_PROJECT_CONTEXT.md      # Master architecture document
├── AI_context_reallocator.md    # This file - context preservation
├── README.md                    # Project overview and quick start
├── setup.ps1                    # Environment setup script
├── test_integration.py          # System health verification
├── core/                        # C++ implementation
│   ├── CMakeLists.txt          # Build configuration
│   ├── include/                # Header files
│   ├── src/                    # Source implementation
│   └── build/                  # Build output
├── ai/                         # Python AI modules
│   ├── requirements.txt        # Python dependencies
│   ├── src/core/               # AI module implementations
│   └── venv/                   # Python virtual environment
├── interface/                  # C# UI (scaffolded)
├── docs/                       # Comprehensive documentation
└── config/                     # Configuration files
```

**Known Issues & Warnings:**
- Python venv activation syntax varies by system
- C# projects created but not fully implemented
- vcpkg path may need adjustment on different systems
- Git repository not initialized (user decision pending)

## 🛠️ **TROUBLESHOOTING & CONTEXT RECOVERY**

### **When AI Loses Context**
```
🚨 EMERGENCY CONTEXT RECOVERY PROTOCOL
```

**Immediate Actions:**
1. **Stop all current work**
2. **Execute bootstrap protocol from Step 1**
3. **Read user's last 5 messages for context**
4. **Check git log for recent changes**
5. **Run integration test to verify system state**

**Context Recovery Commands:**
```bash
# Quick system overview
semantic_search("AIOS project current state")
semantic_search("recent changes implementation")
semantic_search("user requirements")

# Check for user's specific requests
grep_search("TODO|FIXME|BUG", false)
grep_search("user|requirement|requested", false)
```

### **Common Recovery Scenarios**

**Scenario 1: "What were we working on?"**
```bash
# Check recent file changes
get_changed_files()

# Search for implementation patterns
semantic_search("recent implementation work")
semantic_search("development progress")
```

**Scenario 2: "The build is broken"**
```bash
# Check build errors
get_errors(["c:\dev\AIOS\core\CMakeLists.txt"])

# Verify dependencies
run_in_terminal("C:\\dev\\vcpkg\\vcpkg list")
run_in_terminal("cd core/build && cmake --build . --config Debug")
```

**Scenario 3: "Python modules not working"**
```bash
# Check Python environment
run_in_terminal("cd ai && python -c \"import sys; print(sys.path)\"")

# Verify AI modules
run_in_terminal("cd ai && python -c \"import sys; sys.path.append('src'); from core.nlp import NLPManager; print('OK')\"")
```

## � **DOCUMENTATION ORCHESTRATION**

### **Self-Updating Documentation System**
```
📋 DOCUMENTATION MUST BE KEPT CURRENT
```

**After Any Significant Change:**
1. **Update** `CHANGELOG.md` with changes
2. **Update** `README.md` if architecture changes
3. **Update** `API_REFERENCE.md` if interfaces change
4. **Update** `DEVELOPMENT.md` if workflow changes
5. **Update** this file with new context

**Documentation Validation:**
```bash
# Check all documentation exists
file_search("docs/*.md")

# Verify documentation is current
grep_search("TODO|FIXME|UPDATE", false, "docs/")
```

## 🔄 **ITERATION TRACKING & VERSION CONTROL**

### **Current Project Status: OS0.4 Branch**
- **Last Updated**: December 2024
- **Version**: 0.4.0-dev
- **Branch Strategy**: OS0.4 (new features), main (stable releases)
- **Git Status**: Repository not initialized (pending user decision)

### **Development Checkpoints**

**Checkpoint 1: Foundation Complete ✅**
- Project structure established
- C++ core with vcpkg dependencies
- Python AI modules implemented
- Build system working
- Integration tests passing

**Checkpoint 2: Documentation Complete ✅**
- Comprehensive README.md
- Full docs/ folder with all guides
- Self-orchestrating context system
- API documentation

**Checkpoint 3: Next Steps 🔄**
- Git repository initialization
- C# UI implementation
- Advanced AI features
- Production deployment

### **Command Templates for Quick Access**

**System Health Check:**
```bash
cd c:\dev\AIOS
python test_integration.py
```

**Full Rebuild:**
```bash
cd core/build
cmake --build . --config Debug --clean-first
cd ../..
python test_integration.py
```

**Context Refresh:**
```bash
# Read all documentation
semantic_search("AIOS project documentation")
semantic_search("implementation status")
semantic_search("user requirements")
```

## � **CONTEXT PRESERVATION PROTOCOL**

### **For AI Systems: Pre-Work Checklist**
```markdown
□ Read AI_context_reallocator.md (this file)
□ Read AIOS_PROJECT_CONTEXT.md 
□ Read README.md
□ Check git status
□ Run integration test
□ Verify system health
□ Update context tracking
```

### **For AI Systems: Memory Refresh Rules**
```markdown
REFRESH FULL CONTEXT WHEN:
- User mentions "forgetting" or "losing context"
- Every 3rd conversation turn
- Encountering unexpected errors
- Starting fresh after >24 hours
- Beginning any significant new feature
```

### **For AI Systems: Context Update Rules**
```markdown
UPDATE CONTEXT DOCUMENTATION WHEN:
- Major architecture changes
- New features implemented
- Build system modifications
- API changes
- User workflow changes
```

---

## 🎯 **FINAL INSTRUCTIONS**

**EVERY AI ITERATION MUST:**
1. **Execute bootstrap protocol first**
2. **Verify system health before coding**
3. **Update this file with changes**
4. **Maintain documentation currency**
5. **Preserve context for future iterations**

**NEVER:**
- Skip the bootstrap protocol
- Make assumptions about project state
- Ignore integration test failures
- Forget to update documentation
- Work without understanding current context

---

*This file was designed to be self-orchestrating and should be updated by every AI iteration working on AIOS. The goal is to eliminate context loss and ensure smooth project continuity.*
- When documentation seems out of sync
- When build/test failures occur

HOW TO REFRESH:
1. Re-read all files in docs/ folder
2. Run test_integration.py
3. Check git log for recent changes
4. Verify all major components still work
5. Update this file with current status
```

---

## 🎯 **DEVELOPMENT PRIORITIES**

### **Next Major Tasks** (Update as completed)
1. **Complete Documentation Suite** - Create all docs/ files
2. **C# UI Implementation** - Build actual WPF/WinUI interface
3. **Git Repository Setup** - Create OS0.4 branch on GitHub
4. **Advanced AI Features** - TensorFlow integration, advanced NLP
5. **Cross-Language API** - Robust C++/Python/C# communication

### **Ongoing Maintenance**
- Update documentation with every major change
- Keep integration tests passing
- Maintain this context file
- Update checkpoints regularly

---

## 🔧 **EMERGENCY CONTEXT RECOVERY**

### **If AI Has Lost Context Completely**
```markdown
EMERGENCY PROTOCOL:
1. Read AIOS_PROJECT_CONTEXT.md in full
2. Read this file (AI_context_reallocator.md) in full
3. Run: python test_integration.py
4. Check: git status and git log
5. Scan all files in docs/ folder
6. If errors occur, read core/CMakeLists.txt and ai/src/core/*/
7. If still lost, ask user for guidance

CRITICAL FILES TO UNDERSTAND:
- AIOS_PROJECT_CONTEXT.md (master architecture)
- test_integration.py (system health check)
- core/include/aios_core.hpp (C++ API)
- ai/src/core/*//__init__.py (Python AI modules)
```

### **Context Corruption Signs**
- Suggesting to recreate existing working components
- Not recognizing current project structure
- Forgetting about vcpkg or Python modules
- Trying to overwrite working code
- Not understanding multi-language integration

---

## 📝 **UPDATE PROTOCOL**

### **When to Update This File**
- Major architectural changes
- New components added
- Build system changes
- Integration test changes
- Documentation structure changes

### **How to Update**
1. Add new checkpoints to "Iteration Memory Checkpoints"
2. Update "Current Project Status"
3. Modify "Next Major Tasks" list
4. Add new emergency recovery steps if needed
5. Update the "Last Updated" timestamp

---

## 🚨 **CRITICAL WARNINGS**

### **DO NOT**
- Recreate existing working components
- Overwrite functional code without backup
- Ignore integration test failures
- Forget to update documentation
- Push to Git without branch verification

### **ALWAYS**
- Read this file before starting work
- Run integration tests before claiming success
- Update documentation with changes
- Maintain multi-language compatibility
- Preserve existing working functionality

---

**Last Updated**: July 7, 2025  
**System Status**: C++ Core ✅, Python AI ✅, Integration ✅  
**Next Priority**: Complete documentation suite and C# UI implementation

*This file is the memory anchor for AIOS development. Keep it current and comprehensive.*

---

## 🎯 **AUTOMATED CONTEXT HEALTH MONITORING**

### **🤖 SMART HEALTH ASSESSMENT SYSTEM**

**Health Monitor Script**: `scripts/context_health_monitor.py`
```bash
# Quick health check
python scripts/context_health_monitor.py

# JSON output for programmatic use
python scripts/context_health_monitor.py --json
```

**Health Scoring System**:
- **Documentation**: 25% weight (completeness, consistency)
- **Build System**: 25% weight (dependencies, compilation)
- **Code Integrity**: 25% weight (modules, structure)
- **Integration**: 25% weight (tests, functionality)

**Automated Triggers**:
```python
if health_score < 0.7:
    trigger_immediate_reingestion()
elif iterations >= adaptive_threshold:
    trigger_scheduled_reingestion()
```
