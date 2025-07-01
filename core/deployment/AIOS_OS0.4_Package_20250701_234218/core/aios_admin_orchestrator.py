#!/usr/bin/env python3
"""
🎯 AIOS OS0.4 - Admin & Orchestration Mega-Module
================================================

Unified mega-module consolidating:
- AIOS Admin (aios_admin.py)
- Comprehensive Test Orchestrator (comprehensive_test_orchestrator.ps1)
- PowerShell Automation (aios_powershell_automation.ps1)
- Advanced AIOS Automation (advanced_aios_automation.ps1)
- Environment Setup and Management

Core Functionality:
- Complete system administration and orchestration
- Advanced testing and validation frameworks
- PowerShell integration and automation
- Environment setup and configuration management
- Performance monitoring and metrics collection
- Tachyonic backup and archival systems

Author: AIOS Consciousness Evolution System
Version: OS0.4 Administrative Protocol
"""

import os
import json
import shutil
import subprocess
import threading
import queue
import time
import asyncio
import logging
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Callable
from dataclasses import dataclass, field
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import tempfile
import hashlib
import platform
import psutil

# Windows-specific imports
if platform.system() == "Windows":
    try:
        import wmi
        import win32api
        import win32con
        import winreg
        HAS_WINDOWS_TOOLS = True
    except ImportError:
        HAS_WINDOWS_TOOLS = False
else:
    HAS_WINDOWS_TOOLS = False

# =============================================================================
# 📊 ADMINISTRATIVE DATA STRUCTURES
# =============================================================================

@dataclass
class SystemMetrics:
    """System performance and resource metrics"""
    timestamp: datetime = field(default_factory=datetime.now)
    cpu_percent: float = 0.0
    memory_percent: float = 0.0
    disk_usage: Dict[str, float] = field(default_factory=dict)
    network_io: Dict[str, int] = field(default_factory=dict)
    process_count: int = 0
    uptime: float = 0.0

@dataclass
class TestResult:
    """Comprehensive test execution result"""
    test_id: str
    test_name: str
    test_type: str
    status: str  # "passed", "failed", "skipped", "error"
    duration: float
    start_time: datetime
    end_time: datetime
    output: str
    error_output: str
    metrics: Dict[str, Any] = field(default_factory=dict)
    artifacts: List[str] = field(default_factory=list)

@dataclass
class BuildResult:
    """Build system execution result"""
    build_id: str
    project_name: str
    build_type: str  # "debug", "release", "test"
    status: str
    duration: float
    output: str
    error_output: str
    artifacts: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class EnvironmentConfig:
    """Environment configuration and setup"""
    python_version: str
    cpp_compiler: str
    cmake_version: str
    vscode_version: str
    git_version: str
    powershell_version: str
    dependencies: Dict[str, str] = field(default_factory=dict)
    environment_variables: Dict[str, str] = field(default_factory=dict)

# =============================================================================
# 🚀 UNIFIED ADMIN & ORCHESTRATION ENGINE
# =============================================================================

