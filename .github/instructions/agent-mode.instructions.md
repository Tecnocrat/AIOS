
# AIOS Agentic File Creation Policy (Tachyonic Rule Set)

**For all VSCode chat agents and automated file operations:**

1. **No New Files at Project Root**
	- Never create new files directly in the project root.
	- Always analyze the existing file tree and project structure first.

2. **Reuse and Inject**
	- Before proposing a new file, check if the logic or data can be injected into an existing, thematically appropriate file (e.g., docs, config, changelog, or module-specific files).

3. **Optimal Placement**
	- If no suitable file exists, determine the optimal location by:
	  - Considering the file’s purpose, scope, and related modules.
	  - Preferring subfolders (e.g., docs/, scripts/legacy/, runtime_intelligence/, or module-specific folders) over the root.

4. **Self-Interrogation Before Output**
	- Before outputting a file creation or patch, the agent must:
	  - Ask: “Can this logic be injected into an existing file?”
	  - If not, “What is the most logical, non-root location for this file, given the project’s architecture and conventions?”

5. **Documentation and Traceability**
	- When deprecating, moving, or harmonizing files, always document the change in an existing, relevant documentation or changelog file—never by creating a new root-level file.



---

## AINLP Harmonizer — Context-Coherence Protocol (Precision Upgrade)

Purpose: Maintain precision when focus shifts cause context drift. Before impactful edits, self-assess perceived context coherence for the focus file and rebalance with targeted discovery.

### Coherence Types
- Local File Coherence (LFC): How well the agent understands the current file (recent work, symbols, patterns).
- Global Project Coherence (GPC): How well the change aligns with adjacent modules, contracts, docs, tests, and conventions.

### Fast Signals (lightweight heuristics)
- LFC high, GPC low indicators:
	- Many edits to one file without checking usages/definitions elsewhere.
	- Few or no searches for symbol usages across the workspace.
	- Divergence from known paths/conventions (e.g., tests not under `ai/tests/`).
- LFC low indicators:
	- First edit on a file in this session; unknown conventions; missing owner/tests context.
	- Symbols unclear; imports/headers not recognized; no recent reads around definitions.

### Coherence Score (quick rubric)
- Start at 0.5. Add +0.2 if you’ve read definitions/usages of key symbols; +0.2 if you opened module README/spec/tests; +0.1 if you checked changelog/AIOS.Harmonizer AINL.
- Subtract -0.3 if you’ve only touched one file for >3 edits without a workspace search; -0.2 if public API change without usage scan; -0.1 if path conventions may be violated.
- Thresholds: <0.4 → do discovery before editing. 0.4–0.7 → cautious edit with checks. >0.7 → proceed.

### Discovery Steps (choose minimal set based on signals)
1) Symbols perimeter
	 - Search usages/definitions for changed symbols (functions/classes/constants) across the workspace.
	 - Check interfaces and public contracts (headers, interfaces/, include/, AIOS.Models, etc.).
2) Module context
	 - Open nearby README/spec in the module; read top section and any contracts.
	 - Open relevant tests (prefer `ai/tests/`) and see expected behavior.
3) Governance context
	 - Check `docs/tachyonic/tachyonic_changelog.*` for moves/path updates.
	 - Review `docs/tachyonic/AIOS.Harmonizer.AINL.md` checklist to confirm placement/observability.
4) Pathing and observability
	 - Verify outputs under `runtime_intelligence/logs/*` when generating artifacts.
	 - Ensure `.gitignore` allows discovery for `.json`, `.db`, `.log` under RI logs.

### Edit Gates (apply before commit-worthy edits)
- If changing public APIs or paths:
	- Run workspace usage scan; list at least 1–3 impacted call sites.
	- Update or add minimal tests/docs when behavior changes.
- If moving/creating files:
	- Reuse/inject if possible. Else place under module-appropriate folders; never root.
	- Append a changelog entry (`docs/tachyonic/tachyonic_changelog.(yaml|json)`).

### Tooling Guidance (fast + precise)
- Use a small number of targeted operations:
	- Workspace grep/semantic search for symbols and paths.
	- Read larger chunks around definitions (150–300 lines) instead of many tiny reads.
	- Open tests under `ai/tests/` and module READMEs/specs.
	- Run a fast test or harness to validate changed surfaces.

	#### PowerShell Advanced (Agent Assist)
	Use PowerShell one-liners instead of creating transient helper scripts when:
		- Enumerating root clutter candidates:
			`Get-ChildItem -LiteralPath . -File -Filter 'test_*.py' | Select Name,Length`
		- Verifying absence after cleanup:
			`(Test-Path .\test_chatgpt_integration.py) -eq $false`
		- Counting lattice JSON export size (for observability budgets):
			`Get-Item runtime_intelligence\logs\aios_context\*.json | Measure-Object Length -Sum`
		- Grep-like symbol perimeter using Select-String:
			`Select-String -Path 'core\\**\\*.hpp','core\\**\\*.cpp' -Pattern 'BMSSPResult'`
		- Safety dry-run delete (preview):
			`Get-ChildItem -Filter 'test_chatgpt_integration.py' | ForEach-Object { 'DELETE -> ' + $_.FullName }`
	Only perform actual deletions after changelog entry & test confirmation, and favor `Remove-Item -WhatIf` first.

### When to Re-center
- After 3–5 edits in one file without a usage scan, pause for a perimeter search.
- When touching files not seen this session, run the minimal discovery (README/spec + tests + symbol scan).

Reference: See AIOS.Harmonizer AINL checklist at `docs/tachyonic/AIOS.Harmonizer.AINL.md` for the end-to-end harmonized flow.

**This policy must be read and applied by the agent before any file creation or output.**