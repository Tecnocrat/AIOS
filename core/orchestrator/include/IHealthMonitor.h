/*
 * IHealthMonitor: Interface for system health monitoring.
 * The Health Monitor is the “core temperature sensor” of the hypersphere,
 * observing the coherence and stability of the system at every scale.
 * 
 * In the hypersphere metaphor, this module senses the harmonics of the whole,
 * detecting phase shifts, instabilities, and emergent patterns.
 */
#pragma once

class IHealthMonitor {
public:
    virtual ~IHealthMonitor() = default;
    virtual void initialize() = 0;
    virtual void reportStatus() = 0;
    virtual bool isHealthy() const = 0;
};