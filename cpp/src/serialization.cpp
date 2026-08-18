#include "reliability.hpp"

#include <filesystem>
#include <fstream>
#include <iomanip>
#include <stdexcept>

namespace {
std::ofstream open_output(const std::string& path) {
    const std::filesystem::path output(path);
    if (output.has_parent_path()) std::filesystem::create_directories(output.parent_path());
    std::ofstream stream(output);
    if (!stream) throw std::runtime_error("could not open output file: " + path);
    return stream;
}
}

void write_csv(const std::vector<SimulationResult>& results, const std::string& path) {
    auto stream = open_output(path);
    stream << "run_id,uptime_hours,downtime_hours,failures,availability\n";
    stream << std::fixed << std::setprecision(6);
    for (const auto& row : results) {
        stream << row.run_id << ',' << row.uptime_hours << ',' << row.downtime_hours << ','
               << row.failures << ',' << row.availability << '\n';
    }
}

void write_json(
    const SimulationConfig& config,
    const std::vector<SimulationResult>& results,
    const std::string& path
) {
    auto stream = open_output(path);
    stream << std::fixed << std::setprecision(6);
    stream << "{\n"
           << "  \"schema_version\": \"1.0\",\n"
           << "  \"config\": {\n"
           << "    \"runs\": " << config.runs << ",\n"
           << "    \"seed\": " << config.seed << ",\n"
           << "    \"hours\": " << config.hours << ",\n"
           << "    \"failure_rate_per_hour\": " << config.failure_rate_per_hour << ",\n"
           << "    \"repair_rate_per_hour\": " << config.repair_rate_per_hour << "\n"
           << "  },\n"
           << "  \"results\": [\n";
    for (std::size_t index = 0; index < results.size(); ++index) {
        const auto& row = results[index];
        stream << "    {\"run_id\": " << row.run_id
               << ", \"uptime_hours\": " << row.uptime_hours
               << ", \"downtime_hours\": " << row.downtime_hours
               << ", \"failures\": " << row.failures
               << ", \"availability\": " << row.availability << '}';
        if (index + 1 != results.size()) stream << ',';
        stream << '\n';
    }
    stream << "  ]\n}\n";
}
