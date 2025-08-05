"""
AIOS VSCode Health Guard - Real-time Corruption Prevention
========================================================
Monitors and prevents VSCode workspace corruption
Blocks auto-formatters and enforces manual control
"""

import json
import time
import threading
from pathlib import Path
from typing import Dict, Any
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class WorkspaceCorruptionPreventer(FileSystemEventHandler):
    """Prevents workspace corruption by monitoring and blocking harmful changes"""

    def __init__(self, workspace_root: Path):
        self.workspace_root = Path(workspace_root)
        self.workspace_file = self.workspace_root / "AIOS.code-workspace"
        self.settings_file = self.workspace_root / ".vscode" / "settings.json"
        
        # Store safe configurations
        self.safe_workspace_settings = {
            "editor.formatOnSave": False,
            "python.formatting.provider": "none",
            "python.linting.enabled": False,
            "editor.codeActionsOnSave": {"source.fixAll": "never"}
        }
        
        self.monitoring = False
        self.last_check = time.time()

    def start_monitoring(self):
        """Start real-time workspace monitoring"""
        print("🛡️  Starting AIOS Workspace Health Guard...")
        print("🔒 Protection active against auto-formatter corruption")
        
        observer = Observer()
        observer.schedule(self, str(self.workspace_root / ".vscode"), recursive=False)
        observer.schedule(self, str(self.workspace_file.parent), recursive=False)
        
        observer.start()
        self.monitoring = True
        
        try:
            # Initial health check
            self._validate_and_fix_configurations()
            
            print("✅ Workspace Health Guard active")
            print("🔍 Monitoring for configuration corruption...")
            
            while self.monitoring:
                time.sleep(5)  # Check every 5 seconds
                self._periodic_health_check()
                
        except KeyboardInterrupt:
            print("\n🛑 Stopping Workspace Health Guard...")
        finally:
            observer.stop()
            observer.join()

    def on_modified(self, event):
        """Handle file modification events"""
        if event.is_directory:
            return
        
        file_path = Path(event.src_path)
        
        # Check if critical configuration files were modified
        if file_path.name in ["settings.json", "AIOS.code-workspace"]:
            print(f"🔔 Configuration change detected: {file_path.name}")
            time.sleep(0.5)  # Allow file to finish writing
            self._validate_and_fix_configurations()

    def _validate_and_fix_configurations(self):
        """Validate and auto-fix configuration corruption"""
        
        # Check workspace file
        if self._is_workspace_corrupted():
            print("🚨 Workspace corruption detected - auto-fixing...")
            self._fix_workspace_corruption()
        
        # Check settings file
        if self._is_settings_corrupted():
            print("🚨 Settings corruption detected - auto-fixing...")
            self._fix_settings_corruption()

    def _is_workspace_corrupted(self) -> bool:
        """Check if workspace configuration is corrupted"""
        if not self.workspace_file.exists():
            return False
        
        try:
            with open(self.workspace_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Remove comments for parsing
            import re
            content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
            workspace_config = json.loads(content)
            
            settings = workspace_config.get("settings", {})
            
            # Check for corruption patterns
            corruption_indicators = [
                settings.get("editor.formatOnSave", False) is True,
                settings.get("python.formatting.provider") != "none",
                settings.get("python.linting.enabled", False) is True,
                settings.get("editor.codeActionsOnSave", {}).get("source.fixAll") not in ["never", "explicit"]
            ]
            
            return any(corruption_indicators)
            
        except Exception:
            return True  # Parse error = corruption

    def _fix_workspace_corruption(self):
        """Fix corrupted workspace configuration"""
        try:
            # Read current workspace
            with open(self.workspace_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Find and fix problematic settings
            fixed_lines = []
            in_settings = False
            
            for line in lines:
                if '"settings"' in line:
                    in_settings = True
                elif in_settings and line.strip().startswith('}'):
                    in_settings = False
                
                # Fix specific corruption patterns
                if in_settings:
                    if '"editor.formatOnSave": true' in line:
                        line = line.replace('true', 'false')
                        print("  ✅ Fixed: formatOnSave disabled")
                    
                    if '"python.formatting.provider"' in line and '"none"' not in line:
                        line = re.sub(r'"python.formatting.provider":\s*"[^"]*"',
                                    '"python.formatting.provider": "none"', line)
                        print("  ✅ Fixed: Python formatter disabled")
                
                fixed_lines.append(line)
            
            # Write fixed configuration
            with open(self.workspace_file, 'w', encoding='utf-8') as f:
                f.writelines(fixed_lines)
            
            print("✅ Workspace configuration restored")
            
        except Exception as e:
            print(f"❌ Failed to fix workspace corruption: {e}")

    def _is_settings_corrupted(self) -> bool:
        """Check if settings configuration is corrupted"""
        if not self.settings_file.exists():
            return False
        
        try:
            with open(self.settings_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Remove comments
            import re
            content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
            settings = json.loads(content)
            
            # Check for corruption
            return (
                settings.get("python.linting.enabled", False) or
                settings.get("python.analysis.autoImportCompletions", False) or
                settings.get("omnisharp.organizeImportsOnFormat", False)
            )
            
        except Exception:
            return True

    def _fix_settings_corruption(self):
        """Fix corrupted settings configuration"""
        try:
            with open(self.settings_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Fix specific corruption patterns
            fixes = [
                (r'"python\.linting\.enabled":\s*true', '"python.linting.enabled": false'),
                (r'"python\.analysis\.autoImportCompletions":\s*true', '"python.analysis.autoImportCompletions": false'),
                (r'"omnisharp\.organizeImportsOnFormat":\s*true', '"omnisharp.organizeImportsOnFormat": false')
            ]
            
            import re
            for pattern, replacement in fixes:
                if re.search(pattern, content):
                    content = re.sub(pattern, replacement, content)
                    print(f"  ✅ Fixed corruption pattern: {pattern}")
            
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ Settings configuration restored")
            
        except Exception as e:
            print(f"❌ Failed to fix settings corruption: {e}")

    def _periodic_health_check(self):
        """Periodic background health validation"""
        current_time = time.time()
        
        # Check every 30 seconds
        if current_time - self.last_check >= 30:
            self.last_check = current_time
            self._validate_and_fix_configurations()

    def stop_monitoring(self):
        """Stop the monitoring system"""
        self.monitoring = False


def main():
    """Main health guard execution"""
    workspace_root = Path(__file__).parent.parent
    
    print("🛡️  AIOS VSCode Workspace Health Guard")
    print("=" * 50)
    print("🎯 Mission: Prevent auto-formatter corruption")
    print("🔒 Protection: Real-time configuration monitoring")
    print("⚡ Auto-fix: Immediate corruption reversal")
    print()
    
    guard = WorkspaceCorruptionPreventer(workspace_root)
    
    try:
        guard.start_monitoring()
    except KeyboardInterrupt:
        print("\n👋 Health Guard shutdown complete")
        return 0
    except Exception as e:
        print(f"❌ Health Guard failed: {e}")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
