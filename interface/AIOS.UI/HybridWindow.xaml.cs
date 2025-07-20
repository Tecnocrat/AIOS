using System;
using System.Threading.Tasks;
using System.Windows;
using Microsoft.Web.WebView2.Wpf;
using AIOS.Models;

namespace AIOS.UI
{
    /// <summary>
    /// Hybrid Window that integrates both WPF and HTML5 interfaces
    /// Demonstrates the future of AIOS UI development
    /// </summary>
    public partial class HybridWindow : Window
    {
        private WebView2 _webView;
        private WebInterfaceService _webInterface;
        private AIServiceManager _aiService;
        private DatabaseService _dbService;

        public HybridWindow()
        {
            InitializeComponent();
            InitializeServices();
            SetupHybridInterface();
        }

        private void InitializeServices()
        {
            _aiService = new AIServiceManager();
            _dbService = new DatabaseService(_aiService);
            _webInterface = new WebInterfaceService(_aiService, _dbService);
        }

        private async void SetupHybridInterface()
        {
            // Create WebView2 for HTML5 interface
            _webView = new WebView2
            {
                Name = "AIOSWebInterface",
                Margin = new Thickness(0)
            };

            // Add to main container
            MainContainer.Children.Add(_webView);

            try
            {
                // Initialize WebView2
                await _webView.EnsureCoreWebView2Async(null);
                await _webInterface.InitializeAsync(_webView);

                // Set up navigation event handlers
                _webView.CoreWebView2.DOMContentLoaded += OnWebContentLoaded;
                _webView.CoreWebView2.WebMessageReceived += OnWebMessageReceived;

                StatusText.Text = "Hybrid AIOS interface ready";
            }
            catch (Exception ex)
            {
                StatusText.Text = $"Web interface error: {ex.Message}";
                
                // Fallback to traditional interface
                ShowTraditionalInterface();
            }
        }

        private async void OnWebContentLoaded(object sender, Microsoft.Web.WebView2.Core.CoreWebView2DOMContentLoadedEventArgs e)
        {
            // Send initial system status to web interface
            var healthData = await _aiService.GetSystemHealth();
            await _webInterface.SendEventToWeb("SystemInitialized", healthData);
        }

        private async void OnWebMessageReceived(object sender, Microsoft.Web.WebView2.Core.CoreWebView2WebMessageReceivedEventArgs e)
        {
            try
            {
                var message = e.TryGetWebMessageAsString();
                // Handle messages from web interface
                // This enables bidirectional communication
                
                if (message.Contains("health_check"))
                {
                    var health = await _aiService.GetSystemHealth();
                    await _webInterface.SendEventToWeb("HealthUpdate", health);
                }
                else if (message.Contains("database_query"))
                {
                    // Handle database operations from web interface
                    var result = await _dbService.ExecuteQuery(message);
                    await _webInterface.SendEventToWeb("QueryResult", result);
                }
            }
            catch (Exception ex)
            {
                StatusText.Text = $"Message handling error: {ex.Message}";
            }
        }

        private void ShowTraditionalInterface()
        {
            // Create traditional WPF interface as fallback
            var traditionalInterface = new MainWindow();
            traditionalInterface.Show();
            this.Close();
        }

        // Demonstration of AINLP integration
        private async Task ProcessAINLPCommand(string naturalLanguageCommand)
        {
            try
            {
                // Example of how AINLP would work
                /*
                AINLP_INTENT: "Create a real-time dashboard showing system performance"
                AINLP_CONTEXT: "User wants to monitor AIOS health metrics"
                AINLP_REQUIREMENTS:
                  - Update every 5 seconds
                  - Show CPU, memory, and AI module status
                  - Alert on anomalies
                  - Mobile-responsive design
                */

                // This would be processed by the AINLP compiler
                var intent = await _aiService.ProcessNLP($"AINLP_COMPILE: {naturalLanguageCommand}");
                
                // The compiled result would be executable code
                // For now, we'll simulate the concept
                await _webInterface.SendEventToWeb("AINLPResult", new 
                { 
                    command = naturalLanguageCommand,
                    compiled = true,
                    execution = "success"
                });
            }
            catch (Exception ex)
            {
                StatusText.Text = $"AINLP processing error: {ex.Message}";
            }
        }

        protected override void OnClosed(EventArgs e)
        {
            _webView?.Dispose();
            base.OnClosed(e);
        }
    }
}
