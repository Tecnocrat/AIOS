#!/usr/bin/env python3
"""
AIOS System Health Monitor & Context Validator
Comprehensive health check for AI systems working on AIOS
"""

import os
import sys
import json
import subprocess
import time
from pathlib import Path
from typing import Dict, List, Tuple, Optional

def supports_unicode():
    """Check if the current environment supports Unicode emojis"""
    try:
        # Try to encode a simple emoji
        '\u2705'.encode(sys.stdout.encoding or 'utf-8')
        return True
    except (UnicodeEncodeError, AttributeError):
        return False

# Set display characters based on environment capability
UNICODE_SUPPORT = supports_unicode()
STATUS_EXCELLENT = '\U0001F7E2 EXCELLENT' if UNICODE_SUPPORT else '>> EXCELLENT'
STATUS_HEALTHY = '\U0001F7E2 HEALTHY' if UNICODE_SUPPORT else '>> HEALTHY'
STATUS_GOOD = '\U0001F7E1 GOOD' if UNICODE_SUPPORT else '>> GOOD'
STATUS_DEGRADED = '\U0001F7E1 DEGRADED' if UNICODE_SUPPORT else '>> DEGRADED'
STATUS_CRITICAL = '\U0001F534 CRITICAL' if UNICODE_SUPPORT else '>> CRITICAL'
STATUS_FAILURE = '\U0001F534 SYSTEM FAILURE' if UNICODE_SUPPORT else '>> SYSTEM FAILURE'
ICON_ISSUES = '\U0001F6A8' if UNICODE_SUPPORT else '[!]'
ICON_WARNINGS = '\u26A0\uFE0F' if UNICODE_SUPPORT else '[W]'
ICON_RECOMMENDATIONS = '\U0001F4A1' if UNICODE_SUPPORT else '[R]'

