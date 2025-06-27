"""
Service Execution Manager (SEM)
-------------------------------
Bridges Python orchestration and C++ plugin execution.
Invokes C++ plugins with JSON commands and logs results for AI ingestion.

Usage:
    python sem.py --plugin <plugin_path> --command '{"action": "start", "params": {"foo": "bar"}}'
"""

import argparse
import subprocess
import json
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("sem.log"),
        logging.StreamHandler()
    ]
)

def run_plugin(plugin_path, command_json):
    try:
        result = subprocess.run(
            [plugin_path, command_json],
            capture_output=True,
            text=True,
            timeout=30
        )
        logging.info("Plugin output: %s", result.stdout.strip())
        if result.stderr:
            logging.error("Plugin error: %s", result.stderr.strip())
        return result.stdout.strip()
    except Exception as e:
        logging.error("Failed to run plugin: %s", e)
        return None

def main():
    parser = argparse.ArgumentParser(description="Service Execution Manager (SEM)")
    parser.add_argument("--plugin", type=str, default="../orchestrator/build/Release/PluginLoader.exe", help="Path to C++ plugin executable")
    parser.add_argument("--command", type=str, required=True, help="JSON command string")
    args = parser.parse_args()

    logging.info("Invoking plugin: %s", args.plugin)
    logging.info("Command: %s", args.command)
    output = run_plugin(args.plugin, args.command)
    if output:
        print(output)

if __name__ == "__main__":
    main()