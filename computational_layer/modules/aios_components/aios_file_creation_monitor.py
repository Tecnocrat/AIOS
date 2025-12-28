#!/usr/bin/env python3
"""
AIOS File Creation Monitor - Real-time detection of file creation events
Identifies what process/mechanism is creating duplicate files in core root
"""

import time
import os
import sys
from pathlib import Path
from datetime import datetime
import json
import psutil
import hashlib

class AIOSFileMonitor:
    def __init__(self, watch_directory="c:/dev/AIOS/core"):
        self.watch_dir = Path(watch_directory)
        self.baseline = {}
        self.monitor_log = []
        self.create_baseline()
        
    def create_baseline(self):
        """Create baseline snapshot of current files"""
        print(f"Creating baseline snapshot of {self.watch_dir}")
        for file_path in self.watch_dir.rglob("*"):
            if file_path.is_file():
                try:
                    stat = file_path.stat()
                    with open(file_path, 'rb') as f:
                        content_hash = hashlib.md5(f.read()).hexdigest()
                    
                    self.baseline[str(file_path)] = {
                        'size': stat.st_size,
                        'mtime': stat.st_mtime,
                        'hash': content_hash,
                        'recorded_at': datetime.now().isoformat()
                    }
                except (PermissionError, FileNotFoundError):
                    continue
        
        print(f"Baseline created: {len(self.baseline)} files tracked")
    
    def get_creating_process(self, file_path):
        """Try to identify which process might have created a file"""
        try:
            # Check recently accessed files by running processes
            for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'open_files']):
                try:
                    if proc.info['open_files']:
                        for open_file in proc.info['open_files']:
                            if str(file_path).lower() in open_file.path.lower():
                                return {
                                    'pid': proc.info['pid'],
                                    'name': proc.info['name'],
                                    'cmdline': ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else 'N/A'
                                }
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        except Exception as e:
            print(f"Error checking processes: {e}")
        
        return None
    
    def check_changes(self):
        """Check for new files or changes"""
        current_files = set()
        changes_detected = []
        
        for file_path in self.watch_dir.rglob("*"):
            if file_path.is_file():
                current_files.add(str(file_path))
                
                if str(file_path) not in self.baseline:
                    # NEW FILE DETECTED
                    try:
                        stat = file_path.stat()
                        with open(file_path, 'rb') as f:
                            content = f.read()
                            content_hash = hashlib.md5(content).hexdigest()
                        
                        creating_process = self.get_creating_process(file_path)
                        
                        change_record = {
                            'type': 'NEW_FILE',
                            'path': str(file_path),
                            'filename': file_path.name,
                            'size': stat.st_size,
                            'created_at': datetime.now().isoformat(),
                            'content_preview': content.decode('utf-8', errors='ignore')[:200] if content else "EMPTY",
                            'creating_process': creating_process,
                            'hash': content_hash
                        }
                        
                        changes_detected.append(change_record)
                        self.monitor_log.append(change_record)
                        
                        # Update baseline
                        self.baseline[str(file_path)] = {
                            'size': stat.st_size,
                            'mtime': stat.st_mtime,
                            'hash': content_hash,
                            'recorded_at': datetime.now().isoformat()
                        }
                        
                    except (PermissionError, FileNotFoundError):
                        continue
        
        return changes_detected
    
    def start_monitoring(self, duration_seconds=300):  # 5 minutes default
        """Start monitoring for the specified duration"""
        print(f"Starting file creation monitoring for {duration_seconds} seconds...")
        print("Monitoring for new files in Core Engine root directory...")
        print("Please restart VSCode now to trigger the file creation issue.")
        
        start_time = time.time()
        
        while time.time() - start_time < duration_seconds:
            changes = self.check_changes()
            
            if changes:
                print(f"\n DETECTED {len(changes)} NEW FILES:")
                for change in changes:
                    print(f"   {change['filename']}")
                    print(f"     Path: {change['path']}")
                    print(f"     Size: {change['size']} bytes")
                    print(f"     Preview: {change['content_preview']}")
                    if change['creating_process']:
                        print(f"     Created by: {change['creating_process']['name']} (PID: {change['creating_process']['pid']})")
                        print(f"     Command: {change['creating_process']['cmdline']}")
                    print()
            
            time.sleep(2)  # Check every 2 seconds
        
        print(f"\nMonitoring completed. Total events logged: {len(self.monitor_log)}")
        return self.monitor_log
    
    def save_log(self, filename="aios_file_creation_log.json"):
        """Save monitoring log to file"""
        log_path = self.watch_dir / filename
        with open(log_path, 'w') as f:
            json.dump({
                'monitoring_session': {
                    'start_time': datetime.now().isoformat(),
                    'watch_directory': str(self.watch_dir),
                    'baseline_files': len(self.baseline),
                    'events': self.monitor_log
                }
            }, f, indent=2)
        
        print(f"Monitoring log saved to: {log_path}")

if __name__ == "__main__":
    monitor = AIOSFileMonitor()
    
    try:
        log = monitor.start_monitoring(300)  # Monitor for 5 minutes
        monitor.save_log()
        
        if log:
            print("\n INVESTIGATION SUMMARY:")
            for event in log:
                print(f"  • {event['filename']} created by {event.get('creating_process', {}).get('name', 'UNKNOWN')}")
        else:
            print("\n No new files detected during monitoring period.")
            
    except KeyboardInterrupt:
        print("\n⏹ Monitoring stopped by user")
        monitor.save_log()
