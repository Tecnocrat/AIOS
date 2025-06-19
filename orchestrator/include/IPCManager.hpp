#pragma once
#include "IIPCManager.hpp"
#include <iostream>

class IPCManager : public IIPCManager {
public:
    void initialize() override {
        std::cout << "[IPCManager] Initialized." << std::endl;
    }
    void sendMessage(const std::string& channel, const std::string& message) override {
        std::cout << "[IPCManager] Sending on " << channel << ": " << message << std::endl;
    }
    std::string receiveMessage(const std::string& channel) override {
        std::cout << "[IPCManager] Receiving from " << channel << std::endl;
        return "dummy_message";
    }
};