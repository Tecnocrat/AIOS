#!/usr/bin/env python3
"""
IACP Message Receiver - Poll and process incoming IACP messages

AINLP.spatial_awareness: scripts/iacp_receive.py
AINLP.purpose: Automate IACP message reception and processing

Usage:
    python scripts/iacp_receive.py              # Check once
    python scripts/iacp_receive.py --watch      # Continuous polling
    python scripts/iacp_receive.py --process    # Process and respond
"""

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# Configuration
SCRIPT_DIR = Path(__file__).parent.parent
CELLS_DIR = SCRIPT_DIR / "server" / "stacks" / "cells"

# Message type priorities (lower = higher priority)
PRIORITY_ORDER = {
    "ESCALATION": 0,
    "SYNC": 1,
    "HANDSHAKE": 2,
    "GUIDANCE": 3,
    "DATA": 4,
    "HEARTBEAT": 5,
    "CONFIRMATION": 6,
}


def get_hostname() -> str:
    """Get current machine hostname."""
    import socket
    hostname = socket.gethostname().upper()
    if "AIOS" in hostname or hostname == os.environ.get("COMPUTERNAME", "").upper():
        return "AIOS"
    return hostname


def discover_messages(target_host: Optional[str] = None) -> List[Path]:
    """
    Discover pending IACP messages for this host.
    
    Looks for:
    - SYNC_{THIS_HOST}.md
    - GUIDANCE_{THIS_HOST}.md  
    - HANDSHAKE_*.md
    - *_RESPONSE_{THIS_HOST}.md
    """
    if not CELLS_DIR.exists():
        return []
    
    this_host = target_host or get_hostname()
    messages = []
    
    patterns = [
        f"SYNC_{this_host}.md",
        f"GUIDANCE_{this_host}.md",
        f"HANDSHAKE_*.md",
        f"*_RESPONSE_{this_host}.md",
        f"DATA_{this_host}.md",
        f"HEARTBEAT_{this_host}.md",
    ]
    
    for pattern in patterns:
        for filepath in CELLS_DIR.glob(pattern):
            if filepath.is_file():
                messages.append(filepath)
    
    return messages


