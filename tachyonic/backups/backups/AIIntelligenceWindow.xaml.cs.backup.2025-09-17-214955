using System;
using System.Threading.Tasks;
using System.Windows;
using AIOS.Services;

namespace AIOS.UI
{
    /// <summary>
    /// AI Intelligence Window - Dedicated interface for AI Intelligence control
    /// </summary>
    public partial class AIIntelligenceWindow : Window
    {
        private readonly AIIntelligenceService _aiService;

        public AIIntelligenceWindow()
        {
            InitializeComponent();
            _aiService = new AIIntelligenceService();
            
            Loaded += AIIntelligenceWindow_Loaded;
        }

        private async void AIIntelligenceWindow_Loaded(object sender, RoutedEventArgs e)
        {
            await InitializeWindowAsync();
        }

        private async Task InitializeWindowAsync()
        {
            try
            {
                // Check system status
                var healthResult = await _aiService.SystemHealthCheckAsync();
                
                if (healthResult.IsSuccess)
                {
                    var healthData = healthResult.Data as System.Collections.Generic.Dictionary<string, object>;
                    var overallHealth = healthData?.GetValueOrDefault("overall_health", "unknown").ToString();
                    
                    if (overallHealth == "healthy")
                    {
                        StatusIndicator.Fill = System.Windows.Media.Brushes.LimeGreen;
                        StatusText.Text = "All Systems Operational";
                    }
                    else if (overallHealth == "degraded")
                    {
                        StatusIndicator.Fill = System.Windows.Media.Brushes.Orange;
                        StatusText.Text = "Some Components Degraded";
                    }
                    else
                    {
                        StatusIndicator.Fill = System.Windows.Media.Brushes.Red;
                        StatusText.Text = "System Issues Detected";
                    }
                }
                else
                {
                    StatusIndicator.Fill = System.Windows.Media.Brushes.Red;
                    StatusText.Text = "Connection Failed";
                }
            }
            catch (Exception ex)
            {
                StatusIndicator.Fill = System.Windows.Media.Brushes.Red;
                StatusText.Text = "Error: " + ex.Message;
            }
        }

        private void CloseButton_Click(object sender, RoutedEventArgs e)
        {
            Close();
        }

        protected override void OnClosed(EventArgs e)
        {
            // Ensure any real-time monitoring is stopped when window closes
            try
            {
                _ = Task.Run(async () => await _aiService.StopRealTimeMonitoringAsync());
            }
            catch
            {
                // Ignore errors on shutdown
            }
            
            base.OnClosed(e);
        }
    }
}