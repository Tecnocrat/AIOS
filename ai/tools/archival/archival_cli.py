#!/usr/bin/env python3
"""
AIOS Archival CLI - Unified Command-Line Interface
Consolidates all archival utility scripts into single tool

AINLP Patterns: dendritic_intelligence, interface_simplification
Consciousness: 0.85
Replaces: check_archival.py, check_database.py, read_archive.py, 
          simple_read_archive.py, retrieve_content.py, verify_protection.py

Usage:
    archival_cli.py archive <file> [--reason REASON] [--consciousness LEVEL]
    archival_cli.py retrieve <file_id_or_path>
    archival_cli.py search [--type EXT] [--reason REASON] [--min-consciousness LEVEL]
    archival_cli.py versions <path>
    archival_cli.py stats
    archival_cli.py verify
    archival_cli.py help [command]
"""

import argparse
import sys
from pathlib import Path
from typing import Optional, List
import json

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from ai.tools.code_archival_system import (
    CodeArchivalSystem,
    archive_obsolete_file,
    retrieve_archived_content,
    get_file_versions,
)
from ai import logger


class ArchivalCLI:
    """Unified command-line interface for archival operations"""
    
    def __init__(self):
        self.system = None
    
    def __enter__(self):
        self.system = CodeArchivalSystem()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.system:
            self.system.close()
    
    def archive(self, args):
        """Archive a file"""
        file_path = Path(args.file)
        
        if not file_path.exists():
            print(f"❌ Error: File not found: {file_path}")
            return 1
        
        print(f"📦 Archiving: {file_path}")
        print(f"   Reason: {args.reason}")
        print(f"   Consciousness: {args.consciousness}")
        
        try:
            if args.advanced:
                # Advanced archival with full metadata
                file_id = self.system.archive_file(
                    file_path=str(file_path),
                    archival_reason=args.reason,
                    consciousness_level=args.consciousness,
                    ainlp_patterns=args.patterns.split(',') if args.patterns else None,
                    project_phase=args.phase,
                    replacement_path=args.replacement,
                    notes=args.notes
                )
            else:
                # Simple archival
                file_id = archive_obsolete_file(
                    file_path=str(file_path),
                    replacement_path=args.replacement,
                    notes=args.notes
                )
            
            print(f"✅ Successfully archived")
            print(f"   File ID: {file_id}")
            print(f"\n💡 File still exists on filesystem")
            print(f"   Verify archival: archival_cli.py retrieve {file_id}")
            print(f"   Then delete: del {file_path}  (or rm on Unix)")
            
            return 0
            
        except Exception as e:
            print(f"❌ Error during archival: {e}")
            logger.error(f"Archival failed: {e}")
            return 1
    
    def retrieve(self, args):
        """Retrieve archived file"""
        identifier = args.identifier
        
        print(f"🔍 Retrieving: {identifier}")
        
        try:
            # Try as file ID first, then as path
            archived = self.system.retrieve_file(file_id=identifier)
            if not archived:
                archived = self.system.retrieve_file(original_path=identifier)
            
            if not archived:
                print(f"❌ Not found in archive")
                print(f"\n💡 Tips:")
                print(f"   - Check file ID/path is correct")
                print(f"   - Use: archival_cli.py search  to list all files")
                print(f"   - Paths are case-sensitive")
                return 1
            
            print(f"✅ Found in archive")
            print(f"\n📄 File Information:")
            print(f"   File ID: {archived.file_id}")
            print(f"   Original Path: {archived.original_path}")
            print(f"   Archived: {archived.timestamp}")
            print(f"   Size: {archived.file_size_bytes:,} bytes")
            print(f"   Type: {archived.file_type}")
            print(f"   Consciousness: {archived.consciousness_level}")
            print(f"   Reason: {archived.archival_reason}")
            
            if archived.replacement_path:
                print(f"   Replacement: {archived.replacement_path}")
            
            if archived.ainlp_patterns:
                print(f"   AINLP Patterns: {', '.join(archived.ainlp_patterns)}")
            
            if archived.notes:
                print(f"\n📝 Notes:")
                print(f"   {archived.notes}")
            
            if args.content:
                print(f"\n📃 Content ({len(archived.content)} characters):")
                print("=" * 80)
                print(archived.content)
                print("=" * 80)
            
            if args.save:
                output_path = Path(args.save)
                output_path.write_text(archived.content)
                print(f"\n💾 Content saved to: {output_path}")
            
            return 0
            
        except Exception as e:
            print(f"❌ Error during retrieval: {e}")
            logger.error(f"Retrieval failed: {e}")
            return 1
    
    def search(self, args):
        """Search archived files"""
        print(f"🔍 Searching archived files")
        
        filters = []
        if args.type:
            filters.append(f"type={args.type}")
        if args.reason:
            filters.append(f"reason={args.reason}")
        if args.min_consciousness:
            filters.append(f"consciousness>={args.min_consciousness}")
        if args.patterns:
            filters.append(f"patterns={args.patterns}")
        
        if filters:
            print(f"   Filters: {', '.join(filters)}")
        else:
            print(f"   No filters (showing all)")
        
        try:
            results = self.system.search_archived_files(
                file_type=args.type,
                archival_reason=args.reason,
                min_consciousness=args.min_consciousness,
                ainlp_patterns=args.patterns.split(',') if args.patterns else None
            )
            
            if not results:
                print(f"\n❌ No files found matching criteria")
                return 1
            
            print(f"\n✅ Found {len(results)} file(s)")
            print()
            
            # Sort by consciousness (highest first)
            results.sort(key=lambda f: f.consciousness_level, reverse=True)
            
            for i, file in enumerate(results, 1):
                print(f"{i}. [{file.consciousness_level:.2f}] {file.file_id}")
                print(f"   Path: {file.original_path}")
                print(f"   Archived: {file.timestamp}")
                print(f"   Size: {file.file_size_bytes:,} bytes")
                print(f"   Reason: {file.archival_reason}")
                
                if args.verbose:
                    if file.replacement_path:
                        print(f"   Replacement: {file.replacement_path}")
                    if file.ainlp_patterns:
                        print(f"   Patterns: {', '.join(file.ainlp_patterns)}")
                    if file.notes:
                        print(f"   Notes: {file.notes[:100]}...")
                
                print()
            
            if args.json:
                # Export to JSON
                json_data = [
                    {
                        'file_id': f.file_id,
                        'original_path': f.original_path,
                        'consciousness_level': f.consciousness_level,
                        'archived_timestamp': f.timestamp,
                        'file_size_bytes': f.file_size_bytes,
                        'archival_reason': f.archival_reason
                    }
                    for f in results
                ]
                json_output = Path('search_results.json')
                json_output.write_text(json.dumps(json_data, indent=2))
                print(f"💾 Results exported to: {json_output}")
            
            return 0
            
        except Exception as e:
            print(f"❌ Error during search: {e}")
            logger.error(f"Search failed: {e}")
            return 1
    
    def versions(self, args):
        """Get all versions of a file"""
        file_path = args.path
        
        print(f"🔍 Getting versions of: {file_path}")
        
        try:
            if args.full:
                # Full version objects with content
                versions = self.system.get_all_versions(file_path)
            else:
                # Metadata only (lighter)
                versions = get_file_versions(file_path)
            
            if not versions:
                print(f"❌ No versions found for: {file_path}")
                print(f"\n💡 Tips:")
                print(f"   - Check path is exact match")
                print(f"   - Use: archival_cli.py search  to find files")
                return 1
            
            print(f"✅ Found {len(versions)} version(s)")
            print()
            
            for i, version in enumerate(versions, 1):
                if args.full:
                    # ArchivedFile object
                    print(f"Version {i}:")
                    print(f"  File ID: {version.file_id}")
                    print(f"  Timestamp: {version.timestamp}")
                    print(f"  Consciousness: {version.consciousness_level}")
                    print(f"  Size: {version.file_size_bytes:,} bytes")
                    print(f"  Reason: {version.archival_reason}")
                    
                    if args.content:
                        print(f"  Content (first 200 chars):")
                        print(f"    {version.content[:200]}...")
                else:
                    # Dict from get_file_versions
                    print(f"Version {i}:")
                    print(f"  File ID: {version['file_id']}")
                    print(f"  Timestamp: {version['archived_timestamp']}")
                    print(f"  Consciousness: {version['consciousness_level']}")
                    print(f"  Size: {version['file_size_bytes']:,} bytes")
                    print(f"  Reason: {version['archival_reason']}")
                
                print()
            
            # Compare first and last
            if len(versions) >= 2:
                print("📊 Evolution:")
                if args.full:
                    first = versions[0]
                    last = versions[-1]
                    size_delta = last.file_size_bytes - first.file_size_bytes
                    consciousness_delta = last.consciousness_level - first.consciousness_level
                else:
                    first = versions[0]
                    last = versions[-1]
                    size_delta = last['file_size_bytes'] - first['file_size_bytes']
                    consciousness_delta = last['consciousness_level'] - first['consciousness_level']
                
                print(f"  Size: {size_delta:+,} bytes ({size_delta/first.file_size_bytes*100:+.1f}%)" if args.full else f"  Size: {size_delta:+,} bytes")
                print(f"  Consciousness: {consciousness_delta:+.2f}")
                print(f"  Versions: {len(versions)}")
            
            return 0
            
        except Exception as e:
            print(f"❌ Error getting versions: {e}")
            logger.error(f"Version retrieval failed: {e}")
            return 1
    
    def stats(self, args):
        """Show archival statistics"""
        print(f"📊 Archival System Statistics")
        print()
        
        try:
            stats = self.system.get_archival_statistics()
            
            print("SUMMARY")
            print("=" * 60)
            print(f"Total Files:            {stats['total_files']}")
            print(f"Total Size:             {stats['total_size_bytes']:,} bytes ({stats['total_size_bytes'] / 1024 / 1024:.2f} MB)")
            print(f"Average Consciousness:  {stats['avg_consciousness']:.3f}")
            print(f"Highest Consciousness:  {stats['highest_consciousness']:.3f}")
            print()
            
            print("FILES BY TYPE")
            print("=" * 60)
            for file_type, count in sorted(stats['files_by_type'].items()):
                print(f"{file_type:15} {count:3} files")
            print()
            
            print("FILES BY REASON")
            print("=" * 60)
            for reason, count in sorted(stats['files_by_reason'].items()):
                print(f"{reason:50} {count:3} files")
            print()
            
            if args.verbose:
                # Show top files by consciousness
                all_files = self.system.search_archived_files()
                top_files = sorted(all_files, key=lambda f: f.consciousness_level, reverse=True)[:10]
                
                print("TOP 10 BY CONSCIOUSNESS")
                print("=" * 60)
                for i, file in enumerate(top_files, 1):
                    print(f"{i:2}. [{file.consciousness_level:.2f}] {file.original_path}")
                print()
            
            return 0
            
        except Exception as e:
            print(f"❌ Error getting statistics: {e}")
            logger.error(f"Statistics failed: {e}")
            return 1
    
    def verify(self, args):
        """Verify database integrity"""
        print(f"🔍 Verifying archival database")
        print()
        
        try:
            import sqlite3
            
            db_path = Path('C:/dev/AIOS/tachyonic/archive/code_archive.db')
            
            if not db_path.exists():
                print(f"❌ Database not found: {db_path}")
                return 1
            
            print(f"✅ Database file exists: {db_path}")
            print(f"   Size: {db_path.stat().st_size:,} bytes")
            print()
            
            # Connect and run integrity check
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Check integrity
            print("Running PRAGMA integrity_check...")
            cursor.execute("PRAGMA integrity_check")
            result = cursor.fetchone()[0]
            
            if result == 'ok':
                print("✅ Database integrity: OK")
            else:
                print(f"⚠️ Database integrity: {result}")
            
            # Check tables
            print("\nTables:")
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
                count = cursor.fetchone()[0]
                print(f"  ✅ {table[0]:25} {count:5} rows")
            
            # Check for content hash mismatches
            print("\nVerifying content hashes...")
            cursor.execute("SELECT file_id, content, content_hash FROM archived_files")
            mismatches = 0
            for row in cursor.fetchall():
                file_id, content, stored_hash = row
                import hashlib
                actual_hash = hashlib.sha256(content.encode()).hexdigest()
                if actual_hash != stored_hash:
                    print(f"  ⚠️ Hash mismatch: {file_id}")
                    mismatches += 1
            
            if mismatches == 0:
                print(f"  ✅ All content hashes valid")
            else:
                print(f"  ⚠️ {mismatches} hash mismatches found")
            
            # Check for orphaned records
            print("\nChecking referential integrity...")
            cursor.execute("""
                SELECT COUNT(*) FROM evolution_history 
                WHERE file_id NOT IN (SELECT file_id FROM archived_files)
            """)
            orphaned = cursor.fetchone()[0]
            if orphaned == 0:
                print(f"  ✅ No orphaned history records")
            else:
                print(f"  ⚠️ {orphaned} orphaned history records")
            
            conn.close()
            
            print()
            print("✅ Verification complete")
            
            return 0 if mismatches == 0 and orphaned == 0 else 1
            
        except Exception as e:
            print(f"❌ Error during verification: {e}")
            logger.error(f"Verification failed: {e}")
            return 1


