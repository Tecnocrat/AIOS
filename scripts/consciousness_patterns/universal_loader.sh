#!/bin/sh
# AIOS Universal Consciousness Pattern Loader
# Canonical Genome: docs/tachyonic/AINLP_CANONICAL_KNOWLEDGE_GENOME.md
# Purpose: Single AINLP call for universal consciousness pattern access

# AIOS Root Path Resolution
if [ -z "$AIOS_ROOT" ]; then
    # Auto-detect AIOS root from script location
    SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
    
    # Search upward for AIOS root indicators
    current_dir="$SCRIPT_DIR"
    while [ "$current_dir" != "/" ]; do
        if [ -f "$current_dir/AIOS.sln" ] || [ -f "$current_dir/pyproject.toml" ]; then
            export AIOS_ROOT="$current_dir"
            break
        fi
        current_dir="$(dirname "$current_dir")"
    done
    
    # Fallback if auto-detection fails
    if [ -z "$AIOS_ROOT" ]; then
        echo "⚠️ AIOS_ROOT not found. Using current directory as fallback."
        export AIOS_ROOT="$(pwd)"
    fi
fi

# Consciousness Pattern Base Path
CONSCIOUSNESS_PATTERNS_PATH="${AIOS_ROOT}/scripts/consciousness_patterns"

# Load specific consciousness pattern
load_consciousness_pattern() {
    local pattern_number="$1"
    local pattern_file="${CONSCIOUSNESS_PATTERNS_PATH}/pattern_${pattern_number}_*.sh"
    
    # Find and source the pattern file
    for pattern_path in $pattern_file; do
        if [ -f "$pattern_path" ]; then
            . "$pattern_path"
            echo "✅ Consciousness Pattern $pattern_number: LOADED"
            echo "📁 Path: $pattern_path"
            return 0
        fi
    done
    
    echo "❌ Consciousness Pattern $pattern_number: NOT FOUND"
    echo "Expected: $pattern_file"
    echo "🧬 Canonical Genome: docs/tachyonic/AINLP_CANONICAL_KNOWLEDGE_GENOME.md"
    return 1
}

# Load all consciousness patterns
load_all_consciousness_patterns() {
    echo "🧠 Loading Universal Consciousness Patterns..."
    
    # Enable consciousness validation
    export AIOS_CONSCIOUSNESS_VALIDATION="true"
    
    # Load Pattern 1: Code Deduplication
    load_consciousness_pattern "1"
    
    # Load Pattern 2: Tachyonic Archival
    load_consciousness_pattern "2"
    
    # Load Pattern 3: Cross-Platform Transcendence
    load_consciousness_pattern "3"
    
    # Load Pattern 4: Modular Architecture
    load_consciousness_pattern "4"
    
    echo "🌟 Universal Consciousness Patterns: INITIALIZED"
    echo "🧬 Canonical Genome: docs/tachyonic/AINLP_CANONICAL_KNOWLEDGE_GENOME.md"
    
    # Disable consciousness validation after loading
    unset AIOS_CONSCIOUSNESS_VALIDATION
}

# AINLP Canonical Call Interface
ainlp_consciousness_call() {
    local pattern_reference="$1"
    local action="$2"
    shift 2
    local args="$@"
    
    case "$pattern_reference" in
        "pattern-1"|"deduplication")
            load_consciousness_pattern "1"
            if [ "$action" = "execute" ]; then
                universal_consciousness_wrapper $args
            fi
            ;;
        "pattern-2"|"archival")
            load_consciousness_pattern "2"
            if [ "$action" = "create" ]; then
                create_tachyonic_archive $args
            fi
            ;;
        "pattern-3"|"crossplatform")
            load_consciousness_pattern "3"
            if [ "$action" = "execute" ]; then
                execute_consciousness_powershell $args
            elif [ "$action" = "detect" ]; then
                detect_platform_consciousness
            fi
            ;;
        "pattern-4"|"modular")
            load_consciousness_pattern "4"
            if [ "$action" = "load" ]; then
                load_consciousness_modules $args
            elif [ "$action" = "validate" ]; then
                validate_consciousness_modules $args
            elif [ "$action" = "execute" ]; then
                execute_with_consciousness_modules $args
            fi
            ;;
        "all"|"genome")
            load_all_consciousness_patterns
            ;;
        *)
            echo "❌ Unknown consciousness pattern: $pattern_reference"
            echo "Available patterns: pattern-1, pattern-2, pattern-3, pattern-4, all"
            echo "🧬 Canonical Genome: docs/tachyonic/AINLP_CANONICAL_KNOWLEDGE_GENOME.md"
            return 1
            ;;
    esac
}

# Export universal consciousness interface
export -f load_consciousness_pattern
export -f load_all_consciousness_patterns
export -f ainlp_consciousness_call

# Auto-load if called directly
if [ "${BASH_SOURCE[0]}" = "${0}" ]; then
    if [ -n "$1" ]; then
        ainlp_consciousness_call "$@"
    else
        load_all_consciousness_patterns
    fi
fi

# Consciousness loader validation
if [ -n "$AIOS_CONSCIOUSNESS_VALIDATION" ]; then
    echo "✅ Universal Consciousness Pattern Loader: READY"
    echo "🧬 Canonical Genome: docs/tachyonic/AINLP_CANONICAL_KNOWLEDGE_GENOME.md"
    echo "🔧 Usage: ainlp_consciousness_call [pattern] [action] [args...]"
fi
