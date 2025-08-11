# AIOS.Harmonizer — Agentic Integration and Navigation Logic (AINL)

Purpose: A compact, repeatable checklist the agent follows for complex file moves, logic integration, and optimal placement within AIOS.

## Core checklist

1) Read the request and extract explicit and implicit requirements
- List each item as a checklist; keep it visible during the task

2) Gather context fast and in parallel
- Search workspace for symbols/paths; open relevant files in larger chunks
- Prefer semantic/code search before making assumptions

3) Determine optimal placement
- Reuse and inject into existing files where possible
- Avoid project root for new files; prefer module-appropriate folders
- Follow existing conventions (ai/tests, runtime_intelligence/logs, docs/tachyonic)

4) Implement minimal, precise changes
- Smallest set of edits; avoid unrelated reformatting
- Preserve public APIs; create directories with parents=True

5) Wire up observability
- Ensure outputs go under runtime_intelligence/logs/*
- Update .gitignore to include logs (*.json, *.db, *.log) for discovery

6) Record harmonization
- Append YAML+JSON entries under docs/tachyonic/tachyonic_changelog.*
- Include kind, file, old_path, new_path, date, reason, harmonization

7) Validate immediately
- Run a fast test or harness covering the change path
- Check that expected files are created in correct locations

8) Quality gates
- Build/lint/tests quick triage; report PASS/FAIL deltas
- Note any intentionally deferred warnings

9) Close the loop
- Summarize what changed and how it’s verified
- Propose small, safe next steps

## Notes
- This AINL file complements the policy in .github/instructions/agent-mode.instructions.md
- Keep the checklist evolutionary but stable; prefer additive updates.
