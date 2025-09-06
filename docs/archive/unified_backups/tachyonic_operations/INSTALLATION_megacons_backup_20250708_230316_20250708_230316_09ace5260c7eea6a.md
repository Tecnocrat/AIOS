# AIOS Installation Guide

## System Requirements

### Minimum Requirements
- **OS**: Windows 10/11, Ubuntu 20.04+, macOS 12+
- **RAM**: 8 GB
- **Storage**: 5 GB free space
- **CPU**: Intel i5 or AMD Ryzen 5 equivalent

### Recommended Requirements
- **OS**: Windows 11, Ubuntu 22.04+, macOS 13+
- **RAM**: 16 GB or more
- **Storage**: 10 GB free space (SSD recommended)
- **CPU**: Intel i7 or AMD Ryzen 7 equivalent
- **GPU**: NVIDIA GTX 1060 or better (for AI acceleration)

## Prerequisites Installation

### Windows

#### 1. Install Visual Studio 2022
```powershell
# Download from: https://visualstudio.microsoft.com/downloads/
# Required workloads:
# - Desktop development with C++
# - .NET Desktop Development
```

#### 2. Install Python 3.11+
```powershell
# Download from: https://python.org/downloads/
# Or use winget
winget install Python.Python.3.11

# Verify installation
python --version
```

#### 3. Install CMake
```powershell
# Download from: https://cmake.org/download/
# Or use winget
winget install Kitware.CMake

# Verify installation
cmake --version
```

#### 4. Install Git
```powershell
# Download from: https://git-scm.com/download/win
# Or use winget
winget install Git.Git

# Verify installation
git --version
```

#### 5. Install vcpkg (C++ Package Manager)
```powershell
# Clone vcpkg
git clone https://github.com/Microsoft/vcpkg.git C:\dev\vcpkg
cd C:\dev\vcpkg

# Bootstrap vcpkg
.\bootstrap-vcpkg.bat

# Integrate with Visual Studio
.\vcpkg integrate install
```

### Linux (Ubuntu/Debian)

#### 1. Update System
```bash
sudo apt update && sudo apt upgrade -y
```

#### 2. Install Development Tools
```bash
# Essential build tools
sudo apt install -y build-essential cmake git

# Python 3.11+
sudo apt install -y python3.11 python3.11-venv python3.11-dev python3-pip

# .NET 8.0
wget https://packages.microsoft.com/config/ubuntu/22.04/packages-microsoft-prod.deb -O packages-microsoft-prod.deb
sudo dpkg -i packages-microsoft-prod.deb
sudo apt update
sudo apt install -y dotnet-sdk-8.0
```

#### 3. Install vcpkg
```bash
# Clone vcpkg
git clone https://github.com/Microsoft/vcpkg.git ~/vcpkg
cd ~/vcpkg

# Bootstrap vcpkg
./bootstrap-vcpkg.sh

# Add to PATH (add to ~/.bashrc for persistence)
export PATH="$HOME/vcpkg:$PATH"
```

### macOS

#### 1. Install Xcode Command Line Tools
```bash
xcode-select --install
```

#### 2. Install Homebrew
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### 3. Install Dependencies
```bash
# Development tools
brew install cmake git python@3.11

# .NET 8.0
brew install --cask dotnet-sdk
```

#### 4. Install vcpkg
```bash
# Clone vcpkg
git clone https://github.com/Microsoft/vcpkg.git ~/vcpkg
cd ~/vcpkg

# Bootstrap vcpkg
./bootstrap-vcpkg.sh

# Add to PATH (add to ~/.zshrc for persistence)
export PATH="$HOME/vcpkg:$PATH"
```

## AIOS Installation

### Method 1: Automated Setup (Recommended)

#### Windows
```powershell
# Clone the repository
git clone https://github.com/user/AIOS.git -b OS0.4
cd AIOS

# Run the setup script
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\setup.ps1
```

#### Linux/macOS
```bash
# Clone the repository
git clone https://github.com/user/AIOS.git -b OS0.4
cd AIOS

# Make setup script executable and run
chmod +x setup.sh
./setup.sh
```

