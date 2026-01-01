using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using System.Text.Json;
using System.Net.Http;
using Microsoft.Extensions.Logging;

namespace AIOS.Models
{
    /// <summary>
    /// AIOS Python AI Tools Integration Service
    /// Provides seamless integration with Python AI tools via the Interface Bridge
    /// Enables rich metadata generation and dynamic tool discovery for the UI
    /// </summary>
    public class PythonAIToolsService
    {
        private readonly HttpClient _httpClient;
        private readonly ILogger<PythonAIToolsService> _logger;
        private readonly string _bridgeUrl;
        private List<AIToolMetadata> _availableTools;
        private DateTime _lastToolsRefresh;
        private readonly TimeSpan _refreshInterval = TimeSpan.FromMinutes(5);

        public PythonAIToolsService(ILogger<PythonAIToolsService> logger, HttpClient httpClient = null)
        {
            _logger = logger;
            _bridgeUrl = "http://localhost:8000"; // Default Interface Bridge URL
            _httpClient = httpClient ?? new HttpClient();
            _availableTools = new List<AIToolMetadata>();
            _lastToolsRefresh = DateTime.MinValue;
        }

        /// <summary>
        /// Check if the Python Interface Bridge is available
        /// </summary>
        public async Task<bool> IsInterfaceBridgeAvailable()
        {
            try
            {
                var response = await _httpClient.GetAsync($"{_bridgeUrl}/health");
                return response.IsSuccessStatusCode;
            }
            catch
            {
                return false;
            }
        }

        /// <summary>
        /// Get all available AI tools with their metadata
        /// </summary>
        public async Task<List<AIToolMetadata>> GetAvailableToolsAsync()
        {
            // Return cached tools if recent
            if (DateTime.Now - _lastToolsRefresh < _refreshInterval && _availableTools.Count > 0)
            {
                return _availableTools;
            }

            // Refresh from bridge
            await RefreshAvailableToolsAsync();
            return _availableTools;
        }

        /// <summary>
        /// Refresh tools from the Interface Bridge
        /// </summary>
        public async Task RefreshAvailableToolsAsync()
        {
            try
            {
                _logger.LogInformation("🔍 Refreshing AI tools from Interface Bridge...");

                var response = await _httpClient.GetStringAsync($"{_bridgeUrl}/tools");
                var toolsResponse = JsonSerializer.Deserialize<ToolsResponse>(response, new JsonSerializerOptions
                {
                    PropertyNameCaseInsensitive = true
                });

                _availableTools = toolsResponse.Tools ?? new List<AIToolMetadata>();
                _lastToolsRefresh = DateTime.Now;

                _logger.LogInformation("✅ Refreshed {Count} AI tools", _availableTools.Count);

                // Log discovered tools
                foreach (var tool in _availableTools)
                {
                    _logger.LogDebug("📋 Tool: {Name} ({Category}) - {Description}", 
                        tool.DisplayName, tool.Category, tool.Description);
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "❌ Failed to refresh AI tools");
                // Keep existing tools on error
            }
        }

        /// <summary>
        /// Get detailed information about a specific tool
        /// </summary>
        public async Task<AIToolMetadata> GetToolDetailsAsync(string toolName)
        {
            try
            {
                var response = await _httpClient.GetStringAsync($"{_bridgeUrl}/tools/{toolName}");
                return JsonSerializer.Deserialize<AIToolMetadata>(response, new JsonSerializerOptions
                {
                    PropertyNameCaseInsensitive = true
                });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "❌ Failed to get tool details for {ToolName}", toolName);
                throw;
            }
        }

