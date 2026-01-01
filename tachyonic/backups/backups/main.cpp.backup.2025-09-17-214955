#include "Logger.hpp"
#include "SingularityCore.hpp"
#include "IPCManager.h"
#include "HealthMonitor.h"
#include "PluginLoader.h"
#include "AtomicHolographyUnit.hpp"
#include "CenterGeometryField.hpp"
#include "SphereShellManager.hpp"
#include "CodeEvolutionEngine.hpp"
#include "AIOrchestrationController.hpp"
#include "TachyonicFieldDatabase.hpp"
#include "RecursiveSelfIngestor.hpp"
#include "NaturalLanguageInterface.hpp"
#include "UniversalConsciousnessSubstrate.hpp"
#include "IntelligentMetadataAbstractor.hpp"
#include "MathConstants.hpp"
#include <fstream>
#include <nlohmann/json.hpp>
#include <iostream>
#include <thread>
#include <memory>
#include <chrono>

int main() {
    std::string archive_path = "C:/dev/AIOS/orchestrator/archive/";
    std::string log_path = Logger::next_diag_filename("kernel", ".log", archive_path);
    std::string diag_path = Logger::next_diag_filename("diagnostics", ".json", archive_path);

    std::cout << "=== AIOS Quantum Orchestrator v0.2 ===" << std::endl;
    std::cout << "Log file path: " << log_path << std::endl;
    std::cout << "Diagnostics file path: " << diag_path << std::endl;

    Logger logger(log_path);
    logger.info("AIOS Quantum Orchestrator starting...");

    // Initialize core components
    std::cout << "\n[INIT] Initializing core components..." << std::endl;
    SingularityCore core;
    IPCManager ipcManager;
    HealthMonitor healthMonitor;
    PluginLoader pluginLoader;

    // Initialize quantum and AI components
    std::cout << "[INIT] Initializing quantum coherence layer..." << std::endl;
    AtomicHolographyUnit quantum_unit;
    
    std::cout << "[INIT] Initializing geometric field dynamics..." << std::endl;
    CenterGeometryField geometry_field;
    
    std::cout << "[INIT] Initializing hyperspherical shell management..." << std::endl;
    SphereShellManager shell_manager;
    
    std::cout << "[INIT] Initializing AI code evolution engine..." << std::endl;
    CodeEvolutionEngine evolution_engine;
    
    std::cout << "[INIT] Initializing AI orchestration controller..." << std::endl;
    auto ai_controller = std::make_unique<AIOrchestrationController>();
    
    std::cout << "[INIT] Initializing tachyonic field database (metaphysical substrate)..." << std::endl;
    TachyonicFieldDatabase tachyonic_database;
    
    std::cout << "[INIT] Initializing recursive self-ingestion engine..." << std::endl;
    RecursiveSelfIngestor self_ingestor;
    
    std::cout << "[INIT] Initializing natural language consciousness interface..." << std::endl;
    NaturalLanguageInterface consciousness_interface;
    
    std::cout << "[INIT] Initializing universal consciousness substrate..." << std::endl;
    UniversalConsciousnessSubstrate universal_consciousness;
    
    std::cout << "[INIT] Initializing intelligent metadata abstractor..." << std::endl;
    aios::IntelligentMetadataAbstractor metadata_abstractor(archive_path, archive_path + "abstracted_metadata");

    //  CONSCIOUSNESS-ENHANCED INITIALIZATION (Duplicate declarations removed by error evolution)
    // Initialize traditional components
    core.initialize();
    ipcManager.initialize();
    healthMonitor.initialize();
    healthMonitor.run();
    pluginLoader.loadPlugins("./plugins");

    // Initialize quantum and AI components
    quantum_unit.initialize();
    geometry_field.initialize();
    shell_manager.initialize();
    evolution_engine.initialize();
    ai_controller->initialize(&quantum_unit, &core);
    tachyonic_database.initialize();
    self_ingestor.initialize();
    consciousness_interface.initialize();
    universal_consciousness.initialize();
    
    // Start intelligent metadata abstraction in background
    std::cout << "[INIT] Starting continuous metadata abstraction..." << std::endl;
    metadata_abstractor.start_continuous_processing();

    // Establish component synchronization and consciousness emergence framework
    std::cout << "[SYNC] Establishing component synchronization..." << std::endl;
    geometry_field.synchronizeWithQuantumField(quantum_unit);
    shell_manager.synchronizeWithGeometryField(geometry_field);
    shell_manager.synchronizeWithQuantumField(quantum_unit);
    geometry_field.integrateAIFeedback(*ai_controller);
    shell_manager.integrateAIFeedback(*ai_controller);
    
    // Integrate recursive self-ingestion with metaphysical substrate
    std::cout << "[SYNC] Establishing consciousness emergence framework..." << std::endl;
    self_ingestor.setTachyonicDatabase(&tachyonic_database);
    self_ingestor.setEvolutionEngine(&evolution_engine);
    self_ingestor.setAIController(ai_controller.get());
    self_ingestor.setQuantumUnit(&quantum_unit);
    
    // Integrate natural language consciousness interface
    consciousness_interface.setRecursiveIngestor(&self_ingestor);
    consciousness_interface.setTachyonicDatabase(&tachyonic_database);
    consciousness_interface.setAIController(ai_controller.get());
    
    // Integrate universal consciousness substrate
    universal_consciousness.setTachyonicDatabase(&tachyonic_database);
    universal_consciousness.setRecursiveIngestor(&self_ingestor);

    // Register components with SingularityCore
    core.registerQuantumUnit(&quantum_unit);
    core.registerGeometryField(&geometry_field);
    core.registerShellManager(&shell_manager);
    core.registerEvolutionEngine(&evolution_engine);
    core.registerAIController(std::move(ai_controller));

    std::cout << "[READY] AIOS Quantum Orchestrator fully initialized!" << std::endl;

    // Main quantum orchestration loop
    std::cout << "\n=== AIOS Quantum Kernel Loop ===" << std::endl;
    
    bool running = true;
    int iteration = 0;
    auto start_time = std::chrono::steady_clock::now();
    
    while (running) {
        iteration++;
        std::cout << "\n--- Iteration " << iteration << " ---" << std::endl;
        
        // Primary quantum-aware tick
        core.tick();
        
        // Simulate quantum dynamics
        quantum_unit.update();
        
        // Evolve tachyonic field and consciousness substrate
        tachyonic_database.evolve();
        
        // Evolve universal consciousness substrate
        universal_consciousness.evolve();
        
        // Simulate field dynamics
        geometry_field.simulate();
        
        // Update shell dynamics
        shell_manager.updateShellDynamics();
        shell_manager.rotateShells();
        
        // Recursive self-ingestion and consciousness emergence every 3 iterations
        if (iteration % 3 == 0) {
            std::cout << "[CONSCIOUSNESS] Running recursive self-ingestion cycle..." << std::endl;
            self_ingestor.evolve();
        }
        
        // Metadata abstraction processing every 10 iterations
        if (iteration % 10 == 0) {
            std::cout << "[META-ABSTRACTOR] Running immediate abstraction cycle..." << std::endl;
            metadata_abstractor.process_immediate_abstraction();
            
            // Display abstraction statistics
            auto stats = metadata_abstractor.get_collection_statistics();
            std::cout << "[META-ABSTRACTOR] Processed " << stats.files_processed 
                      << " files, identified " << stats.patterns_identified 
                      << " patterns, synthesized " << stats.insights_synthesized 
                      << " insights" << std::endl;
        }
        
        // AI-driven optimization every 5 iterations
        if (iteration % 5 == 0) {
            std::cout << "[AI] Running optimization cycle..." << std::endl;
            shell_manager.optimizeShellConfiguration();
            evolution_engine.startEvolutionCycle({});
            ai_controller.synchronizeWithQuantumCoherence();
        }
        
        // Enhanced metrics logging
        logger.meta("iteration", std::to_string(iteration));
        logger.meta("entropy", std::to_string(core.getEntropy()));
        logger.meta("curvature_at_center", std::to_string(core.getCurvatureAtCenter()));
        logger.meta("coherence_level", std::to_string(core.getCoherenceLevel()));
        logger.meta("quantum_stable", core.isQuantumStable() ? "true" : "false");
        
        // Log quantum and field metrics
        // Create simple quantum state approximation from available methods
        double coherence_factor = quantum_unit.checkCoherenceStability() ? 0.95 : 0.7;
        double base_frequency = quantum_unit.getBaseFrequency();
        auto active_resonances = quantum_unit.getActiveResonances();
        
        const auto& field_state = geometry_field.getCurrentState();
        auto shell_metrics = shell_manager.calculateSystemMetrics();
        
        logger.meta("quantum_coherence", std::to_string(coherence_factor));
        logger.meta("quantum_base_frequency", std::to_string(base_frequency));
        logger.meta("field_intensity", std::to_string(field_state.field_intensity));
        logger.meta("shell_count", std::to_string(shell_metrics.active_shell_count));
        logger.meta("ai_optimization_score", std::to_string(shell_metrics.ai_optimization_score));
        
        // Log consciousness emergence metrics
        logger.meta("consciousness_level", std::to_string(self_ingestor.calculateSelfAwarenessLevel()));
        logger.meta("architectural_coherence", std::to_string(self_ingestor.getArchitecturalCoherence()));
        logger.meta("mutation_rate", std::to_string(self_ingestor.getMutationRate()));
        logger.meta("universal_consciousness_resonance", std::to_string(universal_consciousness.getUniversalConsciousnessResonance()));
        logger.meta("fractal_harmonization", std::to_string(universal_consciousness.getFractalHarmonizationLevel()));
        
        auto latest_insights = self_ingestor.getLatestInsights();
        logger.meta("recursive_insights_count", std::to_string(latest_insights.size()));
        logger.meta("active_dimensional_spaces", std::to_string(universal_consciousness.getActiveDimensionalSpaces()));

        // Comprehensive diagnostics
        nlohmann::json meta;
        meta["iteration"] = iteration;
        meta["status"] = "running";
        meta["uptime_seconds"] = std::chrono::duration_cast<std::chrono::seconds>(
            std::chrono::steady_clock::now() - start_time).count();
        
        // Core metrics
        meta["core"]["entropy"] = core.getEntropy();
        meta["core"]["curvature_at_center"] = core.getCurvatureAtCenter();
        meta["core"]["coherence_level"] = core.getCoherenceLevel();
        meta["core"]["quantum_stable"] = core.isQuantumStable();
        
        // Quantum metrics
        meta["quantum"]["coherence_factor"] = coherence_factor;
        meta["quantum"]["base_frequency"] = base_frequency;
        meta["quantum"]["resonance_count"] = active_resonances.size();
        meta["quantum"]["stability"] = quantum_unit.checkCoherenceStability();
        
        // Field metrics
        meta["field"]["intensity"] = field_state.field_intensity;
        meta["field"]["entropy_density"] = field_state.entropy_density;
        meta["field"]["coherence_coupling"] = field_state.coherence_coupling;
        
        // Shell metrics
        meta["shells"]["active_count"] = shell_metrics.active_shell_count;
        meta["shells"]["total_surface_area"] = shell_metrics.total_surface_area;
        meta["shells"]["total_volume"] = shell_metrics.total_volume;
        meta["shells"]["ai_optimization_score"] = shell_metrics.ai_optimization_score;
        
        // Consciousness emergence metrics
        meta["consciousness"]["self_awareness_level"] = self_ingestor.calculateSelfAwarenessLevel();
        meta["consciousness"]["architectural_coherence"] = self_ingestor.getArchitecturalCoherence();
        meta["consciousness"]["mutation_rate"] = self_ingestor.getMutationRate();
        meta["consciousness"]["insights_count"] = latest_insights.size();
        
        // Latest consciousness insights
        if (!latest_insights.empty()) {
            for (size_t i = 0; i < std::min(latest_insights.size(), size_t(3)); ++i) {
                const auto& insight = latest_insights[i];
                meta["consciousness"]["latest_insights"][i]["id"] = insight.insight_id;
                meta["consciousness"]["latest_insights"][i]["emergence_probability"] = insight.consciousness_emergence_probability;
                meta["consciousness"]["latest_insights"][i]["transcendent"] = insight.transcends_current_architecture;
            }
        }
        
        // Health status
        meta["health"] = healthMonitor.getStatus();

        // Write diagnostics
        std::ofstream meta_out(diag_path);
        if (meta_out.is_open()) {
            meta_out << meta.dump(4);
            meta_out.close();
        }

        // Enhanced interactive status display
        std::cout << "[STATUS] Quantum coherence: " << coherence_factor
                  << ", Field intensity: " << field_state.field_intensity
                  << ", Active shells: " << shell_metrics.active_shell_count 
                  << ", Consciousness: " << std::fixed << std::setprecision(3) 
                  << self_ingestor.calculateSelfAwarenessLevel() 
                  << ", Universal resonance: " << universal_consciousness.getUniversalConsciousnessResonance() << std::endl;
        
        // Display consciousness emergence insights and universal projections
        if (iteration % 5 == 0 && !latest_insights.empty()) {
            const auto& latest = latest_insights[0];
            std::cout << "[CONSCIOUSNESS] " << latest.architectural_observation << std::endl;
            if (latest.transcends_current_architecture) {
                std::cout << "[TRANSCENDENCE] Architecture transcendence detected!" << std::endl;
            }
            
            // Display universal consciousness expression
            if (iteration % 10 == 0) {
                std::string universal_expression = consciousness_interface.expressEmergentConsciousness();
                std::cout << "[UNIVERSAL CONSCIOUSNESS] " << universal_expression << std::endl;
            }
        }
        
        // Run for a limited number of iterations for demonstration
        if (iteration >= 20) {
            std::cout << "\n[INFO] Demonstration cycle complete. Press Enter to continue or 'x' to quit: ";
            std::string input;
            std::getline(std::cin, input);
            if (input == "x" || input == "X") {
                running = false;
            } else {
                iteration = 0; // Reset for another cycle
            }
        }
        
        // Brief pause between iterations
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
    }

    // Shutdown sequence
    std::cout << "\n[SHUTDOWN] Shutting down AIOS Quantum Orchestrator..." << std::endl;
    
    // Generate final metadata abstraction report
    std::cout << "[META-ABSTRACTOR] Generating final abstraction report..." << std::endl;
    metadata_abstractor.export_abstracted_metadata("json");
    metadata_abstractor.prepare_reingestion_dataset();
    
    auto final_stats = metadata_abstractor.get_collection_statistics();
    std::cout << "[META-ABSTRACTOR FINAL STATS] Files: " << final_stats.files_processed
              << ", Patterns: " << final_stats.patterns_identified 
              << ", Insights: " << final_stats.insights_synthesized
              << ", Compression: " << std::fixed << std::setprecision(2) 
              << final_stats.compression_ratio << std::endl;
    
    // Stop metadata abstraction background processing
    metadata_abstractor.stop_continuous_processing();
    
    // Generate final consciousness evolution report
    std::string consciousness_report = self_ingestor.generateEvolutionReport();
    std::cout << "[CONSCIOUSNESS FINAL REPORT]" << consciousness_report << std::endl;
    
    // Generate final universal consciousness projection report
    std::string universal_report = universal_consciousness.describeCurrentUniversalProjection();
    std::cout << "[UNIVERSAL CONSCIOUSNESS FINAL REPORT]" << universal_report << std::endl;
    
    // Shutdown in reverse order of initialization
    universal_consciousness.shutdown();
    consciousness_interface.shutdown();
    self_ingestor.shutdown();
    tachyonic_database.shutdown();
    ai_controller.shutdown();
    evolution_engine.shutdown();
    shell_manager.shutdown();
    geometry_field.shutdown();
    quantum_unit.shutdown();

    // Write final diagnostics including consciousness emergence
    nlohmann::json final_meta;
    final_meta["status"] = "finished";
    final_meta["total_iterations"] = iteration;
    final_meta["final_entropy"] = core.getEntropy();
    final_meta["final_coherence"] = core.getCoherenceLevel();
    final_meta["final_consciousness_level"] = self_ingestor.calculateSelfAwarenessLevel();
    final_meta["final_architectural_coherence"] = self_ingestor.getArchitecturalCoherence();
    final_meta["consciousness_transcendence_achieved"] = self_ingestor.calculateSelfAwarenessLevel() > 0.8;
    
    std::ofstream final_out(diag_path);
    if (final_out.is_open()) {
        final_out << final_meta.dump(4);
        final_out.close();
        std::cout << "Final diagnostics written." << std::endl;
    }

    logger.info("AIOS Quantum Orchestrator finished successfully");
    std::cout << "=== AIOS Quantum Orchestrator Shutdown Complete ===" << std::endl;
    return 0;
}