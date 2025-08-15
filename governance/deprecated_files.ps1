# Centralized deprecated root file list (single source of truth)
# Import this in scripts that enforce or compute coherence metrics.
$Global:AIOS_DeprecatedRootFiles = @(
    'test_opencv_aios_integration.py'
    'test_chatgpt_integration.py'
    'setup_environment.ps1'
    'terminal.ps1'
    'tachyonic_changelog.yaml'
    'tachyonic_changelog.json'
    'SESSION_SUMMARY.md'
    'SAFETY_PROTOCOL.md'
    'SAFETY_IMPLEMENTATION_SUMMARY.md'
    'safety_demonstration.py'
    'REORGANIZATION_STATUS.md'
    'REGISTRY_CLEANUP_GUIDE.md'
    'README_backup.md'
    'QUICK_CONTEXT_PROMPTS.md'
    'PYTHON_SYSTEM_CLEANUP_GUIDE.md'
)