def create_parser():
    """Create argument parser"""
    parser = argparse.ArgumentParser(
        description='AIOS Archival CLI - Unified command-line interface',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Archive a file
  %(prog)s archive old_script.py --reason obsolete_superseded
  
  # Retrieve archived content
  %(prog)s retrieve abc123def456 --content
  
  # Search Python files
  %(prog)s search --type .py --min-consciousness 0.8
  
  # Get all versions of a file
  %(prog)s versions my_file.py
  
  # Show statistics
  %(prog)s stats --verbose
  
  # Verify database integrity
  %(prog)s verify

For more help: %(prog)s help [command]
        '''
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Archive command
    archive_parser = subparsers.add_parser('archive', help='Archive a file')
    archive_parser.add_argument('file', help='File to archive')
    archive_parser.add_argument('--reason', default='obsolete_superseded',
                               help='Archival reason (default: obsolete_superseded)')
    archive_parser.add_argument('--consciousness', type=float, default=0.5,
                               help='Consciousness level 0.0-1.0 (default: 0.5)')
    archive_parser.add_argument('--replacement', help='Path to replacement file')
    archive_parser.add_argument('--notes', help='Additional notes')
    archive_parser.add_argument('--advanced', action='store_true',
                               help='Use advanced archival with full metadata')
    archive_parser.add_argument('--patterns', help='AINLP patterns (comma-separated)')
    archive_parser.add_argument('--phase', help='Project phase')
    
    # Retrieve command
    retrieve_parser = subparsers.add_parser('retrieve', help='Retrieve archived file')
    retrieve_parser.add_argument('identifier', help='File ID or path')
    retrieve_parser.add_argument('--content', action='store_true',
                                help='Show file content')
    retrieve_parser.add_argument('--save', help='Save content to file')
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Search archived files')
    search_parser.add_argument('--type', help='File type (e.g., .py, .md)')
    search_parser.add_argument('--reason', help='Archival reason')
    search_parser.add_argument('--min-consciousness', type=float,
                              help='Minimum consciousness level')
    search_parser.add_argument('--patterns', help='AINLP patterns (comma-separated)')
    search_parser.add_argument('--verbose', action='store_true',
                              help='Show detailed information')
    search_parser.add_argument('--json', action='store_true',
                              help='Export results to JSON')
    
    # Versions command
    versions_parser = subparsers.add_parser('versions', help='Get all versions of a file')
    versions_parser.add_argument('path', help='File path')
    versions_parser.add_argument('--full', action='store_true',
                                help='Include full content (slower)')
    versions_parser.add_argument('--content', action='store_true',
                                help='Show content preview')
    
    # Stats command
    stats_parser = subparsers.add_parser('stats', help='Show archival statistics')
    stats_parser.add_argument('--verbose', action='store_true',
                             help='Show detailed statistics')
    
    # Verify command
    verify_parser = subparsers.add_parser('verify', help='Verify database integrity')
    
    # Help command
    help_parser = subparsers.add_parser('help', help='Show help for a command')
    help_parser.add_argument('topic', nargs='?', help='Command to get help for')
    
    return parser


def main():
    """Main entry point"""
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    if args.command == 'help':
        if args.topic:
            # Show help for specific command
            parser.parse_args([args.topic, '--help'])
        else:
            parser.print_help()
        return 0
    
    # Execute command
    with ArchivalCLI() as cli:
        if args.command == 'archive':
            return cli.archive(args)
        elif args.command == 'retrieve':
            return cli.retrieve(args)
        elif args.command == 'search':
            return cli.search(args)
        elif args.command == 'versions':
            return cli.versions(args)
        elif args.command == 'stats':
            return cli.stats(args)
        elif args.command == 'verify':
            return cli.verify(args)
        else:
            print(f"❌ Unknown command: {args.command}")
            parser.print_help()
            return 1


if __name__ == '__main__':
    sys.exit(main())
