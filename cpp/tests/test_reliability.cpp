#include "reliability.hpp"

#include <cassert>
#include <cmath>
#include <iostream>

int main() {
    SimulationConfig config;
    config.runs = 25;
    config.seed = 7;
    const auto first = simulate(config);
    const auto second = simulate(config);
    assert(first.size() == config.runs);
    assert(first.front().availability == second.front().availability);
    for (const auto& result : first) {
        assert(result.uptime_hours >= 0.0);
        assert(result.downtime_hours >= 0.0);
        assert(std::abs(result.uptime_hours + result.downtime_hours - config.hours) < 1e-9);
        assert(result.availability >= 0.0 && result.availability <= 1.0);
    }
    std::cout << "All reliability model tests passed\n";
}

