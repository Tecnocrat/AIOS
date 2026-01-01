#!/usr/bin/env python3
"""
AIOS Agentic CI Consumer

Local agent that fetches CI feedback from GitHub Actions and executes
safe autonomous refactoring actions based on the decision schema.

Usage:
    python agentic_ci_consumer.py --repo Tecnocrat/AIOS --branch feature/xyz
    python agentic_ci_consumer.py --watch  # Poll for new feedback
    python agentic_ci_consumer.py --dry-run  # Preview actions without executing
"""

import argparse
import json
import os
import subprocess
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Optional

import yaml


@dataclass
class ConvergenceState:
    """Tracks iteration state for convergence guards."""
    iteration: int = 0
    max_iterations: int = 5
    last_health: float = 0.0
    health_history: list[float] = field(default_factory=list)
    improvement_threshold: float = 0.01  # 1%
    
    def should_continue(self, current_health: float) -> bool:
        """Determine if the loop should continue based on convergence criteria."""
        if self.iteration >= self.max_iterations:
            print(f"⛔ Max iterations ({self.max_iterations}) reached")
            return False
        
        if self.health_history:
            improvement = current_health - self.health_history[-1]
            if improvement < self.improvement_threshold and self.iteration > 1:
                print(f"⛔ Improvement ({improvement:.3f}) below threshold ({self.improvement_threshold})")
                return False
        
        self.health_history.append(current_health)
        self.last_health = current_health
        return True
    
    def next_iteration(self) -> int:
        """Advance to next iteration and return iteration number."""
        self.iteration += 1
        return self.iteration


@dataclass
class AgenticAction:
    """Represents an action to be taken by the agent."""
    trigger_id: str
    action: str
    priority: str
    autonomous: bool
    metadata: dict = field(default_factory=dict)
    
    @property
    def is_safe(self) -> bool:
        """Check if action is safe for autonomous execution."""
        return self.autonomous and self.priority != 'critical'


