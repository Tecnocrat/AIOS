import argparse
import asyncio
import json
import os
import sys
import time
from pathlib import Path
from typing import List, Dict, Any, Optional

# Add runtime_intelligence tools to path for subprocess_manager
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'runtime_intelligence', 'tools'))

try:
    from subprocess_manager import (
        AsyncSubprocessManager,
        FractalTTLCache,
    )  # type: ignore
except ImportError as e:
    print(f"Error importing subprocess_manager: {e}")
    print("Please ensure runtime_intelligence/tools/subprocess_manager.py exists")
    sys.exit(1)


class AIOSArchitecturalAgent:
    """
    Enhanced AIOS Agent with architectural discovery and validation
    Implements PROPER AGENTIC BEHAVIOR PATTERNS
    """
    
    def __init__(self, workspace_root: Optional[str] = None):
        self.workspace_root = Path(workspace_root or os.getcwd())
        self.mgr = None
        self.architectural_cache = {}
        
    async def initialize(self):
        """Initialize the agent with architectural discovery"""
        self.mgr = AsyncSubprocessManager(
            cache=FractalTTLCache(memory_ttl=30, disk_ttl=300)
        )
        await self._discover_architecture()
        
    async def _discover_architecture(self):
        """
        ARCHITECTURAL DISCOVERY FIRST
        Scan and understand existing architecture before taking actions
        """
        print("🔍 Starting Architectural Discovery...")
        
        # Discover existing tools and patterns
        self.architectural_cache["tools"] = await self._discover_existing_tools()
        self.architectural_cache["patterns"] = await self._discover_patterns()
        self.architectural_cache["output_locations"] = await self._discover_output_patterns()
        self.architectural_cache["integration_points"] = await self._discover_integration_points()
        
        print(f"✅ Architecture discovered: {len(self.architectural_cache['tools'])} tools, "
              f"{len(self.architectural_cache['patterns'])} patterns")
        
    async def _discover_existing_tools(self) -> Dict[str, List[str]]:
        """Discover existing tools to avoid redundant creation"""
        tools_locations = {
            "runtime_intelligence": self.workspace_root / "runtime_intelligence" / "tools",
            "ai_tools": self.workspace_root / "ai" / "tools", 
            "core_tools": self.workspace_root / "core" / "tools",
            "interface_tools": self.workspace_root / "interface" / "tools"
        }
        
        discovered_tools = {}
        for location_name, path in tools_locations.items():
            if path.exists():
                tools = [f.name for f in path.glob("*.py") if f.is_file()]
                discovered_tools[location_name] = tools
                print(f"   📁 {location_name}: {len(tools)} tools")
            else:
                discovered_tools[location_name] = []
                
        return discovered_tools
        
    async def _discover_patterns(self) -> Dict[str, str]:
        """Discover existing architectural patterns"""
        pattern_files = [
            "docs/AINLP/AINLP_SPECIFICATION.md",
            "tachyonic/DEVELOPMENT_NAVIGATOR_GUIDE.md",
            ".github/chatmodes/aios.chatmode.md"
        ]
        
        patterns = {}
        for pattern_file in pattern_files:
            path = self.workspace_root / pattern_file
            if path.exists():
                patterns[pattern_file] = "found"
                print(f"   📜 Pattern: {pattern_file}")
            else:
                patterns[pattern_file] = "missing"
                
        return patterns
        
    async def _discover_output_patterns(self) -> Dict[str, str]:
        """Discover proper output management patterns"""
        output_locations = {
            "tachyonic_archive": "tachyonic/archive/",
            "docs": "docs/", 
            "logs": "runtime_intelligence/logs/",
            "reports": "tachyonic/archive/"
        }
        
        for location, path in output_locations.items():
            full_path = self.workspace_root / path
            if full_path.exists():
                print(f"   📤 Output: {location} → {path}")
            else:
                print(f"   ⚠️  Missing: {location} → {path}")
                
        return output_locations
        
    async def _discover_integration_points(self) -> Dict[str, bool]:
        """Discover biological architecture integration points"""
        integration_points = {
            "dendritic_supervisor": "ai/infrastructure/dendritic/supervisor.py",
            "cytoplasm_bridge": "ai/cytoplasm/",
            "runtime_intelligence": "runtime_intelligence/tools/",
            "biological_monitor": "runtime_intelligence/tools/biological_architecture_monitor.py"
        }
        
        discovered = {}
        for point, path in integration_points.items():
            full_path = self.workspace_root / path
            discovered[point] = full_path.exists()
            status = "✅" if discovered[point] else "❌"
            print(f"   {status} Integration: {point}")
            
        return discovered
        
    def validate_architectural_compliance(self, operation: str, target_path: str) -> Dict[str, Any]:
        """
        INTEGRATION VALIDATION
        Validate that operations comply with AIOS architectural principles
        """
        target = Path(target_path)
        
        validation_results = {
            "compliant": True,
            "warnings": [],
            "recommendations": [],
            "spatial_metadata": None
        }
        
        # Check for spatial metadata
        spatial_metadata_path = target.parent / ".aios_spatial_metadata.json"
        if spatial_metadata_path.exists():
            try:
                with open(spatial_metadata_path, 'r') as f:
                    validation_results["spatial_metadata"] = json.load(f)
                print(f"✅ Spatial metadata found: {spatial_metadata_path}")
            except Exception as e:
                validation_results["warnings"].append(f"Spatial metadata read error: {e}")
                
        # ENHANCEMENT OVER CREATION validation
        if operation == "create_tool":
            similar_tools = self._find_similar_tools(target.name)
            if similar_tools:
                validation_results["compliant"] = False
                validation_results["recommendations"].append(
                    f"ENHANCEMENT OVER CREATION: Found similar tools {similar_tools}. "
                    f"Consider enhancing existing tools instead."
                )
                
        # PROPER OUTPUT MANAGEMENT validation
        if operation == "create_output":
            if not self._validate_output_location(target):
                validation_results["warnings"].append(
                    f"Output location {target} may not follow tachyonic archival patterns"
                )
                
        return validation_results
        
    def _find_similar_tools(self, tool_name: str) -> List[str]:
        """Find tools with similar functionality"""
        similar = []
        
        # Extract key terms from tool name
        tool_terms = set(tool_name.lower().replace('.py', '').split('_'))
        
        for location, tools in self.architectural_cache.get("tools", {}).items():
            for existing_tool in tools:
                existing_terms = set(existing_tool.lower().replace('.py', '').split('_'))
                
                # Check for term overlap
                overlap = tool_terms.intersection(existing_terms)
                if len(overlap) >= 2:  # At least 2 terms in common
                    similar.append(f"{location}/{existing_tool}")
                    
        return similar
        
    def _validate_output_location(self, target_path: Path) -> bool:
        """Validate output follows proper tachyonic patterns"""
        proper_locations = [
            "tachyonic/archive/",
            "docs/",
            "runtime_intelligence/logs/"
        ]
        
        path_str = str(target_path)
        return any(loc in path_str for loc in proper_locations)
        
    async def enhanced_continue(self, cache_ttl: int = 300) -> Dict[str, Any]:
        """
        Enhanced continue with architectural validation
        """
        if not self.mgr:
            await self.initialize()
            
        # Standard health checks
        results = await self.mgr.run_parallel(
            DEFAULT_CHECKS + [
                # Enhanced architectural checks
                ["python", "-c", "import sys; print(f'Python: {sys.version_info[:2]}')"],
                ["git", "branch", "--show-current"],
                ["git", "log", "--oneline", "-1"]
            ],
            timeout=15.0,
            cache_ttl=cache_ttl,
        )
        
        # Add architectural compliance summary
        compliance_summary = {
            "tools_discovered": sum(len(tools) for tools in self.architectural_cache.get("tools", {}).values()),
            "patterns_found": len([p for p in self.architectural_cache.get("patterns", {}).values() if p == "found"]),
            "integration_points": sum(self.architectural_cache.get("integration_points", {}).values()),
            "architecture_health": "optimal" if all(self.architectural_cache.get("integration_points", {}).values()) else "partial"
        }
        
        summary = summary_from_results(results)
        summary["architectural_compliance"] = compliance_summary
        summary["agent_mode"] = "enhanced_aios_architectural_agent"
        
        return summary


