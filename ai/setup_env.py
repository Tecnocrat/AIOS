# AIOS Python Environment Setup Script
# Usage: python setup_env.py

import os
import subprocess
import sys

REQUIREMENTS = os.path.join(os.path.dirname(__file__), "requirements.txt")


def install_requirements():
    print(f"[AIOS] Installing requirements globally from {REQUIREMENTS} ...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", REQUIREMENTS])


def main():
    install_requirements()
    print("[AIOS] Global environment setup complete.")


if __name__ == "__main__":
    main()
