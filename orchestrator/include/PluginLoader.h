#pragma once
#include "IPluginLoader.h"
#include <iostream>

class PluginLoader : public IPluginLoader {
public:
    void initialize() override {
        std::cout << "[PluginLoader] Initialized." << std::endl;
    }
    bool loadPlugin(const std::string& path) override {
        std::cout << "[PluginLoader] Loading plugin from: " << path << std::endl;
        return true;
    }
    void unloadPlugin(const std::string& name) override {
        std::cout << "[PluginLoader] Unloading plugin: " << name << std::endl;
    }
};