class AgenticCIConsumer:
    """
    Main consumer class that fetches CI feedback and orchestrates actions.
    """
    
    SAFE_ACTIONS = {
        'refactor_coherence',
        'analyze_patterns', 
        'migrate_deprecated',
        'suggest_compression',
        'generate_tests',
    }
    
    REQUIRES_APPROVAL = {
        'block_and_alert',
        'request_rationale',
        'upgrade_protocol',
    }
    
    def __init__(
        self,
        repo: str,
        branch: Optional[str] = None,
        workspace: Optional[Path] = None,
        dry_run: bool = False,
    ):
        self.repo = repo
        self.branch = branch
        self.workspace = workspace or Path.cwd()
        self.dry_run = dry_run
        self.convergence = ConvergenceState()
        
        # Load decision schema
        schema_path = self.workspace / 'governance' / 'agentic_ci' / 'decision_schema.yaml'
        if schema_path.exists():
            with open(schema_path) as f:
                self.schema = yaml.safe_load(f)
        else:
            self.schema = {}
            print(f"⚠️  Decision schema not found at {schema_path}")
    
    def fetch_latest_feedback(self) -> Optional[dict]:
        """Fetch the latest CI feedback artifact from GitHub Actions."""
        print(f"📥 Fetching CI feedback for {self.repo}...")
        
        # Get latest workflow run with agentic-ci-feedback artifact
        cmd = [
            'gh', 'run', 'list',
            '--repo', self.repo,
            '--workflow', 'CI Feedback Aggregator',
            '--limit', '5',
            '--json', 'databaseId,conclusion,headBranch,createdAt'
        ]
        
        if self.branch:
            cmd.extend(['--branch', self.branch])
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            runs = json.loads(result.stdout)
            
            if not runs:
                print("❌ No aggregator runs found")
                return None
            
            # Find successful run
            for run in runs:
                if run['conclusion'] == 'success':
                    run_id = run['databaseId']
                    print(f"✅ Found run {run_id} on {run['headBranch']}")
                    return self._download_feedback(run_id)
            
            print("❌ No successful aggregator runs")
            return None
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to fetch runs: {e.stderr}")
            return None
    
    def _download_feedback(self, run_id: int) -> Optional[dict]:
        """Download and parse the feedback artifact."""
        import tempfile
        
        with tempfile.TemporaryDirectory() as tmpdir:
            cmd = [
                'gh', 'run', 'download', str(run_id),
                '--repo', self.repo,
                '--name', 'agentic-ci-feedback',
                '--dir', tmpdir
            ]
            
            try:
                subprocess.run(cmd, capture_output=True, text=True, check=True)
                feedback_path = Path(tmpdir) / 'ci_feedback.json'
                
                if feedback_path.exists():
                    with open(feedback_path) as f:
                        return json.load(f)
                else:
                    print(f"❌ Feedback file not found in artifact")
                    return None
                    
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to download artifact: {e.stderr}")
                return None
    
    def evaluate_actions(self, feedback: dict) -> list[AgenticAction]:
        """Evaluate triggered actions from feedback."""
        actions = []
        
        for trigger in feedback.get('triggered_actions', []):
            action = AgenticAction(
                trigger_id=trigger['trigger_id'],
                action=trigger['action'],
                priority=trigger['priority'],
                autonomous=trigger.get('autonomous', False),
                metadata=trigger
            )
            actions.append(action)
        
        return actions
    
    def execute_action(self, action: AgenticAction) -> bool:
        """Execute a single agentic action."""
        print(f"\n🔧 Executing: {action.action} (trigger: {action.trigger_id})")
        
        if self.dry_run:
            print(f"   [DRY RUN] Would execute {action.action}")
            return True
        
        # Dispatch to specific action handlers
        handlers = {
            'refactor_coherence': self._action_refactor_coherence,
            'analyze_patterns': self._action_analyze_patterns,
            'migrate_deprecated': self._action_migrate_deprecated,
            'generate_tests': self._action_generate_tests,
            'suggest_compression': self._action_suggest_compression,
        }
        
        handler = handlers.get(action.action)
        if handler:
            return handler(action)
        else:
            print(f"   ⚠️  No handler for action: {action.action}")
            return False
    
    def _action_refactor_coherence(self, action: AgenticAction) -> bool:
        """Improve code coherence through refactoring."""
        print("   📊 Analyzing coherence gaps...")
        
        # This would integrate with your existing coherence tools
        # For now, we'll create a placeholder that calls existing scripts
        coherence_script = self.workspace / 'runtime' / 'tools' / 'scripts' / 'dev_terminal.ps1'
        
        if coherence_script.exists():
            cmd = ['pwsh', '-File', str(coherence_script), '-Action', 'coherence', '-ReportCoherence']
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.workspace)
                print(f"   Coherence analysis complete (exit: {result.returncode})")
                return result.returncode == 0
            except Exception as e:
                print(f"   ❌ Error: {e}")
                return False
        
        return True
    
    def _action_analyze_patterns(self, action: AgenticAction) -> bool:
        """Analyze and document pattern inconsistencies."""
        print("   🔍 Analyzing patterns...")
        
        # Generate pattern analysis report
        report = {
            'timestamp': datetime.now().isoformat(),
            'trigger': action.trigger_id,
            'findings': [],
            'recommendations': []
        }
        
        output_path = self.workspace / 'governance' / 'agentic_ci' / 'feedback' / 'pattern_analysis.json'
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"   📄 Report written to {output_path}")
        return True
    
    def _action_migrate_deprecated(self, action: AgenticAction) -> bool:
        """Migrate deprecated code patterns."""
        deprecated_files = action.metadata.get('files', [])
        print(f"   📦 Migrating {len(deprecated_files)} deprecated files...")
        
        for file_path in deprecated_files:
            print(f"      - {file_path}")
        
        # Actual migration would happen here
        return True
    
    def _action_generate_tests(self, action: AgenticAction) -> bool:
        """Generate test files for untested code."""
        print("   🧪 Generating tests...")
        
        # This would integrate with test generation tools
        # Could use AI to generate test stubs
        return True
    
    def _action_suggest_compression(self, action: AgenticAction) -> bool:
        """Suggest file compression or splitting."""
        oversized_files = action.metadata.get('files', [])
        
        suggestions = []
        for file_info in oversized_files:
            suggestions.append({
                'file': file_info,
                'recommendation': 'Consider splitting or compressing'
            })
        
        output_path = self.workspace / 'governance' / 'agentic_ci' / 'feedback' / 'compression_suggestions.json'
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(suggestions, f, indent=2)
        
        print(f"   📄 Suggestions written to {output_path}")
        return True
    
    def commit_changes(self, iteration: int, actions_taken: list[str]) -> bool:
        """Commit changes with agentic CI marker."""
        if self.dry_run:
            print(f"\n[DRY RUN] Would commit with marker [agentic-ci iter:{iteration}]")
            return True
        
        # Check for changes
        result = subprocess.run(
            ['git', 'status', '--porcelain'],
            capture_output=True, text=True, cwd=self.workspace
        )
        
        if not result.stdout.strip():
            print("ℹ️  No changes to commit")
            return True
        
        # Stage all changes
        subprocess.run(['git', 'add', '-A'], cwd=self.workspace, check=True)
        
        # Create commit message
        actions_str = ', '.join(actions_taken)
        message = f"refactor(agentic-ci): auto-improvements [agentic-ci iter:{iteration}]\n\nActions: {actions_str}"
        
        subprocess.run(['git', 'commit', '-m', message], cwd=self.workspace, check=True)
        print(f"✅ Committed changes: [agentic-ci iter:{iteration}]")
        
        return True
    
    def push_changes(self) -> bool:
        """Push changes to remote."""
        if self.dry_run:
            print("[DRY RUN] Would push changes")
            return True
        
        branch = self.branch or 'HEAD'
        result = subprocess.run(
            ['git', 'push', 'origin', branch],
            capture_output=True, text=True, cwd=self.workspace
        )
        
        if result.returncode == 0:
            print("✅ Pushed changes to remote")
            return True
        else:
            print(f"❌ Push failed: {result.stderr}")
            return False
    
    def run_iteration(self) -> bool:
        """Run a single iteration of the agentic loop."""
        print(f"\n{'='*60}")
        print(f"🔄 AGENTIC CI ITERATION {self.convergence.iteration + 1}")
        print(f"{'='*60}")
        
        # Fetch latest feedback
        feedback = self.fetch_latest_feedback()
        if not feedback:
            print("❌ Could not fetch feedback, stopping")
            return False
        
        # Check convergence
        health = feedback.get('overall_health', 0.0)
        if health and not self.convergence.should_continue(health):
            print(f"✅ Convergence reached (health: {health:.3f})")
            return False
        
        # Evaluate actions
        actions = self.evaluate_actions(feedback)
        safe_actions = [a for a in actions if a.is_safe]
        
        print(f"\n📋 Actions Summary:")
        print(f"   Total triggered: {len(actions)}")
        print(f"   Safe for auto-execution: {len(safe_actions)}")
        
        if not safe_actions:
            print("ℹ️  No safe autonomous actions to execute")
            return False
        
        # Execute safe actions
        actions_taken = []
        for action in safe_actions:
            if self.execute_action(action):
                actions_taken.append(action.action)
        
        if actions_taken:
            iteration = self.convergence.next_iteration()
            self.commit_changes(iteration, actions_taken)
            
            if feedback.get('convergence', {}).get('should_continue', False):
                self.push_changes()
                return True  # Continue loop
        
        return False
    
    def watch(self, poll_interval: int = 60):
        """Watch for new CI feedback and process automatically."""
        print(f"👁️  Watching for CI feedback (poll every {poll_interval}s)...")
        print("   Press Ctrl+C to stop")
        
        last_run_id = None
        
        while True:
            try:
                feedback = self.fetch_latest_feedback()
                
                if feedback:
                    run_id = feedback.get('meta', {}).get('run_id')
                    
                    if run_id != last_run_id:
                        last_run_id = run_id
                        print(f"\n🆕 New feedback from run {run_id}")
                        
                        # Run iteration loop
                        while self.run_iteration():
                            time.sleep(10)  # Brief pause between iterations
                
                time.sleep(poll_interval)
                
            except KeyboardInterrupt:
                print("\n👋 Stopping watch mode")
                break


