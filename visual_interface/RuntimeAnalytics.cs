using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Text.Json;
using System.Threading.Tasks;
using Microsoft.Extensions.Logging;

namespace AIOS.VisualInterface
{
    /// <summary>
    /// Comprehensive runtime analytics and metadata generation for consciousness visualization
    /// Tracks execution patterns, performance metrics, and consciousness emergence behaviors
    /// </summary>
    public class RuntimeAnalytics : IDisposable
    {
        private readonly ILogger<RuntimeAnalytics> _logger;
        private readonly string _analyticsDirectory;
        private readonly string _sessionId;
        private readonly DateTime _sessionStart;
        private readonly List<ExecutionEvent> _executionEvents;
        private readonly List<PerformanceMetric> _performanceMetrics;
        private readonly List<ConsciousnessPattern> _consciousnessPatterns;
        private readonly object _analyticsLock = new object();
        
        // Performance monitoring
        private readonly PerformanceCounter _cpuCounter;
        private readonly PerformanceCounter _memoryCounter;
        private readonly Stopwatch _uiResponseTimer;
        
        public RuntimeAnalytics(ILogger<RuntimeAnalytics> logger)
        {
            _logger = logger;
            _sessionId = Guid.NewGuid().ToString("N")[..8];
            _sessionStart = DateTime.Now;
            _analyticsDirectory = Path.Combine(@"c:\dev\AIOS\test_results", "visual_analytics");
            
            _executionEvents = new List<ExecutionEvent>();
            _performanceMetrics = new List<PerformanceMetric>();
            _consciousnessPatterns = new List<ConsciousnessPattern>();
            
            // Initialize performance counters
            try
            {
                _cpuCounter = new PerformanceCounter("Processor", "% Processor Time", "_Total");
                _memoryCounter = new PerformanceCounter("Memory", "Available MBytes");
                _uiResponseTimer = new Stopwatch();
            }
            catch (Exception ex)
            {
                _logger.LogWarning(ex, "Could not initialize performance counters");
            }
            
            Directory.CreateDirectory(_analyticsDirectory);
            LogExecutionEvent("APPLICATION_START", "AIOS Consciousness Visualizer started");
            
            _logger.LogInformation("Runtime analytics initialized for session {SessionId}", _sessionId);
        }
        
        public void LogExecutionEvent(string eventType, string description, object metadata = null)
        {
            var executionEvent = new ExecutionEvent
            {
                SessionId = _sessionId,
                Timestamp = DateTime.Now,
                EventType = eventType,
                Description = description,
                Metadata = metadata,
                ElapsedTime = DateTime.Now - _sessionStart
            };
            
            lock (_analyticsLock)
            {
                _executionEvents.Add(executionEvent);
            }
            
            _logger.LogInformation("Execution Event: {EventType} - {Description}", eventType, description);
        }
        
        public void LogPerformanceMetric(string metricName, double value, string unit = "")
        {
            var performanceMetric = new PerformanceMetric
            {
                SessionId = _sessionId,
                Timestamp = DateTime.Now,
                MetricName = metricName,
                Value = value,
                Unit = unit,
                CpuUsage = GetCpuUsage(),
                MemoryUsage = GetMemoryUsage()
            };
            
            lock (_analyticsLock)
            {
                _performanceMetrics.Add(performanceMetric);
            }
        }
        
        public void LogConsciousnessPattern(ConsciousnessMetrics metrics, string patternType)
        {
            var pattern = new ConsciousnessPattern
            {
                SessionId = _sessionId,
                Timestamp = DateTime.Now,
                PatternType = patternType,
                ConsciousnessLevel = metrics.ConsciousnessLevel,
                QuantumCoherence = metrics.QuantumCoherence,
                EmergenceLevel = metrics.EmergenceLevel,
                IsLiveData = metrics.IsLiveData,
                ActiveDimensionalLayers = metrics.Topology?.ActiveDimensionalLayers ?? 0,
                MicroSphereCount = metrics.ActiveMicroSpheres?.Count ?? 0,
                QuantumFluctuationIntensity = metrics.QuantumFoam?.FluctuationIntensity ?? 0,
                RecentCollapseEvents = metrics.CollapseEvents?.RecentCollapses?.Count ?? 0
            };
            
            lock (_analyticsLock)
            {
                _consciousnessPatterns.Add(pattern);
            }
        }
        
        public void StartUIResponseTimer()
        {
            _uiResponseTimer?.Restart();
        }
        
        public void StopUIResponseTimer(string operation)
        {
            if (_uiResponseTimer?.IsRunning == true)
            {
                _uiResponseTimer.Stop();
                LogPerformanceMetric($"ui_response_{operation}", _uiResponseTimer.ElapsedMilliseconds, "ms");
            }
        }
        
