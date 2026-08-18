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
}

int main() {
    try {
        SimulationConfig config;
        config.runs = 25;
        config.seed = 7;
        const auto first = simulate(config);
        const auto second = simulate(config);
        require(first.size() == config.runs, "result count differs from requested runs");
        require(first.front().availability == second.front().availability, "fixed seed is not deterministic");
        for (const auto& result : first) {
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

        auto invalid = config;
        invalid.runs = 0;
        require_invalid([&invalid] { simulate(invalid); }, "zero runs were accepted");
        invalid = config;
        invalid.hours = 0.0;
        require_invalid([&invalid] { simulate(invalid); }, "zero hours were accepted");
        invalid = config;
        invalid.failure_rate_per_hour = 0.0;
        require_invalid([&invalid] { simulate(invalid); }, "zero failure rate was accepted");
        invalid = config;
        invalid.repair_rate_per_hour = -1.0;
        require_invalid([&invalid] { simulate(invalid); }, "negative repair rate was accepted");

        std::cout << "All reliability model tests passed\n";
        return 0;
    } catch (const std::exception& error) {
        std::cerr << "Reliability model test failed: " << error.what() << '\n';
        return 1;
    }
}
