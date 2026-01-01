using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Text;
using System.Text.Json;
using System.Text.Json.Serialization;
using System.Threading.Tasks;

namespace AIOS.Services
{
    /// <summary>
    /// Phase 11 Day 1: HTTP client for Python AI Layer integration
    /// Provides C# interface to Python AI tools via Interface Bridge
    /// Pattern: AINLP.three-layer-integration
    /// </summary>
    public class AILayerClient : IDisposable
    {
        private readonly HttpClient _httpClient;
        private readonly string _baseUrl;
        private bool _disposed;

        /// <summary>
        /// Initialize AI Layer client with Interface Bridge URL
        /// </summary>
        /// <param name="baseUrl">
        /// Interface Bridge URL (default: http://localhost:8001)
        /// </param>
        public AILayerClient(string baseUrl = "http://localhost:8001")
        {
            _baseUrl = baseUrl;
            _httpClient = new HttpClient
            {
                BaseAddress = new Uri(baseUrl),
                Timeout = TimeSpan.FromSeconds(30)
            };
        }

        /// <summary>
        /// Health check for AI Layer connectivity
        /// </summary>
        public async Task<HealthCheckResponse> HealthCheckAsync()
        {
            try
            {
                var response = await _httpClient.GetAsync("/health");
                response.EnsureSuccessStatusCode();

                var json = await response.Content.ReadAsStringAsync();
                return JsonSerializer.Deserialize<HealthCheckResponse>(json);
            }
            catch (Exception ex)
            {
                return new HealthCheckResponse
                {
                    Status = "unhealthy",
                    Error = ex.Message
                };
            }
        }

        /// <summary>
        /// AI Similarity Search with LLM reasoning
        /// Phase 11: Embedding + LLM consensus scoring
        /// </summary>
        /// <param name="query">Functionality to search for</param>
        /// <param name="maxResults">Maximum results (default: 5)</param>
        public async Task<SimilaritySearchResponse> SimilaritySearchAsync(
            string query,
            int maxResults = 5
        )
        {
            try
            {
                var request = new SimilaritySearchRequest
                {
                    Query = query,
                    MaxResults = maxResults
                };

                var json = JsonSerializer.Serialize(request);
                var content = new StringContent(
                    json,
                    Encoding.UTF8,
                    "application/json"
                );

                var response = await _httpClient.PostAsync(
                    "/ai/similarity",
                    content
                );
                response.EnsureSuccessStatusCode();

                var responseJson = await response.Content.ReadAsStringAsync();
                return JsonSerializer.Deserialize<SimilaritySearchResponse>(
                    responseJson
                );
            }
            catch (HttpRequestException ex)
            {
                return new SimilaritySearchResponse
                {
                    Error = $"HTTP request failed: {ex.Message}",
                    Results = new List<SimilarityResult>()
                };
            }
            catch (Exception ex)
            {
                return new SimilaritySearchResponse
                {
                    Error = $"Search failed: {ex.Message}",
                    Results = new List<SimilarityResult>()
                };
            }
        }

        /// <summary>
        /// Get neuron database statistics
        /// </summary>
        public async Task<NeuronStatsResponse> GetNeuronStatsAsync()
        {
            try
            {
                var response = await _httpClient.GetAsync("/ai/neurons");
                response.EnsureSuccessStatusCode();

                var json = await response.Content.ReadAsStringAsync();
                return JsonSerializer.Deserialize<NeuronStatsResponse>(json);
            }
            catch (Exception ex)
            {
                return new NeuronStatsResponse
                {
                    Error = ex.Message
                };
            }
        }

        /// <summary>
        /// Get all discovered AI tools
        /// </summary>
        public async Task<ToolsResponse> GetToolsAsync()
        {
            try
            {
                var response = await _httpClient.GetAsync("/tools");
                response.EnsureSuccessStatusCode();

                var json = await response.Content.ReadAsStringAsync();
                return JsonSerializer.Deserialize<ToolsResponse>(json);
            }
            catch (Exception ex)
            {
                return new ToolsResponse
                {
                    Error = ex.Message,
                    Tools = new List<AIToolMetadata>()
                };
            }
        }

