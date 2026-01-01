
using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using System.Text.Json;
using System.Net.Http;

namespace AIOS.Models
{
    /// <summary>
    /// Generated interface for Python AI Tools Bridge
    /// Automatically generated from AIOS Interface Bridge discovery
    /// </summary>
    public class PythonAIToolsBridge
    {
        private readonly HttpClient _httpClient;
        private readonly string _bridgeUrl;
        
        public PythonAIToolsBridge(string bridgeUrl = "http://localhost:8000")
        {
            _bridgeUrl = bridgeUrl;
            _httpClient = new HttpClient();
        }
        
        public async Task<List<AIToolMetadata>> GetAvailableToolsAsync()
        {
            var response = await _httpClient.GetStringAsync($"{_bridgeUrl}/tools");
            var result = JsonSerializer.Deserialize<ToolsResponse>(response);
            return result.Tools;
        }
        
        public async Task<AIToolMetadata> GetToolDetailsAsync(string toolName)
        {
            var response = await _httpClient.GetStringAsync($"{_bridgeUrl}/tools/{toolName}");
            return JsonSerializer.Deserialize<AIToolMetadata>(response);
        }
        
        public async Task<ToolExecutionResult> ExecuteToolAsync(string toolName, Dictionary<string, object> parameters = null)
        {
            var json = JsonSerializer.Serialize(parameters ?? new Dictionary<string, object>());
            var content = new StringContent(json, System.Text.Encoding.UTF8, "application/json");
            
            var response = await _httpClient.PostAsync($"{_bridgeUrl}/tools/{toolName}/execute", content);
            var resultJson = await response.Content.ReadAsStringAsync();
            
            return JsonSerializer.Deserialize<ToolExecutionResult>(resultJson);
        }
        
        public async Task<List<ToolCategory>> GetToolCategoriesAsync()
        {
            var response = await _httpClient.GetStringAsync($"{_bridgeUrl}/categories");
            var result = JsonSerializer.Deserialize<CategoriesResponse>(response);
            return result.Categories;
        }
    }
    
    public class AIToolMetadata
    {
        public string Name { get; set; }
        public string DisplayName { get; set; }
        public string Description { get; set; }
        public string Category { get; set; }
        public string Version { get; set; }
        public string Status { get; set; }
        public List<string> Capabilities { get; set; }
        public List<ToolParameter> Parameters { get; set; }
        public List<string> OutputFormats { get; set; }
        public string ExecutionTimeEstimate { get; set; }
        public ResourceRequirements ResourceRequirements { get; set; }
        public DateTime MetadataGenerated { get; set; }
    }
    
    public class ToolParameter
    {
        public string Name { get; set; }
        public string Type { get; set; }
        public bool Required { get; set; }
        public string Description { get; set; }
        public object Example { get; set; }
    }
    
    public class ResourceRequirements
    {
        public string Memory { get; set; }
        public string Cpu { get; set; }
        public string Disk { get; set; }
        public string Network { get; set; }
    }
    
    public class ToolExecutionResult
    {
        public string ToolName { get; set; }
        public string ExecutionStatus { get; set; }
        public int? ReturnCode { get; set; }
        public string Stdout { get; set; }
        public string Stderr { get; set; }
        public double ExecutionTimeSeconds { get; set; }
        public Dictionary<string, object> ParametersUsed { get; set; }
        public DateTime Timestamp { get; set; }
    }
    
    public class ToolCategory
    {
        public string Name { get; set; }
        public string DisplayName { get; set; }
        public List<string> Tools { get; set; }
    }
    
    public class ToolsResponse
    {
        public List<AIToolMetadata> Tools { get; set; }
        public int TotalCount { get; set; }
        public DateTime? LastDiscovery { get; set; }
    }
    
    public class CategoriesResponse
    {
        public List<ToolCategory> Categories { get; set; }
        public int TotalCategories { get; set; }
    }
}
