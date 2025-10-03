# AIOS Engineering Tenets (Kernel‑grade)

Purpose: Converge on clear, explicit, low-footgun engineering practices inspired by kernel-level review rigor. These tenets apply across AIOS languages (C++/C#, Python, TypeScript) and especially to shared/generic surfaces.

## Core tenets
1) Prefer explicit code over clever helpers
- Express the operation directly at the call site when it’s trivial (bit ops, casts, bounds). Hide as little as possible.

2) Make semantics visible at the call site
- Names and types should encode roles (hi/lo, src/dst). Avoid ambiguous parameters like a, b for asymmetric ops.

3) Don’t generalize the uncommon
- Local, rare transforms don’t deserve generic APIs. Avoid indirection that increases cognitive load without real reuse.

4) Keep generic surfaces minimal
- Do not pollute generic headers/modules with niche helpers. Scope to the tightest owner (arch/subsystem/folder) first.

5) Be explicit about width and endianness
- Casts and shifts should be visible. Prefer names that encode endianness and bit width when relevant.

6) Optimize for maintainability over terseness
- Readability > line count. One more obvious line beats a magic helper.

7) Make wrong code hard to write
- Use types, naming, and structures that prevent swap/mix-ups. Example: struct with named fields over two positional ints.

8) Respect process and timing
- Late windows (merge/release) are not for new cross-cutting helpers or refactors. Favor stability and clear diffs.

9) Localize change
- Prefer arch/subsystem-local solutions. Don’t widen blast radius unless broadly justified.

10) One good call site > a bad abstraction
- If only a couple of places need it, write it clearly those times.

## PR review checklist (apply to all languages)
- [ ] Helper/APIs: Is a helper truly broadly reusable? Would explicit code be clearer?
- [ ] Call-site clarity: Are roles obvious (e.g., hi, lo) without opening the helper?
- [ ] Endianness/width: Are bit width and endianness explicit at the usage site?
- [ ] Scope: Is the file/module header the narrowest possible owner? Avoid generic/global placement.
- [ ] Naming: Do names prevent swap errors and ambiguity? No a,b for asymmetric ops.
- [ ] Timing: Is this appropriate for the current merge/release phase?
- [ ] Diff quality: Does the change reduce cognitive load and make the code easier to review?

## Implementation guidance in AIOS
- Documentation: This file is referenced by the master index and the project context. Treat it as a living standard.
- Health checks: The runtime intelligence health tool emits advisory findings for potential violations (ambiguous parameter patterns, risky bit tricks). Findings are non-fatal.
- Code examples: Prefer explicit composition at call sites, e.g. in Python: `val = (hi << 16) | lo` with typed/named variables; in C++: `uint32_t v = (uint32_t(hi) << 16) | uint32_t(lo);` scoped locally.
- Scope: If a helper remains, encode roles in the name (…_hi_lo) and keep it local to the subsystem. Document endianness in a one-line comment.

— End of Tenets —
