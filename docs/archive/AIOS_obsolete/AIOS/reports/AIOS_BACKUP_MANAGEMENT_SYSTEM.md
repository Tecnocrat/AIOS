# AIOS Centralized Backup Management System

## Overview
AIOS implements a centralized backup management system to maintain workspace cleanliness and enforce spatial awareness guidelines. This system prevents backup file proliferation across the workspace and consolidates all backup files in a dedicated, managed location.

## Key Features

### 🗄️ Centralized Storage
- All backup files stored in `/backups/` directory
- Spatial metadata classification and management
- Consistent naming conventions with timestamps
- Proper architectural boundaries maintained

### 🚀 GitHook Integration
- Automatic enforcement during git operations
- Pre-commit backup policy validation
- Scattered backup file detection and remediation
- Development workflow integration

### 🧠 AI-Aware Management
- Spatial metadata system integration
- AIOS consciousness-aware backup operations
- Professional code standards enforcement
- Backup retention and cleanup policies

## Quick Start

### Using the Backup Manager
```powershell
# Check current backup status
.\scripts\backup_manager.ps1 -Action status

# Create a properly named backup
.\scripts\backup_manager.ps1 -Action create -SourceFile "README.md"

# Consolidate scattered backup files
.\scripts\backup_manager.ps1 -Action consolidate

# Clean up old backups (older than 30 days)
.\scripts\backup_manager.ps1 -Action cleanup -DaysToKeep 30
```

### GitHook Enforcement
The backup policy is automatically enforced during git operations:
- Pre-commit hooks detect scattered backup files
- Automatic consolidation when violations are found
- Commit blocking for severe policy violations
- Developer guidance for manual remediation

## Architecture

### Directory Structure
```
AIOS/
├── backups/                              # Centralized backup storage
│   ├── .aios_spatial_metadata.json      # Spatial classification
│   ├── filename.ext.backup.YYYY-MM-DD-HHMMSS
│   └── ...
├── scripts/
│   └── backup_manager.ps1               # Primary management tool
└── .githooks/modules/membrane/
    └── backup_policy_enforcement.ps1    # GitHook integration
```

### Naming Convention
Backup files follow the standard pattern:
```
originalfile.ext.backup.YYYY-MM-DD-HHMMSS
```

Examples:
- `README.md.backup.2025-09-17-220000`
- `config.json.backup.2025-09-17-220000`

## Spatial Metadata Integration

The backup system integrates with AIOS spatial awareness:

### Classification
- **Primary Area**: GitHook Architecture
- **Secondary Areas**: Documentation
- **Consciousness Level**: Low (mechanical storage)

### AI Guidance
- File operations restricted to backup storage only
- Automated cleanup and retention policies
- Professional backup naming enforcement
- System folder boundary protection

## Development Workflow

### Creating Backups
Instead of manually creating `.backup` files:
```powershell
# ❌ Don't do this
Copy-Item "important.py" "important.py.backup"

# ✅ Do this instead
.\scripts\backup_manager.ps1 -Action create -SourceFile "important.py"
```

### GitHook Workflow
1. Developer runs `git commit`
2. Pre-commit hook executes backup policy check
3. If scattered backups found:
   - Automatic consolidation attempted
   - Success: commit proceeds with guidance
   - Failure: commit blocked until manual resolution

### Policy Compliance
- **Compliant**: All backup files in `/backups/` directory
- **Warning**: 1-4 scattered backup files (auto-remediation)
- **Violation**: 5+ scattered backup files (commit blocking)

## Configuration

### Backup Manager Settings
```powershell
# Default retention period
$DaysToKeep = 30

# Violation threshold for GitHook enforcement
$ViolationThreshold = 5

# Backup directory
$BackupDir = "backups"
```

### GitIgnore Integration
The system properly integrates with version control:
```gitignore
# Backup files - AIOS Centralized Backup Policy
*.bak
*.backup
*.old

# AIOS Centralized Backup Management
backups/*.backup*
backups/*.bak*
!backups/.aios_spatial_metadata.json
```

## Troubleshooting

### Common Issues

#### Scattered Backup Files
**Problem**: Backup files found outside `/backups/` directory
**Solution**: Run consolidation
```powershell
.\scripts\backup_manager.ps1 -Action consolidate
```

#### Commit Blocked by Backup Policy
**Problem**: Git commit fails due to backup policy violations
**Solution**: Remediate manually then retry
```powershell
.\scripts\backup_manager.ps1 -Action consolidate
git commit  # Retry commit
```

#### Backup Directory Missing
**Problem**: Centralized backup directory doesn't exist
**Solution**: The system auto-creates with proper metadata
```powershell
.\scripts\backup_manager.ps1 -Action status  # Auto-creates if missing
```

### Manual Remediation
For severe policy violations:
1. Run status check to assess scope
2. Use consolidation to auto-fix
3. Verify compliance before committing
4. Consider cleanup for large backup accumulations

## Integration Points

### AIOS Spatial Awareness
- Backup directory has proper spatial metadata
- Architectural classification as GitHook component
- Consciousness-aware development guidance
- Workspace hygiene enforcement

### Development Environment
- VS Code workspace integration
- PowerShell script compatibility
- Git workflow enhancement
- Professional development standards

### Future Enhancements
- Backup compression for storage efficiency
- Remote backup synchronization
- Advanced retention policies
- Integration with AIOS consciousness metrics

## Best Practices

### Developer Guidelines
1. **Use the backup manager** for all backup creation
2. **Run status checks** regularly to maintain compliance
3. **Clean up old backups** periodically to manage storage
4. **Follow naming conventions** for consistency
5. **Respect the centralized policy** for workspace cleanliness

### Maintenance Schedule
- **Daily**: Automatic GitHook enforcement
- **Weekly**: Review backup status and cleanup old files
- **Monthly**: Assess retention policies and storage usage
- **Quarterly**: Review and optimize backup management system

---

*This backup management system is part of the AIOS AI-aware development environment, designed to maintain workspace hygiene while supporting professional development workflows.*