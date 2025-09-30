# Assembly components for AIOS Core
# Builds consciousness SIMD processor and related assembly functions

# For now, use precompiled object files
# TODO: Fix CMake assembly compilation
set(ASM_OBJECTS
    ${CMAKE_CURRENT_SOURCE_DIR}/consciousness_simd_processor.obj
)

# Create assembly object library from precompiled objects
add_library(aios_asm_lib STATIC ${ASM_OBJECTS})

# Set properties
set_target_properties(aios_asm_lib PROPERTIES
    LINKER_LANGUAGE CXX
)