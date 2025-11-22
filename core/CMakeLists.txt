cmake_minimum_required(VERSION 3.20)

# Set vcpkg toolchain if available
if(EXISTS "C:/dev/vcpkg/scripts/buildsystems/vcpkg.cmake")
    set(CMAKE_TOOLCHAIN_FILE "C:/dev/vcpkg/scripts/buildsystems/vcpkg.cmake")
endif()

project(AIOS_Core VERSION 1.0.0 LANGUAGES CXX)

# Set C++ standard
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Set build type if not specified
if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release)
endif()

# Compiler-specific options
if(MSVC)
    # Need MASM for kernel ops regardless of tachyonic surface toggle
    enable_language(ASM_MASM)
    add_compile_definitions(_CRT_SECURE_NO_WARNINGS)
endif()

# ============================================================================
# AINLP Pattern: phase11-day2.optional-dependencies
# Make Boost optional for DLL-only builds (consciousness engine is self-contained)
# ============================================================================

# Find packages (make Boost optional for minimal build)
find_package(Boost QUIET COMPONENTS system filesystem thread)
if(Boost_FOUND)
    message(STATUS "Boost found: ${Boost_VERSION}")
    set(AIOS_HAS_BOOST TRUE)
else()
    message(WARNING "Boost not found - some features will be disabled")
    set(AIOS_HAS_BOOST FALSE)
endif()

find_package(nlohmann_json QUIET)
if(nlohmann_json_FOUND)
    message(STATUS "nlohmann_json found")
    set(AIOS_HAS_JSON TRUE)
else()
    message(WARNING "nlohmann_json not found - using fallback JSON handling")
    set(AIOS_HAS_JSON FALSE)
endif()

# Find Python for TensorFlow integration (optional for now)
find_package(Python3 QUIET COMPONENTS Development NumPy)

# Optional: TensorFlow C++ (if available)
# find_package(TensorFlow QUIET)
# For now, we'll use TensorFlow C++ through pkg-config
find_package(PkgConfig QUIET)
if(PkgConfig_FOUND)
    pkg_check_modules(TENSORFLOW tensorflow)
endif()

# Use built-in JSON handling for now
set(JSON_FOUND TRUE)

# Include directories
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/include)
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/orchestrator/include)
if(AIOS_HAS_BOOST)
    include_directories(${Boost_INCLUDE_DIRS})
endif()

# Source files
file(GLOB_RECURSE SOURCES "src/*.cpp" "src/*.cxx")
file(GLOB_RECURSE HEADERS "include/*.h" "include/*.hpp")

# For Day 2: Use minimal consciousness engine stub instead of full orchestrator
# (Full orchestrator has C++20 concepts issues that need separate fixing)
# Add orchestrator sources later when C++20 compiler fully configured
# file(GLOB ORCHESTRATOR_SOURCES "orchestrator/src/*.cpp")
# list(APPEND SOURCES ${ORCHESTRATOR_SOURCES})

# Exclude test/main files
list(REMOVE_ITEM SOURCES "${CMAKE_CURRENT_SOURCE_DIR}/src/aios_core.cpp")
list(REMOVE_ITEM SOURCES "${CMAKE_CURRENT_SOURCE_DIR}/src/universal_quantum_holographic.cpp")
list(REMOVE_ITEM SOURCES "${CMAKE_CURRENT_SOURCE_DIR}/src/tachyonic_surface_viewer_main.cpp")
list(REMOVE_ITEM SOURCES "${CMAKE_CURRENT_SOURCE_DIR}/src/main.cpp")
# Exclude files with ASM dependencies (Day 2 minimal build)
list(REMOVE_ITEM SOURCES "${CMAKE_CURRENT_SOURCE_DIR}/src/aios_core_minimal.cpp")
list(REMOVE_ITEM SOURCES "${CMAKE_CURRENT_SOURCE_DIR}/src/test_consciousness_simd.cpp")
list(REMOVE_ITEM SOURCES "${CMAKE_CURRENT_SOURCE_DIR}/src/kernel_ops_wrapper.cpp")
list(REMOVE_ITEM SOURCES "${CMAKE_CURRENT_SOURCE_DIR}/orchestrator/src/main.cpp")

option(AIOS_TACHYONIC_ASM "Enable MASM optimized tachyonic renderer" OFF)
option(AIOS_KERNEL_ASM "Enable kernel_ops ASM optimizations" OFF)

