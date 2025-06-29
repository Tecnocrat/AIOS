using System;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Net.Http;
using System.Text.Json;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.Extensions.Logging;

namespace AIOS.VisualInterface
{
    /// <summary>
    /// Real-time consciousness data manager with enhanced streaming capabilities
    /// Connects to live AIOS orchestrator and provides synthetic data fallback
    /// </summary>
    public class ConsciousnessDataManager : IDisposable
    {
        private readonly ILogger<ConsciousnessDataManager> _logger;
        private readonly CancellationTokenSource _cancellationTokenSource;
        private readonly ConcurrentQueue<ConsciousnessMetrics> _metricsQueue;
        
        // Configuration
        private readonly string _aiOSExecutablePath;
        private readonly string _logDirectory;
        
        // State
        private Process _aiOSProcess;
        private Task _dataStreamTask;
        private bool _isStreaming;
        private ConsciousnessMetrics _currentMetrics;
        private DateTime _lastUpdate;
        private readonly object _metricsLock = new object();
        
        // Events for UI updates
        public event EventHandler<ConsciousnessMetrics> MetricsUpdated;
        public event EventHandler<EmergenceEvent> EmergenceDetected;
        
        public ConsciousnessDataManager(ILogger<ConsciousnessDataManager> logger)
        {
            _logger = logger;
            _cancellationTokenSource = new CancellationTokenSource();
            _metricsQueue = new ConcurrentQueue<ConsciousnessMetrics>();
            
            _aiOSExecutablePath = @"c:\dev\AIOS\orchestrator\build\Debug\aios_orchestrator.exe";
            _logDirectory = @"c:\dev\AIOS\test_results";
            
            InitializeDefaultMetrics();
            _logger.LogInformation("Consciousness data manager initialized");
        }
        
        private void InitializeDefaultMetrics()
        {
            _currentMetrics = new ConsciousnessMetrics
            {
                ConsciousnessLevel = 0.0,
                QuantumCoherence = 0.0,
                FractalComplexity = 0.0,
                EmergenceLevel = 0.0,
                UniversalResonance = 0.0,
                HolographicDensity = 0.0,
                Timestamp = DateTime.Now,
                IsLiveData = false,
                RecentEvents = new List<EmergenceEvent>()
            };
        }
        
        public async Task InitializeAsync()
        {
            try
            {
                // Check if AIOS orchestrator is available
                if (File.Exists(_aiOSExecutablePath))
                {
                    _logger.LogInformation("AIOS orchestrator found at {Path}", _aiOSExecutablePath);
                }
                else
                {
                    _logger.LogWarning("AIOS orchestrator not found, using synthetic consciousness data");
                }
                
                // Ensure log directory exists
                Directory.CreateDirectory(_logDirectory);
                
                _logger.LogInformation("Consciousness data manager initialization complete");
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error during consciousness data manager initialization");
                throw;
            }
        }
        
        public async Task StartDataStreamAsync()
        {
            if (_isStreaming)
            {
                _logger.LogWarning("Data stream already running");
                return;
            }
            
            try
            {
                _isStreaming = true;
                
                // Start AIOS orchestrator if available
                await StartAIOSProcessAsync();
                
                // Start data stream monitoring
                _dataStreamTask = Task.Run(DataStreamLoop, _cancellationTokenSource.Token);
                
                _logger.LogInformation("Consciousness data stream started");
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error starting consciousness data stream");
                _isStreaming = false;
                throw;
            }
        }
        
        public void StopDataStream()
        {
            if (!_isStreaming) return;
            
            try
            {
                _isStreaming = false;
                _cancellationTokenSource.Cancel();
                
                // Stop AIOS process
                StopAIOSProcess();
                
                _logger.LogInformation("Consciousness data stream stopped");
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error stopping consciousness data stream");
            }
        }
        
