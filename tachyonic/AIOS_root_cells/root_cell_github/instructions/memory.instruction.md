---
applyTo: '**'
---

# AIOS Agent Memory

preferences:
  code_style:
    - keep changes minimal
    - avoid reformatting unrelated code
  safety:
    - offline-first
    - do not exfiltrate secrets
    - PR-gated writes
  workflow:
    - use existing VS Code tasks when possible
    - checkpoint after 3–5 tool calls
  ui:
    - use shadcn/ui docs fetch before usage