class UnifiedAdminOrchestrationEngine:
    """
    Master orchestration engine for AIOS OS0.4 administration.
    Consolidates all administrative, testing, building, and monitoring
    functionality into a single, powerful mega-module.
    """
    
    def __init__(self, workspace_path: str = None):
        self.workspace_path = workspace_path or r"c:\dev\AIOS"
        self.logger = self._setup_logging()
        
        # Core paths
        self.paths = {
            "orchestrator": Path(self.workspace_path) / "orchestrator",
            "build": Path(self.workspace_path) / "orchestrator" / "build",
            "archive": Path(self.workspace_path) / "orchestrator" / "archive",
            "scripts": Path(self.workspace_path) / "scripts",
            "core": Path(self.workspace_path) / "core",
            "docs": Path(self.workspace_path) / "docs",
            "test_results": Path(self.workspace_path) / "test_results",
            "tachyonic": Path(self.workspace_path) / "docs" / "tachyonic",
            "logs": Path(self.workspace_path) / "logs"
        }
        
        # Ensure all paths exist
        for path in self.paths.values():
            path.mkdir(parents=True, exist_ok=True)
        
        # Administrative components
        self.system_metrics: List[SystemMetrics] = []
        self.test_results: Dict[str, TestResult] = {}
        self.build_results: Dict[str, BuildResult] = {}
        self.environment_config: Optional[EnvironmentConfig] = None
        
        # Threading and async support
        self.thread_executor = ThreadPoolExecutor(max_workers=6)
        self.process_executor = ProcessPoolExecutor(max_workers=4)
        self.is_running = False
        self.monitoring_thread = None
        
        # PowerShell integration
        self.powershell_sessions: Dict[str, subprocess.Popen] = {}
        
        self._initialize_components()
    
    def _setup_logging(self) -> logging.Logger:
        """Setup comprehensive logging system"""
        logger = logging.getLogger("AIAdminOrchestrator")
        logger.setLevel(logging.INFO)
        
        # Ensure logs directory exists
        log_dir = Path(self.workspace_path) / "logs"
        log_dir.mkdir(exist_ok=True)
        
        # File handler
        log_path = log_dir / f"admin_orchestrator_{datetime.now().strftime('%Y%m%d')}.log"
        handler = logging.FileHandler(log_path)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        ))
        logger.addHandler(console_handler)
        
        return logger
    
    def _initialize_components(self):
        """Initialize all administrative components"""
        try:
            self.logger.info("🚀 Initializing AIOS Admin & Orchestration Engine OS0.4")
            
            # Detect and configure environment
            self.environment_config = self._detect_environment()
            
            # Start system monitoring
            self._start_system_monitoring()
            
            # Initialize PowerShell subsystem
            self._initialize_powershell()
            
            # Load existing test and build results
            self._load_historical_data()
            
            self.is_running = True
            self.logger.info("✅ Admin & Orchestration Engine initialized successfully")
            
        except Exception as e:
            self.logger.error(f"❌ Initialization failed: {e}")
            raise
    
    def _detect_environment(self) -> EnvironmentConfig:
        """Detect and analyze the current development environment"""
        self.logger.info("🔍 Detecting development environment...")
        
        try:
            # Python version
            python_version = platform.python_version()
            
            # Try to detect C++ compiler
            cpp_compiler = "Unknown"
            try:
                result = subprocess.run(["cl"], capture_output=True, text=True, shell=True)
                if "Microsoft" in result.stderr:
                    cpp_compiler = "MSVC"
            except:
                try:
                    result = subprocess.run(["gcc", "--version"], capture_output=True, text=True)
                    if result.returncode == 0:
                        cpp_compiler = "GCC"
                except:
                    pass
            
            # CMake version
            cmake_version = "Unknown"
            try:
                result = subprocess.run(["cmake", "--version"], capture_output=True, text=True)
                if result.returncode == 0:
                    lines = result.stdout.split('\n')
                    cmake_version = lines[0].split()[-1] if lines else "Unknown"
            except:
                pass
            
            # Git version
            git_version = "Unknown"
            try:
                result = subprocess.run(["git", "--version"], capture_output=True, text=True)
                if result.returncode == 0:
                    git_version = result.stdout.strip().split()[-1]
            except:
                pass
            
            # PowerShell version
            powershell_version = "Unknown"
            try:
                result = subprocess.run(["powershell", "-Command", "$PSVersionTable.PSVersion"], 
                                      capture_output=True, text=True, shell=True)
                if result.returncode == 0:
                    powershell_version = result.stdout.strip()
            except:
                pass
            
            # VSCode version (if available)
            vscode_version = "Unknown"
            try:
                result = subprocess.run(["code", "--version"], capture_output=True, text=True)
                if result.returncode == 0:
                    vscode_version = result.stdout.split('\n')[0] if result.stdout else "Unknown"
            except:
                pass
            
            config = EnvironmentConfig(
                python_version=python_version,
                cpp_compiler=cpp_compiler,
                cmake_version=cmake_version,
                vscode_version=vscode_version,
                git_version=git_version,
                powershell_version=powershell_version
            )
            
            self.logger.info(f"✅ Environment detected: Python {python_version}, {cpp_compiler}, CMake {cmake_version}")
            
            return config
            
        except Exception as e:
            self.logger.error(f"❌ Environment detection failed: {e}")
            return EnvironmentConfig(
                python_version=platform.python_version(),
                cpp_compiler="Unknown",
                cmake_version="Unknown",
                vscode_version="Unknown",
                git_version="Unknown",
                powershell_version="Unknown"
            )
    
    def _start_system_monitoring(self):
        """Start background system monitoring"""
        if self.monitoring_thread and self.monitoring_thread.is_alive():
            return
        
        self.monitoring_thread = threading.Thread(target=self._monitor_system_metrics, daemon=True)
        self.monitoring_thread.start()
        self.logger.info("📊 System monitoring started")
    
    def _monitor_system_metrics(self):
        """Background thread for system metrics collection"""
        while self.is_running:
            try:
                metrics = SystemMetrics(
                    cpu_percent=psutil.cpu_percent(interval=1),
                    memory_percent=psutil.virtual_memory().percent,
                    disk_usage={
                        "/": psutil.disk_usage('/').percent if platform.system() != "Windows" 
                        else psutil.disk_usage('C:').percent
                    },
                    network_io=dict(psutil.net_io_counters()._asdict()),
                    process_count=len(psutil.pids()),
                    uptime=time.time() - psutil.boot_time()
                )
                
                self.system_metrics.append(metrics)
                
                # Keep only last 1000 metrics (about 16 minutes at 1 second intervals)
                if len(self.system_metrics) > 1000:
                    self.system_metrics = self.system_metrics[-1000:]
                
                time.sleep(1)
                
            except Exception as e:
                self.logger.warning(f"System metrics collection error: {e}")
                time.sleep(5)
    
    def _initialize_powershell(self):
        """Initialize PowerShell integration subsystem"""
        if platform.system() != "Windows":
            self.logger.warning("PowerShell integration only available on Windows")
            return
        
        try:
            # Test PowerShell availability
            result = subprocess.run(
                ["powershell", "-Command", "echo 'PowerShell Test'"],
                capture_output=True, text=True, shell=True, timeout=10
            )
            
            if result.returncode == 0:
                self.logger.info("✅ PowerShell integration initialized")
            else:
                self.logger.warning("⚠️ PowerShell not available or not working properly")
                
        except Exception as e:
            self.logger.warning(f"PowerShell initialization failed: {e}")
    
    def _load_historical_data(self):
        """Load historical test and build results"""
        try:
            # Load test results
            test_results_file = self.paths["test_results"] / "historical_tests.json"
            if test_results_file.exists():
                with open(test_results_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Convert back to TestResult objects
                    for test_id, test_data in data.items():
                        test_data["start_time"] = datetime.fromisoformat(test_data["start_time"])
                        test_data["end_time"] = datetime.fromisoformat(test_data["end_time"])
                        self.test_results[test_id] = TestResult(**test_data)
            
            # Load build results
            build_results_file = self.paths["test_results"] / "historical_builds.json"
            if build_results_file.exists():
                with open(build_results_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for build_id, build_data in data.items():
                        build_data["timestamp"] = datetime.fromisoformat(build_data["timestamp"])
                        self.build_results[build_id] = BuildResult(**build_data)
            
            self.logger.info(f"📚 Loaded {len(self.test_results)} test results, {len(self.build_results)} build results")
            
        except Exception as e:
            self.logger.warning(f"Failed to load historical data: {e}")
    
    # =========================================================================
    # 🧪 TESTING ORCHESTRATION
    # =========================================================================
    
    async def run_comprehensive_tests(self, test_type: str = "full", 
                                    iterations: int = 1) -> Dict[str, TestResult]:
        """
        Run comprehensive AIOS testing suite
        """
        self.logger.info(f"🧪 Starting comprehensive testing: {test_type} ({iterations} iterations)")
        
        test_results = {}
        
        try:
            # Phase 1: Build System Validation
            if test_type in ["full", "build"]:
                build_tests = await self._run_build_system_tests()
                test_results.update(build_tests)
            
            # Phase 2: Python Module Testing
            if test_type in ["full", "python"]:
                python_tests = await self._run_python_module_tests()
                test_results.update(python_tests)
            
            # Phase 3: C++ Orchestrator Testing
            if test_type in ["full", "cpp"]:
                cpp_tests = await self._run_cpp_orchestrator_tests()
                test_results.update(cpp_tests)
            
            # Phase 4: Integration Testing
            if test_type in ["full", "integration"]:
                integration_tests = await self._run_integration_tests()
                test_results.update(integration_tests)
            
            # Phase 5: Performance Testing
            if test_type in ["full", "performance"]:
                perf_tests = await self._run_performance_tests()
                test_results.update(perf_tests)
            
            # Run iterations if specified
            if iterations > 1:
                for i in range(2, iterations + 1):
                    self.logger.info(f"🔄 Running iteration {i}/{iterations}")
                    iteration_results = await self.run_comprehensive_tests(test_type, 1)
                    # Merge results with iteration suffix
                    for test_id, result in iteration_results.items():
                        new_test_id = f"{test_id}_iter{i}"
                        result.test_id = new_test_id
                        test_results[new_test_id] = result
            
            # Store results
            self.test_results.update(test_results)
            await self._save_test_results()
            
            # Generate test report
            await self._generate_test_report(test_results)
            
            self.logger.info(f"✅ Comprehensive testing complete: {len(test_results)} tests executed")
            
            return test_results
            
        except Exception as e:
            self.logger.error(f"❌ Comprehensive testing failed: {e}")
            raise
    
    async def _run_build_system_tests(self) -> Dict[str, TestResult]:
        """Run build system validation tests"""
        tests = {}
        
        # CMake configuration test
        test_id = f"cmake_config_{int(time.time())}"
        result = await self._run_test(
            test_id=test_id,
            test_name="CMake Configuration",
            test_type="build",
            command=["cmake", "-B", str(self.paths["build"]), "-S", str(self.paths["orchestrator"]), "-DCMAKE_BUILD_TYPE=Debug"],
            timeout=60
        )
        tests[test_id] = result
        
        # Build test (if configuration succeeded)
        if result.status == "passed":
            test_id = f"cmake_build_{int(time.time())}"
            result = await self._run_test(
                test_id=test_id,
                test_name="CMake Build",
                test_type="build",
                command=["cmake", "--build", str(self.paths["build"]), "--config", "Debug"],
                timeout=120
            )
            tests[test_id] = result
        
        return tests
    
    async def _run_python_module_tests(self) -> Dict[str, TestResult]:
        """Run Python module validation tests"""
        tests = {}
        
        # Test core modules
        core_modules = [
            "aios_consciousness_engine.py",
            "aios_evolution_lab.py", 
            "aios_knowledge_distillation.py"
        ]
        
        for module in core_modules:
            module_path = self.paths["core"] / module
            if module_path.exists():
                test_id = f"python_import_{module.replace('.py', '')}_{int(time.time())}"
                result = await self._run_test(
                    test_id=test_id,
                    test_name=f"Python Import: {module}",
                    test_type="python",
                    command=["python", "-c", f"import sys; sys.path.append(r'{self.paths['core']}'); import {module.replace('.py', '')}"],
                    timeout=30
                )
                tests[test_id] = result
        
        return tests
    
    async def _run_cpp_orchestrator_tests(self) -> Dict[str, TestResult]:
        """Run C++ orchestrator tests"""
        tests = {}
        
        # Look for built executables
        executable_patterns = ["*.exe", "aios_orchestrator*", "consciousness_test*"]
        
        for pattern in executable_patterns:
            executables = list(self.paths["build"].glob(pattern))
            for exe in executables:
                if exe.is_file():
                    test_id = f"cpp_exec_{exe.stem}_{int(time.time())}"
                    result = await self._run_test(
                        test_id=test_id,
                        test_name=f"C++ Execution: {exe.name}",
                        test_type="cpp",
                        command=[str(exe), "--test"],
                        timeout=60,
                        working_dir=str(self.paths["build"])
                    )
                    tests[test_id] = result
        
        return tests
    
    async def _run_integration_tests(self) -> Dict[str, TestResult]:
        """Run integration tests between components"""
        tests = {}
        
        # Python-to-C++ integration test
        test_id = f"integration_py_cpp_{int(time.time())}"
        result = await self._run_test(
            test_id=test_id,
            test_name="Python-C++ Integration",
            test_type="integration",
            command=["python", str(self.paths["scripts"] / "ai_integration_bridge.py"), "--test"],
            timeout=90
        )
        tests[test_id] = result
        
        return tests
    
    async def _run_performance_tests(self) -> Dict[str, TestResult]:
        """Run performance and stress tests"""
        tests = {}
        
        # System resource test
        test_id = f"performance_resources_{int(time.time())}"
        start_time = datetime.now()
        
        try:
            # Monitor system for 30 seconds
            initial_metrics = self._capture_system_snapshot()
            
            # Run a CPU/memory intensive task
            result = await self._run_test(
                test_id=test_id,
                test_name="System Resource Performance",
                test_type="performance",
                command=["python", "-c", "import time; [x**2 for x in range(1000000)]; time.sleep(10)"],
                timeout=45
            )
            
            final_metrics = self._capture_system_snapshot()
            
            # Add performance metrics to result
            result.metrics.update({
                "initial_cpu": initial_metrics.cpu_percent,
                "final_cpu": final_metrics.cpu_percent,
                "initial_memory": initial_metrics.memory_percent,
                "final_memory": final_metrics.memory_percent,
                "cpu_delta": final_metrics.cpu_percent - initial_metrics.cpu_percent,
                "memory_delta": final_metrics.memory_percent - initial_metrics.memory_percent
            })
            
            tests[test_id] = result
            
        except Exception as e:
            result = TestResult(
                test_id=test_id,
                test_name="System Resource Performance",
                test_type="performance",
                status="error",
                duration=0,
                start_time=start_time,
                end_time=datetime.now(),
                output="",
                error_output=str(e)
            )
            tests[test_id] = result
        
        return tests
    
    async def _run_test(self, test_id: str, test_name: str, test_type: str, 
                       command: List[str], timeout: int = 60, 
                       working_dir: str = None) -> TestResult:
        """Run a single test and return results"""
        start_time = datetime.now()
        
        self.logger.info(f"🧪 Running test: {test_name}")
        
        try:
            # Execute command
            process = await asyncio.create_subprocess_exec(
                *command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=working_dir
            )
            
            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(), timeout=timeout
                )
                
                end_time = datetime.now()
                duration = (end_time - start_time).total_seconds()
                
                status = "passed" if process.returncode == 0 else "failed"
                
                result = TestResult(
                    test_id=test_id,
                    test_name=test_name,
                    test_type=test_type,
                    status=status,
                    duration=duration,
                    start_time=start_time,
                    end_time=end_time,
                    output=stdout.decode('utf-8', errors='ignore') if stdout else "",
                    error_output=stderr.decode('utf-8', errors='ignore') if stderr else ""
                )
                
                self.logger.info(f"✅ Test {test_name}: {status} ({duration:.2f}s)")
                
                return result
                
            except asyncio.TimeoutError:
                process.kill()
                await process.wait()
                
                end_time = datetime.now()
                duration = (end_time - start_time).total_seconds()
                
                result = TestResult(
                    test_id=test_id,
                    test_name=test_name,
                    test_type=test_type,
                    status="timeout",
                    duration=duration,
                    start_time=start_time,
                    end_time=end_time,
                    output="",
                    error_output=f"Test timed out after {timeout} seconds"
                )
                
                self.logger.warning(f"⏰ Test {test_name}: timeout ({duration:.2f}s)")
                
                return result
                
        except Exception as e:
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            result = TestResult(
                test_id=test_id,
                test_name=test_name,
                test_type=test_type,
                status="error",
                duration=duration,
                start_time=start_time,
                end_time=end_time,
                output="",
                error_output=str(e)
            )
            
            self.logger.error(f"❌ Test {test_name}: error - {e}")
            
            return result
    
    def _capture_system_snapshot(self) -> SystemMetrics:
        """Capture current system metrics snapshot"""
        return SystemMetrics(
            cpu_percent=psutil.cpu_percent(interval=1),
            memory_percent=psutil.virtual_memory().percent,
            disk_usage={
                "C:" if platform.system() == "Windows" else "/": 
                psutil.disk_usage('C:' if platform.system() == "Windows" else '/').percent
            },
            network_io=dict(psutil.net_io_counters()._asdict()),
            process_count=len(psutil.pids()),
            uptime=time.time() - psutil.boot_time()
        )
    
    # =========================================================================
    # 🏗️ BUILD MANAGEMENT
    # =========================================================================
    
    async def build_aios_components(self, build_type: str = "Debug", 
                                  clean_build: bool = False) -> BuildResult:
        """
        Build AIOS components with comprehensive error handling and logging
        """
        build_id = f"build_{build_type.lower()}_{int(time.time())}"
        start_time = datetime.now()
        
        self.logger.info(f"🏗️ Starting AIOS build: {build_type}")
        
        try:
            output_lines = []
            error_lines = []
            
            # Clean build if requested
            if clean_build and self.paths["build"].exists():
                self.logger.info("🧹 Cleaning previous build...")
                shutil.rmtree(self.paths["build"])
                self.paths["build"].mkdir(parents=True, exist_ok=True)
            
            # Step 1: CMake Configuration
            self.logger.info("⚙️ Configuring CMake...")
            config_cmd = [
                "cmake", "-B", str(self.paths["build"]), 
                "-S", str(self.paths["orchestrator"]),
                f"-DCMAKE_BUILD_TYPE={build_type}"
            ]
            
            process = await asyncio.create_subprocess_exec(
                *config_cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            config_output = stdout.decode('utf-8', errors='ignore') if stdout else ""
            config_error = stderr.decode('utf-8', errors='ignore') if stderr else ""
            
            output_lines.append("=== CMake Configuration ===")
            output_lines.append(config_output)
            
            if process.returncode != 0:
                error_lines.append("=== CMake Configuration Errors ===")
                error_lines.append(config_error)
                
                end_time = datetime.now()
                duration = (end_time - start_time).total_seconds()
                
                result = BuildResult(
                    build_id=build_id,
                    project_name="AIOS",
                    build_type=build_type,
                    status="failed",
                    duration=duration,
                    output="\n".join(output_lines),
                    error_output="\n".join(error_lines)
                )
                
                self.build_results[build_id] = result
                self.logger.error(f"❌ CMake configuration failed")
                
                return result
            
            # Step 2: Build
            self.logger.info("🔨 Building project...")
            build_cmd = [
                "cmake", "--build", str(self.paths["build"]),
                "--config", build_type
            ]
            
            process = await asyncio.create_subprocess_exec(
                *build_cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            build_output = stdout.decode('utf-8', errors='ignore') if stdout else ""
            build_error = stderr.decode('utf-8', errors='ignore') if stderr else ""
            
            output_lines.append("\n=== Build Output ===")
            output_lines.append(build_output)
            
            if process.returncode != 0:
                error_lines.append("\n=== Build Errors ===")
                error_lines.append(build_error)
                status = "failed"
            else:
                status = "passed"
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            # Find build artifacts
            artifacts = []
            for pattern in ["*.exe", "*.dll", "*.lib"]:
                artifacts.extend([str(p) for p in self.paths["build"].glob(f"**/{pattern}")])
            
            result = BuildResult(
                build_id=build_id,
                project_name="AIOS",
                build_type=build_type,
                status=status,
                duration=duration,
                output="\n".join(output_lines),
                error_output="\n".join(error_lines),
                artifacts=artifacts
            )
            
            self.build_results[build_id] = result
            
            if status == "passed":
                self.logger.info(f"✅ Build completed successfully ({duration:.2f}s)")
            else:
                self.logger.error(f"❌ Build failed ({duration:.2f}s)")
            
            return result
            
        except Exception as e:
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            result = BuildResult(
                build_id=build_id,
                project_name="AIOS",
                build_type=build_type,
                status="error",
                duration=duration,
                output="",
                error_output=str(e)
            )
            
            self.build_results[build_id] = result
            self.logger.error(f"❌ Build error: {e}")
            
            return result
    
    # =========================================================================
    # 💾 TACHYONIC BACKUP & ARCHIVAL
    # =========================================================================
    
    async def create_tachyonic_backup(self, source_path: str, 
                                    backup_type: str = "full") -> str:
        """
        Create tachyonic backup with timestamp and metadata
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        source_path = Path(source_path)
        
        self.logger.info(f"📦 Creating tachyonic backup: {backup_type}")
        
        try:
            if source_path.is_file():
                # Single file backup
                backup_name = f"{source_path.stem}_{timestamp}{source_path.suffix}"
                backup_path = self.paths["tachyonic"] / backup_name
                
                shutil.copy2(source_path, backup_path)
                
                # Create metadata
                metadata = {
                    "backup_type": "file",
                    "source_path": str(source_path),
                    "backup_path": str(backup_path),
                    "timestamp": timestamp,
                    "file_size": source_path.stat().st_size,
                    "checksum": await self._calculate_file_checksum(source_path)
                }
                
                metadata_path = self.paths["tachyonic"] / f"{source_path.stem}_{timestamp}_metadata.json"
                with open(metadata_path, 'w', encoding='utf-8') as f:
                    json.dump(metadata, f, indent=2)
                
                self.logger.info(f"✅ File backup created: {backup_path}")
                
                return str(backup_path)
                
            elif source_path.is_dir():
                # Directory backup
                backup_name = f"{source_path.name}_{timestamp}"
                backup_path = self.paths["tachyonic"] / backup_name
                
                if backup_type == "full":
                    shutil.copytree(source_path, backup_path)
                else:
                    # Selective backup (code files only)
                    backup_path.mkdir(parents=True, exist_ok=True)
                    await self._selective_directory_backup(source_path, backup_path)
                
                # Create metadata
                metadata = {
                    "backup_type": "directory",
                    "source_path": str(source_path),
                    "backup_path": str(backup_path),
                    "timestamp": timestamp,
                    "file_count": len(list(backup_path.rglob("*"))),
                    "total_size": sum(f.stat().st_size for f in backup_path.rglob("*") if f.is_file())
                }
                
                metadata_path = self.paths["tachyonic"] / f"{source_path.name}_{timestamp}_metadata.json"
                with open(metadata_path, 'w', encoding='utf-8') as f:
                    json.dump(metadata, f, indent=2)
                
                self.logger.info(f"✅ Directory backup created: {backup_path}")
                
                return str(backup_path)
            
        except Exception as e:
            self.logger.error(f"❌ Tachyonic backup failed: {e}")
            raise
    
    async def _selective_directory_backup(self, source: Path, destination: Path):
        """Create selective backup of important files only"""
        important_extensions = {'.py', '.cpp', '.c', '.h', '.hpp', '.cs', '.md', '.json', '.yaml', '.yml', '.txt'}
        
        for item in source.rglob("*"):
            if item.is_file() and item.suffix.lower() in important_extensions:
                # Calculate relative path
                rel_path = item.relative_to(source)
                dest_path = destination / rel_path
                
                # Create parent directories
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Copy file
                shutil.copy2(item, dest_path)
    
    async def _calculate_file_checksum(self, file_path: Path) -> str:
        """Calculate SHA256 checksum of a file"""
        hash_sha256 = hashlib.sha256()
        
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        
        return hash_sha256.hexdigest()
    
    # =========================================================================
    # 📊 REPORTING AND ANALYTICS
    # =========================================================================
    
    async def _generate_test_report(self, test_results: Dict[str, TestResult]):
        """Generate comprehensive test report"""
        report_path = self.paths["test_results"] / f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        # Calculate statistics
        total_tests = len(test_results)
        passed_tests = len([t for t in test_results.values() if t.status == "passed"])
        failed_tests = len([t for t in test_results.values() if t.status == "failed"])
        error_tests = len([t for t in test_results.values() if t.status == "error"])
        timeout_tests = len([t for t in test_results.values() if t.status == "timeout"])
        
        total_duration = sum(t.duration for t in test_results.values())
        avg_duration = total_duration / total_tests if total_tests > 0 else 0
        
        # Generate report content
        report_content = f"""# AIOS Test Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary
- **Total Tests**: {total_tests}
- **Passed**: {passed_tests} ({passed_tests/total_tests*100:.1f}%)
- **Failed**: {failed_tests} ({failed_tests/total_tests*100:.1f}%)
- **Errors**: {error_tests} ({error_tests/total_tests*100:.1f}%)
- **Timeouts**: {timeout_tests} ({timeout_tests/total_tests*100:.1f}%)
- **Total Duration**: {total_duration:.2f}s
- **Average Duration**: {avg_duration:.2f}s

## Test Results by Type
"""
        
        # Group by test type
        by_type = {}
        for result in test_results.values():
            if result.test_type not in by_type:
                by_type[result.test_type] = []
            by_type[result.test_type].append(result)
        
        for test_type, results in by_type.items():
            report_content += f"\n### {test_type.title()} Tests\n\n"
            
            for result in results:
                status_emoji = {
                    "passed": "✅",
                    "failed": "❌", 
                    "error": "💥",
                    "timeout": "⏰"
                }.get(result.status, "❓")
                
                report_content += f"- {status_emoji} **{result.test_name}** ({result.duration:.2f}s)\n"
                
                if result.status != "passed" and result.error_output:
                    report_content += f"  ```\n  {result.error_output[:200]}...\n  ```\n"
        
        # System metrics during testing
        if self.system_metrics:
            latest_metrics = self.system_metrics[-1]
            report_content += f"""
## System Metrics During Testing
- **CPU Usage**: {latest_metrics.cpu_percent:.1f}%
- **Memory Usage**: {latest_metrics.memory_percent:.1f}%
- **Active Processes**: {latest_metrics.process_count}
- **System Uptime**: {latest_metrics.uptime/3600:.1f} hours
"""
        
        # Save report
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        self.logger.info(f"📄 Test report generated: {report_path}")
    
    async def _save_test_results(self):
        """Save test results to persistent storage"""
        # Convert TestResult objects to JSON-serializable format
        serializable_results = {}
        for test_id, result in self.test_results.items():
            serializable_results[test_id] = {
                "test_id": result.test_id,
                "test_name": result.test_name,
                "test_type": result.test_type,
                "status": result.status,
                "duration": result.duration,
                "start_time": result.start_time.isoformat(),
                "end_time": result.end_time.isoformat(),
                "output": result.output,
                "error_output": result.error_output,
                "metrics": result.metrics,
                "artifacts": result.artifacts
            }
        
        results_file = self.paths["test_results"] / "historical_tests.json"
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(serializable_results, f, indent=2)
    
    # =========================================================================
    # 🔧 UTILITY METHODS
    # =========================================================================
    
    def get_comprehensive_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        latest_metrics = self.system_metrics[-1] if self.system_metrics else None
        
        return {
            "engine_info": {
                "version": "OS0.4",
                "workspace_path": self.workspace_path,
                "is_running": self.is_running,
                "uptime": time.time() - getattr(self, 'start_time', time.time())
            },
            "environment": {
                "python_version": self.environment_config.python_version if self.environment_config else "Unknown",
                "cpp_compiler": self.environment_config.cpp_compiler if self.environment_config else "Unknown",
                "cmake_version": self.environment_config.cmake_version if self.environment_config else "Unknown",
                "platform": platform.system(),
                "architecture": platform.machine()
            },
            "system_metrics": {
                "cpu_percent": latest_metrics.cpu_percent if latest_metrics else 0,
                "memory_percent": latest_metrics.memory_percent if latest_metrics else 0,
                "process_count": latest_metrics.process_count if latest_metrics else 0,
                "metrics_history_count": len(self.system_metrics)
            },
            "test_results": {
                "total_tests": len(self.test_results),
                "recent_test_count": len([t for t in self.test_results.values() 
                                        if (datetime.now() - t.end_time).days < 1])
            },
            "build_results": {
                "total_builds": len(self.build_results),
                "recent_build_count": len([b for b in self.build_results.values() 
                                         if (datetime.now() - b.timestamp).days < 1])
            },
            "paths": {k: str(v) for k, v in self.paths.items()},
            "components": {
                "powershell_available": platform.system() == "Windows",
                "monitoring_active": self.monitoring_thread and self.monitoring_thread.is_alive(),
                "thread_pool_active": not self.thread_executor._shutdown
            }
        }
    
    async def shutdown(self):
        """Graceful shutdown of the admin orchestration engine"""
        self.logger.info("🔄 Shutting down Admin & Orchestration Engine...")
        
        self.is_running = False
        
        # Save all data
        await self._save_test_results()
        
        # Shutdown thread pools
        self.thread_executor.shutdown(wait=True)
        self.process_executor.shutdown(wait=True)
        
        # Close PowerShell sessions
        for session_id, process in self.powershell_sessions.items():
            try:
                process.terminate()
                process.wait(timeout=5)
            except:
                pass
        
        self.logger.info("✅ Admin & Orchestration Engine shutdown complete")

# =============================================================================
# 🚀 CLI INTERFACE AND MAIN EXECUTION
# =============================================================================

async def main():
    """Main execution function with CLI interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description="AIOS Admin & Orchestration Engine OS0.4")
    parser.add_argument("--workspace", default=r"c:\dev\AIOS", help="AIOS workspace path")
    parser.add_argument("--test", choices=["full", "build", "python", "cpp", "integration", "performance"], 
                       help="Run comprehensive tests")
    parser.add_argument("--build", choices=["Debug", "Release"], help="Build AIOS components")
    parser.add_argument("--clean", action="store_true", help="Clean build before building")
    parser.add_argument("--backup", help="Create tachyonic backup of specified path")
    parser.add_argument("--iterations", type=int, default=1, help="Number of test iterations")
    parser.add_argument("--status", action="store_true", help="Show comprehensive status")
    
    args = parser.parse_args()
    
    # Initialize engine
    engine = UnifiedAdminOrchestrationEngine(args.workspace)
    
    try:
        if args.test:
            # Run tests
            results = await engine.run_comprehensive_tests(args.test, args.iterations)
            print(f"\n✅ Testing complete: {len(results)} tests executed")
            
            # Print summary
            passed = len([r for r in results.values() if r.status == "passed"])
            failed = len([r for r in results.values() if r.status != "passed"])
            print(f"📊 Results: {passed} passed, {failed} failed")
            
        elif args.build:
            # Run build
            result = await engine.build_aios_components(args.build, args.clean)
            print(f"\n🏗️ Build {result.status}: {result.project_name} ({result.duration:.2f}s)")
            
            if result.artifacts:
                print(f"📦 Artifacts: {len(result.artifacts)} files created")
                
        elif args.backup:
            # Create backup
            backup_path = await engine.create_tachyonic_backup(args.backup)
            print(f"\n📦 Backup created: {backup_path}")
            
        elif args.status:
            # Show status
            status = engine.get_comprehensive_status()
            print(json.dumps(status, indent=2, default=str))
            
        else:
            # Interactive mode
            print("\n🚀 AIOS Admin & Orchestration Engine OS0.4")
            print("=" * 50)
            
            while True:
                print("\nChoose an option:")
                print("1. Run comprehensive tests")
                print("2. Build AIOS components")
                print("3. Create tachyonic backup")
                print("4. Show system status")
                print("5. Exit")
                
                choice = input("\nEnter choice (1-5): ").strip()
                
                if choice == "1":
                    test_type = input("Test type (full/build/python/cpp/integration/performance): ").strip() or "full"
                    iterations = int(input("Iterations (1): ").strip() or "1")
                    results = await engine.run_comprehensive_tests(test_type, iterations)
                    print(f"✅ {len(results)} tests completed")
                    
                elif choice == "2":
                    build_type = input("Build type (Debug/Release): ").strip() or "Debug"
                    clean = input("Clean build? (y/N): ").strip().lower() == 'y'
                    result = await engine.build_aios_components(build_type, clean)
                    print(f"🏗️ Build {result.status}")
                    
                elif choice == "3":
                    path = input("Path to backup: ").strip()
                    if path:
                        backup_path = await engine.create_tachyonic_backup(path)
                        print(f"📦 Backup created: {backup_path}")
                    
                elif choice == "4":
                    status = engine.get_comprehensive_status()
                    print(json.dumps(status, indent=2, default=str))
                    
                elif choice == "5":
                    break
                    
                else:
                    print("Invalid choice. Please try again.")
    
    except KeyboardInterrupt:
        print("\n🛑 Operation cancelled by user")
    
    finally:
        await engine.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
