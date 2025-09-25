#pragma once
#include <string>
#include <vector>
#include "IService.h"

/*
 * IPluginLoader: Interface for dynamic plugin management.
 * The Plugin Loader is the “event horizon” of the hypersphere,
 * allowing new modules to enter the system, adapt, and extend its capabilities.
 * 
 * In the hypersphere metaphor, this is the boundary where new subspaces are
 * harmonized and integrated into the whole.
 */
class IPluginLoader {
public:
    virtual ~IPluginLoader() noexcept = default;
    virtual void loadPlugins(const std::string& directory) = 0;
    virtual std::vector<IService*> getLoadedServices() const = 0;
};