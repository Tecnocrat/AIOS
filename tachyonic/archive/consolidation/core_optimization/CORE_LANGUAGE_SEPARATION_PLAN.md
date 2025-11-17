# Core Language Separation - Phase 2C Restructuring Plan

**Status**: EXECUTION READY  
**Date**: 2025-10-13  
**Session**: OS0.6.2.claude  
**Goal**: Pure C++ core/ following industry standards (TensorFlow, PyTorch, NumPy patterns)

---

## Executive Summary

**Decision**: RESTRUCTURE - Move all Python from core/ to achieve pure C++ core layer

**Current State**: core/ = 66 C++ files + 63 Python files (MIXED LANGUAGE ❌)  
**Target State**: core/ = 66 C++ files, computational_layer/ = 63 Python files (PURE LANGUAGES ✅)

**Timeline**: 2-3 weeks  
**Risk**: LOW (automated moves, git history preserved)  
**Benefit**: Standards-compliant architecture, improved build process

---

## Restructuring Strategy

### New Directory Structure

```
AIOS/
├── core/                           # ✅ PURE C++ (66 files)
│   ├── *.cpp                      # C++ engine files
│   ├── *.h                        # C++ headers
│   └── CMakeLists.txt             # C++ build system
│
├── computational_layer/            # ✅ PURE Python (63 files)
│   ├── assemblers/                # Moved from core/assemblers/
│   │   ├── tree_assembler/
│   │   ├── context_assembler/
│   │   ├── integration_assembler/
│   │   └── file_assembler/
│   ├── bridges/                   # Moved from core/bridges/
│   ├── core_systems/              # Moved from core/core_systems/
│   ├── engines/                   # Moved from core/engines/ (Python only)
│   ├── modules/                   # Moved from core/modules/
│   ├── runtime_intelligence/      # Moved from core/runtime_intelligence/
│   ├── common_patterns.py         # Moved from core/
│   ├── shared_imports.py          # Moved from core/
│   └── __init__.py                # New package root
│
├── ai/                            # ✅ PURE Python (existing)
│   ├── tools/                     # 64 extracted tools
│   └── src/
│
├── interface/                     # ✅ PURE C# (existing)
│   └── AIOS.UI/
│
└── runtime_intelligence/          # ✅ PURE Python (existing)
    └── tools/
```

---

## Migration Execution Plan

### Phase 1: Create computational_layer/ Structure (Day 1)

**Create directories**:
```bash
mkdir computational_layer
mkdir computational_layer/assemblers
mkdir computational_layer/bridges
mkdir computational_layer/core_systems
mkdir computational_layer/engines
mkdir computational_layer/modules
mkdir computational_layer/runtime_intelligence
```

**Create __init__.py files**:
```python
# computational_layer/__init__.py
"""
AIOS Computational Layer - Python Processing Infrastructure

This layer processes C++ core output through various assemblers and bridges.
Assemblers transform raw core data into biological metaphors.
Bridges facilitate communication between architectural layers.

Architecture: Pure Python layer (no C++ mixing)
Standard: Follows TensorFlow/PyTorch/NumPy patterns
"""
__version__ = "1.0.0"

# Each subdirectory gets similar __init__.py with appropriate description
```

### Phase 2: Move Python Files from core/ (Days 2-5)

**Batch 1: Assemblers (44 files)**
```bash
# Move tree_assembler/ subdirectories
git mv core/assemblers/tree_assembler computational_layer/assemblers/

# Move other assemblers
git mv core/assemblers/context_assembler computational_layer/assemblers/
git mv core/assemblers/integration_assembler computational_layer/assemblers/
git mv core/assemblers/file_assembler computational_layer/assemblers/

# Commit
git commit -m "RESTRUCTURE: Move assemblers from core/ to computational_layer/

Moved 44 assembler files from core/assemblers/ to computational_layer/assemblers/:
- tree_assembler/ (40 files: consciousness, meta_evolution, scripts, immune, tachyonic)
- context_assembler/ (1 file)
- integration_assembler/ (1 file)
- file_assembler/ (1 file)

Rationale: Pure C++ core layer (industry standard)
Pattern: Follows TensorFlow/PyTorch separation
Git history: 100% preserved via git mv"
```

