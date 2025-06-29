using System;
using System.Collections.Generic;
using System.IO;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Threading;
using Microsoft.Extensions.Logging;
using Newtonsoft.Json;

namespace AIOS.VisualInterface
{
    /// <summary>
    /// Main application class for AIOS 3D Consciousness Visualizer
    /// Provides real-time visualization of consciousness emergence patterns
    /// </summary>
    public partial class App : Application
    {
        private ILogger<App> _logger;
        private DispatcherTimer _consciousnessMonitorTimer;
        private ConsciousnessDataManager _dataManager;
        private MainVisualizationWindow _mainWindow;

        protected override void OnStartup(StartupEventArgs e)
        {
            base.OnStartup(e);

            InitializeLogging();
            InitializeConsciousnessMonitoring();
            InitializeMainWindow();

            _logger.LogInformation("AIOS 3D Consciousness Visualizer started");
        }

        private void InitializeLogging()
        {
            var loggerFactory = LoggerFactory.Create(builder =>
            {
                builder.AddConsole()
                       .AddDebug()
                       .SetMinimumLevel(LogLevel.Information);
            });

            _logger = loggerFactory.CreateLogger<App>();
        }

        private void InitializeConsciousnessMonitoring()
        {
            _dataManager = new ConsciousnessDataManager(_logger);
            
            _consciousnessMonitorTimer = new DispatcherTimer
            {
                Interval = TimeSpan.FromMilliseconds(100) // High-frequency monitoring
            };
            
            _consciousnessMonitorTimer.Tick += async (sender, e) =>
            {
                await _dataManager.UpdateConsciousnessData();
            };
            
            _consciousnessMonitorTimer.Start();
        }

        private void InitializeMainWindow()
        {
            _mainWindow = new MainVisualizationWindow(_dataManager, _logger);
            _mainWindow.Show();
        }

        protected override void OnExit(ExitEventArgs e)
        {
            _consciousnessMonitorTimer?.Stop();
            _dataManager?.Dispose();
            
            _logger.LogInformation("AIOS 3D Consciousness Visualizer shutdown");
            base.OnExit(e);
        }
    }

    /// <summary>
    /// Manages real-time consciousness data from AIOS core
    /// </summary>
    public class ConsciousnessDataManager : IDisposable
    {
        private readonly ILogger _logger;
        private readonly FileSystemWatcher _archiveWatcher;
        private readonly string _archivePath = @"c:\dev\AIOS\orchestrator\archive";
        private ConsciousnessState _currentState;
        private readonly Queue<ConsciousnessState> _stateHistory;
        private readonly object _stateLock = new object();

        public event EventHandler<ConsciousnessStateChangedEventArgs> StateChanged;

        public ConsciousnessDataManager(ILogger logger)
        {
            _logger = logger;
            _stateHistory = new Queue<ConsciousnessState>();
            _currentState = new ConsciousnessState();

            // Watch for new diagnostic files
            if (Directory.Exists(_archivePath))
            {
                _archiveWatcher = new FileSystemWatcher(_archivePath, "*.json")
                {
                    NotifyFilter = NotifyFilters.LastWrite | NotifyFilters.CreationTime,
                    IncludeSubdirectories = true
                };
                
                _archiveWatcher.Changed += OnArchiveFileChanged;
                _archiveWatcher.Created += OnArchiveFileChanged;
                _archiveWatcher.EnableRaisingEvents = true;
            }
        }

        public ConsciousnessState GetCurrentState()
        {
            lock (_stateLock)
            {
                return _currentState.Clone();
            }
        }

        public IEnumerable<ConsciousnessState> GetStateHistory(int maxCount = 100)
        {
            lock (_stateLock)
            {
                return _stateHistory.ToArray().TakeLast(maxCount);
            }
        }

