"""
AIOS Maintenance Orchestrator - Fractal/Holographic Development Engine
=====================================================================

This module provides the main interface for executing comprehensive
maintenance operations using the tachyonic paradigm.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

from .backup_consolidator import BackupConsolidator
from .documentation_optimizer import DocumentationOptimizer
from .garbage_collector import GarbageCollector
from .tachyonic_archiver import TachyonicArchiver


class MaintenanceOrchestrator:
    """
    Central orchestrator for all AIOS maintenance operations.

    Implements fractal/holographic principles where each maintenance
    operation contains the essence of the whole system's evolution.
    """

    def __init__(self, workspace_root: str):
        self.workspace_root = Path(workspace_root)
        self.reports_path = self.workspace_root / "ai" / "maintenance_reports"
        self.reports_path.mkdir(parents=True, exist_ok=True)

        # Initialize all subsystems
        self.garbage_collector = GarbageCollector(workspace_root)
        self.optimizer = DocumentationOptimizer(workspace_root)
        self.consolidator = BackupConsolidator(workspace_root)
        self.archiver = TachyonicArchiver(workspace_root)

    def execute_full_optimization(self, save_report: bool = True) -> Dict:
        """
        Execute complete system optimization with tachyonic preservation.

        Args:
            save_report: Whether to save detailed report to file

        Returns:
            Dict containing comprehensive optimization results
        """
        print("🚀 Initiating AIOS Tachyonic Optimization...")

        optimization_result = {
            "session_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "timestamp": datetime.now().isoformat(),
            "operation": "full_system_optimization",
            "phases": {},
            "summary": {},
            "recommendations": []
        }

        try:
            # Execute garbage collection cycle
            print("📊 Running comprehensive optimization cycle...")
            gc_result = self.garbage_collector.run_full_optimization()
            optimization_result["phases"]["garbage_collection"] = gc_result

            # Verify system integrity
            print("🔍 Verifying system integrity...")
            integrity_result = self.garbage_collector.verify_integrity()
            optimization_result["phases"]["integrity_verification"] = integrity_result

            # Generate summary
            optimization_result["summary"] = self._generate_summary(
                gc_result,
                integrity_result
            )

            # Generate recommendations
            optimization_result["recommendations"] = self._generate_recommendations(
                gc_result,
                integrity_result
            )

            print("✅ Optimization complete!")

        except Exception as e:
            optimization_result["error"] = str(e)
            print(f"❌ Optimization failed: {e}")

        # Save report if requested
        if save_report:
            report_path = self._save_optimization_report(optimization_result)
            optimization_result["report_path"] = str(report_path)
            print(f"📄 Report saved: {report_path}")

        return optimization_result

    def execute_quick_optimization(self) -> Dict:
        """
        Execute lightweight optimization for routine maintenance.

        Performs essential documentation cleanup without full archival.

        Returns:
            Dict containing quick optimization results
        """
        print("⚡ Running AIOS Quick Optimization...")

        start_time = datetime.now()
        results = {
            "operation": "quick_optimization",
            "start_time": start_time.isoformat(),
            "steps": []
        }

        try:
            # Step 1: Quick documentation analysis
            print("📊 Analyzing documentation structure...")
            analysis = self.optimizer.analyze_documentation_structure()
            results["steps"].append({
                "step": "analysis",
                "status": "completed",
                "details": f"Found {analysis.get('total_files', 0)} files, {analysis.get('fragmentation_score', 0):.1f} fragmentation score"
            })

            # Step 2: Light optimization (only if needed)
            if analysis.get('fragmentation_score', 0) > 0.3:
                print("🔧 Running lightweight optimization...")
                opt_result = self.optimizer.optimize_with_minimal_changes()
                results["steps"].append({
                    "step": "optimization",
                    "status": "completed",
                    "details": f"Optimized {opt_result.get('files_processed', 0)} files"
                })
            else:
                print("✅ Documentation already optimized")
                results["steps"].append({
                    "step": "optimization",
                    "status": "skipped",
                    "details": "No optimization needed"
                })

            # Step 3: Update metadata
            print("📝 Updating system metadata...")
            metadata = self._update_maintenance_metadata("quick_optimization")
            results["steps"].append({
                "step": "metadata_update",
                "status": "completed",
                "details": "Metadata updated"
            })

            # Final status
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()

            results.update({
                "status": "success",
                "end_time": end_time.isoformat(),
                "duration_seconds": duration,
                "message": f"Quick optimization completed in {duration:.1f} seconds"
            })

            print(f"✅ Quick optimization completed in {duration:.1f} seconds")
            return results

        except Exception as e:
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()

            results.update({
                "status": "error",
                "end_time": end_time.isoformat(),
                "duration_seconds": duration,
                "error": str(e),
                "message": f"Quick optimization failed: {str(e)}"
            })

            print(f"❌ Quick optimization failed: {e}")
            return results

    def quick_analysis(self) -> Dict:
        """
        Perform quick system analysis without modifications.

        Returns:
            Dict containing analysis results
        """
        print("🔍 Running quick system analysis...")

        analysis_result = {
            "timestamp": datetime.now().isoformat(),
            "operation": "quick_analysis",
            "documentation_analysis": {},
            "archive_status": {},
            "recommendations": []
        }

        # Documentation analysis
        analysis_result["documentation_analysis"] = (
            self.optimizer.analyze_documentation_structure()
        )

        # Archive status
        analysis_result["archive_status"] = (
            self.archiver.get_archive_statistics()
        )

        # Quick recommendations
        doc_analysis = analysis_result["documentation_analysis"]
        fragmentation = doc_analysis.get("fragmentation_score", 0.0)

        if fragmentation > 0.5:
            analysis_result["recommendations"].append(
                "High documentation fragmentation detected. Consider running full optimization."
            )

        if fragmentation == 0.0:
            analysis_result["recommendations"].append(
                "Documentation structure is optimal. System is well-maintained."
            )

        print("✅ Analysis complete!")
        return analysis_result

    def search_archives(self, query: str, category: Optional[str] = None) -> Dict:
        """
        Search tachyonic archives for specific content.

        Args:
            query: Search query string
            category: Optional category filter

        Returns:
            Dict containing search results
        """
        print(f"🔍 Searching archives for: {query}")

        search_results = self.archiver.search_archive(query, category)

        result = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "category_filter": category,
            "results_count": len(search_results),
            "results": search_results
        }

        print(f"📋 Found {len(search_results)} matching documents")
        return result

    def restore_from_archive(self, content_hash: str,
                           target_filename: str) -> Dict:
        """
        Restore content from tachyonic archive.

        Args:
            content_hash: SHA-256 hash of content to restore
            target_filename: Filename for restored content

        Returns:
            Dict containing restoration result
        """
        print(f"🔄 Restoring content: {content_hash[:8]}...")

        content = self.archiver.retrieve_content(content_hash)

        if content is None:
            return {
                "success": False,
                "error": "Content not found in archive",
                "content_hash": content_hash
            }

        # Restore to docs directory
        restore_path = self.workspace_root / "docs" / target_filename

        try:
            with open(restore_path, 'w', encoding='utf-8') as f:
                f.write(content)

            print(f"✅ Content restored to: {restore_path}")

            return {
                "success": True,
                "restore_path": str(restore_path),
                "content_hash": content_hash,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "content_hash": content_hash
            }

    def get_archive_info(self) -> Dict:
        """
        Get comprehensive information about the tachyonic archive.

        Returns:
            Dict containing archive statistics and metadata
        """
        try:
            archive_stats = self.archiver.get_archive_statistics()
            archive_path = self.workspace_root / "docs" / "tachyonic_archive.db"

            info = {
                "total_files": archive_stats.get("total_entries", 0),
                "total_size": self._format_file_size(archive_stats.get("total_size", 0)),
                "last_archive": archive_stats.get("last_archive_time", "Never"),
                "archive_path": str(archive_path),
                "database_exists": archive_path.exists(),
                "categories": archive_stats.get("categories", {})
            }

            return info

        except Exception as e:
            return {
                "total_files": -1,
                "total_size": "Error",
                "last_archive": "Error",
                "archive_path": f"Error: {str(e)}",
                "database_exists": False,
                "categories": {}
            }

    def _generate_summary(self, gc_result: Dict, integrity_result: Dict) -> Dict:
        """Generate optimization summary."""
        final_state = gc_result.get("final_state", {})
        doc_structure = final_state.get("documentation_structure", {})

        return {
            "optimization_successful": final_state.get("optimization_complete", False),
            "final_file_count": doc_structure.get("total_files", 0),
            "fragmentation_score": doc_structure.get("fragmentation_score", 1.0),
            "archive_documents": final_state.get("archive_statistics", {}).get("total_documents", 0),
            "integrity_status": integrity_result.get("overall_status", "unknown"),
            "core_document_coverage": integrity_result.get("core_documents_check", {}).get("coverage_percentage", 0)
        }

    def _generate_recommendations(self, gc_result: Dict,
                                integrity_result: Dict) -> list:
        """Generate recommendations based on results."""
        recommendations = []

        # Check integrity status
        integrity_status = integrity_result.get("overall_status", "unknown")

        if integrity_status == "optimal":
            recommendations.append(
                "✅ System is in optimal state. Maintain current structure."
            )
        elif integrity_status == "acceptable":
            recommendations.append(
                "⚠️ System is acceptable but could be improved. Monitor closely."
            )
        else:
            recommendations.append(
                "❌ System needs attention. Consider manual review."
            )

        # Check fragmentation
        final_state = gc_result.get("final_state", {})
        fragmentation = final_state.get("documentation_structure", {}).get("fragmentation_score", 1.0)

        if fragmentation < 0.1:
            recommendations.append(
                "📚 Documentation structure is perfectly optimized."
            )
        elif fragmentation > 0.5:
            recommendations.append(
                "📚 Consider running additional optimization cycles."
            )

        return recommendations

    def _save_optimization_report(self, result: Dict) -> Path:
        """Save optimization report to file."""
        session_id = result.get("session_id", "unknown")
        report_filename = f"optimization_report_{session_id}.json"
        report_path = self.reports_path / report_filename

        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        return report_path

    def _format_file_size(self, size_bytes: int) -> str:
        """Format file size in human-readable format."""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        elif size_bytes < 1024 * 1024 * 1024:
            return f"{size_bytes / (1024 * 1024):.1f} MB"
        else:
            return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"

    def _update_maintenance_metadata(self, operation_type: str) -> Dict:
        """Update maintenance metadata with latest operation info."""
        metadata_file = self.workspace_root / "ai" / "maintenance_metadata.json"

        try:
            if metadata_file.exists():
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
            else:
                metadata = {"operations": [], "last_update": None}

            # Add new operation
            metadata["operations"].append({
                "type": operation_type,
                "timestamp": datetime.now().isoformat(),
                "version": "1.0.0"
            })

            # Keep only last 50 operations
            metadata["operations"] = metadata["operations"][-50:]
            metadata["last_update"] = datetime.now().isoformat()

            # Save metadata
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)

            return metadata

        except Exception as e:
            print(f"Warning: Could not update metadata: {e}")
            return {}

    def get_system_status(self) -> Dict:
        """
        Get comprehensive system status for maintenance monitoring.

        Returns:
            Dict containing current system health and maintenance status
        """
        try:
            # Get documentation analysis
            doc_analysis = self.optimizer.analyze_documentation_structure()

            # Get archive info
            archive_info = self.get_archive_info()

            # Get maintenance metadata
            metadata_file = self.workspace_root / "ai" / "maintenance_metadata.json"
            metadata = {}
            if metadata_file.exists():
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)

            # Compile status
            status = {
                "timestamp": datetime.now().isoformat(),
                "system_health": "healthy",
                "documentation_status": {
                    "total_files": doc_analysis.get("total_files", 0),
                    "fragmentation_score": doc_analysis.get("fragmentation_score", 0),
                    "categories": doc_analysis.get("categories", {})
                },
                "archive_status": {
                    "total_archived": archive_info.get("total_files", 0),
                    "archive_size": archive_info.get("total_size", "0 B"),
                    "last_archive": archive_info.get("last_archive", "Never")
                },
                "maintenance_history": {
                    "last_operation": metadata.get("operations", [])[-1] if metadata.get("operations") else None,
                    "operation_count": len(metadata.get("operations", [])),
                    "last_update": metadata.get("last_update", "Never")
                },
                "optimization_enabled": True,
                "current_fragmentation": round(doc_analysis.get("fragmentation_score", 0) * 100, 1)
            }

            # Determine overall health
            frag_score = doc_analysis.get("fragmentation_score", 0)
            if frag_score > 0.7:
                status["system_health"] = "critical"
            elif frag_score > 0.4:
                status["system_health"] = "warning"
            else:
                status["system_health"] = "healthy"

            return status

        except Exception as e:
            return {
                "timestamp": datetime.now().isoformat(),
                "system_health": "error",
                "error": str(e),
                "message": f"Status check failed: {str(e)}"
            }
