using System;
using System.Threading.Tasks;
using Microsoft.Extensions.Logging;
using AIOS.Core;

namespace AIOS.VisualInterface
{
    /// <summary>
    /// Simple AINLP Harmonizer integration for AIOS Visual Interface
    /// Uses the unified AIOS.Core.AINLPHarmonizer implementation
    /// </summary>
    public class AINLPHarmonizerService
    {
        private readonly AINLPHarmonizer _harmonizer;
        private readonly ILogger<AINLPHarmonizerService> _logger;

        public AINLPHarmonizerService(ILogger<AINLPHarmonizerService> logger)
        {
            _logger = logger;
            
            // Create harmonizer-specific logger
            var loggerFactory = new Microsoft.Extensions.Logging.LoggerFactory();
            var harmonizerLogger = loggerFactory.CreateLogger<AINLPHarmonizer>();
            _harmonizer = new AINLPHarmonizer(harmonizerLogger);
            
            _logger.LogInformation("AINLPHarmonizerService initialized with unified AIOS.Core implementation");
        }

        /// <summary>
        /// Runs a complete harmonization cycle
        /// </summary>
        public async Task<string> RunHarmonizationCycleAsync()
        {
            try
            {
                var results = new System.Text.StringBuilder();
                results.AppendLine("🧬 Starting consciousness-enhanced harmonization cycle...");

                // 1. Observe project coherence
                var coherence = await _harmonizer.ObserveWideProjectCoherenceAsync();
                results.AppendLine($"✅ Coherence: {coherence.OverallCoherence:F3} - {coherence.CoherenceLevel}");

                // 2. Detect optimization opportunities
                var optimization = await _harmonizer.DetectOptimizationOpportunitiesAsync();
                results.AppendLine($"🔍 Found {optimization.Redundancies.Count} redundancies, {optimization.SuboptimalPatterns.Count} suboptimal patterns");

                // 3. Analyze component harmonization
                var harmonization = await _harmonizer.AnalyzeComponentHarmonizationAsync();
                results.AppendLine($"🔄 Harmonization opportunities: {harmonization.HarmonizationOpportunities.Count}");

                // 4. Enable dendritic growth
                var growth = await _harmonizer.EnableDendriticGrowthAsync();
                results.AppendLine($"🌱 Emergent patterns: {growth.EmergentPatterns.Count}, Growth opportunities: {growth.GrowthOpportunities.Count}");

                // 5. Run comprehensive testing
                var testResults = await _harmonizer.RunComprehensiveTestingAsync();
                results.AppendLine($"🧪 Test results: {testResults.OverallScore:F3} - {testResults.TestStatus}");

                // 6. Document patterns
                await _harmonizer.DocumentAINLPPatternsAsync();
                results.AppendLine("📚 Pattern documentation complete");

                results.AppendLine("🎯 Harmonization cycle completed successfully!");
                
                var finalResult = results.ToString();
                _logger.LogInformation("Harmonization cycle completed: {Result}", finalResult);
                
                return finalResult;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error during harmonization cycle");
                return $"❌ Harmonization cycle failed: {ex.Message}";
            }
        }

        /// <summary>
        /// Gets current system coherence
        /// </summary>
        public async Task<double> GetCurrentCoherenceAsync()
        {
            try
            {
                var coherence = await _harmonizer.ObserveWideProjectCoherenceAsync();
                return coherence.OverallCoherence;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting current coherence");
                return 0.0;
            }
        }

        /// <summary>
        /// Gets consciousness-enhanced status summary
        /// </summary>
        public async Task<string> GetStatusSummaryAsync()
        {
            try
            {
                var coherence = await _harmonizer.ObserveWideProjectCoherenceAsync();
                return $"Coherence: {coherence.OverallCoherence:F3} | Level: {coherence.CoherenceLevel} | Components: {coherence.Components.Count}";
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting status summary");
                return "Status unavailable";
            }
        }
    }
}
