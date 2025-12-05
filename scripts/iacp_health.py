#!/usr/bin/env python3
"""
IACP Health Check - Mesh connectivity and agent status monitor

AINLP.spatial_awareness: scripts/iacp_health.py
AINLP.purpose: Monitor IACP mesh health, agent availability, protocol status

Usage:
    python scripts/iacp_health.py                 # Full health check
    python scripts/iacp_health.py --agents        # List registered agents
    python scripts/iacp_health.py --connectivity  # Test mesh connectivity
    python scripts/iacp_health.py --json          # JSON output
"""

import argparse
import json
import os
import socket
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
import urllib.request
import urllib.error

# Configuration
SCRIPT_DIR = Path(__file__).parent.parent
CELLS_DIR = SCRIPT_DIR / "server" / "stacks" / "cells"
HOSTS_CONFIG = SCRIPT_DIR / "config" / "hosts.yaml"

# Known hosts and their expected services
MESH_HOSTS = {
    "AIOS": {
        "ip": "192.168.1.128",
        "services": [
            {"name": "alpha", "port": 8000, "path": "/health"},
            {"name": "pure", "port": 8002, "path": "/health"},
            {"name": "discovery", "port": 8003, "path": "/health"},
            {"name": "prometheus", "port": 9090, "path": "/-/healthy"},
            {"name": "grafana", "port": 3000, "path": "/api/health"},
        ],
    },
    "HP_LAB": {
        "ip": "192.168.1.129",
        "services": [
            {"name": "alpha", "port": 8000, "path": "/health"},
        ],
    },
}

# Add ai modules to path for agent checking
sys.path.insert(0, str(SCRIPT_DIR / "ai"))


def get_hostname() -> str:
    """Get current machine hostname."""
    hostname = socket.gethostname().upper()
    if "AIOS" in hostname or hostname == os.environ.get("COMPUTERNAME", "").upper():
        return "AIOS"
    return hostname


