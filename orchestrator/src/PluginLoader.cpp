#include <vector>
#include "PluginLoader.h"
#include <iostream>

/*
 * PluginLoader: Concrete implementation of IPluginLoader.
 * Loads and unloads plugins dynamically.
 * 
 * // TODO (Copilot): Implement dynamic library loading and plugin registry.
 */

void PluginLoader::loadPlugins(const std::string& directory) {
    std::cout << "[PluginLoader] Loading plugins from: " << directory << std::endl;
    // TODO: Implement dynamic plugin loading
}

std::vector<IService*> PluginLoader::getLoadedServices() const {
    return services_;
}