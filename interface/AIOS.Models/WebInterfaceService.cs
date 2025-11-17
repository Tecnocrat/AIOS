using Microsoft.Web.WebView2.Core;
using Microsoft.Web.WebView2.Wpf;
using System;
using System.Threading.Tasks;
using System.Text.Json;

namespace AIOS.Models
{
    /// <summary>
    /// Service for managing HTML5/JavaScript integration with C# backend
    /// Enables bi-directional communication between web UI and AIOS core
    /// </summary>
    public class WebInterfaceService
    {
        private WebView2 _webView;
        // Accept either interfaces or concrete implementations
        private readonly object _aiService;
        private readonly object _dbService;

        // Default constructor for DI containers
        public WebInterfaceService(IAIService aiService, IDatabaseService dbService)
        {
            _aiService = aiService;
            _dbService = dbService;
        }

        // Overload accepting concrete service instances used by UI demos
        public WebInterfaceService(AIOS.Models.AIServiceManager aiService, AIOS.Models.DatabaseService dbService)
        {
            _aiService = aiService;
            _dbService = dbService;
        }

        public async Task InitializeAsync(WebView2 webView)
        {
            _webView = webView;

            // Enable developer tools in debug mode
#if DEBUG
            _webView.CoreWebView2.Settings.AreDevToolsEnabled = true;
#endif

            // Register C# methods that can be called from JavaScript
            await RegisterJavaScriptBindings();

            // Load the main HTML interface
            await LoadMainInterface();
        }

        private async Task RegisterJavaScriptBindings()
        {
            // AI Module Interactions
            _webView.CoreWebView2.AddWebResourceRequestedFilter("*", CoreWebView2WebResourceContext.All);

            // Register AIOS API endpoints
            await _webView.CoreWebView2.AddScriptToExecuteOnDocumentCreatedAsync(@"
                window.AIOS = {
                    // AI Module Communication
                    async processNLP(input) {
                        return await window.chrome.webview.hostObjects.aiService.ProcessNLP(input);
                    },

                    async makePrediction(data) {
                        return await window.chrome.webview.hostObjects.aiService.MakePrediction(data);
                    },

                    async runAutomation(task) {
                        return await window.chrome.webview.hostObjects.aiService.RunAutomation(task);
                    },

                    // Database Operations
                    async queryDatabase(query) {
                        return await window.chrome.webview.hostObjects.dbService.ExecuteQuery(query);
                    },

                    async saveData(collection, data) {
                        return await window.chrome.webview.hostObjects.dbService.SaveData(collection, data);
                    },

                    // System Health
                    async getSystemHealth() {
                        return await window.chrome.webview.hostObjects.aiService.GetSystemHealth();
                    },

                    // Real-time Events
                    onDataUpdate: null,
                    onSystemAlert: null,
                    onAIResponse: null
                };
            ");

            // Add host objects for direct C# method calls
            _webView.CoreWebView2.AddHostObjectToScript("aiService", _aiService);
            _webView.CoreWebView2.AddHostObjectToScript("dbService", _dbService);
        }

        private async Task LoadMainInterface()
        {
            // Load the HTML5 interface
            var htmlPath = System.IO.Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "web", "index.html");
            _webView.Source = new Uri($"file:///{htmlPath}");
        }

        // Send real-time updates to the web interface
        public async Task SendEventToWeb(string eventType, object data)
        {
            var json = JsonSerializer.Serialize(data);
            await _webView.CoreWebView2.ExecuteScriptAsync($@"
                if (window.AIOS && window.AIOS.on{eventType}) {{
                    window.AIOS.on{eventType}({json});
                }}
            ");
        }
    }
}
