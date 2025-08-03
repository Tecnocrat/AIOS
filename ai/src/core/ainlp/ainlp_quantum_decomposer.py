#!/usr/bin/env python3
"""
AINLP Quantum Line Decomposition Engine
Automated E501 compliance through fractal code patterns
AINLP.quantum [line_decomposition] (comment.AINLP.class)
"""

import re

from ai.src.core.ainlp.utils import get_logger

logger = get_logger(__name__)


def apply_quantum_line_decomposition(filename):
    """Apply AINLP quantum decomposition to fix E501 violations"""
    logger.info("🧠 AINLP Quantum Line Decomposition Engine")
    logger.info("🔧 Applying fractal code patterns for E501 compliance")
    logger.info("=" * 60)

    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Track changes
    changes_made = 0
    fixed_lines = []

    for i, line in enumerate(lines):
        original_line = line.rstrip()

        if len(original_line) > 79:
            logger.debug(
                "📏 Line %d: %d chars -> Decomposing",
                i + 1,
                len(original_line),
            )
            changes_made += 1

            # Apply AINLP quantum decomposition
            decomposed_lines = decompose_line(original_line, i + 1)
            fixed_lines.extend(decomposed_lines)
        else:
            fixed_lines.append(line)

    # Write back the fixed content
    with open(filename, "w", encoding="utf-8") as f:
        f.writelines(fixed_lines)

    logger.info("✅ AINLP Decomposition Complete: %d lines fixed", changes_made)
    return changes_made


# AINLP.mind: decompose_line now leverages line_num for context-aware decomposition,
#   advanced logging, and future AINLP/AIOS integration. Each line is treated as an
#   atomic reasoning kernel (ark), enabling traceable, auditable, and extensible
#   quantum decomposition for E501 and beyond.
def decompose_line(line, line_num):
    """Apply fractal decomposition patterns to a long line, with line_num for context-aware logic."""
    indent = len(line) - len(line.lstrip())
    base_indent = " " * indent
    decomposition_ark = {
        "line_num": line_num,
        "original": line,
        "decomposed": None,
        "pattern": None,
    }

    # Pattern 1: Assignment with conditional
    if " = " in line and " if " in line and " else " in line:
        parts = line.split(" = ", 1)
        if len(parts) == 2:
            var_name = parts[0]
            expression = parts[1]
            decomposition_ark["decomposed"] = [
                f"{var_name} = (\n",
                f"{base_indent}    {expression}\n",
                f"{base_indent})\n",
            ]
            decomposition_ark["pattern"] = "assignment_conditional"
            logger.info(
                "[ARK] Decomposed assignment with conditional at line %d: %s",
                line_num,
                var_name,
            )
            return decomposition_ark["decomposed"]

    # Pattern 2: Print statements with f-strings
    if line.strip().startswith('print(f"') and line.count('"') >= 2:
        match = re.match(r'(\s*)print\(f"([^"]+)"\)', line)
        if match:
            indent_str, content = match.groups()
            decomposition_ark["decomposed"] = [
                f"{indent_str}print(\n",
                f'{indent_str}    f"{content}"\n',
                f"{indent_str})\n",
            ]
            decomposition_ark["pattern"] = "print_fstring"
            logger.info("[ARK] Decomposed f-string print at line %d.", line_num)
            return decomposition_ark["decomposed"]

    # Pattern 3: Regular print statements
    if line.strip().startswith("print(") and not line.strip().startswith("print(f"):
        match = re.match(r"(\s*)print\((.+)\)", line)
        if match:
            indent_str, content = match.groups()
            if content.startswith('"') and content.endswith('"'):
                content = content[1:-1]
                decomposition_ark["decomposed"] = [
                    f"{indent_str}print(\n",
                    f'{indent_str}    "{content}"\n',
                    f"{indent_str})\n",
                ]
                decomposition_ark["pattern"] = "print_regular"
                logger.info("[ARK] Decomposed regular print at line %d.", line_num)
                return decomposition_ark["decomposed"]

    # Pattern 4: Dictionary assignments
    if ": (" in line and ")," in line:
        indent_str = " " * indent
        key_match = re.match(r'(\s*)"([^"]+)": \((.+)\),?', line)
        if key_match:
            spaces, key, value = key_match.groups()
            comma = "," if line.rstrip().endswith(",") else ""
            decomposition_ark["decomposed"] = [
                f'{spaces}"{key}": (\n',
                f"{spaces}    {value}\n",
                f"{spaces}){comma}\n",
            ]
            decomposition_ark["pattern"] = "dict_assignment"
            logger.info(
                "[ARK] Decomposed dict assignment at line %d: %s", line_num, key
            )
            return decomposition_ark["decomposed"]

    # Pattern 5: Function calls with long parameters
    if ".get(" in line and len(line) > 79:
        parts = line.split(".get(", 1)
        if len(parts) == 2:
            before_get = parts[0]
            after_get = parts[1]
            decomposition_ark["decomposed"] = [
                f"{before_get}.get(\n",
                f"{base_indent}    {after_get}\n",
            ]
            decomposition_ark["pattern"] = "function_get"
            logger.info("[ARK] Decomposed function .get at line %d.", line_num)
            return decomposition_ark["decomposed"]

    # Pattern 6: List assignments
    if ": [" in line and "]," in line:
        match = re.match(r'(\s*)"([^"]+)": \[(.+)\],?', line)
        if match:
            spaces, key, values = match.groups()
            comma = "," if line.rstrip().endswith(",") else ""
            decomposition_ark["decomposed"] = [
                f'{spaces}"{key}": [\n',
                f"{spaces}    {values}\n",
                f"{spaces}]{comma}\n",
            ]
            decomposition_ark["pattern"] = "list_assignment"
            logger.info(
                "[ARK] Decomposed list assignment at line %d: %s", line_num, key
            )
            return decomposition_ark["decomposed"]

    # Default: Simple break at natural points
    if len(line) > 79:
        for break_char in [", ", " + ", " and ", " or "]:
            if break_char in line:
                parts = line.split(break_char, 1)
                if len(parts) == 2 and len(parts[0]) < 75:
                    decomposition_ark["decomposed"] = [
                        f"{parts[0]}{break_char[0]}\n",
                        f"{base_indent}    {break_char[1:]}{parts[1]}\n",
                    ]
                    decomposition_ark["pattern"] = f"break_{break_char.strip()}"
                    logger.info(
                        "[ARK] Decomposed line at %d using break char '%s'.",
                        line_num,
                        break_char.strip(),
                    )
                    return decomposition_ark["decomposed"]

    # If no pattern matches, return original
    decomposition_ark["decomposed"] = [line]
    decomposition_ark["pattern"] = "none"
    logger.info("[ARK] No decomposition applied at line %d.", line_num)
    return decomposition_ark["decomposed"]


if __name__ == "__main__":
    apply_quantum_line_decomposition("test_compression_integration.py")
