#!/usr/bin/env python3
"""
AIOS Knowledge Ingestion Protocol - Workflow Runner
===================================================

AINLP.dendritic[ai/ingestion/runner]{workflow,automation,github-actions}

Standalone runner for GitHub Actions workflows.
Fetches from registered providers and generates output files.

Usage:
    python -m ai.ingestion.runner --provider microsoft --output docs/distilled
    
Environment Variables:
    MAX_ITEMS: Maximum items per source (default: 10)
    PRIORITY_FILTER: Filter by priority (high, medium, low, all)
    OUTPUT_DIR: Output directory (default: docs/distilled)
    KIP_STATE_DIR: State directory for dedup/registry (default: .kip)
"""

import argparse
import asyncio
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

# Add AIOS root to path
AIOS_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(AIOS_ROOT))

from ai.ingestion import (
    SourceRegistry,
    DeduplicationEngine,
    OutputGenerator,
)
from ai.ingestion.providers import MicrosoftProvider


def get_env_config() -> dict:
    """Get configuration from environment variables."""
    return {
        "max_items": int(os.environ.get("MAX_ITEMS", "10")),
        "priority_filter": os.environ.get("PRIORITY_FILTER", "all"),
        "output_dir": Path(os.environ.get(
            "OUTPUT_DIR", "docs/distilled"
        )),
        "state_dir": Path(os.environ.get("KIP_STATE_DIR", ".kip")),
    }


async def run_ingestion(
    provider_name: str,
    output_dir: Path,
    state_dir: Path,
    max_items: int = 10,
    priority_filter: str = "all",
) -> int:
    """
    Run knowledge ingestion for a provider.

    Returns:
        Number of new items ingested
    """
    print("=" * 60)
    print("AIOS Knowledge Ingestion Protocol")
    print("=" * 60)
    print(f"Provider: {provider_name}")
    print(f"Output: {output_dir}")
    print(f"Max items: {max_items}")
    print(f"Priority: {priority_filter}")
    print("-" * 60)

    # Initialize components
    state_dir.mkdir(parents=True, exist_ok=True)

    registry = SourceRegistry(state_dir / "registry_state.json")
    dedup = DeduplicationEngine(state_dir / "dedup_state.json")
    output = OutputGenerator(output_dir)

    # Register provider
    if provider_name == "microsoft":
        registry.register_provider(MicrosoftProvider())
    else:
        print(f"❌ Unknown provider: {provider_name}")
        return 0

    print(f"\n📡 Fetching from {len(registry.list_sources())} sources...")

    # Fetch
    results = await registry.fetch_provider(provider_name, max_items=max_items)

    # Deduplicate
    total_new = 0
    total_dup = 0

    for result in results:
        if result.errors:
            print(f"❌ {result.source_name}: {result.errors}")
            continue

        new_items, dups = dedup.deduplicate(result.items)
        result.items = new_items
        result.new_items = len(new_items)
        result.duplicate_items = len(dups)
        total_new += len(new_items)
        total_dup += len(dups)

        print(f"✓ {result.source_name}: {len(new_items)} new, {len(dups)} dup")

    # Filter by priority if specified
    if priority_filter != "all":
        for result in results:
            result.items = [
                item for item in result.items
                if item.priority.value == priority_filter
            ]

    # Generate output
    if total_new > 0:
        print(f"\n📝 Generating output...")
        output.write_provider_index(provider_name, results)
        print(f"✓ Wrote to {output_dir / provider_name}")

    # Save state
    dedup.save()

    print("\n" + "=" * 60)
    print(f"Total: {total_new} new items, {total_dup} duplicates skipped")
    print(f"Dedup database: {dedup.get_seen_count()} total hashes")
    print("=" * 60)

    return total_new


def main():
    parser = argparse.ArgumentParser(
        description="AIOS Knowledge Ingestion Protocol Runner"
    )
    parser.add_argument(
        "--provider", "-p", type=str, default="microsoft",
        help="Provider to fetch from"
    )
    parser.add_argument(
        "--output", "-o", type=str,
        help="Output directory"
    )
    parser.add_argument(
        "--max-items", "-n", type=int,
        help="Maximum items per source"
    )
    parser.add_argument(
        "--priority", type=str,
        help="Priority filter (high, medium, low, all)"
    )

    args = parser.parse_args()

    # Get config from env, override with args
    config = get_env_config()

    if args.output:
        config["output_dir"] = Path(args.output)
    if args.max_items:
        config["max_items"] = args.max_items
    if args.priority:
        config["priority_filter"] = args.priority

    # Run
    new_items = asyncio.run(run_ingestion(
        provider_name=args.provider,
        output_dir=config["output_dir"],
        state_dir=config["state_dir"],
        max_items=config["max_items"],
        priority_filter=config["priority_filter"],
    ))

    # Exit with 0 if we got items, useful for CI
    sys.exit(0 if new_items >= 0 else 1)


if __name__ == "__main__":
    main()
