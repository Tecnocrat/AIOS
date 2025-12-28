using System;
using System.Collections.Generic;
using System.Text.Json;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Threading;
using AIOS.Services;

namespace AIOS.UI.Controls
{
    /// <summary>
    /// Runtime Intelligence Control for Interface Supercell
    /// Manages communication with Runtime Intelligence tools which process
    /// through AI Intelligence engine via cytoplasm communication
    /// </summary>
    public partial class RuntimeIntelligenceControl : UserControl
    {
        private readonly RuntimeIntelligenceService _runtimeService;
        private readonly DispatcherTimer _healthCheckTimer;
        private bool _continuousMonitoring = false;
        private bool _disposed = false;

        public RuntimeIntelligenceControl()
        {
            InitializeComponent();
            _runtimeService = new RuntimeIntelligenceService();
            
            // Setup health check timer
            _healthCheckTimer = new DispatcherTimer
            {
                Interval = TimeSpan.FromSeconds(30)
            };
            _healthCheckTimer.Tick += HealthCheckTimer_Tick;
        }

        /// <summary>
        /// Initialize the Runtime Intelligence control asynchronously
        /// </summary>
        public async Task InitializeAsync()
        {
            try
            {
                await LoadAvailableToolsAsync();
                _healthCheckTimer.Start();
            }
            catch (Exception ex)
            {
                // Log error if needed
            }
        }

        private async void HealthCheckTimer_Tick(object sender, EventArgs e)
        {
            try
            {
                await CheckRuntimeHealthAsync();
            }
            catch (Exception ex)
            {
                // Log error
            }
        }

        /// <summary>
        /// Load available Runtime Intelligence tools
        /// </summary>
        private async Task LoadAvailableToolsAsync()
        {
            try
            {
                var result = await _runtimeService.GetAvailableToolsAsync();
                
                if (result.IsSuccess && result.Data is Dictionary<string, object> data &&
                    data.TryGetValue("tools", out var toolsObj) && 
                    toolsObj is List<RuntimeIntelligenceTool> tools)
                {
                    // Clear existing items
                    ToolsListBox.Items.Clear();
                    
                    // Add tool items
                    foreach (var tool in tools)
                    {
                        ToolsListBox.Items.Add(tool);
                    }
                    
                    ToolCountText.Text = tools.Count.ToString();
                }
                else
                {
                    ToolCountText.Text = "0";
                    LastOperationText.Text = "No tools available";
                }
            }
            catch (Exception ex)
            {
                LastOperationText.Text = $"Error loading tools: {ex.Message}";
            }
        }

        /// <summary>
        /// Check Runtime Intelligence system health
        /// </summary>
        private async Task CheckRuntimeHealthAsync()
        {
            try
            {
                var health = await _runtimeService.CheckSystemHealthAsync();
                
                // Update UI based on health status
                HealthStatusText.Text = health.Status;
                
                // Update last operation text
                LastOperationText.Text = $"Health check: {health.Status} - {DateTime.Now:HH:mm:ss}";
            }
            catch (Exception ex)
            {
                HealthStatusText.Text = "Health check failed";
                LastOperationText.Text = $"Health check failed: {ex.Message}";
            }
        }

        #region Event Handlers

        private async void VisualIntelligenceButton_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                LastOperationText.Text = "Processing visual intelligence...";
                
                var result = await _runtimeService.GetVisualIntelligenceAsync();
                
                if (result.IsSuccess)
                {
                    // Show results in a new window
                    var resultWindow = new RuntimeIntelligenceResultWindow();
                    resultWindow.DisplayResult(result);
                    resultWindow.Show();
                    
                    LastOperationText.Text = "Visual intelligence processing completed";
                }
                else
                {
                    LastOperationText.Text = $"Error: {result.Message}";
                }
            }
            catch (Exception ex)
            {
                LastOperationText.Text = $"Error processing visual intelligence: {ex.Message}";
            }
        }

        private async void SystemHealthButton_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                LastOperationText.Text = "Checking system health...";
                
                var health = await _runtimeService.CheckSystemHealthAsync();
                
                LastOperationText.Text = $"System Health: {health.Status}";
                HealthStatusText.Text = health.Status;
            }
            catch (Exception ex)
            {
                LastOperationText.Text = $"Error checking system health: {ex.Message}";
            }
        }

        private async void ContinuousMonitoringToggle_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                if (_continuousMonitoring)
                {
                    // Stop monitoring (simulate stopping)
                    _continuousMonitoring = false;
                    MonitoringStatusText.Text = "Stopped";
                    LastOperationText.Text = "Continuous monitoring stopped";
                }
                else
                {
                    // Start monitoring
                    var result = await _runtimeService.StartContinuousMonitoringAsync();
                    if (result.IsSuccess)
                    {
                        _continuousMonitoring = true;
                        MonitoringStatusText.Text = "Running";
                        LastOperationText.Text = "Continuous monitoring started";
                    }
                    else
                    {
                        LastOperationText.Text = $"Failed to start monitoring: {result.Message}";
                    }
                }
            }
            catch (Exception ex)
            {
                LastOperationText.Text = $"Error toggling monitoring: {ex.Message}";
            }
        }

        private void RefreshToolsButton_Click(object sender, RoutedEventArgs e)
        {
            _ = LoadAvailableToolsAsync();
        }

        private void RefreshHealthButton_Click(object sender, RoutedEventArgs e)
        {
            _ = CheckRuntimeHealthAsync();
        }

        private void ProcessVisualIntelligenceButton_Click(object sender, RoutedEventArgs e)
        {
            VisualIntelligenceButton_Click(sender, e);
        }

        private void StartMonitoringButton_Click(object sender, RoutedEventArgs e)
        {
            ContinuousMonitoringToggle_Click(sender, e);
        }

        private void ClearResultsButton_Click(object sender, RoutedEventArgs e)
        {
            ResultsTextBox.Clear();
            LastOperationText.Text = "Results cleared";
        }

        private void ExportResultsButton_Click(object sender, RoutedEventArgs e)
        {
            // Export functionality would be implemented here
            LastOperationText.Text = "Export functionality not yet implemented";
        }

        private async void ToolsListBox_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            if (ToolsListBox.SelectedItem != null)
            {
                LastOperationText.Text = $"Selected tool: {ToolsListBox.SelectedItem.ToString()}";
            }
        }

        #endregion

        /// <summary>
        /// Public dispose method
        /// </summary>
        public void Dispose()
        {
            Dispose(true);
            GC.SuppressFinalize(this);
        }

        /// <summary>
        /// Protected dispose method
        /// </summary>
        protected virtual void Dispose(bool disposing)
        {
            if (!_disposed && disposing)
            {
                _healthCheckTimer?.Stop();
                _continuousMonitoring = false;
                _disposed = true;
            }
        }
    }
}