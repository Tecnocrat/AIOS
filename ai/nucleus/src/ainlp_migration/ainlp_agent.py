import argparse
import asyncio
import json
import os
import sys
import time
from pathlib import Path
from typing import List, Dict, Any, Optional

# Add ai tools to path for subprocess_manager
<<<<<<< HEAD
tools_path = os.path.join(
    os.path.dirname(__file__), "..", "..", "..", "..", "ai", "tools", "system"
)
=======
tools_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 
                         'ai', 'tools', 'system')
>>>>>>> origin/OS0.6.2.grok
sys.path.insert(0, tools_path)

try:
    from subprocess_manager import (
        AsyncSubprocessManager,
        FractalTTLCache,
    )  # type: ignore
except ImportError as e:
    print(f"Error importing subprocess_manager: {e}")
    print("Please ensure runtime/tools/subprocess_manager.py exists")
    sys.exit(1)


class AIOSArchitecturalAgent:
    """
    Enhanced AIOS Agent with architectural discovery and validation
    Implements PROPER AGENTIC BEHAVIOR PATTERNS
    """
<<<<<<< HEAD

=======
    
>>>>>>> origin/OS0.6.2.grok
    def __init__(self, workspace_root: Optional[str] = None):
        self.workspace_root = Path(workspace_root or os.getcwd())
        self.mgr = None
        self.architectural_cache = {}
<<<<<<< HEAD

=======
        
>>>>>>> origin/OS0.6.2.grok
    async def initialize(self):
        """Initialize the agent with architectural discovery"""
        self.mgr = AsyncSubprocessManager(
            cache=FractalTTLCache(memory_ttl=30, disk_ttl=300)
        )
        await self._discover_architecture()
<<<<<<< HEAD

=======
        
>>>>>>> origin/OS0.6.2.grok
    async def _discover_architecture(self):
        """
        ARCHITECTURAL DISCOVERY FIRST
        Scan and understand existing architecture before taking actions
        """
        print("🔍 Starting Architectural Discovery...")
<<<<<<< HEAD

        # Discover existing tools and patterns
        self.architectural_cache["tools"] = await self._discover_existing_tools()
        self.architectural_cache["patterns"] = await self._discover_patterns()
        self.architectural_cache["output_locations"] = (
            await self._discover_output_patterns()
        )
        self.architectural_cache["integration_points"] = (
            await self._discover_integration_points()
        )

        print(
            f"✅ Architecture discovered: {len(self.architectural_cache['tools'])} tools, "
            f"{len(self.architectural_cache['patterns'])} patterns"
        )

=======
        
        # Discover existing tools and patterns
        self.architectural_cache["tools"] = await self._discover_existing_tools()
        self.architectural_cache["patterns"] = await self._discover_patterns()
        self.architectural_cache["output_locations"] = await self._discover_output_patterns()
        self.architectural_cache["integration_points"] = await self._discover_integration_points()
        
        print(f"✅ Architecture discovered: {len(self.architectural_cache['tools'])} tools, "
              f"{len(self.architectural_cache['patterns'])} patterns")
        
>>>>>>> origin/OS0.6.2.grok
    async def _discover_existing_tools(self) -> Dict[str, List[str]]:
        """Discover existing tools to avoid redundant creation"""
        tools_locations = {
            "runtime": self.workspace_root / "runtime" / "tools",
<<<<<<< HEAD
            "ai_tools": self.workspace_root / "ai" / "tools",
            "core_tools": self.workspace_root / "core" / "tools",
            "interface_tools": self.workspace_root / "interface" / "tools",
        }

=======
            "ai_tools": self.workspace_root / "ai" / "tools", 
            "core_tools": self.workspace_root / "core" / "tools",
            "interface_tools": self.workspace_root / "interface" / "tools"
        }
        
>>>>>>> origin/OS0.6.2.grok
        discovered_tools = {}
        for location_name, path in tools_locations.items():
            if path.exists():
                tools = [f.name for f in path.glob("*.py") if f.is_file()]
                discovered_tools[location_name] = tools
                print(f"   📁 {location_name}: {len(tools)} tools")
            else:
                discovered_tools[location_name] = []
<<<<<<< HEAD

        return discovered_tools

=======
                
        return discovered_tools
        
>>>>>>> origin/OS0.6.2.grok
    async def _discover_patterns(self) -> Dict[str, str]:
        """Discover existing architectural patterns"""
        pattern_files = [
            "docs/AINLP/AINLP_SPECIFICATION.md",
            "tachyonic/DEVELOPMENT_NAVIGATOR_GUIDE.md",
<<<<<<< HEAD
            ".github/chatmodes/aios.chatmode.md",
        ]

=======
            ".github/chatmodes/aios.chatmode.md"
        ]
        
