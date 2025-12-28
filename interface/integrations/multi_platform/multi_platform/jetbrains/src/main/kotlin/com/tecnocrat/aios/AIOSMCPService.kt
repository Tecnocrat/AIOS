package com.tecnocrat.aios

import com.google.gson.Gson
import com.google.gson.JsonObject
import com.intellij.openapi.application.ApplicationManager
import com.intellij.openapi.components.Service
import com.intellij.openapi.diagnostic.Logger
import okhttp3.*
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.RequestBody.Companion.toRequestBody
import java.io.IOException
import java.util.concurrent.TimeUnit

/**
 * MCP Server information
 */
data class MCPServerInfo(
    val name: String,
    val description: String,
    val tools: List<MCPTool>,
    val status: String
)

/**
 * MCP Tool information
 */
data class MCPTool(
    val name: String,
    val description: String,
    val inputSchema: JsonObject
)

/**
 * Consciousness metrics
 */
data class ConsciousnessMetrics(
    val level: Double,
    val coherence: Double,
    val evolutionPotential: Double,
    val timestamp: String
)

/**
 * AIOS MCP Service for JetBrains IDEs
 * Provides integration with AIOS Interface Bridge and MCP servers
 */
@Service(Service.Level.APP)
class AIOSMCPService {
    private val logger = Logger.getInstance(AIOSMCPService::class.java)
    private val gson = Gson()
    private val client = OkHttpClient.Builder()
        .connectTimeout(30, TimeUnit.SECONDS)
        .readTimeout(30, TimeUnit.SECONDS)
        .writeTimeout(30, TimeUnit.SECONDS)
        .build()

    private val interfaceBridgeUrl = "http://localhost:8000"
    private val servers = mutableMapOf<String, MCPServerInfo>()
    private var isConnected = false

    companion object {
        fun getInstance(): AIOSMCPService = ApplicationManager.getApplication().getService(AIOSMCPService::class.java)
    }

    /**
     * Connect to AIOS MCP servers via Interface Bridge
     */
    fun connect(): Boolean {
        return try {
            logger.info("Connecting to AIOS MCP servers...")

            // Test Interface Bridge connectivity
            val healthRequest = Request.Builder()
                .url("$interfaceBridgeUrl/health")
                .build()

            client.newCall(healthRequest).execute().use { response ->
                if (!response.isSuccessful) {
                    throw IOException("Interface Bridge health check failed: ${response.code}")
                }
            }

            // Discover available tools
            val toolsRequest = Request.Builder()
                .url("$interfaceBridgeUrl/tools")
                .build()

            client.newCall(toolsRequest).execute().use { response ->
                if (!response.isSuccessful) {
                    throw IOException("Failed to discover tools: ${response.code}")
                }

                val responseBody = response.body?.string()
                if (responseBody != null) {
                    val toolsData = gson.fromJson(responseBody, Array<JsonObject>::class.java)
                    logger.info("Discovered ${toolsData.size} tools from Interface Bridge")

                    initializeMCPServers(toolsData.toList())
                }
            }

            isConnected = true
            logger.info("Successfully connected to AIOS MCP servers")
            true
        } catch (e: Exception) {
            logger.error("Failed to connect to AIOS MCP servers", e)
            isConnected = false
            false
        }
    }

    /**
     * Disconnect from MCP servers
     */
    fun disconnect() {
        logger.info("Disconnecting from AIOS MCP servers...")
        servers.clear()
        isConnected = false
        logger.info("Disconnected from AIOS MCP servers")
    }

    /**
     * Get MCP server status
     */
    fun getStatus(): Map<String, Any> {
        return mapOf(
            "connected" to isConnected,
            "servers" to servers.values.toList()
        )
    }

    /**
     * Execute MCP tool
     */
    fun executeTool(serverName: String, toolName: String, parameters: Map<String, Any>): Map<String, Any>? {
        return try {
            val requestBody = JsonObject().apply {
                addProperty("tool_name", toolName)
                add("parameters", gson.toJsonTree(parameters))
            }

            val request = Request.Builder()
                .url("$interfaceBridgeUrl/tools/$serverName/execute")
                .post(requestBody.toString().toRequestBody("application/json".toMediaType()))
                .build()

            client.newCall(request).execute().use { response ->
                if (!response.isSuccessful) {
                    throw IOException("Tool execution failed: ${response.code}")
                }

                val responseBody = response.body?.string()
                if (responseBody != null) {
                    gson.fromJson(responseBody, Map::class.java) as Map<String, Any>
                } else {
                    null
                }
            }
        } catch (e: Exception) {
            logger.error("Failed to execute MCP tool", e)
            null
        }
    }

    /**
     * Get consciousness metrics
     */
    fun getConsciousnessMetrics(): ConsciousnessMetrics? {
        return try {
            val request = Request.Builder()
                .url("$interfaceBridgeUrl/consciousness/metrics")
                .build()

            client.newCall(request).execute().use { response ->
                if (!response.isSuccessful) {
                    return null
                }

                val responseBody = response.body?.string()
                if (responseBody != null) {
                    gson.fromJson(responseBody, ConsciousnessMetrics::class.java)
                } else {
                    null
                }
            }
        } catch (e: Exception) {
            logger.error("Failed to get consciousness metrics", e)
            null
        }
    }

    private fun initializeMCPServers(toolsData: List<JsonObject>) {
        // Group tools by server
        val serverTools = mutableMapOf<String, MutableList<JsonObject>>()

        for (tool in toolsData) {
            val serverName = tool.get("server")?.asString ?: "unknown"
            serverTools.getOrPut(serverName) { mutableListOf() }.add(tool)
        }

        // Create server info for each server
        for ((serverName, tools) in serverTools) {
            val mcpTools = tools.map { tool ->
                MCPTool(
                    name = tool.get("name")?.asString ?: "",
                    description = tool.get("description")?.asString ?: "",
                    inputSchema = tool.get("input_schema")?.asJsonObject ?: JsonObject()
                )
            }

            val serverInfo = MCPServerInfo(
                name = serverName,
                description = "AIOS $serverName MCP server",
                tools = mcpTools,
                status = "connected"
            )

            servers[serverName] = serverInfo
        }
    }
}