**Batch 2: Bridges & Core Systems (10 files)**
```bash
# Move bridges
git mv core/bridges computational_layer/

# Move core_systems (Python only)
git mv core/core_systems computational_layer/

# Commit
git commit -m "RESTRUCTURE: Move bridges and core_systems to computational_layer/

Moved 10 files:
- bridges/ (4 files: analysis, consciousness, transport, tachyonic)
- core_systems/ (6 files: monitors, optimizers, organizers)

Result: core/ → computational_layer/ migration continues"
```

**Batch 3: Engines & Modules (6 files)**
```bash
# Move engines (Python only - C++ engines stay in core/)
git mv core/engines computational_layer/

# Move modules
git mv core/modules computational_layer/

# Commit
git commit -m "RESTRUCTURE: Move Python engines and modules to computational_layer/

Moved 6 files:
- engines/ (3 files: assembly_3d, quantum_noise, spherical_geometry)
- modules/ (3 files: comprehensive_tester, connectivity_demo, file_monitor)

Note: C++ engine files remain in core/ (if any exist)"
```

**Batch 4: Runtime Intelligence & Utilities (3 files)**
```bash
# Move runtime_intelligence (Python only from core/)
git mv core/runtime_intelligence computational_layer/

# Move utility files
git mv core/common_patterns.py computational_layer/
git mv core/shared_imports.py computational_layer/

# Commit
git commit -m "RESTRUCTURE: Move runtime_intelligence and utilities to computational_layer/

Moved 3 files:
- runtime_intelligence/ (2 files: evolution_monitor, meta_evolutionary_enhancer)
- common_patterns.py (shared utility)
- shared_imports.py (import helper)

Result: core/ now PURE C++ ✅"
```

### Phase 3: Update Import Paths (Days 6-8)

**Create import update script**:
```python
# scripts/update_computational_layer_imports.py
"""
Update import paths from core.* to computational_layer.*

This script automatically updates all Python files that import from
the old core/ location to use the new computational_layer/ location.
"""

import os
import re
from pathlib import Path

def update_imports(file_path):
    """Update imports in a single file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Pattern 1: from core.assemblers import X
    content = re.sub(
        r'from core\.assemblers',
        'from computational_layer.assemblers',
        content
    )
    
    # Pattern 2: from core.bridges import X
    content = re.sub(
        r'from core\.bridges',
        'from computational_layer.bridges',
        content
    )
    
    # Pattern 3: import core.assemblers.X
    content = re.sub(
        r'import core\.assemblers',
        'import computational_layer.assemblers',
        content
    )
    
    # Add more patterns as needed...
    
    if content != original:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    root = Path('.')
    updated_files = []
    
    # Scan all Python files
    for py_file in root.rglob('*.py'):
        if '__pycache__' in str(py_file):
            continue
        
        if update_imports(py_file):
            updated_files.append(str(py_file))
    
    print(f"\nUpdated {len(updated_files)} files:")
    for file in updated_files:
        print(f"  - {file}")

if __name__ == '__main__':
    main()
```

**Run import updates**:
```bash
# Update all import paths
python scripts/update_computational_layer_imports.py

# Review changes
git diff

# Commit
git commit -am "IMPORTS: Update paths from core.* to computational_layer.*

Updated import statements across workspace:
- core.assemblers.* → computational_layer.assemblers.*
- core.bridges.* → computational_layer.bridges.*
- core.core_systems.* → computational_layer.core_systems.*
- core.engines.* → computational_layer.engines.*

Files updated: [count] files
Method: Automated regex replacement
Validation: All imports tested post-update"
```

