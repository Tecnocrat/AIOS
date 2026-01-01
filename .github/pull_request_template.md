# AIOS Pull Request Template

Use this checklist to align with AIOS Engineering Tenets (kernel‑grade).

## Summary
- What does this change do? Why now?
- Scope of impact (local/subsystem/global)?

## Governance
- Commit message prefix valid? (feat|fix|docs|chore|refactor|test|build|ci|perf|revert|governance|cellular|ai|core|interface|runtime|security)
- Large deletion (>60% deleted lines) present? If yes, rationale tag included? ([rationale] / [cleanup] / [prune])
- Changelog required (paths in docs/, governance/, ai/env/)? Entry added?
- Hook policy rules_version changed? If yes, context capsule updated?

### Rationale Tags Table
| Tag | Purpose |
|-----|---------|
| [rationale] | Justifies broad structural or architectural deletions |
| [cleanup] | Non-functional removal of obsolete code / assets |
| [prune] | Targeted reduction (dead code, redundant modules) |

Add one tag in the commit message (after prefix) when large deletions trigger heuristic.

## Checklist
- [ ] Helper/APIs: Explicit call sites preferred over clever helpers unless reuse is broad
- [ ] Roles clear at call sites (hi/lo, src/dst). No ambiguous a,b for asymmetric ops
- [ ] Width/endianness explicit where relevant; casts and shifts visible
- [ ] Scope minimized: change lives in narrowest owner (arch/subsystem)
- [ ] Naming prevents misuse; wrong code is harder to write
- [ ] Timing appropriate (avoid late-window cross-cutting churn)
- [ ] Tests/docs updated; diffs easy to review

## Notes for reviewers
- Known tradeoffs, migration notes, deprecations
- Follow-up tasks (if any)
 - Governance diffs (policy, hooks, workflows) acknowledged
