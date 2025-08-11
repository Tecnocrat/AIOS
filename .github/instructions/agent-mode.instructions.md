
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

**This policy must be read and applied by the agent before any file creation or output.**