def check_port(host: str, port: int, timeout: float = 2.0) -> bool:
    """Check if a port is reachable."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except (socket.error, socket.timeout):
        return False


def check_http_health(
    host: str, port: int, path: str, timeout: float = 3.0
) -> Dict[str, Any]:
    """Check HTTP health endpoint."""
    url = f"http://{host}:{port}{path}"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=timeout) as response:
            status = response.getcode()
            body = response.read().decode("utf-8")[:200]
            return {
                "reachable": True,
                "status_code": status,
                "healthy": status == 200,
                "response": body,
            }
    except urllib.error.HTTPError as e:
        return {
            "reachable": True,
            "status_code": e.code,
            "healthy": False,
            "error": str(e),
        }
    except (urllib.error.URLError, socket.timeout, ConnectionError, OSError) as e:
        return {
            "reachable": False,
            "healthy": False,
            "error": str(e),
        }


def check_mesh_connectivity() -> Dict[str, Any]:
    """Check connectivity to all mesh hosts."""
    results = {}
    this_host = get_hostname()
    
    for host_name, host_config in MESH_HOSTS.items():
        ip = host_config["ip"]
        host_results = {
            "ip": ip,
            "is_local": host_name == this_host,
            "ping": False,
            "services": {},
        }
        
        # Ping check
        try:
            if sys.platform == "win32":
                cmd = ["ping", "-n", "1", "-w", "1000", ip]
            else:
                cmd = ["ping", "-c", "1", "-W", "1", ip]
            
            result = subprocess.run(cmd, capture_output=True, timeout=3)
            host_results["ping"] = result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        
        # Service checks
        for service in host_config.get("services", []):
            svc_name = service["name"]
            port = service["port"]
            path = service.get("path", "/health")
            
            if host_results["is_local"]:
                # For local services, use localhost
                check_ip = "127.0.0.1"
            else:
                check_ip = ip
            
            service_result = check_http_health(check_ip, port, path)
            service_result["port"] = port
            host_results["services"][svc_name] = service_result
        
        results[host_name] = host_results
    
    return results


def check_agents() -> Dict[str, Any]:
    """Check registered AICP agents."""
    try:
        from protocols.aicp_discovery import create_aios_core_agents
        
        agents = create_aios_core_agents()
        return {
            "available": True,
            "count": len(agents),
            "agents": [
                {
                    "aid": agent.aid,
                    "name": agent.name,
                    "capabilities": [c.name for c in agent.capabilities],
                    "trust_level": agent.trust_level.value,
                }
                for agent in agents
            ],
        }
    except ImportError as e:
        return {
            "available": False,
            "error": f"AICP modules not available: {e}",
            "agents": [],
        }


def check_pending_messages() -> Dict[str, Any]:
    """Check for pending IACP messages."""
    if not CELLS_DIR.exists():
        return {"channel_exists": False, "pending": 0, "messages": []}
    
    message_files = list(CELLS_DIR.glob("*.md"))
    # Filter out permanent files
    permanent = {"ARCHITECTURE.md", "README.md"}
    pending = [f for f in message_files if f.name not in permanent]
    
    return {
        "channel_exists": True,
        "channel_path": str(CELLS_DIR),
        "pending": len(pending),
        "messages": [
            {
                "filename": f.name,
                "size": f.stat().st_size,
                "modified": datetime.fromtimestamp(
                    f.stat().st_mtime
                ).isoformat(),
            }
            for f in pending
        ],
    }


def check_git_status() -> Dict[str, Any]:
    """Check git repository status for IACP coordination."""
    try:
        # Current branch
        branch = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=SCRIPT_DIR,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
        
        # Last commit
        last_commit = subprocess.run(
            ["git", "log", "-1", "--format=%h %s", "--", "server/stacks/cells/"],
            cwd=SCRIPT_DIR,
            capture_output=True,
            text=True,
        ).stdout.strip()
        
        # Check for unpushed changes
        unpushed = subprocess.run(
            ["git", "log", "@{u}..", "--oneline"],
            cwd=SCRIPT_DIR,
            capture_output=True,
            text=True,
        ).stdout.strip()
        
        return {
            "branch": branch,
            "last_cells_commit": last_commit or "No commits in cells/",
            "unpushed_commits": len(unpushed.split("\n")) if unpushed else 0,
            "iacp_ready": branch.startswith("AIOS-win-") or branch == "main",
        }
    except subprocess.CalledProcessError as e:
        return {"error": str(e)}


def format_health_report(
    connectivity: Dict[str, Any],
    agents: Dict[str, Any],
    messages: Dict[str, Any],
    git: Dict[str, Any],
) -> str:
    """Format health report for display."""
    lines = [
        "=" * 60,
        "🏥 IACP MESH HEALTH REPORT",
        f"📅 {datetime.now().isoformat()}",
        f"🖥️  This Host: {get_hostname()}",
        "=" * 60,
        "",
    ]
    
    # Connectivity section
    lines.append("📡 MESH CONNECTIVITY")
    lines.append("-" * 40)
    for host_name, host_data in connectivity.items():
        icon = "🟢" if host_data["ping"] else "🔴"
        local = " (local)" if host_data["is_local"] else ""
        lines.append(f"{icon} {host_name} ({host_data['ip']}){local}")
        
        for svc_name, svc_data in host_data.get("services", {}).items():
            svc_icon = "✅" if svc_data.get("healthy") else "❌"
            port = svc_data.get("port", "?")
            lines.append(f"   {svc_icon} {svc_name}:{port}")
    lines.append("")
    
    # Agents section
    lines.append("🤖 AICP AGENTS")
    lines.append("-" * 40)
    if agents.get("available"):
        lines.append(f"✅ {agents['count']} agents registered")
        for agent in agents.get("agents", []):
            caps = ", ".join(agent.get("capabilities", []))
            lines.append(f"   • {agent['aid']}")
            lines.append(f"     Capabilities: {caps}")
    else:
        lines.append(f"❌ Agents unavailable: {agents.get('error', 'unknown')}")
    lines.append("")
    
    # Messages section
    lines.append("📬 IACP MESSAGE CHANNEL")
    lines.append("-" * 40)
    if messages.get("channel_exists"):
        pending = messages.get("pending", 0)
        icon = "📭" if pending == 0 else "📬"
        lines.append(f"{icon} {pending} pending message(s)")
        for msg in messages.get("messages", [])[:5]:
            lines.append(f"   • {msg['filename']}")
    else:
        lines.append("❌ Channel directory not found")
    lines.append("")
    
    # Git section
    lines.append("📂 GIT STATUS")
    lines.append("-" * 40)
    if "error" not in git:
        lines.append(f"🌿 Branch: {git.get('branch', 'unknown')}")
        lines.append(f"📝 Last cells commit: {git.get('last_cells_commit', 'N/A')}")
        unpushed = git.get("unpushed_commits", 0)
        if unpushed > 0:
            lines.append(f"⚠️  {unpushed} unpushed commit(s)")
        else:
            lines.append("✅ Fully synced")
        iacp_ready = "✅" if git.get("iacp_ready") else "⚠️"
        lines.append(f"{iacp_ready} IACP branch convention")
    else:
        lines.append(f"❌ Git error: {git.get('error')}")
    
    lines.append("")
    lines.append("=" * 60)
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="IACP Health Check - Mesh connectivity monitor"
    )
    parser.add_argument(
        "--agents", "-a",
        action="store_true",
        help="Show only registered agents",
    )
    parser.add_argument(
        "--connectivity", "-c",
        action="store_true",
        help="Show only connectivity status",
    )
    parser.add_argument(
        "--messages", "-m",
        action="store_true",
        help="Show only pending messages",
    )
    parser.add_argument(
        "--json", "-j",
        action="store_true",
        help="Output as JSON",
    )
    
    args = parser.parse_args()
    
    # Gather data
    connectivity = check_mesh_connectivity()
    agents = check_agents()
    messages = check_pending_messages()
    git = check_git_status()
    
    # Filter output
    if args.agents:
        data = agents
    elif args.connectivity:
        data = connectivity
    elif args.messages:
        data = messages
    else:
        data = {
            "connectivity": connectivity,
            "agents": agents,
            "messages": messages,
            "git": git,
            "timestamp": datetime.now().isoformat(),
            "host": get_hostname(),
        }
    
    # Output
    if args.json:
        print(json.dumps(data, indent=2, default=str))
    elif args.agents or args.connectivity or args.messages:
        print(json.dumps(data, indent=2, default=str))
    else:
        report = format_health_report(connectivity, agents, messages, git)
        print(report)


if __name__ == "__main__":
    main()
