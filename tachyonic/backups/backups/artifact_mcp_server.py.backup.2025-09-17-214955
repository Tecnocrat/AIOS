#!/usr/bin/env python3
"""
AIOS Artifact Factory MCP Server
Provides artifact creation and management tools
"""

import sys
import json
sys.path.insert(0, r"c:\dev\AIOS\scripts")

from artifact_factory import ArtifactFactory, ArtifactType

def main():
    if len(sys.argv) < 2:
        print("Usage: artifact_mcp_server.py <tool_name> [args...]")
        sys.exit(1)
    
    tool_name = sys.argv[1]
    args = sys.argv[2:] if len(sys.argv) > 2 else []
    
    factory = ArtifactFactory()
    
    if tool_name == "list_tools":
        tools = [
            {
                "name": "create_artifact",
                "description": "Create a new Python artifact",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "artifact_type": {"type": "string", "enum": ["calculator", "text_processor", "data_analyzer"]},
                        "complexity": {"type": "integer", "minimum": 1, "maximum": 5}
                    },
                    "required": ["artifact_type"]
                }
            },
            {
                "name": "create_population", 
                "description": "Create diverse population of artifacts",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "size": {"type": "integer", "minimum": 1, "maximum": 20}
                    },
                    "required": ["size"]
                }
            }
        ]
        print(json.dumps({"tools": tools}))
    
    elif tool_name == "create_artifact":
        if len(args) < 1:
            print(json.dumps({"error": "Missing artifact_type"}))
            sys.exit(1)
        
        artifact_type_str = args[0]
        complexity = int(args[1]) if len(args) > 1 else None
        
        artifact_type = getattr(ArtifactType, artifact_type_str.upper(), None)
        if not artifact_type:
            print(json.dumps({"error": f"Unknown artifact type: {artifact_type_str}"}))
            sys.exit(1)
        
        try:
            artifact_path = factory.create_artifact(artifact_type, complexity)
            metadata = factory.get_artifact_metadata(artifact_path)
            result = {
                "artifact_path": str(artifact_path),
                "metadata": metadata
            }
            print(json.dumps(result))
        except Exception as e:
            print(json.dumps({"error": str(e)}))
    
    elif tool_name == "create_population":
        size = int(args[0]) if args else 10
        try:
            population = factory.create_diverse_population(size)
            result = {
                "population_size": len(population),
                "artifacts": [str(p) for p in population]
            }
            print(json.dumps(result))
        except Exception as e:
            print(json.dumps({"error": str(e)}))
    
    else:
        print(json.dumps({"error": f"Unknown tool: {tool_name}"}))

if __name__ == "__main__":
    main()
