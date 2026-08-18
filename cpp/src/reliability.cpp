#include "reliability.hpp"

#include <algorithm>
#include <filesystem>
#include <fstream>
#include <iomanip>
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

void write_csv(const std::vector<SimulationResult>& results, const std::string& path) {
    const std::filesystem::path output(path);
    if (output.has_parent_path()) std::filesystem::create_directories(output.parent_path());
    std::ofstream stream(output);
    if (!stream) throw std::runtime_error("could not open output file: " + path);
    stream << "run_id,uptime_hours,downtime_hours,failures,availability\n";
    stream << std::fixed << std::setprecision(6);
    for (const auto& row : results) {
        stream << row.run_id << ',' << row.uptime_hours << ',' << row.downtime_hours << ','
               << row.failures << ',' << row.availability << '\n';
    }
}

