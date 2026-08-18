#include "reliability.hpp"

#include <algorithm>
#include <random>
#include <stdexcept>
#include <thread>

namespace {
SimulationResult simulate_one(const SimulationConfig& config, const std::size_t run_index) {
    const auto run_number = static_cast<std::uint64_t>(run_index);
    std::seed_seq seed{config.seed, static_cast<std::uint32_t>(run_number),
                       static_cast<std::uint32_t>(run_number >> 32U)};
    std::mt19937 generator(seed);
    std::exponential_distribution<double> time_to_failure(config.failure_rate_per_hour);
    std::exponential_distribution<double> time_to_repair(config.repair_rate_per_hour);
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
    return {run_index + 1, uptime, downtime, failures, uptime / config.hours};
}
}  // namespace

std::vector<SimulationResult> simulate(const SimulationConfig& config) {
    if (config.runs == 0 || config.hours <= 0.0 ||
        config.failure_rate_per_hour <= 0.0 || config.repair_rate_per_hour <= 0.0) {
        throw std::invalid_argument("all simulation parameters must be positive");
    }
    if (config.threads == 0 || config.threads > 256) {
        throw std::invalid_argument("threads must be between 1 and 256");
    }

    std::vector<SimulationResult> results(config.runs);
    const std::size_t worker_count = std::min(config.threads, config.runs);
    std::vector<std::thread> workers;
    workers.reserve(worker_count);
    try {
        for (std::size_t worker = 0; worker < worker_count; ++worker) {
            workers.emplace_back([&, worker] {
                for (std::size_t run = worker; run < config.runs; run += worker_count) {
                    results[run] = simulate_one(config, run);
                }
            });
        }
    } catch (...) {
        for (auto& worker : workers) worker.join();
        throw;
    }
    for (auto& worker : workers) worker.join();
    return results;
}
