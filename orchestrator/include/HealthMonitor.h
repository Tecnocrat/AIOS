#pragma once
#include "IHealthMonitor.h"
#include <iostream>

class HealthMonitor : public IHealthMonitor {
public:
    void initialize() override {
        std::cout << "[HealthMonitor] Initialized." << std::endl;
    }
    void reportStatus() override {
        std::cout << "[HealthMonitor] System is healthy." << std::endl;
    }
    bool isHealthy() const override {
        return true;
    }
};