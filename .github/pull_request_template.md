# AIOS Pull Request Template

Use this checklist to align with AIOS Engineering Tenets (kernel‑grade).

## Summary
- What does this change do? Why now?
- Scope of impact (local/subsystem/global)?

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
