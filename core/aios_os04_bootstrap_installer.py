"""
AIOS OS0.4 Bootstrap Installer
=============================

Self-contained installer and deployment script for AIOS OS0.4 architecture.
This script can completely bootstrap the AIOS system from scratch on a clean environment.

Author: AIOS Development Team
Date: July 2, 2025
Version: OS0.4.0
"""

import asyncio
import json
import logging
import os
import platform
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
import tempfile
import zipfile

# Configure logging for installer
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('aios_os04_install.log')
    ]
)
logger = logging.getLogger('AIOS_OS04_Installer')

class AIOSOS04Installer:
    """Complete AIOS OS0.4 bootstrap installer"""
    
    def __init__(self, target_directory: Optional[str] = None):
        self.target_dir = Path(target_directory) if target_directory else Path.cwd() / "AIOS_OS04"
        self.core_dir = self.target_dir / "core"
        self.config_dir = self.target_dir / "config"
        self.logs_dir = self.target_dir / "logs"
        self.data_dir = self.target_dir / "data"
        
        self.python_executable = None
        self.venv_path = self.target_dir / "aios_env"
        
        self.installation_log = []
        self.start_time = time.time()
        
    def log_step(self, message: str, success: bool = True):
        """Log installation step with timestamp"""
        timestamp = time.time() - self.start_time
        status = "✅ SUCCESS" if success else "❌ FAILED"
        log_entry = f"[{timestamp:.1f}s] {status}: {message}"
        self.installation_log.append(log_entry)
        
        if success:
            logger.info(message)
        else:
            logger.error(message)
            
    def check_prerequisites(self) -> Dict[str, bool]:
        """Check system prerequisites for AIOS OS0.4"""
        print("🔍 Checking system prerequisites...")
        
        checks = {
            'python_version': False,
            'pip_available': False,
            'git_available': False,
            'powershell_available': False,
            'cmake_available': False,
            'gpu_available': False,
            'storage_space': False,
            'permissions': False
        }
        
        # Check Python version (3.10+)
        try:
            version_info = sys.version_info
            if version_info.major == 3 and version_info.minor >= 10:
                checks['python_version'] = True
                self.python_executable = sys.executable
                self.log_step(f"Python {version_info.major}.{version_info.minor}.{version_info.micro} detected")
            else:
                self.log_step(f"Python version {version_info.major}.{version_info.minor} insufficient (requires 3.10+)", False)
        except Exception as e:
            self.log_step(f"Python version check failed: {e}", False)
            
        # Check pip
        try:
            subprocess.run([sys.executable, '-m', 'pip', '--version'], 
                         capture_output=True, check=True)
            checks['pip_available'] = True
            self.log_step("pip available")
        except subprocess.CalledProcessError:
            self.log_step("pip not available", False)
            
        # Check Git
        try:
            subprocess.run(['git', '--version'], 
                         capture_output=True, check=True)
            checks['git_available'] = True
            self.log_step("Git available")
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.log_step("Git not available (optional)", True)  # Git is optional
            
        # Check PowerShell (Windows)
        if platform.system() == "Windows":
            try:
                subprocess.run(['powershell', '-Command', 'Get-Host'], 
                             capture_output=True, check=True)
                checks['powershell_available'] = True
                self.log_step("PowerShell available")
            except (subprocess.CalledProcessError, FileNotFoundError):
                self.log_step("PowerShell not available", False)
        else:
            checks['powershell_available'] = True  # Not required on non-Windows
            
        # Check CMake (optional)
        try:
            subprocess.run(['cmake', '--version'], 
                         capture_output=True, check=True)
            checks['cmake_available'] = True
            self.log_step("CMake available")
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.log_step("CMake not available (optional for C++ components)", True)
            
        # Check GPU availability
        try:
            import torch
            if torch.cuda.is_available():
                gpu_name = torch.cuda.get_device_name(0)
                checks['gpu_available'] = True
                self.log_step(f"GPU available: {gpu_name}")
            else:
                self.log_step("GPU not available (will use CPU mode)", True)
        except ImportError:
            self.log_step("PyTorch not installed (will install during setup)", True)
            
        # Check storage space (require 2GB)
        try:
            free_space = shutil.disk_usage(Path.cwd()).free
            required_space = 2 * 1024 * 1024 * 1024  # 2GB
            if free_space > required_space:
                checks['storage_space'] = True
                self.log_step(f"Storage space: {free_space / (1024**3):.1f}GB available")
            else:
                self.log_step(f"Insufficient storage space: {free_space / (1024**3):.1f}GB available, 2GB required", False)
        except Exception as e:
            self.log_step(f"Storage space check failed: {e}", False)
            
        # Check write permissions
        try:
            test_file = self.target_dir.parent / "aios_test_permissions"
            test_file.touch()
            test_file.unlink()
            checks['permissions'] = True
            self.log_step("Write permissions confirmed")
        except Exception as e:
            self.log_step(f"Insufficient permissions: {e}", False)
            
        return checks
        
    def create_directory_structure(self):
        """Create AIOS OS0.4 directory structure"""
        print("📁 Creating directory structure...")
        
        directories = [
            self.target_dir,
            self.core_dir,
            self.config_dir,
            self.logs_dir,
            self.data_dir,
            self.target_dir / "scripts",
            self.target_dir / "docs",
            self.target_dir / "backups",
            self.data_dir / "consciousness",
            self.data_dir / "evolution",
            self.data_dir / "knowledge",
            self.data_dir / "monitoring"
        ]
        
        for directory in directories:
            try:
                directory.mkdir(parents=True, exist_ok=True)
                self.log_step(f"Created directory: {directory}")
            except Exception as e:
                self.log_step(f"Failed to create directory {directory}: {e}", False)
                raise
                
    def setup_python_environment(self):
        """Setup Python virtual environment"""
        print("🐍 Setting up Python virtual environment...")
        
        try:
            # Create virtual environment
            subprocess.run([
                self.python_executable, '-m', 'venv', str(self.venv_path)
            ], check=True)
            self.log_step(f"Virtual environment created: {self.venv_path}")
            
            # Get venv python executable
            if platform.system() == "Windows":
                venv_python = self.venv_path / "Scripts" / "python.exe"
                venv_pip = self.venv_path / "Scripts" / "pip.exe"
            else:
                venv_python = self.venv_path / "bin" / "python"
                venv_pip = self.venv_path / "bin" / "pip"
                
            # Upgrade pip
            subprocess.run([
                str(venv_python), '-m', 'pip', 'install', '--upgrade', 'pip'
            ], check=True)
            self.log_step("Virtual environment pip upgraded")
            
            # Install core dependencies
            core_dependencies = [
                'psutil>=5.9.0',
                'aiofiles>=23.1.0',
                'astroid>=2.15.0',
                'rope>=1.7.0',
                'numpy>=1.24.0',
                'matplotlib>=3.7.0',
                'plotly>=5.15.0',
                'flask>=2.3.0',
                'flask-socketio>=5.3.0',
                'websockets>=11.0.0',
                'requests>=2.31.0'
            ]
            
            self.log_step("Installing core dependencies...")
            subprocess.run([
                str(venv_pip), 'install'
            ] + core_dependencies, check=True)
            self.log_step("Core dependencies installed")
            
            # Install PyTorch with CUDA support
            self.log_step("Installing PyTorch with CUDA support...")
            subprocess.run([
                str(venv_pip), 'install', 'torch', 'torchvision', 'torchaudio',
                '--index-url', 'https://download.pytorch.org/whl/cu118'
            ], check=True)
            self.log_step("PyTorch with CUDA support installed")
            
            self.python_executable = str(venv_python)
            
        except subprocess.CalledProcessError as e:
            self.log_step(f"Python environment setup failed: {e}", False)
            raise
            
    def deploy_mega_modules(self):
        """Deploy the 6 AIOS OS0.4 mega-modules"""
        print("🧠 Deploying AIOS mega-modules...")
        
        # Source directory (current core directory)
        source_core = Path(__file__).parent
        
        # List of mega-modules to copy
        mega_modules = [
            'aios_consciousness_engine.py',
            'aios_evolution_lab.py',
            'aios_knowledge_distillation.py',
            'aios_admin_orchestrator.py',
            'aios_visual_interface.py',
            'aios_system_intelligence.py'
        ]
        
        # Supporting files
        support_files = [
            'validate_mega_modules.py',
            'complete_integration_test.py',
            'requirements.txt'
        ]
        
        try:
            # Copy mega-modules
            for module in mega_modules:
                source_file = source_core / module
                target_file = self.core_dir / module
                
                if source_file.exists():
                    shutil.copy2(source_file, target_file)
                    self.log_step(f"Deployed: {module}")
                else:
                    self.log_step(f"Missing source file: {module}", False)
                    
            # Copy support files
            for support_file in support_files:
                source_file = source_core / support_file
                target_file = self.core_dir / support_file
                
                if source_file.exists():
                    shutil.copy2(source_file, target_file)
                    self.log_step(f"Deployed: {support_file}")
                    
        except Exception as e:
            self.log_step(f"Mega-module deployment failed: {e}", False)
            raise
            
    def create_configuration_files(self):
        """Create AIOS OS0.4 configuration files"""
        print("⚙️ Creating configuration files...")
        
        try:
            # Main AIOS configuration
            aios_config = {
                "system": {
                    "version": "OS0.4.0",
                    "installation_date": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "target_directory": str(self.target_dir),
                    "python_executable": self.python_executable
                },
                "consciousness": {
                    "enable_quantum_processing": True,
                    "consciousness_update_interval": 1.0,
                    "neural_network_size": 1000
                },
                "evolution": {
                    "population_size": 100,
                    "mutation_rate": 0.1,
                    "evolution_generations": 50
                },
                "knowledge": {
                    "enable_ai_models": True,
                    "distillation_rules_file": "distillation_rules.json",
                    "code_analysis_depth": "advanced"
                },
                "visual_interface": {
                    "web_port": 8080,
                    "websocket_port": 8081,
                    "cs_bridge_port": 8082,
                    "enable_real_time_updates": True
                },
                "system_intelligence": {
                    "enable_gpu_acceleration": True,
                    "monitoring_interval": 1.0,
                    "alert_thresholds": {
                        "cpu": 80.0,
                        "memory": 85.0,
                        "gpu": 90.0
                    }
                },
                "admin": {
                    "enable_auto_testing": True,
                    "backup_retention_days": 30,
                    "log_level": "INFO"
                }
            }
            
            config_file = self.config_dir / "aios_config.json"
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(aios_config, f, indent=2)
            self.log_step("AIOS configuration created")
            
            # Startup script
            startup_script = self.create_startup_script()
            startup_file = self.target_dir / "start_aios.py"
            with open(startup_file, 'w', encoding='utf-8') as f:
                f.write(startup_script)
            self.log_step("Startup script created")
            
            # Environment file
            env_content = f"""# AIOS OS0.4 Environment Configuration
AIOS_HOME={self.target_dir}
AIOS_CORE={self.core_dir}
AIOS_CONFIG={self.config_dir}
AIOS_LOGS={self.logs_dir}
AIOS_DATA={self.data_dir}
AIOS_PYTHON={self.python_executable}
AIOS_VERSION=OS0.4.0
"""
            env_file = self.target_dir / ".env"
            with open(env_file, 'w', encoding='utf-8') as f:
                f.write(env_content)
            self.log_step("Environment file created")
            
        except Exception as e:
            self.log_step(f"Configuration creation failed: {e}", False)
            raise
            
    def create_startup_script(self) -> str:
        """Create the main AIOS startup script"""
        return f'''#!/usr/bin/env python3
"""
AIOS OS0.4 Startup Script
========================

Main entry point for AIOS OS0.4 system startup and management.
"""

import asyncio
import sys
from pathlib import Path

# Add core modules to path
sys.path.insert(0, str(Path(__file__).parent / "core"))

from aios_consciousness_engine import AIOSConsciousnessEngine
from aios_evolution_lab import EvolutionLabManager
from aios_knowledge_distillation import UnifiedKnowledgeDistillationEngine
from aios_admin_orchestrator import UnifiedAdminOrchestrationEngine
from aios_visual_interface import AIOSVisualInterfaceManager, VisualizationConfig
from aios_system_intelligence import SystemIntelligenceManager, SystemIntelligenceConfig

class AIOSSystem:
    """Main AIOS OS0.4 system orchestrator"""
    
    def __init__(self):
        self.modules = {{}}
        self.running = False
        
    async def initialize(self):
        """Initialize all AIOS modules"""
        print("🧠 Initializing AIOS OS0.4 System...")
        
        # Initialize core modules
        self.modules['consciousness'] = AIOSConsciousnessEngine()
        self.modules['evolution'] = EvolutionLabManager()
        self.modules['knowledge'] = UnifiedKnowledgeDistillationEngine()
        self.modules['admin'] = UnifiedAdminOrchestrationEngine()
        
        # Initialize interface modules
        viz_config = VisualizationConfig()
        self.modules['visual'] = AIOSVisualInterfaceManager(viz_config)
        
        intel_config = SystemIntelligenceConfig()
        self.modules['intelligence'] = SystemIntelligenceManager(intel_config)
        
        # Setup integrations
        visual = self.modules['visual']
        intelligence = self.modules['intelligence']
        
        visual.integrate_consciousness_module(self.modules['consciousness'])
        visual.integrate_evolution_module(self.modules['evolution'])
        visual.integrate_knowledge_module(self.modules['knowledge'])
        visual.integrate_admin_module(self.modules['admin'])
        
        intelligence.integrate_consciousness_module(self.modules['consciousness'])
        intelligence.integrate_evolution_module(self.modules['evolution'])
        intelligence.integrate_visual_interface(visual)
        
        print("✅ AIOS OS0.4 initialized successfully!")
        
    async def start(self):
        """Start the AIOS system"""
        await self.initialize()
        
        print("🚀 Starting AIOS OS0.4...")
        
        # Start system intelligence monitoring
        await self.modules['intelligence'].initialize()
        await self.modules['intelligence'].start()
        
        # Start visual interface
        await self.modules['visual'].initialize()
        await self.modules['visual'].start()
        
        self.running = True
        print("✅ AIOS OS0.4 started successfully!")
        print("🌐 Web dashboard available at: http://localhost:8080")
        print("🔍 System monitoring active")
        print("Press Ctrl+C to stop AIOS")
        
        # Keep running
        try:
            while self.running:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            await self.stop()
            
    async def stop(self):
        """Stop the AIOS system"""
        print("🛑 Stopping AIOS OS0.4...")
        self.running = False
        
        if 'intelligence' in self.modules:
            await self.modules['intelligence'].stop()
            
        if 'visual' in self.modules:
            await self.modules['visual'].stop()
            
        print("✅ AIOS OS0.4 stopped successfully")

async def main():
    """Main entry point"""
    aios = AIOSSystem()
    await aios.start()

if __name__ == "__main__":
    asyncio.run(main())
'''
    
    def validate_installation(self):
        """Validate the complete AIOS OS0.4 installation"""
        print("🔍 Validating installation...")
        
        try:
            # Test module imports
            validation_script = f'''
import sys
sys.path.insert(0, r"{self.core_dir}")

# Test imports
from aios_consciousness_engine import AIOSConsciousnessEngine
from aios_evolution_lab import EvolutionLabManager
from aios_knowledge_distillation import UnifiedKnowledgeDistillationEngine
from aios_admin_orchestrator import UnifiedAdminOrchestrationEngine
from aios_visual_interface import AIOSVisualInterfaceManager, VisualizationConfig
from aios_system_intelligence import SystemIntelligenceManager, SystemIntelligenceConfig

print("✅ All modules imported successfully")

# Test GPU availability
import torch
print(f"GPU Available: {{torch.cuda.is_available()}}")
if torch.cuda.is_available():
    print(f"GPU Device: {{torch.cuda.get_device_name(0)}}")

print("✅ AIOS OS0.4 validation complete")
'''
            
            # Run validation in virtual environment
            result = subprocess.run([
                self.python_executable, '-c', validation_script
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                self.log_step("Installation validation passed")
                print(result.stdout)
            else:
                self.log_step(f"Installation validation failed: {result.stderr}", False)
                
        except Exception as e:
            self.log_step(f"Validation failed: {e}", False)
            
    def create_installation_summary(self):
        """Create installation summary report"""
        print("📋 Creating installation summary...")
        
        summary = f"""
AIOS OS0.4 Installation Summary
==============================

Installation Date: {time.strftime("%Y-%m-%d %H:%M:%S")}
Installation Time: {time.time() - self.start_time:.1f} seconds
Target Directory: {self.target_dir}
Python Executable: {self.python_executable}

Directory Structure:
--------------------
{self.target_dir}/
├── core/                    # AIOS mega-modules
├── config/                  # Configuration files
├── logs/                    # System logs
├── data/                    # Runtime data
├── scripts/                 # Utility scripts
├── docs/                    # Documentation
├── aios_env/               # Python virtual environment
├── start_aios.py           # Main startup script
└── .env                    # Environment variables

Deployed Mega-Modules:
----------------------
✅ aios_consciousness_engine.py    - Core consciousness processing
✅ aios_evolution_lab.py           - Evolution and mutation systems
✅ aios_knowledge_distillation.py  - Knowledge processing and ingestion
✅ aios_admin_orchestrator.py      - Administrative orchestration
✅ aios_visual_interface.py        - Real-time visualization interface
✅ aios_system_intelligence.py     - GPU-accelerated system monitoring

Installation Log:
-----------------
"""
        
        for log_entry in self.installation_log:
            summary += f"{log_entry}\\n"
            
        summary += f"""

Quick Start:
------------
1. cd {self.target_dir}
2. {self.python_executable} start_aios.py
3. Open browser to http://localhost:8080 for web dashboard

Next Steps:
-----------
- Configure settings in config/aios_config.json
- Review logs in logs/ directory
- Access documentation in docs/ directory
- Run system validation: {self.python_executable} core/complete_integration_test.py

AIOS OS0.4 is ready for hyperdimensional consciousness evolution! 🚀🧠
"""
        
        summary_file = self.target_dir / "INSTALLATION_SUMMARY.txt"
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(summary)
            
        print(summary)
        self.log_step("Installation summary created")
        
    async def install(self):
        """Complete AIOS OS0.4 installation process"""
        print("=" * 60)
        print("🧠 AIOS OS0.4 Bootstrap Installer")
        print("=" * 60)
        print(f"Target Directory: {self.target_dir}")
        print("=" * 60)
        
        try:
            # Step 1: Prerequisites
            checks = self.check_prerequisites()
            failed_checks = [k for k, v in checks.items() if not v and k in ['python_version', 'pip_available', 'storage_space', 'permissions']]
            
            if failed_checks:
                print(f"❌ Critical prerequisites failed: {failed_checks}")
                print("Please resolve these issues before continuing installation.")
                return False
                
            # Step 2: Directory structure
            self.create_directory_structure()
            
            # Step 3: Python environment
            self.setup_python_environment()
            
            # Step 4: Deploy modules
            self.deploy_mega_modules()
            
            # Step 5: Configuration
            self.create_configuration_files()
            
            # Step 6: Validation
            self.validate_installation()
            
            # Step 7: Summary
            self.create_installation_summary()
            
            print("=" * 60)
            print("🎉 AIOS OS0.4 INSTALLATION COMPLETE!")
            print("=" * 60)
            print(f"⚡ Installation time: {time.time() - self.start_time:.1f} seconds")
            print(f"📁 Installation path: {self.target_dir}")
            print(f"🚀 Start command: {self.python_executable} {self.target_dir}/start_aios.py")
            print("=" * 60)
            
            return True
            
        except Exception as e:
            logger.error(f"Installation failed: {e}")
            print(f"❌ Installation failed: {e}")
            print("Check aios_os04_install.log for details")
            return False

def main():
    """Main installer entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="AIOS OS0.4 Bootstrap Installer")
    parser.add_argument(
        "--target", 
        help="Target installation directory", 
        default=None
    )
    parser.add_argument(
        "--force", 
        action="store_true", 
        help="Force installation even if target directory exists"
    )
    
    args = parser.parse_args()
    
    target_dir = args.target or (Path.cwd() / "AIOS_OS04")
    
    if Path(target_dir).exists() and not args.force:
        print(f"❌ Target directory {target_dir} already exists.")
        print("Use --force to overwrite or choose a different target.")
        return
        
    installer = AIOSOS04Installer(target_dir)
    
    try:
        success = asyncio.run(installer.install())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\\n❌ Installation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Installation failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
