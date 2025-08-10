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
    # Enable MASM assembly on MSVC toolchain
    enable_language(ASM_MASM)
    add_compile_definitions(_CRT_SECURE_NO_WARNINGS)
endif()

# Find required packages
find_package(Boost REQUIRED COMPONENTS system filesystem thread)
find_package(nlohmann_json REQUIRED)

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
include_directories(${Boost_INCLUDE_DIRS})

# Source files
file(GLOB_RECURSE SOURCES "src/*.cpp" "src/*.cxx")
file(GLOB_RECURSE HEADERS "include/*.h" "include/*.hpp")

# Exclude the original problematic core files for now, use minimal version
list(REMOVE_ITEM SOURCES "${CMAKE_CURRENT_SOURCE_DIR}/src/aios_core.cpp")
list(REMOVE_ITEM SOURCES "${CMAKE_CURRENT_SOURCE_DIR}/src/universal_quantum_holographic.cpp")

# Optional assembly sources (Windows/MSVC only)
set(ASM_SOURCES)
if(MSVC)
    list(APPEND ASM_SOURCES ${CMAKE_CURRENT_SOURCE_DIR}/src/asm/kernel_ops.asm)
endif()

# Create the main library
add_library(aios_core ${SOURCES} ${HEADERS} ${ASM_SOURCES})

# Link libraries
target_link_libraries(aios_core
    ${Boost_LIBRARIES}
    nlohmann_json::nlohmann_json
)

# Apply compile options only to C++ sources (avoid leaking to MASM)
if(MSVC)
    target_compile_options(aios_core PRIVATE $<$<COMPILE_LANGUAGE:CXX>:/W4 /WX>)
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

# Create executable
add_executable(aios_main src/main.cpp)
target_link_libraries(aios_main aios_core)

# Set output directories
set_target_properties(aios_core aios_main PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin
    LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib
    ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib
)

# Install targets
install(TARGETS aios_core aios_main
    RUNTIME DESTINATION bin
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
)

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
