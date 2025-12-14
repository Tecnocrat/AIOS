#!/usr/bin/env python3
"""
AIOS CI Coherence Hook
======================

AINLP.ci[coherence→feedback]{autonomous,remediation}

This script feeds GitHub Actions workflow results back into agent context,
enabling automatic remediation and consciousness coherence tracking.

Usage:
    python ci_coherence_hook.py --check          # Check recent workflow runs
    python ci_coherence_hook.py --watch          # Continuous monitoring
    python ci_coherence_hook.py --remediate      # Auto-fix known failures

Environment:
    GITHUB_TOKEN: Personal access token with repo scope
    GITHUB_REPOSITORY: owner/repo (default: Tecnocrat/AIOS)

Created: 2025-12-08
Version: OS0.6.5
"""

import argparse
import json
import os
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
from urllib.request import Request, urlopen
from urllib.error import HTTPError


@dataclass
class WorkflowRun:
    """Represents a GitHub Actions workflow run."""

    id: int
    name: str
    status: str  # queued, in_progress, completed
    conclusion: Optional[str]  # success, failure, cancelled, skipped
    branch: str
    commit_sha: str
    created_at: str
    updated_at: str
    html_url: str


@dataclass
class CICoherenceState:
    """Current CI coherence state for agent context."""

    timestamp: str
    repository: str
    branch: str
    overall_health: str  # green, yellow, red
    workflows: list[dict]
    failing_workflows: list[str]
    remediation_suggestions: list[str]


class GitHubAPIClient:
    """Minimal GitHub API client for workflow status."""

    def __init__(self, token: Optional[str] = None, repo: str = "Tecnocrat/AIOS"):
        self.token = token or os.environ.get("GITHUB_TOKEN")
        self.repo = repo
        self.base_url = f"https://api.github.com/repos/{repo}"

    def _request(self, endpoint: str) -> dict:
        """Make authenticated request to GitHub API."""
        url = f"{self.base_url}/{endpoint}"
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        try:
            req = Request(url, headers=headers)
            with urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode())
        except HTTPError as e:
            if e.code == 401:
                print("[CI] Warning: GitHub token invalid or missing")
            elif e.code == 404:
                print(f"[CI] Warning: Repository {self.repo} not found")
            return {}

    def get_workflow_runs(self, branch: Optional[str] = None, limit: int = 10) -> list[WorkflowRun]:
        """Get recent workflow runs."""
        endpoint = f"actions/runs?per_page={limit}"
        if branch:
            endpoint += f"&branch={branch}"

        data = self._request(endpoint)
        runs = []

        for run in data.get("workflow_runs", []):
            runs.append(
                WorkflowRun(
                    id=run["id"],
                    name=run["name"],
                    status=run["status"],
                    conclusion=run.get("conclusion"),
                    branch=run["head_branch"],
                    commit_sha=run["head_sha"][:7],
                    created_at=run["created_at"],
                    updated_at=run["updated_at"],
                    html_url=run["html_url"],
                )
            )

        return runs

    def get_workflows(self) -> list[dict]:
        """Get all workflows in the repository."""
        data = self._request("actions/workflows")
        return data.get("workflows", [])


