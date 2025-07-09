using System;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Input;
using AIOS.Models;
using AIOS.Services;
using Microsoft.Extensions.Logging;

namespace AIOS.UI
{
    public partial class SimpleMainWindow : Window
    {
        private readonly AIOS.Models.AdvancedAIServiceManager _aiService;
        private readonly AIOS.Services.MaintenanceService _maintenanceService;
        private readonly DatabaseService _databaseService;
        private readonly ILogger<SimpleMainWindow> _logger;

        public SimpleMainWindow()
        {
            InitializeComponent();

            // Initialize services
            _aiService = new AIOS.Models.AdvancedAIServiceManager();
            _maintenanceService = new AIOS.Services.MaintenanceService();
            _databaseService = new DatabaseService();
            _logger = Microsoft.Extensions.Logging.Abstractions.NullLogger<SimpleMainWindow>.Instance;

            // Load initial status
            LoadInitialStatus();
        }

        private async void LoadInitialStatus()
        {
            try
            {
                StatusText.Text = "Loading system status...";

                // Get system health
                var healthResponse = await _aiService.GetSystemHealthAsync();

                StatusText.Text = healthResponse.Success ? "System Ready" : "System Issues Detected";

                // Update system status tab
                SystemStatusOutput.Text = $"System Health: {healthResponse.HealthStatus}\n" +
                                        $"Health Score: {healthResponse.HealthScore:F2}\n" +
                                        $"Last Updated: {healthResponse.Timestamp}\n\n" +
                                        $"Issues: {string.Join(", ", healthResponse.Issues)}\n" +
                                        $"Recommendations: {string.Join(", ", healthResponse.Recommendations)}";
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error loading initial status");
                StatusText.Text = "Error loading status";
                SystemStatusOutput.Text = $"Error: {ex.Message}";
            }
        }

        private async void SendButton_Click(object sender, RoutedEventArgs e)
        {
            await ProcessChatInput();
        }

        private async void ChatInput_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.Key == Key.Enter)
            {
                await ProcessChatInput();
            }
        }

        private async Task ProcessChatInput()
        {
            var input = ChatInput.Text.Trim();
            if (string.IsNullOrEmpty(input))
                return;

            try
            {
                // Add user message to chat
                ChatOutput.Text += $"\n\nUser: {input}";
                ChatInput.Text = "";
                StatusText.Text = "Processing...";

                // Process with AI service
                var response = await _aiService.ProcessAsync(input);

                // Add AI response to chat
                ChatOutput.Text += $"\n\nAI: {response.Response}";

                // Scroll to bottom
                ChatOutput.ScrollToEnd();

                StatusText.Text = response.Success ? "Ready" : "Error in processing";
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error processing chat input");
                ChatOutput.Text += $"\n\nError: {ex.Message}";
                StatusText.Text = "Error";
            }
        }

        private async void RefreshStatusButton_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                StatusText.Text = "Refreshing status...";

                var healthResponse = await _aiService.GetSystemHealthAsync();
                var maintenanceStatus = await _maintenanceService.GetMaintenanceStatusAsync();

                SystemStatusOutput.Text = $"=== SYSTEM HEALTH ===\n" +
                                        $"Health Status: {healthResponse.HealthStatus}\n" +
                                        $"Health Score: {healthResponse.HealthScore:F2}\n" +
                                        $"Last Updated: {healthResponse.Timestamp}\n\n" +
                                        $"Issues: {string.Join(", ", healthResponse.Issues)}\n" +
                                        $"Warnings: {string.Join(", ", healthResponse.Warnings)}\n" +
                                        $"Recommendations: {string.Join(", ", healthResponse.Recommendations)}\n\n" +
                                        $"=== MAINTENANCE STATUS ===\n" +
                                        $"Documentation Fragmentation: {maintenanceStatus.DocumentationFragmentation}\n" +
                                        $"Backup System: {maintenanceStatus.BackupSystemStatus.Status}\n" +
                                        $"Tachyonic Archive: {maintenanceStatus.TachyonicArchiveStatus.Status}\n" +
                                        $"Available Operations: {string.Join(", ", maintenanceStatus.AvailableOperations)}";

                StatusText.Text = "Status refreshed";
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error refreshing status");
                SystemStatusOutput.Text = $"Error refreshing status: {ex.Message}";
                StatusText.Text = "Error";
            }
        }

        private async void RunMaintenanceButton_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                StatusText.Text = "Running maintenance...";
                MaintenanceOutput.Text = "Starting maintenance operations...\n";

                var result = await _maintenanceService.RunMaintenanceAsync();

                MaintenanceOutput.Text += $"Maintenance completed!\n" +
                                        $"Success: {result.Success}\n" +
                                        $"Message: {result.Message}\n" +
                                        $"Actions: {string.Join(", ", result.Actions)}\n" +
                                        $"Timestamp: {DateTime.Now}\n";

                StatusText.Text = result.Success ? "Maintenance completed" : "Maintenance failed";
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error running maintenance");
                MaintenanceOutput.Text += $"Error: {ex.Message}\n";
                StatusText.Text = "Maintenance error";
            }
        }

        private async void CheckHealthButton_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                StatusText.Text = "Checking system health...";

                var healthResponse = await _aiService.GetSystemHealthAsync();

                MaintenanceOutput.Text = $"=== SYSTEM HEALTH CHECK ===\n" +
                                       $"Status: {healthResponse.HealthStatus}\n" +
                                       $"Score: {healthResponse.HealthScore:F2}\n" +
                                       $"Timestamp: {healthResponse.Timestamp}\n\n" +
                                       $"Issues Found:\n{string.Join("\n", healthResponse.Issues)}\n\n" +
                                       $"Warnings:\n{string.Join("\n", healthResponse.Warnings)}\n\n" +
                                       $"Recommendations:\n{string.Join("\n", healthResponse.Recommendations)}\n";

                StatusText.Text = "Health check completed";
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error checking health");
                MaintenanceOutput.Text = $"Error checking health: {ex.Message}";
                StatusText.Text = "Health check error";
            }
        }
    }
}