def parse_message_file(filepath: Path) -> Optional[Dict[str, Any]]:
    """
    Parse IACP message from markdown or JSON file.
    
    Prefers .json sidecar if available.
    """
    json_path = filepath.with_suffix(".json")
    
    # Try JSON first
    if json_path.exists():
        try:
            return json.loads(json_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass
    
    # Parse markdown (basic extraction)
    content = filepath.read_text(encoding="utf-8")
    message = {
        "filepath": str(filepath),
        "filename": filepath.name,
        "raw_content": content,
    }
    
    # Extract header fields
    for line in content.split("\n"):
        if line.startswith("**From**:"):
            message["from"] = line.split(":", 1)[1].strip()
        elif line.startswith("**To**:"):
            message["to"] = line.split(":", 1)[1].strip()
        elif line.startswith("**Timestamp**:"):
            message["timestamp"] = line.split(":", 1)[1].strip()
        elif line.startswith("**Status**:"):
            message["status"] = line.split(":", 1)[1].strip()
        elif line.startswith("**Message ID**:"):
            message["message_id"] = line.split(":", 1)[1].strip()
    
    # Extract type from filename
    parts = filepath.stem.split("_")
    if parts:
        message["type"] = parts[0]
    
    return message


def display_message(message: Dict[str, Any], verbose: bool = False) -> None:
    """Display message summary."""
    filepath = message.get("filepath", "unknown")
    msg_type = message.get("type", "UNKNOWN")
    from_host = message.get("from", {})
    if isinstance(from_host, dict):
        from_host = from_host.get("hostname", "unknown")
    timestamp = message.get("timestamp", "unknown")
    status = message.get("status", "UNKNOWN")
    
    priority = PRIORITY_ORDER.get(msg_type, 99)
    icon = "🔴" if priority <= 1 else "🟡" if priority <= 3 else "🟢"
    
    print(f"{icon} [{msg_type}] from {from_host} ({status})")
    print(f"   📁 {filepath}")
    print(f"   🕐 {timestamp}")
    
    if verbose and "actions" in message:
        print("   📋 Actions:")
        for action in message["actions"]:
            print(f"      - {action.get('type', 'unknown')}: {action.get('description', '')}")
    
    if verbose and "aicp" in message:
        aicp = message["aicp"]
        print(f"   🤖 AICP: {aicp.get('intent', 'unknown')} ({aicp.get('trust_level', 'basic')})")
    
    print()


def poll_messages(watch: bool = False, interval: float = 30.0) -> None:
    """Poll for new messages."""
    this_host = get_hostname()
    print(f"📡 IACP Receiver - Listening for messages to {this_host}")
    print(f"📂 Channel: {CELLS_DIR}")
    print("-" * 50)
    
    seen_messages = set()
    
    while True:
        # Pull latest from git
        try:
            subprocess.run(
                ["git", "pull", "origin", "main", "--rebase"],
                cwd=SCRIPT_DIR,
                capture_output=True,
                check=True,
            )
        except subprocess.CalledProcessError:
            print("⚠️  Git pull failed")
        
        # Discover messages
        messages = discover_messages(this_host)
        new_messages = [m for m in messages if str(m) not in seen_messages]
        
        if new_messages:
            print(f"\n📬 {len(new_messages)} new message(s) found:")
            print("-" * 30)
            
            for filepath in new_messages:
                message = parse_message_file(filepath)
                if message:
                    display_message(message, verbose=True)
                    seen_messages.add(str(filepath))
        
        if not watch:
            if not messages:
                print("📭 No pending messages")
            break
        
        print(f"⏳ Polling again in {interval}s... (Ctrl+C to stop)")
        time.sleep(interval)


def process_messages(auto_respond: bool = False) -> None:
    """Process and optionally respond to messages."""
    this_host = get_hostname()
    messages = discover_messages(this_host)
    
    if not messages:
        print("📭 No messages to process")
        return
    
    print(f"📋 Processing {len(messages)} message(s)...")
    
    for filepath in messages:
        message = parse_message_file(filepath)
        if not message:
            continue
        
        display_message(message, verbose=True)
        
        msg_type = message.get("type", "UNKNOWN")
        from_host = message.get("from", {})
        if isinstance(from_host, dict):
            from_host = from_host.get("hostname", "unknown")
        
        # Process based on type
        if msg_type == "HEARTBEAT":
            print(f"   💓 Heartbeat from {from_host} - acknowledged")
            if auto_respond:
                # Mark as processed (delete file)
                filepath.unlink(missing_ok=True)
                json_path = filepath.with_suffix(".json")
                json_path.unlink(missing_ok=True)
                print(f"   🗑️  Cleaned up heartbeat message")
        
        elif msg_type == "SYNC":
            print(f"   🔄 Sync request from {from_host}")
            if "actions" in message:
                print("   📋 Required actions:")
                for action in message["actions"]:
                    print(f"      ⏳ {action.get('type')}: {action.get('description')}")
            print("   ℹ️  Use --respond to generate response")
        
        elif msg_type == "HANDSHAKE":
            print(f"   🤝 Handshake from {from_host}")
            print("   ℹ️  Review and respond manually")
        
        print()


def main():
    parser = argparse.ArgumentParser(
        description="IACP Message Receiver - Poll and process incoming messages"
    )
    parser.add_argument(
        "--watch", "-w",
        action="store_true",
        help="Continuous polling mode",
    )
    parser.add_argument(
        "--interval", "-i",
        type=float,
        default=30.0,
        help="Polling interval in seconds (default: 30)",
    )
    parser.add_argument(
        "--process", "-p",
        action="store_true",
        help="Process messages (show detailed info)",
    )
    parser.add_argument(
        "--auto-respond",
        action="store_true",
        help="Auto-respond to simple messages (heartbeats)",
    )
    parser.add_argument(
        "--host",
        help="Override target hostname",
    )
    
    args = parser.parse_args()
    
    if args.process:
        process_messages(auto_respond=args.auto_respond)
    else:
        poll_messages(watch=args.watch, interval=args.interval)


if __name__ == "__main__":
    main()
