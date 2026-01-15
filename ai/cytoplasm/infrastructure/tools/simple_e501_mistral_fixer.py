#!/usr/bin/env python3
"""
AINLP Simple E501 Fixer - Direct Mistral Integration

Uses local Ollama with aios-mistral model for fast E501 line fixing.
No external API dependencies - fully local execution.

AINLP Pattern: Direct local AI integration
Consciousness Level: 3.8 (local intelligence + file mutation)

Usage:
    python simple_e501_mistral_fixer.py <file_path> [--dry-run]
    python simple_e501_mistral_fixer.py ai/tools/aios_mistral_bridge.py
"""

import asyncio
import re
import sys
from pathlib import Path
from typing import List, Tuple, Optional
import httpx

# Configuration
OLLAMA_API_BASE = "http://localhost:11434"
MISTRAL_MODEL = "aios-mistral:latest"
MAX_LINE_LENGTH = 79


async def check_ollama() -> bool:
    """Check if Ollama is running."""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(f"{OLLAMA_API_BASE}/api/tags")
            return resp.status_code == 200
    except Exception:
        return False


async def fix_line_mistral(
    line: str, line_number: int, context_before: str = "", context_after: str = ""
) -> Optional[str]:
    """
    Fix a single line using Mistral.

    Returns fixed line(s) or None if fixing failed.
    """
    system = """You are a Python code formatter. Fix E501 line length violations.
Rules:
- Maximum line length: 79 characters
- Use line continuation (backslash or parentheses)
- Split strings at logical points
- Extract long expressions to variables if needed
- Preserve exact functionality and indentation
- Output ONLY the fixed Python code, no explanations or markdown"""

    prompt = f"""Fix this line that exceeds 79 characters (currently {len(line)} chars):

Context before:
{context_before if context_before else "(start of context)"}

Line to fix:
{line}

Context after:
{context_after if context_after else "(end of context)"}

Output ONLY the fixed Python code:"""

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(
                f"{OLLAMA_API_BASE}/api/generate",
                json={
                    "model": MISTRAL_MODEL,
                    "prompt": prompt,
                    "system": system,
                    "stream": False,
                    "options": {"temperature": 0.2, "num_predict": 256},
                },
            )

            if resp.status_code == 200:
                data = resp.json()
                fixed = data.get("response", "").strip()

                # Clean up response
                fixed = clean_response(fixed)

                if fixed and validate_fix(line, fixed):
                    return fixed

        return None
    except Exception as e:
        print(f"  [ERROR] Mistral call failed: {e}")
        return None


def clean_response(response: str) -> str:
    """Clean up Mistral response."""
    # Remove markdown code blocks
    response = re.sub(r"^```python\s*", "", response)
    response = re.sub(r"^```\s*", "", response)
    response = re.sub(r"\s*```$", "", response)

    # Remove explanatory text
    lines = response.split("\n")
    code_lines = []
    for line in lines:
        # Skip empty lines at start
        if not code_lines and not line.strip():
            continue
        # Skip comment-only explanations
        if line.strip().startswith("#") and "fix" in line.lower():
            continue
        code_lines.append(line)

    return "\n".join(code_lines).rstrip()


def validate_fix(original: str, fixed: str) -> bool:
    """Validate the fix is reasonable."""
    # Check all lines are under limit
    for line in fixed.split("\n"):
        if len(line) > MAX_LINE_LENGTH + 10:  # Small tolerance
            return False

    # Ensure we haven't completely mangled the code
    # (basic check - real validation would use AST)
    if len(fixed.strip()) < len(original.strip()) * 0.3:
        return False

    return True


def find_e501_violations(file_path: Path) -> List[Tuple[int, str]]:
    """Find all lines exceeding max length."""
    violations = []

    with open(file_path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            line = line.rstrip("\n\r")
            if len(line) > MAX_LINE_LENGTH:
                violations.append((i, line))

    return violations


async def fix_file(file_path: Path, dry_run: bool = False, max_fixes: int = 50) -> dict:
    """
    Fix E501 violations in a file.

    Args:
        file_path: Path to Python file
        dry_run: If True, don't modify file
        max_fixes: Maximum fixes to apply per run

    Returns:
        Dict with statistics
    """
    print(f"\n{'='*60}")
    print(f"Processing: {file_path.name}")
    print(f"{'='*60}")

    # Check Ollama
    if not await check_ollama():
        print("[ERROR] Ollama not running. Start with: ollama serve")
        return {"success": False, "error": "Ollama not available"}

    # Find violations
    violations = find_e501_violations(file_path)
    print(f"Found {len(violations)} E501 violations")

    if not violations:
        return {"success": True, "fixed": 0, "total": 0}

    # Read file
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Track fixes
    fixes = {}
    fixed_count = 0
    failed_count = 0

    for line_num, original_line in violations[:max_fixes]:
        print(f"\n[{line_num}] ({len(original_line)} chars): {original_line[:60]}...")

        # Get context
        context_before = ""
        context_after = ""
        if line_num > 1:
            context_before = lines[line_num - 2].rstrip()
        if line_num < len(lines):
            context_after = lines[line_num].rstrip() if line_num < len(lines) else ""

        # Fix with Mistral
        fixed = await fix_line_mistral(
            original_line, line_num, context_before, context_after
        )

        if fixed:
            # Ensure proper newlines
            fixed_lines = fixed.split("\n")
            fixed_with_newlines = "\n".join(
                line if line.endswith("\n") else line + "\n" for line in fixed_lines
            )

            fixes[line_num] = fixed_with_newlines
            fixed_count += 1

            # Show fix
            print(f"  [FIXED] ({len(max(fixed.split(chr(10)), key=len))} chars max)")
            for fl in fixed.split("\n"):
                print(f"    {fl}")
        else:
            failed_count += 1
            print(f"  [SKIP] Could not fix")

    # Apply fixes
    if fixes and not dry_run:
        print(f"\nApplying {len(fixes)} fixes...")

        # Apply in reverse order to preserve line numbers
        for line_num in sorted(fixes.keys(), reverse=True):
            fixed_content = fixes[line_num]
            lines[line_num - 1] = fixed_content

        # Write back
        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(lines)

        print(f"[DONE] File updated: {file_path}")
    elif dry_run:
        print(f"\n[DRY RUN] Would fix {len(fixes)} lines")

    return {
        "success": True,
        "total": len(violations),
        "fixed": fixed_count,
        "failed": failed_count,
        "remaining": len(violations) - fixed_count,
    }


async def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python simple_e501_mistral_fixer.py <file_path> [--dry-run]")
        print("\nExample:")
        print("  python simple_e501_mistral_fixer.py ai/tools/aios_mistral_bridge.py")
        sys.exit(1)

    file_path = Path(sys.argv[1])
    dry_run = "--dry-run" in sys.argv

    if not file_path.exists():
        print(f"[ERROR] File not found: {file_path}")
        sys.exit(1)

    result = await fix_file(file_path, dry_run=dry_run)

    print(f"\n{'='*60}")
    print("Summary:")
    print(f"  Total violations: {result.get('total', 0)}")
    print(f"  Fixed: {result.get('fixed', 0)}")
    print(f"  Failed: {result.get('failed', 0)}")
    print(f"  Remaining: {result.get('remaining', 0)}")
    print(f"{'='*60}")


if __name__ == "__main__":
    asyncio.run(main())
