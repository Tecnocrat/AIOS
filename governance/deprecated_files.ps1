# Centralized deprecated root file list (single source of truth)
# Import this in scripts that enforce or compute coherence metrics.
$Global:AIOS_DeprecatedRootFiles = @(
    'test_opencv_aios_integration.py'
    'test_chatgpt_integration.py'
    'setup_environment.ps1'
    'terminal.ps1'
    'tachyonic_changelog.yaml'
    'tachyonic_changelog.json'
)
