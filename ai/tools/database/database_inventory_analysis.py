#!/usr/bin/env python3
"""
AIOS Database Inventory Analysis
===============================

Comprehensive analysis of all database files in AIOS workspace.
"""

import sqlite3
import os
from pathlib import Path
from datetime import datetime


def analyze_database(db_path, name):
    """Analyze a single database file"""
    print(f"\n=== {name.upper()} ===")
    print(f"Path: {db_path}")

    if not os.path.exists(db_path):
        print("❌ Database file not found")
        return

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Get file size
        size = os.path.getsize(db_path)
        print(f"Size: {size:,} bytes ({size/1024/1024:.2f} MB)")

        # Get tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"Tables: {[t[0] for t in tables]}")

        # Analyze each table
        for table_name, in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"  {table_name}: {count:,} records")

            # Sample data for small tables
            if count <= 10:
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 3")
                samples = cursor.fetchall()
                if samples:
                    print(f"    Sample: {samples[0]}")
                    if len(samples) > 1:
                        print(f"           {samples[1]}")

        conn.close()

    except Exception as e:
        print(f"❌ Error analyzing database: {e}")


def main():
    """Main analysis function"""
    print("🔍 AIOS Database Inventory Analysis")
    print("=" * 50)

    # Define database locations
    databases = [
        ("ai/tools/database/tachyonic/aios_data.db", "Main AIOS Database"),
        ("docs/archive/tachyonic/tachyonic_archive.db", "Tachyonic Archive DB"),
        ("runtime/logs/sessions/session_AIOS_20250811_220407_3e2543c7.db", "Session DB 1"),
        ("runtime/logs/sessions/session_AIOS_20250811_220422_48da9d15.db", "Session DB 2"),
        ("runtime/logs/sessions/session_AIOS_20250813_235739_d04bb138.db", "Session DB 3"),
        ("runtime/logs/sessions/session_AIOS_20250816_172409_0485427a.db", "Session DB 4"),
        ("runtime/logs/sessions/session_AIOS_20250816_174844_47b01432.db", "Session DB 5"),
        ("runtime/logs/sessions/session_AIOS_20250829_114350_09456140.db", "Session DB 6"),
    ]

    base_path = Path("../../..")  # From ai/tools/database to AIOS root

    for db_rel_path, name in databases:
        db_full_path = base_path / db_rel_path
        analyze_database(str(db_full_path), name)

    print(f"\n📊 Total databases analyzed: {len(databases)}")
    print(f"📅 Analysis completed: {datetime.now().isoformat()}")


if __name__ == "__main__":
    main()