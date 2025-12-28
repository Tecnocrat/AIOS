# Relocation Marker - scripts/

**Original Location**: `c:\dev\AIOS\scripts\` (root level)
**New Location**: `c:\dev\AIOS\runtime_intelligence\tools\scripts\` (runtime intelligence tools)
**Relocation Date**: October 4, 2025
**AINLP Compliance**: Enhancement Over Creation

## Reason for Relocation

**Architectural Decoherence**: Utility scripts scattered at root level
**Optimal Location**: `runtime_intelligence/tools/` supercell - operational tooling
**AINLP Principle**: Proper Output Management - utility scripts belong in runtime tools

## Files Relocated

1. `dev_terminal.ps1` - Development terminal setup script
2. `root_clutter_guard.ps1` - Root directory cleanup guard script

**Total**: 2 PowerShell utility scripts

## Script Functionality

**dev_terminal.ps1**:
- Purpose: Initialize development terminal environment
- Usage: PowerShell terminal setup for AIOS development

**root_clutter_guard.ps1**:
- Purpose: Monitor and prevent root directory clutter
- Usage: Automated cleanup and organization enforcement

## References Updated

- `docs/development/AIOS_DEV_PATH.md` - Script references updated
- `.githooks/` - Any hook references to scripts updated (if present)

## Integration Status

✅ Files relocated
✅ References updated
✅ Architectural coherence restored
✅ AINLP compliance maintained

## Access Instructions

**Previous Access**:
```powershell
.\scripts\dev_terminal.ps1
.\scripts\root_clutter_guard.ps1
```

**New Access**:
```powershell
.\runtime_intelligence\tools\scripts\dev_terminal.ps1
.\runtime_intelligence\tools\scripts\root_clutter_guard.ps1
```

## Integration with Runtime Intelligence

Scripts now part of unified runtime intelligence tooling:
- `runtime_intelligence/tools/` - Python tools
- `runtime_intelligence/tools/scripts/` - PowerShell/Bash scripts
- `runtime_intelligence/tools/general/` - General utilities

---

*This relocation enhances AIOS architectural coherence by consolidating utility scripts in the canonical runtime_intelligence/tools/ supercell location.*
