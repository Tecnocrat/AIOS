#!/usr/bin/env python3
"""
AIOS VSCode Workspace Health Validator
=====================================
Checks and validates VSCode workspace configuration for development health
Prevents formatting conflicts and ensures stable development environment
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any


class VSCodeHealthValidator:
    """Validates VSCode workspace health and prevents conflicts"""

    def __init__(self, workspace_root: Path):
        self.workspace_root = Path(workspace_root)
        self.workspace_file = self.workspace_root / "AIOS.code-workspace"
        self.settings_file = self.workspace_root / ".vscode" / "settings.json"
        self.editorconfig = self.workspace_root / ".editorconfig"
        
        self.health_issues = []
        self.recommendations = []

    def validate_workspace_configuration(self) -> Dict[str, Any]:
        """Validate workspace configuration for health issues"""
        
        print(" AIOS VSCode Workspace Health Check")
        print("=" * 50)
        
        # Check workspace file
        workspace_health = self._check_workspace_file()
        
        # Check settings file
        settings_health = self._check_settings_file()
        
        # Check editorconfig
        editorconfig_health = self._check_editorconfig()
        
        # Check for conflicting extensions
        extension_health = self._check_extension_conflicts()
        
        # Generate overall health score
        health_score = self._calculate_health_score(
            workspace_health, settings_health,
            editorconfig_health, extension_health
        )
        
        return {
            "overall_health": health_score,
            "workspace_file": workspace_health,
            "settings_file": settings_health,
            "editorconfig": editorconfig_health,
            "extension_conflicts": extension_health,
            "issues": self.health_issues,
            "recommendations": self.recommendations
        }

    def _check_workspace_file(self) -> Dict[str, Any]:
        """Check AIOS.code-workspace for configuration health"""
        if not self.workspace_file.exists():
            self.health_issues.append(" AIOS.code-workspace file missing")
            return {"status": "missing", "score": 0.0}
        
        try:
            with open(self.workspace_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Remove comments for JSON parsing (JSONC to JSON)
            import re
            # Remove single-line comments
            content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
            # Remove empty lines created by comment removal
            content = re.sub(r'^\s*\n', '', content, flags=re.MULTILINE)
            
            workspace_config = json.loads(content)
            
            issues = []
            
            # Check critical formatter settings
            settings = workspace_config.get("settings", {})
            
            if settings.get("editor.formatOnSave", True):
                issues.append(" editor.formatOnSave should be false")
            
            if settings.get("python.formatting.provider") != "none":
                issues.append(" python.formatting.provider should be 'none'")
            
            if settings.get("python.linting.enabled", True):
                issues.append(" python.linting.enabled should be false")
            
            code_actions = settings.get("editor.codeActionsOnSave", {})
            if code_actions.get("source.fixAll") != "never":
                issues.append(" source.fixAll should be 'never'")
            
            if not issues:
                print(" Workspace file: HEALTHY")
                return {"status": "healthy", "score": 1.0, "issues": []}
            else:
                print(f"  Workspace file: {len(issues)} issues found")
                for issue in issues:
                    print(f"   {issue}")
                return {"status": "issues", "score": 0.5, "issues": issues}
                
        except Exception as e:
            self.health_issues.append(f" Workspace file parse error: {e}")
            return {"status": "error", "score": 0.0}

    def _check_settings_file(self) -> Dict[str, Any]:
        """Check .vscode/settings.json for conflicts"""
        if not self.settings_file.exists():
            print("  .vscode/settings.json missing (using workspace defaults)")
            return {"status": "missing", "score": 0.8}
        
        try:
            with open(self.settings_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Remove comments for JSON parsing (JSONC to JSON)
            import re
            content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
            content = re.sub(r'^\s*\n', '', content, flags=re.MULTILINE)
            
            settings = json.loads(content)
            
            issues = []
            
            # Check for conflicting formatter settings
            if settings.get("python.analysis.autoImportCompletions", False):
                issues.append(" autoImportCompletions should be false")
            
            if settings.get("python.linting.enabled", False):
                issues.append(" Python linting should be disabled")
            
            if settings.get("omnisharp.organizeImportsOnFormat", False):
                issues.append(" C# organize imports on format should be false")
            
            if not issues:
                print(" Settings file: HEALTHY")
                return {"status": "healthy", "score": 1.0, "issues": []}
            else:
                print(f"  Settings file: {len(issues)} issues found")
                return {"status": "issues", "score": 0.6, "issues": issues}
                
        except Exception as e:
            self.health_issues.append(f" Settings file parse error: {e}")
            return {"status": "error", "score": 0.0}

    def _check_editorconfig(self) -> Dict[str, Any]:
        """Check .editorconfig for format enforcement"""
        if not self.editorconfig.exists():
            self.recommendations.append(" Consider adding .editorconfig for consistent formatting")
            return {"status": "missing", "score": 0.7}
        
        try:
            with open(self.editorconfig, 'r', encoding='utf-8') as f:
                content = f.read()
            
            required_sections = ["[*.py]", "max_line_length = 79"]
            missing = [section for section in required_sections if section not in content]
            
            if not missing:
                print(" .editorconfig: HEALTHY")
                return {"status": "healthy", "score": 1.0, "missing": []}
            else:
                print(f"  .editorconfig: Missing {len(missing)} recommendations")
                return {"status": "partial", "score": 0.8, "missing": missing}
                
        except Exception as e:
            return {"status": "error", "score": 0.0}

    def _check_extension_conflicts(self) -> Dict[str, Any]:
        """Check for potentially conflicting extensions"""
        extensions_file = self.workspace_root / ".vscode" / "extensions.json"
        
        if not extensions_file.exists():
            return {"status": "no_config", "score": 0.9}
        
        # For Copilot-driven development, formatters are beneficial tools
        # when configured for manual control rather than auto-formatting
        recommended_formatters = [
            "ms-python.black-formatter",  # Good for Copilot code cleanup
            "ms-python.isort"  # Useful for import organization
        ]
        
        print(" Formatters beneficial with manual control in Copilot")
        self.recommendations.append(
            " Keep formatters for Copilot cleanup, ensure formatOnSave=false"
        )
        
        return {"status": "manual_check_needed", "score": 0.8}

    def _calculate_health_score(self, workspace: Dict, settings: Dict, 
                              editorconfig: Dict, extensions: Dict) -> float:
        """Calculate overall health score"""
        scores = [
            workspace["score"] * 0.4,  # Workspace config most critical
            settings["score"] * 0.3,   # Settings config important
            editorconfig["score"] * 0.2,  # Editorconfig helpful
            extensions["score"] * 0.1   # Extensions check minimal
        ]
        
        overall = sum(scores)
        
        if overall >= 0.9:
            print(f"\n Overall Health: EXCELLENT ({overall:.1%})")
        elif overall >= 0.7:
            print(f"\n Overall Health: GOOD ({overall:.1%})")
        elif overall >= 0.5:
            print(f"\n  Overall Health: NEEDS ATTENTION ({overall:.1%})")
        else:
            print(f"\n Overall Health: CRITICAL ({overall:.1%})")
        
        return overall

    def generate_health_report(self) -> str:
        """Generate a detailed health report"""
        validation_result = self.validate_workspace_configuration()
        
        report = [
            "\n" + "=" * 60,
            " AIOS VSCODE WORKSPACE HEALTH REPORT",
            "=" * 60,
            f"Overall Health Score: {validation_result['overall_health']:.1%}",
            ""
        ]
        
        if self.health_issues:
            report.append(" Critical Issues:")
            for issue in self.health_issues:
                report.append(f"  {issue}")
            report.append("")
        
        if self.recommendations:
            report.append(" Recommendations:")
            for rec in self.recommendations:
                report.append(f"  {rec}")
            report.append("")
        
        report.extend([
            " Component Health:",
            f"  Workspace Config: {validation_result['workspace_file']['score']:.1%}",
            f"  Settings File: {validation_result['settings_file']['score']:.1%}",
            f"  EditorConfig: {validation_result['editorconfig']['score']:.1%}",
            f"  Extension Check: {validation_result['extension_conflicts']['score']:.1%}",
            "",
            " Next Steps:",
            "  1. Fix any critical issues above",
            "  2. Implement recommendations for optimal health",
            "  3. Run health check after VSCode restart",
            "  4. Monitor for formatting conflicts during development",
            "",
            "=" * 60
        ])
        
        return "\n".join(report)


def main():
    """Main health check execution"""
    workspace_root = Path(__file__).parent.parent
    validator = VSCodeHealthValidator(workspace_root)
    
    try:
        report = validator.generate_health_report()
        print(report)
        
        # Save report to file
        report_file = workspace_root / "runtime" / "logs" / "vscode_health_report.txt"
        report_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"\n Health report saved: {report_file}")
        
        return 0
        
    except Exception as e:
        print(f" Health check failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
