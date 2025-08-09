using System;
using System.IO;
using System.Threading.Tasks;
using System.Windows;
using Microsoft.Web.WebView2.Wpf;
using Microsoft.Web.WebView2.Core;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;
using AIOS.Models;
using AIOS.Services;

namespace AIOS.UI
{
    /// <summary>
    /// Complete Hybrid UI Integration Example
    /// Demonstrates full HTML5 + C# integration with advanced features
    /// </summary>
    public partial class CompleteHybridWindow : Window
    {
        private WebView2 _webView;
        private WebInterfaceService _webInterface;
        private AdvancedAIServiceManager _aiService;
        private DatabaseService _dbService;
        private ILogger<CompleteHybridWindow> _logger;
        private bool _isWebViewInitialized = false;

        public CompleteHybridWindow()
        {
            InitializeComponent();
            InitializeServices();
            SetupHybridInterface();
        }

        private void InitializeServices()
        {
            // Set up dependency injection for services
            var services = new ServiceCollection();
            services.AddLogging(builder => builder.AddConsole());
            services.AddSingleton<AdvancedAIServiceManager>();
            services.AddSingleton<DatabaseService>();
            services.AddSingleton<WebInterfaceService>();

            var serviceProvider = services.BuildServiceProvider();

            _logger = serviceProvider.GetRequiredService<ILogger<CompleteHybridWindow>>();
            _aiService = serviceProvider.GetRequiredService<AdvancedAIServiceManager>();
            _dbService = serviceProvider.GetRequiredService<DatabaseService>();
            _webInterface = serviceProvider.GetRequiredService<WebInterfaceService>();

            _logger.LogInformation("AIOS Hybrid UI services initialized");
        }

        private async void SetupHybridInterface()
        {
            try
            {
                // Create WebView2 control
                _webView = new WebView2
                {
                    Name = "AIOSWebInterface",
                    Margin = new Thickness(0)
                };

                // Add to main container
                MainContainer.Children.Add(_webView);

                // Initialize WebView2
                await InitializeWebView();

                // Set up event handlers
                SetupWebViewEventHandlers();

                // Load the HTML interface
                await LoadHtmlInterface();

                StatusText.Text = "✅ AIOS Hybrid Interface Ready";
                _logger.LogInformation("Hybrid interface setup complete");
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Failed to setup hybrid interface");
                StatusText.Text = $"❌ Setup failed: {ex.Message}";
                ShowFallbackInterface();
            }
        }

        private async Task InitializeWebView()
        {
            try
            {
                // Set up WebView2 environment
                var webView2Environment = await CoreWebView2Environment.CreateAsync(
                    userDataFolder: Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData), "AIOS", "WebView2"));

                await _webView.EnsureCoreWebView2Async(webView2Environment);

                // Configure WebView2 settings
                ConfigureWebViewSettings();

                // Initialize web interface service
                await _webInterface.InitializeAsync(_webView);

