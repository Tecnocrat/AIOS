#!/usr/bin/env python3
import requests

# Test evolution_mcp_server execution with correct tool name
url = 'http://localhost:8000/tools/evolution_mcp_server/execute'
response = requests.post(url, json={'tool_name': 'get_evolution_status'})

print(f'Status: {response.status_code}')
if response.status_code == 200:
    result = response.json()
    print('Success! Tool executed.')
    print(f'Return code: {result.get("return_code")}')
    print(f'Stdout: {result.get("stdout", "")[:200]}...')
else:
    print(f'Error: {response.text}')