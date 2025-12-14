#!/usr/bin/env python3
"""
AINLP Comprehensive Linting Enhancement Tool
Enhanced systematic fixer for line length, imports, whitespace, and type issues
Follows AINLP enhancement-over-creation paradigm
"""

import logging
import os
import sys
import re
import ast
from pathlib import Path
from typing import List, Dict, Any, Optional

MAX_LINE_LENGTH = 79

<<<<<<< HEAD

=======
>>>>>>> origin/OS0.6.2.grok
class ComprehensiveLinter:
    """Enhanced linting tool for AIOS codebase"""

    def __init__(self):
        self.setup_logging()

    def setup_logging(self):
        """Setup comprehensive logging"""
<<<<<<< HEAD
        log_path = os.path.join(os.path.dirname(__file__), "comprehensive_linter.log")
=======
        log_path = os.path.join(
            os.path.dirname(__file__),
            "comprehensive_linter.log"
        )
>>>>>>> origin/OS0.6.2.grok
        logger = logging.getLogger("comprehensive_linter")
        logger.setLevel(logging.INFO)

        handler = logging.FileHandler(log_path, mode="a", encoding="utf-8")
<<<<<<< HEAD
        formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
=======
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s"
        )
>>>>>>> origin/OS0.6.2.grok
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        self.logger = logger

    def fix_file(self, file_path: str) -> bool:
        """Fix linting issues in a file"""
        try:
<<<<<<< HEAD
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            original_lines = content.split("\n")
=======
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            original_lines = content.split('\n')
>>>>>>> origin/OS0.6.2.grok
            fixed_lines = []

            for line in original_lines:
                fixed_line = self.fix_line(line)
                fixed_lines.append(fixed_line)

<<<<<<< HEAD
            fixed_content = "\n".join(fixed_lines)

            # Write back if changes were made
            if fixed_content != content:
                with open(file_path, "w", encoding="utf-8") as f:
=======
            fixed_content = '\n'.join(fixed_lines)

            # Write back if changes were made
            if fixed_content != content:
                with open(file_path, 'w', encoding='utf-8') as f:
>>>>>>> origin/OS0.6.2.grok
                    f.write(fixed_content)
                self.logger.info(f"Fixed linting issues in {file_path}")
                return True
            else:
                self.logger.info(f"No changes needed in {file_path}")
                return False

        except Exception as e:
            self.logger.error(f"Error fixing {file_path}: {e}")
            return False

    def fix_line(self, line: str) -> str:
        """Fix common linting issues in a line"""
        # Fix trailing whitespace
        line = line.rstrip()

        # Fix line length (basic approach)
        if len(line) > MAX_LINE_LENGTH:
            line = self.break_long_line(line)

        return line

    def break_long_line(self, line: str) -> str:
        """Break long lines intelligently"""
        if len(line) <= MAX_LINE_LENGTH:
            return line

        # Don't break comments, docstrings, or URLs
<<<<<<< HEAD
        if (
            line.strip().startswith("#")
            or "http" in line
            or line.strip().startswith('"""')
            or line.strip().startswith("'''")
        ):
=======
        if (line.strip().startswith('#') or
            'http' in line or
            line.strip().startswith('"""') or
            line.strip().startswith("'''")):
>>>>>>> origin/OS0.6.2.grok
            return line

        # Try to break at comma
        indent = len(line) - len(line.lstrip())
        content = line[indent:]

<<<<<<< HEAD
        comma_pos = content.rfind(",", 0, MAX_LINE_LENGTH - indent)
        if comma_pos > 0:
            return (
                line[: indent + comma_pos + 1]
                + "\\\n"
                + " " * (indent + 4)
                + content[comma_pos + 1 :].lstrip()
            )

        # Break at operator
        operators = [" and ", " or ", " + ", " - ", " * ", " / "]
=======
        comma_pos = content.rfind(',', 0, MAX_LINE_LENGTH - indent)
        if comma_pos > 0:
            return (line[:indent + comma_pos + 1] + '\\\n' +
                   ' ' * (indent + 4) + content[comma_pos + 1:].lstrip())

        # Break at operator
        operators = [' and ', ' or ', ' + ', ' - ', ' * ', ' / ']
>>>>>>> origin/OS0.6.2.grok
        for op in operators:
            if op in content:
                op_pos = content.find(op)
                if indent + op_pos < MAX_LINE_LENGTH:
                    continue
<<<<<<< HEAD
                return (
                    line[: indent + op_pos]
                    + "\\\n"
                    + " " * (indent + 4)
                    + content[op_pos:].lstrip()
                )

        # Force break at max length
        return (
            line[:MAX_LINE_LENGTH]
            + "\\\n"
            + " " * (indent + 4)
            + line[MAX_LINE_LENGTH:].lstrip()
        )
=======
                return (line[:indent + op_pos] + '\\\n' +
                       ' ' * (indent + 4) + content[op_pos:].lstrip())

        # Force break at max length
        return (line[:MAX_LINE_LENGTH] + '\\\n' +
               ' ' * (indent + 4) + line[MAX_LINE_LENGTH:].lstrip())
>>>>>>> origin/OS0.6.2.grok

    def analyze_imports(self, file_path: str) -> Dict[str, Any]:
        """Analyze import usage in file"""
        try:
<<<<<<< HEAD
            with open(file_path, "r", encoding="utf-8") as f:
=======
            with open(file_path, 'r', encoding='utf-8') as f:
>>>>>>> origin/OS0.6.2.grok
                content = f.read()

            tree = ast.parse(content)
            imports = []
            used_names = set()

            # Collect imports
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
<<<<<<< HEAD
                        imports.append(alias.name.split(".")[0])
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(node.module.split(".")[0])
=======
                        imports.append(alias.name.split('.')[0])
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(node.module.split('.')[0])
>>>>>>> origin/OS0.6.2.grok

                # Collect used names
                if isinstance(node, ast.Name):
                    used_names.add(node.id)

            unused_imports = []
            for imp in imports:
<<<<<<< HEAD
                if imp not in used_names and imp not in ["os", "sys", "logging"]:
                    unused_imports.append(imp)

            return {
                "total_imports": len(imports),
                "unused_imports": unused_imports,
                "used_names": len(used_names),
=======
                if imp not in used_names and imp not in ['os', 'sys', 'logging']:
                    unused_imports.append(imp)

            return {
                'total_imports': len(imports),
                'unused_imports': unused_imports,
                'used_names': len(used_names)
>>>>>>> origin/OS0.6.2.grok
            }

        except Exception as e:
            self.logger.error(f"Error analyzing imports in {file_path}: {e}")
            return {}

<<<<<<< HEAD

=======
>>>>>>> origin/OS0.6.2.grok
def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python comprehensive_linter.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    linter = ComprehensiveLinter()

    print(f"🔍 Analyzing {file_path}...")

    # Analyze imports
    import_analysis = linter.analyze_imports(file_path)
<<<<<<< HEAD
    if import_analysis.get("unused_imports"):
=======
    if import_analysis.get('unused_imports'):
>>>>>>> origin/OS0.6.2.grok
        print(f"⚠️  Unused imports: {import_analysis['unused_imports']}")

    # Fix the file
    if linter.fix_file(file_path):
        print(f"✅ Fixed linting issues in {file_path}")
    else:
        print(f"ℹ️  No changes needed in {file_path}")

<<<<<<< HEAD

if __name__ == "__main__":
    main()
=======
if __name__ == "__main__":
    main()
>>>>>>> origin/OS0.6.2.grok
