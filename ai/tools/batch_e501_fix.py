#!/usr/bin/env python3
"""
Batch E501 fixer using hierarchical agentic pipeline with GitHub Models.

Applies GPT-4o-mini generation + GPT-4o validation to fix all E501 violations.
"""
import asyncio
import sys
from pathlib import Path
from typing import List, Dict
import json

from hierarchical_e501_pipeline import HierarchicalE501Pipeline

# Files with E501 violations (from scan)
TARGET_FILES = {
    "../src/ingestion/ainlp_ingestion_class.py": [
        72,
        93,
        114,
        138,
        159,
        180,
        188,
        212,
        230,
        247,
        264,
        288,
        310,
        333,
        340,
        353,
        357,
    ],
    "dendritic_config_agent.py": [171, 179, 270, 283, 315, 318, 338, 352],
    "hierarchical_e501_pipeline.py": [
        8,
        94,
        169,
        182,
        229,
        259,
        268,
        287,
        296,
        314,
        334,
        343,
        362,
        371,
        391,
        401,
        420,
        534,
        540,
        543,
    ],
    "openrouter_tier3_validator.py": [122, 132, 160, 176, 186, 224, 260, 277],
    "../nucleus/agent_conclave_facade.py": [200],
}


async def fix_file(
    pipeline: HierarchicalE501Pipeline, file_path: Path, line_numbers: List[int]
) -> Dict:
    """Fix all E501 violations in a file"""

    print(f"\n{'='*60}")
    print(f"Processing: {file_path.name}")
    print(f"Lines to fix: {len(line_numbers)}")
    print(f"{'='*60}\n")

    if not file_path.exists():
        print(f"[ERROR] File not found: {file_path}")
        return {
            "file": file_path.name,
            "success": False,
            "error": "File not found",
            "total_violations": len(line_numbers),
            "fixed": 0,
            "failed": len(line_numbers),
        }

    # Read file
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    results = []
    modified_lines = {}

    # Process each violation
    for line_num in sorted(line_numbers):
        if line_num > len(lines):
            msg = f"[WARN] Line {line_num} out of range"
            print(f"{msg} (file has {len(lines)} lines)")
            continue

        original_line = lines[line_num - 1].rstrip("\n")

        if len(original_line) <= 79:
            print(
                f"[OK] Line {line_num}: Already compliant ({len(original_line)} chars)"
            )
            continue

        print(f"\n[FIX] Line {line_num} ({len(original_line)} chars):")
        print(f"   {original_line[:70]}...")

        # Apply hierarchical pipeline
        result = await pipeline.fix_line_hierarchical(
            line=original_line, file_path=str(file_path), line_number=line_num
        )

        if result["success"]:
            tier_path = " -> ".join(result["tier_log"])
            confidence = result.get("confidence", 0)
            print(f"   [SUCCESS] Fixed via {tier_path} (confidence: {confidence:.2f})")

            # Store fix
            modified_lines[line_num] = result["fixed_lines"]
            results.append(
                {
                    "line": line_num,
                    "success": True,
                    "tier_log": result["tier_log"],
                    "confidence": confidence,
                }
            )
        else:
            print(f"   [FAIL] Fix failed: {result.get('error', 'Unknown error')}")
            results.append(
                {"line": line_num, "success": False, "error": result.get("error")}
            )

    # Apply modifications
    if modified_lines:
        count = len(modified_lines)
        print(f"\n[APPLY] Applying {count} fixes to {file_path.name}...")

        # Reconstruct file with fixes
        new_lines = []
        offset = 0  # Track line number shifts from multi-line replacements

        for i, line in enumerate(lines, 1):
            if i in modified_lines:
                # Replace with fixed lines
                fixed = modified_lines[i]
                for fixed_line in fixed:
                    new_lines.append(fixed_line + "\n")
                offset += len(fixed) - 1
            else:
                new_lines.append(line)

        # Write back
        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)

        print(f"[DONE] File updated: {len(modified_lines)} violations fixed")
    else:
        print("[INFO] No changes needed")

    return {
        "file": file_path.name,
        "total_violations": len(line_numbers),
        "fixed": len([r for r in results if r["success"]]),
        "failed": len([r for r in results if not r["success"]]),
        "results": results,
    }


async def main():
    """Batch fix all E501 violations"""

    print("=" * 60)
    print("AIOS Agentic E501 Batch Fixer")
    print("GitHub Models: GPT-4o-mini (Tier 2) + GPT-4o (Tier 3)")
    print("=" * 60)

    pipeline = HierarchicalE501Pipeline(use_openrouter_sdk=False)

    base_dir = Path(__file__).parent
    summary = []

    for filename, line_numbers in TARGET_FILES.items():
        file_path = base_dir / filename
        result = await fix_file(pipeline, file_path, line_numbers)
        summary.append(result)

    # Final summary
    print("\n" + "=" * 60)
    print("BATCH FIX SUMMARY")
    print("=" * 60)

    total_violations = sum(s["total_violations"] for s in summary)
    total_fixed = sum(s["fixed"] for s in summary)
    total_failed = sum(s["failed"] for s in summary)

    for s in summary:
        status = "[OK]" if s["failed"] == 0 else "[WARN]"
        print(f"{status} {s['file']}: {s['fixed']}/{s['total_violations']} fixed")

    print(f"\nOverall: {total_fixed}/{total_violations} violations fixed")
    print(f"Success rate: {(total_fixed/total_violations)*100:.1f}%")

    # Save detailed report
    report_path = base_dir / "e501_fix_report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print(f"\nDetailed report: {report_path}")

    return total_fixed == total_violations


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
