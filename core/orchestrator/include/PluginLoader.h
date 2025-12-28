#pragma once
#include "IPluginLoader.h"

class PluginLoader : public IPluginLoader {
public:
    ~PluginLoader() noexcept override = default;
    void loadPlugins(const std::string& directory) override;
    std::vector<IService*> getLoadedServices() const override;
private:
    std::vector<IService*> services_;
};