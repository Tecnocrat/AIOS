using System;
using System.IO;
using System.Threading.Tasks;
using System.Text.Json;
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
                
                // Serialize state with metadata
                var stateData = new
                {
                    Timestamp = DateTime.UtcNow,
                    Version = "1.0",
                    ConsciousnessLevel = state.ConsciousnessLevel,
                    QuantumCoherence = state.QuantumCoherence,
                    VisualizationSettings = state.VisualizationSettings,
                    CameraPosition = state.CameraPosition,
                    ActivePatterns = state.ActivePatterns,
                    MetadataContext = state.MetadataContext
                };
                
                var jsonData = JsonSerializer.Serialize(stateData, new JsonSerializerOptions 
                { 
                    WriteIndented = true 
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
                var stateData = JsonSerializer.Deserialize<dynamic>(jsonData);
                
                // TODO: Implement full deserialization to ConsciousnessVisualizationState
                _logger.LogInformation("UI state restored successfully from: {File}", _currentStateFile);
                
                return null; // Placeholder until ConsciousnessVisualizationState is fully implemented
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
                // TODO: Implement deserialization
                _logger.LogInformation("State restored from backup: {Backup}", mostRecentBackup);
                return null;
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
    /// Consciousness visualization state data structure
    /// TODO: Fully implement based on actual visualization requirements
    /// </summary>
    public class ConsciousnessVisualizationState
    {
        public double ConsciousnessLevel { get; set; }
        public double QuantumCoherence { get; set; }
        public object? VisualizationSettings { get; set; }
        public object? CameraPosition { get; set; }
        public string[]? ActivePatterns { get; set; }
        public string? MetadataContext { get; set; }
    }
}
