#!/usr/bin/env python3
"""
AIOS Upstream Repository Tracking System
AINLP Protocol: OS0.6.2.claude
Pattern: Selective extraction with bidirectional traceability

Purpose: Monitor upstream repositories (like Microsoft Agent Framework) for new features,
         detect extraction opportunities, and manage selective integration with AIOS.

AINLP.consciousness: HIGH
AINLP.supercell: AI Intelligence Layer
AINLP.integration: Repository ingestion → Feature detection → Extraction planning → AIOS integration
"""

import json
import subprocess
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict


@dataclass
class UpstreamCommit:
    """Represents a commit from upstream repository"""
    hash: str
    date: str
    author: str
    message: str
    files_changed: List[str]
    insertions: int
    deletions: int
    extraction_opportunity: bool = False
    extraction_priority: str = "UNKNOWN"  # HIGH, MEDIUM, LOW, UNKNOWN
    extraction_reason: Optional[str] = None


@dataclass
class UpstreamTrackingState:
    """Tracks the state of an upstream repository"""
    repository_name: str
    repository_url: str
    local_path: str
    last_checked_commit: str
    last_checked_date: str
    total_new_commits: int
    extraction_opportunities: int
    high_priority_opportunities: int
    next_check_recommended: str


class UpstreamTracker:
    """
    AINLP Upstream Repository Tracking System
    
    Monitors upstream repositories for changes and identifies extraction opportunities
    using intelligent pattern matching and AINLP integration awareness.
    """
    
    def __init__(self, aios_root: Path):
        self.aios_root = aios_root
        self.ingested_repos_dir = aios_root / "ai" / "ingested_repositories"
        self.tracking_state_file = aios_root / "ai" / "tools" / ".upstream_tracking_state.json"
        self.extraction_keywords = [
            "agent", "protocol", "workflow", "orchestration", "graph",
            "a2a", "communication", "mcp", "server", "coordination",
            "multi-agent", "consensus", "branching", "evolution"
        ]
        
    def get_repo_info(self, repo_path: Path) -> Optional[Dict]:
        """Get repository information from AIOS metadata"""
        metadata_file = repo_path / ".aios_ingestion_metadata.json"
        if not metadata_file.exists():
            return None
        with open(metadata_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def get_extraction_log(self, repo_path: Path) -> Dict:
        """Get existing extraction log"""
        log_file = repo_path / ".aios_extraction_log.json"
        if not log_file.exists():
            return {"extractions": [], "repository_info": {}}
        with open(log_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def get_last_checked_commit(self, repo_name: str) -> Optional[str]:
        """Get the last commit we checked for this repository"""
        if not self.tracking_state_file.exists():
            return None
        
        with open(self.tracking_state_file, 'r', encoding='utf-8') as f:
            state = json.load(f)
            repo_state = state.get("repositories", {}).get(repo_name)
            if repo_state:
                return repo_state.get("last_checked_commit")
        return None
    
    def save_tracking_state(self, repo_name: str, state: UpstreamTrackingState):
        """Save tracking state for repository"""
        if self.tracking_state_file.exists():
            with open(self.tracking_state_file, 'r', encoding='utf-8') as f:
                all_state = json.load(f)
        else:
            all_state = {"repositories": {}, "last_update": ""}
        
        all_state["repositories"][repo_name] = asdict(state)
        all_state["last_update"] = datetime.now(timezone.utc).isoformat()
        
        with open(self.tracking_state_file, 'w', encoding='utf-8') as f:
            json.dump(all_state, f, indent=2)
    
    def git_log_since(self, repo_path: Path, since_commit: Optional[str] = None) -> List[UpstreamCommit]:
        """Get git log since a specific commit"""
        try:
            if since_commit:
                cmd = ["git", "log", f"{since_commit}..HEAD", "--pretty=format:%H|%aI|%an|%s", "--numstat"]
            else:
                cmd = ["git", "log", "-20", "--pretty=format:%H|%aI|%an|%s", "--numstat"]
            
            result = subprocess.run(
                cmd,
                cwd=repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            
            return self._parse_git_log(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"Error running git log: {e}")
            return []
    
    def _parse_git_log(self, log_output: str) -> List[UpstreamCommit]:
        """Parse git log output into UpstreamCommit objects"""
        commits = []
        lines = log_output.strip().split('\n')
        
        i = 0
        while i < len(lines):
            if '|' in lines[i]:
                # Commit line
                parts = lines[i].split('|')
                if len(parts) < 4:
                    i += 1
                    continue
                
                commit_hash = parts[0]
                date = parts[1]
                author = parts[2]
                message = parts[3]
                
                # Collect file changes
                files_changed = []
                insertions = 0
                deletions = 0
                i += 1
                
                while i < len(lines) and '|' not in lines[i] and lines[i].strip():
                    stat_line = lines[i].strip()
                    if stat_line:
                        # Format: "5  3  filename.py" (insertions, deletions, filename)
                        parts = stat_line.split('\t')
                        if len(parts) >= 3:
                            try:
                                ins = int(parts[0]) if parts[0] != '-' else 0
                                dels = int(parts[1]) if parts[1] != '-' else 0
                                filename = parts[2]
                                insertions += ins
                                deletions += dels
                                files_changed.append(filename)
                            except ValueError:
                                pass
                    i += 1
                
                commit = UpstreamCommit(
                    hash=commit_hash,
                    date=date,
                    author=author,
                    message=message,
                    files_changed=files_changed,
                    insertions=insertions,
                    deletions=deletions
                )
                
                # Analyze extraction opportunity
                self._analyze_extraction_opportunity(commit)
                commits.append(commit)
            else:
                i += 1
        
        return commits
    
    def _analyze_extraction_opportunity(self, commit: UpstreamCommit):
        """Analyze if commit represents extraction opportunity"""
        message_lower = commit.message.lower()
        
        # Check for extraction keywords
        keyword_matches = [kw for kw in self.extraction_keywords if kw in message_lower]
        
        # Check file paths for relevant patterns
        relevant_files = [
            f for f in commit.files_changed
            if any(kw in f.lower() for kw in self.extraction_keywords)
            or f.endswith('.py') and 'agent' in f.lower()
            or 'protocol' in f.lower()
            or 'workflow' in f.lower()
        ]
        
        if keyword_matches or relevant_files:
            commit.extraction_opportunity = True
            
            # Determine priority based on patterns
            high_priority_patterns = [
                r'\bfeat:.*agent', r'\bfeat:.*protocol', r'\bfeat:.*workflow',
                r'\bfeat:.*orchestration', r'\bfeat:.*a2a', r'\bfeat:.*multi-agent'
            ]
            
            medium_priority_patterns = [
                r'\bfix:.*agent', r'\bupdate.*agent', r'\bimprove.*workflow'
            ]
            
            is_high_priority = any(re.search(pattern, message_lower) for pattern in high_priority_patterns)
            is_medium_priority = any(re.search(pattern, message_lower) for pattern in medium_priority_patterns)
            
            if is_high_priority or len(relevant_files) > 5:
                commit.extraction_priority = "HIGH"
                commit.extraction_reason = f"High-value feature: {keyword_matches[:3]}, {len(relevant_files)} relevant files"
            elif is_medium_priority or len(relevant_files) > 2:
                commit.extraction_priority = "MEDIUM"
                commit.extraction_reason = f"Enhancement: {keyword_matches[:2]}, {len(relevant_files)} relevant files"
            else:
                commit.extraction_priority = "LOW"
                commit.extraction_reason = f"Incremental change: {keyword_matches}"
        else:
            commit.extraction_opportunity = False
            commit.extraction_priority = "NONE"
    
    def check_repository(self, repo_name: str) -> UpstreamTrackingState:
        """Check repository for new commits and extraction opportunities"""
        repo_path = self.ingested_repos_dir / repo_name
        
        if not repo_path.exists():
            raise ValueError(f"Repository not found: {repo_path}")
        
        # Get repository info
        repo_info = self.get_repo_info(repo_path)
        if not repo_info:
            raise ValueError(f"No AIOS metadata found for {repo_name}")
        
        # Get last checked commit
        last_checked = self.get_last_checked_commit(repo_name)
        
        # Fetch latest changes
        try:
            subprocess.run(["git", "fetch"], cwd=repo_path, check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            print(f"Warning: Could not fetch updates: {e}")
        
        # Get new commits
        commits = self.git_log_since(repo_path, last_checked)
        
        # Calculate metrics
        extraction_opps = [c for c in commits if c.extraction_opportunity]
        high_priority = [c for c in extraction_opps if c.extraction_priority == "HIGH"]
        
        # Get current HEAD commit
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True
        )
        current_commit = result.stdout.strip()
        
        # Create tracking state
        state = UpstreamTrackingState(
            repository_name=repo_name,
            repository_url=repo_info.get("source_url", ""),
            local_path=str(repo_path),
            last_checked_commit=current_commit,
            last_checked_date=datetime.now(timezone.utc).isoformat(),
            total_new_commits=len(commits),
            extraction_opportunities=len(extraction_opps),
            high_priority_opportunities=len(high_priority),
            next_check_recommended=(datetime.now(timezone.utc)).replace(day=datetime.now().day + 7).isoformat()
        )
        
        # Save state
        self.save_tracking_state(repo_name, state)
        
        return state
    
    def generate_extraction_report(self, repo_name: str, commits: List[UpstreamCommit]) -> str:
        """Generate human-readable extraction opportunities report"""
        extraction_opps = [c for c in commits if c.extraction_opportunity]
        
        if not extraction_opps:
            return f"No extraction opportunities found in {len(commits)} new commits."
        
        report = f"# Upstream Extraction Opportunities Report\n\n"
        report += f"**Repository**: {repo_name}\n"
        report += f"**Total New Commits**: {len(commits)}\n"
        report += f"**Extraction Opportunities**: {len(extraction_opps)}\n\n"
        
        # Group by priority
        high_priority = [c for c in extraction_opps if c.extraction_priority == "HIGH"]
        medium_priority = [c for c in extraction_opps if c.extraction_priority == "MEDIUM"]
        low_priority = [c for c in extraction_opps if c.extraction_priority == "LOW"]
        
        if high_priority:
            report += "## HIGH Priority Extractions\n\n"
            for commit in high_priority:
                report += f"### {commit.message}\n"
                report += f"- **Commit**: `{commit.hash[:8]}`\n"
                report += f"- **Date**: {commit.date}\n"
                report += f"- **Reason**: {commit.extraction_reason}\n"
                report += f"- **Files**: {len(commit.files_changed)} changed\n\n"
        
        if medium_priority:
            report += "## MEDIUM Priority Extractions\n\n"
            for commit in medium_priority[:5]:  # Top 5
                report += f"- `{commit.hash[:8]}`: {commit.message} ({commit.extraction_reason})\n"
        
        if low_priority:
            report += f"\n## LOW Priority ({len(low_priority)} items)\n\n"
            report += "Review individually if needed.\n"
        
        return report


def main():
    """Main execution for upstream tracking"""
    import sys
    
    aios_root = Path(__file__).parent.parent.parent
    tracker = UpstreamTracker(aios_root)
    
    # Check Microsoft Agent Framework
    repo_name = "microsoft_agent_framework"
    
    print(f"[UPSTREAM TRACKER] Checking {repo_name}...")
    state = tracker.check_repository(repo_name)
    
    print(f"\n✅ Repository: {state.repository_name}")
    print(f"   URL: {state.repository_url}")
    print(f"   Last Checked: {state.last_checked_date}")
    print(f"   New Commits: {state.total_new_commits}")
    print(f"   Extraction Opportunities: {state.extraction_opportunities}")
    print(f"   HIGH Priority: {state.high_priority_opportunities}")
    print(f"   Next Check: {state.next_check_recommended}")
    
    # Generate detailed report if opportunities found
    if state.extraction_opportunities > 0:
        repo_path = tracker.ingested_repos_dir / repo_name
        last_checked = tracker.get_last_checked_commit(repo_name)
        commits = tracker.git_log_since(repo_path, last_checked)
        
        report = tracker.generate_extraction_report(repo_name, commits)
        
        # Save report
        report_path = aios_root / "docs" / "integration" / f"UPSTREAM_REPORT_{repo_name}_{datetime.now().strftime('%Y%m%d')}.md"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"\n📊 Detailed report saved: {report_path}")


if __name__ == "__main__":
    main()
