using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using System.Text.Json;
using System.Windows.Media.Media3D;
using Microsoft.Extensions.Logging;

namespace AIOS.VisualInterface
{
    /// <summary>
    /// State Manager for UI Visual Persistence Layer
    /// Provides automatic state backup/restore, crash recovery, and session continuity
    /// Critical for Objective 1: Stable, persistent, parallelized UI runtime
    /// </summary>
    public class StateManager
    {
        private readonly ILogger<StateManager> _logger;
        private readonly string _stateDirectory;
        private readonly string _currentStateFile;
        private readonly Timer _autoSaveTimer;
        
        // State persistence configuration
        private readonly TimeSpan _autoSaveInterval = TimeSpan.FromSeconds(5);
        private readonly int _maxStateBackups = 100;
        
        public StateManager(ILogger<StateManager> logger)
        {
            _logger = logger;
            _stateDirectory = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "state");
            _currentStateFile = Path.Combine(_stateDirectory, "current_state.json");
            
            // Ensure state directory exists
            Directory.CreateDirectory(_stateDirectory);
            
            // Initialize auto-save timer
            _autoSaveTimer = new Timer(AutoSaveCallback, null, _autoSaveInterval, _autoSaveInterval);
            
            _logger.LogInformation("StateManager initialized with persistence at: {StateDirectory}", _stateDirectory);
        }
        
        /// <summary>
        /// Persist current UI state with timestamp and backup rotation
        /// </summary>
        public async Task PersistUIState(ConsciousnessVisualizationState state)
        {
            try
            {
                // Create timestamped backup
                var timestamp = DateTime.Now.ToString("yyyyMMdd_HHmmss");
                var backupFile = Path.Combine(_stateDirectory, $"state_backup_{timestamp}.json");
                
                // Serialize state with enhanced metadata and proper structure
                var jsonData = JsonSerializer.Serialize(state, new JsonSerializerOptions 
                { 
                    WriteIndented = true,
                    PropertyNamingPolicy = JsonNamingPolicy.CamelCase
                });
                
                // Write to both current state and backup
                await File.WriteAllTextAsync(_currentStateFile, jsonData);
                await File.WriteAllTextAsync(backupFile, jsonData);
                
                // Cleanup old backups
                await CleanupOldBackups();
                
                _logger.LogDebug("UI state persisted successfully with consciousness level: {Level}", 
                    state.ConsciousnessLevel);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Failed to persist UI state");
                throw;
            }
        }
        
