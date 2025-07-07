cmake_minimum_required(VERSION 3.20)

# Simple test executable
add_executable(test_core test_core.cpp)
target_link_libraries(test_core aios_core)

# Add test
add_test(NAME CoreTest COMMAND test_core)
