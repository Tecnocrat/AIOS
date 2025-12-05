#!/usr/bin/env python3
"""
IACP Message Sender - Generate and commit IACP messages to git

AINLP.spatial_awareness: scripts/iacp_send.py
AINLP.purpose: Automate IACP message generation with schema validation

Usage:
    python scripts/iacp_send.py --type SYNC --to HP_LAB --action TEST_CONNECTIVITY
    python scripts/iacp_send.py --type HEARTBEAT --to HP_LAB
    python scripts/iacp_send.py --type GUIDANCE --to HP_LAB --message "Deploy cell"
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from uuid import uuid4

# Add ai modules to path
SCRIPT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(SCRIPT_DIR / "ai"))

try:
    from protocols.aicp_core import AIIntent, AITrustLevel
    AICP_AVAILABLE = True
except ImportError:
    AICP_AVAILABLE = False

# Configuration
CELLS_DIR = SCRIPT_DIR / "server" / "stacks" / "cells"
SCHEMA_PATH = SCRIPT_DIR / "ai" / "protocols" / "schemas" / "iacp-message-v1.0.0.json"
HOSTS_CONFIG = SCRIPT_DIR / "config" / "hosts.yaml"

# Host registry (fallback if hosts.yaml unavailable)
KNOWN_HOSTS = {
    "AIOS": {"ip": "192.168.1.128", "branch": "AIOS-win-0-AIOS"},
    "HP_LAB": {"ip": "192.168.1.129", "branch": "AIOS-win-0-HP_LAB"},
}


def get_hostname() -> str:
    """Get current machine hostname."""
    import socket
    hostname = socket.gethostname().upper()
    # Map common patterns
    if "AIOS" in hostname or hostname == os.environ.get("COMPUTERNAME", "").upper():
        return "AIOS"
    return hostname


def generate_message(
    msg_type: str,
    to_host: str,
    actions: Optional[List[Dict[str, Any]]] = None,
    payload: Optional[Dict[str, Any]] = None,
    aicp_intent: Optional[str] = None,
) -> Dict[str, Any]:
    """Generate IACP message following schema."""
    from_host = get_hostname()
    
    message = {
        "protocol": "IACP",
        "version": "1.0.0",
        "type": msg_type.upper(),
        "from": {
            "hostname": from_host,
            "ip": KNOWN_HOSTS.get(from_host, {}).get("ip", "unknown"),
            "branch": KNOWN_HOSTS.get(from_host, {}).get(
                "branch", f"AIOS-win-0-{from_host}"
            ),
        },
        "to": {
            "hostname": to_host.upper(),
            "ip": KNOWN_HOSTS.get(to_host.upper(), {}).get("ip", "unknown"),
            "branch": KNOWN_HOSTS.get(to_host.upper(), {}).get(
                "branch", f"AIOS-win-0-{to_host.upper()}"
            ),
        },
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "status": "PENDING",
        "message_id": str(uuid4()),
    }
    
    if actions:
        message["actions"] = actions
    
    if payload:
        message["payload"] = payload
    
    # Add AICP extension if available
    if AICP_AVAILABLE and aicp_intent:
        message["aicp"] = {
            "intent": aicp_intent,
            "trust_level": "enterprise",
            "source_aid": f"agent://tecnocrat/{from_host.lower()}",
            "target_aid": f"agent://tecnocrat/{to_host.lower()}",
        }
    
    return message


def message_to_markdown(message: Dict[str, Any]) -> str:
    """Convert IACP message to markdown format."""
    lines = [
        f"# {message['type']}: {message['from']['hostname']} → {message['to']['hostname']}",
        "",
        "**AINLP.dendritic Sync Protocol** | **Ephemeral**: Delete after acknowledgment",
        "",
        f"**From**: {message['from']['hostname']} ({message['from'].get('ip', 'unknown')})",
        f"**To**: {message['to']['hostname']} ({message['to'].get('ip', 'unknown')})",
        f"**Timestamp**: {message['timestamp']}",
        f"**Status**: {message['status']}",
        f"**Message ID**: {message['message_id']}",
        "",
        "---",
        "",
    ]
    
    # Actions section
    if "actions" in message:
        lines.append("## Actions Required")
        lines.append("")
        for i, action in enumerate(message["actions"], 1):
            lines.append(f"{i}. **{action['type']}**: {action.get('description', '')}")
            if "parameters" in action:
                lines.append(f"   - Parameters: `{json.dumps(action['parameters'])}`")
        lines.append("")
    
    # Payload section
    if "payload" in message:
        lines.append("## Payload")
        lines.append("")
        lines.append("```json")
        lines.append(json.dumps(message["payload"], indent=2))
        lines.append("```")
        lines.append("")
    
    # AICP section
    if "aicp" in message:
        lines.append("## AICP Extension")
        lines.append("")
        lines.append(f"- **Intent**: {message['aicp'].get('intent', 'unknown')}")
        lines.append(f"- **Trust Level**: {message['aicp'].get('trust_level', 'basic')}")
        lines.append(f"- **Source AID**: {message['aicp'].get('source_aid', '')}")
        lines.append(f"- **Target AID**: {message['aicp'].get('target_aid', '')}")
        lines.append("")
    
    # Response protocol
    lines.extend([
        "---",
        "",
        "## Response Protocol",
        "",
        f"1. Execute actions above",
        f"2. Create `{message['type']}_RESPONSE_{message['from']['hostname']}.md`",
        f"3. Commit with prefix: `AINLP.{message['type'].lower()}({message['to']['hostname']})`",
        "",
    ])
    
    return "\n".join(lines)


def write_message(message: Dict[str, Any], dry_run: bool = False) -> Path:
    """Write message to cells directory."""
    filename = f"{message['type']}_{message['to']['hostname']}.md"
    filepath = CELLS_DIR / filename
    
    content = message_to_markdown(message)
    
    if dry_run:
        print(f"Would write to: {filepath}")
        print("-" * 40)
        print(content)
        return filepath
    
    CELLS_DIR.mkdir(parents=True, exist_ok=True)
    filepath.write_text(content, encoding="utf-8")
    print(f"✅ Message written: {filepath}")
    
    # Also write JSON version for programmatic access
    json_path = filepath.with_suffix(".json")
    json_path.write_text(json.dumps(message, indent=2), encoding="utf-8")
    
    return filepath


def git_commit_and_push(filepath: Path, message: Dict[str, Any]) -> bool:
    """Commit and push the message file."""
    try:
        commit_msg = (
            f"AINLP.{message['type'].lower()}({message['to']['hostname']}): "
            f"{message.get('actions', [{}])[0].get('type', 'message')}"
        )
        
        # Add both .md and .json
        subprocess.run(
            ["git", "add", str(filepath), str(filepath.with_suffix(".json"))],
            cwd=SCRIPT_DIR,
            check=True,
        )
        
        subprocess.run(
            ["git", "commit", "-m", commit_msg],
            cwd=SCRIPT_DIR,
            check=True,
        )
        
        subprocess.run(
            ["git", "push", "origin", "main"],
            cwd=SCRIPT_DIR,
            check=True,
        )
        
        print(f"✅ Committed and pushed: {commit_msg}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Git operation failed: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="IACP Message Sender - Generate and commit IACP messages"
    )
    parser.add_argument(
        "--type", "-t",
        required=True,
        choices=["SYNC", "HANDSHAKE", "DATA", "HEARTBEAT", "GUIDANCE", "CONFIRMATION"],
        help="Message type",
    )
    parser.add_argument(
        "--to",
        required=True,
        help="Target host (e.g., HP_LAB, AIOS)",
    )
    parser.add_argument(
        "--action", "-a",
        action="append",
        choices=[
            "FIREWALL_ADD", "FIREWALL_REMOVE",
            "CONTAINER_START", "CONTAINER_STOP", "CONTAINER_RESTART",
            "CONFIG_UPDATE", "TEST_CONNECTIVITY",
            "SYNC_FILES", "EXECUTE_SCRIPT",
            "REGISTER_AGENT", "DEREGISTER_AGENT",
        ],
        help="Action to request (can be repeated)",
    )
    parser.add_argument(
        "--message", "-m",
        help="Custom message/description",
    )
    parser.add_argument(
        "--intent", "-i",
        choices=[
            "discover", "announce", "query", "respond", "broadcast",
            "sync", "delegate", "coordinate", "heartbeat", "shutdown",
        ],
        default="sync",
        help="AICP intent type",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print message without writing/committing",
    )
    parser.add_argument(
        "--no-push",
        action="store_true",
        help="Write message but don't commit/push",
    )
    
    args = parser.parse_args()
    
    # Build actions list
    actions = []
    if args.action:
        for action_type in args.action:
            actions.append({
                "type": action_type,
                "description": args.message or f"Execute {action_type}",
            })
    elif args.message:
        actions.append({
            "type": "EXECUTE_SCRIPT",
            "description": args.message,
        })
    
    # Build payload
    payload = {}
    if args.message and not actions:
        payload["message"] = args.message
    
    # Generate message
    message = generate_message(
        msg_type=args.type,
        to_host=args.to,
        actions=actions if actions else None,
        payload=payload if payload else None,
        aicp_intent=args.intent,
    )
    
    # Write message
    filepath = write_message(message, dry_run=args.dry_run)
    
    if args.dry_run:
        return
    
    # Commit and push
    if not args.no_push:
        git_commit_and_push(filepath, message)
    else:
        print("ℹ️  Message written but not committed (--no-push)")


if __name__ == "__main__":
    main()