def main():
    parser = argparse.ArgumentParser(description='AIOS Agentic CI Consumer')
    parser.add_argument('--repo', default='Tecnocrat/AIOS', help='GitHub repository')
    parser.add_argument('--branch', help='Branch to process')
    parser.add_argument('--workspace', type=Path, default=Path.cwd(), help='Local workspace path')
    parser.add_argument('--dry-run', action='store_true', help='Preview without executing')
    parser.add_argument('--watch', action='store_true', help='Watch for new feedback')
    parser.add_argument('--poll-interval', type=int, default=60, help='Poll interval in seconds')
    parser.add_argument('--max-iterations', type=int, default=5, help='Max iterations per session')
    
    args = parser.parse_args()
    
    consumer = AgenticCIConsumer(
        repo=args.repo,
        branch=args.branch,
        workspace=args.workspace,
        dry_run=args.dry_run,
    )
    consumer.convergence.max_iterations = args.max_iterations
    
    if args.watch:
        consumer.watch(poll_interval=args.poll_interval)
    else:
        # Single iteration
        while consumer.run_iteration():
            print("\n⏳ Waiting for CI to process changes...")
            time.sleep(30)  # Wait for CI
        
        print("\n✅ Agentic CI session complete")


if __name__ == '__main__':
    main()
