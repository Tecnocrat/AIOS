#!/usr/bin/env python3
"""
AIOS Token Usage Tracker
Monitors and analyzes AI conversation token consumption patterns

Tracks token usage across GitHub Copilot sessions to understand:
- Total tokens consumed per session
- Token consumption rate over time
- Efficiency metrics (tokens per operation)
- Cost projections and budget management
"""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
import statistics


@dataclass
class TokenSnapshot:
    """Single point-in-time token measurement"""
    timestamp: str
    tokens_used: int
    tokens_remaining: int
    total_budget: int
    percentage_used: float
    operation_context: str
    
    @property
    def tokens_per_second(self) -> Optional[float]:
        """Calculate consumption rate if we have time data"""
        return None  # Calculated in analysis phase


@dataclass
class TokenSession:
    """Complete token usage session"""
    session_id: str
    start_time: str
    end_time: Optional[str]
    total_budget: int
    snapshots: List[TokenSnapshot]
    
    @property
    def total_tokens_used(self) -> int:
        """Total tokens consumed in session"""
        if not self.snapshots:
            return 0
        return self.snapshots[-1].tokens_used
    
    @property
    def efficiency_score(self) -> float:
        """Calculate efficiency (operations per 1000 tokens)"""
        if not self.snapshots or self.total_tokens_used == 0:
            return 0.0
        operations = len(self.snapshots)
        return (operations / self.total_tokens_used) * 1000
    
    @property
    def average_tokens_per_operation(self) -> float:
        """Average tokens consumed per operation"""
        if not self.snapshots:
            return 0.0
        return self.total_tokens_used / len(self.snapshots)