        /// <summary>
        /// Execute a specific AI tool with parameters
        /// </summary>
        public async Task<ToolExecutionResult> ExecuteToolAsync(string toolName, Dictionary<string, object> parameters = null)
        {
            try
            {
                _logger.LogInformation("🚀 Executing AI tool: {ToolName}", toolName);

                var json = JsonSerializer.Serialize(parameters ?? new Dictionary<string, object>());
                var content = new StringContent(json, System.Text.Encoding.UTF8, "application/json");

                var response = await _httpClient.PostAsync($"{_bridgeUrl}/tools/{toolName}/execute", content);
                var resultJson = await response.Content.ReadAsStringAsync();

                var result = JsonSerializer.Deserialize<ToolExecutionResult>(resultJson, new JsonSerializerOptions
                {
                    PropertyNameCaseInsensitive = true
                });

                _logger.LogInformation("✅ Tool execution completed: {Status}", result.ExecutionStatus);
                return result;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "❌ Failed to execute tool {ToolName}", toolName);
                throw;
            }
        }

        /// <summary>
        /// Get tools organized by category
        /// </summary>
        public async Task<List<ToolCategory>> GetToolCategoriesAsync()
        {
            try
            {
                var response = await _httpClient.GetStringAsync($"{_bridgeUrl}/categories");
                var categoriesResponse = JsonSerializer.Deserialize<CategoriesResponse>(response, new JsonSerializerOptions
                {
                    PropertyNameCaseInsensitive = true
                });

                return categoriesResponse.Categories ?? new List<ToolCategory>();
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "❌ Failed to get tool categories");
                return new List<ToolCategory>();
            }
        }

        /// <summary>
        /// Generate rich metadata for interface consumption
        /// </summary>
        public async Task<AIOSMetadataSnapshot> GenerateMetadataSnapshotAsync()
        {
            try
            {
                var tools = await GetAvailableToolsAsync();
                var categories = await GetToolCategoriesAsync();

                return new AIOSMetadataSnapshot
                {
                    GeneratedAt = DateTime.UtcNow,
                    TotalTools = tools.Count,
                    TotalCategories = categories.Count,
                    Tools = tools,
                    Categories = categories,
                    CapabilitiesIndex = GenerateCapabilitiesIndex(tools),
                    InterfaceBridgeStatus = await IsInterfaceBridgeAvailable() ? "Connected" : "Disconnected",
                    MetadataVersion = "1.0.0"
                };
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "❌ Failed to generate metadata snapshot");
                throw;
            }
        }

        /// <summary>
        /// Generate capabilities index for UI
        /// </summary>
        private Dictionary<string, List<string>> GenerateCapabilitiesIndex(List<AIToolMetadata> tools)
        {
            var index = new Dictionary<string, List<string>>();

            foreach (var tool in tools)
            {
                foreach (var capability in tool.Capabilities ?? new List<string>())
                {
                    if (!index.ContainsKey(capability))
                    {
                        index[capability] = new List<string>();
                    }
                    index[capability].Add(tool.Name);
                }
            }

            return index;
        }

        /// <summary>
        /// Search tools by capability
        /// </summary>
        public async Task<List<AIToolMetadata>> SearchToolsByCapabilityAsync(string capability)
        {
            var tools = await GetAvailableToolsAsync();
            return tools.FindAll(t => t.Capabilities?.Contains(capability) == true);
        }

        /// <summary>
        /// Get recommended tools for a specific task
        /// </summary>
        public async Task<List<AIToolMetadata>> GetRecommendedToolsAsync(string taskDescription)
        {
            var tools = await GetAvailableToolsAsync();
            var recommended = new List<AIToolMetadata>();

            // Simple keyword-based recommendation
            var keywords = taskDescription.ToLower().Split(' ');

            foreach (var tool in tools)
            {
                var toolText = (tool.Description + " " + string.Join(" ", tool.Capabilities ?? new List<string>())).ToLower();
                
                foreach (var keyword in keywords)
                {
                    if (toolText.Contains(keyword))
                    {
                        recommended.Add(tool);
                        break;
                    }
                }
            }

            return recommended;
        }
    }

    /// <summary>
    /// Comprehensive metadata snapshot for AIOS interface
    /// </summary>
    public class AIOSMetadataSnapshot
    {
        public DateTime GeneratedAt { get; set; }
        public int TotalTools { get; set; }
        public int TotalCategories { get; set; }
        public List<AIToolMetadata> Tools { get; set; }
        public List<ToolCategory> Categories { get; set; }
        public Dictionary<string, List<string>> CapabilitiesIndex { get; set; }
        public string InterfaceBridgeStatus { get; set; }
        public string MetadataVersion { get; set; }
    }
}