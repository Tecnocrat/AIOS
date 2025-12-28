#!/usr/bin/env python3
import json

with open('aios_gemini_bridge_config.json', 'r') as f:
    config = json.load(f)

mcp_servers = config['gemini_cli_config']['mcpServers']
print(f'Configured MCP servers: {len(mcp_servers)}')
for name, server in mcp_servers.items():
    print(f'  - {name}: {server["description"]}')