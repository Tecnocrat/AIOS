using System;
using System.IO;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Media;
using Microsoft.Web.WebView2.Core;
using AIOS.Services;

namespace AIOS.UI
{
    /// <summary>
    /// AIOS Maintenance Center Window
    /// Provides unified access to tachyonic documentation optimization and system maintenance
    /// Integrates Python maintenance modules through C# service layer
    /// </summary>
    public partial class MaintenanceWindow : Window
    {
        private readonly MaintenanceService _maintenanceService;
        private bool _isWebViewInitialized = false;
        private string _maintenanceHtmlPath;

        public MaintenanceWindow(MaintenanceService maintenanceService)
        {
            InitializeComponent();
            _maintenanceService = maintenanceService ?? throw new ArgumentNullException(nameof(maintenanceService));

            // Set up paths
            var workspaceRoot = Path.GetFullPath(Path.Combine(AppDomain.CurrentDomain.BaseDirectory, @"..\..\..\..\"));
            _maintenanceHtmlPath = Path.Combine(workspaceRoot, @"interface\AIOS.UI\web\maintenance-center.html");

            InitializeMaintenanceCenter();
        }

        private async void InitializeMaintenanceCenter()
        {
            try
            {
                // Update status
                UpdateMaintenanceStatus("INITIALIZING", "#FF007ACC");

                // Initialize WebView2
                await InitializeWebView();

                // Load maintenance status
                await RefreshMaintenanceStatus();

                UpdateMaintenanceStatus("READY", "#FF28A745");
                MaintenanceInfoText.Text = "Maintenance Center ready - All systems operational";
            }
            catch (Exception ex)
            {
                UpdateMaintenanceStatus("ERROR", "#FFDC3545");
                MaintenanceInfoText.Text = $"Initialization error: {ex.Message}";
            }
        }

        private async Task InitializeWebView()
        {
            try
            {
                // Ensure WebView2 runtime is available
                await MaintenanceWebView.EnsureCoreWebView2Async();

                // Configure WebView2 settings
                MaintenanceWebView.CoreWebView2.Settings.IsWebMessageEnabled = true;
                MaintenanceWebView.CoreWebView2.Settings.AreDevToolsEnabled = true;
                MaintenanceWebView.CoreWebView2.Settings.IsGeneralAutofillEnabled = false;
                MaintenanceWebView.CoreWebView2.Settings.IsScriptEnabled = true;

                // Add JavaScript interface for C# communication
                MaintenanceWebView.CoreWebView2.AddWebResourceRequestedFilter("*", CoreWebView2WebResourceContext.All);
                MaintenanceWebView.CoreWebView2.WebMessageReceived += OnWebMessageReceived;

                // Navigate to maintenance center HTML
                if (File.Exists(_maintenanceHtmlPath))
                {
                    var uri = new Uri(_maintenanceHtmlPath).AbsoluteUri;
                    MaintenanceWebView.CoreWebView2.Navigate(uri);
                }
                else
                {
                    // Fallback: create a simple HTML interface
                    await CreateFallbackInterface();
                }

                _isWebViewInitialized = true;
            }
            catch (Exception ex)
            {
                throw new InvalidOperationException($"Failed to initialize WebView2: {ex.Message}", ex);
            }
        }

        private async Task CreateFallbackInterface()
        {
            var fallbackHtml = @"
<!DOCTYPE html>
<html>
<head>
    <title>AIOS Maintenance Center</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #1e1e1e; color: #cccccc; margin: 0; padding: 20px; }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { text-align: center; margin-bottom: 30px; }
        .status-card { background: #2d2d30; border-radius: 8px; padding: 20px; margin: 15px 0; border-left: 4px solid #007acc; }
        .action-button { background: #007acc; color: white; border: none; padding: 12px 24px; border-radius: 6px; cursor: pointer; margin: 5px; }
        .action-button:hover { background: #005a9e; }
        .error { border-left-color: #dc3545; }
        .success { border-left-color: #28a745; }
        .warning { border-left-color: #ffc107; }
        #output { background: #000; color: #00ff00; padding: 15px; border-radius: 6px; font-family: 'Courier New', monospace; min-height: 200px; margin-top: 20px; }
    </style>
</head>
<body>
    <div class='container'>
        <div class='header'>
            <h1>🔧 AIOS Maintenance Center</h1>
            <p>Tachyonic Documentation & System Optimization</p>
        </div>

        <div class='status-card'>
            <h3>System Status</h3>
            <p id='system-status'>Checking system status...</p>
        </div>

        <div class='status-card'>
            <h3>Quick Actions</h3>
            <button class='action-button' onclick='runQuickOptimize()'>⚡ Quick Optimize</button>
            <button class='action-button' onclick='runFullMaintenance()'>🔧 Full Maintenance</button>
            <button class='action-button' onclick='checkSystemHealth()'>🏥 System Health Check</button>
            <button class='action-button' onclick='openTachyonicArchive()'>📦 Tachyonic Archive</button>
        </div>

        <div id='output'></div>
    </div>

    <script>
        function log(message) {
            const output = document.getElementById('output');
            const timestamp = new Date().toLocaleTimeString();
            output.innerHTML += `[${timestamp}] ${message}\n`;
            output.scrollTop = output.scrollHeight;
        }

        function runQuickOptimize() {
            log('Running quick documentation optimization...');
            window.chrome.webview.postMessage({action: 'quick-optimize'});
        }

        function runFullMaintenance() {
            log('Running full maintenance cycle...');
            window.chrome.webview.postMessage({action: 'full-maintenance'});
        }

        function checkSystemHealth() {
            log('Checking system health...');
            window.chrome.webview.postMessage({action: 'health-check'});
        }

        function openTachyonicArchive() {
            log('Opening tachyonic archive explorer...');
            window.chrome.webview.postMessage({action: 'tachyonic-archive'});
        }

        // Initialize
        log('AIOS Maintenance Center initialized');
        window.chrome.webview.postMessage({action: 'ready'});
    </script>
</body>
</html>";

            MaintenanceWebView.NavigateToString(fallbackHtml);
        }

    private async void OnWebMessageReceived(object? sender, CoreWebView2WebMessageReceivedEventArgs e)
        {
            try
            {
                var message = e.TryGetWebMessageAsString();
                var data = System.Text.Json.JsonSerializer.Deserialize<dynamic>(message);
                var action = data.GetProperty("action").GetString();

                switch (action)
                {
                    case "ready":
                        await RefreshMaintenanceStatus();
                        break;
                    case "quick-optimize":
                        await RunQuickOptimize();
                        break;
                    case "full-maintenance":
                        await RunFullMaintenance();
                        break;
                    case "health-check":
                        await RunHealthCheck();
                        break;
                    case "tachyonic-archive":
                        await OpenTachyonicArchive();
                        break;
                }
            }
            catch (Exception ex)
            {
                await SendMessageToWebView($"Error processing command: {ex.Message}");
            }
        }

        private async Task SendMessageToWebView(string message)
        {
            if (_isWebViewInitialized)
            {
                var script = $"log('{message.Replace("'", "\\'")}');";
                await MaintenanceWebView.CoreWebView2.ExecuteScriptAsync(script);
            }
        }

        private async Task RefreshMaintenanceStatus()
        {
            try
            {
                var status = await _maintenanceService.GetMaintenanceStatusAsync();
                var statusMessage = $"System Health: {status.SystemHealth} | Docs: {status.DocumentationFragmentation} fragments | Archive: {status.TachyonicArchiveStatus}";

                await SendMessageToWebView($"Status: {statusMessage}");
                LastUpdateText.Text = $"Last Update: {DateTime.Now:HH:mm:ss}";
            }
            catch (Exception ex)
            {
                await SendMessageToWebView($"Error getting status: {ex.Message}");
            }
        }

        private async Task RunQuickOptimize()
        {
            try
            {
                UpdateMaintenanceStatus("OPTIMIZING", "#FFFFC107");
                await SendMessageToWebView("Starting quick optimization...");

                var result = await _maintenanceService.RunQuickOptimizationAsync();

                if (result.Success)
                {
                    UpdateMaintenanceStatus("READY", "#FF28A745");
                    await SendMessageToWebView($"✅ Quick optimization completed: {result.Message}");
                }
                else
                {
                    UpdateMaintenanceStatus("ERROR", "#FFDC3545");
                    await SendMessageToWebView($"❌ Optimization failed: {result.Message}");
                }
            }
            catch (Exception ex)
            {
                UpdateMaintenanceStatus("ERROR", "#FFDC3545");
                await SendMessageToWebView($"❌ Error during optimization: {ex.Message}");
            }
        }

        private async Task RunFullMaintenance()
        {
            try
            {
                UpdateMaintenanceStatus("MAINTENANCE", "#FFFFC107");
                await SendMessageToWebView("Starting full maintenance cycle...");

                var result = await _maintenanceService.RunFullMaintenanceAsync();

                if (result.Success)
                {
                    UpdateMaintenanceStatus("READY", "#FF28A745");
                    await SendMessageToWebView($"✅ Full maintenance completed: {result.Message}");
                }
                else
                {
                    UpdateMaintenanceStatus("ERROR", "#FFDC3545");
                    await SendMessageToWebView($"❌ Maintenance failed: {result.Message}");
                }
            }
            catch (Exception ex)
            {
                UpdateMaintenanceStatus("ERROR", "#FFDC3545");
                await SendMessageToWebView($"❌ Error during maintenance: {ex.Message}");
            }
        }

        private async Task RunHealthCheck()
        {
            try
            {
                await SendMessageToWebView("Running comprehensive health check...");

                var status = await _maintenanceService.GetMaintenanceStatusAsync();

                await SendMessageToWebView($"🏥 Health Check Results:");
                await SendMessageToWebView($"  - System Health: {status.SystemHealth}");
                await SendMessageToWebView($"  - Documentation Fragments: {status.DocumentationFragmentation}");
                await SendMessageToWebView($"  - Backup System: {status.BackupSystemStatus}");
                await SendMessageToWebView($"  - Tachyonic Archive: {status.TachyonicArchiveStatus}");
                await SendMessageToWebView($"  - Last Maintenance: {status.LastMaintenanceRun}");
            }
            catch (Exception ex)
            {
                await SendMessageToWebView($"❌ Health check error: {ex.Message}");
            }
        }

        private async Task OpenTachyonicArchive()
        {
            try
            {
                await SendMessageToWebView("Opening tachyonic archive explorer...");

                var archiveInfo = await _maintenanceService.GetTachyonicArchiveInfoAsync();

                await SendMessageToWebView($"📦 Tachyonic Archive Information:");
                await SendMessageToWebView($"  - Total archived files: {archiveInfo.TotalFiles}");
                await SendMessageToWebView($"  - Archive size: {archiveInfo.TotalSize}");
                await SendMessageToWebView($"  - Last archive operation: {archiveInfo.LastArchiveTime}");
                await SendMessageToWebView($"  - Archive location: {archiveInfo.ArchivePath}");
            }
            catch (Exception ex)
            {
                await SendMessageToWebView($"❌ Archive access error: {ex.Message}");
            }
        }

        private void UpdateMaintenanceStatus(string status, string colorHex)
        {
            MaintenanceStatusText.Text = status;
            MaintenanceStatusBorder.Background = new SolidColorBrush((Color)ColorConverter.ConvertFromString(colorHex));
        }

        // Event Handlers
        private async void RefreshButton_Click(object sender, RoutedEventArgs e)
        {
            await RefreshMaintenanceStatus();
        }

        private void CloseButton_Click(object sender, RoutedEventArgs e)
        {
            this.Close();
        }

        private async void QuickOptimizeButton_Click(object sender, RoutedEventArgs e)
        {
            await RunQuickOptimize();
        }

    private void MaintenanceWebView_NavigationCompleted(object? sender, CoreWebView2NavigationCompletedEventArgs e)
        {
            if (e.IsSuccess)
            {
                LoadingPanel.Visibility = Visibility.Collapsed;
                MaintenanceWebView.Visibility = Visibility.Visible;
            }
        }

    private void MaintenanceWebView_DOMContentLoaded(object? sender, CoreWebView2DOMContentLoadedEventArgs e)
        {
            LoadingPanel.Visibility = Visibility.Collapsed;
            MaintenanceWebView.Visibility = Visibility.Visible;
        }
    }
}
