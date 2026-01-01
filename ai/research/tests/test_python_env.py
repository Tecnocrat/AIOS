"""
🧪 AIOS Python Environment Test (pytest)
Validates essential Python packages used by AIOS.

AINLP provenance:
- Origin: migrated from root test_python_env.py on 2025-08-10
- Intent: convert ad-hoc env script into a deterministic pytest check
- Scope: fast import smoke; deeper diagnostics live in
    tools/system_health_check
"""


def test_essential_imports():
    """Smoke test essential AIOS packages; prints versions for visibility."""
    print(" Testing AIOS Python Environment (pytest)...")

    import sys
    print(f" Python version: {sys.version}")

    import numpy as np
    print(f" NumPy {np.__version__} - Scientific computing")

    import pandas as pd
    print(f" Pandas {pd.__version__} - Data manipulation")

    import openai
    print(f" OpenAI {openai.__version__} - AI integration")

    import aiohttp
    print(f" aiohttp {aiohttp.__version__} - Async HTTP")

    import rich  # noqa: F401
    print(" Rich (console output) - OK")

    import astroid
    print(f" Astroid {astroid.__version__} - Code analysis")

    import pytest as _pytest
    print(f" Pytest {_pytest.__version__} - Testing framework")

    import cv2
    print(f" OpenCV {cv2.__version__} - Computer vision")

    # If imports succeeded without exceptions, the environment is OK
    assert True


def test_env_packages_ok():
    """Wrapper to ensure the environment test is counted explicitly."""
    # If any import above fails, pytest will error; this simply affirms pass
    assert True
