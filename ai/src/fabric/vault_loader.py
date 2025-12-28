#!/usr/bin/env python3
"""
AIOS Vault Organelle Loader (Python)
AINLP Pattern: biological-architecture.vault-organelle

Reads vault.local.yaml and provides paths/secrets to Python scripts.
Environment variables take precedence over vault file values.

Supports ${VAR} syntax in vault.local.yaml for env var references.

Usage:
    from ai.src.fabric.vault_loader import get_vault, get_path, get_secret
    
    # Get specific path
    onedrive = get_path("onedrive_aios")
    
    # Get secret (checks env first, then vault)
    api_key = get_secret("gemini_api_key")
    
    # Get full vault dict
    vault = get_vault()
"""

import os
import re
from pathlib import Path
from typing import Dict, Any, Optional
import logging

# Try yaml, fall back to simple parser
try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    yaml = None
    YAML_AVAILABLE = False

logger = logging.getLogger(__name__)

# Cache for vault data
_vault_cache: Optional[Dict[str, Any]] = None

# Pattern to match ${VAR} or $VAR env var references
_ENV_VAR_PATTERN = re.compile(r'\$\{([^}]+)\}|\$([A-Z_][A-Z0-9_]*)')


def _resolve_env_vars(value: Any) -> Any:
    """Resolve ${VAR} references in string values."""
    if not isinstance(value, str):
        return value
    
    def replacer(match):
        var_name = match.group(1) or match.group(2)
        return os.environ.get(var_name, "")
    
    resolved = _ENV_VAR_PATTERN.sub(replacer, value)
    return resolved if resolved else None


def _find_vault_path() -> Optional[Path]:
    """Locate vault.local.yaml in AIOS hierarchy."""
    # Check environment override
    if env_path := os.environ.get("AIOS_VAULT_PATH"):
        return Path(env_path)
    
    # Search from current location up to AIOS root
    search_paths = [
        Path(__file__).parent.parent.parent.parent / "config" / "vault.local.yaml",  # ai/src/fabric → config
        Path.cwd() / "config" / "vault.local.yaml",
        Path.home() / "AIOS" / "config" / "vault.local.yaml",  # Termux
    ]
    
    for path in search_paths:
        if path.exists():
            return path
    
    return None


def get_vault(reload: bool = False) -> Dict[str, Any]:
    """
    Load vault configuration.
    
    Args:
        reload: Force reload from disk (bypass cache)
        
    Returns:
        Dict with vault configuration or empty dict if not found
    """
    global _vault_cache
    
    if _vault_cache is not None and not reload:
        return _vault_cache
    
    vault_path = _find_vault_path()
    
    if not vault_path:
        logger.warning("Vault not found - using environment variables only")
        _vault_cache = {"paths": {}, "secrets": {}, "environment": {}, "machine": {}}
        return _vault_cache
    
    try:
        if YAML_AVAILABLE and yaml is not None:
            with open(vault_path, "r", encoding="utf-8") as f:
                _vault_cache = yaml.safe_load(f) or {}
        else:
            # Simple YAML parser fallback
            _vault_cache = _parse_simple_yaml(vault_path)
        logger.info("Vault loaded from %s", vault_path)
    except (OSError, ValueError) as e:
        logger.error("Failed to load vault: %s", e)
        _vault_cache = {"paths": {}, "secrets": {}, "environment": {}, "machine": {}}
    
    return _vault_cache or {}


def _parse_simple_yaml(path: Path) -> Dict[str, Any]:
    """Simple YAML parser for when PyYAML is not available."""
    result: Dict[str, Any] = {}
    current_section: Optional[str] = None
    
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip()
            
            # Skip comments and empty lines
            if not line or line.lstrip().startswith("#"):
                continue
            
            # Count leading spaces for indentation
            stripped = line.lstrip()
            indent = len(line) - len(stripped)
            
            # Section header (no indent, ends with colon only)
            if indent == 0 and stripped.endswith(":") and ": " not in stripped:
                current_section = stripped[:-1]
                result[current_section] = {}
                continue
            
            # Key-value pair
            if ": " in stripped or stripped.endswith(":"):
                if ":" in stripped:
                    key, _, value = stripped.partition(":")
                    value = value.strip().strip('"').strip("'")
                    
                    if value in ("null", ""):
                        value = None
                    
                    if current_section and indent > 0:
                        result[current_section][key] = value
                    else:
                        result[key] = value
    
    return result


def get_path(key: str, default: Optional[str] = None) -> Optional[str]:
    """
    Get a path from vault or environment.
    
    Environment variable takes precedence:
    - AIOS_ONEDRIVE_PATH for key="onedrive_aios"
    - AIOS_BACKUP_PATH for key="local_backup"
    - etc.
    
    Args:
        key: Path key (e.g., "onedrive_aios")
        default: Default value if not found
        
    Returns:
        Path string or default
    """
    # Check environment first
    env_name = f"AIOS_{key.upper()}_PATH" if not key.endswith("_path") else f"AIOS_{key.upper()}"
    env_name = env_name.replace("_AIOS_PATH", "_PATH")  # AIOS_ONEDRIVE_AIOS_PATH → AIOS_ONEDRIVE_PATH
    
    if env_value := os.environ.get(env_name):
        return env_value
    
    # Fall back to vault
    vault = get_vault()
    return vault.get("paths", {}).get(key, default)


def get_secret(key: str, default: Optional[str] = None) -> Optional[str]:
    """
    Get a secret from environment or vault.
    
    Priority order:
    1. Direct env var (AIOS_GEMINI_API_KEY)
    2. Common variations (GEMINI_API_KEY, GEMINI_KEY)
    3. Vault value (with ${VAR} resolution)
    4. Default
    
    Args:
        key: Secret key (e.g., "gemini_api_key")
        default: Default value if not found
        
    Returns:
        Secret string or default
    """
    # Environment ALWAYS takes precedence for secrets
    env_name = f"AIOS_{key.upper()}"
    if env_value := os.environ.get(env_name):
        return env_value
    
    # Also check common variations
    variations = [
        key.upper(),  # GEMINI_API_KEY
        key.upper().replace("_API_KEY", "_KEY"),  # GEMINI_KEY
    ]
    for var in variations:
        if env_value := os.environ.get(var):
            return env_value
    
    # Fall back to vault (with ${VAR} resolution)
    vault = get_vault()
    vault_value = vault.get("secrets", {}).get(key)
    if vault_value:
        resolved = _resolve_env_vars(vault_value)
        if resolved:
            return resolved
    
    return default


def get_machine_info() -> Dict[str, str]:
    """Get machine identity from vault or environment."""
    vault = get_vault()
    return {
        "name": os.environ.get("AIOS_MACHINE_NAME", vault.get("machine", {}).get("name", "unknown")),
        "role": os.environ.get("AIOS_MACHINE_ROLE", vault.get("machine", {}).get("role", "development")),
    }


def get_onedrive_path() -> Optional[Path]:
    """
    Convenience function for OneDrive AIOS path.
    
    Returns:
        Path object or None if not configured
    """
    if path_str := get_path("onedrive_aios"):
        path = Path(path_str)
        if path.exists():
            return path
        logger.warning("OneDrive path configured but doesn't exist: %s", path)
    return None


# Auto-load vault on import (lazy, only when accessed)
def __getattr__(name: str):
    """Lazy loading of vault data."""
    if name == "ONEDRIVE_PATH":
        return get_onedrive_path()
    if name == "MACHINE_NAME":
        return get_machine_info()["name"]
    if name == "MACHINE_ROLE":
        return get_machine_info()["role"]
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
