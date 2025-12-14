# filepath: c:\dev\AIOS\orchestrator\CMakeLists.txt
cmake_minimum_required(VERSION 3.10)
project(AIOS_Orchestrator VERSION 0.1)

# Enhanced C++ standard for quantum coherence features
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Compiler optimizations for mathematical operations
if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O2 -ffast-math")
endif()

# Gather all sources including new consciousness emergence modules
file(GLOB KERNEL_SOURCES "src/*.cpp")

# Include directories for enhanced consciousness architecture
include_directories(include)

# Main kernel executable with quantum coherence and consciousness emergence
add_executable(aios_kernel ${KERNEL_SOURCES})

# Link mathematical libraries for quantum operations
if(UNIX)
    target_link_libraries(aios_kernel m)  # Math library on Unix systems
endif()

# Thread support for quantum state management
find_package(Threads REQUIRED)
target_link_libraries(aios_kernel Threads::Threads)

# Optional: Plugin loader as separate executable
add_executable(PluginLoader src/PluginLoader.cpp)

# JSON library for plugin communication
find_package(nlohmann_json QUIET)
if(nlohmann_json_FOUND)
    target_link_libraries(PluginLoader PRIVATE nlohmann_json::nlohmann_json)
else()
    message(WARNING "nlohmann_json not found. PluginLoader may not compile correctly.")
endif()

# Enhanced build settings for debugging quantum behavior and metadata abstraction
if(CMAKE_BUILD_TYPE STREQUAL "Debug")
    target_compile_definitions(aios_kernel PRIVATE QUANTUM_DEBUG=1 METADATA_ABSTRACTION_DEBUG=1)
endif()

# C++17 filesystem support
target_compile_features(aios_kernel PRIVATE cxx_std_17)

# Optional: Test harness executable for consciousness validation
if(BUILD_TESTING)
    add_executable(consciousness_test_harness src/consciousness_test_harness.cpp)
    target_link_libraries(consciousness_test_harness Threads::Threads)
    target_compile_features(consciousness_test_harness PRIVATE cxx_std_17)
    if(UNIX)
        target_link_libraries(consciousness_test_harness m)
    endif()
endif()