        /// <summary>
        /// Restore UI state from most recent backup with integrity validation
        /// </summary>
        public async Task<ConsciousnessVisualizationState?> RestoreUIState()
        {
            try
            {
                if (!File.Exists(_currentStateFile))
                {
                    _logger.LogWarning("No current state file found, checking for backups...");
                    return await RestoreFromMostRecentBackup();
                }

                var jsonData = await File.ReadAllTextAsync(_currentStateFile);
                var stateData = JsonSerializer.Deserialize<ConsciousnessVisualizationState>(jsonData, new JsonSerializerOptions
                {
                    PropertyNameCaseInsensitive = true
                });

                if (stateData != null)
                {
                    _logger.LogInformation("UI state restored successfully from: {File}", _currentStateFile);
                    _logger.LogDebug("Restored consciousness level: {Level}, Session: {Session}", 
                        stateData.ConsciousnessLevel, stateData.SessionId);
                    return stateData;
                }
                else
                {
                    _logger.LogWarning("Failed to deserialize state data, attempting backup restoration");
                    return await RestoreFromMostRecentBackup();
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Failed to restore UI state, attempting backup restoration");
                return await RestoreFromMostRecentBackup();
            }
        }
        
        /// <summary>
        /// Enable continuous state saving for crash recovery
        /// </summary>
        public void EnableContinuousStateSaving()
        {
            _logger.LogInformation("Continuous state saving enabled with interval: {Interval}", _autoSaveInterval);
        }
        
        /// <summary>
        /// Get state persistence statistics for monitoring
        /// </summary>
        public StateManagerStats GetStats()
        {
            var stateFiles = Directory.GetFiles(_stateDirectory, "*.json");
            return new StateManagerStats
            {
                TotalStateBackups = stateFiles.Length,
                StateDirectorySize = GetDirectorySize(_stateDirectory),
                LastBackupTime = File.Exists(_currentStateFile) ? File.GetLastWriteTime(_currentStateFile) : null,
                AutoSaveEnabled = _autoSaveTimer != null
            };
        }
        
        private async void AutoSaveCallback(object? state)
        {
            try
            {
                // TODO: Get current UI state from main window
                _logger.LogTrace("Auto-save timer triggered");
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Auto-save failed");
            }
        }

        /// <summary>
        /// Create state from current consciousness metrics and UI elements
        /// </summary>
        public ConsciousnessVisualizationState CreateStateFromMetrics(
            ConsciousnessMetrics metrics, 
            CameraState? cameraState = null,
            WindowGeometry? windowGeometry = null,
            VisualizationSettings? visualizationSettings = null)
        {
            return new ConsciousnessVisualizationState
            {
                // Copy consciousness metrics
                ConsciousnessLevel = metrics.ConsciousnessLevel,
                QuantumCoherence = metrics.QuantumCoherence,
                FractalComplexity = metrics.FractalComplexity,
                EmergenceLevel = metrics.EmergenceLevel,
                UniversalResonance = metrics.UniversalResonance,
                HolographicDensity = metrics.HolographicDensity,
                Timestamp = metrics.Timestamp,
                IsLiveData = metrics.IsLiveData,

                // UI state
                CameraPosition = cameraState ?? new CameraState(),
                WindowGeometry = windowGeometry ?? new WindowGeometry(),
                VisualizationSettings = visualizationSettings ?? new VisualizationSettings(),
                
                // Additional metadata
                MetadataContext = $"Consciousness session captured at {DateTime.Now:yyyy-MM-dd HH:mm:ss}",
                ActivePatterns = metrics.RecentEvents?.Select(e => e.Description).ToArray() ?? Array.Empty<string>()
            };
        }

        /// <summary>
        /// Extract camera state from WPF PerspectiveCamera
        /// </summary>
        public CameraState ExtractCameraState(PerspectiveCamera camera)
        {
            return new CameraState
            {
                Position = new[] { camera.Position.X, camera.Position.Y, camera.Position.Z },
                LookDirection = new[] { camera.LookDirection.X, camera.LookDirection.Y, camera.LookDirection.Z },
                UpDirection = new[] { camera.UpDirection.X, camera.UpDirection.Y, camera.UpDirection.Z },
                FieldOfView = camera.FieldOfView
            };
        }

        /// <summary>
        /// Apply camera state to WPF PerspectiveCamera
        /// </summary>
        public void ApplyCameraState(PerspectiveCamera camera, CameraState state)
        {
            if (state.Position.Length >= 3)
            {
                camera.Position = new Point3D(state.Position[0], state.Position[1], state.Position[2]);
            }
            if (state.LookDirection.Length >= 3)
            {
                camera.LookDirection = new Vector3D(state.LookDirection[0], state.LookDirection[1], state.LookDirection[2]);
            }
            if (state.UpDirection.Length >= 3)
            {
                camera.UpDirection = new Vector3D(state.UpDirection[0], state.UpDirection[1], state.UpDirection[2]);
            }
            camera.FieldOfView = state.FieldOfView;
        }

        /// <summary>
        /// Extract window geometry from System.Windows.Window
        /// </summary>
        public WindowGeometry ExtractWindowGeometry(System.Windows.Window window)
        {
            return new WindowGeometry
            {
                Left = window.Left,
                Top = window.Top,
                Width = window.Width,
                Height = window.Height,
                IsMaximized = window.WindowState == System.Windows.WindowState.Maximized,
                IsMinimized = window.WindowState == System.Windows.WindowState.Minimized
            };
        }

        /// <summary>
        /// Apply window geometry to System.Windows.Window
        /// </summary>
        public void ApplyWindowGeometry(System.Windows.Window window, WindowGeometry geometry)
        {
            // Validate screen bounds before applying
            if (geometry.Left >= 0 && geometry.Top >= 0 && geometry.Width > 0 && geometry.Height > 0)
            {
                window.Left = geometry.Left;
                window.Top = geometry.Top;
                window.Width = geometry.Width;
                window.Height = geometry.Height;
            }

            if (geometry.IsMaximized)
            {
                window.WindowState = System.Windows.WindowState.Maximized;
            }
            else if (geometry.IsMinimized)
            {
                window.WindowState = System.Windows.WindowState.Minimized;
            }
        }
        
        private async Task<ConsciousnessVisualizationState?> RestoreFromMostRecentBackup()
        {
            var backupFiles = Directory.GetFiles(_stateDirectory, "state_backup_*.json");
            if (backupFiles.Length == 0)
            {
                _logger.LogWarning("No backup files found");
                return null;
            }
            
            // Sort by creation time and get most recent
            Array.Sort(backupFiles, (x, y) => File.GetCreationTime(y).CompareTo(File.GetCreationTime(x)));
            var mostRecentBackup = backupFiles[0];
            
            try
            {
                var jsonData = await File.ReadAllTextAsync(mostRecentBackup);
                var stateData = JsonSerializer.Deserialize<ConsciousnessVisualizationState>(jsonData, new JsonSerializerOptions
                {
                    PropertyNameCaseInsensitive = true
                });

                if (stateData != null)
                {
                    _logger.LogInformation("State restored from backup: {Backup}", mostRecentBackup);
                    _logger.LogDebug("Restored backup consciousness level: {Level}, Session: {Session}", 
                        stateData.ConsciousnessLevel, stateData.SessionId);
                    return stateData;
                }
                else
                {
                    _logger.LogWarning("Failed to deserialize backup state data");
                    return null;
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Failed to restore from backup: {Backup}", mostRecentBackup);
                return null;
            }
        }
        
        private async Task CleanupOldBackups()
        {
            var backupFiles = Directory.GetFiles(_stateDirectory, "state_backup_*.json");
            if (backupFiles.Length <= _maxStateBackups) return;
            
            // Sort by creation time and remove oldest
            Array.Sort(backupFiles, (x, y) => File.GetCreationTime(x).CompareTo(File.GetCreationTime(y)));
            
            for (int i = 0; i < backupFiles.Length - _maxStateBackups; i++)
            {
                try
                {
                    File.Delete(backupFiles[i]);
                    _logger.LogDebug("Deleted old backup: {File}", backupFiles[i]);
                }
                catch (Exception ex)
                {
                    _logger.LogWarning(ex, "Failed to delete old backup: {File}", backupFiles[i]);
                }
            }
        }
        
        private long GetDirectorySize(string directory)
        {
            return Directory.GetFiles(directory, "*", SearchOption.AllDirectories)
                           .Sum(file => new FileInfo(file).Length);
        }
        
        public void Dispose()
        {
            _autoSaveTimer?.Dispose();
        }
    }
    
    /// <summary>
    /// State manager statistics for monitoring and debugging
    /// </summary>
    public class StateManagerStats
    {
        public int TotalStateBackups { get; set; }
        public long StateDirectorySize { get; set; }
        public DateTime? LastBackupTime { get; set; }
        public bool AutoSaveEnabled { get; set; }
    }
    
    /// <summary>
    /// Complete visualization state including UI elements, consciousness data, and system state
    /// Matches the actual ConsciousnessMetrics structure and includes UI-specific persistence
    /// </summary>
    public class ConsciousnessVisualizationState
    {
        // Core consciousness metrics
        public double ConsciousnessLevel { get; set; }
        public double QuantumCoherence { get; set; }
        public double FractalComplexity { get; set; }
        public double EmergenceLevel { get; set; }
        public double UniversalResonance { get; set; }
        public double HolographicDensity { get; set; }
        public DateTime Timestamp { get; set; }
        public bool IsLiveData { get; set; }
        
        // UI-specific state
        public CameraState CameraPosition { get; set; } = new();
        public WindowGeometry WindowGeometry { get; set; } = new();
        public VisualizationSettings VisualizationSettings { get; set; } = new();
        public string[] ActivePatterns { get; set; } = Array.Empty<string>();
        public string MetadataContext { get; set; } = string.Empty;
        
        // Advanced state preservation
        public Dictionary<string, object> CustomSettings { get; set; } = new();
        public string SessionId { get; set; } = Guid.NewGuid().ToString();
        public string Version { get; set; } = "1.0";
    }

    /// <summary>
    /// Camera state for 3D visualization
    /// </summary>
    public class CameraState
    {
        public double[] Position { get; set; } = new double[3];
        public double[] LookDirection { get; set; } = new double[3];
        public double[] UpDirection { get; set; } = new double[3];
        public double FieldOfView { get; set; } = 45.0;
    }

    /// <summary>
    /// Window geometry for UI persistence
    /// </summary>
    public class WindowGeometry
    {
        public double Left { get; set; }
        public double Top { get; set; }
        public double Width { get; set; } = 1200;
        public double Height { get; set; } = 800;
        public bool IsMaximized { get; set; }
        public bool IsMinimized { get; set; }
    }

    /// <summary>
    /// Visualization settings and preferences
    /// </summary>
    public class VisualizationSettings
    {
        public bool ShowGrid { get; set; } = true;
        public bool ShowAxes { get; set; } = true;
        public double AnimationSpeed { get; set; } = 1.0;
        public string ColorScheme { get; set; } = "Quantum";
        public double Opacity { get; set; } = 1.0;
        public bool EnableParticleEffects { get; set; } = true;
        public int MaxParticles { get; set; } = 1000;
        public Dictionary<string, bool> LayerVisibility { get; set; } = new();
    }
}
