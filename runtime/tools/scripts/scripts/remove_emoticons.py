#!/usr/bin/env python3
"""
AIOS Emoticon Removal Tool
Systematically removes all emoticons from the codebase and enforces no-emoticon policy.
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Set, Tuple

class EmoticonRemover:
    """Tool for removing emoticons from codebase"""
    
    def __init__(self, root_path: str):
        self.root_path = Path(root_path)
        self.emoticon_patterns = [
            # Common emoji categories
            r'', r'', r'', r'', r'', r'', r'', r'', r'', r'',
            r'', r'', r'', r'', r'', r'', r'', r'', r'', r'',
            r'', r'', r'', r'', r'', r'', r'', r'', r'', r'',
            r'', r'', r'', r'', r'', r'', r'', r'', r'', r'',
            r'', r'', r'', r'', r'', r'', r'', r'', r'', r'',
            # Additional common emoticons
            r'', r'', r'', r'', r'', r'', r'', r'', r'', r'',
            r'', r'', r'', r'', r'', r'', r'', r'', r'', r'',
            r'', r'', r'', r'', r'', r'', r'', r'', r'', r'',
            # Generic emoji pattern (covers most Unicode emojis)
            r'[\U0001F600-\U0001F64F]',  # emoticons
            r'[\U0001F300-\U0001F5FF]',  # symbols & pictographs
            r'[\U0001F680-\U0001F6FF]',  # transport & map symbols
            r'[\U0001F1E0-\U0001F1FF]',  # flags (iOS)
            r'[\U00002702-\U000027B0]',  # dingbats
            r'[\U000024C2-\U0001F251]'   # enclosed characters
        ]
        
        self.compiled_patterns = [re.compile(pattern) for pattern in self.emoticon_patterns]
        
        # File extensions to process
        self.file_extensions = {
            '.py', '.md', '.txt', '.cs', '.cpp', '.h', '.hpp', '.js', '.ts',
            '.html', '.css', '.ps1', '.sh', '.bat', '.json', '.yaml', '.yml',
            '.xml', '.cmake', '.yml', '.ini', '.cfg'
        }
        
        # Directories to skip
        self.skip_dirs = {
            '__pycache__', '.git', 'node_modules', 'bin', 'obj', 'build',
            '.vs', '.vscode', 'packages', 'dist',
            # Virtual environments
            'venv', '.venv', 'env', 'virtualenv', 'aios_env',
            # Archive and system directories
            'tachyonic_archive', 'archive', 'temp', 'tmp',
            # Build and cache directories
            '.pytest_cache', 'site-packages', 'Scripts', 'Include', 'Lib',
            # Lock and permission protected directories
            'locks'
        }
        
        self.removed_count = 0
        self.processed_files = 0
        self.emoticon_log = []
        
    def find_emoticons_in_text(self, text: str) -> List[Tuple[str, int, int]]:
        """Find all emoticons in text and return with positions"""
        found_emoticons = []
        for pattern in self.compiled_patterns:
            for match in pattern.finditer(text):
                found_emoticons.append((match.group(), match.start(), match.end()))
        return found_emoticons
    
    def remove_emoticons_from_text(self, text: str) -> str:
        """Remove all emoticons from text"""
        for pattern in self.compiled_patterns:
            text = pattern.sub('', text)
        return text
    
    def process_file(self, file_path: Path) -> bool:
        """Process a single file to remove emoticons"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                original_content = f.read()
            
            # Find emoticons before removal
            emoticons_found = self.find_emoticons_in_text(original_content)
            
            if emoticons_found:
                # Remove emoticons
                cleaned_content = self.remove_emoticons_from_text(original_content)
                
                # Write back cleaned content
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(cleaned_content)
                
                # Log the changes
                self.emoticon_log.append({
                    'file': str(file_path),
                    'emoticons_removed': len(emoticons_found),
                    'emoticons': [em[0] for em in emoticons_found]
                })
                
                self.removed_count += len(emoticons_found)
                print(f"Cleaned {file_path}: removed {len(emoticons_found)} emoticons")
                return True
            
            return False
            
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            return False
    
    def should_process_file(self, file_path: Path) -> bool:
        """Determine if file should be processed"""
        # Check file extension
        if file_path.suffix.lower() not in self.file_extensions:
            return False
        
        # Check if in skip directory
        for part in file_path.parts:
            if part in self.skip_dirs:
                return False
        
        return True
    
    def scan_codebase(self) -> List[Path]:
        """Scan codebase for files to process"""
        files_to_process = []
        
        for root, dirs, files in os.walk(self.root_path):
            # Remove skip directories from dirs list
            dirs[:] = [d for d in dirs if d not in self.skip_dirs]
            
            for file in files:
                file_path = Path(root) / file
                if self.should_process_file(file_path):
                    files_to_process.append(file_path)
        
        return files_to_process
    
    def remove_all_emoticons(self) -> Dict:
        """Remove all emoticons from the codebase"""
        print("Starting emoticon removal process...")
        
        files_to_process = self.scan_codebase()
        print(f"Found {len(files_to_process)} files to process")
        
        files_modified = 0
        
        for file_path in files_to_process:
            self.processed_files += 1
            if self.process_file(file_path):
                files_modified += 1
        
        # Generate report
        report = {
            'timestamp': str(datetime.now()),
            'files_processed': self.processed_files,
            'files_modified': files_modified,
            'total_emoticons_removed': self.removed_count,
            'detailed_log': self.emoticon_log
        }
        
        # Save report
        report_path = self.root_path / 'emoticon_removal_report.json'
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\nEmoticon removal complete!")
        print(f"Files processed: {self.processed_files}")
        print(f"Files modified: {files_modified}")
        print(f"Total emoticons removed: {self.removed_count}")
        print(f"Report saved to: {report_path}")
        
        return report
    
    def create_enforcement_pre_commit_hook(self):
        """Create a pre-commit hook to enforce no-emoticon policy"""
        hook_content = '''#!/usr/bin/env python3
"""
Pre-commit hook to enforce no-emoticon policy in AIOS codebase
"""
import re
import sys
from pathlib import Path

def check_file_for_emoticons(file_path):
    """Check if file contains emoticons"""
    emoticon_patterns = [
        r'[\U0001F600-\U0001F64F]',  # emoticons
        r'[\U0001F300-\U0001F5FF]',  # symbols & pictographs
        r'[\U0001F680-\U0001F6FF]',  # transport & map symbols
        r'[\U0001F1E0-\U0001F1FF]',  # flags (iOS)
        r'[\U00002702-\U000027B0]',  # dingbats
        r'[\U000024C2-\U0001F251]'   # enclosed characters
    ]
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        for pattern in emoticon_patterns:
            if re.search(pattern, content):
                return True
        return False
    except:
        return False

def main():
    """Main enforcement function"""
    import subprocess
    
    # Get staged files
    result = subprocess.run(['git', 'diff', '--cached', '--name-only'], 
                          capture_output=True, text=True)
    
    if result.returncode != 0:
        print("Error getting staged files")
        return 1
    
    staged_files = result.stdout.strip().split('\\n')
    files_with_emoticons = []
    
    for file_path in staged_files:
        if file_path and Path(file_path).exists():
            if check_file_for_emoticons(file_path):
                files_with_emoticons.append(file_path)
    
    if files_with_emoticons:
        print("ERROR: Emoticons detected in staged files!")
        print("AIOS codebase has a strict no-emoticon policy.")
        print("\\nFiles with emoticons:")
        for file_path in files_with_emoticons:
            print(f"  - {file_path}")
        print("\\nPlease remove all emoticons before committing.")
        print("Use: python scripts/remove_emoticons.py")
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
'''
        
        hook_path = self.root_path / '.githooks' / 'modules' / 'nucleus' / 'no_emoticon_enforcement.py'
        hook_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(hook_path, 'w', encoding='utf-8') as f:
            f.write(hook_content)
        
        # Make executable on Unix systems
        try:
            hook_path.chmod(0o755)
        except:
            pass  # Windows doesn't support chmod the same way
        
        print(f"Created enforcement hook: {hook_path}")

def main():
    """Main execution function"""
    import sys
    
    if len(sys.argv) > 1:
        root_path = sys.argv[1]
    else:
        root_path = os.getcwd()
    
    remover = EmoticonRemover(root_path)
    
    # Remove all emoticons
    report = remover.remove_all_emoticons()
    
    # Create enforcement mechanism
    remover.create_enforcement_pre_commit_hook()
    
    print(f"\\nEmoticon removal and enforcement setup complete!")

if __name__ == '__main__':
    main()