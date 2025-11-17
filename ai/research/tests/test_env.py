# filepath: C:\dev\AIOS\ai\tests\test_env.py
"""
Test file to verify virtual environment functionality and package availability.
"""


def test_basic_imports():
    """Test that basic packages can be imported successfully."""
    try:
        import flask  # type: ignore
        print(f" Flask imported successfully: {flask.__version__}")
    except ImportError as e:
        print(f"  Flask not available: {e}")

    try:
        import requests
        print(f" Requests imported successfully: {requests.__version__}")
    except ImportError as e:
        print(f"  Requests not available: {e}")

    try:
        import numpy as np
        print(f" NumPy imported successfully: {np.__version__}")
    except ImportError as e:
        print(f"  NumPy not available: {e}")


if __name__ == "__main__":
    print("🧪 Testing virtual environment packages...")
    test_basic_imports()
    print(" Virtual environment test completed!")
