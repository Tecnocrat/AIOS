cmake_minimum_required(VERSION 3.10)

# Project name and version
project(AIOS_Orchestrator VERSION 0.1)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Add source files for the main program
add_executable(hello_aios src/main.cpp)

# Include debugging flags based on the compiler
if(CMAKE_CXX_COMPILER_ID STREQUAL "MSVC")
    target_compile_options(hello_aios PRIVATE /Zi /Od)
    target_link_options(hello_aios PRIVATE /DEBUG)
elseif(CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
    target_compile_options(hello_aios PRIVATE -g)
endif()

# Add source files for the test executable
add_executable(test_main ../tests/test_main.cpp)

# Include debugging flags for the test executable
if(CMAKE_CXX_COMPILER_ID STREQUAL "MSVC")
    target_compile_options(test_main PRIVATE /Zi /Od)
    target_link_options(test_main PRIVATE /DEBUG)
elseif(CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
    target_compile_options(test_main PRIVATE -g)
endif()