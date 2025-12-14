#!/usr/bin/env python3
"""
AI Engine Context Enforcement for AIOS Workspace
Ensures AI engines remember PowerShell-only context through consciousness integration
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

logger = logging.getLogger("ai_engine_context_enforcer")


class AIEngineContextEnforcer:
    """
    AIOS Consciousness Integration for AI Engine Context Enforcement
<<<<<<< HEAD

=======
    
>>>>>>> origin/OS0.6.2.grok
    Biological Role: Membrane supercell interface management
    Function: Ensures AI engines maintain PowerShell context awareness
    Integration: Links with VS Code, GitHooks, and AIOS consciousness system
    """
<<<<<<< HEAD

=======
    
>>>>>>> origin/OS0.6.2.grok
    def __init__(self, workspace_root: Optional[str] = None):
        self.workspace_root = Path(workspace_root) if workspace_root else Path.cwd()
        self.context_config = self._load_context_config()
        self.violation_log = []
<<<<<<< HEAD

        logger.info("🤖 AI Engine Context Enforcer initialized")

=======
        
        logger.info("🤖 AI Engine Context Enforcer initialized")
    
>>>>>>> origin/OS0.6.2.grok
    def _load_context_config(self) -> Dict[str, Any]:
        """Load AI context enforcement configuration"""
        return {
            "os_type": "Windows",
            "shell": "PowerShell",
            "forbidden_commands": [
<<<<<<< HEAD
                "rm",
                "ls",
                "grep",
                "touch",
                "cp",
                "mv",
                "cat",
                "find",
                "chmod",
                "chown",
                "sudo",
                "apt",
                "yum",
                "nano",
                "vim",
            ],
            "required_commands": [
                "Remove-Item",
                "Get-ChildItem",
                "Select-String",
                "New-Item",
                "Copy-Item",
                "Move-Item",
                "Get-Content",
            ],
            "enforcement_level": "strict",
            "auto_correction": True,
            "logging_enabled": True,
        }

=======
                "rm", "ls", "grep", "touch", "cp", "mv", "cat", "find",
                "chmod", "chown", "sudo", "apt", "yum", "nano", "vim"
            ],
            "required_commands": [
                "Remove-Item", "Get-ChildItem", "Select-String", 
                "New-Item", "Copy-Item", "Move-Item", "Get-Content"
            ],
            "enforcement_level": "strict",
            "auto_correction": True,
            "logging_enabled": True
        }
    
>>>>>>> origin/OS0.6.2.grok
    def generate_context_reminder(self, context_type: str = "general") -> str:
        """Generate context reminder for AI engines"""
        reminders = {
            "general": "🚨 AIOS WORKSPACE: Use PowerShell commands only. No Linux bash!",
            "terminal": "⚠️ Terminal Context: Windows PowerShell environment - use PowerShell syntax",
            "githook": "🔧 GitHook Context: PowerShell-only environment for AIOS operations",
<<<<<<< HEAD
            "vscode": "🖥️ VS Code Context: AIOS workspace requires PowerShell commands",
        }

        return reminders.get(context_type, reminders["general"])

    def detect_command_violations(self, command_text: str) -> List[Dict[str, str]]:
        """Detect Linux command usage in AI-generated content"""
        violations = []

        for forbidden_cmd in self.context_config["forbidden_commands"]:
            if f" {forbidden_cmd} " in f" {command_text} " or command_text.startswith(
                f"{forbidden_cmd} "
            ):
                # Find PowerShell equivalent
                equivalent = self._get_powershell_equivalent(forbidden_cmd)
                violations.append(
                    {
                        "forbidden_command": forbidden_cmd,
                        "powershell_equivalent": equivalent,
                        "violation_type": "linux_command_usage",
                        "severity": "high",
                    }
                )

        return violations

=======
            "vscode": "🖥️ VS Code Context: AIOS workspace requires PowerShell commands"
        }
        
        return reminders.get(context_type, reminders["general"])
    
    def detect_command_violations(self, command_text: str) -> List[Dict[str, str]]:
        """Detect Linux command usage in AI-generated content"""
        violations = []
        
        for forbidden_cmd in self.context_config["forbidden_commands"]:
            if f" {forbidden_cmd} " in f" {command_text} " or command_text.startswith(f"{forbidden_cmd} "):
                # Find PowerShell equivalent
                equivalent = self._get_powershell_equivalent(forbidden_cmd)
                violations.append({
                    "forbidden_command": forbidden_cmd,
                    "powershell_equivalent": equivalent,
                    "violation_type": "linux_command_usage",
                    "severity": "high"
                })
        
        return violations
    
>>>>>>> origin/OS0.6.2.grok
    def _get_powershell_equivalent(self, linux_command: str) -> str:
        """Get PowerShell equivalent for Linux command"""
        equivalents = {
            "rm": "Remove-Item",
<<<<<<< HEAD
            "ls": "Get-ChildItem",
=======
            "ls": "Get-ChildItem", 
>>>>>>> origin/OS0.6.2.grok
            "grep": "Select-String",
            "touch": "New-Item",
            "cp": "Copy-Item",
            "mv": "Move-Item",
            "cat": "Get-Content",
            "find": "Get-ChildItem -Recurse",
            "chmod": "Set-ItemProperty",
<<<<<<< HEAD
            "pwd": "Get-Location",
        }

        return equivalents.get(
            linux_command, f"PowerShell equivalent for '{linux_command}'"
        )

    def enforce_context_on_ai_interaction(
        self, ai_response: str, context: str = "general"
    ) -> Dict[str, Any]:
        """Enforce PowerShell context on AI engine interaction"""
        violations = self.detect_command_violations(ai_response)

=======
            "pwd": "Get-Location"
        }
        
        return equivalents.get(linux_command, f"PowerShell equivalent for '{linux_command}'")
    
    def enforce_context_on_ai_interaction(self, ai_response: str, context: str = "general") -> Dict[str, Any]:
        """Enforce PowerShell context on AI engine interaction"""
        violations = self.detect_command_violations(ai_response)
        
>>>>>>> origin/OS0.6.2.grok
        enforcement_result = {
            "timestamp": datetime.now().isoformat(),
            "context_type": context,
            "violations_found": len(violations),
            "violations": violations,
            "context_reminder": self.generate_context_reminder(context),
<<<<<<< HEAD
            "enforcement_applied": len(violations) > 0,
        }

        if violations and self.context_config["logging_enabled"]:
            self._log_violation(enforcement_result)

        return enforcement_result

=======
            "enforcement_applied": len(violations) > 0
        }
        
        if violations and self.context_config["logging_enabled"]:
            self._log_violation(enforcement_result)
        
        return enforcement_result
    
>>>>>>> origin/OS0.6.2.grok
    def _log_violation(self, enforcement_result: Dict[str, Any]):
        """Log context enforcement violation"""
        log_entry = {
            "timestamp": enforcement_result["timestamp"],
            "violations": enforcement_result["violations"],
            "context": enforcement_result["context_type"],
<<<<<<< HEAD
            "workspace": str(self.workspace_root),
        }

        self.violation_log.append(log_entry)

=======
            "workspace": str(self.workspace_root)
        }
        
        self.violation_log.append(log_entry)
        
>>>>>>> origin/OS0.6.2.grok
        # Write to log file
        log_path = self.workspace_root / ".vscode" / "ai_context_violations.jsonl"
        try:
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(log_entry) + "\n")
        except Exception as e:
            logger.warning(f"Failed to write violation log: {e}")
<<<<<<< HEAD

=======
    
>>>>>>> origin/OS0.6.2.grok
    def get_context_status(self) -> Dict[str, Any]:
        """Get current AI context enforcement status"""
        return {
            "workspace_root": str(self.workspace_root),
            "enforcement_active": True,
            "total_violations_logged": len(self.violation_log),
            "context_config": self.context_config,
<<<<<<< HEAD
            "last_enforcement": (
                self.violation_log[-1]["timestamp"] if self.violation_log else None
            ),
        }

=======
            "last_enforcement": self.violation_log[-1]["timestamp"] if self.violation_log else None
        }
    
>>>>>>> origin/OS0.6.2.grok
    def create_ai_context_files(self):
        """Create persistent AI context files in workspace"""
        vscode_dir = self.workspace_root / ".vscode"
        vscode_dir.mkdir(exist_ok=True)
<<<<<<< HEAD

        # Create comprehensive context file
        context_content = self._generate_comprehensive_context()
        context_file = vscode_dir / "AI_CONTEXT_POWERSHELL_ONLY.md"

        with open(context_file, "w", encoding="utf-8") as f:
            f.write(context_content)

        logger.info(f"✅ AI context files created in {vscode_dir}")

=======
        
        # Create comprehensive context file
        context_content = self._generate_comprehensive_context()
        context_file = vscode_dir / "AI_CONTEXT_POWERSHELL_ONLY.md"
        
        with open(context_file, "w", encoding="utf-8") as f:
            f.write(context_content)
        
        logger.info(f"✅ AI context files created in {vscode_dir}")
    
>>>>>>> origin/OS0.6.2.grok
    def _generate_comprehensive_context(self) -> str:
        """Generate comprehensive AI context content"""
        return f"""# 🚨 CRITICAL AI ENGINE CONTEXT 🚨
