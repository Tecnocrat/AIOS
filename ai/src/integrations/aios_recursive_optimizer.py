"""
AIOS Agentic Optimization Continued Execution
Execute multiple optimization iterations for recursive improvement
"""

import sys
sys.path.append("c:\\dev\\AIOS\\ai\\src\\integrations")

from aios_agentic_optimizer import AIOSAgenticOptimizer
import json

def execute_multiple_iterations(iterations=3):
    """Execute multiple optimization iterations"""
    print(" AIOS RECURSIVE OPTIMIZATION EXECUTION")
    print("=" * 50)
    
    optimizer = AIOSAgenticOptimizer()
    all_results = []
    
    for i in range(iterations):
        print(f"\n Executing Optimization Iteration {i+1}/{iterations}")
        print("-" * 40)
        
        results = optimizer.execute_optimization_iteration()
        all_results.append(results)
        
        # Display key metrics
        pass_summary = results['pass_summary']
        print(f" Pass {i+1} Complete:")
        print(f"   • Focus: {pass_summary['focus_area']}")
        print(f"   • Coherence Δ: +{pass_summary['coherence_improvement']:.3f}")
        print(f"   • Insights: {pass_summary['insights_count']}")
        print(f"   • Optimizations: {pass_summary['optimizations_count']}")
    
    # Generate session report
    print(f"\n RECURSIVE OPTIMIZATION SESSION COMPLETE")
    print("=" * 50)
    
    session_report = optimizer.generate_session_report()
    
    print(f" Session Summary:")
    summary = session_report['session_summary']
    print(f"   • Total Passes: {summary['total_passes']}")
    print(f"   • Duration: {summary['duration_seconds']:.1f}s")
    print(f"   • Cumulative Improvement: +{summary['cumulative_coherence_improvement']:.3f}")
    print(f"   • Average Improvement/Pass: +{summary['average_improvement_per_pass']:.3f}")
    
    print(f"\n Optimization Progression:")
    for prog in session_report['optimization_progression']:
        print(f"   Pass {prog['pass_number']}: {prog['focus_area']} (+{prog['coherence_improvement']:.3f})")
    
    print(f"\n Key Insight Themes:")
    for insight in session_report['key_insights']:
        print(f"   • {insight}")
    
    print(f"\n Recommendations for Next Session:")
    for rec in session_report['recommendations']:
        print(f"   • {rec}")
    
    # Save comprehensive results
    results_file = "c:\\dev\\AIOS\\aios_recursive_optimization_session.json"
    try:
        with open(results_file, 'w') as f:
            json.dump({
                'session_report': session_report,
                'all_iterations': all_results
            }, f, indent=2, default=str)
        print(f"\n Comprehensive results saved to: {results_file}")
    except Exception as e:
        print(f"\n Could not save results: {e}")

if __name__ == "__main__":
    execute_multiple_iterations(3)