class AIContextHealthMonitor:
    def __init__(self):
        self.project_root = Path("c:/dev/AIOS")
        self.health_score = 1.0
        self.issues = []
        self.warnings = []
        self.recommendations = []
        
    def calculate_context_health(self) -> float:
        """Calculate overall context health score (0.0 to 1.0)"""
        print("Calculating Context Health Score...")
        
        # Check documentation consistency
        doc_health = self._check_documentation_health()
        
        # Check build system health
        build_health = self._check_build_health()
        
        # Check code integrity
        code_health = self._check_code_health()
        
        # Check system integration
        integration_health = self._check_integration_health()
        
        # Weighted average
        weights = {
            'documentation': 0.25,
            'build': 0.25,
            'code': 0.25,
            'integration': 0.25
        }
        
        total_health = (
            doc_health * weights['documentation'] +
            build_health * weights['build'] +
            code_health * weights['code'] +
            integration_health * weights['integration']
        )
        
        return max(0.0, min(1.0, total_health))
    
    def _check_documentation_health(self) -> float:
        """Check documentation consistency and completeness"""
        print(f"{'📚' if UNICODE_SUPPORT else '[DOC]'} Checking Documentation Health...")
        
        required_docs = [
            "docs/ai-context/AI_context_reallocator.md",
            "AIOS_PROJECT_CONTEXT.md", 
            "README.md",
            "docs/ai-context/PROJECT_STATUS.md",
            "docs/ai-context/AI_QUICK_REFERENCE.md"
        ]
        
        detailed_docs = [
            "docs/ARCHITECTURE.md",
            "docs/DEVELOPMENT.md",
            "docs/API_REFERENCE.md",
            "docs/INSTALLATION.md",
            "docs/CHANGELOG.md"
        ]
        
        score = 1.0
        
        # Check required docs exist
        for doc in required_docs:
            if not (self.project_root / doc).exists():
                self.issues.append(f"Missing required documentation: {doc}")
                score -= 0.15
        
        # Check detailed docs exist
        for doc in detailed_docs:
            if not (self.project_root / doc).exists():
                self.warnings.append(f"Missing detailed documentation: {doc}")
                score -= 0.05
        
        # Check for TODO/FIXME markers
        try:
            result = subprocess.run(
                ["grep", "-r", "TODO\\|FIXME\\|UPDATE", str(self.project_root)],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                todo_count = len(result.stdout.strip().split('\n'))
                if todo_count > 10:
                    self.warnings.append(f"High number of TODO items: {todo_count}")
                    score -= 0.1
        except:
            pass
        
        return max(0.0, score)
    
    def _check_build_health(self) -> float:
        """Check build system health"""
        print(f"{'🔧' if UNICODE_SUPPORT else '[BUILD]'} Checking Build System Health...")
        
        score = 1.0
        
        # Check vcpkg
        vcpkg_path = Path("C:/dev/vcpkg")
        if not vcpkg_path.exists():
            self.issues.append("vcpkg not found at C:/dev/vcpkg")
            score -= 0.3
        
        # Check CMake build directory
        build_dir = self.project_root / "core" / "build"
        if not build_dir.exists():
            self.issues.append("C++ build directory not found")
            score -= 0.2
        
        # Check Python environment
        venv_path = self.project_root / "ai" / "venv"
        if not venv_path.exists():
            self.warnings.append("Python virtual environment not found")
            score -= 0.1
        
        return max(0.0, score)
    
    def _check_code_health(self) -> float:
        """Check code integrity and completeness"""
        print(f"{'💻' if UNICODE_SUPPORT else '[CODE]'} Checking Code Health...")
        
        score = 1.0
        
        # Check C++ core files
        cpp_files = list((self.project_root / "core" / "src").glob("*.cpp"))
        if len(cpp_files) == 0:
            self.issues.append("No C++ source files found")
            score -= 0.3
        
        # Check Python AI modules
        ai_modules = [
            "ai/src/core/nlp/__init__.py",
            "ai/src/core/prediction/__init__.py",
            "ai/src/core/automation/__init__.py",
            "ai/src/core/learning/__init__.py",
            "ai/src/core/integration/__init__.py"
        ]
        
        for module in ai_modules:
            if not (self.project_root / module).exists():
                self.issues.append(f"Missing AI module: {module}")
                score -= 0.1
        
        # Check C# interface structure
        cs_interface = self.project_root / "interface"
        if not cs_interface.exists():
            self.warnings.append("C# interface directory not found")
            score -= 0.05
        
        return max(0.0, score)
    
    def _check_integration_health(self) -> float:
        """Check system integration health"""
        print(f"{'🔗' if UNICODE_SUPPORT else '[INTEGRATION]'} Checking Integration Health...")
        
        score = 1.0
        
        # Check integration test exists
        integration_test = self.project_root / "scripts" / "test_integration.py"
        if not integration_test.exists():
            self.issues.append("Integration test not found")
            score -= 0.3
        else:
            # Try to run integration test
            try:
                result = subprocess.run(
                    [sys.executable, str(integration_test)],
                    cwd=str(self.project_root),
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                if result.returncode != 0:
                    self.issues.append("Integration test failing")
                    score -= 0.4
                else:
                    print("Integration test passed successfully!")
            except subprocess.TimeoutExpired:
                self.warnings.append("Integration test timeout")
                score -= 0.2
            except Exception as e:
                self.warnings.append(f"Integration test error: {e}")
                score -= 0.3
        
        return max(0.0, score)
    
    def should_trigger_reingestion(self, iterations_since_last: int) -> bool:
        """Determine if context reingestion should be triggered"""
        health = self.calculate_context_health()
        
        # Health-based triggers
        if health < 0.7:
            return True
        
        # Adaptive iteration-based triggers
        base_iterations = 6 if health > 0.9 else 8 if health > 0.8 else 9
        
        return iterations_since_last >= base_iterations
    
    def generate_health_report(self) -> Dict:
        """Generate comprehensive health report"""
        health_score = self.calculate_context_health()
        
        return {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "health_score": health_score,
            "health_status": self._get_health_status(health_score),
            "issues": self.issues,
            "warnings": self.warnings,
            "recommendations": self._generate_recommendations(),
            "trigger_reingestion": health_score < 0.7
        }
    
    def _get_health_status(self, score: float) -> str:
        """Get human-readable health status"""
        if score >= 0.9:
            return STATUS_EXCELLENT
        elif score >= 0.8:
            return STATUS_HEALTHY
        elif score >= 0.7:
            return STATUS_GOOD
        elif score >= 0.5:
            return STATUS_DEGRADED
        elif score >= 0.3:
            return STATUS_CRITICAL
        else:
            return STATUS_FAILURE
    
    def _generate_recommendations(self) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        if self.issues:
            recommendations.append("IMMEDIATE ACTION REQUIRED: Fix critical issues")
        
        if len(self.warnings) > 5:
            recommendations.append("Address accumulated warnings")
        
        if not (self.project_root / "test_integration.py").exists():
            recommendations.append("Create integration test for system validation")
        
        return recommendations
    
    def print_health_report(self):
        """Print formatted health report"""
        report = self.generate_health_report()
        
        print("\n" + "="*60)
        print("AIOS CONTEXT HEALTH REPORT")
        print("="*60)
        print(f"Timestamp: {report['timestamp']}")
        print(f"Health Score: {report['health_score']:.2f} / 1.00")
        print(f"Status: {report['health_status']}")
        
        if report['issues']:
            print(f"\n{ICON_ISSUES} CRITICAL ISSUES ({len(report['issues'])}):")
            for issue in report['issues']:
                print(f"   • {issue}")
        
        if report['warnings']:
            print(f"\n{ICON_WARNINGS} WARNINGS ({len(report['warnings'])}):")
            for warning in report['warnings']:
                print(f"   • {warning}")
        
        if report['recommendations']:
            print(f"\n{ICON_RECOMMENDATIONS} RECOMMENDATIONS:")
            for rec in report['recommendations']:
                print(f"   • {rec}")
        
        print(f"\nTrigger Reingestion: {'YES' if report['trigger_reingestion'] else 'NO'}")
        print("="*60)

def main():
    """Main execution function"""
    if len(sys.argv) > 1 and sys.argv[1] == "--json":
        # JSON output for programmatic use
        monitor = AIContextHealthMonitor()
        report = monitor.generate_health_report()
        print(json.dumps(report, indent=2))
    else:
        # Human-readable output
        monitor = AIContextHealthMonitor()
        monitor.print_health_report()
        
        # Exit code based on health
        health_score = monitor.calculate_context_health()
        if health_score < 0.5:
            sys.exit(1)  # Critical issues
        elif health_score < 0.7:
            sys.exit(2)  # Should trigger reingestion
        else:
            sys.exit(0)  # Healthy

if __name__ == "__main__":
    main()