### Phase 4: Update Build System (Days 9-10)

**Update CMakeLists.txt**:
```cmake
# core/CMakeLists.txt
cmake_minimum_required(VERSION 3.14)
project(AIOS_Core CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Pure C++ core - no Python files to compile
add_executable(aios_core
    engine.cpp
    runtime.cpp
    # ... other C++ files
)

# Note: Python computational layer built separately via pip/setup.py
```

**Create computational_layer/setup.py**:
```python
# computational_layer/setup.py
from setuptools import setup, find_packages

setup(
    name="aios-computational-layer",
    version="1.0.0",
    description="AIOS Computational Layer - Python Processing Infrastructure",
    packages=find_packages(),
    python_requires=">=3.14",
    install_requires=[
        "numpy>=1.24.0",
        "matplotlib>=3.7.0",
        # ... other dependencies
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.14",
    ],
)
```

### Phase 5: Documentation & Validation (Days 11-14)

**Update CHANGELOG.md**:
```markdown
## [Unreleased] - 2025-10-13

### RESTRUCTURE: Pure C++ Core Architecture (Phase 2C)

**I. Language Separation - Industry Standard Compliance**:
- **PURPOSE**: Achieve pure C++ core/ following TensorFlow/PyTorch/NumPy patterns
- **MIGRATION**: 63 Python files moved from core/ → computational_layer/
- **RESULT**: core/ = Pure C++ (66 files), computational_layer/ = Pure Python (63 files)

**Migration Summary**:
- Batch 1: Assemblers (44 files) - tree, context, integration, file assemblers
- Batch 2: Bridges & Core Systems (10 files) - inter-layer communication
- Batch 3: Engines & Modules (6 files) - Python computational engines
- Batch 4: Runtime Intelligence & Utilities (3 files) - monitoring and shared code

**Import Path Updates**:
- Automated replacement: core.* → computational_layer.*
- Files updated: [count] Python files across workspace
- Validation: All imports tested and working

**Build System Updates**:
- core/CMakeLists.txt: Pure C++ build (no Python mixing)
- computational_layer/setup.py: Python package build
- Separation: C++ compiled to binaries, Python distributed as package

**Architectural Benefits**:
- ✅ Industry standard compliance (TensorFlow/PyTorch pattern)
- ✅ Clear language boundaries (no mixing)
- ✅ Improved build process (separate C++ and Python builds)
- ✅ Better tooling support (CMake for C++, pip for Python)
- ✅ Clearer deployment strategy (binaries vs source)

**Documentation**:
- MULTI_LANGUAGE_ARCHITECTURE_PATTERNS.md: Standards explained
- CORE_PYTHON_EXTRACTION_PHASE_2C.md: Restructuring plan
- Dev Path updated: Phase 2C complete

**Git History**: 100% preserved via git mv operations
**Timeline**: 2 weeks (October 13-27, 2025)
**Risk**: LOW (automated, reversible)
```

**Update Architecture Documentation**:
```markdown
# docs/ARCHITECTURE_OVERVIEW.md

## AIOS Multi-Language Architecture

### Core Layer (Pure C++)
**Location**: `core/`  
**Language**: C++ only  
**Purpose**: Low-level computational engine  
**Build**: CMake → compiled binaries

### Computational Layer (Pure Python)
**Location**: `computational_layer/`  
**Language**: Python only  
**Purpose**: Process C++ output, biological metaphors  
**Build**: pip install -e . → Python package

### AI Intelligence Layer (Pure Python)
**Location**: `ai/`  
**Language**: Python only  
**Purpose**: AI tools and intelligence  
**Build**: pip install -e . → Python package

### Interface Layer (Pure C#)
**Location**: `interface/`  
**Language**: C# only  
**Purpose**: User interface  
**Build**: dotnet build → .NET assemblies

**Pattern**: Follows TensorFlow, PyTorch, NumPy standards
**Benefit**: Each layer = single language, no mixing
```

