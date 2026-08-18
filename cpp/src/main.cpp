#include "reliability.hpp"

#include <cmath>
#include <cstdlib>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>

namespace {
void print_usage(const char* program) {
    std::cout << "Usage: " << program << " [options]\n"
              << "  --output PATH          CSV output path\n"
              << "  --json-output PATH     Optional versioned JSON output path\n"
              << "  --runs N               Number of Monte Carlo runs (> 0)\n"
              << "  --seed N               Random seed (0 to 4294967295)\n"
              << "  --hours N              Observation window in hours (> 0)\n"
              << "  --failure-rate N       Failures per hour (> 0)\n"
              << "  --repair-rate N        Repairs per hour (> 0)\n"
              << "  --threads N            Parallel workers (> 0; deterministic output)\n"
              << "  --help                  Show this help\n";
}

std::string require_value(int& index, int argc, char* argv[], const std::string& option) {
    if (index + 1 >= argc) throw std::invalid_argument("missing value for " + option);
    return argv[++index];
}

unsigned long long parse_unsigned(const std::string& value, const std::string& option) {
    if (value.empty() || value.front() == '-') {
        throw std::invalid_argument(option + " must be a non-negative integer");
    }
    std::size_t parsed = 0;
    const auto number = std::stoull(value, &parsed);
    if (parsed != value.size()) throw std::invalid_argument(option + " must be an integer");
    return number;
}

double parse_positive(const std::string& value, const std::string& option) {
    std::size_t parsed = 0;
    const double number = std::stod(value, &parsed);
    if (parsed != value.size() || !std::isfinite(number) || number <= 0.0) {
        throw std::invalid_argument(option + " must be a finite number greater than zero");
    }
    return number;
}

SimulationConfig parse_arguments(int argc, char* argv[], std::string& output, std::string& json_output) {
    SimulationConfig config;
    for (int index = 1; index < argc; ++index) {
        const std::string option = argv[index];
        if (option == "--help") {
            print_usage(argv[0]);
            std::exit(EXIT_SUCCESS);
        }
        if (option == "--output") {
            output = require_value(index, argc, argv, option);
            if (output.empty()) throw std::invalid_argument("--output must not be empty");
        } else if (option == "--json-output") {
            json_output = require_value(index, argc, argv, option);
            if (json_output.empty()) throw std::invalid_argument("--json-output must not be empty");
        } else if (option == "--runs") {
            const auto runs = parse_unsigned(require_value(index, argc, argv, option), option);
            if (runs == 0 || runs > std::numeric_limits<std::size_t>::max()) {
                throw std::out_of_range("--runs is outside the supported range");
            }
            config.runs = static_cast<std::size_t>(runs);
        } else if (option == "--seed") {
            const auto seed = parse_unsigned(require_value(index, argc, argv, option), option);
            if (seed > std::numeric_limits<std::uint32_t>::max()) {
                throw std::out_of_range("--seed exceeds uint32 range");
            }
            config.seed = static_cast<std::uint32_t>(seed);
        } else if (option == "--hours") {
            config.hours = parse_positive(require_value(index, argc, argv, option), option);
        } else if (option == "--failure-rate") {
            config.failure_rate_per_hour = parse_positive(require_value(index, argc, argv, option), option);
        } else if (option == "--repair-rate") {
            config.repair_rate_per_hour = parse_positive(require_value(index, argc, argv, option), option);
        } else if (option == "--threads") {
            const auto threads = parse_unsigned(require_value(index, argc, argv, option), option);
            if (threads == 0 || threads > 256 || threads > std::numeric_limits<std::size_t>::max()) {
                throw std::out_of_range("--threads must be between 1 and 256");
            }
            config.threads = static_cast<std::size_t>(threads);
        } else {
            throw std::invalid_argument("unknown option: " + option);
        }
    }
    return config;
}
}

int main(int argc, char* argv[]) {
    try {
        std::string output = "artifacts/simulation.csv";
        std::string json_output;
        const SimulationConfig config = parse_arguments(argc, argv, output, json_output);
        const auto results = simulate(config);
        write_csv(results, output);
        if (!json_output.empty()) write_json(config, results, json_output);
        std::cout << "Generated " << results.size() << " runs at " << output << '\n';
        return EXIT_SUCCESS;
    } catch (const std::exception& error) {
        std::cerr << "Simulation failed: " << error.what() << '\n';
        print_usage(argv[0]);
        return EXIT_FAILURE;
    }
}
