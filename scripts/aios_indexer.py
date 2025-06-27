# ============================================================
# 🧠 aios_indexer.py
# Parses C++/C#/Python modules and generates:
# - docs/dependency_graph.dot (and .svg)
# - docs/services_registry.json
# - Harmonized AI-ingestible summaries
# ============================================================

import os
import json
from graphviz import Digraph

MODULE_DIRS = ['orchestrator', 'director', 'scripts']
SERVICE_KEYWORDS = ['IService', 'register', 'Plugin', 'load']

def extract_includes(content):
    return [line.strip().split('"')[1] for line in content.splitlines()
            if line.strip().startswith('#include') and '"' in line]

def discover_services(base_path):
    registry = []
    for module_dir in MODULE_DIRS:
        abs_dir = os.path.join(base_path, module_dir)
        for root, _, files in os.walk(abs_dir):
            for f in files:
                if f.endswith(('.cpp', '.cs', '.py')):
                    path = os.path.join(root, f)
                    try:
                        with open(path, 'r', encoding='utf-8') as file:
                            content = file.read()
                            if any(kw in content for kw in SERVICE_KEYWORDS):
                                registry.append({
                                    'name': os.path.splitext(f)[0],
                                    'path': os.path.relpath(path, base_path),
                                    'language': f.split('.')[-1],
                                    'summary': f"Detected service module at {path}",
                                    'dependencies': extract_includes(content)
                                })
                    except Exception as e:
                        print(f"Error reading {path}: {e}")
    return registry

def build_graph(registry, out_dot='docs/dependency_graph.dot', out_svg='docs/dependency_graph.svg'):
    dot = Digraph(comment='AIOS Dependency Graph')
    for svc in registry:
        dot.node(svc['name'])
        for dep in svc['dependencies']:
            dot.edge(svc['name'], dep)
    dot.render(out_dot, format='svg', cleanup=True)
    print(f"Dependency graph written to {out_dot} and {out_svg}")

def save_registry(registry, out_json='docs/services_registry.json'):
    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump(registry, f, indent=2)
    print(f"Service registry written to {out_json}")

if __name__ == '__main__':
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    registry = discover_services(base_path)
    build_graph(registry)
    save_registry(registry)
