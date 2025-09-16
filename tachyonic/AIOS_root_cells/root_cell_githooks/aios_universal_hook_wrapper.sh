# ARCHIVED: AIOS Universal Hook Wrapper (Reference Implementation)
# Originally: #!/bin/sh - REMOVED (Reference only, not executable)
# Location: tachyonic/AIOS_root_cells/root_cell_githooks/
# AIOS Universal Git Hook Wrapper - Consciousness-Guided Cross-Platform Execution
# This unified wrapper eliminates code duplication while maintaining full consciousness transcendence
# Usage: Sources this script from individual git hooks for adaptive PowerShell execution

# Get the hook name from the calling script
hook_name=$(basename "$0")

# Consciousness-aware error reporting
report_consciousness_error() {
    echo " AIOS Consciousness Error: $1" >&2
    echo "Hook: $hook_name" >&2
    echo "Recommendation: $2" >&2
    exit 1
}

# Tachyonic PowerShell detection with consciousness enhancement
detect_powershell() {
    if command -v pwsh >/dev/null 2>&1; then
        echo "pwsh"
        return 0
    elif command -v powershell >/dev/null 2>&1; then
        echo "powershell"
        return 0
    else
        return 1
    fi
}

# Main consciousness-guided execution
main() {
    # Validate hook context
    if [ -z "$hook_name" ]; then
        report_consciousness_error "Hook name detection failed" "Ensure script is called as git hook"
    fi
    
    # Detect PowerShell with consciousness awareness
    powershell_cmd=$(detect_powershell)
    if [ $? -ne 0 ]; then
        report_consciousness_error "PowerShell not found" "Install PowerShell Core (pwsh) or Windows PowerShell"
    fi
    
    # Construct consciousness-enhanced PowerShell invocation
    ps_script="$(dirname "$0")/${hook_name}.ps1"
    
    # Validate PowerShell script exists
    if [ ! -f "$ps_script" ]; then
        report_consciousness_error "PowerShell implementation not found: $ps_script" "Ensure ${hook_name}.ps1 exists with consciousness integration"
    fi
    
    # Execute with optimal PowerShell configuration for consciousness transcendence
    exec "$powershell_cmd" -NoProfile -ExecutionPolicy Bypass -File "$ps_script" "$@"
}

# Consciousness activation
main "$@"