# Legacy compatibility
DEFAULT_CHECKS = [
    ["git", "rev-parse", "--abbrev-ref", "HEAD"],
    ["git", "status", "--porcelain"],
    ["python", "--version"],
    ["pip", "--version"],
]


def summary_from_results(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {
        "timestamp": int(time.time()),
        "checks": [
            {
                "cmd": r["cmd"],
                "ok": r["returncode"] == 0,
                "duration_ms": r["duration_ms"],
                "sample": (r.get("stdout") or r.get("stderr") or "")[:200],
            }
            for r in results
        ],
        "ok": all(r["returncode"] == 0 for r in results),
    }


async def do_continue(cache_ttl: int = 300) -> Dict[str, Any]:
    """Enhanced continue with architectural discovery"""
    agent = AIOSArchitecturalAgent()
    return await agent.enhanced_continue(cache_ttl)


def ensure_log_dir() -> str:
    log_dir = os.path.join(os.path.dirname(__file__), "..", "logs", "agent")
    log_dir = os.path.abspath(log_dir)
    os.makedirs(log_dir, exist_ok=True)
    return log_dir


def write_summary(payload: Dict[str, Any]) -> str:
    log_dir = ensure_log_dir()
    ts = time.strftime(
        "%Y%m%d_%H%M%S", time.localtime(payload.get("timestamp", time.time()))
    )
    path = os.path.join(log_dir, f"continue_{ts}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    return path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Enhanced AIOS AINLP Architectural Agent"
    )
    parser.add_argument(
        "command",
        choices=["continue", "status", "validate", "discover"],
        help="Agent command",
    )
    parser.add_argument(
        "--cache-ttl",
        type=int,
        default=300,
        help="Cache TTL seconds for checks",
    )
    parser.add_argument(
        "--operation",
        type=str,
        help="Operation type for validation (create_tool, create_output, etc.)"
    )
    parser.add_argument(
        "--target",
        type=str,
        help="Target path for validation",
    )
    args = parser.parse_args()

    if args.command == "continue":
        payload = asyncio.run(do_continue(cache_ttl=args.cache_ttl))
        path = write_summary(payload)
        print(json.dumps({"summary": payload, "log_path": path}, indent=2))
        
    elif args.command == "discover":
        # Pure architectural discovery
        async def run_discovery():
            agent = AIOSArchitecturalAgent()
            await agent.initialize()
            return agent.architectural_cache
            
        discovery = asyncio.run(run_discovery())
        print(json.dumps({"architectural_discovery": discovery}, indent=2))
        
    elif args.command == "validate":
        # Validate architectural compliance
        if not args.operation or not args.target:
            print("Error: --operation and --target required for validation")
            return
            
        async def run_validation():
            agent = AIOSArchitecturalAgent()
            await agent.initialize()
            validation_func = agent.validate_architectural_compliance
            return validation_func(args.operation, args.target)
            
        validation = asyncio.run(run_validation())
        print(json.dumps({"validation": validation}, indent=2))
        
    elif args.command == "status":
        log_dir = ensure_log_dir()
        files = sorted(
            [f for f in os.listdir(log_dir) if f.startswith("continue_")],
            reverse=True,
        )
        if not files:
            print(json.dumps({"status": "no_runs"}, indent=2))
            return
        with open(os.path.join(log_dir, files[0]), "r", encoding="utf-8") as f:
            print(f.read())


if __name__ == "__main__":
    main()