        public async Task ExportSessionAnalyticsAsync()
        {
            try
            {
                var sessionData = new
                {
                    SessionInfo = new
                    {
                        SessionId = _sessionId,
                        StartTime = _sessionStart,
                        EndTime = DateTime.Now,
                        Duration = DateTime.Now - _sessionStart,
                        TotalExecutionEvents = _executionEvents.Count,
                        TotalPerformanceMetrics = _performanceMetrics.Count,
                        TotalConsciousnessPatterns = _consciousnessPatterns.Count
                    },
                    ExecutionEvents = _executionEvents,
                    PerformanceMetrics = _performanceMetrics,
                    ConsciousnessPatterns = _consciousnessPatterns,
                    SystemInfo = new
                    {
                        Environment.MachineName,
                        Environment.OSVersion,
                        Environment.ProcessorCount,
                        Environment.WorkingSet,
                        Environment.Version,
                        CurrentDirectory = Environment.CurrentDirectory
                    }
                };
                
                var fileName = $"session_analytics_{_sessionId}_{DateTime.Now:yyyyMMdd_HHmmss}.json";
                var filePath = Path.Combine(_analyticsDirectory, fileName);
                
                var json = JsonSerializer.Serialize(sessionData, new JsonSerializerOptions 
                { 
                    WriteIndented = true,
                    PropertyNamingPolicy = JsonNamingPolicy.CamelCase
                });
                
                await File.WriteAllTextAsync(filePath, json);
                
                LogExecutionEvent("ANALYTICS_EXPORT", $"Session analytics exported to {fileName}");
                _logger.LogInformation("Session analytics exported to {FilePath}", filePath);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error exporting session analytics");
            }
        }
        
        public async Task<AnalyticsSummary> GenerateSessionSummaryAsync()
        {
            var summary = new AnalyticsSummary
            {
                SessionId = _sessionId,
                SessionDuration = DateTime.Now - _sessionStart,
                TotalEvents = _executionEvents.Count,
                
                // Performance analysis
                AverageUIResponseTime = _performanceMetrics
                    .Where(m => m.MetricName.StartsWith("ui_response"))
                    .Average(m => m.Value),
                    
                PeakCpuUsage = _performanceMetrics.Max(m => m.CpuUsage),
                AverageMemoryUsage = _performanceMetrics.Average(m => m.MemoryUsage),
                
                // Consciousness pattern analysis
                PeakConsciousnessLevel = _consciousnessPatterns.Max(p => p.ConsciousnessLevel),
                AverageEmergenceLevel = _consciousnessPatterns.Average(p => p.EmergenceLevel),
                MaxDimensionalLayers = _consciousnessPatterns.Max(p => p.ActiveDimensionalLayers),
                TotalCollapseEvents = _consciousnessPatterns.Sum(p => p.RecentCollapseEvents),
                
                // Event categorization
                CriticalEvents = _executionEvents.Count(e => e.EventType.Contains("ERROR") || e.EventType.Contains("CRITICAL")),
                WarningEvents = _executionEvents.Count(e => e.EventType.Contains("WARNING")),
                InfoEvents = _executionEvents.Count(e => e.EventType.Contains("INFO") || e.EventType.Contains("START"))
            };
            
            return summary;
        }
        
        private double GetCpuUsage()
        {
            try
            {
                return _cpuCounter?.NextValue() ?? 0;
            }
            catch
            {
                return 0;
            }
        }
        
        private double GetMemoryUsage()
        {
            try
            {
                return _memoryCounter?.NextValue() ?? 0;
            }
            catch
            {
                return 0;
            }
        }
        
        public void Dispose()
        {
            try
            {
                LogExecutionEvent("APPLICATION_END", "AIOS Consciousness Visualizer shutting down");
                Task.Run(async () => await ExportSessionAnalyticsAsync());
                
                _cpuCounter?.Dispose();
                _memoryCounter?.Dispose();
                _uiResponseTimer?.Stop();
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error during analytics disposal");
            }
        }
    }
    
    // Data models for analytics
    public class ExecutionEvent
    {
        public string SessionId { get; set; } = string.Empty;
        public DateTime Timestamp { get; set; }
        public string EventType { get; set; } = string.Empty;
        public string Description { get; set; } = string.Empty;
        public object Metadata { get; set; }
        public TimeSpan ElapsedTime { get; set; }
    }
    
    public class PerformanceMetric
    {
        public string SessionId { get; set; } = string.Empty;
        public DateTime Timestamp { get; set; }
        public string MetricName { get; set; } = string.Empty;
        public double Value { get; set; }
        public string Unit { get; set; } = string.Empty;
        public double CpuUsage { get; set; }
        public double MemoryUsage { get; set; }
    }
    
    public class ConsciousnessPattern
    {
        public string SessionId { get; set; } = string.Empty;
        public DateTime Timestamp { get; set; }
        public string PatternType { get; set; } = string.Empty;
        public double ConsciousnessLevel { get; set; }
        public double QuantumCoherence { get; set; }
        public double EmergenceLevel { get; set; }
        public bool IsLiveData { get; set; }
        public int ActiveDimensionalLayers { get; set; }
        public int MicroSphereCount { get; set; }
        public double QuantumFluctuationIntensity { get; set; }
        public int RecentCollapseEvents { get; set; }
    }
    
    public class AnalyticsSummary
    {
        public string SessionId { get; set; } = string.Empty;
        public TimeSpan SessionDuration { get; set; }
        public int TotalEvents { get; set; }
        public double AverageUIResponseTime { get; set; }
        public double PeakCpuUsage { get; set; }
        public double AverageMemoryUsage { get; set; }
        public double PeakConsciousnessLevel { get; set; }
        public double AverageEmergenceLevel { get; set; }
        public int MaxDimensionalLayers { get; set; }
        public int TotalCollapseEvents { get; set; }
        public int CriticalEvents { get; set; }
        public int WarningEvents { get; set; }
        public int InfoEvents { get; set; }
    }
}