# Optional assembly sources (Windows/MSVC only, opt-in)
set(ASM_SOURCES)
if(MSVC)
    # Kernel ops assembly (opt-in due to build complexity)
    if(AIOS_KERNEL_ASM AND EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/src/asm/kernel_ops.asm")
        message(STATUS "Kernel ASM optimizations ENABLED")
        list(APPEND ASM_SOURCES ${CMAKE_CURRENT_SOURCE_DIR}/src/asm/kernel_ops.asm)
        add_compile_definitions(AIOS_KERNEL_ASM)
    else()
        message(STATUS "Kernel ASM optimizations DISABLED (using C++ fallback)")
    endif()
    
    if(AIOS_TACHYONIC_ASM AND EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/src/asm/tachyonic_surface.asm")
        message(STATUS "Tachyonic ASM renderer ENABLED")
        list(APPEND ASM_SOURCES ${CMAKE_CURRENT_SOURCE_DIR}/src/asm/tachyonic_surface.asm)
        add_compile_definitions(AIOS_TACHYONIC_ASM)
    else()
        message(STATUS "Tachyonic ASM renderer DISABLED (using C++ fallback)")
        if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/src/asm/tachyonic_surface.asm")
            set_source_files_properties(${CMAKE_CURRENT_SOURCE_DIR}/src/asm/tachyonic_surface.asm PROPERTIES HEADER_FILE_ONLY TRUE EXCLUDE_FROM_ALL TRUE)
        endif()
    endif()
endif()

# ============================================================================
# AINLP Pattern: phase11-day2.cpp-dll-integration
# Create SHARED library for Python/C# interop (Day 2 - C++ Core Integration)
# ============================================================================

# Create the main library as SHARED (DLL on Windows)
add_library(aios_core SHARED ${SOURCES} ${HEADERS} ${ASM_SOURCES})
target_include_directories(aios_core PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include)

# Define DLL export macro
target_compile_definitions(aios_core PRIVATE AIOS_CORE_EXPORTS)

# Set DLL output properties
set_target_properties(aios_core PROPERTIES
    VERSION ${PROJECT_VERSION}
    SOVERSION 1
    OUTPUT_NAME "aios_core"
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin"
    LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/lib"
    ARCHIVE_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/lib"
)

# Link libraries (conditionally based on what's available)
if(AIOS_HAS_BOOST)
    target_link_libraries(aios_core ${Boost_LIBRARIES})
    target_compile_definitions(aios_core PRIVATE AIOS_HAS_BOOST)
endif()

if(AIOS_HAS_JSON)
    target_link_libraries(aios_core nlohmann_json::nlohmann_json)
    target_compile_definitions(aios_core PRIVATE AIOS_HAS_JSON)
endif()

# Apply compile options only to C++ sources (avoid leaking to MASM)
if(MSVC)
    # /W4 for high warning level, but don't treat warnings as errors (/WX removed for Day 2 build)
    target_compile_options(aios_core PRIVATE $<$<COMPILE_LANGUAGE:CXX>:/W4>)
else()
    target_compile_options(aios_core PRIVATE $<$<COMPILE_LANGUAGE:CXX>:-Wall -Wextra -Wpedantic -Werror>)
endif()

# Optional Python linking
if(Python3_FOUND)
    target_link_libraries(aios_core Python3::Python)
    if(Python3_NumPy_FOUND)
        target_link_libraries(aios_core Python3::NumPy)
    endif()
    target_compile_definitions(aios_core PRIVATE AIOS_PYTHON_ENABLED)
endif()

# Optional TensorFlow linking
if(TensorFlow_FOUND)
    target_link_libraries(aios_core ${TensorFlow_LIBRARIES})
    target_compile_definitions(aios_core PRIVATE AIOS_TENSORFLOW_ENABLED)
endif()

# If TensorFlow found via pkg-config
if(TENSORFLOW_FOUND)
    target_include_directories(aios_core PRIVATE ${TENSORFLOW_INCLUDE_DIRS})
    target_link_libraries(aios_core ${TENSORFLOW_LIBRARIES})
    target_compile_definitions(aios_core PRIVATE AIOS_TENSORFLOW_ENABLED)
endif()

# Create executable(s)
add_executable(aios_main src/main.cpp)
target_link_libraries(aios_main aios_core)

# Tachyonic surface viewer (experimental) - only if JSON available
if(AIOS_HAS_JSON)
    add_executable(aios_tachyonic_viewer src/tachyonic_surface_viewer_main.cpp)
    target_link_libraries(aios_tachyonic_viewer aios_core nlohmann_json::nlohmann_json)
    if(MSVC AND AIOS_TACHYONIC_ASM)
        target_compile_definitions(aios_tachyonic_viewer PRIVATE AIOS_TACHYONIC_ASM)
    endif()
    set(ADDITIONAL_TARGETS aios_tachyonic_viewer)
else()
    set(ADDITIONAL_TARGETS "")
    message(STATUS "aios_tachyonic_viewer skipped (requires nlohmann_json)")
endif()

# Set output directories
set_target_properties(aios_core aios_main ${ADDITIONAL_TARGETS} PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin
    LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib
    ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib
)

# Install targets (conditionally based on what was built)
if(AIOS_HAS_JSON)
    install(TARGETS aios_core aios_main aios_tachyonic_viewer
        RUNTIME DESTINATION bin
        LIBRARY DESTINATION lib
        ARCHIVE DESTINATION lib
    )
else()
    install(TARGETS aios_core aios_main
        RUNTIME DESTINATION bin
        LIBRARY DESTINATION lib
        ARCHIVE DESTINATION lib
    )
endif()

# Install headers
install(DIRECTORY include/ DESTINATION include)

# Testing
enable_testing()
if (EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/tests/CMakeLists.txt")
    add_subdirectory(tests)
else()
    message(STATUS "Skipping tests: ${CMAKE_CURRENT_SOURCE_DIR}/tests/CMakeLists.txt not found")
endif()

# Documentation
find_package(Doxygen)
if(DOXYGEN_FOUND)
    configure_file(${CMAKE_CURRENT_SOURCE_DIR}/docs/Doxyfile.in
                   ${CMAKE_CURRENT_BINARY_DIR}/Doxyfile @ONLY)
    add_custom_target(docs
        ${DOXYGEN_EXECUTABLE} ${CMAKE_CURRENT_BINARY_DIR}/Doxyfile
        WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
        COMMENT "Generating API documentation with Doxygen"
        VERBATIM
    )
endif()

# Print configuration summary
message(STATUS "AIOS Core Configuration:")
message(STATUS "  Build Type: ${CMAKE_BUILD_TYPE}")
message(STATUS "  C++ Standard: ${CMAKE_CXX_STANDARD}")
message(STATUS "  Boost Version: ${Boost_VERSION}")
message(STATUS "  OpenCV Version: ${OpenCV_VERSION}")
message(STATUS "  TensorFlow: ${TensorFlow_FOUND}")
message(STATUS "  Install Prefix: ${CMAKE_INSTALL_PREFIX}")
