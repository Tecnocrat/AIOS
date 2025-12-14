#!/usr/bin/env python3
"""
File Criticality Evolution Runner
=================================

Simple runner for the File Criticality Evolution Engine.

Usage:
    python run_criticality_evolution.py [--dry-run]
    [--ollama-only] [--gemini-only]

Options:
    --dry-run: Analyze without updating canonical index
    --ollama-only: Use only Ollama agent
    --gemini-only: Use only Gemini agent
    --no-vscode: Disable VSCode Chat strategic oversight
"""

import asyncio
import argparse
import sys
from pathlib import Path

# Add AI root to path
AI_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(AI_ROOT))

from src.evolution.file_criticality_evolution_engine import (
<<<<<<< HEAD
    FileCriticalityEvolutionEngine,
=======
    FileCriticalityEvolutionEngine
>>>>>>> origin/OS0.6.2.grok
)


async def main():
<<<<<<< HEAD
    parser = argparse.ArgumentParser(description="File Criticality Evolution Runner")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Analyze without updating canonical index",
    )
    parser.add_argument(
        "--ollama-only", action="store_true", help="Use only Ollama agent"
    )
    parser.add_argument(
        "--gemini-only", action="store_true", help="Use only Gemini agent"
    )
    parser.add_argument(
        "--no-vscode",
        action="store_true",
        help="Disable VSCode Chat strategic oversight",
=======
    parser = argparse.ArgumentParser(
        description='File Criticality Evolution Runner'
    )
    parser.add_argument(
        '--dry-run', action='store_true',
        help='Analyze without updating canonical index'
    )
    parser.add_argument(
        '--ollama-only', action='store_true',
        help='Use only Ollama agent'
    )
    parser.add_argument(
        '--gemini-only', action='store_true',
        help='Use only Gemini agent'
    )
    parser.add_argument(
        '--no-vscode', action='store_true',
        help='Disable VSCode Chat strategic oversight'
>>>>>>> origin/OS0.6.2.grok
    )

    args = parser.parse_args()

    # Configure agent usage
    use_ollama = not args.gemini_only
    use_gemini = not args.ollama_only
    use_vscode = not args.no_vscode

    print("[CRITICALITY EVOLUTION RUNNER]")
    print(f"  Ollama: {'✓' if use_ollama else '✗'}")
    print(f"  Gemini: {'✓' if use_gemini else '✗'}")
    print(f"  VSCode Chat: {'✓' if use_vscode else '✗'}")
    print(f"  Dry Run: {'✓' if args.dry_run else '✗'}")
    print()

    # Initialize engine
    engine = FileCriticalityEvolutionEngine(
<<<<<<< HEAD
        use_ollama=use_ollama, use_gemini=use_gemini, use_vscode_chat=use_vscode
=======
        use_ollama=use_ollama,
        use_gemini=use_gemini,
        use_vscode_chat=use_vscode
>>>>>>> origin/OS0.6.2.grok
    )

    try:
        if args.dry_run:
            # Load and analyze without updating
            current_index = engine._load_current_index()
            print(f"[DRY RUN] Loaded {len(current_index)} records")

            # Multi-agent analysis (but don't update)
<<<<<<< HEAD
            enhanced_scores = await engine._multi_agent_analysis(current_index)
            print(
                f"[DRY RUN] Analysis complete - "
                f"{len(enhanced_scores)} records processed"
            )

            # Show sample changes
            changes = 0
            for orig, enhanced in zip(current_index[:5], enhanced_scores[:5]):
                orig_score = orig.get("criticality_score", 0)
                new_score = enhanced.get("criticality_score", 0)
                if abs(new_score - orig_score) > 1:
                    changes += 1
                    path = orig.get("path", "")
                    print(f"  {path}: {orig_score} → {new_score}")

            print(f"[DRY RUN] Sample changes: " f"{changes}/5 records would be updated")
=======
            enhanced_scores = await engine._multi_agent_analysis(
                current_index
            )
            print(f"[DRY RUN] Analysis complete - "
                  f"{len(enhanced_scores)} records processed")

            # Show sample changes
            changes = 0
            for orig, enhanced in zip(current_index[:5],
                                      enhanced_scores[:5]):
                orig_score = orig.get('criticality_score', 0)
                new_score = enhanced.get('criticality_score', 0)
                if abs(new_score - orig_score) > 1:
                    changes += 1
                    path = orig.get('path', '')
                    print(f"  {path}: {orig_score} → {new_score}")

            print(f"[DRY RUN] Sample changes: "
                  f"{changes}/5 records would be updated")
>>>>>>> origin/OS0.6.2.grok

        else:
            # Full evolution
            evolution_report = await engine.evolve_criticality_index()
            print("[SUCCESS] Evolution complete!")
<<<<<<< HEAD
            records = evolution_report["enhanced_records"]
            changes = evolution_report["changes_made"]
            shadow = evolution_report["tachyonic_shadow"]
=======
            records = evolution_report['enhanced_records']
            changes = evolution_report['changes_made']
            shadow = evolution_report['tachyonic_shadow']
>>>>>>> origin/OS0.6.2.grok
            print(f"  Records processed: {records}")
            print(f"  Changes made: {changes}")
            print(f"  Tachyonic shadow: {shadow}")

    except Exception as e:
        print(f"[ERROR] Evolution failed: {e}")
        sys.exit(1)


<<<<<<< HEAD
if __name__ == "__main__":
    asyncio.run(main())
=======
if __name__ == '__main__':
    asyncio.run(main())
>>>>>>> origin/OS0.6.2.grok