>>>>>>> origin/OS0.6.2.grok
        patterns = {}
        for pattern_file in pattern_files:
            path = self.workspace_root / pattern_file
            if path.exists():
                patterns[pattern_file] = "found"
                print(f"   📜 Pattern: {pattern_file}")
            else:
                patterns[pattern_file] = "missing"
<<<<<<< HEAD

        return patterns

=======
                
        return patterns
        
>>>>>>> origin/OS0.6.2.grok
    async def _discover_output_patterns(self) -> Dict[str, str]:
        """Discover proper output management patterns"""
        output_locations = {
            "tachyonic_archive": "tachyonic/archive/",
<<<<<<< HEAD
            "docs": "docs/",
            "logs": "runtime/logs/",
            "reports": "tachyonic/archive/",
        }

=======
            "docs": "docs/", 
            "logs": "runtime/logs/",
            "reports": "tachyonic/archive/"
        }
        
>>>>>>> origin/OS0.6.2.grok
        for location, path in output_locations.items():
            full_path = self.workspace_root / path
            if full_path.exists():
                print(f"   📤 Output: {location} → {path}")
            else:
                print(f"   ⚠️  Missing: {location} → {path}")
<<<<<<< HEAD

        return output_locations

=======
                
        return output_locations
        
>>>>>>> origin/OS0.6.2.grok
    async def _discover_integration_points(self) -> Dict[str, bool]:
        """Discover biological architecture integration points"""
        integration_points = {
            "dendritic_supervisor": "ai/infrastructure/dendritic/supervisor.py",
            "cytoplasm_bridge": "ai/cytoplasm/",
            "runtime": "runtime/tools/",
<<<<<<< HEAD
            "biological_monitor": "runtime/tools/biological_architecture_monitor.py",
        }

=======
            "biological_monitor": "runtime/tools/biological_architecture_monitor.py"
        }
        
>>>>>>> origin/OS0.6.2.grok
        discovered = {}
        for point, path in integration_points.items():
            full_path = self.workspace_root / path
            discovered[point] = full_path.exists()
            status = "✅" if discovered[point] else "❌"
            print(f"   {status} Integration: {point}")
<<<<<<< HEAD

        return discovered

    def validate_architectural_compliance(
        self, operation: str, target_path: str
    ) -> Dict[str, Any]:
=======
            
        return discovered
        
    def validate_architectural_compliance(self, operation: str, target_path: str) -> Dict[str, Any]:
>>>>>>> origin/OS0.6.2.grok
        """
        INTEGRATION VALIDATION
        Validate that operations comply with AIOS architectural principles
        """
        target = Path(target_path)
<<<<<<< HEAD

=======
        
>>>>>>> origin/OS0.6.2.grok
        validation_results = {
            "compliant": True,
            "warnings": [],
            "recommendations": [],
<<<<<<< HEAD
            "spatial_metadata": None,
        }

=======
            "spatial_metadata": None
        }
        
>>>>>>> origin/OS0.6.2.grok
        # Check for spatial metadata
        spatial_metadata_path = target.parent / ".aios_spatial_metadata.json"
        if spatial_metadata_path.exists():
            try:
<<<<<<< HEAD
                with open(spatial_metadata_path, "r") as f:
                    validation_results["spatial_metadata"] = json.load(f)
                print(f"✅ Spatial metadata found: {spatial_metadata_path}")
            except Exception as e:
                validation_results["warnings"].append(
                    f"Spatial metadata read error: {e}"
                )

=======
                with open(spatial_metadata_path, 'r') as f:
                    validation_results["spatial_metadata"] = json.load(f)
                print(f"✅ Spatial metadata found: {spatial_metadata_path}")
            except Exception as e:
                validation_results["warnings"].append(f"Spatial metadata read error: {e}")
                
>>>>>>> origin/OS0.6.2.grok
        # ENHANCEMENT OVER CREATION validation
        if operation == "create_tool":
            similar_tools = self._find_similar_tools(target.name)
            if similar_tools:
                validation_results["compliant"] = False
                validation_results["recommendations"].append(
                    f"ENHANCEMENT OVER CREATION: Found similar tools {similar_tools}. "
                    f"Consider enhancing existing tools instead."
                )
<<<<<<< HEAD

=======
                
>>>>>>> origin/OS0.6.2.grok
        # PROPER OUTPUT MANAGEMENT validation
        if operation == "create_output":
            if not self._validate_output_location(target):
                validation_results["warnings"].append(
                    f"Output location {target} may not follow tachyonic archival patterns"
                )
<<<<<<< HEAD

        return validation_results

    def _find_similar_tools(self, tool_name: str) -> List[str]:
        """Find tools with similar functionality"""
        similar = []

        # Extract key terms from tool name
        tool_terms = set(tool_name.lower().replace(".py", "").split("_"))

        for location, tools in self.architectural_cache.get("tools", {}).items():
            for existing_tool in tools:
                existing_terms = set(
                    existing_tool.lower().replace(".py", "").split("_")
                )

