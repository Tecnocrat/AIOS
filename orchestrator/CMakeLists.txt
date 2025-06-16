cmake_minimum_required(VERSION 3.10)

# Project name and version
project(AIOS_Orchestrator VERSION 0.1)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Enable debugging symbols
set(CMAKE_BUILD_TYPE Debug)

# Add source files
add_executable(hello_aios src/main.cpp)

# Include debugging flags
if(CMAKE_BUILD_TYPE STREQUAL "Debug")
    target_compile_options(hello_aios PRIVATE -g)
endif()