#!/usr/bin/env python3
"""
Apply Semantic Compression Script
"""
from pathlib import Path
import sys
import json
from datetime import datetime

# Add the tools directory to path
sys.path.append('ai/src/tools')
from semantic_validator import IntelligenceDelimitationValidator

def main():
    print('=== Applying Semantic Compression ===')

    validator = IntelligenceDelimitationValidator(Path('runtime'))
    compression = validator.apply_semantic_compression(dry_run=False)

    print(f'Files modified: {compression["files_modified"]}')
    print(f'Transformations applied: {len(compression["transformations_applied"])}')

    # Archive the compression report
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    archive_path = Path('tachyonic/archive/runtime')
    archive_path.mkdir(parents=True, exist_ok=True)
    report_file = archive_path / f'semantic_compression_applied_{timestamp}.json'

    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(compression, f, indent=2)

    print(f'Compression report archived: {report_file}')
    print('✅ Semantic compression completed successfully!')

if __name__ == "__main__":
    main()