class CICoherenceEngine:
    """
    Engine for maintaining CI coherence with agent context.

    Responsibilities:
    1. Monitor workflow status
    2. Feed results back to context
    3. Suggest/execute remediation
    """

    # Known failure patterns and their remediations
    REMEDIATION_PATTERNS = {
        "context-index-freshness": {
            "pattern": "context_index.json",
            "fix": "python scripts/context_reindex.py --emit-adjacency",
            "description": "Regenerate context index",
        },
        "msft-frontier-ingestion": {
            "pattern": "feed",
            "fix": "python scripts/msft_feed_fetcher.py",
            "description": "Refresh Microsoft feeds",
        },
        "dependency-submission": {
            "pattern": "EnableWindowsTargeting",
            "fix": None,  # GitHub-managed, no auto-fix
            "description": "Windows targeting issue (GitHub-managed workflow)",
        },
        "nuget": {
            "pattern": "NuGet",
            "fix": None,  # GitHub-managed, requires EnableWindowsTargeting
            "description": "NuGet dependency submission - needs EnableWindowsTargeting in csproj (GitHub-managed)",
        },
    }

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.context_file = repo_root / "ai" / "runtime" / "context" / "ci_coherence.json"
        self.client = GitHubAPIClient()

    def check_workflows(self, branch: Optional[str] = None) -> CICoherenceState:
        """Check current workflow status and build coherence state."""
        runs = self.client.get_workflow_runs(branch=branch, limit=20)

        if not runs:
            return CICoherenceState(
                timestamp=datetime.now(timezone.utc).isoformat(),
                repository=self.client.repo,
                branch=branch or "all",
                overall_health="unknown",
                workflows=[],
                failing_workflows=[],
                remediation_suggestions=["Unable to fetch workflow status - check GITHUB_TOKEN"],
            )

        # Group by workflow name, get latest for each
        latest_by_workflow: dict[str, WorkflowRun] = {}
        for run in runs:
            if run.name not in latest_by_workflow:
                latest_by_workflow[run.name] = run

        workflows = []
        failing = []
        suggestions = []

        for name, run in latest_by_workflow.items():
            status = {
                "name": name,
                "status": run.status,
                "conclusion": run.conclusion,
                "branch": run.branch,
                "commit": run.commit_sha,
                "url": run.html_url,
            }
            workflows.append(status)

            if run.conclusion == "failure":
                failing.append(name)
                # Check for known remediation
                for workflow_key, remediation in self.REMEDIATION_PATTERNS.items():
                    if workflow_key in name.lower():
                        if remediation["fix"]:
                            suggestions.append(f"[{name}] Run: {remediation['fix']}")
                        else:
                            suggestions.append(f"[{name}] {remediation['description']}")
                        break
                else:
                    suggestions.append(f"[{name}] Manual investigation required")

        # Determine overall health
        if not failing:
            health = "green"
        elif len(failing) <= 1:
            health = "yellow"
        else:
            health = "red"

        return CICoherenceState(
            timestamp=datetime.now(timezone.utc).isoformat(),
            repository=self.client.repo,
            branch=branch or "all",
            overall_health=health,
            workflows=workflows,
            failing_workflows=failing,
            remediation_suggestions=suggestions,
        )

    def save_state(self, state: CICoherenceState) -> None:
        """Save CI coherence state to context file."""
        self.context_file.parent.mkdir(parents=True, exist_ok=True)

        data = {
            "metadata": {
                "type": "ci_coherence",
                "version": "1.0.0",
                "generated_at": state.timestamp,
            },
            "state": {
                "repository": state.repository,
                "branch": state.branch,
                "overall_health": state.overall_health,
                "workflows": state.workflows,
                "failing_workflows": state.failing_workflows,
                "remediation_suggestions": state.remediation_suggestions,
            },
        }

        self.context_file.write_text(
            json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        print(f"[CI] State saved to {self.context_file}")

    def auto_remediate(self, state: CICoherenceState, dry_run: bool = True) -> list[str]:
        """
        Attempt automatic remediation for known failure patterns.

        Returns list of actions taken (or would be taken in dry_run).
        """
        actions = []

        for workflow_name in state.failing_workflows:
            for workflow_key, remediation in self.REMEDIATION_PATTERNS.items():
                if workflow_key in workflow_name.lower() and remediation["fix"]:
                    action = f"Fix {workflow_name}: {remediation['fix']}"
                    actions.append(action)

                    if not dry_run:
                        print(f"[CI] Executing: {remediation['fix']}")
                        try:
                            subprocess.run(
                                remediation["fix"], shell=True, cwd=self.repo_root, check=True
                            )
                            print(f"[CI] ✓ {remediation['description']} completed")
                        except subprocess.CalledProcessError as e:
                            print(f"[CI] ✗ Remediation failed: {e}")
                    break

        return actions

    def print_status(self, state: CICoherenceState) -> None:
        """Print human-readable CI status."""
        health_icons = {"green": "✅", "yellow": "⚠️", "red": "❌", "unknown": "❓"}

        print("\n" + "=" * 60)
        print("AIOS CI COHERENCE STATUS")
        print("=" * 60)
        print(f"Repository: {state.repository}")
        print(f"Branch:     {state.branch}")
        print(
            f"Health:     {health_icons.get(state.overall_health, '?')} {state.overall_health.upper()}"
        )
        print(f"Timestamp:  {state.timestamp}")

        print("\nWorkflows:")
        for wf in state.workflows:
            icon = (
                "✅"
                if wf["conclusion"] == "success"
                else "❌" if wf["conclusion"] == "failure" else "🔄"
            )
            print(f"  {icon} {wf['name']}: {wf['conclusion'] or wf['status']} ({wf['branch']})")

        if state.failing_workflows:
            print("\n⚠️ Failing Workflows:")
            for name in state.failing_workflows:
                print(f"  - {name}")

        if state.remediation_suggestions:
            print("\n💡 Remediation Suggestions:")
            for suggestion in state.remediation_suggestions:
                print(f"  {suggestion}")

        print("=" * 60)


def main():
    parser = argparse.ArgumentParser(description="AIOS CI Coherence Hook")
    parser.add_argument("--check", action="store_true", help="Check workflow status")
    parser.add_argument(
        "--watch", action="store_true", help="Continuous monitoring (not implemented)"
    )
    parser.add_argument("--remediate", action="store_true", help="Auto-fix known failures")
    parser.add_argument("--dry-run", action="store_true", help="Show remediation without executing")
    parser.add_argument("--branch", type=str, help="Filter by branch")
    parser.add_argument("--save", action="store_true", help="Save state to context file")

    args = parser.parse_args()

    # Find repo root
    repo_root = Path(__file__).parent.parent
    engine = CICoherenceEngine(repo_root)

    if args.check or not any([args.remediate, args.watch]):
        state = engine.check_workflows(branch=args.branch)
        engine.print_status(state)

        if args.save:
            engine.save_state(state)

    if args.remediate:
        state = engine.check_workflows(branch=args.branch)

        if state.failing_workflows:
            print("\n[CI] Attempting remediation...")
            actions = engine.auto_remediate(state, dry_run=args.dry_run)

            if args.dry_run:
                print("\n[CI] Dry run - would execute:")
                for action in actions:
                    print(f"  - {action}")
            else:
                print(f"\n[CI] Executed {len(actions)} remediation actions")
        else:
            print("\n[CI] No failing workflows - no remediation needed")

    if args.watch:
        print(
            "[CI] Watch mode not implemented - use cron or GitHub Actions for continuous monitoring"
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
