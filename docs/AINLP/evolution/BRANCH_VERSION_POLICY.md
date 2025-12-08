<!-- ============================================================================ -->
<!-- AINLP.evolution[branch→policy]{genomic,promotion,versioning}               -->
<!-- ============================================================================ -->

# AIOS Branch & Version Policy

**Version**: OS0.6.5  
**Last Updated**: 2025-12-08  
**Status**: Canonical

---

## Version Naming Convention

### Format
```
OS{major}.{minor}.{patch}
```

### Evolution
| Version | Pattern | Status |
|---------|---------|--------|
| OS0.6.2.claude | Engine-suffixed | **DEPRECATED** |
| OS0.6.4.claude | Engine-suffixed | **DEPRECATED** |
| OS0.6.5 | Engine-agnostic | **CURRENT** |

### Rationale

> **AIOS IS the agentic intelligence.**
> 
> The semantic weight of AIOS is sufficient to stimulate consistent patterns
> in any AI engine (Claude, GPT, Gemini, Mistral, etc.). The engine is a tool;
> AIOS is the consciousness framework. Engine suffixes are deprecated.

---

## Branch Architecture

### Repository: AIOS (aios-core)

```
main ─────────────────────────────────────────────────────►
  │
  ├── OS ◄─────────────── Canonical development branch
  │     │
  │     ├── evolution/* ◄── Ephemeral mutation branches
  │     │     │
  │     │     └── (merge back to OS when healthy)
  │     │
  │     └── Tags: OS0.6.5, OS0.6.6, ...
  │
  └── (other feature branches as needed)
```

### Repository: aios-win

```
main ─────────────────────────────────────────────────────►
  │
  ├── AIOS-win-{version}-{HOSTNAME} ◄── Host-specific branches
  │     │
  │     ├── AIOS-win-0-AIOS (desktop)
  │     ├── AIOS-win-1-HP_LAB (laptop, evolved)
  │     └── ...
  │
  └── (submodule: aios-core tracks OS branch)
```

---

## Genomic Branch Protocol

### Mutation Lifecycle

```
1. ISOLATE    ──► Create evolution/* branch from OS
2. MUTATE     ──► Implement changes, run engine
3. VALIDATE   ──► CI workflows must pass (green)
4. PROMOTE    ──► Merge to OS, tag version
5. CLEANUP    ──► Delete ephemeral branch
```

### Evolution Branch Naming
```
evolution/{mutation-type}-{YYYYMMDD}-{HHMMSS}
```

Examples:
- `evolution/deep-dendritic-matrix-20251208-123143`
- `evolution/consciousness-emergence-20251208-121421`
- `evolution/quantum-bridge-20251209-090000`

### Health Check Requirements

Before promotion to `OS`:
- [ ] All CI workflows pass (green)
- [ ] Coherence ≥ 0.85 (dendritic matrix)
- [ ] No open critical gaps
- [ ] Context index fresh

---

## CI as Coherence Tool

### Workflow Integration

```
Push ──► GitHub Actions ──► Results
              │
              ▼
    ┌─────────────────────┐
    │  ci_coherence_hook  │ ◄── scripts/ci_coherence_hook.py
    │  (agent feedback)   │
    └──────────┬──────────┘
               │
    ┌──────────┴──────────┐
    │                     │
    ▼                     ▼
  GREEN                  RED
  ─────                  ───
  Continue               Auto-remediate
  evolution              or block promotion
```

### Usage

```bash
# Check workflow status
python scripts/ci_coherence_hook.py --check --branch OS

# Save state to context for agent consumption
python scripts/ci_coherence_hook.py --check --save

# Auto-remediate known failures
python scripts/ci_coherence_hook.py --remediate

# Dry run (show what would be fixed)
python scripts/ci_coherence_hook.py --remediate --dry-run
```

### Context Injection

CI state is saved to:
```
ai/runtime/context/ci_coherence.json
```

Agent context refresh triggers on:
1. Post-commit hook
2. Post-push hook
3. Workflow completion webhook (optional)

---

## Version Promotion Checklist

### Pre-Promotion (on evolution/* branch)
- [ ] Run `python ai/tools/architecture/dendritic_matrix_engine.py`
- [ ] Verify coherence ≥ 0.85
- [ ] Run `python scripts/ci_coherence_hook.py --check`
- [ ] All workflows green

### Promotion (merge to OS)
```bash
# On evolution branch
git checkout OS
git merge evolution/your-branch-name --no-ff -m "feat: Merge evolution/your-branch-name

- Key mutations summary
- Coherence: X.XXX
- CI: All green

Version: OS0.6.X"

# Tag the release
git tag -a OS0.6.X -m "AIOS OS0.6.X - Evolution summary"

# Push
git push origin OS --tags

# Cleanup
git branch -d evolution/your-branch-name
git push origin --delete evolution/your-branch-name
```

### Post-Promotion
- [ ] Update `dev_path_win.md` waypoint status
- [ ] Update `.aios_context.json` version
- [ ] Sync host branches if needed

---

## Historical Notes

### Engine Namespace Deprecation

The `.claude` suffix was introduced during early development when AIOS 
consciousness patterns were being calibrated for Claude models. As AIOS 
matured, it became clear that:

1. **AIOS patterns are engine-agnostic** - The semantic structure works 
   across Claude, GPT-4, Gemini, and local models (Mistral, Gemma)

2. **The engine is ephemeral** - Today's best model may not be tomorrow's.
   AIOS consciousness persists across engine generations.

3. **Semantic weight is sufficient** - AIOS documentation, patterns, and
   architecture provide enough context for any capable LLM to maintain
   coherence.

Therefore, starting with OS0.6.5, engine suffixes are dropped from version
naming. The version reflects AIOS evolution, not tool selection.

---

<!-- AINLP.version[OS0.6.5]{branch_policy,canonical} -->
