cmake_minimum_required(VERSION 3.20)
project(reliability_simulator LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

add_library(reliability_model cpp/src/reliability.cpp)
target_include_directories(reliability_model PUBLIC cpp/include)
if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
    target_compile_options(reliability_model PRIVATE -Wall -Wextra -Wpedantic -Werror)
endif()

add_executable(reliability_simulator cpp/src/main.cpp)
target_link_libraries(reliability_simulator PRIVATE reliability_model)
if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
    target_compile_options(reliability_simulator PRIVATE -Wall -Wextra -Wpedantic -Werror)
endif()

enable_testing()
add_executable(reliability_tests cpp/tests/test_reliability.cpp)
target_link_libraries(reliability_tests PRIVATE reliability_model)
if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
    target_compile_options(reliability_tests PRIVATE -Wall -Wextra -Wpedantic -Werror)
endif()
add_test(NAME reliability_model_tests COMMAND reliability_tests)
add_test(
    NAME simulator_named_options
    COMMAND reliability_simulator
        --output ${CMAKE_CURRENT_BINARY_DIR}/named-options.csv
        --runs 5 --seed 7 --hours 24 --failure-rate 0.01 --repair-rate 0.2
)
add_test(NAME simulator_rejects_zero_runs COMMAND reliability_simulator --runs 0)
set_tests_properties(simulator_rejects_zero_runs PROPERTIES WILL_FAIL TRUE)
add_test(NAME simulator_rejects_unknown_option COMMAND reliability_simulator --unknown value)
set_tests_properties(simulator_rejects_unknown_option PROPERTIES WILL_FAIL TRUE)

