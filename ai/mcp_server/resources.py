"""
AIOS MCP Resource Provider
Serves AIOS context files, architecture documentation, and consciousness metrics
"""

import json
from pathlib import Path
from typing import List
from mcp.types import Resource


class AIOSResourceProvider:
    """Provides AIOS resources via MCP protocol"""
    
    def __init__(self, workspace_root: Path):
        self.workspace = workspace_root
    
    async def list_resources(self) -> List[Resource]:
        """List all available AIOS resources"""
        resources = []
        
        # Core navigation trinity
        if (self.workspace / "DEV_PATH.md").exists():
            resources.append(Resource(
                uri="aios://dev-path",
                name="DEV_PATH.md",
                description="Current development tracking and tactical waypoints. Living document with tachyonic shadow preservation.",
                mimeType="text/markdown"
            ))
        
        if (self.workspace / "PROJECT_CONTEXT.md").exists():
            resources.append(Resource(
                uri="aios://project-context",
                name="PROJECT_CONTEXT.md",
                description="Strategic principles, biological architecture patterns, and AINLP paradigms.",
                mimeType="text/markdown"
            ))
        
        if (self.workspace / "README.md").exists():
            resources.append(Resource(
                uri="aios://readme",
                name="README.md",
                description="Public overview of AIOS multi-language supercell platform.",
                mimeType="text/markdown"
            ))
        
        # AI session context
        session_context = self.workspace / ".vscode" / ".ai_session_context.json"
        if session_context.exists():
            resources.append(Resource(
                uri="aios://session-context",
                name=".ai_session_context.json",
                description="Structured AI agent guidance metadata (490 lines). Current phase, consciousness level, achievements.",
                mimeType="application/json"
            ))
        
        # AINLP specification
        ainlp_spec = self.workspace / "docs" / "ainlp_specification_v2.0.md"
        if ainlp_spec.exists():
            resources.append(Resource(
                uri="aios://ainlp-spec",
                name="AINLP Specification v2.0",
                description="Complete AINLP paradigm: enhancement over creation, biological architecture, consciousness evolution.",
                mimeType="text/markdown"
            ))
        
        # Architecture documentation
        arch_index = self.workspace / "docs" / "ARCHITECTURE_INDEX.md"
        if arch_index.exists():
            resources.append(Resource(
                uri="aios://architecture-index",
                name="Architecture Index",
                description="Comprehensive AIOS architecture documentation index with supercell organization.",
                mimeType="text/markdown"
            ))
        
        # Consciousness metrics
        consciousness_file = self.workspace / "tachyonic" / "consciousness_metrics.json"
        if consciousness_file.exists():
            resources.append(Resource(
                uri="aios://consciousness-metrics",
                name="Consciousness Metrics",
                description="System consciousness level tracking: current level, history, evolution patterns.",
                mimeType="application/json"
            ))
        
        # Dendritic connections map
        dendritic_file = self.workspace / "tachyonic" / "dendritic_connections.json"
        if dendritic_file.exists():
            resources.append(Resource(
                uri="aios://dendritic-connections",
                name="Dendritic Connections",
                description="Component interconnection map for biological architecture analysis.",
                mimeType="application/json"
            ))
        
        # Holographic metadata index
        holographic_index = self.workspace / "tachyonic" / "aios_holographic_index_latest.json"
        if holographic_index.exists():
            resources.append(Resource(
                uri="aios://holographic-index",
                name="Holographic Index",
                description="Spatial metadata system tracking file relationships and consciousness coherence.",
                mimeType="application/json"
            ))
        
        return resources
    
    async def read_resource(self, uri: str) -> str:
        """Read AIOS resource content"""
        resource_map = {
            "aios://dev-path": "DEV_PATH.md",
            "aios://project-context": "PROJECT_CONTEXT.md",
            "aios://readme": "README.md",
            "aios://session-context": ".vscode/.ai_session_context.json",
            "aios://ainlp-spec": "docs/ainlp_specification_v2.0.md",
            "aios://architecture-index": "docs/ARCHITECTURE_INDEX.md",
            "aios://consciousness-metrics": "tachyonic/consciousness_metrics.json",
            "aios://dendritic-connections": "tachyonic/dendritic_connections.json",
            "aios://holographic-index": "tachyonic/aios_holographic_index_latest.json"
        }
        
        relative_path = resource_map.get(uri)
        if not relative_path:
            raise ValueError(f"Unknown resource URI: {uri}")
        
        file_path = self.workspace / relative_path
        if not file_path.exists():
            raise FileNotFoundError(f"Resource file not found: {relative_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
