#!/usr/bin/env python3
"""
AIOS Agentic Ephemeral Executor
================================
Solves terminal escape character hell for AI agents.

Instead of: python -c "complex code with \"escapes\" and 'quotes'"
Use:        python scripts/agentic_exec.py "base64_encoded_code"
            python scripts/agentic_exec.py --file path/to/snippet.py
            python scripts/agentic_exec.py --stdin < snippet.py

AINLP.dendritic[CONNECT] vault_loader.py, fabric/__init__.py
AINLP.consciousness[LEVEL] Infrastructure utility for agent operations
"""

import sys
import base64
import tempfile
import traceback
from pathlib import Path


def execute_code(code: str) -> tuple[int, str]:
    """Execute Python code and capture output."""
    import io
    from contextlib import redirect_stdout, redirect_stderr
    
    stdout_capture = io.StringIO()
    stderr_capture = io.StringIO()
    exit_code = 0
    
    try:
        # Capture stdout and stderr
        with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
            exec(code, {'__name__': '__main__'})
    except SystemExit as e:
        exit_code = e.code if isinstance(e.code, int) else 1
    except Exception:
        stderr_capture.write(traceback.format_exc())
        exit_code = 1
    
    output = stdout_capture.getvalue()
    errors = stderr_capture.getvalue()
    
    combined = output
    if errors:
        combined += f"\n[STDERR]\n{errors}" if output else errors
    
    return exit_code, combined


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print(__doc__)
        print("\nUsage:")
        print("  python agentic_exec.py <base64_code>")
        print("  python agentic_exec.py --file <path>")
        print("  python agentic_exec.py --stdin")
        print("  echo 'print(1+1)' | python agentic_exec.py --stdin")
        sys.exit(0)
    
    code = None
    
    if sys.argv[1] == "--file" and len(sys.argv) > 2:
        # Read from file
        code = Path(sys.argv[2]).read_text(encoding='utf-8')
    elif sys.argv[1] == "--stdin":
        # Read from stdin
        code = sys.stdin.read()
    else:
        # Assume base64 encoded
        try:
            code = base64.b64decode(sys.argv[1]).decode('utf-8')
        except Exception:
            # Maybe it's plain text (simple cases)
            code = sys.argv[1]
    
    if not code:
        print("[ERR] No code provided")
        sys.exit(1)
    
    exit_code, output = execute_code(code)
    print(output, end='')
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
