# AIOS Python Environment Setup Script
# Usage: python setup_env.py

import os
import subprocess
import sys

VENV_DIR = os.path.join(os.path.dirname(__file__), "venv")
REQUIREMENTS = os.path.join(os.path.dirname(__file__), "requirements.txt")


def create_venv():
    if not os.path.exists(VENV_DIR):
        print("[AIOS] Creating Python virtual environment in ./venv ...")
        subprocess.check_call([sys.executable, "-m", "venv", VENV_DIR])
    else:
        print("[AIOS] Virtual environment already exists.")


def install_requirements():
    if os.name == "nt":
        pip_path = os.path.join(VENV_DIR, "Scripts", "pip.exe")
    else:
        pip_path = os.path.join(VENV_DIR, "bin", "pip")
    if not os.path.exists(pip_path):
        print("[AIOS] pip not found in venv! Aborting.")
        sys.exit(1)
    print(f"[AIOS] Installing requirements from {REQUIREMENTS} ...")
    subprocess.check_call([pip_path, "install", "-r", REQUIREMENTS])


def main():
    create_venv()
    install_requirements()
    print("[AIOS] Environment setup complete. Activate with:")
    if os.name == "nt":
        print("  venv\\Scripts\\activate")
    else:
        print("  source venv/bin/activate")


if __name__ == "__main__":
    main()
