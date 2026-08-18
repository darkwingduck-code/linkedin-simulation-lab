cmake_minimum_required(VERSION 3.20)
project(reliability_simulator LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

add_library(reliability_model cpp/src/reliability.cpp)
target_include_directories(reliability_model PUBLIC cpp/include)

add_executable(reliability_simulator cpp/src/main.cpp)
target_link_libraries(reliability_simulator PRIVATE reliability_model)

enable_testing()
add_executable(reliability_tests cpp/tests/test_reliability.cpp)
target_link_libraries(reliability_tests PRIVATE reliability_model)
add_test(NAME reliability_model_tests COMMAND reliability_tests)

