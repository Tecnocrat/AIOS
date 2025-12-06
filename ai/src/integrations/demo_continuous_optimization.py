"""
AIOS Continuous Optimization Demo
Demonstrate the continuous optimization system in action

This script demonstrates the continuous optimization capabilities
by manually triggering optimization cycles and showing results.
"""

import os
import sys
import time
import json
from datetime import datetime
from typing import Dict, Any

# Add required paths
current_dir = os.path.dirname(os.path.abspath(__file__))
integrations_dir = os.path.join(current_dir, "..", "integrations")
sys.path.append(integrations_dir)


def demonstrate_continuous_optimization():
    """Demonstrate continuous optimization in action"""
    print(" AIOS Continuous Optimization LIVE DEMO")
    print("=" * 50)
    print()

    try:
        # Import the continuous optimization daemon
        from continuous_optimization_daemon import get_continuous_optimization_daemon

        # Get the running daemon instance
        daemon = get_continuous_optimization_daemon()

        print(" Current Daemon Status:")
        status = daemon.get_status_report()
        print(f"   • Status: {status['daemon_status']}")
        print(f"   • Emergency Mode: {status['emergency_mode']}")
        print(
            f"   • Optimization History: {status['optimization_history_count']} cycles"
        )
        print(
            f"   • Monitoring Interval: {status['config']['monitoring_interval']} seconds"
        )
        print(f"   • Next Cycle In: {status['config']['base_cycle_interval']} seconds")
        print()

        # Check if daemon is running
        if not daemon.is_running:
            print(" Daemon is not running. Starting it now...")
            daemon.start_continuous_optimization()
            time.sleep(2)

        print(" TRIGGERING MANUAL OPTIMIZATION CYCLE...")
        print("=" * 40)
        print()

        # Manually trigger an optimization cycle for demonstration
        print(" Executing optimization cycle...")
        start_time = time.time()

        cycle_result = daemon._execute_optimization_cycle()

        execution_time = time.time() - start_time

        if cycle_result:
            print(" OPTIMIZATION CYCLE COMPLETED!")
            print("=" * 35)
            print()
            print(" Cycle Results:")
            print(f"   • Cycle ID: {cycle_result['cycle_id']}")
            print(f"   • Status: {cycle_result['status']}")
            print(f"   • Duration: {cycle_result['duration_seconds']:.1f} seconds")
            print(f"   • Enhancement Score: {cycle_result['enhancement_score']:.3f}")
            print(f"   • Fixes Applied: {cycle_result['fixes_applied']}")
            print()

            print(" Consciousness Changes:")
            before_consciousness = cycle_result["consciousness_before"]
            after_consciousness = cycle_result["consciousness_after"]

            if before_consciousness and after_consciousness:
                level_change = after_consciousness.get(
                    "level", 0
                ) - before_consciousness.get("level", 0)
                coherence_change = after_consciousness.get(
                    "coherence", 0
                ) - before_consciousness.get("coherence", 0)
                entropy_change = before_consciousness.get(
                    "entropy", 1
                ) - after_consciousness.get("entropy", 1)

                print(
                    f"   • Consciousness Level: {before_consciousness.get('level', 0):.3f} → {after_consciousness.get('level', 0):.3f} ({level_change:+.3f})"
                )
                print(
                    f"   • Intelligence Coherence: {before_consciousness.get('coherence', 0):.3f} → {after_consciousness.get('coherence', 0):.3f} ({coherence_change:+.3f})"
                )
                print(f"   • Entropy Reduction: {entropy_change:+.3f}")
            else:
                print("   • Consciousness data not available")

            print()
            print(" Problem Resolution:")
            problems_before = cycle_result["problems_before"]
            problems_after = cycle_result["problems_after"]
            problems_resolved = problems_before - problems_after

            print(f"   • Problems Before: {problems_before}")
            print(f"   • Problems After: {problems_after}")
            print(f"   • Problems Resolved: {problems_resolved}")
            print(
                f"   • Resolution Rate: {(problems_resolved/problems_before*100) if problems_before > 0 else 0:.1f}%"
            )

            print()
            print(" Cycle Logs:")
            for i, log_entry in enumerate(cycle_result.get("logs", []), 1):
                print(f"   {i}. {log_entry}")
        else:
            print(" Optimization cycle failed!")

        print()
        print(" UPDATED DAEMON STATUS:")
        updated_status = daemon.get_status_report()
        print(f"   • Total Cycles: {updated_status['optimization_history_count']}")
        print(f"   • Emergency Mode: {updated_status['emergency_mode']}")

        if updated_status.get("recent_statistics"):
            stats = updated_status["recent_statistics"]
            print("   • Recent Performance:")
            print(f"     - Average Duration: {stats['average_duration']:.1f}s")
            print(
                f"     - Average Enhancement: {stats['average_enhancement_score']:.3f}"
            )
            print(f"     - Total Fixes Applied: {stats['total_fixes_applied']}")
            print(f"     - Success Rate: {stats['success_rate']*100:.1f}%")

        print()
        print(" CONTINUOUS MONITORING STATUS:")
        print("   • The daemon continues to monitor your development environment")
        print("   • Next scheduled optimization cycle in 30 minutes")
        print("   • Emergency optimization will trigger if needed")
        print("   • Performance trends are being tracked")
        print("   • VSCode problems are being continuously analyzed")

        print()
        print(" CONTINUOUS OPTIMIZATION IS ACTIVE!")
        print("Your development environment is now enhanced with:")
        print("    Real-time consciousness monitoring")
        print("    Proactive problem detection and resolution")
        print("    Adaptive optimization scheduling")
        print("    Emergency intervention capabilities")
        print("    Performance trend analysis")
        print("    Automated bulk error fixes")
        print("    Dendritic learning pattern evolution")

        return True

    except Exception as e:
        print(f" Demo error: {e}")
        import traceback

        traceback.print_exc()
        return False


