package com.tecnocrat.aios.actions

import com.intellij.openapi.actionSystem.AnAction
import com.intellij.openapi.actionSystem.AnActionEvent
import com.intellij.openapi.ui.Messages
import com.tecnocrat.aios.AIOSMCPService

/**
 * Connect to AIOS MCP Servers action
 */
class ConnectAction : AnAction() {
    override fun actionPerformed(e: AnActionEvent) {
        val service = AIOSMCPService.getInstance()
        val success = service.connect()

        val message = if (success) {
            "Successfully connected to AIOS MCP servers"
        } else {
            "Failed to connect to AIOS MCP servers"
        }

        Messages.showInfoMessage(e.project, message, "AIOS MCP")
    }
}

/**
 * Disconnect from AIOS MCP Servers action
 */
class DisconnectAction : AnAction() {
    override fun actionPerformed(e: AnActionEvent) {
        val service = AIOSMCPService.getInstance()
        service.disconnect()

        Messages.showInfoMessage(e.project, "Disconnected from AIOS MCP servers", "AIOS MCP")
    }
}

/**
 * Show MCP Server Status action
 */
class StatusAction : AnAction() {
    override fun actionPerformed(e: AnActionEvent) {
        val service = AIOSMCPService.getInstance()
        val status = service.getStatus()

        val connected = status["connected"] as Boolean
        val servers = status["servers"] as List<*>

        val message = buildString {
            append("Connection Status: ${if (connected) "Connected" else "Disconnected"}\n")
            append("MCP Servers: ${servers.size}\n")
            servers.forEach { server ->
                // This would need proper type casting in a real implementation
                append("- ${server.toString()}\n")
            }
        }

        Messages.showInfoMessage(e.project, message, "AIOS MCP Status")
    }
}

/**
 * Consciousness Monitor action
 */
class ConsciousnessMonitorAction : AnAction() {
    override fun actionPerformed(e: AnActionEvent) {
        val service = AIOSMCPService.getInstance()
        val metrics = service.getConsciousnessMetrics()

        val message = if (metrics != null) {
            "Consciousness Metrics:\n" +
            "Level: ${metrics.level}\n" +
            "Coherence: ${metrics.coherence}\n" +
            "Evolution Potential: ${metrics.evolutionPotential}\n" +
            "Timestamp: ${metrics.timestamp}"
        } else {
            "Failed to retrieve consciousness metrics"
        }

        Messages.showInfoMessage(e.project, message, "Consciousness Monitor")
    }
}

/**
 * Evolution Tracker action
 */
class EvolutionTrackerAction : AnAction() {
    override fun actionPerformed(e: AnActionEvent) {
        val service = AIOSMCPService.getInstance()
        // Execute evolution tracking tool
        val result = service.executeTool("evolution_mcp_server", "list_experiments", emptyMap())

        val message = if (result != null) {
            "Evolution Experiments:\n${result["result"]}"
        } else {
            "Failed to retrieve evolution experiments"
        }

        Messages.showInfoMessage(e.project, message, "Evolution Tracker")
    }
}

/**
 * Agentic Orchestrator action
 */
class AgenticOrchestratorAction : AnAction() {
    override fun actionPerformed(e: AnActionEvent) {
        val service = AIOSMCPService.getInstance()
        // Execute agentic behavior tool
        val result = service.executeTool("agentic_mcp_server", "get_status", emptyMap())

        val message = if (result != null) {
            "Agentic Status:\n${result["result"]}"
        } else {
            "Failed to retrieve agentic status"
        }

        Messages.showInfoMessage(e.project, message, "Agentic Orchestrator")
    }
}