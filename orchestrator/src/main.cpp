#include "IPCManager.h"
#include "HealthMonitor.h"
#include "PluginLoader.h"
#include <memory>
#include <iostream>

int main() {
    std::unique_ptr<IIPCManager> ipc = std::make_unique<IPCManager>();
    std::unique_ptr<IHealthMonitor> health = std::make_unique<HealthMonitor>();
    std::unique_ptr<IPluginLoader> plugins = std::make_unique<PluginLoader>();

    ipc->initialize();
    health->initialize();
    plugins->initialize();

    ipc->sendMessage("system", "Hello, AI OS kernel core!");
    health->reportStatus();
    plugins->loadPlugin("example_plugin.so");

    std::cout << "Kernel core modules initialized and running." << std::endl;
    return 0;
}