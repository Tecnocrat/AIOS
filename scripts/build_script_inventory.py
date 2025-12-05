#!/usr/bin/env python3
"""
AINLP.testing[BUILD_INVENTORY] - Script Inventory Builder

Analyzes all Python scripts in AIOS codebase and generates
comprehensive inventory for agentic auto-upgrader paths.
"""

import ast
import json
from pathlib import Path
from datetime import datetime

def build_inventory():
    """Build comprehensive script inventory."""
    print('=' * 70)
    print('AINLP.testing[BUILD_INVENTORY] - Script Analysis')
    print('=' * 70)
    
    inventory = {
        'generated': datetime.now().isoformat(),
        'version': '1.0.0',
        'categories': {},
        'stats': {
            'total': 0,
            'valid': 0,
            'has_main': 0,
            'has_class': 0,
            'syntax_errors': 0
        }
    }
    
    # Directories to scan
    scan_dirs = [
        ('scripts', Path('scripts')),
        ('ai_tools_root', Path('ai/tools')),
        ('system', Path('ai/tools/system')),
        ('consciousness', Path('ai/tools/consciousness')),
        ('architecture', Path('ai/tools/architecture')),
        ('tachyonic', Path('ai/tools/tachyonic')),
        ('visual', Path('ai/tools/visual')),
        ('database', Path('ai/tools/database')),
        ('archival', Path('ai/tools/archival')),
        ('protocols', Path('ai/protocols')),
        ('runtime_tools', Path('runtime_intelligence/tools')),
    ]
    
    for cat_name, cat_path in scan_dirs:
        if not cat_path.exists():
            continue
        
        files = list(cat_path.glob('*.py'))
        files = [f for f in files if not f.name.startswith('__')]
        
        cat_data = []
        for py_file in files:
            inventory['stats']['total'] += 1
            try:
                content = py_file.read_text(encoding='utf-8')
                tree = ast.parse(content)
                inventory['stats']['valid'] += 1
                
                # Extract metadata
                classes = [n.name for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]
                functions = [n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
                has_main = 'main' in functions or '__main__' in content
                
                if has_main:
                    inventory['stats']['has_main'] += 1
                if classes:
                    inventory['stats']['has_class'] += 1
                
                docstring = ast.get_docstring(tree) or ''
                
                cat_data.append({
                    'name': py_file.name,
                    'path': str(py_file),
                    'classes': classes[:5],
                    'functions': [f for f in functions if not f.startswith('_')][:5],
                    'has_main': has_main,
                    'docstring': docstring[:200] if docstring else None,
                    'lines': len(content.split('\n'))
                })
            except SyntaxError:
                inventory['stats']['syntax_errors'] += 1
                cat_data.append({
                    'name': py_file.name,
                    'path': str(py_file),
                    'error': 'syntax_error'
                })
            except Exception as e:
                cat_data.append({
                    'name': py_file.name,
                    'path': str(py_file),
                    'error': str(e)[:50]
                })
        
        if cat_data:
            inventory['categories'][cat_name] = cat_data
    
    # Save inventory
    output_dir = Path('docs/AINLP/testing')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / 'SCRIPT_INVENTORY.json'
    with open(output_file, 'w') as f:
        json.dump(inventory, f, indent=2)
    
    # Print summary
    stats = inventory['stats']
    print(f'\n📊 INVENTORY COMPLETE')
    print(f'   Total scripts: {stats["total"]}')
    print(f'   Valid syntax: {stats["valid"]}')
    print(f'   Syntax errors: {stats["syntax_errors"]}')
    print(f'   Executable (has main): {stats["has_main"]}')
    print(f'   Has classes: {stats["has_class"]}')
    print(f'\n📁 Categories:')
    for cat_name, cat_data in inventory['categories'].items():
        print(f'   {cat_name}: {len(cat_data)} files')
    
    print(f'\n✅ Saved to: {output_file}')
    return inventory


if __name__ == '__main__':
    build_inventory()
