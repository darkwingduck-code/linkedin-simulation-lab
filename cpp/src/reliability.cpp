#include "reliability.hpp"

#include <algorithm>
#include <random>
#include <stdexcept>

std::vector<SimulationResult> simulate(const SimulationConfig& config) {
    if (config.runs == 0 || config.hours <= 0.0 ||
        config.failure_rate_per_hour <= 0.0 || config.repair_rate_per_hour <= 0.0) {
        throw std::invalid_argument("all simulation parameters must be positive");
    }

    std::mt19937 generator(config.seed);
    std::exponential_distribution<double> time_to_failure(config.failure_rate_per_hour);
    std::exponential_distribution<double> time_to_repair(config.repair_rate_per_hour);
    std::vector<SimulationResult> results;
    results.reserve(config.runs);

    for (std::size_t run = 1; run <= config.runs; ++run) {
        double clock = 0.0;
        double downtime = 0.0;
        std::size_t failures = 0;

        while (clock < config.hours) {
            clock += time_to_failure(generator);
            if (clock >= config.hours) break;
            ++failures;
            const double repair = std::min(time_to_repair(generator), config.hours - clock);
            downtime += repair;
            clock += repair;
        }

        const double uptime = config.hours - downtime;
        results.push_back({run, uptime, downtime, failures, uptime / config.hours});
    }
    return results;
}
