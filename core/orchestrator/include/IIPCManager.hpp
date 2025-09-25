#pragma once
#include <string>

class IIPCManager {
public:
    virtual ~IIPCManager() = default;
    virtual void initialize() = 0;
    virtual void sendMessage(const std::string& channel, const std::string& message) = 0;
    virtual std::string receiveMessage(const std::string& channel) = 0;
};