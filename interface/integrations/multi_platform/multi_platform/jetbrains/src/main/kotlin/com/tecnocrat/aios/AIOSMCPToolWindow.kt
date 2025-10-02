package com.tecnocrat.aios

import com.intellij.openapi.components.Service
import com.intellij.openapi.project.Project
import com.intellij.openapi.wm.ToolWindow
import com.intellij.openapi.wm.ToolWindowFactory
import com.intellij.ui.components.JBScrollPane
import com.intellij.ui.table.JBTable
import java.awt.BorderLayout
import javax.swing.*
import javax.swing.table.DefaultTableModel

/**
 * Project-level service for AIOS MCP integration
 */
@Service(Service.Level.PROJECT)
class AIOSMCPProjectService(private val project: Project) {

    private var toolWindow: ToolWindow? = null

    fun setToolWindow(toolWindow: ToolWindow) {
        this.toolWindow = toolWindow
    }

    fun refreshToolWindow() {
        toolWindow?.contentManager?.contents?.forEach { content ->
            if (content.component is AIOSMCPPanel) {
                (content.component as AIOSMCPPanel).refresh()
            }
        }
    }
}

/**
 * Tool window factory for AIOS MCP integration
 */
class AIOSMCPToolWindowFactory : ToolWindowFactory {

    override fun createToolWindowContent(project: Project, toolWindow: ToolWindow) {
        val projectService = project.getService(AIOSMCPProjectService::class.java)
        projectService.setToolWindow(toolWindow)

        val panel = AIOSMCPPanel(project)
        val content = toolWindow.contentManager.factory.createContent(panel, "AIOS MCP", false)
        toolWindow.contentManager.addContent(content)
    }
}

/**
 * Main panel for AIOS MCP tool window
 */
class AIOSMCPPanel(private val project: Project) : JPanel(BorderLayout()) {

    private val service = AIOSMCPService.getInstance()
    private val statusLabel = JLabel("Disconnected")
    private val serversTable = JBTable()
    private val refreshButton = JButton("Refresh")

    init {
        setupUI()
        setupListeners()
        refresh()
    }

    private fun setupUI() {
        // Status panel
        val statusPanel = JPanel(BorderLayout())
        statusPanel.border = BorderFactory.createTitledBorder("Connection Status")
        statusPanel.add(statusLabel, BorderLayout.CENTER)

        val connectButton = JButton("Connect")
        val disconnectButton = JButton("Disconnect")

        connectButton.addActionListener { connect() }
        disconnectButton.addActionListener { disconnect() }
        refreshButton.addActionListener { refresh() }

        val buttonPanel = JPanel()
        buttonPanel.add(connectButton)
        buttonPanel.add(disconnectButton)
        buttonPanel.add(refreshButton)

        statusPanel.add(buttonPanel, BorderLayout.SOUTH)

        // Servers table
        val tablePanel = JPanel(BorderLayout())
        tablePanel.border = BorderFactory.createTitledBorder("MCP Servers")

        serversTable.model = DefaultTableModel(
            arrayOf("Server", "Status", "Tools"),
            0
        )
        tablePanel.add(JBScrollPane(serversTable), BorderLayout.CENTER)

        // Consciousness panel
        val consciousnessPanel = JPanel(BorderLayout())
        consciousnessPanel.border = BorderFactory.createTitledBorder("Consciousness Monitor")

        val consciousnessLabel = JLabel("Level: -- | Coherence: -- | Evolution: --")
        consciousnessPanel.add(consciousnessLabel, BorderLayout.CENTER)

        val monitorButton = JButton("Monitor Consciousness")
        monitorButton.addActionListener {
            val metrics = service.getConsciousnessMetrics()
            if (metrics != null) {
                consciousnessLabel.text = String.format(
                    "Level: %.3f | Coherence: %.3f | Evolution: %.3f",
                    metrics.level, metrics.coherence, metrics.evolutionPotential
                )
            } else {
                consciousnessLabel.text = "Failed to get consciousness metrics"
            }
        }
        consciousnessPanel.add(monitorButton, BorderLayout.SOUTH)

        // Main layout
        add(statusPanel, BorderLayout.NORTH)
        add(tablePanel, BorderLayout.CENTER)
        add(consciousnessPanel, BorderLayout.SOUTH)
    }

    private fun setupListeners() {
        // Add any additional listeners here
    }

    private fun connect() {
        val success = service.connect()
        statusLabel.text = if (success) "Connected" else "Connection Failed"
        refresh()
    }

    private fun disconnect() {
        service.disconnect()
        statusLabel.text = "Disconnected"
        refresh()
    }

    fun refresh() {
        val status = service.getStatus()
        val connected = status["connected"] as Boolean
        statusLabel.text = if (connected) "Connected" else "Disconnected"

        // Update servers table
        val tableModel = serversTable.model as DefaultTableModel
        tableModel.rowCount = 0

        val servers = status["servers"] as List<MCPServerInfo>
        for (server in servers) {
            tableModel.addRow(arrayOf(
                server.name,
                server.status,
                server.tools.size.toString()
            ))
        }
    }
}