        public void Dispose()
        {
            if (!_disposed)
            {
                _httpClient?.Dispose();
                _disposed = true;
            }
        }
    }

    // ======================================================================
    // Data Transfer Objects (DTOs) for Interface Bridge Communication
    // ======================================================================

    public class SimilaritySearchRequest
    {
        [JsonPropertyName("query")]
        public string Query { get; set; }

        [JsonPropertyName("max_results")]
        public int MaxResults { get; set; }
    }

    public class SimilaritySearchResponse
    {
        [JsonPropertyName("results")]
        public List<SimilarityResult> Results { get; set; }

        [JsonPropertyName("query")]
        public string Query { get; set; }

        [JsonPropertyName("method")]
        public string Method { get; set; }

        [JsonPropertyName("total_results")]
        public int TotalResults { get; set; }

        [JsonPropertyName("error")]
        public string Error { get; set; }
    }

    public class SimilarityResult
    {
        [JsonPropertyName("neuron")]
        public string Neuron { get; set; }

        [JsonPropertyName("similarity")]
        public double Similarity { get; set; }

        [JsonPropertyName("embedding_score")]
        public double EmbeddingScore { get; set; }

        [JsonPropertyName("llm_score")]
        public double LlmScore { get; set; }

        [JsonPropertyName("reasoning")]
        public string Reasoning { get; set; }

        [JsonPropertyName("path")]
        public string Path { get; set; }

        [JsonPropertyName("purpose")]
        public string Purpose { get; set; }
    }

    public class HealthCheckResponse
    {
        [JsonPropertyName("status")]
        public string Status { get; set; }

        [JsonPropertyName("bridge_version")]
        public string BridgeVersion { get; set; }

        [JsonPropertyName("tools_discovered")]
        public int ToolsDiscovered { get; set; }

        [JsonPropertyName("discovery_age_seconds")]
        public double? DiscoveryAgeSeconds { get; set; }

        [JsonPropertyName("sequencer_status")]
        public string SequencerStatus { get; set; }

        [JsonPropertyName("capabilities")]
        public Dictionary<string, bool> Capabilities { get; set; }

        [JsonPropertyName("timestamp")]
        public string Timestamp { get; set; }

        [JsonPropertyName("error")]
        public string Error { get; set; }
    }

    public class NeuronStatsResponse
    {
        [JsonPropertyName("total_neurons")]
        public int TotalNeurons { get; set; }

        [JsonPropertyName("embeddings_generated")]
        public bool EmbeddingsGenerated { get; set; }

        [JsonPropertyName("supercells")]
        public Dictionary<string, int> Supercells { get; set; }

        [JsonPropertyName("database_path")]
        public string DatabasePath { get; set; }

        [JsonPropertyName("error")]
        public string Error { get; set; }
    }

    public class ToolsResponse
    {
        [JsonPropertyName("tools")]
        public List<AIToolMetadata> Tools { get; set; }

        [JsonPropertyName("total_count")]
        public int TotalCount { get; set; }

        [JsonPropertyName("last_discovery")]
        public string LastDiscovery { get; set; }

        [JsonPropertyName("error")]
        public string Error { get; set; }
    }

    public class AIToolMetadata
    {
        [JsonPropertyName("name")]
        public string Name { get; set; }

        [JsonPropertyName("display_name")]
        public string DisplayName { get; set; }

        [JsonPropertyName("description")]
        public string Description { get; set; }

        [JsonPropertyName("category")]
        public string Category { get; set; }

        [JsonPropertyName("version")]
        public string Version { get; set; }

        [JsonPropertyName("status")]
        public string Status { get; set; }

        [JsonPropertyName("capabilities")]
        public List<string> Capabilities { get; set; }
    }
}