### Method 2: Manual Installation

#### 1. Clone Repository
```bash
git clone https://github.com/user/AIOS.git -b OS0.4
cd AIOS
```

#### 2. Setup Python Environment
```bash
# Create virtual environment
cd ai
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

#### 3. Install C++ Dependencies
```bash
# Windows
cd C:\dev\vcpkg
.\vcpkg install boost-system boost-filesystem boost-thread nlohmann-json opencv --triplet x64-windows

# Linux
cd ~/vcpkg
./vcpkg install boost-system boost-filesystem boost-thread nlohmann-json opencv --triplet x64-linux

# macOS
cd ~/vcpkg
./vcpkg install boost-system boost-filesystem boost-thread nlohmann-json opencv --triplet x64-osx
```

#### 4. Build C++ Core
```bash
cd core
mkdir build && cd build

# Configure with vcpkg
# Windows
cmake .. -DCMAKE_TOOLCHAIN_FILE=C:/dev/vcpkg/scripts/buildsystems/vcpkg.cmake -DCMAKE_BUILD_TYPE=Debug

# Linux
cmake .. -DCMAKE_TOOLCHAIN_FILE=~/vcpkg/scripts/buildsystems/vcpkg.cmake -DCMAKE_BUILD_TYPE=Debug

# macOS
cmake .. -DCMAKE_TOOLCHAIN_FILE=~/vcpkg/scripts/buildsystems/vcpkg.cmake -DCMAKE_BUILD_TYPE=Debug

# Build
cmake --build . --config Debug
```

#### 5. Setup C# Interface (Optional)
```bash
cd interface

# Restore NuGet packages
dotnet restore

# Build solution
dotnet build
```

## Verification

### 1. Run Integration Tests
```bash
# From project root
python test_integration.py
```

**Expected Output:**
```
==================================================
AIOS Integration Test
==================================================
Testing C++ core...
C++ core executed successfully!
==================================================
Testing AI modules...
NLP processing result: {'input': 'Hello, how are you?', 'intent': 'help', ...}
Prediction result: {'type': 'general', 'input': {...}, ...}
Automation task result: {'task_id': 'unknown', 'status': 'completed', ...}
Learning result: {'update_type': 'general', 'data_stored': True, ...}
Integration result: {'message_id': 'msg_1', 'target': 'test_target', ...}
All AI modules tested successfully!
==================================================
INTEGRATION TEST RESULTS
==================================================
C++ Core: ✅ PASS
Python AI: ✅ PASS
🎉 ALL TESTS PASSED! AIOS system is ready!
```

### 2. Test C++ Core Individually
```bash
cd core/build/bin/Debug
./aios_main  # Linux/macOS
aios_main.exe  # Windows
```

**Expected Output:**
```
AIOS - Artificial Intelligence Operating System
Version 1.0.0
Initializing system...
AIOS Core initialized successfully!
System initialized successfully
AIOS>help
Available commands: help, status, health, exit
AIOS>exit
```

### 3. Test Python AI Modules
```bash
cd ai
# Activate virtual environment if not already active
python -c "import sys; sys.path.append('src'); from core.nlp import NLPManager; print('✅ Python AI modules working')"
```

## Troubleshooting

### Common Issues

#### Issue: Python virtual environment not working
**Symptoms**: `ModuleNotFoundError` when importing AI modules
**Solution**:
```bash
# Recreate virtual environment
cd ai
rm -rf venv
python -m venv venv
# Activate and reinstall dependencies
pip install -r requirements.txt
```

#### Issue: C++ compilation errors
**Symptoms**: CMake or build errors mentioning missing libraries
**Solution**:
```bash
# Verify vcpkg dependencies
vcpkg list

# Reinstall if necessary
vcpkg install boost-system boost-filesystem boost-thread nlohmann-json opencv --triplet [your-triplet]

# Clean and rebuild
cd core/build
rm -rf *
cmake .. -DCMAKE_TOOLCHAIN_FILE=[vcpkg-path]/scripts/buildsystems/vcpkg.cmake
cmake --build .
```

#### Issue: CMake can't find vcpkg
**Symptoms**: `Could not find a package configuration file provided by`
**Solution**:
```bash
# Verify vcpkg path and ensure it's integrated
# Windows
C:\dev\vcpkg\vcpkg integrate install

