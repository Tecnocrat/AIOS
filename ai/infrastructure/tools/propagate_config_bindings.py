#!/usr/bin/env python3
"""
Propagate workspace bindings from the semantic registry to tool config files.
Performs schema validation, atomic writes with backups, and idempotent propagation.

Usage examples:
  python propagate_config_bindings.py --registry tachyonic/consciousness/config_registry.json
  python propagate_config_bindings.py --dry-run --workspace "AIOS/core"

Features:
- Validates registry against provided schema (optional if jsonschema not installed)
- For each `workspace_bindings`, applies configured files (c_cpp_properties.json, settings.json)
- Writes files atomically and creates timestamped backups
- Updates `last_sync` and `propagation_status` in registry and writes registry atomically
"""

import argparse
import json
import json5
import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import jsonschema
    JSONSCHEMA_AVAILABLE = True
except Exception:
    JSONSCHEMA_AVAILABLE = False


def now_z():
    return datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')


class Propagator:
    def __init__(self, workspace_root: Path, registry_path: Path, schema_path: Path | None = None, dry_run: bool = False, approval_token: str | None = None):
        self.workspace_root = workspace_root
        self.registry_path = registry_path
        self.schema_path = schema_path
        self.dry_run = dry_run
        self.approval_token = approval_token or os.getenv('AIOS_APPROVAL_TOKEN')

    def load_registry(self) -> dict:
        if not self.registry_path.exists():
            raise FileNotFoundError(f"Registry not found: {self.registry_path}")
        with open(self.registry_path, 'r', encoding='utf-8') as f:
            return json5.load(f)

    def validate_registry(self, registry: dict) -> bool:
        if not self.schema_path:
            print('  ℹ️  No schema provided; skipping schema validation')
            return True
        if not JSONSCHEMA_AVAILABLE:
            print('  ⚠️  jsonschema not installed; skipping schema validation. Install with `pip install jsonschema`')
            return True
        with open(self.schema_path, 'r', encoding='utf-8') as f:
            schema = json.load(f)
        try:
            jsonschema.validate(instance=registry, schema=schema)
            print('  ✅ Registry schema validation: OK')
            return True
        except Exception as e:
            print(f'  ❌ Registry schema validation failed: {e}')
            return False

    def _atomic_write(self, target: Path, content: dict) -> None:
        tmp = target.with_name(target.name + '.tmp')
        timestamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')
        bak = target.with_name(target.name + f'.bak.{timestamp}')

        target.parent.mkdir(parents=True, exist_ok=True)

        if target.exists():
            shutil.copy2(target, bak)
            print(f'    🔐 Backup: {bak}')

        with open(tmp, 'w', encoding='utf-8') as f:
            json.dump(content, f, indent=2)

        # validate by reading back
        with open(tmp, 'r', encoding='utf-8') as f:
            _ = json.load(f)

        os.replace(str(tmp), str(target))
        print(f'    ✅ Wrote: {target}')

    def apply_binding(self, binding_name: str, binding: dict, registry: dict) -> None:
        print(f'  ▶ Applying binding: {binding_name}')
        compiler_key = binding.get('compiler')
        if not compiler_key:
            print('    ⚠️  binding missing `compiler` key; skipping')
            return
        comp = registry.get('compilers', {}).get(compiler_key)
        if not comp:
            print(f'    ⚠️  compiler `{compiler_key}` not found in registry; skipping')
            return
        msvc_cfg = comp.get('configuration', {})

        files = binding.get('configuration_files', [])
        for rel in files:
            target = self.workspace_root / rel
            if 'c_cpp_properties.json' in target.name:
                # Create c_cpp_properties.json content
                cpp_props = {
                    'configurations': [
                        {
                            'name': 'Win32',
                            'intelliSenseMode': msvc_cfg.get('intelliSenseMode'),
                            'compilerPath': msvc_cfg.get('compilerPath'),
                            'cStandard': msvc_cfg.get('cStandard'),
                            'cppStandard': msvc_cfg.get('cppStandard'),
                            'includePath': msvc_cfg.get('includePath', []),
                            'defines': msvc_cfg.get('defines', []),
                        }
                    ],
                    'version': 4,
                }
                if self.dry_run:
                    print(f'    (dry-run) would write {target}')
                else:
                    self._atomic_write(target, cpp_props)
            elif 'settings.json' in target.name:
                # Read existing (json5) or start new
                settings = {}
                if target.exists():
                    try:
                        with open(target, 'r', encoding='utf-8') as f:
                            settings = json5.load(f)
                    except Exception:
                        settings = {}

                settings['C_Cpp.default.intelliSenseMode'] = msvc_cfg.get('intelliSenseMode')
                settings['C_Cpp.default.compilerPath'] = msvc_cfg.get('compilerPath')
                settings['C_Cpp.default.cStandard'] = msvc_cfg.get('cStandard')
                settings['C_Cpp.default.cppStandard'] = msvc_cfg.get('cppStandard')

                settings['_dendritic_metadata'] = {
                    'source': 'tachyonic::consciousness::config_registry',
                    'last_propagated': now_z(),
                    'agent': 'propagate_config_bindings.py',
                }

                if self.dry_run:
                    print(f'    (dry-run) would update {target}')
                else:
                    self._atomic_write(target, settings)
            else:
                print(f'    ⚠️  Unsupported binding target: {target} (skipping)')

        # On successful propagation, update registry entry
        if not self.dry_run:
            binding['propagation_status'] = 'auto'
            binding['last_sync'] = now_z()

    def run(self, workspace_filter: str | None = None) -> int:
        registry = self.load_registry()
        if not self.validate_registry(registry):
            print('  ❌ Registry validation failed; aborting')
            return 2

        bindings = registry.get('workspace_bindings', {})
        if workspace_filter:
            bindings = {k: v for k, v in bindings.items() if k == workspace_filter}

        if not bindings:
            print('  ℹ️  No workspace_bindings to apply')

        for name, binding in bindings.items():
            try:
                self.apply_binding(name, binding, registry)
            except Exception as e:
                print(f'    ❌ Failed to apply binding {name}: {e}')

        # Write registry back with updated last_sync fields
        if not self.dry_run:
            # attach provenance
            prov_entry = {
                'actor': os.getenv('AIOS_LAST_EDITOR') or os.getenv('USER') or os.getenv('USERNAME') or 'propagator',
                'method': 'propagate_config_bindings.run',
                'timestamp': now_z(),
                'change_ticket': os.getenv('AIOS_CHANGE_TICKET'),
                'approval_token_provided': bool(self.approval_token),
            }
            registry.setdefault('metadata', {}).setdefault('provenance', {}).setdefault('sources', []).append(prov_entry)
            registry.setdefault('metadata', {})['last_updated'] = now_z()

            # atomic write registry
            tmp = self.registry_path.with_name(self.registry_path.name + '.tmp')
            timestamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')
            bak = self.registry_path.with_name(self.registry_path.name + f'.bak.{timestamp}')
            try:
                if self.registry_path.exists():
                    shutil.copy2(self.registry_path, bak)
                    print(f'  🔐 Registry backup: {bak}')
                with open(tmp, 'w', encoding='utf-8') as f:
                    json.dump(registry, f, indent=2)
                with open(tmp, 'r', encoding='utf-8') as f:
                    _ = json.load(f)
                os.replace(str(tmp), str(self.registry_path))
                print(f'  ✅ Registry updated: {self.registry_path}')
            except Exception as e:
                print(f'  ❌ Failed to write registry: {e}')
                return 3

        return 0


def main():
    parser = argparse.ArgumentParser(description='Propagate workspace bindings from registry')
    parser.add_argument('--registry', default='tachyonic/consciousness/config_registry.json')
    parser.add_argument('--schema', default='tachyonic/consciousness/schemas/config_registry.v1.json')
    parser.add_argument('--workspace-root', default='.')
    parser.add_argument('--workspace', default=None, help='Apply only a single workspace binding')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--approval-token', default=None)
    args = parser.parse_args()

    workspace_root = Path(args.workspace_root)
    registry_path = workspace_root / args.registry
    schema_path = workspace_root / args.schema if args.schema else None

    propagator = Propagator(workspace_root, registry_path, schema_path, dry_run=args.dry_run, approval_token=args.approval_token)
    rc = propagator.run(workspace_filter=args.workspace)
    sys.exit(rc)


if __name__ == '__main__':
    main()
