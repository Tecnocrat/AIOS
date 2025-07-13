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
            logger.debug(f"📏 Line {i+1}: {len(original_line)} chars -> Decomposing")
            changes_made += 1

            # Apply AINLP quantum decomposition
            decomposed_lines = decompose_line(original_line, i + 1)
            fixed_lines.extend(decomposed_lines)
        else:
            fixed_lines.append(line)

    # Write back the fixed content
    with open(filename, "w", encoding="utf-8") as f:
        f.writelines(fixed_lines)

    logger.info(f"✅ AINLP Decomposition Complete: {changes_made} lines fixed")
    return changes_made


def decompose_line(line, line_num):
    """Apply fractal decomposition patterns to a long line"""
    indent = len(line) - len(line.lstrip())
    base_indent = " " * indent

    # Pattern 1: Assignment with conditional
    if " = " in line and " if " in line and " else " in line:
        parts = line.split(" = ", 1)
        if len(parts) == 2:
            var_name = parts[0]
            expression = parts[1]
            return [
                f"{var_name} = (\n",
                f"{base_indent}    {expression}\n",
                f"{base_indent})\n",
            ]

    # Pattern 2: Print statements with f-strings
    if line.strip().startswith('print(f"') and line.count('"') >= 2:
        match = re.match(r'(\s*)print\(f"([^"]+)"\)', line)
        if match:
            indent_str, content = match.groups()
            return [
                f"{indent_str}print(\n",
                f'{indent_str}    f"{content}"\n',
                f"{indent_str})\n",
            ]

    # Pattern 3: Regular print statements
    if line.strip().startswith("print(") and not line.strip().startswith("print(f"):
        match = re.match(r"(\s*)print\((.+)\)", line)
        if match:
            indent_str, content = match.groups()
            # Remove outer quotes if present
            if content.startswith('"') and content.endswith('"'):
                content = content[1:-1]
                return [
                    f"{indent_str}print(\n",
                    f'{indent_str}    "{content}"\n',
                    f"{indent_str})\n",
                ]

    # Pattern 4: Dictionary assignments
    if ": (" in line and ")," in line:
        # Complex dictionary value assignment
        indent_str = " " * indent
        key_match = re.match(r'(\s*)"([^"]+)": \((.+)\),?', line)
        if key_match:
            spaces, key, value = key_match.groups()
            comma = "," if line.rstrip().endswith(",") else ""
            return [
                f'{spaces}"{key}": (\n',
                f"{spaces}    {value}\n",
                f"{spaces}){comma}\n",
            ]

    # Pattern 5: Function calls with long parameters
    if ".get(" in line and len(line) > 79:
        parts = line.split(".get(", 1)
        if len(parts) == 2:
            before_get = parts[0]
            after_get = parts[1]
            return [f"{before_get}.get(\n", f"{base_indent}    {after_get}\n"]

    # Pattern 6: List assignments
    if ": [" in line and "]," in line:
        match = re.match(r'(\s*)"([^"]+)": \[(.+)\],?', line)
        if match:
            spaces, key, values = match.groups()
            comma = "," if line.rstrip().endswith(",") else ""
            return [
                f'{spaces}"{key}": [\n',
                f"{spaces}    {values}\n",
                f"{spaces}]{comma}\n",
            ]

    # Default: Simple break at natural points
    if len(line) > 79:
        # Try to break at comma or operator
        for break_char in [", ", " + ", " and ", " or "]:
            if break_char in line:
                parts = line.split(break_char, 1)
                if len(parts) == 2 and len(parts[0]) < 75:
                    return [
                        f"{parts[0]}{break_char[0]}\n",
                        f"{base_indent}    {break_char[1:]}{parts[1]}\n",
                    ]

    # If no pattern matches, return original
    return [line]


if __name__ == "__main__":
    apply_quantum_line_decomposition("test_compression_integration.py")