# Linux/macOS
~/vcpkg/vcpkg integrate install

# Use explicit toolchain file path in CMake
cmake .. -DCMAKE_TOOLCHAIN_FILE=[full-path-to-vcpkg]/scripts/buildsystems/vcpkg.cmake
```

#### Issue: Integration test fails
**Symptoms**: `AIOS Integration Test` reports failures
**Solution**:
1. Check C++ core builds successfully
2. Verify Python modules import without errors
3. Ensure working directory is project root
4. Check that all dependencies are installed

#### Issue: Permission denied on setup scripts
**Symptoms**: Scripts fail to execute
**Solution**:
```bash
# Windows PowerShell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Linux/macOS
chmod +x setup.sh
```

### Platform-Specific Issues

#### Windows

**Issue**: vcpkg triplet mismatch
**Solution**: Use `x64-windows` triplet for 64-bit Windows
```powershell
vcpkg install [packages] --triplet x64-windows
```

**Issue**: Visual Studio not found
**Solution**: Install Visual Studio 2022 with C++ workload, or use Visual Studio Build Tools

#### Linux

**Issue**: Missing development headers
**Solution**:
```bash
sudo apt install -y python3.11-dev build-essential
```

**Issue**: OpenCV build fails
**Solution**:
```bash
sudo apt install -y libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev
```

#### macOS

**Issue**: Command Line Tools not found
**Solution**:
```bash
sudo xcode-select --reset
xcode-select --install
```

**Issue**: brew command not found
**Solution**: Install Homebrew first, then restart terminal

## Performance Optimization

### SSD Recommendation
For best performance, install AIOS on an SSD drive, especially for AI model loading and processing.

### Memory Configuration
For systems with limited RAM:
```json
// config/system.json
{
  "core": {
    "threads": 4,
    "memory_limit_mb": 512
  },
  "ai": {
    "nlp": {
      "model_cache_size": 100
    }
  }
}
```

### GPU Acceleration (Optional)
For NVIDIA GPUs:
```bash
# Install CUDA toolkit
# Windows: Download from NVIDIA website
# Linux: sudo apt install nvidia-cuda-toolkit
# macOS: CUDA not supported on newer macOS versions

# Install GPU-accelerated packages
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

## Next Steps

After successful installation:

1. **Read Documentation**: Start with [ARCHITECTURE.md](ARCHITECTURE.md)
2. **Explore APIs**: Check [API_REFERENCE.md](API_REFERENCE.md)
3. **Development Setup**: Follow [DEVELOPMENT.md](DEVELOPMENT.md)
4. **Run Examples**: Try the sample commands in the C++ core interface
5. **Contribute**: See contributing guidelines in the development guide

## Support

If you encounter issues not covered in this guide:

1. Check [Known Issues](../README.md#known-issues) in README
2. Search [GitHub Issues](https://github.com/user/AIOS/issues)
3. Create a new issue with:
   - Operating system and version
   - Installation method used
   - Complete error messages
   - Output of `python test_integration.py`

## Automated Installation Verification

To verify your installation is working correctly, run this comprehensive check:

```bash
# Quick verification script
python -c "
import sys
import subprocess
print('🔍 AIOS Installation Verification')
print('=' * 40)

# Check Python
print(f'Python version: {sys.version}')

# Check C++ core
try:
    result = subprocess.run(['core/build/bin/Debug/aios_main'], 
                          input='help\nexit\n', text=True, 
                          capture_output=True, timeout=10)
    print('✅ C++ core: Working')
except:
    print('❌ C++ core: Failed')

# Check Python modules
try:
    sys.path.append('ai/src')
    from core.nlp import NLPManager
    print('✅ Python AI: Working')
except:
    print('❌ Python AI: Failed')

print('\\n✅ Installation verification complete!')
"
```

This installation guide provides comprehensive instructions for setting up AIOS across all supported platforms with detailed troubleshooting information.
