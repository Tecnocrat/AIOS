using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Threading;
using AIOS.Services;

namespace AIOS.UI.Controls
{
    /// <summary>
    /// AI Intelligence Control for real-time interaction with the AI supercell
    /// Connects through the Cytoplasm UI Bridge
    /// </summary>
    public partial class AIIntelligenceControl : UserControl
    {
        private readonly AIIntelligenceService _aiService;
        private readonly DispatcherTimer _healthCheckTimer;
        private bool _realTimeMonitoring = false;

        public AIIntelligenceControl()
        {
            InitializeComponent();
            _aiService = new AIIntelligenceService();
            
            // Setup health check timer
            _healthCheckTimer = new DispatcherTimer
            {
                Interval = TimeSpan.FromMinutes(5)
            };
            _healthCheckTimer.Tick += HealthCheckTimer_Tick;
            
            Loaded += AIIntelligenceControl_Loaded;
        }

        private async void AIIntelligenceControl_Loaded(object sender, RoutedEventArgs e)
        {
            await InitializeAIControlAsync();
        }

        private async Task InitializeAIControlAsync()
        {
            try
            {
                LoadingPanel.Visibility = Visibility.Visible;
                MainContent.Visibility = Visibility.Collapsed;

                // Load available AI functions
                var functions = await _aiService.GetAvailableFunctionsAsync();
                FunctionsListBox.ItemsSource = functions;

                // Initial health check
                await PerformHealthCheckAsync();

                // Start health monitoring
                _healthCheckTimer.Start();

                LoadingPanel.Visibility = Visibility.Collapsed;
                MainContent.Visibility = Visibility.Visible;
            }
            catch (Exception ex)
            {
                ShowError($"Failed to initialize AI control: {ex.Message}");
            }
        }

        private async void HealthCheckTimer_Tick(object sender, EventArgs e)
        {
            await PerformHealthCheckAsync();
        }

        private async Task PerformHealthCheckAsync()
        {
            try
            {
                var healthResult = await _aiService.SystemHealthCheckAsync();
                
                if (healthResult.IsSuccess && healthResult.Data is Dictionary<string, object> healthData)
                {
                    var overallHealth = healthData.GetValueOrDefault("overall_health", "unknown").ToString();
                    
                    Dispatcher.Invoke(() =>
                    {
                        HealthStatusText.Text = overallHealth;
                        HealthStatusText.Foreground = overallHealth == "healthy" 
                            ? System.Windows.Media.Brushes.Green 
                            : System.Windows.Media.Brushes.Orange;
                    });
                }
            }
            catch (Exception ex)
            {
                Dispatcher.Invoke(() =>
                {
                    HealthStatusText.Text = "Error";
                    HealthStatusText.Foreground = System.Windows.Media.Brushes.Red;
                });
            }
        }

        private async void ProcessVisualIntelligenceButton_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                ProcessVisualIntelligenceButton.IsEnabled = false;
                var analysisDepth = EnhancedAnalysisCheckBox.IsChecked == true ? "enhanced" : "standard";
                
                var result = await _aiService.ProcessVisualIntelligenceAsync(false, analysisDepth);
                
