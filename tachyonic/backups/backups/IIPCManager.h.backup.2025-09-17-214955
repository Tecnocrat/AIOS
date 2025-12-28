#pragma once
#include <string>

/*
 * IIPCManager: Interface for Inter-Process Communication management.
 * The IPC Manager is the hypersphere’s membrane—projecting and receiving signals
 * across the boundaries of the OS, maintaining coherence between all modules.
 * 
 * In the hypersphere metaphor, this is the channel through which subspaces communicate,
 * and where the projection of intent becomes action.
 */
class IIPCManager {
public:
    virtual ~IIPCManager() = default;
    virtual void initialize() = 0;
    virtual void sendMessage(const std::string& channel, const std::string& message) = 0;
    virtual std::string receiveMessage(const std::string& channel) = 0;
};