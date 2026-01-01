#!/usr/bin/env python3
"""
AIOS GitHooks Emoji Integration
===============================
Location: ai/laboratory/scripts/githooks_emoji_integration.py
Purpose: Integration between emoji detector and GitHooks system
Architecture: LABORATORY supercell -> CYTOPLASM orchestration

This script provides the bridge between the emoji detector utility
and the AIOS GitHooks governance system for automated cleanup.
"""

import os
import sys
from pathlib import Path

# Add AIOS paths
sys.path.append(str(Path(__file__).parent))
sys.path.append(str(Path(__file__).parent.parent.parent))

from emoji_detector import EmojiDetector

def scan_githooks_readme() -> list:
    """Scan the GitHooks README for emoji issues"""
    workspace_root = Path(__file__).parent.parent.parent.parent
    readme_path = workspace_root / '.githooks' / 'README.md'
    
    if not readme_path.exists():
        print(f"Warning: README not found at {readme_path}")
        return []
    
    detector = EmojiDetector(workspace_root)
    matches = detector.scan_file(readme_path)
    
    return matches

def generate_cleanup_suggestions(matches: list) -> list:
    """Generate specific cleanup suggestions for found emojis"""
    suggestions = []
    
    emoji_replacements = {
        '': '[COMPLETED]',
        '': '[FAILED]',
        '': 'TARGET:',
        '': 'SUPERCELL:',
        '': 'LAUNCH:',
        '': 'FOLDER:',
        '': 'METRICS:',
        '': 'ANALYSIS:',
        '': 'PROCESS:',
        '': 'CORE:',
        '': 'RUNTIME:',
        '': 'ARCHIVE:',
        '': 'AI:',
        '': 'INTERFACE:',
        '': 'DOCS:'
    }
    
    for match in matches:
        replacement = emoji_replacements.get(match.emoji, f'[{match.emoji}]')
        suggestions.append({
            'file': match.file_path,
            'line': match.line_number,
            'emoji': match.emoji,
            'replacement': replacement,
            'context': match.context
        })
    
    return suggestions

def print_cleanup_report(matches: list, suggestions: list):
    """Print a comprehensive cleanup report"""
    print("\nAIOS GITHOOKS EMOJI CLEANUP REPORT")
    print("===================================")
    print(f"Total emojis found: {len(matches)}")
    print()
    
    if not matches:
        print(" No emoji characters detected!")
        return
    
    print("DETECTED EMOJIS:")
    print("----------------")
    for i, match in enumerate(matches, 1):
        rel_path = os.path.relpath(match.file_path)
        print(f"{i}. Line {match.line_number}: '{match.emoji}'")
        print(f"   File: {rel_path}")
        print(f"   Context: {match.context.strip()}")
        print()
    
    print("CLEANUP SUGGESTIONS:")
    print("-------------------")
    for suggestion in suggestions:
        rel_path = os.path.relpath(suggestion['file'])
        print(f"Line {suggestion['line']}: Replace '{suggestion['emoji']}' with '{suggestion['replacement']}'")
        print(f"  File: {rel_path}")
        print()

def main():
    """Main execution"""
    print("AIOS GitHooks Emoji Detection Integration")
    print("=========================================")
    
    # Scan GitHooks README
    matches = scan_githooks_readme()
    
    # Generate suggestions
    suggestions = generate_cleanup_suggestions(matches)
    
    # Print report
    print_cleanup_report(matches, suggestions)
    
    # Return exit code based on findings
    return len(matches)

if __name__ == '__main__':
    sys.exit(main())