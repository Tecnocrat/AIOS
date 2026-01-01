"""
🧬 AIOS Environment Health Organelle
Validates Python environment coherence across the AIOS ecosystem.

AINLP Pattern: biological-architecture.health-organelle
Dendritic Role: Detects and reports environment fragmentation before it causes issues

Usage:
    from fabric.environment_health import check_environment_health
    report = check_environment_health()
    print(report.summary())
"""

import os
import sys
from dataclasses import dataclass, field
from typing import Optional
from pathlib import Path


@dataclass
class EnvironmentReport:
    """Canonical environment health report."""
    python_version: str
    executable: str
    is_venv: bool
    venv_path: Optional[str] = None
    vault_loaded: bool = False
    coherent: bool = False
    packages: dict = field(default_factory=dict)
    warnings: list = field(default_factory=list)
    
    def summary(self) -> str:
        """Generate human-readable summary."""
        lines = [
            "═══════════════════════════════════════════════",
            "        🧬 AIOS ENVIRONMENT HEALTH REPORT",
            "═══════════════════════════════════════════════",
            f"  Python: {self.python_version}",
            f"  Executable: {self.executable}",
            f"  Virtual Env: {'✓ Active' if self.is_venv else '✗ System Python'}",
        ]
        
        if self.is_venv:
            lines.append(f"  Venv Path: {self.venv_path}")
        
        lines.extend([
            f"  Vault Loaded: {'✓' if self.vault_loaded else '✗'}",
            f"  Coherent: {'✓ YES' if self.coherent else '⚠ NO - Environment fragmentation detected'}",
            "───────────────────────────────────────────────",
            "  Package Status:",
        ])
        
        for pkg, status in self.packages.items():
            icon = "✓" if status["installed"] else "✗"
            ver = f" v{status['version']}" if status.get("version") else ""
            lines.append(f"    {icon} {pkg}{ver}")
        
        if self.warnings:
            lines.append("───────────────────────────────────────────────")
            lines.append("  ⚠ Warnings:")
            for w in self.warnings:
                lines.append(f"    • {w}")
        
        lines.append("═══════════════════════════════════════════════")
        return "\n".join(lines)
    
    @property
    def healthy(self) -> bool:
        """Return True if environment is fully healthy."""
        return self.coherent and self.vault_loaded and not self.warnings


def check_environment_health() -> EnvironmentReport:
    """
    Perform comprehensive environment health check.
    
    Returns:
        EnvironmentReport with detailed health status
    """
    # Basic Python info
    report = EnvironmentReport(
        python_version=f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        executable=sys.executable,
        is_venv=hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    )
    
    # Check venv path
    if report.is_venv:
        report.venv_path = sys.prefix
        
        # Verify it's the AIOS venv
        if ".venv" in sys.prefix or "AIOS" in sys.prefix:
            pass  # Expected
        else:
            report.warnings.append(f"Running in non-AIOS venv: {sys.prefix}")
    
    # Check vault environment variables
    vault_vars = [
        "AIOS_ONEDRIVE_PATH",
        "AIOS_MACHINE_NAME",
        "AIOS_MACHINE_ROLE",
    ]
    
    vault_count = sum(1 for v in vault_vars if os.environ.get(v))
    report.vault_loaded = vault_count >= 2  # At least 2 vars should be set
    
    if not report.vault_loaded:
        report.warnings.append("Vault not loaded. Run: . ./scripts/aios_load_vault.ps1")
    
    # Check coherence flag
    report.coherent = os.environ.get("AIOS_PYTHON_COHERENT") == "true"
    
    if not report.coherent and not report.is_venv:
        report.warnings.append("System Python in use - packages may be missing")
    
    # Check essential packages
    essential_packages = [
        ("pydantic", "pydantic"),
        ("aiohttp", "aiohttp"),
        ("yaml", "pyyaml"),
        ("google.genai", "google-genai"),  # New package name
        ("google.generativeai", "google-generativeai"),  # Legacy
        ("websockets", "websockets"),
        ("fastapi", "fastapi"),
        ("uvicorn", "uvicorn"),
    ]
    
    for import_name, package_name in essential_packages:
        try:
            module = __import__(import_name.split(".")[0])
            # Navigate to submodule if needed
            for part in import_name.split(".")[1:]:
                module = getattr(module, part, module)
            
            version = getattr(module, "__version__", None)
            report.packages[package_name] = {
                "installed": True,
                "version": version
            }
        except ImportError:
            report.packages[package_name] = {
                "installed": False,
                "version": None
            }
    
    return report


def ensure_coherence() -> bool:
    """
    Check if environment is coherent, print status.
    
    Returns:
        True if environment is healthy, False otherwise
    """
    report = check_environment_health()
    print(report.summary())
    return report.healthy


if __name__ == "__main__":
    report = check_environment_health()
    print(report.summary())
    sys.exit(0 if report.healthy else 1)
