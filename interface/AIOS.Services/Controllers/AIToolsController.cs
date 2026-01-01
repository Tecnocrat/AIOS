using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;
using AIOS.Models;
using System.Text.Json;

namespace AIOS.Services.Controllers
{
    /// <summary>
    /// REST API Controller for Python AI Tools Integration
    /// Provides HTTP endpoints for tool discovery, execution, and metadata management
    /// </summary>
    [ApiController]
    [Route("api/[controller]")]
    public class AIToolsController : ControllerBase
    {
        private readonly PythonAIToolsService _pythonToolsService;
        private readonly ILogger<AIToolsController> _logger;

        public AIToolsController(PythonAIToolsService pythonToolsService, ILogger<AIToolsController> logger)
        {
            _pythonToolsService = pythonToolsService;
            _logger = logger;
        }

        /// <summary>
        /// Discover all available Python AI tools
        /// </summary>
        [HttpGet("discover")]
        public async Task<IActionResult> DiscoverTools()
        {
            try
            {
                var tools = await _pythonToolsService.GetAvailableToolsAsync();
                return Ok(tools);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Failed to discover Python AI tools");
                return StatusCode(500, new { error = ex.Message });
            }
        }

        /// <summary>
        /// Get metadata for all discovered tools
        /// </summary>
        [HttpGet("metadata")]
        public async Task<IActionResult> GetToolsMetadata()
        {
            try
            {
                var metadata = await _pythonToolsService.GenerateMetadataSnapshotAsync();
                return Ok(metadata);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Failed to get tools metadata");
                return StatusCode(500, new { error = ex.Message });
            }
        }

        /// <summary>
        /// Execute a specific Python AI tool
        /// </summary>
        [HttpPost("execute/{toolId}")]
        public async Task<IActionResult> ExecuteTool(string toolId, [FromBody] Dictionary<string, object> parameters)
        {
            try
            {
                var result = await _pythonToolsService.ExecuteToolAsync(toolId, parameters);
                return Ok(result);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Failed to execute tool {ToolId}", toolId);
                return StatusCode(500, new { error = ex.Message });
            }
        }

        /// <summary>
        /// Search tools by category, description, or capabilities
        /// </summary>
        [HttpGet("search")]
        public async Task<IActionResult> SearchTools([FromQuery] string query, [FromQuery] string? category = null)
        {
            try
            {
                var results = await _pythonToolsService.SearchToolsByCapabilityAsync(query);
                return Ok(results);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Failed to search tools with query '{Query}'", query);
                return StatusCode(500, new { error = ex.Message });
            }
        }

        /// <summary>
        /// Get health status of Python interface bridge
        /// </summary>
        [HttpGet("health")]
        public async Task<IActionResult> GetHealthStatus()
        {
            try
            {
                var isAvailable = await _pythonToolsService.IsInterfaceBridgeAvailable();
                var health = new { available = isAvailable, status = isAvailable ? "healthy" : "unavailable" };
                return Ok(health);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Failed to get health status");
                return StatusCode(500, new { error = ex.Message });
            }
        }

        /// <summary>
        /// Refresh the tools cache by re-discovering all Python AI tools
        /// </summary>
        [HttpPost("refresh")]
        public async Task<IActionResult> RefreshTools()
        {
            try
            {
                await _pythonToolsService.RefreshAvailableToolsAsync();
                return Ok(new { message = "Tools cache refreshed successfully" });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Failed to refresh tools cache");
                return StatusCode(500, new { error = ex.Message });
            }
        }

        /// <summary>
        /// Generate C# bridge classes for discovered Python tools
        /// </summary>
        [HttpPost("generate-bridge")]
        public IActionResult GenerateBridge()
        {
            try
            {
                // TODO: Implement GenerateCSharpBridgeAsync in PythonAIToolsService
                return Ok(new { message = "Bridge generation not yet implemented", bridge_code = "" });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Failed to generate C# bridge");
                return StatusCode(500, new { error = ex.Message });
            }
        }
    }
}