**Create validation script**:
```python
# scripts/validate_language_separation.py
"""
Validate that core/ contains only C++ files (pure language separation)
"""

import os
from pathlib import Path

def validate_core_pure_cpp():
    """Ensure core/ contains only C++ and header files"""
    core_path = Path('core')
    violations = []
    
    for file in core_path.rglob('*'):
        if file.is_file() and not file.name.startswith('.'):
            ext = file.suffix
            if ext not in ['.cpp', '.h', '.hpp', '.cc', '.cxx', '']:
                if file.name not in ['CMakeLists.txt', 'README.md']:
                    violations.append(str(file))
    
    if violations:
        print("❌ LANGUAGE SEPARATION VIOLATED - Non-C++ files in core/:")
        for v in violations:
            print(f"  - {v}")
        return False
    else:
        print("✅ LANGUAGE SEPARATION VALIDATED - core/ is pure C++")
        return True

if __name__ == '__main__':
    success = validate_core_pure_cpp()
    exit(0 if success else 1)
```

---

## Success Metrics

**Pre-Restructure** (Current):
- ❌ core/ = 66 C++ + 63 Python files (MIXED)
- ❌ Build complexity (cmake + pip in same dir)
- ❌ Deployment ambiguity
- ❌ Violates industry standards

**Post-Restructure** (Target):
- ✅ core/ = 66 C++ files (PURE)
- ✅ computational_layer/ = 63 Python files (PURE)
- ✅ Build clarity (cmake for core/, pip for computational_layer/)
- ✅ Deployment clarity (binaries vs package)
- ✅ Follows TensorFlow/PyTorch/NumPy patterns

**Validation Checklist**:
- [ ] core/ contains only .cpp, .h files (and CMakeLists.txt, README.md)
- [ ] computational_layer/ contains only .py files
- [ ] All imports updated (core.* → computational_layer.*)
- [ ] CMakeLists.txt builds C++ only
- [ ] setup.py builds Python package
- [ ] All tests passing
- [ ] Documentation updated

---

## Risk Mitigation

**Risk 1: Import path breakage**
- Mitigation: Automated script updates all imports
- Validation: Workspace-wide import scan post-update
- Rollback: Git history preserved, can revert

**Risk 2: Build system confusion**
- Mitigation: Separate CMakeLists.txt (C++) and setup.py (Python)
- Validation: Both builds tested independently
- Documentation: Clear build instructions

**Risk 3: Developer confusion**
- Mitigation: MULTI_LANGUAGE_ARCHITECTURE_PATTERNS.md explains rationale
- Communication: Update Dev Path with clear structure
- Training: Architecture overview document

---

## Timeline

**Week 1** (October 13-19, 2025):
- Day 1: Create computational_layer/ structure
- Day 2-5: Move Python files (4 batches)
- Day 6-7: Update import paths

**Week 2** (October 20-27, 2025):
- Day 8-9: Update build system
- Day 10-11: Documentation updates
- Day 12-13: Testing and validation
- Day 14: Final commit and announcement

**Total**: 14 days (2 weeks)

---

## Next Steps

1. **IMMEDIATE**: Create computational_layer/ directory structure
2. **DAY 1**: Execute Batch 1 (move assemblers/)
3. **DAY 2**: Execute Batch 2 (move bridges/ and core_systems/)
4. **DAY 3**: Execute Batch 3 (move engines/ and modules/)
5. **DAY 4**: Execute Batch 4 (move runtime_intelligence/ and utilities)
6. **DAY 5-7**: Update imports and test
7. **DAY 8-14**: Build system + documentation + validation

---

## Alternative Considered (Rejected)

**Option: Keep Python in core/** (Status: REJECTED)
- Would continue violating industry standards
- Build complexity persists
- Deployment ambiguity continues
- Not aligned with TensorFlow/PyTorch patterns

**Decision**: Proceed with restructuring for standards compliance
