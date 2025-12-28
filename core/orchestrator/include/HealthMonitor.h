#pragma once
#include <string>

class HealthMonitor {
public:
    void initialize();
    void run();
    std::string getStatus() const;
private:
    bool healthy_ = true;
};