# -*- coding: utf-8 -*-
"""
AIOS Universal Encoding Helper
Provides cross-platform Unicode support for all cellular components.
"""
import sys
import os

def setup_unicode_support():
    """Setup Unicode support for console output."""
    try:
        # Windows console encoding fix
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8')
        if hasattr(sys.stderr, 'reconfigure'):
            sys.stderr.reconfigure(encoding='utf-8')
        
        # Set environment variables for UTF-8
        os.environ['PYTHONIOENCODING'] = 'utf-8'
        
        return True
    except Exception:
        return False

def safe_print(text):
    """Print text with Unicode fallback."""
    try:
        print(text)
    except UnicodeEncodeError:
        # Replace problematic characters
        safe_text = text.encode('ascii', 'replace').decode('ascii')
        print(safe_text)

# Auto-setup when imported
setup_unicode_support()