class TokenUsageTracker:
    """Track and analyze token consumption patterns"""
    
    def __init__(self, archive_path: Path = None):
        """Initialize token usage tracker"""
        if archive_path is None:
            archive_path = Path(__file__).parent.parent / "logs" / "token_usage"
        
        self.archive_path = Path(archive_path)
        self.archive_path.mkdir(parents=True, exist_ok=True)
        
        self.current_session: Optional[TokenSession] = None
    
    def parse_system_warning(self, warning_text: str) -> Optional[TokenSnapshot]:
        """
        Parse token usage from system warning messages
        
        Expected format: "Token usage: 98786/1000000; 901214 remaining"
        """
        pattern = r"Token usage: (\d+)/(\d+); (\d+) remaining"
        match = re.search(pattern, warning_text)
        
        if not match:
            return None
        
        tokens_used = int(match.group(1))
        total_budget = int(match.group(2))
        tokens_remaining = int(match.group(3))
        
        percentage = (tokens_used / total_budget) * 100
        
        return TokenSnapshot(
            timestamp=datetime.now().isoformat(),
            tokens_used=tokens_used,
            tokens_remaining=tokens_remaining,
            total_budget=total_budget,
            percentage_used=round(percentage, 2),
            operation_context="unknown"
        )
    
    def start_session(self, session_id: str, total_budget: int = 1000000):
        """Start new token tracking session"""
        self.current_session = TokenSession(
            session_id=session_id,
            start_time=datetime.now().isoformat(),
            end_time=None,
            total_budget=total_budget,
            snapshots=[]
        )
        
        print(f"🔵 Token tracking session started: {session_id}")
        print(f"📊 Total budget: {total_budget:,} tokens")
    
    def record_snapshot(self, snapshot: TokenSnapshot):
        """Record token usage snapshot"""
        if not self.current_session:
            raise ValueError("No active session. Call start_session() first.")
        
        self.current_session.snapshots.append(snapshot)
        
        # Auto-save every 10 snapshots
        if len(self.current_session.snapshots) % 10 == 0:
            self._save_session()
    
    def record_from_warning(self, warning_text: str, operation: str = "unknown"):
        """Record snapshot from system warning text"""
        snapshot = self.parse_system_warning(warning_text)
        if snapshot:
            snapshot.operation_context = operation
            self.record_snapshot(snapshot)
    
    def end_session(self) -> Dict:
        """End current session and generate report"""
        if not self.current_session:
            raise ValueError("No active session to end.")
        
        self.current_session.end_time = datetime.now().isoformat()
        
        # Generate final report
        report = self._generate_session_report()
        
        # Save session
        self._save_session()
        
        # Clear current session
        self.current_session = None
        
        return report
    
    def _generate_session_report(self) -> Dict:
        """Generate comprehensive session report"""
        if not self.current_session:
            return {}
        
        session = self.current_session
        snapshots = session.snapshots
        
        if not snapshots:
            return {
                "session_id": session.session_id,
                "status": "no_data",
                "total_tokens_used": 0
            }
        
        # Calculate consumption rate
        token_deltas = []
        for i in range(1, len(snapshots)):
            delta = snapshots[i].tokens_used - snapshots[i-1].tokens_used
            token_deltas.append(delta)
        
        report = {
            "session_id": session.session_id,
            "start_time": session.start_time,
            "end_time": session.end_time,
            "total_budget": session.total_budget,
            "total_tokens_used": session.total_tokens_used,
            "tokens_remaining": session.total_budget - session.total_tokens_used,
            "percentage_used": round((session.total_tokens_used / session.total_budget) * 100, 2),
            "total_operations": len(snapshots),
            "efficiency_score": round(session.efficiency_score, 2),
            "average_tokens_per_operation": round(session.average_tokens_per_operation, 2),
            "token_consumption_stats": {
                "min_delta": min(token_deltas) if token_deltas else 0,
                "max_delta": max(token_deltas) if token_deltas else 0,
                "median_delta": statistics.median(token_deltas) if token_deltas else 0,
                "mean_delta": statistics.mean(token_deltas) if token_deltas else 0
            },
            "cost_projection": self._calculate_cost_projection(session.total_tokens_used),
            "snapshots": [asdict(s) for s in snapshots[-10:]]  # Last 10 snapshots
        }
        
        return report
    
    def _calculate_cost_projection(self, tokens_used: int) -> Dict:
        """
        Calculate cost projections
        
        Note: GitHub Copilot pricing is different from standard Claude API
        This is for reference/comparison only
        """
        # Standard Claude Sonnet 3.5 pricing (for comparison)
        INPUT_COST_PER_MTK = 3.00  # $3 per million tokens
        OUTPUT_COST_PER_MTK = 15.00  # $15 per million tokens
        
        # Assume 50/50 input/output split (rough estimate)
        input_tokens = tokens_used * 0.5
        output_tokens = tokens_used * 0.5
        
        cost_input = (input_tokens / 1_000_000) * INPUT_COST_PER_MTK
        cost_output = (output_tokens / 1_000_000) * OUTPUT_COST_PER_MTK
        total_cost = cost_input + cost_output
        
        return {
            "estimated_input_tokens": int(input_tokens),
            "estimated_output_tokens": int(output_tokens),
            "estimated_cost_usd": round(total_cost, 4),
            "note": "GitHub Copilot uses different pricing model",
            "github_copilot_monthly": 10.00,
            "sessions_per_month_estimate": 10  # Assuming 1M tokens per session
        }
    
    def _save_session(self):
        """Save current session to archive"""
        if not self.current_session:
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"token_session_{self.current_session.session_id}_{timestamp}.json"
        filepath = self.archive_path / filename
        
        report = self._generate_session_report()
        
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)
        
        # Also save as latest
        latest_path = self.archive_path / "token_session_latest.json"
        with open(latest_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"💾 Session saved: {filepath.name}")
    
    def analyze_historical_sessions(self) -> Dict:
        """Analyze all historical token usage sessions"""
        session_files = sorted(self.archive_path.glob("token_session_*.json"))
        
        if not session_files:
            return {"status": "no_historical_data"}
        
        sessions_data = []
        for session_file in session_files:
            if "latest" in session_file.name:
                continue
            with open(session_file, 'r') as f:
                sessions_data.append(json.load(f))
        
        if not sessions_data:
            return {"status": "no_historical_data"}
        
        total_tokens = sum(s.get("total_tokens_used", 0) for s in sessions_data)
        total_operations = sum(s.get("total_operations", 0) for s in sessions_data)
        
        analysis = {
            "total_sessions": len(sessions_data),
            "total_tokens_consumed": total_tokens,
            "total_operations": total_operations,
            "average_tokens_per_session": round(total_tokens / len(sessions_data), 2),
            "average_operations_per_session": round(total_operations / len(sessions_data), 2),
            "most_efficient_session": max(sessions_data, key=lambda s: s.get("efficiency_score", 0)),
            "most_expensive_session": max(sessions_data, key=lambda s: s.get("total_tokens_used", 0)),
            "archive_path": str(self.archive_path)
        }
        
        return analysis


def demo_usage():
    """Demonstrate token usage tracking"""
    tracker = TokenUsageTracker()
    
    # Start session
    tracker.start_session("demo_20251021", total_budget=1000000)
    
    # Simulate some operations with token warnings
    example_warnings = [
        ("Token usage: 52736/1000000; 947264 remaining", "initial_context_load"),
        ("Token usage: 65206/1000000; 934794 remaining", "dev_path_discovery"),
        ("Token usage: 81645/1000000; 918355 remaining", "semantic_search"),
        ("Token usage: 98786/1000000; 901214 remaining", "git_operations"),
    ]
    
    for warning, operation in example_warnings:
        tracker.record_from_warning(warning, operation)
    
    # End session and get report
    report = tracker.end_session()
    
    print("\n" + "="*60)
    print("📊 TOKEN USAGE REPORT")
    print("="*60)
    print(f"Session ID: {report['session_id']}")
    print(f"Total Tokens Used: {report['total_tokens_used']:,} / {report['total_budget']:,}")
    print(f"Percentage Used: {report['percentage_used']}%")
    print(f"Total Operations: {report['total_operations']}")
    print(f"Efficiency Score: {report['efficiency_score']} ops/1K tokens")
    print(f"Avg Tokens/Operation: {report['average_tokens_per_operation']:,.0f}")
    print(f"\nEstimated Cost (Claude API): ${report['cost_projection']['estimated_cost_usd']}")
    print(f"GitHub Copilot: ${report['cost_projection']['github_copilot_monthly']}/month")
    print("="*60)


if __name__ == "__main__":
    demo_usage()
