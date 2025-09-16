# AIOS GitHook Emotikiller Module
# STRICT NO EMOTICON POLICY ENFORCED
# Automated emoticon detection and removal for commit/push enforcement

## Overview

This module integrates the AIOS Emotikiller functionality into the GitHook system for automated enforcement of the no-emoticon policy during commit and push operations.

## Architecture

### Integration Points
- **Pre-Commit Hook**: Scans staged files for emoticons before allowing commit
- **Pre-Push Hook**: Validates branch content before allowing push
- **Policy Enforcement**: Blocks commits/pushes containing emoticons
- **Automated Cleanup**: Optional auto-removal with user confirmation

### Module Structure
```
.githooks/modules/laboratory/emotikiller/
├── README.md                    # This documentation
├── emoticon_detector.ps1        # Core emoticon detection logic
├── hook_integration.ps1         # GitHook integration functions
├── policy_config.json          # Emoticon policy configuration
└── test_emotikiller_hooks.ps1   # Testing and validation
```

## Integration with Nucleus Module

The emotikiller integrates with the nucleus pre-commit and pre-push scripts through:

1. **Function Import**: Nucleus modules import emotikiller functions
2. **Policy Validation**: Emoticon checks added to validation pipeline
3. **Reporting Integration**: Results included in hook logging
4. **Bypass Mechanism**: Emergency bypass for critical commits

## Configuration

### Policy Settings (`policy_config.json`)
```json
{
    "enabled": true,
    "enforcement_level": "block",
    "auto_cleanup": false,
    "patterns": {
        "unicode_emoticons": true,
        "ascii_emoticons": true,
        "text_expressions": true,
        "kaomoji": true
    },
    "excluded_paths": [
        "docs/examples/",
        "test/fixtures/"
    ],
    "bypass_env_var": "AIOS_EMOTIKILLER_BYPASS"
}
```

### Enforcement Levels
- **block**: Prevent commit/push when emoticons detected
- **warn**: Show warnings but allow operation
- **report**: Log detection without blocking
- **disabled**: Turn off emoticon detection

## Usage

### Automatic Operation
The emotikiller runs automatically during:
- `git commit` - Scans staged files
- `git push` - Validates branch content

### Manual Testing
```powershell
# Test emoticon detection on specific files
.\test_emotikiller_hooks.ps1 -TestFiles @("file1.md", "file2.py")

# Test entire repository
.\test_emotikiller_hooks.ps1 -FullScan

# Test with auto-cleanup
.\test_emotikiller_hooks.ps1 -AutoCleanup
```

### Emergency Bypass
```powershell
# Bypass emoticon checks for emergency commits
$env:AIOS_EMOTIKILLER_BYPASS = "emergency-fix-2025-09-15"
git commit -m "Emergency fix"
```

## Professional Standards

### Code Quality
- No emoticons in any detection or enforcement code
- Professional error messages and logging
- Comprehensive validation and testing
- Clean integration with existing hooks

### Performance
- Fast scanning algorithms for large repositories
- Incremental detection for staged files only
- Efficient pattern matching with compiled regex
- Minimal impact on commit/push operations

### Reliability
- Robust error handling and recovery
- Fallback mechanisms for detection failures
- Comprehensive logging for troubleshooting
- Integration testing with GitHook pipeline

## Implementation Status

### Completed
- [x] Core emoticon detection algorithms
- [x] Multi-language implementation (C++, Python, PowerShell)
- [x] GitHook module architecture
- [x] Policy configuration system

### In Progress
- [ ] Hook integration with nucleus module
- [ ] Testing and validation framework
- [ ] Documentation and user guides

### Planned
- [ ] Performance optimization
- [ ] Advanced pattern detection
- [ ] Integration with AIOS governance
- [ ] Metrics and reporting dashboard