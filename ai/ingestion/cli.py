#!/usr/bin/env python3
"""
AIOS Knowledge Ingestion Protocol - CLI Runner
==============================================

AINLP.dendritic[ai/ingestion/cli]{runner,fetch,test}

Command-line interface for testing KIP providers.

Usage:
    python -m ai.ingestion.cli --provider microsoft --max-items 5
    python -m ai.ingestion.cli --test
"""

import argparse
import asyncio
import json
import sys
from pathlib import Path

# Add AIOS root to path
AIOS_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(AIOS_ROOT))

from ai.ingestion import SourceRegistry
from ai.ingestion.providers import MicrosoftProvider


async def test_providers():
    """Test all registered providers."""
    print("=" * 60)
    print("AIOS Knowledge Ingestion Protocol - Test")
    print("=" * 60)

    registry = SourceRegistry()
    registry.register_provider(MicrosoftProvider())

    print(f"\nRegistered providers: {registry.list_providers()}")
    print(f"Registered sources: {registry.list_sources()}")

    print("\n" + "-" * 60)
    print("Fetching from all sources (max 3 items each)...")
    print("-" * 60)

    results = await registry.fetch_all(max_items=3)

    total_items = 0
    for result in results:
        print(f"\n📰 {result.source_name}:")
        if result.errors:
            print(f"   ❌ Errors: {result.errors}")
        else:
            print(f"   ✓ {len(result.items)} items fetched")
            total_items += len(result.items)
            for item in result.items[:3]:
                title = item.title[:55] + "..." if len(item.title) > 55 else item.title
                print(f"   - {title}")

    print("\n" + "=" * 60)
    print(f"Total items fetched: {total_items}")
    print("=" * 60)


async def fetch_provider(provider_name: str, max_items: int, output_json: bool):
    """Fetch from a specific provider."""
    registry = SourceRegistry()

    if provider_name == "microsoft":
        registry.register_provider(MicrosoftProvider())
    else:
        print(f"Unknown provider: {provider_name}")
        return

    results = await registry.fetch_provider(provider_name, max_items=max_items)

    if output_json:
        all_items = []
        for result in results:
            all_items.extend([item.to_dict() for item in result.items])
        print(json.dumps(all_items, indent=2))
    else:
        for result in results:
            print(f"\n{result.source_name}: {len(result.items)} items")
            for item in result.items:
                print(f"  - [{item.category}] {item.title}")


def main():
    parser = argparse.ArgumentParser(
        description="AIOS Knowledge Ingestion Protocol CLI"
    )
    parser.add_argument(
        "--test", action="store_true",
        help="Run test fetch from all providers"
    )
    parser.add_argument(
        "--provider", "-p", type=str,
        help="Provider to fetch from (e.g., microsoft)"
    )
    parser.add_argument(
        "--max-items", "-n", type=int, default=10,
        help="Maximum items per source"
    )
    parser.add_argument(
        "--json", "-j", action="store_true",
        help="Output as JSON"
    )

    args = parser.parse_args()

    if args.test:
        asyncio.run(test_providers())
    elif args.provider:
        asyncio.run(fetch_provider(args.provider, args.max_items, args.json))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
