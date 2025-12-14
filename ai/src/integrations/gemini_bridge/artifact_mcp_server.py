#!/usr/bin/env python3
"""
AIOS Artifact Factory MCP Server
Provides artifact creation and management tools
"""

import sys
import json
<<<<<<< HEAD

=======
>>>>>>> origin/OS0.6.2.grok
sys.path.insert(0, r"c:\dev\AIOS\scripts")

from artifact_factory import ArtifactFactory, ArtifactType

<<<<<<< HEAD

=======
>>>>>>> origin/OS0.6.2.grok
def main():
    if len(sys.argv) < 2:
        print("Usage: artifact_mcp_server.py <tool_name> [args...]")
        sys.exit(1)
<<<<<<< HEAD

    tool_name = sys.argv[1]
    args = sys.argv[2:] if len(sys.argv) > 2 else []

    factory = ArtifactFactory()

=======
    
    tool_name = sys.argv[1]
    args = sys.argv[2:] if len(sys.argv) > 2 else []
    
    factory = ArtifactFactory()
    
>>>>>>> origin/OS0.6.2.grok
    if tool_name == "list_tools":
        tools = [
            {
                "name": "create_artifact",
                "description": "Create a new Python artifact",
                "input_schema": {
                    "type": "object",
                    "properties": {
<<<<<<< HEAD
                        "artifact_type": {
                            "type": "string",
                            "enum": ["calculator", "text_processor", "data_analyzer"],
                        },
                        "complexity": {"type": "integer", "minimum": 1, "maximum": 5},
                    },
                    "required": ["artifact_type"],
                },
            },
            {
                "name": "create_population",
=======
                        "artifact_type": {"type": "string", "enum": ["calculator", "text_processor", "data_analyzer"]},
                        "complexity": {"type": "integer", "minimum": 1, "maximum": 5}
                    },
                    "required": ["artifact_type"]
                }
            },
            {
                "name": "create_population", 
>>>>>>> origin/OS0.6.2.grok
                "description": "Create diverse population of artifacts",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "size": {"type": "integer", "minimum": 1, "maximum": 20}
                    },
<<<<<<< HEAD
                    "required": ["size"],
                },
            },
        ]
        print(json.dumps({"tools": tools}))

=======
                    "required": ["size"]
                }
            }
        ]
        print(json.dumps({"tools": tools}))
    
>>>>>>> origin/OS0.6.2.grok
    elif tool_name == "create_artifact":
        if len(args) < 1:
            print(json.dumps({"error": "Missing artifact_type"}))
            sys.exit(1)
<<<<<<< HEAD

        artifact_type_str = args[0]
        complexity = int(args[1]) if len(args) > 1 else None

=======
        
        artifact_type_str = args[0]
        complexity = int(args[1]) if len(args) > 1 else None
        
>>>>>>> origin/OS0.6.2.grok
        artifact_type = getattr(ArtifactType, artifact_type_str.upper(), None)
        if not artifact_type:
            print(json.dumps({"error": f"Unknown artifact type: {artifact_type_str}"}))
            sys.exit(1)
<<<<<<< HEAD

        try:
            artifact_path = factory.create_artifact(artifact_type, complexity)
            metadata = factory.get_artifact_metadata(artifact_path)
            result = {"artifact_path": str(artifact_path), "metadata": metadata}
            print(json.dumps(result))
        except Exception as e:
            print(json.dumps({"error": str(e)}))

=======
        
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
    
>>>>>>> origin/OS0.6.2.grok
    elif tool_name == "create_population":
        size = int(args[0]) if args else 10
        try:
            population = factory.create_diverse_population(size)
            result = {
                "population_size": len(population),
<<<<<<< HEAD
                "artifacts": [str(p) for p in population],
=======
                "artifacts": [str(p) for p in population]
>>>>>>> origin/OS0.6.2.grok
            }
            print(json.dumps(result))
        except Exception as e:
            print(json.dumps({"error": str(e)}))
<<<<<<< HEAD

    else:
        print(json.dumps({"error": f"Unknown tool: {tool_name}"}))


=======
    
    else:
        print(json.dumps({"error": f"Unknown tool: {tool_name}"}))

>>>>>>> origin/OS0.6.2.grok
if __name__ == "__main__":
    main()
