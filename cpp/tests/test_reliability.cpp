#include "reliability.hpp"

#include <cmath>
#include <iostream>
#include <stdexcept>
#include <string>

namespace {
void require(bool condition, const std::string& message) {
    if (!condition) throw std::runtime_error(message);
}

template <typename Callable>
void require_invalid(Callable callable, const std::string& message) {
    try {
        callable();
    } catch (const std::invalid_argument&) {
        return;
    }
    throw std::runtime_error(message);
}

void verify_invariants(const SimulationConfig& config) {
    const auto results = simulate(config);
    require(results.size() == config.runs, "result count differs from requested runs");
    for (const auto& result : results) {
        require(result.run_id >= 1 && result.run_id <= config.runs, "run_id outside expected range");
        require(std::isfinite(result.uptime_hours), "non-finite uptime");
        require(std::isfinite(result.downtime_hours), "non-finite downtime");
        require(result.uptime_hours >= 0.0, "negative uptime");
        require(result.downtime_hours >= 0.0, "negative downtime");
        require(
            std::abs(result.uptime_hours + result.downtime_hours - config.hours) < 1e-9,
            "uptime and downtime do not equal observation hours"
        );
        require(
            result.availability >= 0.0 && result.availability <= 1.0,
            "availability is outside zero through one"
        );
    }
}
}

int main() {
    try {
        SimulationConfig config;
        config.runs = 25;
        config.seed = 7;
        const auto first = simulate(config);
        const auto second = simulate(config);
        require(first.front().availability == second.front().availability, "fixed seed is not deterministic");
        verify_invariants(config);

        auto parallel_config = config;
        parallel_config.threads = 4;
        const auto parallel = simulate(parallel_config);
        require(first.size() == parallel.size(), "parallel result count differs");
        for (std::size_t index = 0; index < first.size(); ++index) {
            require(first[index].availability == parallel[index].availability,
                    "parallel output differs from serial output");
            require(first[index].failures == parallel[index].failures,
                    "parallel failure count differs from serial output");
        }

        for (std::uint32_t seed = 0; seed < 50; ++seed) {
            SimulationConfig generated;
            generated.runs = 20 + seed % 7;
            generated.seed = seed;
            generated.hours = 24.0 + static_cast<double>(seed);
            generated.failure_rate_per_hour = 0.0005 + static_cast<double>(seed) * 0.0001;
            generated.repair_rate_per_hour = 0.02 + static_cast<double>(seed) * 0.001;
            verify_invariants(generated);
        }

        auto invalid = config;
        invalid.runs = 0;
        require_invalid([&invalid] { simulate(invalid); }, "zero runs were accepted");
        invalid = config;
        invalid.threads = 0;
        require_invalid([&invalid] { simulate(invalid); }, "zero threads were accepted");
        invalid = config;
        invalid.threads = 257;
        require_invalid([&invalid] { simulate(invalid); }, "excessive thread count was accepted");
        invalid = config;
        invalid.hours = 0.0;
        require_invalid([&invalid] { simulate(invalid); }, "zero hours were accepted");
        invalid = config;
        invalid.failure_rate_per_hour = 0.0;
        require_invalid([&invalid] { simulate(invalid); }, "zero failure rate was accepted");
        invalid = config;
        invalid.repair_rate_per_hour = -1.0;
        require_invalid([&invalid] { simulate(invalid); }, "negative repair rate was accepted");

        std::cout << "All reliability model tests passed, including 50 generated configurations\n";
        return 0;
    } catch (const std::exception& error) {
        std::cerr << "Reliability model test failed: " << error.what() << '\n';
        return 1;
    }
}
