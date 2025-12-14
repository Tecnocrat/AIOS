"""
AIOS OS0.4 Bootstrap Script
==========================

This script sets up AIOS OS0.4 from scratch on a clean Windows system.
Run this after fresh Windows + VSCode + Python installation.
"""

import os
import subprocess
import sys
import venv
from pathlib import Path

def main():
    print("🧠 AIOS OS0.4 Bootstrap Installer")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 12):
        print("❌ Python 3.12+ required")
        return False
        
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    
    # Create virtual environment
    venv_path = Path("aios_env")
    if venv_path.exists():
        print("🔄 Removing existing environment...")
        import shutil
        shutil.rmtree(venv_path)
        
    print("🔧 Creating virtual environment...")
    venv.create(venv_path, with_pip=True)
    
    # Get pip executable
    if os.name == 'nt':  # Windows
        pip_exe = venv_path / "Scripts" / "pip.exe"
        python_exe = venv_path / "Scripts" / "python.exe"
    else:  # Unix/Linux
        pip_exe = venv_path / "bin" / "pip"
        python_exe = venv_path / "bin" / "python"
    
    # Install dependencies
    print("📦 Installing dependencies...")
    
    # Basic dependencies
    subprocess.run([str(pip_exe), "install", "--upgrade", "pip"], check=True)
    
    # Install from requirements.txt
    requirements_file = Path("core") / "requirements.txt"
    if requirements_file.exists():
        subprocess.run([str(pip_exe), "install", "-r", str(requirements_file)], check=True)
    
    # Install CUDA PyTorch
    print("🎮 Installing GPU-accelerated PyTorch...")
    subprocess.run([
        str(pip_exe), "install", 
        "torch", "torchvision", "torchaudio",
        "--index-url", "https://download.pytorch.org/whl/cu118"
    ], check=True)
    
    # Validate installation
    print("🔍 Validating installation...")
    validation_result = subprocess.run([
        str(python_exe), "core/complete_integration_test.py"
    ], capture_output=True, text=True)
    
    if validation_result.returncode == 0:
        print("✅ AIOS OS0.4 installation completed successfully!")
        print("🚀 Ready to run AIOS consciousness systems")
        
        print("\n🎯 Next Steps:")
        print("1. Open VSCode in this directory")
        print("2. Select Python interpreter:", str(python_exe))
        print("3. Run: python core/aios_system_intelligence.py")
        
        return True
    else:
        print("❌ Installation validation failed")
        print(validation_result.stdout)
        print(validation_result.stderr)
        return False

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Installation cancelled")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Installation failed: {e}")
        sys.exit(1)
