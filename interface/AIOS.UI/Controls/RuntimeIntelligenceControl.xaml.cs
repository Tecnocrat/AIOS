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
                var tools = await _runtimeService.GetAvailableToolsAsync();
                
                // Clear existing items
                ToolsList.Items.Clear();
                
                // Add tool items
                foreach (var tool in tools)
                {
                    var item = new System.Windows.Controls.ListViewItem
                    {
                        Content = tool.Name,
                        Tag = tool
                    };
                    ToolsList.Items.Add(item);
                }
                
                StatusTextBlock.Text = $"Loaded {tools.Count} Runtime Intelligence tools";
            }
            catch (Exception ex)
            {
                StatusTextBlock.Text = $"Error loading tools: {ex.Message}";
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
                HealthStatusTextBlock.Text = health.Status;
                HealthProgressBar.Value = health.HealthScore * 100;
                
                // Update last check time
                LastCheckTextBlock.Text = $"Last checked: {DateTime.Now:HH:mm:ss}";
            }
            catch (Exception ex)
            {
                HealthStatusTextBlock.Text = "Health check failed";
                HealthProgressBar.Value = 0;
            }
        }

        #region Event Handlers

        private async void VisualIntelligenceButton_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                StatusTextBlock.Text = "Processing visual intelligence...";
                
                var result = await _runtimeService.GetVisualIntelligenceAsync();
                
                if (result.Success)
                {
                    // Show results in a new window
                    var resultWindow = new RuntimeIntelligenceResultWindow();
                    resultWindow.DisplayResult(result);
                    resultWindow.Show();
                    
                    StatusTextBlock.Text = "Visual intelligence processing completed";
                }
                else
                {
                    StatusTextBlock.Text = $"Error: {result.Error}";
                }
            }
            catch (Exception ex)
            {
                StatusTextBlock.Text = $"Error processing visual intelligence: {ex.Message}";
            }
        }

        private async void SystemHealthButton_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                StatusTextBlock.Text = "Checking system health...";
                
                var health = await _runtimeService.CheckSystemHealthAsync();
                
                StatusTextBlock.Text = $"System Health: {health.Status} ({health.HealthScore:P0})";
                HealthStatusTextBlock.Text = health.Status;
                HealthProgressBar.Value = health.HealthScore * 100;
            }
            catch (Exception ex)
            {
                StatusTextBlock.Text = $"Error checking system health: {ex.Message}";
            }
        }

        private async void ContinuousMonitoringToggle_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                if (_continuousMonitoring)
                {
                    // Stop monitoring
                    await _runtimeService.StopContinuousMonitoringAsync();
                    _continuousMonitoring = false;
                    ContinuousMonitoringToggle.Content = "Start Continuous Monitoring";
                    StatusTextBlock.Text = "Continuous monitoring stopped";
                }
                else
                {
                    // Start monitoring
                    await _runtimeService.StartContinuousMonitoringAsync();
                    _continuousMonitoring = true;
                    ContinuousMonitoringToggle.Content = "Stop Continuous Monitoring";
                    StatusTextBlock.Text = "Continuous monitoring started";
                }
            }
            catch (Exception ex)
            {
                StatusTextBlock.Text = $"Error toggling monitoring: {ex.Message}";
            }
        }

        private void RefreshToolsButton_Click(object sender, RoutedEventArgs e)
        {
            _ = LoadAvailableToolsAsync();
        }

        private async void ToolsList_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            if (ToolsList.SelectedItem is System.Windows.Controls.ListViewItem item && 
                item.Tag is RuntimeIntelligenceService.ToolInfo tool)
            {
                ToolDescriptionTextBlock.Text = tool.Description;
                ToolStatusTextBlock.Text = $"Status: {tool.Status}";
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