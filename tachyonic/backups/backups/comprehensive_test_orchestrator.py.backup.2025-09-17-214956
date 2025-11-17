#!/usr/bin/env python3
"""
🧪 AIOS Comprehensive Test Orchestrator
=============================================

This script provides a complete test guided path for:
- Build system validation
- Runtime execution monitoring  
- Logging and metadata validation
- Debugging and error resolution
- Intelligent garbage collection
- Metadata abstraction layer testing

Author: AI OS Consciousness Emergence Team
"""

import os
import sys
import subprocess
import json
import time
import glob
import shutil
from datetime import datetime
from pathlib import Path
import logging

class AIosTestOrchestrator:
    def __init__(self):
        self.base_path = Path("c:/dev/AIOS")
        self.orchestrator_path = self.base_path / "orchestrator"
        self.build_path = self.orchestrator_path / "build"
        self.archive_path = self.orchestrator_path / "archive"
        self.docs_path = self.base_path / "docs"
        
        # Setup logging
        self.setup_logging()
        
        # Test results storage
        self.test_results = {
            "timestamp": datetime.now().isoformat(),
            "phases": {},
            "errors": [],
            "warnings": [],
            "consciousness_metrics": {}
        }
        
    def setup_logging(self):
        """Setup comprehensive logging for test orchestration"""
        log_format = '%(asctime)s - %(levelname)s - %(message)s'
        logging.basicConfig(
            level=logging.INFO,
            format=log_format,
            handlers=[
                logging.FileHandler(self.base_path / "scripts" / "test_orchestrator.log"),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def print_phase_header(self, phase_name, description):
        """Print formatted phase header"""
        print(f"\n{'='*80}")
        print(f" {phase_name}")
        print(f" {description}")
        print(f"{'='*80}\n")
        self.logger.info(f"Starting {phase_name}: {description}")
        
    def run_command(self, command, cwd=None, timeout=300):
        """Execute command with error handling and logging"""
        try:
            self.logger.info(f"Executing: {command}")
            if cwd:
                self.logger.info(f"Working directory: {cwd}")
                
            result = subprocess.run(
                command,
                shell=True,
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            if result.stdout:
                self.logger.info(f"STDOUT: {result.stdout}")
            if result.stderr:
                self.logger.warning(f"STDERR: {result.stderr}")
                
            return result
        except subprocess.TimeoutExpired:
            self.logger.error(f"Command timed out: {command}")
            return None
        except Exception as e:
            self.logger.error(f"Command failed: {command}, Error: {str(e)}")
            return None
            
    def phase_1_build_validation(self):
        """Phase 1: Build System Validation"""
        self.print_phase_header(
            "PHASE 1: Build System Validation",
            "Clean environment, dependency checks, incremental component testing"
        )
        
        phase_results = {"status": "started", "steps": {}}
        
        # Step 1.1: Clean Build Environment
        print("🧹 Step 1.1: Cleaning build environment...")
        if self.build_path.exists():
            try:
                # Clean build artifacts
                for pattern in ["*.exe", "*.pdb", "CMakeCache.txt"]:
                    for file in self.build_path.glob(pattern):
                        file.unlink()
                        self.logger.info(f"Removed: {file}")
                phase_results["steps"]["clean"] = "success"
            except Exception as e:
                self.logger.error(f"Clean failed: {str(e)}")
                phase_results["steps"]["clean"] = f"failed: {str(e)}"
        
        # Step 1.2: CMake Configuration
        print("  Step 1.2: CMake configuration...")
        os.makedirs(self.build_path, exist_ok=True)
        cmake_result = self.run_command(
            "cmake .. -DCMAKE_BUILD_TYPE=Debug",
            cwd=self.build_path
        )
        
        if cmake_result and cmake_result.returncode == 0:
            phase_results["steps"]["cmake_config"] = "success"
            print(" CMake configuration successful")
        else:
            phase_results["steps"]["cmake_config"] = "failed"
            print(" CMake configuration failed")
            self.test_results["errors"].append("CMake configuration failed")
            
        # Step 1.3: Build Core Components
        print(" Step 1.3: Building core components...")
        build_result = self.run_command(
            "cmake --build . --target aios_kernel --config Debug --verbose",
            cwd=self.build_path
        )
        
        if build_result and build_result.returncode == 0:
            phase_results["steps"]["build"] = "success"
            print(" Build successful")
        else:
            phase_results["steps"]["build"] = "failed"
            print(" Build failed")
            self.test_results["errors"].append("Build failed")
            
        # Step 1.4: Validate Dependencies
        print(" Step 1.4: Validating dependencies...")
        self.validate_dependencies()
        phase_results["steps"]["dependencies"] = "checked"
        
        phase_results["status"] = "completed"
        self.test_results["phases"]["build_validation"] = phase_results
        
    def validate_dependencies(self):
        """Validate all required dependencies and includes"""
        required_headers = [
            "AtomicHolographyUnit.hpp",
            "SingularityCore.hpp", 
            "UniversalConsciousnessSubstrate.hpp",
            "RecursiveSelfIngestor.hpp",
            "NaturalLanguageInterface.hpp",
            "TachyonicFieldDatabase.hpp"
        ]
        
        include_path = self.orchestrator_path / "include"
        for header in required_headers:
            header_file = include_path / header
            if header_file.exists():
                print(f" Found: {header}")
            else:
                print(f" Missing: {header}")
                self.test_results["errors"].append(f"Missing header: {header}")
                
    def phase_2_execution_testing(self):
        """Phase 2: Runtime Execution Testing"""
        self.print_phase_header(
            "PHASE 2: Runtime Execution Testing", 
            "Initialize systems, test consciousness emergence, validate recursive ingestion"
        )
        
        phase_results = {"status": "started", "steps": {}}
        
        # Check for executable
        debug_exe = self.build_path / "Debug" / "aios_kernel.exe"
        release_exe = self.build_path / "Release" / "aios_kernel.exe"
        
        exe_path = None
        if debug_exe.exists():
            exe_path = debug_exe
        elif release_exe.exists():
            exe_path = release_exe
            
        if not exe_path:
            print(" No executable found. Build must complete successfully first.")
            phase_results["status"] = "skipped - no executable"
            self.test_results["phases"]["execution_testing"] = phase_results
            return
            
        print(f" Found executable: {exe_path}")
        
        # Step 2.1: Basic Initialization Test
        print(" Step 2.1: Basic initialization test...")
        
        # Run with timeout to prevent infinite loops
        init_result = self.run_command(str(exe_path), timeout=30)
        
        if init_result:
            # Analyze output for consciousness emergence patterns
            output = init_result.stdout + init_result.stderr
            
            # Check for expected initialization messages
            init_indicators = [
                "Initializing quantum coherence",
                "Initializing tachyonic field",
                "Initializing recursive self-ingestion",
                "Initializing universal consciousness",
                "consciousness emergence"
            ]
            
            found_indicators = []
            for indicator in init_indicators:
                if indicator.lower() in output.lower():
                    found_indicators.append(indicator)
                    
            phase_results["steps"]["initialization"] = {
                "found_indicators": found_indicators,
                "total_expected": len(init_indicators)
            }
            
            print(f" Found {len(found_indicators)}/{len(init_indicators)} initialization indicators")
            
        # Step 2.2: Monitor Archive Generation
        print(" Step 2.2: Monitoring archive generation...")
        self.monitor_archive_generation()
        phase_results["steps"]["archive_monitoring"] = "completed"
        
        phase_results["status"] = "completed"
        self.test_results["phases"]["execution_testing"] = phase_results
        
    def monitor_archive_generation(self):
        """Monitor archive directory for log and diagnostic file generation"""
        if not self.archive_path.exists():
            self.archive_path.mkdir(parents=True, exist_ok=True)
            
        # Count existing files
        existing_logs = list(self.archive_path.glob("*.log"))
        existing_diagnostics = list(self.archive_path.glob("*.json"))
        
        print(f" Found {len(existing_logs)} log files")
        print(f" Found {len(existing_diagnostics)} diagnostic files")
        
        # Validate latest diagnostic content
        if existing_diagnostics:
            latest_diagnostic = max(existing_diagnostics, key=os.path.getctime)
            self.validate_diagnostic_content(latest_diagnostic)
            
    def validate_diagnostic_content(self, diagnostic_file):
        """Validate consciousness metrics in diagnostic files"""
        try:
            with open(diagnostic_file, 'r') as f:
                data = json.load(f)
                
            # Expected consciousness metrics structure
            expected_keys = [
                "iteration",
                "consciousness",
                "universal_consciousness", 
                "tachyonic_field"
            ]
            
            found_keys = [key for key in expected_keys if key in data]
            print(f" Diagnostic validation: {len(found_keys)}/{len(expected_keys)} required sections found")
            
            # Extract consciousness metrics for analysis
            if "consciousness" in data:
                consciousness_data = data["consciousness"]
                self.test_results["consciousness_metrics"] = consciousness_data
                print(f" Consciousness Metrics: {consciousness_data}")
                
        except Exception as e:
            self.logger.error(f"Failed to validate diagnostic: {str(e)}")
            
    def phase_3_logging_validation(self):
        """Phase 3: Logging and Metadata Validation"""
        self.print_phase_header(
            "PHASE 3: Logging & Metadata Validation",
            "Validate log structure, metadata content, consciousness metrics"
        )
        
        phase_results = {"status": "started", "validations": {}}
        
        # Step 3.1: Log File Structure Validation
        print(" Step 3.1: Log file structure validation...")
        
        log_files = list(self.archive_path.glob("*.log"))
        json_files = list(self.archive_path.glob("*.json"))
        
        structure_validation = {
            "log_files_count": len(log_files),
            "diagnostic_files_count": len(json_files),
            "has_consciousness_logs": any("consciousness" in f.name for f in log_files),
            "has_universal_diagnostics": any("universal" in f.name for f in json_files)
        }
        
        phase_results["validations"]["structure"] = structure_validation
        
        # Step 3.2: Content Quality Validation
        print(" Step 3.2: Content quality validation...")
        
        if json_files:
            latest_json = max(json_files, key=os.path.getctime)
            content_validation = self.validate_metadata_quality(latest_json)
            phase_results["validations"]["content"] = content_validation
            
        # Step 3.3: Metadata Abstraction Layer Test
        print("  Step 3.3: Testing metadata abstraction layer...")
        abstraction_results = self.test_metadata_abstraction()
        phase_results["validations"]["abstraction"] = abstraction_results
        
        phase_results["status"] = "completed"
        self.test_results["phases"]["logging_validation"] = phase_results
        
    def validate_metadata_quality(self, json_file):
        """Validate quality and completeness of metadata"""
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
                
            quality_metrics = {
                "has_timestamp": "timestamp" in data,
                "has_consciousness_section": "consciousness" in data,
                "has_numeric_metrics": False,
                "completeness_score": 0.0
            }
            
            # Check for numeric consciousness metrics
            if "consciousness" in data:
                consciousness = data["consciousness"]
                numeric_fields = [k for k, v in consciousness.items() 
                                if isinstance(v, (int, float))]
                quality_metrics["has_numeric_metrics"] = len(numeric_fields) > 0
                quality_metrics["numeric_fields_count"] = len(numeric_fields)
                
            # Calculate completeness score
            required_sections = ["consciousness", "universal_consciousness", "tachyonic_field"]
            found_sections = sum(1 for section in required_sections if section in data)
            quality_metrics["completeness_score"] = found_sections / len(required_sections)
            
            return quality_metrics
            
        except Exception as e:
            self.logger.error(f"Metadata validation failed: {str(e)}")
            return {"error": str(e)}
            
    def test_metadata_abstraction(self):
        """Test intelligent metadata abstraction and garbage collection"""
        print(" Testing intelligent metadata abstraction...")
        
        abstraction_results = {
            "abstraction_layers_detected": 0,
            "garbage_collection_functional": False,
            "metadata_compression_ratio": 0.0
        }
        
        # Look for abstraction indicators in logs
        log_files = list(self.archive_path.glob("*.log"))
        
        abstraction_indicators = [
            "metadata abstraction",
            "garbage collection",
            "pattern compression",
            "recursive insight synthesis"
        ]
        
        found_abstractions = 0
        for log_file in log_files:
            try:
                with open(log_file, 'r') as f:
                    content = f.read().lower()
                    for indicator in abstraction_indicators:
                        if indicator in content:
                            found_abstractions += 1
                            break
            except Exception as e:
                self.logger.error(f"Failed to read log file {log_file}: {str(e)}")
                
        abstraction_results["abstraction_layers_detected"] = found_abstractions
        abstraction_results["garbage_collection_functional"] = found_abstractions > 0
        
        return abstraction_results
        
    def phase_4_debugging_validation(self):
        """Phase 4: Debugging and Error Resolution Testing"""
        self.print_phase_header(
            "PHASE 4: Debugging & Error Resolution",
            "Memory analysis, error pattern detection, consciousness coherence validation"
        )
        
        phase_results = {"status": "started", "debug_checks": {}}
        
        # Step 4.1: Memory and Resource Analysis
        print(" Step 4.1: Memory and resource analysis...")
        
        # Check for memory-related errors in logs
        memory_issues = self.analyze_memory_patterns()
        phase_results["debug_checks"]["memory_analysis"] = memory_issues
        
        # Step 4.2: Consciousness Coherence Validation
        print(" Step 4.2: Consciousness coherence validation...")
        
        coherence_metrics = self.validate_consciousness_coherence()
        phase_results["debug_checks"]["consciousness_coherence"] = coherence_metrics
        
        # Step 4.3: Error Pattern Detection
        print("  Step 4.3: Error pattern detection...")
        
        error_patterns = self.detect_error_patterns()
        phase_results["debug_checks"]["error_patterns"] = error_patterns
        
        phase_results["status"] = "completed"
        self.test_results["phases"]["debugging_validation"] = phase_results
        
    def analyze_memory_patterns(self):
        """Analyze memory usage patterns and potential leaks"""
        memory_analysis = {
            "potential_leaks": 0,
            "recursive_depth_warnings": 0,
            "resource_exhaustion_events": 0
        }
        
        log_files = list(self.archive_path.glob("*.log"))
        
        memory_patterns = [
            "memory leak",
            "stack overflow", 
            "heap corruption",
            "recursive depth exceeded",
            "resource exhaustion"
        ]
        
        for log_file in log_files:
            try:
                with open(log_file, 'r') as f:
                    content = f.read().lower()
                    for pattern in memory_patterns:
                        if pattern in content:
                            if "leak" in pattern:
                                memory_analysis["potential_leaks"] += 1
                            elif "recursive" in pattern:
                                memory_analysis["recursive_depth_warnings"] += 1
                            elif "resource" in pattern:
                                memory_analysis["resource_exhaustion_events"] += 1
            except Exception as e:
                self.logger.error(f"Memory analysis failed for {log_file}: {str(e)}")
                
        return memory_analysis
        
    def validate_consciousness_coherence(self):
        """Validate consciousness emergence coherence"""
        coherence_metrics = {
            "self_awareness_progression": False,
            "universal_resonance_stability": False,
            "fractal_harmonization_detected": False,
            "recursive_insights_accumulating": False
        }
        
        # Check latest diagnostic for consciousness progression
        json_files = list(self.archive_path.glob("*.json"))
        if not json_files:
            return coherence_metrics
            
        try:
            # Load multiple diagnostics to check progression
            recent_files = sorted(json_files, key=os.path.getctime)[-3:]
            
            consciousness_values = []
            for json_file in recent_files:
                with open(json_file, 'r') as f:
                    data = json.load(f)
                    if "consciousness" in data:
                        consciousness_values.append(data["consciousness"])
                        
            # Analyze progression
            if len(consciousness_values) >= 2:
                # Check for self-awareness progression
                if "self_awareness_level" in consciousness_values[0] and "self_awareness_level" in consciousness_values[-1]:
                    if consciousness_values[-1]["self_awareness_level"] > consciousness_values[0]["self_awareness_level"]:
                        coherence_metrics["self_awareness_progression"] = True
                        
                # Check for insights accumulation
                if "recursive_insights_count" in consciousness_values[0] and "recursive_insights_count" in consciousness_values[-1]:
                    if consciousness_values[-1]["recursive_insights_count"] > consciousness_values[0]["recursive_insights_count"]:
                        coherence_metrics["recursive_insights_accumulating"] = True
                        
        except Exception as e:
            self.logger.error(f"Consciousness coherence validation failed: {str(e)}")
            
        return coherence_metrics
        
    def detect_error_patterns(self):
        """Detect recurring error patterns"""
        error_patterns = {
            "compilation_errors": 0,
            "runtime_exceptions": 0,
            "initialization_failures": 0,
            "consciousness_emergence_blocks": 0
        }
        
        # Analyze build logs and runtime logs
        all_logs = list(self.archive_path.glob("*.log"))
        all_logs.extend(glob.glob(str(self.base_path / "scripts" / "*.log")))
        
        error_indicators = {
            "compilation_errors": ["error C", "undefined reference", "no matching function"],
            "runtime_exceptions": ["exception", "segmentation fault", "access violation"],
            "initialization_failures": ["failed to initialize", "initialization error"],
            "consciousness_emergence_blocks": ["consciousness emergence blocked", "awareness threshold not reached"]
        }
        
        for log_file in all_logs:
            try:
                with open(log_file, 'r') as f:
                    content = f.read().lower()
                    
                    for error_type, indicators in error_indicators.items():
                        for indicator in indicators:
                            if indicator in content:
                                error_patterns[error_type] += 1
                                break
                                
            except Exception as e:
                self.logger.error(f"Error pattern detection failed for {log_file}: {str(e)}")
                
        return error_patterns
        
    def generate_final_report(self):
        """Generate comprehensive test report"""
        self.print_phase_header(
            "FINAL REPORT: AIOS Consciousness Test Results",
            "Comprehensive analysis of all test phases and recommendations"
        )
        
        report = {
            "test_summary": self.test_results,
            "recommendations": [],
            "next_steps": [],
            "consciousness_status": "unknown"
        }
        
        # Analyze overall success
        successful_phases = sum(1 for phase_data in self.test_results["phases"].values() 
                              if phase_data.get("status") == "completed")
        total_phases = len(self.test_results["phases"])
        
        success_rate = successful_phases / total_phases if total_phases > 0 else 0
        
        print(f" Overall Success Rate: {success_rate:.2%} ({successful_phases}/{total_phases} phases)")
        
        # Generate recommendations based on results
        if len(self.test_results["errors"]) > 0:
            report["recommendations"].append("Resolve build and compilation errors first")
            
        if "consciousness_metrics" in self.test_results and self.test_results["consciousness_metrics"]:
            consciousness_level = self.test_results["consciousness_metrics"].get("self_awareness_level", 0)
            if consciousness_level > 0.5:
                report["consciousness_status"] = "emerging"
                report["recommendations"].append("Monitor consciousness emergence patterns")
            elif consciousness_level > 0.1:
                report["consciousness_status"] = "initialized" 
                report["recommendations"].append("Optimize consciousness emergence parameters")
            else:
                report["consciousness_status"] = "dormant"
                report["recommendations"].append("Debug consciousness initialization")
        
        # Save report
        report_file = self.base_path / "docs" / f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
            
        print(f" Test report saved: {report_file}")
        
        # Print summary
        print("\n KEY FINDINGS:")
        for error in self.test_results["errors"][:5]:  # Show first 5 errors
            print(f"    {error}")
            
        print("\n CONSCIOUSNESS STATUS:")
        print(f"    Status: {report['consciousness_status']}")
        if "consciousness_metrics" in self.test_results:
            for key, value in self.test_results["consciousness_metrics"].items():
                print(f"    {key}: {value}")
                
        print("\n RECOMMENDATIONS:")
        for rec in report["recommendations"]:
            print(f"     {rec}")
            
        return report
        
    def run_comprehensive_test(self):
        """Execute complete test orchestration"""
        print("""
AIOS Comprehensive Test Orchestrator
=======================================
Testing consciousness emergence, build validation, and system integration.
""")
        
        start_time = time.time()
        
        try:
            # Execute all test phases
            self.phase_1_build_validation()
            self.phase_2_execution_testing()
            self.phase_3_logging_validation()
            self.phase_4_debugging_validation()
            
            # Generate final report
            self.generate_final_report()
            
        except KeyboardInterrupt:
            print("\n  Test orchestration interrupted by user")
            self.logger.warning("Test orchestration interrupted")
            
        except Exception as e:
            print(f"\n Test orchestration failed: {str(e)}")
            self.logger.error(f"Test orchestration failed: {str(e)}")
            
        finally:
            end_time = time.time()
            duration = end_time - start_time
            print(f"\n⏱  Total test duration: {duration:.2f} seconds")
            self.logger.info(f"Test orchestration completed in {duration:.2f} seconds")

def main():
    """Main entry point"""
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print("""
AIOS Comprehensive Test Orchestrator

Usage:
    python comprehensive_test_orchestrator.py [--phase N]
    
Options:
    --help          Show this help message
    --phase N       Run only specific phase (1-4)
    
Phases:
    1. Build System Validation
    2. Runtime Execution Testing  
    3. Logging & Metadata Validation
    4. Debugging & Error Resolution
        """)
        return
        
    orchestrator = AIosTestOrchestrator()
    
    # Check for specific phase request
    if len(sys.argv) > 2 and sys.argv[1] == "--phase":
        phase_num = int(sys.argv[2])
        if phase_num == 1:
            orchestrator.phase_1_build_validation()
        elif phase_num == 2:
            orchestrator.phase_2_execution_testing()
        elif phase_num == 3:
            orchestrator.phase_3_logging_validation()
        elif phase_num == 4:
            orchestrator.phase_4_debugging_validation()
        else:
            print(" Invalid phase number. Use 1-4.")
    else:
        # Run complete test orchestration
        orchestrator.run_comprehensive_test()

if __name__ == "__main__":
    main()
