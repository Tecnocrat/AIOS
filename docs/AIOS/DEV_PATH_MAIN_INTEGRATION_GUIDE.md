# DEV PATH MAIN Integration Guide (2025-07-20)

## Executive Summary
This guide unifies the AIOS strategic roadmap, AINLP paradigms, and VSCode extension command usage to provide a clear, actionable path for developers working on the main development trajectory of AIOS. All recent refactorization, import logic upgrades, and context preservation strategies are now integrated.

---

## 1. DEV PATH MAIN Objectives & Milestones
- **Immediate Focus:** VSCode extension production integration (see `STRATEGIC_DEVELOPMENT_PATH_2025_2026.md`)
- **Key Milestones:**
  - Real AIOS communication bridge
  - Git branch and project type detection
  - Advanced context awareness and preservation
  - Professional developer experience optimization
  - Harmonized subsystem imports and canonical code locations
  - ✅ **COMPLETED:** AINLP dendritic consolidation of `aios_vscode_integration` module

---

## 1.1 AINLP Architecture Consolidation (2025-08-27)

### **Consolidated Module Structure**
The `aios_vscode_integration` module has been fully consolidated following AINLP dendritic paradigms:

```
🧠 AIOS VSCode Integration/
├── main.py                     # FastAPI app with consolidated middleware
├── models.py                   # Shared Pydantic models
├── services/                   # Shared service modules
│   ├── debug_manager.py       # Debug functionality (all endpoints)
│   └── fractal_cache_manager.py # Caching system (all endpoints)
└── endpoints/                  # Consolidated endpoint modules
    ├── ai_endpoints.py        # AI processing + intent handlers
    ├── development_endpoints.py # Code operations + architecture
    ├── system_endpoints.py    # System health + bridge communication
    └── ux_endpoints.py        # User experience + guidance
```

### **Consolidation Achievements**
- **File Reduction:** 8 endpoint files → 4 consolidated files (50% reduction)
- **Logic Densification:** Increased functional density while reducing complexity
- **Service Separation:** Shared services moved to dedicated `services/` directory
- **Import Optimization:** Clean relative imports with proper dependency management
- **AINLP Readiness:** Architecture designed for AI ingestion and evolution

### **Testing Validation**
- ✅ All modules import successfully
- ✅ FastAPI application initializes correctly
- ✅ All routers register without errors
- ✅ Service dependencies resolve properly
- ✅ Middleware functions execute successfully

---

## 2. AINLP Paradigm Integration
- **Comment-Driven Code Management:** Use AINLP comment classes for dynamic, environment-aware code (see `AINLP_SPECIFICATION.md`)
- **Fractal Logic & Context Preservation:** Micro-fractal sampling and memory class processing for robust context management
- **OP ITER Process:**
  - Analyze → Refactor → Optimize → Document
  - Use in all major code and documentation updates

---

## 3. VSCode Extension Command Usage
- **Core Commands:**
  - `/save` – Persist conversation and workspace context
  - `/load` – Restore saved context
  - `/reset` – Clear context for new tasks
  - `/refresh.context` – Trigger AINLP-based context harmonization
- **Best Practices:**
  - Save before major changes or session end
  - Use `/refresh.context` regularly for optimal context
  - Monitor status with `/status`

---

## 4. Cross-References
- [Strategic Roadmap](STRATEGIC_DEVELOPMENT_PATH_2025_2026.md)
- [AINLP Language Specification](../AINLP/AINLP_SPECIFICATION.md)
- [VSCode AINLP Commands](AIOS_VSCODE_AINLP_COMMANDS.md)
- [VSCode Save Command](AIOS_VSCODE_SAVE_COMMAND.md)

---

## 5. Integration Checklist
- [x] All developers use `/save` and `/refresh.context` as part of workflow
- [x] AINLP comment classes present in new/updated code
- [x] OP ITER process followed for major changes
- [x] Documentation cross-linked and up to date
- [x] Feedback loop established for continuous improvement

---

*This guide is a living document. Update as integration evolves and new best practices emerge.*
