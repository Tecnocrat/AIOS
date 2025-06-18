#pragma once
#include <string>
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
    virtual ~IPluginLoader() = default;
    virtual void initialize() = 0;
    virtual bool loadPlugin(const std::string& path) = 0;
    virtual void unloadPlugin(const std::string& name) = 0;
};