                if (result.IsSuccess)
                {
                    ShowResult("Visual Intelligence", result);
                }
                else
                {
                    ShowError($"Visual Intelligence processing failed: {result.Message}");
                }
            }
            catch (Exception ex)
            {
                ShowError($"Error processing visual intelligence: {ex.Message}");
            }
            finally
            {
                ProcessVisualIntelligenceButton.IsEnabled = true;
            }
        }

        private async void AnalyzeConsciousnessButton_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                AnalyzeConsciousnessButton.IsEnabled = false;
                
                var result = await _aiService.AnalyzeConsciousnessPatternsAsync();
                
                if (result.IsSuccess)
                {
                    ShowResult("Consciousness Analysis", result);
                }
                else
                {
                    ShowError($"Consciousness analysis failed: {result.Message}");
                }
            }
            catch (Exception ex)
            {
                ShowError($"Error analyzing consciousness: {ex.Message}");
            }
            finally
            {
                AnalyzeConsciousnessButton.IsEnabled = true;
            }
        }

        private async void EnhancedAnalysisButton_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                EnhancedAnalysisButton.IsEnabled = false;
                
                var result = await _aiService.EnhancedVisualAnalysisAsync(null, true);
                
                if (result.IsSuccess)
                {
                    ShowResult("Enhanced Visual Analysis", result);
                }
                else
                {
                    ShowError($"Enhanced analysis failed: {result.Message}");
                }
            }
            catch (Exception ex)
            {
                ShowError($"Error performing enhanced analysis: {ex.Message}");
            }
            finally
            {
                EnhancedAnalysisButton.IsEnabled = true;
            }
        }

        private async void RealTimeToggleButton_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                RealTimeToggleButton.IsEnabled = false;
                
                if (_realTimeMonitoring)
                {
                    var result = await _aiService.StopRealTimeMonitoringAsync();
                    if (result.IsSuccess)
                    {
                        _realTimeMonitoring = false;
                        RealTimeToggleButton.Content = "Start Real-time";
                        RealTimeStatusText.Text = "Stopped";
                        RealTimeStatusText.Foreground = System.Windows.Media.Brushes.Gray;
                    }
                }
                else
                {
                    var interval = int.TryParse(IntervalTextBox.Text, out var i) ? i : 30;
                    var result = await _aiService.StartRealTimeMonitoringAsync(interval);
                    if (result.IsSuccess)
                    {
                        _realTimeMonitoring = true;
                        RealTimeToggleButton.Content = "Stop Real-time";
                        RealTimeStatusText.Text = "Running";
                        RealTimeStatusText.Foreground = System.Windows.Media.Brushes.Green;
                    }
                }
            }
            catch (Exception ex)
            {
                ShowError($"Error toggling real-time monitoring: {ex.Message}");
            }
            finally
            {
                RealTimeToggleButton.IsEnabled = true;
            }
        }

        private async void CreateSessionButton_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                var result = await _aiService.CreateSessionAsync();
                
                if (result.IsSuccess)
                {
                    await RefreshSessionsAsync();
                    ShowInfo($"Session created successfully");
                }
                else
                {
                    ShowError($"Failed to create session: {result.Message}");
                }
            }
            catch (Exception ex)
            {
                ShowError($"Error creating session: {ex.Message}");
            }
        }

        private async void RefreshSessionsButton_Click(object sender, RoutedEventArgs e)
        {
            await RefreshSessionsAsync();
        }

        private async Task RefreshSessionsAsync()
        {
            try
            {
                var result = await _aiService.GetActiveSessionsAsync();
                
                if (result.IsSuccess && result.Data is Dictionary<string, object> sessionData)
                {
                    var sessions = sessionData.GetValueOrDefault("sessions") as List<object> ?? new List<object>();
                    SessionsListBox.ItemsSource = sessions;
                    SessionCountText.Text = sessions.Count.ToString();
                }
            }
            catch (Exception ex)
            {
                ShowError($"Error refreshing sessions: {ex.Message}");
            }
        }

        private async void ExportDataButton_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                var format = FormatComboBox.SelectedItem?.ToString()?.ToLower() ?? "json";
                var sessionId = SessionsListBox.SelectedItem?.ToString();
                
                var result = await _aiService.ExportAnalysisDataAsync(format, sessionId);
                
                if (result.IsSuccess)
                {
                    ShowInfo($"Data exported successfully: {result.Message}");
                }
                else
                {
                    ShowError($"Export failed: {result.Message}");
                }
            }
            catch (Exception ex)
            {
                ShowError($"Error exporting data: {ex.Message}");
            }
        }

        private async void GetDebugInfoButton_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                var result = await _aiService.GetDebugInfoAsync();
                
                if (result.IsSuccess)
                {
                    ShowResult("Debug Information", result);
                }
                else
                {
                    ShowError($"Failed to get debug info: {result.Message}");
                }
            }
            catch (Exception ex)
            {
                ShowError($"Error getting debug info: {ex.Message}");
            }
        }

        private void ShowResult(string title, AIExecutionResult result)
        {
            var resultWindow = new AIResultWindow(title, result);
            resultWindow.Owner = Window.GetWindow(this);
            resultWindow.ShowDialog();
        }

        private void ShowError(string message)
        {
            MessageBox.Show(message, "AI Intelligence Error", MessageBoxButton.OK, MessageBoxImage.Error);
        }

        private void ShowInfo(string message)
        {
            MessageBox.Show(message, "AI Intelligence", MessageBoxButton.OK, MessageBoxImage.Information);
        }

        private void OnUnloaded(object sender, RoutedEventArgs e)
        {
            _healthCheckTimer?.Stop();
        }
    }

    /// <summary>
    /// Window to display AI execution results
    /// </summary>
    public partial class AIResultWindow : Window
    {
        public AIResultWindow(string title, AIExecutionResult result)
        {
            InitializeComponent();
            Title = $"AI Intelligence - {title}";
            
            TitleText.Text = title;
            StatusText.Text = result.Status;
            StatusText.Foreground = result.IsSuccess 
                ? System.Windows.Media.Brushes.Green 
                : System.Windows.Media.Brushes.Red;
            
            MessageText.Text = result.Message;
            TimestampText.Text = result.Timestamp;
            
            if (result.Data != null)
            {
                DataTextBox.Text = System.Text.Json.JsonSerializer.Serialize(result.Data, new System.Text.Json.JsonSerializerOptions 
                { 
                    WriteIndented = true 
                });
            }
            else
            {
                DataTextBox.Text = "No data available";
            }
        }

        private void CloseButton_Click(object sender, RoutedEventArgs e)
        {
            Close();
        }
    }
}