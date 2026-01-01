#pragma once
#include "IIPCManager.h"
#include <iostream>
#include <map>
#include <queue>
#include <mutex>
#include <condition_variable>

class IPCManager : public IIPCManager {
public:
    void initialize() override {
        std::cout << "[IPCManager] Initialized." << std::endl;
    }
    void sendMessage(const std::string& channel, const std::string& message) override {
        {
            std::lock_guard<std::mutex> lock(mtx_);
            channels_[channel].push(message);
        }
        cv_.notify_all();
        std::cout << "[IPCManager] Sending on " << channel << ": " << message << std::endl;
    }
    std::string receiveMessage(const std::string& channel) override {
        std::unique_lock<std::mutex> lock(mtx_);
        cv_.wait(lock, [&] { return !channels_[channel].empty(); });
        std::string message = channels_[channel].front();
        channels_[channel].pop();
        std::cout << "[IPCManager] Receiving from " << channel << std::endl;
        return message;
    }

private:
    std::map<std::string, std::queue<std::string>> channels_;
    std::mutex mtx_;
    std::condition_variable cv_;
};