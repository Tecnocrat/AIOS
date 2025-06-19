#include "IPCManager.hpp"
#include <memory>
#include <iostream>

int main() {
    std::unique_ptr<IIPCManager> ipc = std::make_unique<IPCManager>();
    ipc->initialize();
    ipc->sendMessage("system", "Hello, IPC!");
    std::cout << ipc->receiveMessage("system") << std::endl;
    return 0;
}