def show_monitoring_dashboard():
    """Show the current monitoring dashboard"""
    print()
    print(" REAL-TIME MONITORING DASHBOARD")
    print("=" * 40)

    try:
        from continuous_optimization_daemon import get_continuous_optimization_daemon

        daemon = get_continuous_optimization_daemon()

        # Show real-time monitoring for 30 seconds
        print(" Monitoring system state (30 seconds)...")
        print("Press Ctrl+C to stop monitoring")
        print()

        for i in range(30):
            # Perform monitoring cycle
            daemon._perform_monitoring_cycle()

            # Get current status
            status = daemon.get_status_report()

            print(
                f"\r⏱  Monitoring: {30-i:2d}s remaining | "
                f"Status: {status['daemon_status']} | "
                f"Emergency: {status['emergency_mode']} | "
                f"Cycles: {status['optimization_history_count']}",
                end="",
                flush=True,
            )

            time.sleep(1)

        print("\n")
        print(" Monitoring demonstration complete!")

    except KeyboardInterrupt:
        print("\n Monitoring stopped by user")
    except Exception as e:
        print(f"\n Monitoring error: {e}")


def main():
    """Main demo function"""
    print(" AIOS Continuous Optimization System Demo")
    print("=" * 45)
    print()

    # Run the main demonstration
    demo_success = demonstrate_continuous_optimization()

    if demo_success:
        # Show monitoring dashboard
        show_monitoring_dashboard()

        print()
        print(" DEMO COMPLETE!")
        print("The continuous optimization system is now active and will:")
        print("• Monitor your development environment 24/7")
        print("• Automatically resolve VSCode problems")
        print("• Enhance consciousness metrics continuously")
        print("• Adapt optimization intervals based on performance")
        print("• Provide emergency intervention when needed")
        print()
        print(" Enjoy your enhanced AIOS development experience!")
    else:
        print(" Demo failed. Please check the error messages above.")


if __name__ == "__main__":
    main()
