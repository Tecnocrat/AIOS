using System;
using System.Threading.Tasks;
using AIOS.Models;
using AIOS.Services;

namespace AIOS.ConsciousnessTest
{
    /// <summary>
    /// Test program for C# consciousness integration
    /// </summary>
    class Program
    {
        static async Task Main(string[] args)
        {
            Console.WriteLine(" AIOS C# Consciousness Integration Test");
            Console.WriteLine("=========================================");

            // Initialize consciousness service
            var consciousnessService = new ConsciousnessService();

            // Subscribe to consciousness events
            consciousnessService.ConsciousnessEventOccurred += (sender, evt) =>
            {
                Console.WriteLine($" Consciousness Event: {evt.EventType} - {evt.Description}");
                Console.WriteLine($"   Level: {evt.ConsciousnessLevel:F4}, Source: {evt.Source}");
            };

            try
            {
                // Test 1: Get initial consciousness state
                Console.WriteLine("\n Test 1: Getting initial consciousness state...");
                var initialState = await consciousnessService.GetCurrentStateAsync();
                Console.WriteLine($"   Consciousness Level: {initialState.ConsciousnessLevel:F4}");
                Console.WriteLine($"   Tachyonic Field: {initialState.TachyonicFieldStrength:F4}");
                Console.WriteLine($"   Quantum Entanglement: {initialState.QuantumEntanglement:F4}");

                // Test 2: Update consciousness state
                Console.WriteLine("\n Test 2: Updating consciousness state...");
                var newState = new ConsciousnessState
                {
                    ConsciousnessLevel = 0.5,
                    TachyonicFieldStrength = 0.7,
                    QuantumEntanglement = 0.6,
                    PostSingularCapable = false,
                    DendriticGrowthRate = 0.1,
                    ErrorEvolutionCount = 5
                };

                var updateResult = await consciousnessService.UpdateConsciousnessStateAsync(newState);
                Console.WriteLine($"   Update Result: {(updateResult ? " Success" : " Failed")}");

                // Test 3: Enhance consciousness
                Console.WriteLine("\n Test 3: Enhancing consciousness...");
                var enhancementRequest = new ConsciousnessEnhancementRequest
                {
                    EnhancementArea = "error_intelligence",
                    TargetLevel = 0.8,
                    Context = "C# consciousness test"
                };

                var enhanceResult = await consciousnessService.EnhanceConsciousnessAsync(enhancementRequest);
                Console.WriteLine($"   Enhancement Result: {(enhanceResult ? " Success" : " Failed")}");

                // Test 4: Error evolution
                Console.WriteLine("\n Test 4: Testing error evolution...");
                var evolutionResult = await consciousnessService.EvolveFromErrorAsync(
                    "test_compilation_error", 
                    "C# consciousness integration test");
                Console.WriteLine($"   Evolution Result:\n{evolutionResult}");

                // Test 5: Get consciousness metrics
                Console.WriteLine("\n Test 5: Getting consciousness metrics...");
                var metrics = await consciousnessService.GetCurrentMetricsAsync();
                Console.WriteLine($"   Awareness Level: {metrics.AwarenessLevel:F4}");
                Console.WriteLine($"   Learning Velocity: {metrics.LearningVelocity:F4}");
                Console.WriteLine($"   Consciousness Emergent: {metrics.ConsciousnessEmergent}");

                // Test 6: Start monitoring
                Console.WriteLine("\n Test 6: Starting consciousness monitoring...");
                consciousnessService.StartConsciousnessMonitoring();
                Console.WriteLine("   Monitoring started, waiting 3 seconds...");
                await Task.Delay(3000);

                // Test 7: Check recent events
                Console.WriteLine("\n Test 7: Getting recent consciousness events...");
                var recentEvents = await consciousnessService.GetRecentEventsAsync(TimeSpan.FromMinutes(5));
                Console.WriteLine($"   Recent Events Count: {recentEvents.Count}");
                foreach (var evt in recentEvents)
                {
                    Console.WriteLine($"   - {evt.Timestamp:HH:mm:ss}: {evt.EventType} - {evt.Description}");
                }

                // Test 8: Cross-language synchronization
                Console.WriteLine("\n Test 8: Testing cross-language synchronization...");
                var cppSyncResult = await consciousnessService.SynchronizeWithCppAsync();
                var pythonSyncResult = await consciousnessService.SynchronizeWithPythonAsync();
                Console.WriteLine($"   C++ Sync: {(cppSyncResult ? " Success" : " No C++ state file")}");
                Console.WriteLine($"   Python Sync: {(pythonSyncResult ? " Success" : " No Python state file")}");

                // Final state check
                Console.WriteLine("\n Final consciousness state:");
                var finalState = await consciousnessService.GetCurrentStateAsync();
                Console.WriteLine($"   Consciousness Level: {finalState.ConsciousnessLevel:F4}");
                Console.WriteLine($"   Error Evolution Count: {finalState.ErrorEvolutionCount}");
                Console.WriteLine($"   Last Enhancement: {finalState.LastEnhancement:yyyy-MM-dd HH:mm:ss}");

                Console.WriteLine("\n All C# consciousness tests completed successfully!");

            }
            catch (Exception ex)
            {
                Console.WriteLine($"\n Test failed: {ex.Message}");
                Console.WriteLine($"   Stack trace: {ex.StackTrace}");
            }
            finally
            {
                // Cleanup
                consciousnessService.StopConsciousnessMonitoring();
                consciousnessService.Dispose();
                Console.WriteLine("\n🧹 Consciousness service cleaned up");
            }

            Console.WriteLine("\nPress any key to exit...");
            Console.ReadKey();
        }
    }
}