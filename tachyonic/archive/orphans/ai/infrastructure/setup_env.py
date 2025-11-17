# AIOS Python Environment Setup Script
# Usage: python setup_env.py

import os
import subprocess
import sys

REQUIREMENTS = os.path.join(os.path.dirname(__file__), "requirements.txt")


def install_requirements():
    print(
        "[AIOS] Installing requirements using interpreter: "
        f"{sys.executable}"
    )
    print(f"[AIOS] Requirements file: {REQUIREMENTS}")
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", REQUIREMENTS]
        )
        print("[AIOS] Requirements installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"[AIOS] ERROR: Failed to install requirements. {e}")
        sys.exit(1)


def show_python_info():
    print(f"[AIOS] Python executable: {sys.executable}")
    print(f"[AIOS] Python version: {sys.version}")
    print(f"[AIOS] PYTHONPATH: {os.environ.get('PYTHONPATH', '(not set)')}")


def main():
    show_python_info()
    install_requirements()
    print("[AIOS] Environment setup complete.")


if __name__ == "__main__":
    main()
