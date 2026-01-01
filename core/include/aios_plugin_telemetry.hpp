// AIOS Core Telemetry Plugin Interface (UP4)
#ifndef AIOS_PLUGIN_TELEMETRY_HPP
#define AIOS_PLUGIN_TELEMETRY_HPP

#include <string>
#include <memory>
#include <vector>
#include <cstdint>
#include <functional>

namespace aios {

struct CoreMetricSample {
    double timestamp_sec{0};
    uint64_t sequence{0};
    double process_cpu_pct{-1};
    double process_mem_mb{-1};
    double frame_time_ms{-1};
    double avg_frame_time_ms{-1};
};

class ITelemetrySink {
public:
    virtual ~ITelemetrySink() = default;
    virtual void on_sample(const CoreMetricSample& sample) = 0;
};

class TelemetryBus {
public:
    static TelemetryBus& instance();
    void register_sink(std::shared_ptr<ITelemetrySink> sink);
    void publish(const CoreMetricSample& sample);
private:
    TelemetryBus() = default;
    std::vector<std::shared_ptr<ITelemetrySink>> sinks_;
};

class JsonFileTelemetrySink : public ITelemetrySink {
public:
    explicit JsonFileTelemetrySink(const std::string& root_dir, size_t flush_every=1);
    void on_sample(const CoreMetricSample& sample) override;
    ~JsonFileTelemetrySink();
private:
    std::string dir_;
    size_t flush_every_{1};
    size_t pending_{0};
    std::vector<CoreMetricSample> buffer_;
    void flush();
};

class TelemetrySampler {
public:
    TelemetrySampler();
    ~TelemetrySampler();
    void start(double interval_sec = 1.0);
    void stop();
    void record_frame(double frame_time_ms);
private:
    struct Impl; std::unique_ptr<Impl> impl_;
};

} // namespace aios

#endif // AIOS_PLUGIN_TELEMETRY_HPP
