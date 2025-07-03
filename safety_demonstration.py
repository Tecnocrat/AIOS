"""
AIOS Safety Demonstration: Showcasing Mandatory Safety Controls
This script demonstrates the safety governor system in action

⚠️ This demonstrates how autonomous operations are now controlled by safety measures.
"""

import sys
import time
from pathlib import Path

# Add scripts to path for imports
sys.path.append(str(Path(__file__).parent / "scripts"))

try:
    from safety_governor import SafetyGovernor, SafetyLevel, EmergencyReason
    from evolutionary_code_mutator import EvolutionaryCodeMutator
    from evolution_lab_manager import EvolutionLabManager
    SAFETY_AVAILABLE = True
except ImportError as e:
    print(f"❌ Safety system not available: {e}")
    SAFETY_AVAILABLE = False

def demonstrate_safety_control():
    """Demonstrate the safety governor controlling autonomous operations"""
    
    print("\n" + "="*80)
    print("🛡️  AIOS SAFETY GOVERNOR DEMONSTRATION")
    print("="*80)
    print("This demonstrates how autonomous operations are now controlled by safety measures.")
    print()
    
    if not SAFETY_AVAILABLE:
        print("❌ Safety system not available - this is a CRITICAL security issue!")
        return
    
    # Create safety governor
    print("1. Initializing Safety Governor...")
    governor = SafetyGovernor()
    
    # Show status before authorization
    print("\n2. Checking initial safety status:")
    status = governor.get_status()
    for key, value in status.items():
        print(f"   {key}: {value}")
    
    # Attempt unauthorized operation
    print("\n3. Attempting unauthorized autonomous operation...")
    try:
        mutator = EvolutionaryCodeMutator()
        # This should fail due to safety checks
        print("   ❌ This should not be possible without authorization!")
    except Exception as e:
        print(f"   ✅ Operation blocked by safety system: {e}")
    
    # Request authorization for a supervised session
    print("\n4. Requesting authorization for supervised evolution experiment...")
    authorized = governor.start_supervised_session(
        experiment_description="Safety demonstration experiment",
        safety_level=SafetyLevel.SUPERVISED,
        duration_minutes=2,  # Short demo
        authorized_by="safety_demonstration"
    )
    
    if authorized:
        print("   ✅ Authorization granted - starting supervised session")
        
        # Show authorized status
        print("\n5. Safety status during authorized session:")
        status = governor.get_status()
        for key, value in status.items():
            print(f"   {key}: {value}")
        
        # Now operations are allowed
        print("\n6. Running authorized evolutionary operations...")
        try:
            mutator = EvolutionaryCodeMutator()
            
            # Create a simple population
            seed_code = '''
def hello_world():
    """A simple function for evolution"""
    return "Hello, World!"

if __name__ == "__main__":
    print(hello_world())
'''
            
            print("   Creating small population...")
            population = mutator.create_population("safety_demo", seed_code, 3)
            print(f"   ✅ Created population with {len(population.organisms)} organisms")
            
            # Demonstrate mutation (with safety checks)
            print("   Attempting code mutation...")
            if len(population.organisms) > 0:
                mutated = mutator.mutate_organism(population.organisms[0])
                print(f"   ✅ Mutation successful: {mutated.id}")
            
        except Exception as e:
            print(f"   ❌ Operation failed: {e}")
        
        # Demonstrate human check-in
        print("\n7. Recording human check-in...")
        governor.human_check_in("safety_demonstration")
        
        # Wait a moment to show monitoring
        print("\n8. Monitoring system for 5 seconds...")
        for i in range(5):
            print(f"   Monitoring... {i+1}/5")
            time.sleep(1)
        
        # End session safely
        print("\n9. Ending safety session...")
        governor.end_session("safety_demonstration")
        
    else:
        print("   ❌ Authorization denied - operations remain blocked")
    
    # Show final status
    print("\n10. Final safety status:")
    status = governor.get_status()
    for key, value in status.items():
        print(f"    {key}: {value}")
    
    print("\n" + "="*80)
    print("🛡️  SAFETY DEMONSTRATION COMPLETE")
    print("="*80)
    print("Key takeaways:")
    print("• Autonomous operations require explicit human authorization")
    print("• Resource monitoring and time limits are enforced")
    print("• Emergency shutdown capabilities are always available")
    print("• All operations are logged for accountability")
    print("• Human check-ins are required for extended operations")
    print("="*80)

def demonstrate_emergency_shutdown():
    """Demonstrate emergency shutdown functionality"""
    
    print("\n" + "="*80)
    print("🚨 EMERGENCY SHUTDOWN DEMONSTRATION")
    print("="*80)
    
    if not SAFETY_AVAILABLE:
        print("❌ Safety system not available!")
        return
    
    governor = SafetyGovernor()
    
    # Start a session
    print("1. Starting session for emergency shutdown demo...")
    if governor.start_supervised_session(
        "Emergency shutdown demonstration",
        SafetyLevel.SUPERVISED,
        1,  # 1 minute
        "emergency_demo"
    ):
        print("   ✅ Session started")
        
        # Simulate emergency
        print("\n2. Simulating emergency condition...")
        time.sleep(1)
        
        print("3. Triggering emergency shutdown...")
        governor.emergency_shutdown(
            EmergencyReason.HUMAN_INTERVENTION,
            "Demonstration of emergency shutdown procedure"
        )
        
        print("4. Verifying all operations are halted...")
        status = governor.get_status()
        print(f"   Emergency stopped: {status['emergency_stopped']}")
        print(f"   Session active: {status['session_active']}")
        
    print("\n✅ Emergency shutdown demonstration complete")
    print("="*80)

if __name__ == "__main__":
    print("🛡️ AIOS Safety System Demonstration")
    print("This script shows how the safety governor protects against unauthorized autonomous operations.")
    print()
    
    try:
        demonstrate_safety_control()
        print("\n" + "-"*60)
        demonstrate_emergency_shutdown()
        
    except Exception as e:
        print(f"\n❌ Demonstration failed: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n🛡️ Safety demonstration complete.")
    print("The AIOS system is now protected by mandatory safety controls.")
