#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Database File Search Script
Check if attached README files are stored in AIOS databases
"""

import sqlite3
import os
from pathlib import Path

# Database files to check
db_files = [
    'ai/tools/database/tachyonic/aios_data.db',
    'docs/archive/tachyonic/tachyonic_archive.db',
    'runtime/context/knowledge_crystals.db',
    'runtime/logs/sessions/session_AIOS_20250811_220407_3e2543c7.db',
    'runtime/logs/sessions/session_AIOS_20250811_220422_48da9d15.db',
    'runtime/logs/sessions/session_AIOS_20250813_235739_d04bb138.db',
    'runtime/logs/sessions/session_AIOS_20250816_172409_0485427a.db',
    'runtime/logs/sessions/session_AIOS_20250816_174844_47b01432.db',
    'runtime/logs/sessions/session_AIOS_20250829_114350_09456140.db',
    'tachyonic/archive/code_archive.db'
]

# Files to check for
target_files = [
    'tachyonic/archive/runtime/README_archived_20251025_213000.md',
    'tachyonic/archive/runtime/README.md'
]

def check_database_for_files(db_file, target_files):
    """Check a single database for target files"""
    if not os.path.exists(db_file):
        return False, f"Database not found: {db_file}"

    found_files = []

    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Check different table structures
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()

        for table_name in [t[0] for t in tables]:
            try:
                # Try different column patterns
                cursor.execute(f'PRAGMA table_info({table_name})')
                columns = cursor.fetchall()
                col_names = [c[1] for c in columns]

                # Check for filename/path columns
                if 'filename' in col_names or 'file_path' in col_names:
                    for col in ['filename', 'file_path']:
                        if col in col_names:
                            cursor.execute(f'SELECT {col} FROM {table_name}')
                            paths = cursor.fetchall()
                            for path_tuple in paths:
                                path = path_tuple[0]
                                for target in target_files:
                                    if target in path or path in target:
                                        found_files.append((table_name, col, path))

                # Check content columns for file content
                if 'content' in col_names:
                    cursor.execute("SELECT rowid, content FROM " + table_name + " WHERE content LIKE ?", ('%README_archived_20251025_213000%',))
                    results = cursor.fetchall()
                    if results:
                        for row in results:
                            found_files.append((table_name, 'content', f'Row {row[0]}: contains README_archived_20251025_213000'))

            except Exception as e:
                print(f'   ⚠️ Error checking table {table_name}: {e}')

        conn.close()

    except Exception as e:
        return False, f"Error accessing database {db_file}: {e}"

    return found_files, None

def main():
    print('🔍 Checking database storage for attached files...')
    print()

    all_found_files = []

    for db_file in db_files:
        found_files, error = check_database_for_files(db_file, target_files)

        if error:
            print(f'❌ {error}')
            print()
            continue

        print(f'📊 Checking database: {db_file}')

        if isinstance(found_files, list) and found_files:
            print(f'   ✅ FOUND FILES:')
            for table, col, path in found_files:
                print(f'      Table: {table}, Column: {col}, Path: {path}')
                all_found_files.append((db_file, table, col, path))
        else:
            print(f'   ❌ No target files found')

        print()

    if all_found_files:
        print('🎯 SUMMARY: Target files found in databases!')
        for db, table, col, path in all_found_files:
            print(f'   {db} → {table}.{col}: {path}')
        return True
    else:
        print('🎯 SUMMARY: No target files found in any database.')
        return False

if __name__ == "__main__":
    main()