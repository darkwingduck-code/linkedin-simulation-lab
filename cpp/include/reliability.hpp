#ifndef RELIABILITY_HPP
#define RELIABILITY_HPP

#include <cstddef>
#include <cstdint>
#include <string>
#include <vector>

struct SimulationConfig {
    std::size_t runs{1000};
    std::uint32_t seed{42};
    double hours{720.0};
    double failure_rate_per_hour{0.0015};
    double repair_rate_per_hour{0.08};
};

struct SimulationResult {
    std::size_t run_id{};
    double uptime_hours{};
    double downtime_hours{};
    std::size_t failures{};
    double availability{};
};

std::vector<SimulationResult> simulate(const SimulationConfig& config);
void write_csv(const std::vector<SimulationResult>& results, const std::string& path);
void write_json(
    const SimulationConfig& config,
    const std::vector<SimulationResult>& results,
    const std::string& path
);

#endif  // RELIABILITY_HPP
