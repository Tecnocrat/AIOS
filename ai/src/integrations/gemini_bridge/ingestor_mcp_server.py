#!/usr/bin/env python3
"""
<<<<<<< HEAD
AIOS Evolution Ingestor MCP Server
=======
AIOS Evolution Ingestor MCP Server  
>>>>>>> origin/OS0.6.2.grok
Provides evolutionary experiment tools
"""

import sys
import json
<<<<<<< HEAD

=======
>>>>>>> origin/OS0.6.2.grok
sys.path.insert(0, r"c:\dev\AIOS\scripts")

from enhanced_artifact_ingestor import EnhancedArtifactIngestor

<<<<<<< HEAD

=======
>>>>>>> origin/OS0.6.2.grok
def main():
    if len(sys.argv) < 2:
        print("Usage: ingestor_mcp_server.py <tool_name> [args...]")
        sys.exit(1)
<<<<<<< HEAD

    tool_name = sys.argv[1]
    args = sys.argv[2:] if len(sys.argv) > 2 else []

    ingestor = EnhancedArtifactIngestor()

=======
    
    tool_name = sys.argv[1]
    args = sys.argv[2:] if len(sys.argv) > 2 else []
    
    ingestor = EnhancedArtifactIngestor()
    
>>>>>>> origin/OS0.6.2.grok
    if tool_name == "list_tools":
        tools = [
            {
                "name": "run_evolution",
                "description": "Run evolutionary experiment",
                "input_schema": {
<<<<<<< HEAD
                    "type": "object",
                    "properties": {
                        "population_size": {
                            "type": "integer",
                            "minimum": 5,
                            "maximum": 50,
                        },
                        "generations": {"type": "integer", "minimum": 1, "maximum": 20},
                        "mutation_rate": {
                            "type": "number",
                            "minimum": 0.1,
                            "maximum": 1.0,
                        },
                    },
                },
            }
        ]
        print(json.dumps({"tools": tools}))

=======
                    "type": "object", 
                    "properties": {
                        "population_size": {"type": "integer", "minimum": 5, "maximum": 50},
                        "generations": {"type": "integer", "minimum": 1, "maximum": 20},
                        "mutation_rate": {"type": "number", "minimum": 0.1, "maximum": 1.0}
                    }
                }
            }
        ]
        print(json.dumps({"tools": tools}))
    
>>>>>>> origin/OS0.6.2.grok
    elif tool_name == "run_evolution":
        population_size = int(args[0]) if len(args) > 0 else 10
        generations = int(args[1]) if len(args) > 1 else 5
        mutation_rate = float(args[2]) if len(args) > 2 else 0.3
<<<<<<< HEAD

=======
        
>>>>>>> origin/OS0.6.2.grok
        try:
            experiment_id = ingestor.run_evolutionary_experiment(
                population_size, generations, mutation_rate
            )
            result = {
                "experiment_id": experiment_id,
                "population_size": population_size,
                "generations": generations,
<<<<<<< HEAD
                "mutation_rate": mutation_rate,
=======
                "mutation_rate": mutation_rate
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
