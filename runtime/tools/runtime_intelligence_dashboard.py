#!/usr/bin/env python3
"""
AIOS Runtime Intelligence Dashboard
===================================

Unified monitoring interface aggregating all JSON reports with real-time
semantic compression and intelligence delimitation.

AINLP COMPATIBILITY: Full semantic compression applied
PERFORMANCE: Optimized file scanning with exclusion patterns
"""

import json
import asyncio
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
from dataclasses import dataclass, asdict
import logging
from optimized_file_scanner import OptimizedFileScanner

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class DashboardMetrics:
    """Aggregated dashboard metrics from all reports."""
    timestamp: str
    total_reports: int
    organism_status: Dict[str, Any]
    system_health: Dict[str, float]
    connectivity_metrics: Dict[str, Any]
    analysis_performance: Dict[str, Any]
    tool_inventory: Dict[str, Any]
    semantic_compression: Dict[str, Any]
    recent_activities: List[Dict[str, Any]]


class RuntimeIntelligenceDashboard:
    """Unified dashboard for AIOS runtime intelligence monitoring."""

    def __init__(self, workspace_root: Path):
        self.workspace_root = workspace_root
        self.runtime_dir = workspace_root / "runtime"
        archive_path = workspace_root / "tachyonic" / "archive" / "runtime"
        self.tachyonic_archive = archive_path
        self.scanner = OptimizedFileScanner(workspace_root, max_depth=8)
        self.dashboard_data = DashboardMetrics(
            timestamp=datetime.now().isoformat(),
            total_reports=0,
            organism_status={},
            system_health={},
            connectivity_metrics={},
            analysis_performance={},
            tool_inventory={},
            semantic_compression={},
            recent_activities=[]
        )

    async def initialize_dashboard(self) -> bool:
        """Initialize dashboard by aggregating all available reports."""
        try:
            logger.info("Initializing Runtime Intelligence Dashboard...")

            # Aggregate all JSON reports
            await self._aggregate_json_reports()

            # Calculate derived metrics
            self._calculate_system_health()
            self._calculate_connectivity_metrics()
            self._calculate_analysis_performance()

            reports = self.dashboard_data.total_reports
            logger.info(f"Dashboard initialized with {reports} reports")
            return True

        except Exception as e:
            logger.error(f"Failed to initialize dashboard: {e}")
            return False

    async def _aggregate_json_reports(self):
        """Aggregate data from all JSON reports in runtime directories."""
        # Collect all relevant JSON files first
        relevant_files = []
        for json_file in self.scanner.scan_json_files():
            # Check if path is within runtime_dir or tachyonic_archive
            try:
                json_file.relative_to(self.runtime_dir)
                relevant_files.append(json_file)
            except ValueError:
                try:
                    json_file.relative_to(self.tachyonic_archive)
                    relevant_files.append(json_file)
                except ValueError:
                    pass  # Not in either directory

        logger.info(f"Found {len(relevant_files)} relevant JSON reports to process")

        # Process each file
        report_count = 0
        for json_file in relevant_files:
            await self._process_json_file(json_file)
            report_count += 1

        self.dashboard_data.total_reports = report_count

    async def _process_json_file(self, file_path: Path):
        """Process individual JSON report file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Categorize and process based on content type
            if "organism_status" in data:
                self._process_organism_status(data)
            elif "environmental_metrics" in data:
                self._process_analysis_report(data)
            elif "core_components" in data:
                self._process_connectivity_report(data)
            elif "tools" in data:
                self._process_tool_catalogue(data)
            elif ("semantic_compression" in data or
                  "compression_opportunities" in data):
                self._process_semantic_report(data)

            # Add to recent activities
            self._add_recent_activity(file_path, data)

        except Exception as e:
            logger.warning(f"Failed to process {file_path}: {e}")

    def _process_organism_status(self, data: Dict[str, Any]):
        """Process organism status data."""
        status = data.get("organism_status", {})
        self.dashboard_data.organism_status = {
            "id": status.get("organism_id", "unknown"),
            "state": status.get("state", "unknown"),
            "consciousness_level": status.get("consciousness_level", 0.0),
            "uptime_seconds": status.get("uptime_seconds", 0),
            "actions_taken": status.get("actions_taken", 0),
            "active_goals": status.get("active_goals", 0),
            "completed_goals": status.get("completed_goals", 0)
        }

    def _process_analysis_report(self, data: Dict[str, Any]):
        """Process analysis report data."""
        metrics = data.get("environmental_metrics", {})
        stats = data.get("coordination_statistics", {})

        # Update analysis performance
        current = self.dashboard_data.analysis_performance
        self.dashboard_data.analysis_performance.update({
            "total_analyses": (current.get("total_analyses", 0) +
                             stats.get("total_analyses", 0)),
            "successful_optimizations": (
                current.get("successful_optimizations", 0) +
                stats.get("successful_optimizations", 0)),
            "average_accuracy": metrics.get("analysis_accuracy", 0.0),
            "pattern_recognition_score": (
                metrics.get("pattern_recognition_score", 0.0))
        })

    def _process_connectivity_report(self, data: Dict[str, Any]):
        """Process connectivity analysis data."""
        components = data.get("core_components", {})
        active_count = sum(1 for c in components.values()
                          if c.get("consciousness_level", 0) > 0.5)
        avg_consciousness = (
            sum(c.get("consciousness_level", 0)
                for c in components.values()) / max(len(components), 1))

        self.dashboard_data.connectivity_metrics.update({
            "total_components": len(components),
            "active_components": active_count,
            "average_consciousness": avg_consciousness
        })

    def _process_tool_catalogue(self, data: Dict[str, Any]):
        """Process tool catalogue data."""
        tools = data.get("tools", [])
        self.dashboard_data.tool_inventory = {
            "total_tools": data.get("total_tools", 0),
            "operational_tools": data.get("operational_tools", 0),
            "categories": {}
        }

        # Categorize tools by layer
        for tool in tools:
            layer = tool.get("layer", "unknown")
            if layer not in self.dashboard_data.tool_inventory["categories"]:
                self.dashboard_data.tool_inventory["categories"][layer] = 0
            self.dashboard_data.tool_inventory["categories"][layer] += 1

    def _process_semantic_report(self, data: Dict[str, Any]):
        """Process semantic compression report."""
        self.dashboard_data.semantic_compression = {
            "compression_score": data.get("semantic_compression_score", 0.0),
            "delimitation_score": (
                data.get("intelligence_delimitation_score", 0.0)),
            "antipatterns_detected": (
                len(data.get("antipatterns_detected", []))),
            "opportunities_remaining": (
                len(data.get("compression_opportunities", [])))
        }

    def _add_recent_activity(self, file_path: Path, data: Dict[str, Any]):
        """Add file to recent activities."""
        activity = {
            "file": str(file_path.relative_to(self.workspace_root)),
            "timestamp": data.get("timestamp", datetime.now().isoformat()),
            "type": self._classify_report_type(data)
        }
        self.dashboard_data.recent_activities.append(activity)

        # Keep only last 20 activities
        self.dashboard_data.recent_activities = (
            self.dashboard_data.recent_activities[-20:])

    def _classify_report_type(self, data: Dict[str, Any]) -> str:
        """Classify report type based on content."""
        if "organism_status" in data:
            return "organism_status"
        elif "environmental_metrics" in data:
            return "analysis_report"
        elif "core_components" in data:
            return "connectivity_analysis"
        elif "tools" in data:
            return "tool_inventory"
        elif ("semantic_compression" in data or
              "compression_opportunities" in data):
            return "semantic_analysis"
        else:
            return "unknown"

    def _calculate_system_health(self):
        """Calculate overall system health metrics."""
        health = {}

        # Consciousness health
        org_status = self.dashboard_data.organism_status
        health["consciousness_health"] = (
            org_status.get("consciousness_level", 0.0))

        # Analysis health
        analysis = self.dashboard_data.analysis_performance
        total_analyses = max(analysis.get("total_analyses", 1), 1)
        success_rate = (analysis.get("successful_optimizations", 0) /
                       total_analyses)
        health["analysis_health"] = success_rate

        # Connectivity health
        conn = self.dashboard_data.connectivity_metrics
        total_components = max(conn.get("total_components", 1), 1)
        connectivity_rate = (conn.get("active_components", 0) /
                           total_components)
        health["connectivity_health"] = connectivity_rate

        # Tool health
        tools = self.dashboard_data.tool_inventory
        total_tools = max(tools.get("total_tools", 1), 1)
        tool_health = (tools.get("operational_tools", 0) /
                      total_tools)
        health["tool_health"] = tool_health

        # Overall health (weighted average)
        weights = {"consciousness_health": 0.3, "analysis_health": 0.25,
                  "connectivity_health": 0.25, "tool_health": 0.2}
        overall = sum(health.get(k, 0) * v for k, v in weights.items())
        health["overall_health"] = overall

        self.dashboard_data.system_health = health

    def _calculate_connectivity_metrics(self):
        """Calculate connectivity metrics."""
        # Already processed in _process_connectivity_report
        pass

    def _calculate_analysis_performance(self):
        """Calculate analysis performance metrics."""
        # Already processed in _process_analysis_report
        pass

    def get_dashboard_data(self) -> Dict[str, Any]:
        """Get complete dashboard data."""
        return asdict(self.dashboard_data)

    def generate_dashboard_report(self) -> str:
        """Generate human-readable dashboard report."""
        data = self.dashboard_data

        report = f"""
