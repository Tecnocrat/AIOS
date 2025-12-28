# AIOS Core Source Components
# This file builds the basic core components in src/

# Core source files
set(CORE_SOURCES
    aios_core_minimal.cpp
    aios_plugin_telemetry.cpp
    bmssp.cpp
    image_io.cpp
    kernel_ops_wrapper.cpp
    lattice_space.cpp
    tachyonic_surface.cpp
    tensorflow_performance_cell.cpp
)

# Create a static library for core components
add_library(aios_core_lib STATIC ${CORE_SOURCES})

# Include directories for this library
target_include_directories(aios_core_lib PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${CMAKE_SOURCE_DIR}/include
)

# Platform-specific settings
if(WIN32)
    target_compile_definitions(aios_core_lib PRIVATE WINDOWS_PLATFORM)
elseif(UNIX)
    target_compile_definitions(aios_core_lib PRIVATE UNIX_PLATFORM)
endif()

# Add threading support
find_package(Threads REQUIRED)
target_link_libraries(aios_core_lib Threads::Threads)

# Link assembly library to core library
target_link_libraries(aios_core_lib aios_asm_lib)

# Add subdirectories if they have their own CMakeLists
if(EXISTS ${CMAKE_CURRENT_SOURCE_DIR}/asm/CMakeLists.txt)
    add_subdirectory(asm)
endif()

if(EXISTS ${CMAKE_CURRENT_SOURCE_DIR}/assembly/CMakeLists.txt)
    add_subdirectory(assembly)
endif()

# Build test executables
if(BUILD_TESTS)
    # Consciousness SIMD processor test
    add_executable(test_consciousness_simd test_consciousness_simd.cpp)
    target_link_libraries(test_consciousness_simd
        aios_core_lib
        Threads::Threads
    )
    target_include_directories(test_consciousness_simd PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}
    )

    # Set test properties
    set_target_properties(test_consciousness_simd PROPERTIES
        RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/tests
    )
endif()