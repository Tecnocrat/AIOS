package com.tecnocrat.aios

import com.intellij.openapi.application.ApplicationManager
import com.intellij.openapi.components.ApplicationComponent

/**
 * Application component for AIOS MCP plugin initialization
 */
class AIOSMCPApplicationComponent : ApplicationComponent {

    override fun initComponent() {
        // Initialize the MCP service
        val service = AIOSMCPService.getInstance()
        // Auto-connect if configured (would read from settings in real implementation)
        // service.connect()
    }

    override fun disposeComponent() {
        // Cleanup
        val service = AIOSMCPService.getInstance()
        service.disconnect()
    }

    override fun getComponentName(): String {
        return "AIOSMCPApplicationComponent"
    }
}