=======
                
        return validation_results
        
    def _find_similar_tools(self, tool_name: str) -> List[str]:
        """Find tools with similar functionality"""
        similar = []
        
        # Extract key terms from tool name
        tool_terms = set(tool_name.lower().replace('.py', '').split('_'))
        
        for location, tools in self.architectural_cache.get("tools", {}).items():
            for existing_tool in tools:
                existing_terms = set(existing_tool.lower().replace('.py', '').split('_'))
                
>>>>>>> origin/OS0.6.2.grok
                # Check for term overlap
                overlap = tool_terms.intersection(existing_terms)
                if len(overlap) >= 2:  # At least 2 terms in common
                    similar.append(f"{location}/{existing_tool}")
<<<<<<< HEAD

        return similar

    def _validate_output_location(self, target_path: Path) -> bool:
        """Validate output follows proper tachyonic patterns"""
        proper_locations = ["tachyonic/archive/", "docs/", "runtime/logs/"]

        path_str = str(target_path)
        return any(loc in path_str for loc in proper_locations)

=======
                    
        return similar
        
    def _validate_output_location(self, target_path: Path) -> bool:
        """Validate output follows proper tachyonic patterns"""
        proper_locations = [
            "tachyonic/archive/",
            "docs/",
            "runtime/logs/"
        ]
        
        path_str = str(target_path)
        return any(loc in path_str for loc in proper_locations)
        
>>>>>>> origin/OS0.6.2.grok
    async def enhanced_continue(self, cache_ttl: int = 300) -> Dict[str, Any]:
        """
        Enhanced continue with architectural validation
        """
        if not self.mgr:
            await self.initialize()
<<<<<<< HEAD

        # Standard health checks
        results = await self.mgr.run_parallel(
            DEFAULT_CHECKS
            + [
                # Enhanced architectural checks
                [
                    "python",
                    "-c",
                    "import sys; print(f'Python: {sys.version_info[:2]}')",
                ],
                ["git", "branch", "--show-current"],
                ["git", "log", "--oneline", "-1"],
=======
            
        # Standard health checks
        results = await self.mgr.run_parallel(
            DEFAULT_CHECKS + [
                # Enhanced architectural checks
                ["python", "-c", "import sys; print(f'Python: {sys.version_info[:2]}')"],
                ["git", "branch", "--show-current"],
                ["git", "log", "--oneline", "-1"]
>>>>>>> origin/OS0.6.2.grok
            ],
            timeout=15.0,
            cache_ttl=cache_ttl,
        )
<<<<<<< HEAD

        # Add architectural compliance summary
        compliance_summary = {
            "tools_discovered": sum(
                len(tools)
                for tools in self.architectural_cache.get("tools", {}).values()
            ),
            "patterns_found": len(
                [
                    p
                    for p in self.architectural_cache.get("patterns", {}).values()
                    if p == "found"
                ]
            ),
            "integration_points": sum(
                self.architectural_cache.get("integration_points", {}).values()
            ),
            "architecture_health": (
                "optimal"
                if all(self.architectural_cache.get("integration_points", {}).values())
                else "partial"
            ),
        }

        summary = summary_from_results(results)
        summary["architectural_compliance"] = compliance_summary
        summary["agent_mode"] = "enhanced_aios_architectural_agent"

=======
        
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
        
>>>>>>> origin/OS0.6.2.grok
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
<<<<<<< HEAD
        help="Operation type for validation (create_tool, create_output, etc.)",
=======
        help="Operation type for validation (create_tool, create_output, etc.)"
>>>>>>> origin/OS0.6.2.grok
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
<<<<<<< HEAD

=======
        
>>>>>>> origin/OS0.6.2.grok
    elif args.command == "discover":
        # Pure architectural discovery
        async def run_discovery():
            agent = AIOSArchitecturalAgent()
            await agent.initialize()
            return agent.architectural_cache
<<<<<<< HEAD

        discovery = asyncio.run(run_discovery())
        print(json.dumps({"architectural_discovery": discovery}, indent=2))

=======
            
        discovery = asyncio.run(run_discovery())
        print(json.dumps({"architectural_discovery": discovery}, indent=2))
        
>>>>>>> origin/OS0.6.2.grok
    elif args.command == "validate":
        # Validate architectural compliance
        if not args.operation or not args.target:
            print("Error: --operation and --target required for validation")
            return
<<<<<<< HEAD

=======
            
>>>>>>> origin/OS0.6.2.grok
        async def run_validation():
            agent = AIOSArchitecturalAgent()
            await agent.initialize()
            validation_func = agent.validate_architectural_compliance
            return validation_func(args.operation, args.target)
<<<<<<< HEAD

        validation = asyncio.run(run_validation())
        print(json.dumps({"validation": validation}, indent=2))

=======
            
        validation = asyncio.run(run_validation())
        print(json.dumps({"validation": validation}, indent=2))
        
>>>>>>> origin/OS0.6.2.grok
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
