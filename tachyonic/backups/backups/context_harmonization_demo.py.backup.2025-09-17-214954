#!/usr/bin/env python3
"""
AIOS Context Harmonization Demo
===============================

Demonstration of intelligent context harmonization system integration
with AINLP kernel logic for practical project organization.

This shows how the system:
1. Analyzes project files intelligently
2. Categorizes based on development patterns
3. Provides actionable recommendations
4. Integrates with AINLP for context understanding

Usage: python context_harmonization_demo.py
"""

import sys
from pathlib import Path

# Add AIOS paths
sys.path.extend([
    str(Path(__file__).parent),
    str(Path(__file__).parent / "ai" / "src"),
    str(Path(__file__).parent / "ai" / "src" / "core"),
    str(Path(__file__).parent / "ai" / "src" / "core" / "integration"),
])

try:
    from ai.src.core.integration.aios_context_harmonizer import (
        AIOSContextHarmonizer, get_harmonized_context_for_bootstrap)
except ImportError as e:
    print(f"Import error: {e}")
    print("Please ensure AIOS context harmonizer is available")
    sys.exit(1)


def demonstrate_context_harmonization():
    """Demonstrate the practical context harmonization system."""
    print("🧠 AIOS Context Harmonization Demonstration")
    print("=" * 50)

    # Initialize harmonizer
    root_path = Path(__file__).parent
    harmonizer = AIOSContextHarmonizer(root_path)

    print(f"📁 Analyzing project root: {root_path}")
    print("🔍 Scanning files and extracting context patterns...")

    # Perform context scan
    recommendations = harmonizer.scan_project_context()

    print(f"\n📊 Analysis Results:")
    print(f"   Total files profiled: {len(harmonizer.profiles)}")

    # Show file classifications
    classifications = {}
    for profile in harmonizer.profiles.values():
        classifications[profile.file_classification] = classifications.get(
            profile.file_classification, 0
        ) + 1

    print("\n🏷️  File Classifications:")
    for classification, count in classifications.items():
        print(f"   {classification}: {count} files")

    # Show high priority monitoring
    high_priority = recommendations.get("high_priority_monitoring", [])
    print(f"\n🔥 High Priority Monitoring ({len(high_priority)} files):")
    for item in high_priority[:5]:  # Show top 5
        print(
        f"   • {item['file']} (score: {item['score']:.2f}) - {item['reason']}")

    # Show AI reingestion candidates
    reingestion = recommendations.get("ai_reingestion_candidates", [])
    print(f"\n🧠 AI Reingestion Candidates ({len(reingestion)} files):")
    for item in reingestion[:5]:  # Show top 5
        tags_str = ", ".join(item['tags'][:3]) if item['tags'] else "none"
        print(
        f"   • {item['file']} (potential: {item['potential']:.2f}) - tags: {tags_str}")

    # Show organization suggestions
    suggestions = recommendations.get("organization_suggestions", [])
    print(
    f"\n💡 Organization Suggestions ({len(suggestions)} recommendations):")
    for suggestion in suggestions:
        print(f"   • {suggestion['type']}: {suggestion['message']}")
        print(f"     Impact: {suggestion['impact']}")

    # Show safe to archive
    safe_archive = recommendations.get("safe_to_archive", [])
    print(f"\n📦 Safe to Archive ({len(safe_archive)} files):")
    for item in safe_archive[:3]:  # Show top 3
        print(
        f"   • {item['file']} (score: {item['score']:.2f}) - {item['reason']}")

    return harmonizer, recommendations


def demonstrate_ainlp_integration(harmonizer, recommendations):
    """Demonstrate AINLP integration with context harmonization."""
    print("\n" + "=" * 50)
    print("🔗 AINLP Integration Demonstration")
    print("=" * 50)

    # Simulate AINLP context
    ainlp_context = {
        "current_focus": [
            "quantum fractal bootstrap",
            "context harmonization",
            "ainlp compiler",
            "hyperlayer activation"
        ],
        "active_development": True,
        "learning_mode": "continuous"
    }

    # Integrate with AINLP
    integration_result = harmonizer.integrate_with_ainlp(ainlp_context)

    print("🎯 Context Priorities by AINLP Focus:")
    for priority, files in integration_result["context_priorities"].items():
        print(f"\n   {priority.upper()}:")
        for file_info in files[:3]:  # Show top 3 per priority
            print(
            f"     • {file_info['file']} (importance: {file_info['importance']:.2f})")

    print(
    f"\n🔄 Reingestion Queue ({len(integration_result['reingestion_queue'])} files):")
    for item in integration_result["reingestion_queue"][:5]:
        print(f"   • {item['file']} (potential: {item['potential']:.2f})")
        print(f"     Reason: {item['reason']}")

    print(
    f"\n👁️  Monitoring Targets ({len(integration_result['monitoring_targets'])} files):")
    for target in integration_result["monitoring_targets"][:5]:
        print(f"   • {target}")


def demonstrate_practical_benefits():
    """Demonstrate practical benefits of the harmonization system."""
    print("\n" + "=" * 50)
    print("✨ Practical Benefits Demonstration")
    print("=" * 50)

    benefits = [
        {
            "category": "🎯 Focused Development",
            "benefits": [
                "Automatic identification of files requiring close monitoring",
                "Clear separation of active vs. reference vs. archival content"\
                ,
                "Reduced cognitive load from unnecessary file clutter"
            ]
        },
        {
            "category": "🧠 AI Integration",
            "benefits": [
                "Intelligent file prioritization for AI context loading",
                "Automatic reingestion candidate identification",
                "Context-aware AINLP compilation enhancement"
            ]
        },
        {
            "category": "🏗️ Project Organization",
            "benefits": [
                "Actionable recommendations for file organization",
                "Automated archival suggestions based on usage patterns",
                "Clean development environment maintenance"
            ]
        },
        {
            "category": "⚡ Development Efficiency",
            "benefits": [
                "Faster navigation to important files",
                "Reduced time spent on file organization decisions",
                "Better understanding of project structure evolution"
            ]
        }
    ]

    for benefit_group in benefits:
        print(f"\n{benefit_group['category']}:")
        for benefit in benefit_group['benefits']:
            print(f"   • {benefit}")


def main():
    """Main demonstration function."""
    try:
        # Demonstrate context harmonization
        harmonizer, recommendations = demonstrate_context_harmonization()

        # Demonstrate AINLP integration
        demonstrate_ainlp_integration(harmonizer, recommendations)

        # Show practical benefits
        demonstrate_practical_benefits()

        print("\n" + "=" * 50)
        print("🎉 Context Harmonization Demo Complete!")
        print("\nKey Insight: Instead of complex tachyonic archival,")
        print("we now have intelligent, practical context understanding")
        print("that integrates directly with AINLP kernel logic.")
        print("=" * 50)

    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
