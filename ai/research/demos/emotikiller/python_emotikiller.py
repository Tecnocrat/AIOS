#!/usr/bin/env python3
"""
AIOS Emoticon Destroyer - Python Implementation
STRICT NO EMOTICON POLICY ENFORCED
Ultra-robust emoticon detection and removal system
"""

import os
import re
import sys
import time
import argparse
import logging
import shutil
from pathlib import Path
from typing import List, Set, Tuple, Optional
import unicodedata

class EmoticonDestroyer:
    """High-performance emoticon detection and removal engine"""
    
    def __init__(self, create_backup: bool = True, verbose: bool = False):
        self.stats = {
            'files_processed': 0,
            'emoticons_destroyed': 0,
            'backup_files_created': 0,
            'start_time': time.time()
        }
        
        self.create_backup = create_backup
        self.verbose = verbose
        
        # Configure logging
        log_level = logging.DEBUG if verbose else logging.INFO
        logging.basicConfig(
            level=log_level,
            format='[%(asctime)s] [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        self.logger = logging.getLogger(__name__)
        
        # Configuration
        self.config = {
            'target_extensions': {
                '.md', '.txt', '.py', '.cpp', '.c', '.h', '.hpp', 
                '.cs', '.js', '.ts', '.json', '.yaml', '.yml',
                '.html', '.css', '.xml', '.rst', '.ini', '.cfg'
            },
            'skip_directories': {
                'node_modules', '.git', 'venv', 'env', '__pycache__',
                'aios_env', '.vscode', 'bin', 'obj', 'build', '.vs',
                '.pytest_cache', 'dist', '.egg-info'
            },
            'max_file_size': 50 * 1024 * 1024  # 50MB
        }
        
        # Comprehensive emoticon patterns
        self.emoticon_patterns = self._build_emoticon_patterns()
        
        # Compile regex patterns for performance
        self.compiled_patterns = [
            re.compile(pattern, re.UNICODE | re.IGNORECASE)
            for pattern in self.emoticon_patterns
        ]
    
    def _build_emoticon_patterns(self) -> List[str]:
        """Build comprehensive emoticon detection patterns"""
        patterns = [
            # Unicode emoticon blocks
            r'[\U0001F600-\U0001F64F]',  # Emoticons
            r'[\U0001F300-\U0001F5FF]',  # Misc Symbols and Pictographs
            r'[\U0001F680-\U0001F6FF]',  # Transport and Map
            r'[\U0001F1E0-\U0001F1FF]',  # Regional Indicator Symbols (Flags)
            r'[\U0001F900-\U0001F9FF]',  # Supplemental Symbols and Pictographs
            r'[\U0001FA70-\U0001FAFF]',  # Symbols and Pictographs Extended-A
            r'[\U00002600-\U000026FF]',  # Miscellaneous Symbols
            r'[\U00002700-\U000027BF]',  # Dingbats
            r'[\U0000FE00-\U0000FE0F]',  # Variation Selectors
            r'[\U0001F000-\U0001F02F]',  # Mahjong Tiles
            r'[\U0001F0A0-\U0001F0FF]',  # Playing Cards
            
            # ASCII emoticons (comprehensive list)
            r'[:;=8xX][\-o\*\']?[\)\]\(\[dDpP/\\oO\{\}]',  # Basic emoticons
            r'[\)\]\(\[][:;=8xX][\-o\*\']?',               # Reverse emoticons
            r'[oO][\-_]?[oO]',                              # Surprised faces
            r'[xX][\-_]?[xX]',                              # Dead/dizzy faces
            r'[>][\.\-]?[<]',                               # Fish emoticon
            r'[<][\-_]?[3]',                                # Heart emoticon
            r'[\-_][\.\-_]+[\-_]',                          # Line faces
            r'[\\][oO][/]',                                 # Shrug emoticon
            r'[oO][_][oO]',                                 # Confused face
            r'[uU][_][uU]',                                 # Crying face
            r'[nN][_][nN]',                                 # Annoyed face
            r'[@][\-_]?[@]',                                # Dizzy eyes
            r'[*][\-_]?[*]',                                # Star eyes
            r'[$][\-_]?[$]',                                # Money eyes
            r'[%][\-_]?[%]',                                # Confused percentage
            r'[#][\-_]?[#]',                                # Hashtag eyes
            r'[&][\-_]?[&]',                                # Ampersand eyes
            
            # Text-based emoticons
            r'\b[xX][dD]\b',                                # XD, xD
            r'\b[lL][oO][lL]\b',                            # LOL
            r'\b[lL][mM][aA][oO]\b',                        # LMAO
            r'\b[rR][oO][fF][lL]\b',                        # ROFL
            r'\b[lL][mM][fF][aA][oO]\b',                    # LMFAO
            r'\b[hH][aA][hH][aA][\+hH]*\b',                 # HAHA, HAHAHA+
            r'\b[hH][eE][hH][eE][\+hH]*\b',                 # HEHE, HEHEHE+
            r'\b[hH][iI][hH][iI][\+hH]*\b',                 # HIHI, HIHIHI+
            r'\b[oO][mM][gG]\b',                            # OMG
            r'\b[wW][tT][fF]\b',                            # WTF
            r'\b[fF][mM][lL]\b',                            # FML
            r'\b[bB][rR][bB]\b',                            # BRB
            r'\b[tT][tT][yY][lL]\b',                        # TTYL
            r'\b[gG][tT][gG]\b',                            # GTG
            r'\b[aA][fF][kK]\b',                            # AFK
            r'\b[bB][bB][lL]\b',                            # BBL
            
            # Kaomoji (Japanese emoticons) - common patterns
            r'[\(\uff08][\^><\-~\*\+\=\.][\w\s\-_\.\*\+\=\^><~]*[\)\uff09]',
            r'[\(\uff08][\s]*[><\^v\-\*\+\=\.][_\-]*[><\^v\-\*\+\=\.]*[\s]*[\)\uff09]',
            r'[<>\-\*\+\=\.]{2,}',
            r'[\(\uff08][><\^v\-\*\+\=\.\s]*[\)\uff09]',
            
            # Emoticon patterns with text formatting
            r'\*[^*]+\*[^*]*[:;][^*]*\*[^*]+\*',           # Bold emoticons
            r'_[^_]+_[^_]*[:;][^_]*_[^_]+_',               # Italic emoticons
            r'`[^`]+`[^`]*[:;][^`]*`[^`]+`',               # Code emoticons
        ]
        
        return patterns
    
    def should_skip_path(self, path: Path) -> bool:
        """Check if path should be skipped"""
        path_str = str(path).lower()
        return any(skip_dir in path_str for skip_dir in self.config['skip_directories'])
    
    def has_target_extension(self, file_path: Path) -> bool:
        """Check if file has target extension"""
        return file_path.suffix.lower() in self.config['target_extensions']
    
    def create_backup_file(self, file_path: Path) -> bool:
        """Create backup of file before modification"""
        try:
            backup_path = file_path.with_suffix(file_path.suffix + '.backup')
            shutil.copy2(file_path, backup_path)
            self.stats['backup_files_created'] += 1
            self.logger.info(f"Backup created: {backup_path}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to create backup for {file_path}: {e}")
            return False
    
    def count_emoticons(self, content: str) -> int:
        """Count emoticons in content"""
        total_count = 0
        for pattern in self.compiled_patterns:
            matches = pattern.findall(content)
            total_count += len(matches)
        return total_count
    
    def remove_emoticons(self, content: str) -> str:
        """Remove all emoticons from content"""
        cleaned_content = content
        
        for pattern in self.compiled_patterns:
            cleaned_content = pattern.sub('', cleaned_content)
        
        # Additional cleanup for leftover whitespace
        cleaned_content = re.sub(r'\s{3,}', '  ', cleaned_content)  # Reduce multiple spaces
        cleaned_content = re.sub(r'\n{3,}', '\n\n', cleaned_content)  # Reduce multiple newlines
        
        return cleaned_content
    
    def detect_encoding(self, file_path: Path) -> str:
        """Detect file encoding"""
        try:
            import chardet
            with open(file_path, 'rb') as f:
                raw_data = f.read(10000)  # Read first 10KB
                result = chardet.detect(raw_data)
                return result.get('encoding', 'utf-8') or 'utf-8'
        except ImportError:
            # Fallback if chardet not available
            return 'utf-8'
        except Exception:
            return 'utf-8'
    
    def process_file(self, file_path: Path) -> bool:
        """Process single file for emoticon removal"""
        self.logger.info(f"Processing file: {file_path}")
        
        try:
            # Check file size
            if file_path.stat().st_size > self.config['max_file_size']:
                self.logger.warning(f"Skipping large file: {file_path} (Size: {file_path.stat().st_size} bytes)")
                return True
            
            # Detect encoding
            encoding = self.detect_encoding(file_path)
            
            # Read file content
            try:
                with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
                    content = f.read()
            except UnicodeDecodeError:
                # Fallback to utf-8 with error handling
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
            
            if not content:
                self.logger.warning(f"Empty file skipped: {file_path}")
                return True
            
            # Count emoticons
            initial_count = self.count_emoticons(content)
            if initial_count == 0:
                self.logger.info(f"No emoticons found in: {file_path}")
                return True
            
            # Create backup if requested
            if self.create_backup and not self.create_backup_file(file_path):
                return False
            
            # Remove emoticons
            cleaned_content = self.remove_emoticons(content)
            
            # Write cleaned content back
            with open(file_path, 'w', encoding=encoding, errors='ignore') as f:
                f.write(cleaned_content)
            
            # Update statistics
            self.stats['emoticons_destroyed'] += initial_count
            self.stats['files_processed'] += 1
            
            self.logger.info(f"SUCCESS: Removed {initial_count} emoticons from: {file_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to process file {file_path}: {e}")
            return False
    
    def process_directory(self, directory_path: Path) -> bool:
        """Process directory recursively"""
        self.logger.info(f"Scanning directory: {directory_path}")
        
        try:
            # Collect all target files
            target_files = []
            for file_path in directory_path.rglob('*'):
                if (file_path.is_file() and 
                    not self.should_skip_path(file_path) and 
                    self.has_target_extension(file_path)):
                    target_files.append(file_path)
            
            total_files = len(target_files)
            self.logger.info(f"Found {total_files} files to process")
            
            # Process files with progress indication
            for i, file_path in enumerate(target_files, 1):
                percent_complete = (i / total_files) * 100
                self.logger.info(f"Progress: {i}/{total_files} ({percent_complete:.1f}%)")
                
                self.process_file(file_path)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to process directory {directory_path}: {e}")
            return False
    
    def print_statistics(self):
        """Print processing statistics"""
        end_time = time.time()
        execution_time = end_time - self.stats['start_time']
        
        print("\n" + "="*50)
        print("[STATISTICS]")
        print("="*50)
        print(f"Files processed: {self.stats['files_processed']}")
        print(f"Emoticons destroyed: {self.stats['emoticons_destroyed']}")
        print(f"Backup files created: {self.stats['backup_files_created']}")
        print(f"Execution time: {execution_time:.2f} seconds")
        
        if self.stats['emoticons_destroyed'] > 0 and execution_time > 0:
            rate = self.stats['emoticons_destroyed'] / execution_time
            print(f"Destruction rate: {rate:.2f} emoticons/second")
        
        print("="*50)

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="AIOS Emoticon Destroyer - Python Implementation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python python_emotikiller.py /path/to/file.txt
  python python_emotikiller.py /path/to/directory
  python python_emotikiller.py /path/to/project --no-backup --verbose
        """
    )
    
    parser.add_argument(
        'target_path',
        help='Path to file or directory to process'
    )
    
    parser.add_argument(
        '--no-backup',
        action='store_true',
        help='Do not create backup files'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    print("[AIOS] Emoticon Destroyer Python Engine")
    print("[POLICY] No emoticons allowed in codebase")
    print()
    
    # Validate target path
    target_path = Path(args.target_path)
    if not target_path.exists():
        print(f"[ERROR] Invalid path: {target_path}")
        sys.exit(1)
    
    # Initialize destroyer
    destroyer = EmoticonDestroyer(
        create_backup=not args.no_backup,
        verbose=args.verbose
    )
    
    # Process target
    success = False
    if target_path.is_dir():
        success = destroyer.process_directory(target_path)
    elif target_path.is_file():
        if destroyer.has_target_extension(target_path):
            success = destroyer.process_file(target_path)
        else:
            print(f"[WARNING] File type not supported: {target_path}")
            success = True
    else:
        print(f"[ERROR] Invalid path type: {target_path}")
        sys.exit(1)
    
    # Print results
    destroyer.print_statistics()
    
    if success:
        print("[SUCCESS] Emoticon destruction completed successfully")
        sys.exit(0)
    else:
        print("[ERROR] Emoticon destruction failed")
        sys.exit(1)

if __name__ == "__main__":
    main()