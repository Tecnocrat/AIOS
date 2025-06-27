# filepath: c:\dev\AIOS\orchestrator\CMakeLists.txt
cmake_minimum_required(VERSION 3.10)
project(AIOS_Orchestrator VERSION 0.1)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Gather all sources
file(GLOB KERNEL_SOURCES "src/*.cpp")

include_directories(include)

add_executable(aios_kernel ${KERNEL_SOURCES})

# Optionally, add a library for core modules
# add_library(aio_core src/SingularityCore.cpp src/FractalSyncBus.cpp ...)
# target_link_libraries(aios_kernel aio_core)

add_executable(PluginLoader src/PluginLoader.cpp)
target_link_libraries(PluginLoader PRIVATE nlohmann_json::nlohmann_json)