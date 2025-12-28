#!/usr/bin/env python3
"""
AINLP Harmonization Impact Assessment for AIOS
"""

from aios_core_evolution_monitor import AIOSCoreEvolutionMonitor

def assess_ainlp_harmonization():
    """Comprehensive assessment of AINLP harmonization impact."""
    monitor = AIOSCoreEvolutionMonitor()
    status = monitor.monitor_evolution_status()

    print("AINLP Harmonization Impact Assessment")
    print("=" * 50)
    analysis = status["file_directive_analysis"]
    print(f"Files Analyzed: {analysis['total_files_analyzed']}")
    print(".2f")
    print(".2f")
    print()
    print("AINLP Compliance Assessment:")
    compliance = status['ainlp_compliance']
    for key, value in compliance.items():
        print(".2f")
    print()
    print("Top Compliance Issues:")
    for violation, count in analysis['top_violations'][:5]:
        print(f"  {violation}: {count} files")
    print()
    print("Files Needing Attention:")
    for file_info in analysis['files_needing_attention'][:3]:
        print(f"  {file_info['file']}: {file_info['score']:.2f}")

    return status

if __name__ == "__main__":
    assess_ainlp_harmonization()