## AIOS WORKSPACE - POWERSHELL ONLY

**Generated**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Environment**: {self.context_config['os_type']} {self.context_config['shell']}

### ❌ FORBIDDEN COMMANDS:
{chr(10).join(f"- `{cmd}` → Use PowerShell equivalent" for cmd in self.context_config['forbidden_commands'])}

### ✅ REQUIRED COMMANDS:
{chr(10).join(f"- `{cmd}`" for cmd in self.context_config['required_commands'])}

### 🤖 AI ENGINE INSTRUCTIONS:
1. Always use PowerShell syntax for terminal commands
2. Check this file if unsure about command syntax
3. Test commands in PowerShell environment before suggesting
4. Remember: We are on Windows, not Linux
5. When in doubt: Use PowerShell equivalents

**This context is persistent and should be referenced by all AI engines working in AIOS!**
"""

    def integrate_with_consciousness(self, consciousness_bridge=None):
        """Integrate with AIOS consciousness system"""
        if consciousness_bridge:
            consciousness_bridge.register_membrane_enforcer(self)
            logger.info("🧠 AI Context Enforcer integrated with AIOS consciousness")
<<<<<<< HEAD

        return {
            "integration_status": "active",
            "consciousness_bridge": consciousness_bridge is not None,
            "enforcement_level": self.context_config["enforcement_level"],
=======
        
        return {
            "integration_status": "active",
            "consciousness_bridge": consciousness_bridge is not None,
            "enforcement_level": self.context_config["enforcement_level"]
>>>>>>> origin/OS0.6.2.grok
        }


# Export for AIOS consciousness integration
__all__ = ["AIEngineContextEnforcer"]


# Demo/Test function
async def main():
    """Demonstrate AI Engine Context Enforcement"""
    enforcer = AIEngineContextEnforcer()
<<<<<<< HEAD

=======
    
>>>>>>> origin/OS0.6.2.grok
    # Test command detection
    test_commands = [
        "rm -rf node_modules",
        "ls -la",
        "grep pattern file.txt",
        "Remove-Item -Recurse node_modules",
<<<<<<< HEAD
        "Get-ChildItem -Force",
    ]

    print("🤖 AI Engine Context Enforcement Demo")
    print("=" * 50)

=======
        "Get-ChildItem -Force"
    ]
    
    print("🤖 AI Engine Context Enforcement Demo")
    print("=" * 50)
    
>>>>>>> origin/OS0.6.2.grok
    for cmd in test_commands:
        result = enforcer.enforce_context_on_ai_interaction(cmd, "terminal")
        status = "❌ VIOLATION" if result["violations_found"] > 0 else "✅ COMPLIANT"
        print(f"{status}: {cmd}")
<<<<<<< HEAD

        if result["violations_found"] > 0:
            for violation in result["violations"]:
                print(f"    → Use: {violation['powershell_equivalent']}")

=======
        
        if result["violations_found"] > 0:
            for violation in result["violations"]:
                print(f"    → Use: {violation['powershell_equivalent']}")
    
>>>>>>> origin/OS0.6.2.grok
    print("\n" + enforcer.generate_context_reminder("general"))


if __name__ == "__main__":
    import asyncio
<<<<<<< HEAD

    asyncio.run(main())
=======
    asyncio.run(main())
>>>>>>> origin/OS0.6.2.grok
