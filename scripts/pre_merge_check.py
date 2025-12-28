#!/usr/bin/env python3
"""
Pre-Merge Conflict Detection Script

AINLP.spatial_awareness: scripts/pre_merge_check.py
AINLP.purpose: Detect potential merge conflicts before integration

Usage:
    python scripts/pre_merge_check.py [branch_a] [branch_b]
    python scripts/pre_merge_check.py  # Uses defaults
"""

import subprocess
import json
import sys
from pathlib import Path
from datetime import datetime


def run_git(args: list) -> str:
    """Execute git command and return output."""
    result = subprocess.run(
        ["git"] + args,
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent
    )
    return result.stdout.strip()


def get_changed_files(base: str, branch: str) -> set:
    """Get files changed between base and branch."""
    output = run_git(["diff", "--name-only", f"{base}...{branch}"])
    return set(output.split('\n')) if output else set()


def get_branch_status(branch: str) -> dict:
    """Get commits ahead/behind main."""
    ahead = run_git(["rev-list", "--count", f"origin/main..{branch}"])
    behind = run_git(["rev-list", "--count", f"{branch}..origin/main"])
    last_commit = run_git(["log", "-1", "--format=%H %s", branch])
    
    return {
        "branch": branch,
        "commits_ahead": int(ahead) if ahead.isdigit() else 0,
        "commits_behind": int(behind) if behind.isdigit() else 0,
        "last_commit": last_commit[:80] if last_commit else "unknown"
    }


def categorize_conflicts(files: set) -> dict:
    """Categorize conflicting files by domain."""
    categories = {
        "protocol": [],      # ai/protocols/*
        "evolution": [],     # evolution_lab/*
        "scripts": [],       # scripts/*
        "docs": [],          # docs/*
        "config": [],        # *.json, *.yaml, *.toml
        "other": []
    }
    
    for f in files:
        if f.startswith("ai/protocols"):
            categories["protocol"].append(f)
        elif f.startswith("evolution_lab"):
            categories["evolution"].append(f)
        elif f.startswith("scripts"):
            categories["scripts"].append(f)
        elif f.startswith("docs"):
            categories["docs"].append(f)
        elif any(f.endswith(ext) for ext in [".json", ".yaml", ".toml"]):
            categories["config"].append(f)
        else:
            categories["other"].append(f)
    
    return {k: v for k, v in categories.items() if v}


def generate_resolution_plan(conflicts: dict) -> list:
    """Generate resolution recommendations based on conflict types."""
    plan = []
    
    if conflicts.get("protocol"):
        plan.append({
            "category": "protocol",
            "files": conflicts["protocol"],
            "recommendation": "AIOS branch should win for protocol files",
            "strategy": "--strategy-option=theirs for HP_LAB merge"
        })
    
    if conflicts.get("evolution"):
        plan.append({
            "category": "evolution",
            "files": conflicts["evolution"],
            "recommendation": "HP_LAB branch should win for evolution files",
            "strategy": "--strategy-option=theirs for AIOS merge"
        })
    
    if conflicts.get("scripts"):
        plan.append({
            "category": "scripts",
            "files": conflicts["scripts"],
            "recommendation": "Manual review required - both may have valid changes",
            "strategy": "Interactive merge with careful review"
        })
    
    if conflicts.get("docs"):
        plan.append({
            "category": "docs",
            "files": conflicts["docs"],
            "recommendation": "Usually safe to merge both - documentation can coexist",
            "strategy": "merge=union in .gitattributes"
        })
    
    return plan


def main():
    """Run conflict detection and generate report."""
    # Parse arguments
    branch_a = sys.argv[1] if len(sys.argv) > 1 else "AIOS-win-0-AIOS"
    branch_b = sys.argv[2] if len(sys.argv) > 2 else "AIOS-win-0-HP_LAB"
    output_json = "--json" in sys.argv
    
    print("=" * 70)
    print("IACP PRE-MERGE CONFLICT DETECTION")
    print("=" * 70)
    
    # Fetch latest
    print("\n📡 Fetching latest from origin...")
    run_git(["fetch", "origin"])
    
    # Get branch statuses
    print("\n📊 Analyzing branch status...")
    status_a = get_branch_status(branch_a)
    status_b = get_branch_status(branch_b)
    
    # Get changed files
    files_a = get_changed_files("main", branch_a)
    files_b = get_changed_files("main", branch_b)
    
    # Find conflicts
    potential_conflicts = files_a & files_b
    conflicts_by_category = categorize_conflicts(potential_conflicts)
    
    # Generate report
    report = {
        "timestamp": datetime.now().isoformat(),
        "branches": {
            branch_a: {
                **status_a,
                "files_changed": len(files_a)
            },
            branch_b: {
                **status_b,
                "files_changed": len(files_b)
            }
        },
        "analysis": {
            "total_conflicts": len(potential_conflicts),
            "conflicts_by_category": conflicts_by_category,
            "safe_to_merge": len(potential_conflicts) == 0
        },
        "resolution_plan": generate_resolution_plan(conflicts_by_category)
    }
    
    if output_json:
        print(json.dumps(report, indent=2))
    else:
        # Pretty print
        print(f"\n📁 Branch: {branch_a}")
        print(f"   Ahead: {status_a['commits_ahead']}, Behind: {status_a['commits_behind']}")
        print(f"   Files changed: {len(files_a)}")
        
        print(f"\n📁 Branch: {branch_b}")
        print(f"   Ahead: {status_b['commits_ahead']}, Behind: {status_b['commits_behind']}")
        print(f"   Files changed: {len(files_b)}")
        
        print(f"\n{'='*70}")
        
        if potential_conflicts:
            print(f"⚠️  {len(potential_conflicts)} POTENTIAL CONFLICTS DETECTED")
            print("=" * 70)
            
            for category, files in conflicts_by_category.items():
                print(f"\n📂 {category.upper()} ({len(files)} files):")
                for f in sorted(files)[:10]:
                    print(f"   - {f}")
                if len(files) > 10:
                    print(f"   ... and {len(files) - 10} more")
            
            print("\n📋 RESOLUTION PLAN:")
            for item in report["resolution_plan"]:
                print(f"\n   [{item['category'].upper()}]")
                print(f"   Recommendation: {item['recommendation']}")
                print(f"   Strategy: {item['strategy']}")
        else:
            print("✅ NO CONFLICTS DETECTED")
            print("=" * 70)
            print("Safe to proceed with merge.")
    
    # Return exit code
    return 1 if potential_conflicts else 0


if __name__ == "__main__":
    sys.exit(main())
