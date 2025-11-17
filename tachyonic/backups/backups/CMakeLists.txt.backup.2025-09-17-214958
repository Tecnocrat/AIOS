cmake_minimum_required(VERSION 3.16)
project(AIOS_Core)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Include directories
include_directories(include)
include_directories(src)
include_directories(../orchestrator/include)

# Add subdirectories
add_subdirectory(src)

# Include consciousness engine components
include(consciousness.cmake)

# Main executable
add_executable(aios_core
    src/main.cpp
)

# Consciousness test executable
add_executable(consciousness_test
    consciousness_test.cpp
)

# Find threading support
find_package(Threads REQUIRED)

# Link libraries
target_link_libraries(aios_core
    aios_core_lib
    aios_consciousness_engine
    Threads::Threads
)

target_link_libraries(consciousness_test
    aios_core_lib
    aios_consciousness_engine
    Threads::Threads
)

# Platform-specific settings
if(WIN32)
    target_compile_definitions(aios_core PRIVATE WINDOWS_PLATFORM)
elseif(UNIX)
    target_compile_definitions(aios_core PRIVATE UNIX_PLATFORM)
endif()

# Build configuration
if(CMAKE_BUILD_TYPE STREQUAL "Debug")
    target_compile_definitions(aios_core PRIVATE DEBUG_BUILD)
else()
    target_compile_definitions(aios_core PRIVATE RELEASE_BUILD)
endif()

# Installation
install(TARGETS aios_core DESTINATION bin)