#!/usr/bin/env python3
"""
Test script for enhanced AIOS Core Evolution Monitor with file directive checking.
"""

from aios_core_evolution_monitor import AIOSCoreEvolutionMonitor

def test_directive_checking():
    """Test the enhanced directive checking capabilities."""
    print("[TEST] Initializing AIOS Core Evolution Monitor...")

    monitor = AIOSCoreEvolutionMonitor()

    print("[TEST] Running evolution status monitoring...")
    result = monitor.monitor_evolution_status()

    print("Evolution monitoring completed successfully!")
    print(f"Files analyzed: {result['file_directive_analysis']['total_files_analyzed']}")
    print(".2f")
    print(f"Top violations: {result['file_directive_analysis']['top_violations'][:3]}")

    # Test individual file checking
    print("\n[TEST] Testing individual file compliance check...")
    test_file = "c:\\dev\\AIOS\\core\\runtime_intelligence\\aios_core_evolution_monitor.py"
    file_result = monitor.check_file_compliance(test_file)

    if "error" not in file_result:
        print(f"File compliance score: {file_result['compliance_score']:.2f}")
        print(f"Violations found: {len(file_result['violations'])}")
        print(f"Recommendations: {len(file_result['recommendations'])}")
    else:
        print(f"Error checking file: {file_result['error']}")

    # Generate report
    print("\n[TEST] Generating directive compliance report...")
    report_path = monitor.generate_directive_report()
    print(f"Report generated: {report_path}")

    return result

if __name__ == "__main__":
    test_directive_checking()