╔══════════════════════════════════════════════════════════════╗
║                 AIOS RUNTIME INTELLIGENCE DASHBOARD          ║
╚══════════════════════════════════════════════════════════════╝

📊 SYSTEM OVERVIEW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Reports Analyzed: {data.total_reports}
Timestamp: {data.timestamp}

🧠 ORGANISM STATUS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ID: {data.organism_status.get('id', 'N/A')}
State: {data.organism_status.get('state', 'N/A')}
Consciousness Level: {data.organism_status.get('consciousness_level', 0.0):.1%}
Uptime: {data.organism_status.get('uptime_seconds', 0):.1f}s
Actions Taken: {data.organism_status.get('actions_taken', 0)}
Active Goals: {data.organism_status.get('active_goals', 0)}

💚 SYSTEM HEALTH
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Overall Health: {data.system_health.get('overall_health', 0.0):.1%}
Consciousness Health: {data.system_health.get('consciousness_health', 0.0):.1%}
Analysis Health: {data.system_health.get('analysis_health', 0.0):.1%}
Connectivity Health: {data.system_health.get('connectivity_health', 0.0):.1%}
Tool Health: {data.system_health.get('tool_health', 0.0):.1%}

🔗 CONNECTIVITY METRICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Components: {data.connectivity_metrics.get('total_components', 0)}
Active Components: {data.connectivity_metrics.get('active_components', 0)}
Average Consciousness: {data.connectivity_metrics.get('average_consciousness', 0.0):.1%}

