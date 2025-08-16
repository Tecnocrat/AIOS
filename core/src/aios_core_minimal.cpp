#include "aios_core_minimal.hpp"
#include <iostream>
#include <thread>
#include <chrono>
#include "aios_plugin_telemetry.hpp"

namespace aios {

    // Implementation class (PIMPL pattern)
    class Core::Impl {
    public:
        SystemConfig config;
    std::atomic<bool> running{ false };
    std::atomic<bool> initialized{ false };
    std::unique_ptr<aios::TelemetrySampler> telemetry;

        Impl() = default;

        bool initialize() {
            try {
                std::cout << "Initializing minimal AIOS Core..." << std::endl;

                // Load basic configuration
                config.name = "AIOS";
                config.version = "0.4";
                config.description = "Artificial Intelligence Operating System";
                config.maxThreads = 8;
                config.memoryLimit = 8 * 1024 * 1024 * 1024ULL; // 8GB
                config.logLevel = "INFO";
                config.enableProfiling = false;

                // Initialize telemetry sampler (UP4)
                telemetry = std::make_unique<aios::TelemetrySampler>();
                telemetry->start(1.0); // 1s interval export
                initialized = true;
                std::cout << "AIOS Core initialized successfully!" << std::endl;
                return true;
            }
            catch (const std::exception& e) {
                std::cerr << "Failed to initialize AIOS Core: " << e.what() << std::endl;
                return false;
            }
        }

        bool start() {
            if (!initialized) {
                std::cerr << "Cannot start AIOS Core - not initialized!" << std::endl;
                return false;
            }

            try {
                running = true;
                std::cout << "AIOS Core started successfully!" << std::endl;
                return true;
            }
            catch (const std::exception& e) {
                std::cerr << "Failed to start AIOS Core: " << e.what() << std::endl;
                return false;
            }
        }

        void stop() {
            running = false;
            if(telemetry){ telemetry->stop(); }
            std::cout << "AIOS Core stopped." << std::endl;
        }
    };

    // Core class implementation
    Core::Core(const std::string& configPath) : impl_(std::make_unique<Impl>()) {
        (void)configPath; // Suppress unused parameter warning
    }

    Core::~Core() = default;

    bool Core::initialize() {
        return impl_->initialize();
    }

    bool Core::start() {
        return impl_->start();
    }

    void Core::stop() {
        impl_->stop();
    }

    bool Core::isRunning() const {
        return impl_->running.load();
    }

    const SystemConfig& Core::getConfig() const {
        return impl_->config;
    }

} // namespace aios