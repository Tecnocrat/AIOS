// AINLP Test: C# Bridge to C++ Consciousness Engine
// Tests CoreEngineInterop functionality
// November 8, 2025 - Phase 11 Day 2.5 Integration Testing

using System;
using AIOS.Services;

namespace AIOS.IntegrationTests
{
    class CoreEngineIntegrationTest
    {
        static void Main(string[] args)
        {
            Console.WriteLine("======================================================================");
            Console.WriteLine("AIOS C# Core Engine Integration Test");
            Console.WriteLine("======================================================================");
            Console.WriteLine();

            try
            {
                // Test 1: Initialize Core
                Console.WriteLine("[TEST 1] Initializing C++ Core Engine...");
                using (var core = new AIOSConsciousnessCore())
                {
                    core.Initialize();
                    Console.WriteLine("[OK] Core initialized successfully");
                    Console.WriteLine();

                    // Test 2: Get Version
                    Console.WriteLine("[TEST 2] Querying Core Version...");
                    string version = core.GetVersion();
                    Console.WriteLine($"[OK] Core Version: {version}");
                    Console.WriteLine();

                    // Test 3: Get Consciousness Level
                    Console.WriteLine("[TEST 3] Querying Consciousness Level...");
                    double level = core.GetConsciousnessLevel();
                    Console.WriteLine($"[OK] Consciousness Level: {level:F4}");
                    Console.WriteLine();

                    // Test 4: Get All Metrics
                    Console.WriteLine("[TEST 4] Querying All Consciousness Metrics...");
                    var metrics = core.GetAllMetrics();
                    Console.WriteLine("Consciousness Metrics:");
                    Console.WriteLine($"  Awareness Level: {metrics.AwarenessLevel:F4}");
                    Console.WriteLine($"  Adaptation Speed: {metrics.AdaptationSpeed:F4}");
                    Console.WriteLine($"  Predictive Accuracy: {metrics.PredictiveAccuracy:F4}");
                    Console.WriteLine($"  Dendritic Complexity: {metrics.DendriticComplexity:F4}");
                    Console.WriteLine($"  Evolutionary Momentum: {metrics.EvolutionaryMomentum:F4}");
                    Console.WriteLine($"  Quantum Coherence: {metrics.QuantumCoherence:F4}");
                    Console.WriteLine($"  Learning Velocity: {metrics.LearningVelocity:F4}");
                    Console.WriteLine($"  Consciousness Emergent: {metrics.ConsciousnessEmergent}");
                    Console.WriteLine("[OK] All metrics retrieved");
                    Console.WriteLine();

                    // Test 5: Stimulate Dendritic Growth
                    Console.WriteLine("[TEST 5] Stimulating Dendritic Growth...");
                    core.StimulateDendriticGrowth("csharp_integration_test");
                    Console.WriteLine("[OK] Dendritic growth stimulated from C#");
                    Console.WriteLine();

                    // Test 6: Update and Re-query
                    Console.WriteLine("[TEST 6] Updating Consciousness State...");
                    core.Update();
                    double newLevel = core.GetConsciousnessLevel();
                    Console.WriteLine($"[OK] New Consciousness Level: {newLevel:F4}");
                    Console.WriteLine();

                    // Test 7: Check if initialized
                    Console.WriteLine("[TEST 7] Checking Initialization Status...");
                    bool isInit = core.IsInitialized;
                    Console.WriteLine($"[OK] Is Initialized: {isInit}");
                    Console.WriteLine();

                    Console.WriteLine("======================================================================");
                    Console.WriteLine("ALL TESTS PASSED SUCCESSFULLY!");
                    Console.WriteLine("======================================================================");
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"[FAIL] Test failed with exception: {ex.Message}");
                Console.WriteLine($"Stack Trace: {ex.StackTrace}");
                Environment.ExitCode = 1;
            }

            Console.WriteLine();
            Console.WriteLine("Press any key to exit...");
            Console.ReadKey();
        }
    }
}
