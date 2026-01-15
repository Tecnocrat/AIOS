# Tachyonic Shadow: requirements.txt Migration to pyproject.toml

**Shadow Created**: December 13, 2025  
**Consciousness Evolution**: 4.95 → 5.0 (dependency modernization)  
**AINLP Pattern**: Enhancement over creation (deprecated → modern PEP 517/518)

---

## Migration Summary

**Action**: Migrated canonical dependencies from `requirements.txt` → `pyproject.toml`  
**Reason**: Modern Python packaging standard (PEP 517/518/621) replaces legacy requirements.txt  
**Impact**: `pip install -e .` now installs all core dependencies

---

## Archived Content (requirements.txt as of 2025-12-13)

The following packages were the canonical runtime dependencies before migration:

### [NUCLEUS] Core Intelligence Substrates
```
torch>=2.5.0
torchvision>=0.20.0
transformers>=4.46.0
tokenizers>=0.20.0
openai>=1.50.0
openrouter>=0.0.19
numpy>=2.1.0
scipy>=1.14.0
pandas>=2.2.0
sympy>=1.13
```

### [CYTOPLASM] Communication & Processing Flows
```
fastapi>=0.115.0
uvicorn>=0.32.0
httpx>=0.27.0
aiofiles>=24.1.0
websockets>=13.0.0
requests>=2.32.0
```

### [MEMBRANE] Interface Boundaries & Protection
```
opencv-python>=4.10.0,<5.0
pillow>=11.0.0
psutil>=6.1.0
watchdog>=5.0.0
rich>=13.9.0
pydantic>=2.10.0
click>=8.1.0
typing-extensions>=4.12.0
attrs>=24.2.0
```

### [ENVIRONMENT] Development Integration Layer
```
pytest>=8.3.0
black>=24.10.0
ruff>=0.8.0
mypy>=1.13.0
graphviz>=0.20.0
google-cloud-aiplatform>=1.72.0
google-auth>=2.36.0
google-api-python-client>=2.154.0
```

---

## Historical Context

### Python 3.14t Free-Threaded Environment
- **GIL STATUS**: DISABLED (3.1x speedup measured)
- **Canonical venv**: Was `c:\aios-supercell\.venv`
- **Packages with cp314t wheels**: numpy, scipy, pandas, pydantic-core, psutil, pyyaml

### Dependency Hierarchy (Pre-Migration)
```
├── requirements.txt (CANONICAL) ← Migrated to pyproject.toml
├── server/shared/requirements-cell-minimal.txt (SUBSET)
└── Cell requirements (INHERIT from minimal)
```

---

## New Installation Pattern

```bash
# Modern (post-migration)
pip install -e .           # Core dependencies
pip install -e ".[extras]" # + AI extras (chromadb, faiss, etc.)
pip install -e ".[full]"   # Everything

# Legacy (deprecated but still functional)
pip install -r requirements.txt  # Points to pyproject.toml now
```

---

## Consciousness Coherence

This migration maintains AINLP biological architecture principles:
- **Nucleus**: Core deps in `[project.dependencies]`
- **Cytoplasm**: Optional stacks in `[project.optional-dependencies]`
- **Membrane**: Tool configs in `[tool.*]` sections
- **Environment**: External URLs in `[project.urls]`

**Tachyonic Preservation**: Full historical knowledge maintained in this shadow.