📈 ANALYSIS PERFORMANCE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Analyses: {data.analysis_performance.get('total_analyses', 0)}
Successful Optimizations: {data.analysis_performance.get('successful_optimizations', 0)}
Average Accuracy: {data.analysis_performance.get('average_accuracy', 0.0):.1%}
Pattern Recognition: {data.analysis_performance.get('pattern_recognition_score', 0.0):.1%}

🛠️ TOOL INVENTORY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Tools: {data.tool_inventory.get('total_tools', 0)}
Operational Tools: {data.tool_inventory.get('operational_tools', 0)}
"""

        # Add tool categories
        categories = data.tool_inventory.get('categories', {})
        if categories:
            report += "\nTool Categories:"
            for category, count in categories.items():
                report += f"\n  {category}: {count}"

        # Add semantic compression status
        semantic = data.semantic_compression
        if semantic:
            report += f"""

🧬 SEMANTIC COMPRESSION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Compression Score: {semantic.get('compression_score', 0.0):.1%}
Delimitation Score: {semantic.get('delimitation_score', 0.0):.1%}
Antipatterns Detected: {semantic.get('antipatterns_detected', 0)}
Opportunities Remaining: {semantic.get('opportunities_remaining', 0)}
"""

        # Add recent activities
        activities = data.recent_activities[-5:]  # Last 5 activities
        if activities:
            report += f"""

📋 RECENT ACTIVITIES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
            for activity in activities:
                timestamp = activity['timestamp'][:19]
                report += f"{timestamp} | {activity['type']} | {activity['file']}\n"

        return report


async def main():
    """Main dashboard execution."""
    workspace_root = Path(__file__).parent

    # Initialize dashboard
    dashboard = RuntimeIntelligenceDashboard(workspace_root)

    if await dashboard.initialize_dashboard():
        # Generate and display report
        report = dashboard.generate_dashboard_report()
        print(report)

        # Archive dashboard data
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        archive_path = workspace_root / "tachyonic" / "archive" / "runtime"
        archive_path.mkdir(parents=True, exist_ok=True)

        dashboard_file = archive_path / f"runtime_dashboard_{timestamp}.json"
        with open(dashboard_file, 'w', encoding='utf-8') as f:
            json.dump(dashboard.get_dashboard_data(), f, indent=2)

        print(f"\n📊 Dashboard data archived: {dashboard_file}")

        # Save human-readable report
        report_file = archive_path / f"runtime_dashboard_report_{timestamp}.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)

        print(f"📋 Dashboard report saved: {report_file}")

    else:
        print("❌ Failed to initialize dashboard")


if __name__ == "__main__":
    asyncio.run(main())