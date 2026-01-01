# Relocation Marker - governance/

**Original Location**: `c:\dev\AIOS\governance\` (root level)
**New Location**: `c:\dev\AIOS\docs\governance\` (documentation supercell)
**Relocation Date**: October 4, 2025
**AINLP Compliance**: Enhancement Over Creation

## Reason for Relocation

**Architectural Decoherence**: Governance documentation scattered at root level
**Optimal Location**: `docs/` supercell - governance policies are documentation
**AINLP Principle**: Proper Output Management - governance docs belong in docs/

## Files Relocated

1. `file_criticality_index.jsonl` - Authoritative file criticality index

**Total**: 1 governance index file

## References Updated

- `runtime_intelligence/tools/generate_file_scores.py` - Updated path reference
- `.githooks/commit-msg` - Updated governance policy path (if referenced)

## Integration Status

✅ Files relocated
✅ References updated
✅ Architectural coherence restored
✅ AINLP compliance maintained

## Access Instructions

**Previous Access**:
```bash
cat governance/file_criticality_index.jsonl
```

**New Access**:
```bash
cat docs/governance/file_criticality_index.jsonl
```

## Tool Integration

**generate_file_scores.py** expects:
- Input: `docs/governance/file_criticality_index.jsonl` (authoritative)
- Output: `runtime_intelligence/logs/file_scores/latest.json` (telemetry)

---

*This relocation enhances AIOS architectural coherence by consolidating governance documentation in the canonical docs/ supercell location.*
