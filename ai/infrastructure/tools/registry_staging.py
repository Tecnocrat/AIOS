#!/usr/bin/env python3
"""
Registry staging and rollback helper.

Commands:
  stage    - create staging copy of current registry
  promote  - promote staging copy to live registry (requires approval token)
  rollback - restore from latest backup

Safety:
  - Promotes require approval token via `--approval-token` or `AIOS_APPROVAL_TOKEN` env
  - All operations create timestamped backups
"""

import os
import shutil
import json
from datetime import datetime, timezone
from pathlib import Path


def now_ts():
    return datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')


class RegistryStager:
    def __init__(self, workspace_root: Path):
        self.root = workspace_root
        self.registry = self.root / 'tachyonic' / 'consciousness' / 'config_registry.json'
        self.staging = self.root / 'tachyonic' / 'consciousness' / 'config_registry.staging.json'

    def stage(self) -> Path:
        if not self.registry.exists():
            raise FileNotFoundError('Registry not found')
        timestamp = now_ts()
        bak = self.registry.with_name(self.registry.name + f'.bak.{timestamp}')
        shutil.copy2(self.registry, bak)
        shutil.copy2(self.registry, self.staging)
        return self.staging

    def promote(self, approval_token: str | None = None) -> Path:
        token = approval_token or os.getenv('AIOS_APPROVAL_TOKEN')
        if not token:
            raise PermissionError('approval token required to promote staging to live registry')
        if not self.staging.exists():
            raise FileNotFoundError('Staging registry not found')
        timestamp = now_ts()
        bak = self.registry.with_name(self.registry.name + f'.bak.{timestamp}')
        shutil.copy2(self.registry, bak)
        shutil.copy2(self.staging, self.registry)
        return self.registry

    def rollback(self) -> Path:
        # Find latest backup
        parent = self.registry.parent
        candidates = sorted(parent.glob(self.registry.name + '.bak.*'))
        if not candidates:
            raise FileNotFoundError('No backups found to rollback')
        latest = candidates[-1]
        shutil.copy2(latest, self.registry)
        return self.registry


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser(description='Registry staging/promote/rollback')
    p.add_argument('command', choices=['stage', 'promote', 'rollback'])
    p.add_argument('--workspace-root', default='.')
    p.add_argument('--approval-token', default=None)
    args = p.parse_args()

    stager = RegistryStager(Path(args.workspace_root))
    if args.command == 'stage':
        out = stager.stage()
        print(f'Staged registry: {out}')
    elif args.command == 'promote':
        try:
            out = stager.promote(approval_token=args.approval_token)
            print(f'Promoted staging to live: {out}')
        except Exception as e:
            print(f'Failed to promote: {e}')
            raise
    elif args.command == 'rollback':
        out = stager.rollback()
        print(f'Rolled back registry from backup: {out}')
