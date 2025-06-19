# filepath: c:\dev\AIOS\orchestrator\CMakeLists.txt
cmake_minimum_required(VERSION 3.10)

# Project name and version
project(AIOS_Orchestrator VERSION 0.1)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Gather all kernel source files (excluding test files)
file(GLOB KERNEL_SOURCES "src/*.cpp")

# Optionally exclude test files if they still exist
list(REMOVE_ITEM KERNEL_SOURCES "${CMAKE_CURRENT_SOURCE_DIR}/src/test_orchestrator.cpp")
list(REMOVE_ITEM KERNEL_SOURCES "${CMAKE_CURRENT_SOURCE_DIR}/src/test_main.cpp")

# Include the headers directory
include_directories(include)

# Define the main orchestrator executable
add_executable(orchestrator ${KERNEL_SOURCES})

# Debugging flags (optional, for MSVC and GNU)
if(CMAKE_CXX_COMPILER_ID STREQUAL "MSVC")
    target_compile_options(orchestrator PRIVATE /Zi /Od)
    target_link_options(orchestrator PRIVATE /DEBUG)
elseif(CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
    target_compile_options(orchestrator PRIVATE -g)
endif()