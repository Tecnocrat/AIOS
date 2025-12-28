#!/usr/bin/env python3
import requests

response = requests.get('http://localhost:8000/tools')
if response.status_code == 200:
    data = response.json()
    tools = data.get('tools', [])
    print(f'Tools count: {len(tools)}')
    print('Tools:')
    for tool in tools:
        if isinstance(tool, dict):
            desc = tool.get("description", "No description")
            print(f'  - {tool["name"]}: {desc[:50]}...')
        else:
            print(f'  - {tool}')
else:
    print(f'Error: {response.status_code}')