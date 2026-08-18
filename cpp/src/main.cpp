#include "reliability.hpp"

#include <cstdlib>
#include <iostream>
#include <stdexcept>
#include <string>

int main(int argc, char* argv[]) {
    try {
        SimulationConfig config;
        std::string output = "artifacts/simulation.csv";
        if (argc > 1) output = argv[1];
        if (argc > 2) config.runs = std::stoull(argv[2]);
        if (argc > 3) config.seed = static_cast<std::uint32_t>(std::stoul(argv[3]));

        const auto results = simulate(config);
        write_csv(results, output);
        std::cout << "Generated " << results.size() << " runs at " << output << '\n';
        return EXIT_SUCCESS;
    } catch (const std::exception& error) {
        std::cerr << "Simulation failed: " << error.what() << '\n';
        return EXIT_FAILURE;
    }
}

