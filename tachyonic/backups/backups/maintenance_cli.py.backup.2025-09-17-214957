#!/usr/bin/env python3
"""
AIOS Maintenance CLI - Command Line Interface for Tachyonic Operations
=====================================================================

This script provides a command-line interface for executing AIOS
maintenance operations with fractal/holographic development paradigm.
"""

import argparse
import sys
from pathlib import Path

# Add the maintenance module to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from maintenance.orchestrator import MaintenanceOrchestrator


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="AIOS Tachyonic Maintenance System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python maintenance_cli.py optimize              # Full optimization
  python maintenance_cli.py analyze               # Quick analysis
  python maintenance_cli.py search "api"          # Search archives
  python maintenance_cli.py restore HASH file.md  # Restore from archive
        """
    )

    parser.add_argument(
        "command",
        choices=["optimize", "analyze", "search", "restore", "quick_optimize", "get_archive_info", "status"],
        help="Maintenance operation to perform"
    )

    parser.add_argument(
        "query",
        nargs="?",
        help="Search query or content hash for restore"
    )

    parser.add_argument(
        "filename",
        nargs="?",
        help="Target filename for restore operation"
    )

    parser.add_argument(
        "--workspace",
        default="../../..",
        help="Path to AIOS workspace root (default: ../../..)"
    )

    parser.add_argument(
        "--category",
        help="Category filter for search operations"
    )

    parser.add_argument(
        "--no-report",
        action="store_true",
        help="Skip saving detailed report for optimize command"
    )

    args = parser.parse_args()

    # Resolve workspace path
    workspace_root = Path(__file__).parent / args.workspace
    workspace_root = workspace_root.resolve()

    if not workspace_root.exists():
        print(f" Workspace not found: {workspace_root}")
        sys.exit(1)

    print(f" Workspace: {workspace_root}")

    # Initialize orchestrator
    orchestrator = MaintenanceOrchestrator(str(workspace_root))

    # Execute command
    try:
        if args.command == "optimize":
            result = orchestrator.execute_full_optimization(
                save_report=not args.no_report
            )
            print_optimization_result(result)

        elif args.command == "analyze":
            result = orchestrator.quick_analysis()
            print_analysis_result(result)

        elif args.command == "search":
            if not args.query:
                print(" Search command requires a query")
                sys.exit(1)

            result = orchestrator.search_archives(args.query, args.category)
            print_search_result(result)

        elif args.command == "restore":
            if not args.query or not args.filename:
                print(" Restore command requires content hash and filename")
                sys.exit(1)

            result = orchestrator.restore_from_archive(args.query, args.filename)
            print_restore_result(result)

        elif args.command == "quick_optimize":
            result = orchestrator.execute_quick_optimization()
            print_quick_optimization_result(result)

        elif args.command == "get_archive_info":
            result = orchestrator.get_archive_info()
            print_archive_info(result)

        elif args.command == "status":
            result = orchestrator.get_system_status()
            print_system_status(result)

    except KeyboardInterrupt:
        print("\n Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f" Error: {e}")
        sys.exit(1)


def print_optimization_result(result: dict):
    """Print optimization results in a user-friendly format."""
    print("\n" + "="*60)
    print(" AIOS TACHYONIC OPTIMIZATION RESULTS")
    print("="*60)

    summary = result.get("summary", {})

    print(f" Optimization Complete: {summary.get('optimization_successful', False)}")
    print(f" Final File Count: {summary.get('final_file_count', 0)}")
    print(f" Fragmentation Score: {summary.get('fragmentation_score', 1.0):.3f}")
    print(f" Archived Documents: {summary.get('archive_documents', 0)}")
    print(f" Integrity Status: {summary.get('integrity_status', 'unknown')}")
    print(f" Core Document Coverage: {summary.get('core_document_coverage', 0):.1f}%")

    recommendations = result.get("recommendations", [])
    if recommendations:
        print("\n Recommendations:")
        for rec in recommendations:
            print(f"  {rec}")

    if "report_path" in result:
        print(f"\n Detailed report saved: {result['report_path']}")


def print_analysis_result(result: dict):
    """Print analysis results in a user-friendly format."""
    print("\n" + "="*50)
    print(" AIOS SYSTEM ANALYSIS")
    print("="*50)

    doc_analysis = result.get("documentation_analysis", {})
    archive_status = result.get("archive_status", {})

    print(f" Documentation Files: {doc_analysis.get('total_files', 0)}")
    print(f" Fragmentation Score: {doc_analysis.get('fragmentation_score', 1.0):.3f}")
    print(f" Archived Documents: {archive_status.get('total_documents', 0)}")
    print(f" Archive Size: {archive_status.get('total_size_bytes', 0)} bytes")

    recommendations = result.get("recommendations", [])
    if recommendations:
        print("\n Recommendations:")
        for rec in recommendations:
            print(f"  {rec}")


def print_search_result(result: dict):
    """Print search results in a user-friendly format."""
    print("\n" + "="*50)
    print(" ARCHIVE SEARCH RESULTS")
    print("="*50)

    print(f" Query: {result['query']}")
    if result.get('category_filter'):
        print(f" Category: {result['category_filter']}")
    print(f" Results: {result['results_count']} documents found")

    if result['results_count'] > 0:
        print("\n Matching Documents:")
        for i, doc in enumerate(result['results'][:10], 1):  # Show first 10
            print(f"  {i}. {doc['filename']}")
            print(f"     Hash: {doc['content_hash'][:16]}...")
            print(f"     Category: {doc['category']}")
            print(f"     Archived: {doc['archive_timestamp']}")
            print()

        if result['results_count'] > 10:
            print(f"  ... and {result['results_count'] - 10} more documents")


def print_restore_result(result: dict):
    """Print restore results in a user-friendly format."""
    print("\n" + "="*50)
    print(" CONTENT RESTORATION")
    print("="*50)

    if result['success']:
        print(f" Content successfully restored")
        print(f" File: {result['restore_path']}")
        print(f" Hash: {result['content_hash']}")
    else:
        print(f" Restoration failed")
        print(f" Hash: {result['content_hash']}")
        print(f" Error: {result['error']}")


def print_quick_optimization_result(result: dict):
    """Print quick optimization results in a user-friendly format."""
    print("\n" + "="*60)
    print(" AIOS QUICK OPTIMIZATION RESULTS")
    print("="*60)

    summary = result.get("summary", {})

    print(f" Quick Optimization Complete: {summary.get('optimization_successful', False)}")
    print(f" Optimized File Count: {summary.get('optimized_file_count', 0)}")
    print(f" Fragmentation Score: {summary.get('fragmentation_score', 1.0):.3f}")

    recommendations = result.get("recommendations", [])
    if recommendations:
        print("\n Recommendations:")
        for rec in recommendations:
            print(f"  {rec}")


def print_archive_info(result: dict):
    """Print archive information in a user-friendly format."""
    print("\n" + "="*50)
    print(" ARCHIVE INFORMATION")
    print("="*50)

    archive_info = result.get("archive_info", {})

    print(f" Total Documents: {archive_info.get('total_documents', 0)}")
    print(f" Total Size: {archive_info.get('total_size_bytes', 0)} bytes")
    print(f" Last Updated: {archive_info.get('last_updated', 'N/A')}")

    if archive_info.get('documents'):
        print("\n Documents:")
        for doc in archive_info['documents'][:10]:  # Show first 10 documents
            print(f"  - {doc['filename']} (Hash: {doc['content_hash'][:16]}...)")

        if len(archive_info['documents']) > 10:
            print(f"  ... and {len(archive_info['documents']) - 10} more documents")


def print_system_status(result: dict):
    """Print system status in a user-friendly format."""
    print("\n" + "="*50)
    print(" SYSTEM STATUS")
    print("="*50)

    status = result.get("status", {})

    print(f" Optimization Enabled: {status.get('optimization_enabled', False)}")
    print(f" Current Fragmentation: {status.get('current_fragmentation', 0)}%")
    print(f" Archived Documents: {status.get('archived_documents', 0)}")
    print(f" Last Optimization: {status.get('last_optimization', 'N/A')}")
    print(f" Next Scheduled Task: {status.get('next_scheduled_task', 'N/A')}")

    if "issues" in status and status["issues"]:
        print("\n Issues Detected:")
        for issue in status["issues"]:
            print(f"  - {issue}")


if __name__ == "__main__":
    main()
