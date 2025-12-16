#!/usr/bin/env python3
"""
Semantic Compression Analysis Script
"""
from pathlib import Path
import sys
# Add the tools directory to path
sys.path.append('ai/src/tools')
from semantic_validator import IntelligenceDelimitationValidator

def main():
    # Analyze runtime directory
    validator = IntelligenceDelimitationValidator(Path('runtime'))
    compression = validator.apply_semantic_compression(dry_run=True)

    print('=== Semantic Compression Analysis ===')
    print(f'Transformations to apply: {len(compression["transformations_applied"])}')

    total_changes = sum(len(t['changes']) for t in compression['transformations_applied'])
    print(f'Total line changes: {total_changes}')

    print('\nFiles to be modified:')
    for transform in compression['transformations_applied']:
        file_path = Path(transform["file"])
        print(f'  {file_path.name}: {len(transform["changes"])} changes')

    # Show sample changes from first file
    if compression['transformations_applied']:
        first_file = compression['transformations_applied'][0]
        print(f'\nSample changes from {Path(first_file["file"]).name}:')
        for change in first_file['changes'][:3]:  # Show first 3 changes
            print(f'  {change}')

if __name__ == "__main__":
    main()