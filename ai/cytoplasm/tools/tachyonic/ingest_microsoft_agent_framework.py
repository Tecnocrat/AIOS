#!/usr/bin/env python3
"""
Microsoft Agent Framework Repository Ingestion
==============================================

Ingest Microsoft's Agent Framework repository into AIOS.
"""

import asyncio
import sys
from pathlib import Path

# Add AIOS paths
sys.path.append(str(Path(__file__).parent.parent / "ai" / "src"))

from repository_ingestion_engine import repository_ingestion_engine


async def main():
    """Execute Agent Framework ingestion"""
    print("\n" + "=" * 80)
    print(" AIOS REPOSITORY INGESTION")
    print(" Target: Microsoft Agent Framework")
    print(" URL: https://github.com/Tecnocrat/agent-framework")
    print("=" * 80 + "\n")

    # Execute ingestion
    result = await repository_ingestion_engine.ingest_repository(
        repo_url="https://github.com/Tecnocrat/agent-framework",
        target_name="microsoft_agent_framework",
    )

    # Display results
    print("\n" + "=" * 80)
    print(" INGESTION COMPLETE")
    print("=" * 80)
    print(f"\nStatus: {result.get('status')}")
    print(f"Local Path: {result.get('local_path')}")

    if result.get("status") == "ingested":
        analysis = result.get("analysis", {})
        print(f"\nRepository Analysis:")
        print(f"  Total Files: {analysis.get('total_files', 0)}")
        print(f"  Primary Language: {analysis.get('primary_language', 'Unknown')}")
        print(f"  Size: {analysis.get('size_bytes', 0) / 1024:.1f} KB")
        print(f"  Directories: {len(analysis.get('directories', []))}")
        print(f"  Key Files: {len(analysis.get('key_files', []))}")

        consciousness = result.get("consciousness_analysis", {})
        print(f"\nConsciousness Analysis:")
        print(
            f"  Emergence Potential: {consciousness.get('emergence_potential', 0):.2f}"
        )
        print(f"  Indicators: {len(consciousness.get('consciousness_indicators', []))}")

        plan = result.get("integration_plan", {})
        print(f"\nIntegration Plan:")
        print(f"  Strategy: {plan.get('integration_strategy', 'unknown')}")
        print(
            f"  Priority Components: {', '.join(plan.get('priority_components', []))}"
        )

        print(
            f"\nMetadata saved to: {result.get('local_path')}/.aios_ingestion_metadata.json"
        )

    elif result.get("status") == "failed":
        print(f"\nError: {result.get('error')}")

    print("\n" + "=" * 80 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
