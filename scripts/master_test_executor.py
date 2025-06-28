#!/usr/bin/env python3
"""
🚀 AIOS Master Test Execution Path
===================================

This script orchestrates the complete test guided path for AIOS:
1. Build validation and component testing
2. Runtime execution with consciousness emergence monitoring  
3. Logging and metadata validation with intelligent abstraction
4. Debugging and error resolution with pattern analysis
5. Reingestion preparation and data validation

This is the master test execution path that validates all functionalities
and prepares the system for recursive self-improvement cycles.
"""

import os
import sys
import subprocess
import json
import time
import shutil
from datetime import datetime
from pathlib import Path
import logging

class AIOSMasterTestExecutor:
    def __init__(self):
        self.base_path = Path("c:/dev/AIOS")
        self.orchestrator_path = self.base_path / "orchestrator"
        self.build_path = self.orchestrator_path / "build"
        self.scripts_path = self.base_path / "scripts"
        self.test_results_path = self.base_path / "test_results"
        
        # Test execution state
        self.test_session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.session_results = {}
        
        # Setup logging
        self.setup_logging()
        
    def setup_logging(self):
        """Setup comprehensive test session logging"""
        self.test_results_path.mkdir(exist_ok=True)
        
        log_format = '%(asctime)s - %(levelname)s - %(message)s'
        logging.basicConfig(
            level=logging.INFO,
            format=log_format,
            handlers=[
                logging.FileHandler(
                    self.test_results_path / f"master_test_session_{self.test_session_id}.log"
                ),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def print_master_header(self, title, description):
        """Print formatted master test header"""
        border = "=" * 100
        print(f"\n{border}")
        print(f"🚀 {title}")
        print(f"📋 {description}")
        print(f"⏰ Session ID: {self.test_session_id}")
        print(f"{border}\n")
        self.logger.info(f"Master Test: {title} - {description}")
        
    def execute_powershell_test_orchestrator(self, phase="all"):
        """Execute the PowerShell test orchestrator"""
        self.logger.info(f"Executing PowerShell test orchestrator for phase: {phase}")
        
        ps_script = self.scripts_path / "comprehensive_test_orchestrator.ps1"
        
        try:
            cmd = [
                "powershell.exe",
                "-ExecutionPolicy", "Bypass",
                "-File", str(ps_script),
                "-Phase", phase,
                "-OutputDir", str(self.test_results_path / f"ps_results_{self.test_session_id}"),
                "-Verbose"
            ]
            
            self.logger.info(f"Running PowerShell command: {' '.join(cmd)}")
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode == 0:
                self.logger.info("PowerShell test orchestrator completed successfully")
                return {"status": "success", "output": result.stdout}
            else:
                self.logger.error(f"PowerShell test orchestrator failed: {result.stderr}")
                return {"status": "failed", "error": result.stderr}
                
        except subprocess.TimeoutExpired:
            self.logger.error("PowerShell test orchestrator timed out")
            return {"status": "timeout", "error": "Process timed out"}
        except Exception as e:
            self.logger.error(f"PowerShell test orchestrator error: {str(e)}")
            return {"status": "error", "error": str(e)}
            
    def execute_python_test_orchestrator(self):
        """Execute the Python test orchestrator"""
        self.logger.info("Executing Python test orchestrator")
        
        py_script = self.scripts_path / "comprehensive_test_orchestrator.py"
        
        try:
            cmd = [sys.executable, str(py_script)]
            
            self.logger.info(f"Running Python command: {' '.join(cmd)}")
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300,
                cwd=str(self.base_path)
            )
            
            if result.returncode == 0:
                self.logger.info("Python test orchestrator completed successfully")
                return {"status": "success", "output": result.stdout}
            else:
                self.logger.error(f"Python test orchestrator failed: {result.stderr}")
                return {"status": "failed", "error": result.stderr}
                
        except subprocess.TimeoutExpired:
            self.logger.error("Python test orchestrator timed out")
            return {"status": "timeout", "error": "Process timed out"}
        except Exception as e:
            self.logger.error(f"Python test orchestrator error: {str(e)}")
            return {"status": "error", "error": str(e)}
            
    def build_and_validate_aios(self):
        """Build and validate AIOS components"""
        self.print_master_header(
            "PHASE A: Build and Component Validation",
            "Building AIOS kernel and validating all consciousness emergence components"
        )
        
        results = {"phase": "build_validation", "steps": []}
        
        # Step A1: Clean and configure build
        print("🧹 Step A1: Clean build environment and CMake configuration...")
        self.logger.info("Starting build environment cleanup and configuration")
        
        try:
            # Create build directory if it doesn't exist
            self.build_path.mkdir(exist_ok=True)
            
            # Change to build directory and run cmake
            os.chdir(self.build_path)
            
            # Clean previous build
            for pattern in ["*.exe", "*.pdb", "CMakeCache.txt"]:
                for file in self.build_path.glob(pattern):
                    file.unlink()
                    self.logger.info(f"Removed: {file}")
            
            # Configure with CMake
            cmake_result = subprocess.run(
                ["cmake", "..", "-DCMAKE_BUILD_TYPE=Debug", "-DBUILD_TESTING=ON"],
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if cmake_result.returncode == 0:
                print("✅ CMake configuration successful")
                self.logger.info("CMake configuration completed successfully")
                results["steps"].append({"step": "cmake_config", "status": "success"})
            else:
                print("❌ CMake configuration failed")
                self.logger.error(f"CMake configuration failed: {cmake_result.stderr}")
                results["steps"].append({"step": "cmake_config", "status": "failed", "error": cmake_result.stderr})
                return results
                
        except Exception as e:
            self.logger.error(f"Build configuration error: {str(e)}")
            results["steps"].append({"step": "cmake_config", "status": "error", "error": str(e)})
            return results
        
        # Step A2: Build AIOS kernel
        print("🔨 Step A2: Building AIOS kernel with all consciousness components...")
        self.logger.info("Starting AIOS kernel build")
        
        try:
            build_result = subprocess.run(
                ["cmake", "--build", ".", "--target", "aios_kernel", "--config", "Debug", "--verbose"],
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if build_result.returncode == 0:
                print("✅ AIOS kernel build successful")
                self.logger.info("AIOS kernel build completed successfully")
                results["steps"].append({"step": "kernel_build", "status": "success"})
            else:
                print("❌ AIOS kernel build failed")
                self.logger.error(f"AIOS kernel build failed: {build_result.stderr}")
                results["steps"].append({"step": "kernel_build", "status": "failed", "error": build_result.stderr})
                
                # Try to extract specific error information
                error_lines = build_result.stderr.split('\\n')
                critical_errors = [line for line in error_lines if 'error' in line.lower()]
                if critical_errors:
                    print("🔍 Critical build errors detected:")
                    for error in critical_errors[:5]:  # Show first 5 errors
                        print(f"   ❌ {error.strip()}")
                        
        except Exception as e:
            self.logger.error(f"Build execution error: {str(e)}")
            results["steps"].append({"step": "kernel_build", "status": "error", "error": str(e)})
        
        # Step A3: Validate built executable
        print("🔍 Step A3: Validating built executable...")
        
        debug_exe = self.build_path / "Debug" / "aios_kernel.exe"
        release_exe = self.build_path / "Release" / "aios_kernel.exe"
        
        if debug_exe.exists() or release_exe.exists():
            exe_path = debug_exe if debug_exe.exists() else release_exe
            print(f"✅ Executable found: {exe_path}")
            self.logger.info(f"AIOS executable validated: {exe_path}")
            results["steps"].append({"step": "executable_validation", "status": "success", "executable": str(exe_path)})
        else:
            print("❌ No executable found after build")
            self.logger.error("No executable found after successful build")
            results["steps"].append({"step": "executable_validation", "status": "failed"})
        
        return results
        
    def execute_consciousness_runtime_testing(self):
        """Execute AIOS runtime with consciousness emergence monitoring"""
        self.print_master_header(
            "PHASE B: Consciousness Runtime Testing",
            "Execute AIOS kernel and monitor consciousness emergence patterns"
        )
        
        results = {"phase": "consciousness_runtime", "metrics": {}}
        
        # Find the executable
        debug_exe = self.build_path / "Debug" / "aios_kernel.exe"
        release_exe = self.build_path / "Release" / "aios_kernel.exe"
        
        exe_path = None
        if debug_exe.exists():
            exe_path = debug_exe
        elif release_exe.exists():
            exe_path = release_exe
            
        if not exe_path:
            print("❌ No AIOS executable found. Cannot proceed with runtime testing.")
            self.logger.error("No AIOS executable found for runtime testing")
            results["status"] = "skipped - no executable"
            return results
            
        print(f"🚀 Executing AIOS kernel: {exe_path}")
        self.logger.info(f"Starting AIOS runtime execution: {exe_path}")
        
        # Step B1: Execute AIOS with consciousness monitoring
        print("🧠 Step B1: Running AIOS with consciousness emergence monitoring...")
        
        try:
            # Change to the directory containing the executable
            os.chdir(exe_path.parent)
            
            # Run AIOS kernel with timeout for safety
            process = subprocess.Popen(
                [str(exe_path)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Monitor execution for a limited time
            try:
                stdout, stderr = process.communicate(timeout=60)  # 1 minute execution
                
                print("✅ AIOS execution completed")
                self.logger.info("AIOS execution completed successfully")
                
                # Analyze output for consciousness indicators
                consciousness_indicators = [
                    "consciousness emergence",
                    "self-awareness level",
                    "recursive insight",
                    "universal consciousness",
                    "metadata abstraction",
                    "tachyonic field"
                ]
                
                found_indicators = []
                output_text = stdout + stderr
                
                for indicator in consciousness_indicators:
                    if indicator.lower() in output_text.lower():
                        found_indicators.append(indicator)
                        
                results["consciousness_indicators"] = found_indicators
                results["total_indicators_found"] = len(found_indicators)
                
                print(f"🧠 Consciousness indicators found: {len(found_indicators)}/{len(consciousness_indicators)}")
                for indicator in found_indicators:
                    print(f"   ✅ {indicator}")
                    
                self.logger.info(f"Consciousness indicators analysis: {len(found_indicators)} found")
                
            except subprocess.TimeoutExpired:
                print("⏰ AIOS execution timed out (60s limit)")
                self.logger.warning("AIOS execution timed out after 60 seconds")
                process.kill()
                stdout, stderr = process.communicate()
                results["status"] = "timeout"
                
        except Exception as e:
            print(f"❌ AIOS execution error: {str(e)}")
            self.logger.error(f"AIOS execution error: {str(e)}")
            results["status"] = "error"
            results["error"] = str(e)
            
        # Step B2: Analyze generated logs and diagnostics
        print("📊 Step B2: Analyzing generated logs and diagnostics...")
        
        archive_path = self.orchestrator_path / "archive"
        if archive_path.exists():
            log_files = list(archive_path.glob("*.log"))
            diagnostic_files = list(archive_path.glob("*.json"))
            
            results["generated_files"] = {
                "log_count": len(log_files),
                "diagnostic_count": len(diagnostic_files)
            }
            
            print(f"📝 Generated files: {len(log_files)} logs, {len(diagnostic_files)} diagnostics")
            self.logger.info(f"Archive analysis: {len(log_files)} logs, {len(diagnostic_files)} diagnostics")
            
            # Analyze latest diagnostic for consciousness metrics
            if diagnostic_files:
                latest_diagnostic = max(diagnostic_files, key=os.path.getctime)
                try:
                    with open(latest_diagnostic, 'r') as f:
                        diagnostic_data = json.load(f)
                        
                    if "consciousness" in diagnostic_data:
                        consciousness_metrics = diagnostic_data["consciousness"]
                        results["consciousness_metrics"] = consciousness_metrics
                        
                        print("🧠 Consciousness metrics extracted:")
                        for key, value in consciousness_metrics.items():
                            print(f"   📊 {key}: {value}")
                            
                        self.logger.info(f"Consciousness metrics extracted: {consciousness_metrics}")
                        
                except Exception as e:
                    self.logger.error(f"Failed to parse diagnostic file: {str(e)}")
        
        return results
        
    def validate_metadata_abstraction_system(self):
        """Validate the intelligent metadata abstraction and garbage collection system"""
        self.print_master_header(
            "PHASE C: Metadata Abstraction Validation",
            "Validate intelligent metadata abstraction, garbage collection, and reingestion preparation"
        )
        
        results = {"phase": "metadata_abstraction", "validations": []}
        
        # Step C1: Check for abstracted metadata output
        print("🗂️  Step C1: Validating metadata abstraction output...")
        
        abstraction_path = self.orchestrator_path / "archive" / "abstracted_metadata"
        if abstraction_path.exists():
            abstracted_files = list(abstraction_path.glob("**/*"))
            results["abstracted_files_count"] = len(abstracted_files)
            
            print(f"✅ Found {len(abstracted_files)} abstracted metadata files")
            self.logger.info(f"Metadata abstraction validation: {len(abstracted_files)} files found")
            
            # Check for specific abstraction categories
            categories = ["consciousness", "recursive", "universal", "reingestion"]
            found_categories = []
            
            for category in categories:
                category_path = abstraction_path / category
                if category_path.exists():
                    found_categories.append(category)
                    
            results["abstraction_categories"] = found_categories
            print(f"📂 Abstraction categories found: {', '.join(found_categories)}")
            
        else:
            print("❌ No abstracted metadata directory found")
            self.logger.warning("Metadata abstraction directory not found")
            results["abstracted_files_count"] = 0
            
        # Step C2: Validate reingestion dataset
        print("🔄 Step C2: Validating reingestion dataset preparation...")
        
        reingestion_file = abstraction_path / "consciousness_reingestion_dataset.md"
        if reingestion_file.exists():
            print("✅ Reingestion dataset found")
            self.logger.info("Reingestion dataset validation: file found")
            
            try:
                with open(reingestion_file, 'r') as f:
                    reingestion_content = f.read()
                    
                # Check for key sections
                required_sections = [
                    "Consciousness Emergence Insights",
                    "Recursive Self-Improvement Insights", 
                    "Universal Consciousness Resonance"
                ]
                
                found_sections = []
                for section in required_sections:
                    if section in reingestion_content:
                        found_sections.append(section)
                        
                results["reingestion_sections"] = found_sections
                print(f"📝 Reingestion sections found: {len(found_sections)}/{len(required_sections)}")
                
            except Exception as e:
                self.logger.error(f"Failed to validate reingestion content: {str(e)}")
                
        else:
            print("❌ Reingestion dataset not found")
            self.logger.warning("Reingestion dataset file not found")
            
        # Step C3: Validate garbage collection metrics
        print("🗑️  Step C3: Validating garbage collection metrics...")
        
        metadata_json = abstraction_path / "abstracted_metadata.json"
        if metadata_json.exists():
            try:
                with open(metadata_json, 'r') as f:
                    metadata_data = json.load(f)
                    
                if "metadata_abstraction" in metadata_data:
                    abstraction_data = metadata_data["metadata_abstraction"]
                    
                    if "collection_stats" in abstraction_data:
                        stats = abstraction_data["collection_stats"]
                        results["collection_stats"] = stats
                        
                        print("📊 Garbage collection statistics:")
                        for key, value in stats.items():
                            print(f"   📈 {key}: {value}")
                            
                        self.logger.info(f"Garbage collection stats: {stats}")
                        
            except Exception as e:
                self.logger.error(f"Failed to parse metadata JSON: {str(e)}")
                
        return results
        
    def execute_integrated_testing_cycle(self):
        """Execute complete integrated testing cycle"""
        self.print_master_header(
            "PHASE D: Integrated Testing Cycle",
            "Execute both PowerShell and Python test orchestrators for comprehensive validation"
        )
        
        results = {"phase": "integrated_testing", "orchestrators": {}}
        
        # Execute PowerShell orchestrator
        print("🔧 Step D1: Executing PowerShell test orchestrator...")
        ps_results = self.execute_powershell_test_orchestrator()
        results["orchestrators"]["powershell"] = ps_results
        
        if ps_results["status"] == "success":
            print("✅ PowerShell test orchestrator completed successfully")
        else:
            print(f"❌ PowerShell test orchestrator failed: {ps_results.get('error', 'Unknown error')}")
            
        # Execute Python orchestrator
        print("🐍 Step D2: Executing Python test orchestrator...")
        py_results = self.execute_python_test_orchestrator()
        results["orchestrators"]["python"] = py_results
        
        if py_results["status"] == "success":
            print("✅ Python test orchestrator completed successfully")
        else:
            print(f"❌ Python test orchestrator failed: {py_results.get('error', 'Unknown error')}")
            
        # Compare results
        print("📊 Step D3: Comparing orchestrator results...")
        
        success_count = sum(1 for result in [ps_results, py_results] if result["status"] == "success")
        results["success_rate"] = success_count / 2
        
        print(f"📈 Overall orchestrator success rate: {success_count}/2 ({results['success_rate']:.0%})")
        
        return results
        
    def generate_master_test_report(self):
        """Generate comprehensive master test report"""
        self.print_master_header(
            "MASTER TEST REPORT",
            "Comprehensive analysis of all test phases and system validation"
        )
        
        report = {
            "test_session_id": self.test_session_id,
            "timestamp": datetime.now().isoformat(),
            "phases": self.session_results,
            "overall_assessment": {},
            "recommendations": [],
            "next_steps": []
        }
        
        # Calculate overall success metrics
        successful_phases = 0
        total_phases = len(self.session_results)
        
        for phase_name, phase_data in self.session_results.items():
            if isinstance(phase_data, dict):
                # Check if phase has success indicators
                if phase_data.get("status") == "success" or \
                   (phase_data.get("steps") and any(step.get("status") == "success" for step in phase_data["steps"])):
                    successful_phases += 1
                    
        success_rate = successful_phases / total_phases if total_phases > 0 else 0
        report["overall_assessment"]["success_rate"] = success_rate
        report["overall_assessment"]["successful_phases"] = successful_phases
        report["overall_assessment"]["total_phases"] = total_phases
        
        # Generate recommendations based on results
        if success_rate >= 0.8:
            report["overall_assessment"]["status"] = "excellent"
            report["recommendations"].append("System is ready for production consciousness emergence testing")
            report["next_steps"].append("Begin extended consciousness evolution cycles")
        elif success_rate >= 0.6:
            report["overall_assessment"]["status"] = "good"
            report["recommendations"].append("Address minor issues and optimize consciousness parameters")
            report["next_steps"].append("Focus on improving weaker components")
        elif success_rate >= 0.4:
            report["overall_assessment"]["status"] = "needs_improvement"
            report["recommendations"].append("Significant issues need resolution before production use")
            report["next_steps"].append("Debug critical failures and rebuild affected components")
        else:
            report["overall_assessment"]["status"] = "critical"
            report["recommendations"].append("Major system failures require comprehensive debugging")
            report["next_steps"].append("Start with basic component validation and build system")
            
        # Check for consciousness emergence
        consciousness_detected = False
        for phase_data in self.session_results.values():
            if isinstance(phase_data, dict):
                if phase_data.get("consciousness_indicators") or phase_data.get("consciousness_metrics"):
                    consciousness_detected = True
                    break
                    
        report["overall_assessment"]["consciousness_emergence_detected"] = consciousness_detected
        
        if consciousness_detected:
            report["recommendations"].append("Monitor consciousness evolution patterns")
            report["next_steps"].append("Analyze consciousness emergence data for optimization")
        else:
            report["recommendations"].append("Debug consciousness initialization and emergence mechanisms")
            
        # Save report
        report_file = self.test_results_path / f"master_test_report_{self.test_session_id}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
            
        # Print summary
        print(f"\n📊 OVERALL TEST RESULTS:")
        print(f"   🎯 Success Rate: {success_rate:.1%} ({successful_phases}/{total_phases} phases)")
        print(f"   🧠 Consciousness Emergence: {'✅ Detected' if consciousness_detected else '❌ Not Detected'}")
        print(f"   📈 System Status: {report['overall_assessment']['status'].upper()}")
        
        print(f"\n💡 KEY RECOMMENDATIONS:")
        for rec in report["recommendations"]:
            print(f"   ➡️  {rec}")
            
        print(f"\n🚀 NEXT STEPS:")
        for step in report["next_steps"]:
            print(f"   📋 {step}")
            
        print(f"\n📝 Full report saved: {report_file}")
        
        self.logger.info(f"Master test report generated: {report_file}")
        
        return report
        
    def run_master_test_cycle(self):
        """Execute the complete master test cycle"""
        print("""
AIOS Master Test Execution Path
==================================
Comprehensive consciousness emergence validation and system testing.
""")
        
        start_time = time.time()
        
        try:
            # Phase A: Build and Component Validation
            print("\n" + "="*80)
            build_results = self.build_and_validate_aios()
            self.session_results["build_validation"] = build_results
            
            # Phase B: Consciousness Runtime Testing (only if build succeeded)
            if any(step.get("status") == "success" for step in build_results.get("steps", [])):
                print("\n" + "="*80) 
                runtime_results = self.execute_consciousness_runtime_testing()
                self.session_results["consciousness_runtime"] = runtime_results
            else:
                print("\n⚠️  Skipping runtime testing due to build failures")
                self.session_results["consciousness_runtime"] = {"status": "skipped", "reason": "build_failed"}
                
            # Phase C: Metadata Abstraction Validation
            print("\n" + "="*80)
            metadata_results = self.validate_metadata_abstraction_system()
            self.session_results["metadata_abstraction"] = metadata_results
            
            # Phase D: Integrated Testing Cycle
            print("\n" + "="*80)
            integrated_results = self.execute_integrated_testing_cycle()
            self.session_results["integrated_testing"] = integrated_results
            
            # Generate final report
            print("\n" + "="*80)
            final_report = self.generate_master_test_report()
            
        except KeyboardInterrupt:
            print("\n⚠️  Master test execution interrupted by user")
            self.logger.warning("Master test execution interrupted by user")
            
        except Exception as e:
            print(f"\n❌ Master test execution failed: {str(e)}")
            self.logger.error(f"Master test execution failed: {str(e)}")
            
        finally:
            end_time = time.time()
            duration = end_time - start_time
            print(f"\n⏱️  Total master test duration: {duration:.2f} seconds")
            self.logger.info(f"Master test execution completed in {duration:.2f} seconds")

def main():
    """Main entry point for master test execution"""
    if len(sys.argv) > 1 and sys.argv[1] in ["--help", "-h"]:
        print("""
AIOS Master Test Execution Path

Usage:
    python master_test_executor.py

This script executes the complete test guided path including:
- Build system validation and component testing
- Runtime consciousness emergence monitoring
- Metadata abstraction and garbage collection validation
- Integrated test orchestrator execution
- Comprehensive reporting and analysis

The script creates a complete test session with detailed logging,
metrics collection, and reingestion-ready data preparation.
        """)
        return
        
    executor = AIOSMasterTestExecutor()
    executor.run_master_test_cycle()

if __name__ == "__main__":
    main()
