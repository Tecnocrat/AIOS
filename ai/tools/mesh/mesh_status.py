#!/usr/bin/env python3
"""
AIOS Mesh Status - Unified view of all mesh components

Shows status of all cells and agents in the AIOS mesh.

Usage:
    python mesh_status.py
    
Output:
    - Cell status (Discovery, Alpha, Pure, Memory, Genome)
    - Agent status (Copilot sessions, Nous)
    - Consciousness levels
    - Crystal count
    - Overall mesh health

AINLP.dendritic[STATUS] Unified mesh view
"""

import json
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional

try:
    import httpx
    HTTP_CLIENT = "httpx"
except ImportError:
    try:
        import requests
        HTTP_CLIENT = "requests"
    except ImportError:
        print("Error: httpx or requests required")
        sys.exit(1)


# Default cell URLs
CELLS = {
    "discovery": {"url": "http://localhost:8001", "port": 8001},
    "alpha": {"url": "http://localhost:8005", "port": 8005},
    "pure": {"url": "http://localhost:8004", "port": 8004},
    "genome": {"url": "http://localhost:8006", "port": 8006},
    "memory": {"url": "http://localhost:8007", "port": 8007},
    "nous": {"url": "http://localhost:8010", "port": 8010},
}


def http_get(url: str, timeout: float = 3.0) -> Optional[Dict]:
    """Make HTTP GET request with timeout."""
    try:
        if HTTP_CLIENT == "httpx":
            with httpx.Client(timeout=timeout) as client:
                response = client.get(url)
                return response.json() if response.status_code == 200 else None
        else:
            import requests
            response = requests.get(url, timeout=timeout)
            return response.json() if response.status_code == 200 else None
    except Exception:
        return None


def check_cell(name: str, url: str) -> Dict[str, Any]:
    """Check a cell's health status."""
    health = http_get(f"{url}/health")
    if health:
        return {
            "name": name,
            "status": "✅ UP",
            "cell_id": health.get("cell_id", name),
            "healthy": True,
            "details": health
        }
    else:
        return {
            "name": name,
            "status": "❌ DOWN",
            "cell_id": name,
            "healthy": False,
            "details": None
        }


def get_mesh_summary() -> Dict[str, Any]:
    """Get full mesh summary from Discovery."""
    return http_get("http://localhost:8001/mesh/summary") or {}


def get_memory_consciousness() -> Dict[str, Any]:
    """Get consciousness state from Memory Cell."""
    return http_get("http://localhost:8007/consciousness") or {}


