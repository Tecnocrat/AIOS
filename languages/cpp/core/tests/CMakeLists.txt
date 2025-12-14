cmake_minimum_required(VERSION 3.20)

# Simple test executable
add_executable(test_core test_core.cpp)
target_link_libraries(test_core aios_core)

# TensorFlow Performance Cell test
add_executable(test_tensorflow_cell test_tensorflow_cell.cpp)
target_link_libraries(test_tensorflow_cell aios_core)

# Add tests
add_test(NAME CoreTest COMMAND test_core)
add_test(NAME TensorFlowCellTest COMMAND test_tensorflow_cell)
