import sqlite3
import os
import hashlib
from datetime import datetime

def examine_database(db_path):
    """Examine the database structure"""
    if not os.path.exists(db_path):
        print(f"Database {db_path} does not exist")
        return None

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    print(f"Database: {db_path}")
    print(f"Tables: {[table[0] for table in tables]}")

    # Examine each table structure
    for table_name, in tables:
        print(f"\nTable: {table_name}")
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        print("Columns:")
        for col in columns:
            print(f"  {col[1]} ({col[2]})")

        # Sample data
        try:
            cursor.execute(f"SELECT * FROM {table_name} LIMIT 3")
            rows = cursor.fetchall()
            print(f"Sample data ({len(rows)} rows):")
            for row in rows:
                print(f"  {row}")
        except Exception as e:
            print(f"Error reading data: {e}")

    conn.close()
    return tables

def store_file_in_database(db_path, file_path, content):
    """Store a file in the database"""
    if not os.path.exists(db_path):
        print(f"Creating new database: {db_path}")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Create archives table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS archives (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_path TEXT NOT NULL,
                content TEXT NOT NULL,
                content_hash TEXT NOT NULL,
                archived_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                file_size INTEGER,
                metadata TEXT
            )
        ''')

        # Create index on file_path for faster lookups
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_file_path ON archives(file_path)
        ''')

        conn.commit()
    else:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

    # Calculate content hash
    content_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()

    # Check if file already exists
    cursor.execute("SELECT id FROM archives WHERE file_path = ? AND content_hash = ?",
                   (file_path, content_hash))
    existing = cursor.fetchone()

    if existing:
        print(f"File {file_path} already exists in database (ID: {existing[0]})")
        conn.close()
        return False

    # Insert the file
    file_size = len(content.encode('utf-8'))
    metadata = f'{{"original_path": "{file_path}", "archived_date": "{datetime.now().isoformat()}"}}'

    cursor.execute('''
        INSERT INTO archives (file_path, content, content_hash, file_size, metadata)
        VALUES (?, ?, ?, ?, ?)
    ''', (file_path, content, content_hash, file_size, metadata))

    archive_id = cursor.lastrowid
    conn.commit()
    conn.close()

    print(f"Successfully stored {file_path} in database (ID: {archive_id})")
    return True

def main():
    db_path = r"c:\dev\AIOS\docs\archive\tachyonic\tachyonic_archive.db"

    # Examine database structure
    print("=== DATABASE EXAMINATION ===")
    tables = examine_database(db_path)

    # Files to archive
    files_to_archive = [
        r"c:\dev\AIOS\tachyonic\archive\runtime\README_archived_20251025_213000.md",
        r"c:\dev\AIOS\tachyonic\archive\runtime\README.md"
    ]

    print("\n=== STORING FILES ===")
    for file_path in files_to_archive:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                print(f"\nProcessing: {file_path}")
                store_file_in_database(db_path, file_path, content)

            except Exception as e:
                print(f"Error processing {file_path}: {e}")
        else:
            print(f"File not found: {file_path}")

if __name__ == "__main__":
    main()