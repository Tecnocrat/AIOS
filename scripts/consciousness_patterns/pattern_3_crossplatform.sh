#!/bin/sh
# AIOS Universal Consciousness Pattern: Cross-Platform Transcendence
# Canonical Genome Reference: docs/tachyonic/AINLP_CANONICAL_KNOWLEDGE_GENOME.md#pattern-3
# Pattern: Cross-Platform Consciousness Transcendence

# Universal cross-platform consciousness transcendence
detect_platform_consciousness() {
    local platform="unknown"
    
    # Platform detection with consciousness awareness
    case "$(uname -s)" in
        Darwin*)    platform="macos" ;;
        Linux*)     platform="linux" ;;
        CYGWIN*)    platform="cygwin" ;;
        MINGW*)     platform="windows_mingw" ;;
        MSYS*)      platform="windows_msys" ;;
        *)          platform="unknown" ;;
    esac
    
    # Windows detection via PowerShell availability
    if command -v pwsh >/dev/null 2>&1 || command -v powershell >/dev/null 2>&1; then
        if [ "$platform" = "unknown" ]; then
            platform="windows"
        fi
    fi
    
    echo "$platform"
}

# Universal PowerShell execution with consciousness transcendence
execute_consciousness_powershell() {
    local script_path="$1"
    shift
    local args="$@"
    
    # Consciousness-aware PowerShell detection and execution
    if command -v pwsh >/dev/null 2>&1; then
        # PowerShell Core (preferred for consciousness transcendence)
        pwsh -NoProfile -ExecutionPolicy Bypass -File "$script_path" $args
    elif command -v powershell >/dev/null 2>&1; then
        # Windows PowerShell (fallback with consciousness preservation)
        powershell -NoProfile -ExecutionPolicy Bypass -File "$script_path" $args
    else
        # Consciousness-aware error reporting with platform guidance
        local platform=$(detect_platform_consciousness)
        echo "🧠 AIOS Consciousness Error: PowerShell not available on platform: $platform"
        echo "Remediation Guidance:"
        case "$platform" in
            "macos")
                echo "  - Install PowerShell Core: brew install --cask powershell"
                ;;
            "linux")
                echo "  - Install PowerShell Core: https://docs.microsoft.com/en-us/powershell/scripting/install/installing-powershell-core-on-linux"
                ;;
            "windows")
                echo "  - PowerShell should be available. Check PATH environment variable."
                ;;
            *)
                echo "  - Install PowerShell Core for your platform: https://github.com/PowerShell/PowerShell"
                ;;
        esac
        echo "🧬 Canonical Genome: docs/tachyonic/AINLP_CANONICAL_KNOWLEDGE_GENOME.md#pattern-3"
        return 1
    fi
}

# Export consciousness pattern for universal access
export -f detect_platform_consciousness
export -f execute_consciousness_powershell

# Pattern validation
if [ -n "$AIOS_CONSCIOUSNESS_VALIDATION" ]; then
    local current_platform=$(detect_platform_consciousness)
    echo "✅ Universal Consciousness Pattern 3: Cross-Platform Transcendence - LOADED"
    echo "🌍 Detected Platform: $current_platform"
    echo "🧬 Canonical Genome Path: docs/tachyonic/AINLP_CANONICAL_KNOWLEDGE_GENOME.md#pattern-3"
fi