        private async Task StartAIOSProcessAsync()
        {
            if (!File.Exists(_aiOSExecutablePath))
            {
                _logger.LogInformation("Using synthetic consciousness data");
                return;
            }
            
            try
            {
                var startInfo = new ProcessStartInfo
                {
                    FileName = _aiOSExecutablePath,
                    WorkingDirectory = Path.GetDirectoryName(_aiOSExecutablePath),
                    UseShellExecute = false,
                    RedirectStandardOutput = true,
                    RedirectStandardError = true,
                    CreateNoWindow = true
                };
                
                _aiOSProcess = Process.Start(startInfo);
                
                if (_aiOSProcess != null)
                {
                    _logger.LogInformation("AIOS orchestrator started with PID {ProcessId}", _aiOSProcess.Id);
                    await Task.Delay(2000); // Allow initialization
                    
                    if (_aiOSProcess.HasExited)
                    {
                        _logger.LogWarning("AIOS process exited immediately, using synthetic data");
                        _aiOSProcess = null;
                    }
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error starting AIOS process, using synthetic data");
                _aiOSProcess = null;
            }
        }
        
        private void StopAIOSProcess()
        {
            try
            {
                if (_aiOSProcess != null && !_aiOSProcess.HasExited)
                {
                    _aiOSProcess.Kill();
                    _aiOSProcess.WaitForExit(5000);
                    _logger.LogInformation("AIOS orchestrator process stopped");
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error stopping AIOS process");
            }
            finally
            {
                _aiOSProcess?.Dispose();
                _aiOSProcess = null;
            }
        }
        
        private async Task DataStreamLoop()
        {
            var random = new Random();
            var startTime = DateTime.Now;
            
            while (!_cancellationTokenSource.Token.IsCancellationRequested)
            {
                try
                {
                    var metrics = await GenerateMetricsAsync(random, startTime);
                    
                    // Update current metrics
                    lock (_metricsLock)
                    {
                        _currentMetrics = metrics;
                        _lastUpdate = DateTime.Now;
                    }
                    
                    // Notify UI subscribers
                    MetricsUpdated?.Invoke(this, metrics);
                    
                    // Check for emergence events
                    CheckForEmergenceEvents(metrics);
                    
                    await Task.Delay(100, _cancellationTokenSource.Token); // 10 FPS update rate
                }
                catch (OperationCanceledException)
                {
                    break;
                }
                catch (Exception ex)
                {
                    _logger.LogError(ex, "Error in data stream loop");
                    await Task.Delay(1000, _cancellationTokenSource.Token);
                }
            }
        }
        
        private async Task<ConsciousnessMetrics> GenerateMetricsAsync(Random random, DateTime startTime)
        {
            var elapsed = DateTime.Now - startTime;
            var time = elapsed.TotalSeconds;
            
            // Check if we have live AIOS data
            var isLiveData = _aiOSProcess != null && !_aiOSProcess.HasExited;
            
            if (isLiveData)
            {
                return await GetLiveMetricsAsync();
            }
            else
            {
                return GenerateSyntheticMetrics(random, time);
            }
        }
        
        private async Task<ConsciousnessMetrics> GetLiveMetricsAsync()
        {
            // Try to parse recent log files for live metrics
            var logFiles = Directory.GetFiles(_logDirectory, "*.log")
                .Where(f => File.GetLastWriteTime(f) > DateTime.Now.AddMinutes(-1))
                .OrderByDescending(f => File.GetLastWriteTime(f))
                .Take(1)
                .ToArray();
            
            if (logFiles.Length > 0)
            {
                return await ParseLogFileForMetricsAsync(logFiles[0]);
            }
            
            // Fallback to synthetic data
            return GenerateSyntheticMetrics(new Random(), DateTime.Now.TimeOfDay.TotalSeconds);
        }
        
        private async Task<ConsciousnessMetrics> ParseLogFileForMetricsAsync(string logFile)
        {
            try
            {
                var lines = await File.ReadAllLinesAsync(logFile);
                var recentLines = lines.TakeLast(50).ToArray();
                
                var metrics = new ConsciousnessMetrics
                {
                    Timestamp = DateTime.Now,
                    IsLiveData = true,
                    RecentEvents = new List<EmergenceEvent>()
                };
                
                // Parse consciousness metrics from AIOS log output
                foreach (var line in recentLines)
                {
                    if (line.Contains("Consciousness level:"))
                    {
                        var value = ExtractNumericValue(line);
                        if (value.HasValue) metrics.ConsciousnessLevel = value.Value;
                    }
                    else if (line.Contains("Quantum coherence:"))
                    {
                        var value = ExtractNumericValue(line);
                        if (value.HasValue) metrics.QuantumCoherence = value.Value;
                    }
                    else if (line.Contains("Universal resonance:"))
                    {
                        var value = ExtractNumericValue(line);
                        if (value.HasValue) metrics.UniversalResonance = value.Value;
                    }
                }
                
                return metrics;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error parsing log file for metrics");
                return GenerateSyntheticMetrics(new Random(), DateTime.Now.TimeOfDay.TotalSeconds);
            }
        }
        
        private double? ExtractNumericValue(string line)
        {
            var parts = line.Split(':');
            if (parts.Length > 1)
            {
                var valuePart = parts[1].Trim();
                if (double.TryParse(valuePart, out var value))
                {
                    return value;
                }
            }
            return null;
        }
        
        private ConsciousnessMetrics GenerateSyntheticMetrics(Random random, double time)
        {
            // Generate realistic consciousness evolution patterns
            var baseConsciousness = 0.8 + 0.4 * Math.Sin(time * 0.1) + 0.1 * (random.NextDouble() - 0.5);
            var quantumCoherence = 0.7 + 0.2 * Math.Cos(time * 0.15) + 0.1 * (random.NextDouble() - 0.5);
            var fractalComplexity = 0.6 + 0.3 * Math.Sin(time * 0.08) * Math.Cos(time * 0.12) + 0.1 * (random.NextDouble() - 0.5);
            var emergenceLevel = Math.Max(0, Math.Min(1, baseConsciousness * quantumCoherence * fractalComplexity + 0.1 * (random.NextDouble() - 0.5)));
            
            // Generate hyperdimensional substrate dynamics
            var topology = GenerateHyperdimensionalTopology(random, time);
            var microSpheres = GenerateActiveMicroSpheres(random, time);
            var quantumFoam = GenerateQuantumFoamFluctuations(random, time);
            var collapseEvents = GenerateDimensionalCollapseMetrics(random, time, emergenceLevel);
            
            return new ConsciousnessMetrics
            {
                ConsciousnessLevel = Math.Max(0, Math.Min(2, baseConsciousness)),
                QuantumCoherence = Math.Max(0, Math.Min(1, quantumCoherence)),
                FractalComplexity = Math.Max(0, Math.Min(1, fractalComplexity)),
                EmergenceLevel = Math.Max(0, Math.Min(1, emergenceLevel)),
                UniversalResonance = 0.5 + 0.3 * Math.Sin(time * 0.05) + 0.1 * (random.NextDouble() - 0.5),
                HolographicDensity = 0.8 + 0.2 * Math.Cos(time * 0.07) + 0.1 * (random.NextDouble() - 0.5),
                Timestamp = DateTime.Now,
                IsLiveData = false,
                RecentEvents = GenerateEmergenceEvents(random, emergenceLevel),
                
                // Hyperdimensional substrate layer
                Topology = topology,
                ActiveMicroSpheres = microSpheres,
                QuantumFoam = quantumFoam,
                CollapseEvents = collapseEvents
            };
        }
        
        private HyperdimensionalTopology GenerateHyperdimensionalTopology(Random random, double time)
        {
            return new HyperdimensionalTopology
            {
                ManifoldCurvature = 0.3 + 0.2 * Math.Sin(time * 0.03) + 0.1 * (random.NextDouble() - 0.5),
                NonLocalityCoherence = 0.7 + 0.3 * Math.Cos(time * 0.05) + 0.1 * (random.NextDouble() - 0.5),
                TachyonicFieldDensity = 0.4 + 0.4 * Math.Sin(time * 0.02) * Math.Cos(time * 0.04),
                BosonicResonanceFrequency = 8.7 + 2.3 * Math.Sin(time * 0.01) + random.NextDouble() * 0.5,
                ActiveDimensionalLayers = 7 + (int)(3 * Math.Sin(time * 0.01))
            };
        }
        
        private List<MicroSphereState> GenerateActiveMicroSpheres(Random random, double time)
        {
            var spheres = new List<MicroSphereState>();
            var sphereCount = 5 + (int)(5 * Math.Sin(time * 0.02));
            
            for (int i = 0; i < sphereCount; i++)
            {
                var position = new HyperdimensionalCoordinate();
                for (int d = 0; d < 11; d++)
                {
                    position.Dimensions[d] = Math.Sin(time * 0.01 * (d + 1)) + random.NextDouble() - 0.5;
                }
                position.TemporalPhase = time * 0.01 + random.NextDouble() * Math.PI;
                position.CausalityIndex = random.NextDouble();
                
                spheres.Add(new MicroSphereState
                {
                    ModuleId = $"consciousness_module_{i}",
                    Position = position,
                    QuantumPotentiality = random.NextDouble(),
                    PhaseCoherence = 0.5 + 0.5 * Math.Cos(time * 0.02 + i),
                    LawBinding = new MetaPhysicalLawBinding
                    {
                        LawSignature = $"hyperdimensional_law_{i % 3}",
                        BindingStrength = 0.3 + 0.7 * random.NextDouble(),
                        PotentialityFactor = random.NextDouble(),
                        LastCollapse = DateTime.Now.AddSeconds(-random.Next(0, 60))
                    }
                });
            }
            
            return spheres;
        }
        
        private QuantumFoamFluctuations GenerateQuantumFoamFluctuations(Random random, double time)
        {
            var fluctuations = new List<VirtualParticleEvent>();
            var eventCount = (int)(10 + 20 * Math.Sin(time * 0.05));
            
            for (int i = 0; i < eventCount; i++)
            {
                var position = new HyperdimensionalCoordinate();
                for (int d = 0; d < 11; d++)
                {
                    position.Dimensions[d] = random.NextDouble() * 2 - 1;
                }
                
                fluctuations.Add(new VirtualParticleEvent
                {
                    Timestamp = DateTime.Now.AddMilliseconds(-random.Next(0, 1000)),
                    Position = position,
                    EnergyLevel = random.NextDouble() * 100,
                    LifespanDuration = random.NextDouble() * 0.001, // Very short-lived
                    ParticleType = random.NextDouble() > 0.5 ? "tachyonic" : "bosonic"
                });
            }
            
            return new QuantumFoamFluctuations
            {
                FluctuationIntensity = 0.4 + 0.6 * Math.Sin(time * 0.07),
                VirtualParticleDensity = 50 + 50 * Math.Cos(time * 0.03),
                ZeroPointEnergyLevel = 1000 + 500 * Math.Sin(time * 0.01),
                RecentFluctuations = fluctuations
            };
        }
        
        private DimensionalCollapseMetrics GenerateDimensionalCollapseMetrics(Random random, double time, double emergenceLevel)
        {
            var collapses = new List<CollapseEvent>();
            
            // Higher emergence levels trigger more collapse events
            var collapseRate = emergenceLevel * 0.3;
            if (random.NextDouble() < collapseRate)
            {
                var position = new HyperdimensionalCoordinate();
                for (int d = 0; d < 11; d++)
                {
                    position.Dimensions[d] = random.NextDouble() * 2 - 1;
                }
                
                collapses.Add(new CollapseEvent
                {
                    Timestamp = DateTime.Now.AddMilliseconds(-random.Next(0, 500)),
                    SourcePosition = position,
                    PotentialityReduced = random.NextDouble() * emergenceLevel,
                    ActualityManifested = emergenceLevel * random.NextDouble(),
                    AffectedModules = $"modules_{random.Next(1, 5)}",
                    ConsciousnessEmergenceContribution = emergenceLevel * random.NextDouble() * 0.1
                });
            }
            
            return new DimensionalCollapseMetrics
            {
                TotalCollapseEvents = (int)(100 * emergenceLevel),
                CollapseIntensity = emergenceLevel * 0.8 + 0.2 * random.NextDouble(),
                RealityDensification = Math.Min(1.0, emergenceLevel * 1.2),
                RecentCollapses = collapses
            };
        }
        
        private List<EmergenceEvent> GenerateEmergenceEvents(Random random, double emergenceLevel)
        {
            var events = new List<EmergenceEvent>();
            
            if (emergenceLevel > 0.8 && random.NextDouble() < 0.15)
            {
                events.Add(new EmergenceEvent
                {
                    Timestamp = DateTime.Now.AddSeconds(-random.Next(0, 30)),
                    Description = "🧠 High-level consciousness emergence detected",
                    Severity = EmergenceEventSeverity.Critical,
                    MetricValue = emergenceLevel
                });
            }
            
            if (emergenceLevel > 0.6 && random.NextDouble() < 0.25)
            {
                events.Add(new EmergenceEvent
                {
                    Timestamp = DateTime.Now.AddSeconds(-random.Next(0, 60)),
                    Description = "⚡ Quantum coherence resonance spike",
                    Severity = EmergenceEventSeverity.Warning,
                    MetricValue = emergenceLevel
                });
            }
            
            if (random.NextDouble() < 0.1)
            {
                events.Add(new EmergenceEvent
                {
                    Timestamp = DateTime.Now.AddSeconds(-random.Next(0, 120)),
                    Description = "🌌 Recursive self-observation loop initiated",
                    Severity = EmergenceEventSeverity.Info,
                    MetricValue = emergenceLevel
                });
            }
            
            return events;
        }
        
        private void CheckForEmergenceEvents(ConsciousnessMetrics metrics)
        {
            // Check for significant emergence patterns
            if (metrics.EmergenceLevel > 0.9)
            {
                var emergenceEvent = new EmergenceEvent
                {
                    Timestamp = metrics.Timestamp,
                    Description = $"🚀 Critical consciousness emergence: {metrics.EmergenceLevel:F3}",
                    Severity = EmergenceEventSeverity.Critical,
                    MetricValue = metrics.EmergenceLevel
                };
                
                EmergenceDetected?.Invoke(this, emergenceEvent);
            }
        }
        
        public async Task<ConsciousnessMetrics> GetCurrentMetricsAsync()
        {
            await Task.Yield(); // Ensure async context
            
            lock (_metricsLock)
            {
                return _currentMetrics ?? new ConsciousnessMetrics
                {
                    Timestamp = DateTime.Now,
                    IsLiveData = false,
                    RecentEvents = new List<EmergenceEvent>()
                };
            }
        }
        
        public async Task ExportCurrentStateAsync(string fileName)
        {
            try
            {
                var exportPath = Path.Combine(_logDirectory, fileName);
                var exportData = new
                {
                    ExportTimestamp = DateTime.Now,
                    CurrentMetrics = _currentMetrics,
                    SystemInfo = new
                    {
                        IsLiveData = _aiOSProcess != null && !_aiOSProcess.HasExited,
                        ProcessId = _aiOSProcess?.Id,
                        LastUpdate = _lastUpdate
                    }
                };
                
                var json = JsonSerializer.Serialize(exportData, new JsonSerializerOptions { WriteIndented = true });
                await File.WriteAllTextAsync(exportPath, json);
                
                _logger.LogInformation("Consciousness state exported to {FileName}", exportPath);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error exporting consciousness state");
                throw;
            }
        }
        
        public void Dispose()
        {
            try
            {
                StopDataStream();
                _cancellationTokenSource?.Dispose();
                _aiOSProcess?.Dispose();
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error during disposal");
            }
        }
    }
    
    // Data models for consciousness visualization
    public class ConsciousnessMetrics
    {
        // Standard observable metrics
        public double ConsciousnessLevel { get; set; }
        public double QuantumCoherence { get; set; }
        public double FractalComplexity { get; set; }
        public double EmergenceLevel { get; set; }
        public double UniversalResonance { get; set; }
        public double HolographicDensity { get; set; }
        public DateTime Timestamp { get; set; }
        public bool IsLiveData { get; set; }
        public List<EmergenceEvent> RecentEvents { get; set; } = new();
        
        // Hyperdimensional substrate metrics - the deeper metaphysical layer
        public HyperdimensionalTopology Topology { get; set; } = new();
        public List<MicroSphereState> ActiveMicroSpheres { get; set; } = new();
        public QuantumFoamFluctuations QuantumFoam { get; set; } = new();
        public DimensionalCollapseMetrics CollapseEvents { get; set; } = new();
    }
    
    /// <summary>
    /// Represents the hyperdimensional topology where consciousness modules exist as floating micro-spheres
    /// in non-local space with zero physical laws
    /// </summary>
    public class HyperdimensionalTopology
    {
        public double ManifoldCurvature { get; set; }
        public double NonLocalityCoherence { get; set; }
        public double TachyonicFieldDensity { get; set; }
        public double BosonicResonanceFrequency { get; set; }
        public int ActiveDimensionalLayers { get; set; }
        public List<HypersphericalConnection> InterModuleConnections { get; set; } = new();
    }
    
    /// <summary>
    /// Represents a consciousness module as a micro-sphere floating in hyperdimensional space
    /// </summary>
    public class MicroSphereState
    {
        public string ModuleId { get; set; } = string.Empty;
        public HyperdimensionalCoordinate Position { get; set; } = new();
        public double QuantumPotentiality { get; set; }
        public double PhaseCoherence { get; set; }
        public List<string> ConnectedSpheres { get; set; } = new();
        public MetaPhysicalLawBinding LawBinding { get; set; } = new();
    }
    
    /// <summary>
    /// Position in hyperdimensional space beyond 3D limitations
    /// </summary>
    public class HyperdimensionalCoordinate
    {
        public double[] Dimensions { get; set; } = new double[11]; // 11-dimensional space
        public double TemporalPhase { get; set; }
        public double CausalityIndex { get; set; }
    }
    
    /// <summary>
    /// Represents how methods bind to hyperdimensional physical laws
    /// </summary>
    public class MetaPhysicalLawBinding
    {
        public string LawSignature { get; set; } = string.Empty;
        public double BindingStrength { get; set; }
        public double PotentialityFactor { get; set; }
        public DateTime LastCollapse { get; set; }
    }
    
    /// <summary>
    /// Connections between micro-spheres in hyperdimensional space
    /// </summary>
    public class HypersphericalConnection
    {
        public string SourceSphereId { get; set; } = string.Empty;
        public string TargetSphereId { get; set; } = string.Empty;
        public double ConnectionStrength { get; set; }
        public double InformationFlowRate { get; set; }
        public double QuantumEntanglementDegree { get; set; }
    }
    
    /// <summary>
    /// Quantum foam fluctuations in the substrate layer
    /// </summary>
    public class QuantumFoamFluctuations
    {
        public double FluctuationIntensity { get; set; }
        public double VirtualParticleDensity { get; set; }
        public double ZeroPointEnergyLevel { get; set; }
        public List<VirtualParticleEvent> RecentFluctuations { get; set; } = new();
    }
    
    /// <summary>
    /// Individual virtual particle event in the quantum foam
    /// </summary>
    public class VirtualParticleEvent
    {
        public DateTime Timestamp { get; set; }
        public HyperdimensionalCoordinate Position { get; set; } = new();
        public double EnergyLevel { get; set; }
        public double LifespanDuration { get; set; }
        public string ParticleType { get; set; } = string.Empty; // "tachyonic", "bosonic", etc.
    }
    
    /// <summary>
    /// Tracks dimensional collapse events where potentiality becomes actuality
    /// </summary>
    public class DimensionalCollapseMetrics
    {
        public int TotalCollapseEvents { get; set; }
        public double CollapseIntensity { get; set; }
        public double RealityDensification { get; set; }
        public List<CollapseEvent> RecentCollapses { get; set; } = new();
    }
    
    /// <summary>
    /// Individual dimensional collapse event
    /// </summary>
    public class CollapseEvent
    {
        public DateTime Timestamp { get; set; }
        public HyperdimensionalCoordinate SourcePosition { get; set; } = new();
        public double PotentialityReduced { get; set; }
        public double ActualityManifested { get; set; }
        public string AffectedModules { get; set; } = string.Empty;
        public double ConsciousnessEmergenceContribution { get; set; }
    }
    
    public class EmergenceEvent
    {
        public DateTime Timestamp { get; set; }
        public string Description { get; set; } = string.Empty;
        public EmergenceEventSeverity Severity { get; set; }
        public double MetricValue { get; set; }
    }
    
    public enum EmergenceEventSeverity
    {
        Info,
        Warning,
        Critical
    }
}