                _isWebViewInitialized = true;
                _logger.LogInformation("WebView2 initialized successfully");
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "WebView2 initialization failed");
                throw;
            }
        }

        private void ConfigureWebViewSettings()
        {
            var settings = _webView.CoreWebView2.Settings;

            // Enable/disable features based on requirements
            settings.IsWebMessageEnabled = true;
            settings.AreDevToolsEnabled = true; // Enable for development
            settings.IsGeneralAutofillEnabled = false;
            settings.IsScriptEnabled = true;
            settings.AreDefaultScriptDialogsEnabled = true;
            settings.IsPasswordAutosaveEnabled = false;

            // Security settings
            settings.AreHostObjectsAllowed = true; // Required for C# integration
            settings.IsWebMessageEnabled = true;   // Required for message passing

            _logger.LogInformation("WebView2 settings configured");
        }

        private void SetupWebViewEventHandlers()
        {
            // Navigation events
            _webView.CoreWebView2.NavigationStarting += OnNavigationStarting;
            _webView.CoreWebView2.NavigationCompleted += OnNavigationCompleted;
            _webView.CoreWebView2.DOMContentLoaded += OnDOMContentLoaded;

            // Communication events
            _webView.CoreWebView2.WebMessageReceived += OnWebMessageReceived;

            // Permission events
            _webView.CoreWebView2.PermissionRequested += OnPermissionRequested;

            // Error handling
            _webView.CoreWebView2.ProcessFailed += OnProcessFailed;

            _logger.LogInformation("WebView2 event handlers registered");
        }

        private async Task LoadHtmlInterface()
        {
            try
            {
                // Load the advanced demo HTML file
                var htmlPath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "web", "advanced-demo.html");

                if (File.Exists(htmlPath))
                {
                    var uri = new Uri(htmlPath);
                    _webView.Source = uri;
                    _logger.LogInformation($"Loading HTML interface from: {htmlPath}");
                }
                else
                {
                    // Load from embedded resources or create minimal interface
                    await LoadFallbackHtml();
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Failed to load HTML interface");
                throw;
            }
        }

        private async Task LoadFallbackHtml()
        {
            var fallbackHtml = @"
<!DOCTYPE html>
<html>
<head>
    <title>AIOS Hybrid Interface</title>
    <style>
        body { font-family: Arial, sans-serif; background: #1e1e1e; color: #fff; padding: 20px; }
        .container { max-width: 800px; margin: 0 auto; }
        .header { text-align: center; margin-bottom: 30px; }
        .demo-button { background: #007acc; color: white; padding: 10px 20px; border: none; border-radius: 4px; margin: 5px; cursor: pointer; }
        .result { background: #2d2d30; padding: 15px; border-radius: 4px; margin: 10px 0; }
    </style>
</head>
<body>
    <div class='container'>
        <div class='header'>
            <h1>AIOS Hybrid Interface</h1>
            <p>HTML5 + C# Integration Demo</p>
        </div>
        <div>
            <button class='demo-button' onclick='testAI()'>Test AI Service</button>
            <button class='demo-button' onclick='testDB()'>Test Database</button>
            <button class='demo-button' onclick='getHealth()'>System Health</button>
        </div>
        <div id='results' class='result'>
            Ready for testing...
        </div>
    </div>
    <script>
    async function testAI() {
            try {
        const result = await window.chrome.webview.hostObjects.aiService.ProcessNLP('Hello AIOS');
                document.getElementById('results').innerHTML = '<h3>AI Response:</h3><pre>' + JSON.stringify(result, null, 2) + '</pre>';
            } catch (error) {
                document.getElementById('results').innerHTML = '<h3>Error:</h3><pre>' + error.message + '</pre>';
            }
        }

        async function testDB() {
            try {
                const result = await window.chrome.webview.hostObjects.dbService.ExecuteQuery('SELECT * FROM users LIMIT 5');
                document.getElementById('results').innerHTML = '<h3>Database Result:</h3><pre>' + JSON.stringify(result, null, 2) + '</pre>';
            } catch (error) {
                document.getElementById('results').innerHTML = '<h3>Error:</h3><pre>' + error.message + '</pre>';
            }
        }

    async function getHealth() {
            try {
        const result = await window.chrome.webview.hostObjects.aiService.GetSystemHealth();
                document.getElementById('results').innerHTML = '<h3>System Health:</h3><pre>' + JSON.stringify(result, null, 2) + '</pre>';
            } catch (error) {
                document.getElementById('results').innerHTML = '<h3>Error:</h3><pre>' + error.message + '</pre>';
            }
        }

        window.addEventListener('load', function() {
            console.log('AIOS Hybrid Interface loaded successfully');
        });
    </script>
</body>
</html>";

            _webView.NavigateToString(fallbackHtml);
            _logger.LogInformation("Loaded fallback HTML interface");
        }

        // Event Handlers
        private void OnNavigationStarting(object sender, CoreWebView2NavigationStartingEventArgs e)
        {
            _logger.LogInformation($"Navigation starting: {e.Uri}");
            StatusText.Text = "🔄 Loading interface...";
        }

        private async void OnNavigationCompleted(object sender, CoreWebView2NavigationCompletedEventArgs e)
        {
            _logger.LogInformation($"Navigation completed: Success={e.IsSuccess}");

            if (e.IsSuccess)
            {
                StatusText.Text = "✅ Interface loaded successfully";

                // Send initialization data to web interface
                await SendInitializationData();
            }
            else
            {
                StatusText.Text = "❌ Failed to load interface";
                _logger.LogError($"Navigation failed: {e.WebErrorStatus}");
            }
        }

        private async void OnDOMContentLoaded(object sender, CoreWebView2DOMContentLoadedEventArgs e)
        {
            _logger.LogInformation("DOM content loaded");

            try
            {
                // Execute initialization scripts
                await ExecuteInitializationScripts();

                // Start real-time updates
                await StartRealTimeUpdates();

                StatusText.Text = "✅ AIOS Hybrid Interface Ready";
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error during DOM content loaded");
                StatusText.Text = $"⚠️ Initialization error: {ex.Message}";
            }
        }

        private async void OnWebMessageReceived(object sender, CoreWebView2WebMessageReceivedEventArgs e)
        {
            try
            {
                var message = e.TryGetWebMessageAsString();
                _logger.LogInformation($"Web message received: {message}");

                // Handle different message types
                await HandleWebMessage(message);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error handling web message");
            }
        }

    // Note: CoreWebView2.ScriptDialogOpening can be used to monitor dialogs; no ScriptException or IsPrivateBrowsingEnabled in stable API

        private void OnPermissionRequested(object sender, CoreWebView2PermissionRequestedEventArgs e)
        {
            _logger.LogInformation($"Permission requested: {e.PermissionKind}");

            // Grant necessary permissions
            if (e.PermissionKind == CoreWebView2PermissionKind.Notifications ||
                e.PermissionKind == CoreWebView2PermissionKind.Geolocation)
            {
                e.State = CoreWebView2PermissionState.Allow;
            }
        }

        // XAML button handlers declared in CompleteHybridWindow.xaml
        private async void RetryButton_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                ErrorFallback.Visibility = Visibility.Collapsed;
                LoadingOverlay.Visibility = Visibility.Visible;
                await InitializeWebView();
                await LoadHtmlInterface();
                LoadingOverlay.Visibility = Visibility.Collapsed;
                StatusText.Text = "✅ AIOS Hybrid Interface Ready";
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Retry failed");
                ErrorFallback.Visibility = Visibility.Visible;
                StatusText.Text = $"❌ Retry failed: {ex.Message}";
            }
        }

        private void FallbackButton_Click(object sender, RoutedEventArgs e)
        {
            ShowFallbackInterface();
        }

        private void CloseCommand_Executed(object sender, System.Windows.Input.ExecutedRoutedEventArgs e)
        {
            this.Close();
        }

        private void OnProcessFailed(object sender, CoreWebView2ProcessFailedEventArgs e)
        {
            _logger.LogError($"WebView2 process failed: {e.Reason}");
            StatusText.Text = $"❌ WebView2 process failed: {e.Reason}";

            // Attempt to recover
            Task.Run(async () =>
            {
                await Task.Delay(2000);
                await Dispatcher.InvokeAsync(() => AttemptRecovery());
            });
        }

        // Helper Methods
        private async Task SendInitializationData()
        {
            try
            {
                var healthData = await _aiService.GetSystemHealth();
                var modules = _aiService.GetAvailableModules();

                var initData = new
                {
                    timestamp = DateTime.UtcNow.ToString("O"),
                    systemHealth = healthData,
                    aiModules = modules,
                    version = "2.0.0"
                };

                await _webInterface.SendEventToWeb("SystemInitialized", initData);
                _logger.LogInformation("Initialization data sent to web interface");
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Failed to send initialization data");
            }
        }

        private async Task ExecuteInitializationScripts()
        {
            try
            {
                // Inject additional JavaScript functionality
                await _webView.CoreWebView2.AddScriptToExecuteOnDocumentCreatedAsync(@"
                    console.log('AIOS Hybrid Interface - JavaScript bridge initialized');

                    // Enhanced error handling
                    window.addEventListener('error', function(e) {
                        console.error('JavaScript error:', e.error);
                        window.chrome.webview.postMessage(JSON.stringify({
                            type: 'javascript_error',
                            message: e.error.message,
                            stack: e.error.stack
                        }));
                    });

                    // Performance monitoring
                    window.addEventListener('load', function() {
                        const perfData = {
                            type: 'performance_data',
                            loadTime: performance.timing.loadEventEnd - performance.timing.navigationStart,
                            domReady: performance.timing.domContentLoadedEventEnd - performance.timing.navigationStart
                        };
                        window.chrome.webview.postMessage(JSON.stringify(perfData));
                    });
                ");

                _logger.LogInformation("Initialization scripts executed");
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Failed to execute initialization scripts");
            }
        }

        private async Task StartRealTimeUpdates()
        {
            try
            {
                // Start periodic health updates
                var timer = new System.Timers.Timer(5000); // 5 seconds
                timer.Elapsed += async (sender, e) =>
                {
                    try
                    {
                        var health = await _aiService.GetSystemHealth();
                        await _webInterface.SendEventToWeb("HealthUpdate", health);
                    }
                    catch (Exception ex)
                    {
                        _logger.LogError(ex, "Error sending health update");
                    }
                };
                timer.Start();

                _logger.LogInformation("Real-time updates started");
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Failed to start real-time updates");
            }
        }

        private async Task HandleWebMessage(string message)
        {
            try
            {
                var messageData = System.Text.Json.JsonSerializer.Deserialize<dynamic>(message);

                // Handle different message types
                // Implementation would depend on your specific needs

                _logger.LogInformation($"Handled web message: {message}");
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error handling web message");
            }
        }

        private void ShowFallbackInterface()
        {
            // Show traditional WPF interface as fallback
            var fallbackWindow = new MainWindow();
            fallbackWindow.Show();
            this.Close();
        }

        private void AttemptRecovery()
        {
            try
            {
                _logger.LogInformation("Attempting WebView2 recovery");
                StatusText.Text = "🔄 Attempting recovery...";

                // Restart the hybrid interface
                Task.Run(async () =>
                {
                    await Task.Delay(1000);
                    await Dispatcher.InvokeAsync(() => SetupHybridInterface());
                });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Recovery attempt failed");
                StatusText.Text = "❌ Recovery failed";
            }
        }

        protected override void OnClosed(EventArgs e)
        {
            try
            {
                _webView?.Dispose();
                _logger.LogInformation("AIOS Hybrid Interface closed");
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error during window close");
            }

            base.OnClosed(e);
        }
    }
}
