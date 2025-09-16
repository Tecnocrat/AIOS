# AI Quick Reference - AIOS Project

##  **IMMEDIATE ACTIONS FOR NEW AI CHAT SESSION**

### **1. Bootstrap Protocol (MANDATORY)**
```bash
# Read context files in order
read_file("c:\dev\AIOS\docs\ai-context\AI_context_reallocator.md")
read_file("c:\dev\AIOS\AIOS_PROJECT_CONTEXT.md")
read_file("c:\dev\AIOS\README.md")
read_file("c:\dev\AIOS\docs\ai-context\PROJECT_STATUS.md")
```

### **2. System Health Check (MANDATORY)**
```bash
# Run integration test
run_in_terminal("cd c:\dev\AIOS && python test_integration.py")

# Check git status
run_in_terminal("cd c:\dev\AIOS && git status")

# Verify build
run_in_terminal("cd c:\dev\AIOS\core\build && cmake --build . --config Debug")
```

### **3. Context Validation (MANDATORY)**
```bash
# Check recent changes
get_changed_files()

# Search for current work
semantic_search("AIOS current implementation")
semantic_search("user requirements")
```

##  **CRITICAL FILES TO UNDERSTAND**

| File | Purpose | When to Read |
|------|---------|--------------|
| `AI_context_reallocator.md` | Context preservation protocol | **ALWAYS FIRST** |
| `AIOS_PROJECT_CONTEXT.md` | Master architecture document | Every session |
| `README.md` | Project overview and quick start | Every session |
| `PROJECT_STATUS.md` | Current implementation status | Every session |
| `docs/ARCHITECTURE.md` | System design details | When working on architecture |
| `docs/DEVELOPMENT.md` | Development workflow | When coding |
| `test_integration.py` | System health verification | Before any work |

##  **COMMON COMMANDS**

### **System Health**
```bash
# Quick health check
cd c:\dev\AIOS && python test_integration.py

# Full rebuild
cd core/build && cmake --build . --config Debug --clean-first

# Python module check
cd ai && python -c "import sys; sys.path.append('src'); from core.nlp import NLPManager; print('OK')"
```

### **Context Recovery**
```bash
# Find recent work
semantic_search("recent implementation")
semantic_search("user requested")

# Check file changes
get_changed_files()

# Find errors
grep_search("TODO|FIXME|BUG", false)
```

### **Documentation Updates**
```bash
# Check docs are current
grep_search("TODO|UPDATE", false, "docs/")

# Validate all docs exist
file_search("docs/*.md")
```

##  **EMERGENCY PROCEDURES**

### **When Context is Lost**
1. **STOP** all current work
2. **READ** `AI_context_reallocator.md` completely
3. **EXECUTE** bootstrap protocol
4. **VERIFY** system health
5. **ASK** user for clarification if needed

### **When Build is Broken**
1. **CHECK** integration test output
2. **VERIFY** vcpkg dependencies
3. **REBUILD** from clean state
4. **CHECK** Python environment

### **When Confused About Requirements**
1. **SEARCH** for user requirements in conversation
2. **READ** PROJECT_STATUS.md for current state
3. **ASK** user for clarification
4. **NEVER** make assumptions

##  **PROJECT STATE QUICK REFERENCE**

### **What's Working **
- C++ core with vcpkg dependencies
- Python AI modules (all 5 modules)
- Build system (CMake + vcpkg)
- Integration tests
- Documentation system

### **What's Not Done **
- C# UI implementation
- Git repository initialization
- Advanced AI features

### **Critical Paths**
- `c:\dev\AIOS\` - Project root
- `c:\dev\vcpkg\` - C++ dependencies
- `core/build/` - C++ build output
- `ai/venv/` - Python environment

##  **ITERATION RULES**

### **Every 3rd Turn**
- Execute full bootstrap protocol
- Read all context files
- Verify system health

### **Every Session Start**
- Read AI_context_reallocator.md
- Check PROJECT_STATUS.md
- Run integration test

### **Before Any Coding**
- Understand current state
- Verify system health
- Check user requirements

### **After Any Changes**
- Update PROJECT_STATUS.md
- Run integration test
- Update documentation

---

##  **SUCCESS CRITERIA**

### **You're Ready to Work When:**
-  Bootstrap protocol executed
-  System health verified
-  Context fully understood
-  User requirements clear

### **You Should Stop and Ask When:**
-  Context is unclear
-  System health failing
-  User requirements ambiguous
-  Integration tests failing

---

##  **ADAPTIVE CONTEXT HEALTH SYSTEM**

### **Smart Reingestion Algorithm**
```javascript
// Adaptive frequency instead of fixed 3 iterations
baseIterations = randomBetween(6, 9)
contextHealth = calculateContextHealth()

if (contextHealth < 0.7 || userMentionsConfusion) {
    executeBootstrapProtocol()
} else if (currentIteration >= baseIterations) {
    executeBootstrapProtocol()
    baseIterations = randomBetween(6, 9)
}
```

### **Context Health Indicators**
- 🟢 **Healthy (0.8-1.0)**: Tests pass, user satisfied, no errors
- 🟡 **Degraded (0.5-0.7)**: Minor issues, user asking questions
-  **Critical (0.0-0.4)**: Tests failing, user confused, build errors

### **Trigger Phrases for Immediate Reingestion**
- User says: "What were we doing?", "I'm confused", "This isn't working"
- System errors: Build failures, import errors, file not found
- Test failures: Integration test not passing
- Time elapsed: >48 hours since last context refresh

---

*This quick reference is designed to prevent context loss and ensure efficient AI iterations on the AIOS project.*
