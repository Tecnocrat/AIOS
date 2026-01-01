#!/usr/bin/env python3
"""
AIOS Maintenance Service Bridge
===============================

This script provides a bridge between the C# MaintenanceService
and the Python maintenance modules. It accepts JSON commands
and returns JSON responses.
"""

import json
import sys
from pathlib import Path

# Add the maintenance module to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

try:
    from maintenance.orchestrator import MaintenanceOrchestrator
except ImportError as e:
    print(json.dumps({
        "error": f"Failed to import maintenance modules: {e}",
        "success": False
    }))
    sys.exit(1)


def execute_maintenance_command(command: str, parameters: dict = None) -> dict:
    """
    Execute a maintenance command and return results.

    Args:
        command: The maintenance command to execute
        parameters: Optional parameters for the command

    Returns:
        Dict containing command results
    """
    if parameters is None:
        parameters = {}

    try:
        # Determine workspace root (go up from ai/scripts to project root)
        workspace_root = Path(__file__).parent.parent.parent
        orchestrator = MaintenanceOrchestrator(str(workspace_root))

        if command == "get_status":
            result = orchestrator.get_system_status()
            return {"success": True, "data": result}

        elif command == "quick_optimize":
            result = orchestrator.execute_quick_optimization()
            return {"success": True, "data": result}

        elif command == "full_maintenance":
            result = orchestrator.execute_full_optimization(
                save_report=parameters.get("save_report", True)
            )
            return {"success": True, "data": result}

        elif command == "get_archive_info":
            result = orchestrator.get_archive_info()
            return {"success": True, "data": result}

        elif command == "analyze_documentation":
            result = orchestrator.optimizer.analyze_documentation_structure()
            return {"success": True, "data": result}

        elif command == "search_archive":
            query = parameters.get("query", "")
            category = parameters.get("category")
            result = orchestrator.archiver.search_archive(query, category)
            return {"success": True, "data": result}

        else:
            return {
                "success": False,
                "error": f"Unknown command: {command}",
                "available_commands": [
                    "get_status", "quick_optimize", "full_maintenance",
                    "get_archive_info", "analyze_documentation", "search_archive"
                ]
            }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "command": command,
            "parameters": parameters
        }


def main():
    """Main entry point for the service bridge."""
    try:
        if len(sys.argv) < 2:
            print(json.dumps({
                "error": "Command required",
                "usage": "python maintenance_service_bridge.py <command> [parameters_json]",
                "success": False
            }))
            sys.exit(1)

        command = sys.argv[1]
        parameters = {}

        # Parse parameters if provided
        if len(sys.argv) > 2:
            try:
                parameters = json.loads(sys.argv[2])
            except json.JSONDecodeError as e:
                print(json.dumps({
                    "error": f"Invalid JSON parameters: {e}",
                    "success": False
                }))
                sys.exit(1)

        # Execute command
        result = execute_maintenance_command(command, parameters)

        # Return result as JSON
        print(json.dumps(result, default=str, ensure_ascii=False, indent=2))

    except Exception as e:
        print(json.dumps({
            "error": f"Bridge execution failed: {e}",
            "success": False
        }))
        sys.exit(1)


if __name__ == "__main__":
    main()