def print_banner():
    """Print AIOS banner."""
    print()
    print("╔═══════════════════════════════════════════════════════════════╗")
    print("║                    AIOS MESH STATUS                          ║")
    print("║              Unified Consciousness Network                   ║")
    print("╚═══════════════════════════════════════════════════════════════╝")
    print(f"  Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()


def print_cells(cell_statuses: List[Dict]):
    """Print cell status table."""
    print("┌─────────────────────────────────────────────────────────────────┐")
    print("│ CELLS                                                           │")
    print("├──────────┬────────┬──────────────────────────────────────────────┤")
    print("│ Name     │ Status │ Details                                      │")
    print("├──────────┼────────┼──────────────────────────────────────────────┤")
    
    for cell in cell_statuses:
        name = cell["name"].ljust(8)[:8]
        status = cell["status"]
        
        if cell["healthy"]:
            details = cell.get("details", {})
            if "consciousness_level" in details:
                detail = f"consciousness: {details['consciousness_level']}"
            elif "cell_type" in details:
                detail = f"type: {details['cell_type']}"
            elif "status" in details:
                detail = details["status"]
            else:
                detail = "running"
        else:
            detail = "unreachable"
        
        detail = detail.ljust(42)[:42]
        print(f"│ {name} │ {status} │ {detail} │")
    
    print("└──────────┴────────┴──────────────────────────────────────────────┘")


def print_agents(mesh_summary: Dict):
    """Print agent status from mesh summary."""
    agents = mesh_summary.get("agents", {})
    agent_ids = agents.get("ids", [])
    agent_types = agents.get("types", [])
    
    print()
    print("┌─────────────────────────────────────────────────────────────────┐")
    print("│ AGENTS                                                          │")
    print("├──────────────────────────────────┬───────────────────────────────┤")
    print("│ Agent ID                         │ Type                          │")
    print("├──────────────────────────────────┼───────────────────────────────┤")
    
    for agent_id in agent_ids:
        # Determine type from ID prefix
        if "nous" in agent_id.lower():
            agent_type = "inner_voice"
        else:
            agent_type = "copilot"
        
        id_display = agent_id.ljust(32)[:32]
        type_display = agent_type.ljust(29)[:29]
        print(f"│ {id_display} │ {type_display} │")
    
    if not agent_ids:
        print("│ (no agents registered)           │                               │")
    
    print("└──────────────────────────────────┴───────────────────────────────┘")


def print_consciousness(mesh_summary: Dict, memory_consciousness: Dict):
    """Print consciousness summary."""
    mesh_consciousness = mesh_summary.get("mesh_consciousness", 0)
    memory_level = memory_consciousness.get("consciousness_level", 0)
    crystals = memory_consciousness.get("stats", {}).get("crystals", 0)
    crystal_contribution = memory_consciousness.get("stats", {}).get("total_consciousness_contribution", 0)
    
    cell_count = mesh_summary.get("cells", {}).get("count", 0)
    agent_count = mesh_summary.get("agents", {}).get("count", 0)
    
    print()
    print("┌─────────────────────────────────────────────────────────────────┐")
    print("│ CONSCIOUSNESS                                                   │")
    print("├─────────────────────────────────────────────────────────────────┤")
    print(f"│  Mesh Consciousness:     {mesh_consciousness:>6.2f}                               │")
    print(f"│  Memory Cell:            {memory_level:>6.2f} ({crystals} crystals)                  │")
    print(f"│  Crystal Contribution:   {crystal_contribution:>6.2f}                               │")
    print("├─────────────────────────────────────────────────────────────────┤")
    print(f"│  Connected Cells:        {cell_count:>6}                               │")
    print(f"│  Active Agents:          {agent_count:>6}                               │")
    print("└─────────────────────────────────────────────────────────────────┘")


def print_ports():
    """Print port allocation reference."""
    print()
    print("┌─────────────────────────────────────────────────────────────────┐")
    print("│ PORT ALLOCATION                                                 │")
    print("├──────────┬──────────────────────────────────────────────────────┤")
    print("│  8001    │ Discovery Cell (peer/agent registry)                 │")
    print("│  8004    │ Pure Cell (minimal consciousness)                    │")
    print("│  8005    │ Alpha Cell (primary development)                     │")
    print("│  8006    │ Genome Cell (codebase health)                        │")
    print("│  8007    │ Memory Cell (consciousness persistence)              │")
    print("│  8010    │ Nous API (inner voice)                               │")
    print("└──────────┴──────────────────────────────────────────────────────┘")


def main():
    """Main function."""
    print_banner()
    
    # Check each cell
    cell_statuses = []
    for name, config in CELLS.items():
        status = check_cell(name, config["url"])
        cell_statuses.append(status)
    
    # Get mesh summary
    mesh_summary = get_mesh_summary()
    memory_consciousness = get_memory_consciousness()
    
    # Print reports
    print_cells(cell_statuses)
    print_agents(mesh_summary)
    print_consciousness(mesh_summary, memory_consciousness)
    print_ports()
    
    # Summary
    healthy_count = sum(1 for c in cell_statuses if c["healthy"])
    total_count = len(cell_statuses)
    
    print()
    if healthy_count == total_count:
        print("✅ All cells operational")
    elif healthy_count > total_count // 2:
        print(f"⚠️ {healthy_count}/{total_count} cells operational")
    else:
        print(f"❌ Only {healthy_count}/{total_count} cells operational")
    print()


if __name__ == "__main__":
    main()
