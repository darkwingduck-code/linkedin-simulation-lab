cmake_minimum_required(VERSION 3.20)
project(reliability_simulator VERSION 0.4.0 LANGUAGES CXX)

option(ENABLE_SANITIZERS "Enable AddressSanitizer and UndefinedBehaviorSanitizer" OFF)
option(ENABLE_CLANG_TIDY "Enable clang-tidy static analysis" OFF)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

if(ENABLE_CLANG_TIDY)
    find_program(CLANG_TIDY_EXECUTABLE NAMES clang-tidy REQUIRED)
    set(CMAKE_CXX_CLANG_TIDY
        "${CLANG_TIDY_EXECUTABLE};-checks=bugprone-*,performance-*,portability-*,-bugprone-exception-escape,-bugprone-easily-swappable-parameters;--warnings-as-errors=bugprone-*,performance-*"
    )
endif()

function(configure_reliability_target target)
    if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
        target_compile_options(${target} PRIVATE -Wall -Wextra -Wpedantic -Werror)
        if(ENABLE_SANITIZERS AND NOT WIN32)
            target_compile_options(${target} PRIVATE -fsanitize=address,undefined -fno-omit-frame-pointer)
            target_link_options(${target} PRIVATE -fsanitize=address,undefined)
        endif()
    endif()
endfunction()

add_library(reliability_model cpp/src/reliability.cpp cpp/src/serialization.cpp)
target_include_directories(reliability_model PUBLIC cpp/include)
configure_reliability_target(reliability_model)

add_executable(reliability_simulator cpp/src/main.cpp)
target_link_libraries(reliability_simulator PRIVATE reliability_model)
configure_reliability_target(reliability_simulator)

enable_testing()
add_executable(reliability_tests cpp/tests/test_reliability.cpp)
target_link_libraries(reliability_tests PRIVATE reliability_model)
configure_reliability_target(reliability_tests)

add_test(NAME reliability_model_tests COMMAND reliability_tests)
add_test(
    NAME simulator_named_options
    COMMAND reliability_simulator
        --output ${CMAKE_CURRENT_BINARY_DIR}/named-options.csv
        --json-output ${CMAKE_CURRENT_BINARY_DIR}/named-options.json
        --runs 5 --seed 7 --hours 24 --failure-rate 0.01 --repair-rate 0.2
)
add_test(NAME simulator_rejects_zero_runs COMMAND reliability_simulator --runs 0)
set_tests_properties(simulator_rejects_zero_runs PROPERTIES WILL_FAIL TRUE)
add_test(NAME simulator_rejects_unknown_option COMMAND reliability_simulator --unknown value)
set_tests_properties(simulator_rejects_unknown_option PROPERTIES WILL_FAIL TRUE)

install(TARGETS reliability_simulator RUNTIME DESTINATION bin)