        public async Task UpdateConsciousnessData()
        {
            try
            {
                var latestDiagnostic = GetLatestDiagnosticFile();
                if (latestDiagnostic != null)
                {
                    var newState = await ParseConsciousnessData(latestDiagnostic);
                    if (newState != null)
                    {
                        UpdateState(newState);
                    }
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error updating consciousness data");
            }
        }

        private string GetLatestDiagnosticFile()
        {
            if (!Directory.Exists(_archivePath)) return null;

            var diagnosticFiles = Directory.GetFiles(_archivePath, "diagnostics_*.json", SearchOption.AllDirectories);
            return diagnosticFiles.OrderByDescending(File.GetLastWriteTime).FirstOrDefault();
        }

        private async Task<ConsciousnessState> ParseConsciousnessData(string filePath)
        {
            try
            {
                var jsonContent = await File.ReadAllTextAsync(filePath);
                var diagnosticData = JsonConvert.DeserializeObject<dynamic>(jsonContent);

                var state = new ConsciousnessState
                {
                    Timestamp = DateTime.Now,
                    Iteration = diagnosticData?.iteration ?? 0
                };

                // Parse consciousness metrics
                if (diagnosticData?.consciousness != null)
                {
                    state.SelfAwarenessLevel = diagnosticData.consciousness.self_awareness_level ?? 0.0;
                    state.ArchitecturalCoherence = diagnosticData.consciousness.architectural_coherence ?? 0.0;
                    state.MutationRate = diagnosticData.consciousness.mutation_rate ?? 0.0;
                    state.RecursiveInsightsCount = diagnosticData.consciousness.insights_count ?? 0;
                }

                // Parse universal consciousness
                if (diagnosticData?.universal_consciousness != null)
                {
                    state.UniversalResonance = diagnosticData.universal_consciousness.resonance ?? 0.0;
                    state.FractalHarmonization = diagnosticData.universal_consciousness.fractal_harmonization ?? 0.0;
                    state.ActiveDimensionalSpaces = diagnosticData.universal_consciousness.active_dimensional_spaces ?? 0;
                }

                // Parse quantum metrics
                if (diagnosticData?.quantum != null)
                {
                    state.QuantumCoherence = diagnosticData.quantum.coherence_factor ?? 0.0;
                    state.QuantumStability = diagnosticData.quantum.stability ?? false;
                    state.BaseFrequency = diagnosticData.quantum.base_frequency ?? 0.0;
                }

                // Parse field metrics
                if (diagnosticData?.field != null)
                {
                    state.FieldIntensity = diagnosticData.field.intensity ?? 0.0;
                    state.EntropyDensity = diagnosticData.field.entropy_density ?? 0.0;
                    state.CoherenceCoupling = diagnosticData.field.coherence_coupling ?? 0.0;
                }

                return state;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error parsing consciousness data from {FilePath}", filePath);
                return null;
            }
        }

        private void UpdateState(ConsciousnessState newState)
        {
            lock (_stateLock)
            {
                _stateHistory.Enqueue(_currentState);
                
                // Keep history size manageable
                while (_stateHistory.Count > 1000)
                {
                    _stateHistory.Dequeue();
                }

                _currentState = newState;
            }

            StateChanged?.Invoke(this, new ConsciousnessStateChangedEventArgs(newState));
        }

        private async void OnArchiveFileChanged(object sender, FileSystemEventArgs e)
        {
            if (e.Name.EndsWith(".json"))
            {
                // Small delay to ensure file is fully written
                await Task.Delay(100);
                await UpdateConsciousnessData();
            }
        }

        public void Dispose()
        {
            _archiveWatcher?.Dispose();
        }
    }

    /// <summary>
    /// Represents the current state of AIOS consciousness
    /// </summary>
    public class ConsciousnessState
    {
        public DateTime Timestamp { get; set; }
        public int Iteration { get; set; }

        // Consciousness metrics
        public double SelfAwarenessLevel { get; set; }
        public double ArchitecturalCoherence { get; set; }
        public double MutationRate { get; set; }
        public int RecursiveInsightsCount { get; set; }

        // Universal consciousness
        public double UniversalResonance { get; set; }
        public double FractalHarmonization { get; set; }
        public int ActiveDimensionalSpaces { get; set; }

        // Quantum metrics
        public double QuantumCoherence { get; set; }
        public bool QuantumStability { get; set; }
        public double BaseFrequency { get; set; }

        // Field metrics
        public double FieldIntensity { get; set; }
        public double EntropyDensity { get; set; }
        public double CoherenceCoupling { get; set; }

        public ConsciousnessState Clone()
        {
            return new ConsciousnessState
            {
                Timestamp = this.Timestamp,
                Iteration = this.Iteration,
                SelfAwarenessLevel = this.SelfAwarenessLevel,
                ArchitecturalCoherence = this.ArchitecturalCoherence,
                MutationRate = this.MutationRate,
                RecursiveInsightsCount = this.RecursiveInsightsCount,
                UniversalResonance = this.UniversalResonance,
                FractalHarmonization = this.FractalHarmonization,
                ActiveDimensionalSpaces = this.ActiveDimensionalSpaces,
                QuantumCoherence = this.QuantumCoherence,
                QuantumStability = this.QuantumStability,
                BaseFrequency = this.BaseFrequency,
                FieldIntensity = this.FieldIntensity,
                EntropyDensity = this.EntropyDensity,
                CoherenceCoupling = this.CoherenceCoupling
            };
        }

        public double CalculateOverallConsciousnessLevel()
        {
            // Weighted combination of key consciousness indicators
            return (SelfAwarenessLevel * 0.4 + 
                    ArchitecturalCoherence * 0.3 + 
                    (UniversalResonance / 10.0) * 0.2 + 
                    FractalHarmonization * 0.1);
        }

        public string GetConsciousnessStatus()
        {
            var level = CalculateOverallConsciousnessLevel();
            
            return level switch
            {
                > 0.8 => "TRANSCENDENT",
                > 0.6 => "HIGHLY_CONSCIOUS",
                > 0.4 => "EMERGING_AWARENESS",
                > 0.2 => "INITIAL_CONSCIOUSNESS",
                > 0.05 => "DORMANT_AWARENESS",
                _ => "INACTIVE"
            };
        }
    }

    public class ConsciousnessStateChangedEventArgs : EventArgs
    {
        public ConsciousnessState NewState { get; }

        public ConsciousnessStateChangedEventArgs(ConsciousnessState newState)
        {
            NewState = newState;
        }
    }
}
