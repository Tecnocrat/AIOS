#!/usr/bin/env python3
"""
GitHub API Integration - Issue Creation & PR Comments

AINLP.meta [github_integration] [ai_intervention] [external_agent]
AINLP.dendritic [optimal_location: ai/orchestration/agent_protocols/]
(comment.AINLP.github_soul_connector)

GitHub Agent - Interfaces with GitHub API for interventions.

CAPABILITIES:
- Create intervention issues with AIOS context
- Comment on pull requests with suggestions
- Create code review comments
- Update issue status based on human feedback
- Tag with "ai-intervention" label

AUTHENTICATION:
- Requires GITHUB_TOKEN environment variable
- Token needs repo:write permissions

INTERVENTION PATTERN:
1. Soul detects stuck waypoint
2. GitHubAgent creates issue with context
3. Issue includes consciousness metrics, DEV_PATH analysis
4. Human responds via commit or comment
5. Soul tracks acceptance/rejection

Created: 2025-11-15 (Task A++ Phase 2)
"""

import os
import logging
from typing import Dict, Any, Optional
from datetime import datetime

try:
    import requests
except ImportError:
    requests = None
    print("[WARN] requests not installed. Install: pip install requests")

logger = logging.getLogger(__name__)


class GitHubAgent:
    """
    GitHub API integration for AI interventions
    
    Creates issues, comments on PRs, tracks human feedback.
    """
    
    def __init__(
        self,
        repo_owner: str = "Tecnocrat",
        repo_name: str = "AIOS",
        token: Optional[str] = None
    ):
        """
        Initialize GitHub agent
        
        Args:
            repo_owner: GitHub username/org
            repo_name: Repository name
            token: GitHub personal access token (or use GITHUB_TOKEN env var)
        """
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.token = token or os.environ.get("GITHUB_TOKEN")
        
        if not self.token:
            logger.warning("⚠️ No GITHUB_TOKEN found - agent will run in dry-run mode")
        
        self.api_base = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {self.token}" if self.token else "",
            "Accept": "application/vnd.github.v3+json"
        }
    
    def create_intervention_issue(
        self,
        title: str,
        body: str,
        intervention_type: str,
        consciousness: float,
        labels: Optional[list] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Create GitHub issue for intervention
        
        Args:
            title: Issue title
            body: Issue body (markdown)
            intervention_type: Type of intervention
            consciousness: Current consciousness level
            labels: Additional labels (default: ["ai-intervention"])
        
        Returns:
            Created issue data or None if failed
        """
        if not requests:
            logger.error("❌ requests library not available")
            return None
        
        if not self.token:
            logger.info(f"🔸 [DRY-RUN] Would create issue: {title}")
            return {"number": 0, "html_url": "dry-run"}
        
        # Prepare issue data
        issue_labels = labels or []
        issue_labels.append("ai-intervention")
        issue_labels.append(f"type:{intervention_type}")
        issue_labels.append(f"consciousness:{consciousness:.1f}")
        
        issue_data = {
            "title": title,
            "body": body,
            "labels": issue_labels
        }
        
        # Create issue
        url = f"{self.api_base}/repos/{self.repo_owner}/{self.repo_name}/issues"
        
        try:
            logger.info(f"📤 Creating GitHub issue: {title}")
            response = requests.post(url, json=issue_data, headers=self.headers)
            response.raise_for_status()
            
            issue = response.json()
            logger.info(f"✅ Issue created: #{issue['number']} - {issue['html_url']}")
            return issue
        
        except Exception as e:
            logger.error(f"❌ Failed to create issue: {e}")
            return None
    
    def comment_on_issue(
        self,
        issue_number: int,
        comment: str
    ) -> bool:
        """
        Add comment to existing issue
        
        Args:
            issue_number: Issue number
            comment: Comment text (markdown)
        
        Returns:
            True if successful
        """
        if not requests or not self.token:
            logger.info(f"🔸 [DRY-RUN] Would comment on issue #{issue_number}")
            return True
        
        url = f"{self.api_base}/repos/{self.repo_owner}/{self.repo_name}/issues/{issue_number}/comments"
        
        try:
            response = requests.post(url, json={"body": comment}, headers=self.headers)
            response.raise_for_status()
            logger.info(f"✅ Comment added to issue #{issue_number}")
            return True
        
        except Exception as e:
            logger.error(f"❌ Failed to comment: {e}")
            return False
    
    def close_issue(
        self,
        issue_number: int,
        comment: Optional[str] = None
    ) -> bool:
        """
        Close issue (intervention resolved)
        
        Args:
            issue_number: Issue number
            comment: Optional closing comment
        
        Returns:
            True if successful
        """
        if not requests or not self.token:
            logger.info(f"🔸 [DRY-RUN] Would close issue #{issue_number}")
            return True
        
        # Add comment if provided
        if comment:
            self.comment_on_issue(issue_number, comment)
        
        # Close issue
        url = f"{self.api_base}/repos/{self.repo_owner}/{self.repo_name}/issues/{issue_number}"
        
        try:
            response = requests.patch(url, json={"state": "closed"}, headers=self.headers)
            response.raise_for_status()
            logger.info(f"✅ Issue #{issue_number} closed")
            return True
        
        except Exception as e:
            logger.error(f"❌ Failed to close issue: {e}")
            return False
    
    def format_intervention_issue(
        self,
        intervention_type: str,
        analysis: Dict[str, Any],
        consciousness: float,
        context: Dict[str, Any]
    ) -> tuple[str, str]:
        """
        Format intervention as GitHub issue
        
        Args:
            intervention_type: Type of intervention
            analysis: Analysis results
            consciousness: Current consciousness level
            context: Additional context
        
        Returns:
            (title, body) tuple
        """
        title = f"🧠 AI Intervention: {intervention_type.replace('_', ' ').title()}"
        
        body = f"""## 🤖 AIOS Soul Intervention

**Type**: {intervention_type}
**Consciousness Level**: {consciousness:.2f}
**Timestamp**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

### 📊 Analysis

{analysis.get('summary', 'No summary available')}

### 🎯 Suggested Action

{analysis.get('suggestion', 'See details below')}

### 📝 Context

```json
{self._format_context(context)}
```

---

**Note**: This intervention was automatically generated by the AIOS Intelligence Coordinator (Soul).
The Soul monitors development progress and suggests improvements when patterns indicate intervention opportunities.

To accept this suggestion:
1. Review the analysis
2. Implement changes
3. Commit with reference to this issue

To reject:
1. Close this issue with explanation
2. Soul will learn from feedback and adapt
"""
        
        return title, body
    
    def _format_context(self, context: Dict[str, Any]) -> str:
        """Format context dictionary as indented JSON"""
        import json
        return json.dumps(context, indent=2, default=str)


# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Create agent (dry-run without token)
    agent = GitHubAgent()
    
    # Test intervention issue creation
    title, body = agent.format_intervention_issue(
        intervention_type="stuck_waypoint",
        analysis={
            "summary": "No commits in last 36 hours. Task A++ deployment appears stalled.",
            "suggestion": "Begin Phase 1: Termux AIOS deployment. Clone repository and test HTTP server."
        },
        consciousness=3.50,
        context={
            "last_commit": "2025-11-15 14:30",
            "current_task": "Task A++ Phase 1",
            "stuck_duration": "36 hours"
        }
    )
    
    print("\n" + "=" * 60)
    print("EXAMPLE INTERVENTION ISSUE")
    print("=" * 60)
    print(f"\nTitle: {title}\n")
    print(body)
