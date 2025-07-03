
import sys
import subprocess
import venv
from pathlib import Path

def setup_isolated_environment():
    """Setup isolated Python environment"""
    venv_path = Path("isolated_env")
    if not venv_path.exists():
        venv.create(venv_path, with_pip=True)
    
    # Install basic packages
    pip_path = venv_path / "Scripts" / "pip.exe"
    if pip_path.exists():
        subprocess.run([str(pip_path), "install", "numpy", "psutil"], 
                      capture_output=True, text=True)
    
    return venv_path

if __name__ == "__main__":
    setup_isolated_environment()
