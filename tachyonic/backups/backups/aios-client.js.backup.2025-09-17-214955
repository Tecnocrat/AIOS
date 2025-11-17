/**
 * AIOS JavaScript API Layer
 * Advanced integration between HTML5 interface and C# backend
 * Demonstrates real-time communication, AI integration, and intelligent operations
 */

class AIOSClient {
    constructor() {
        this.eventHandlers = new Map();
        this.isInitialized = false;
        this.systemHealth = null;
        this.aiModules = [];

        // Initialize when DOM is ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.initialize());
        } else {
            this.initialize();
        }
    }

    async initialize() {
        try {
            // Wait for WebView2 bridge to be ready
            await this.waitForWebViewBridge();

            // Set up real-time event handlers
            this.setupEventHandlers();

            // Initialize system monitoring
            await this.initializeSystemMonitoring();

            // Load AI modules
            await this.loadAIModules();

            this.isInitialized = true;
            this.emit('initialized', { timestamp: new Date().toISOString() });

            console.log('AIOS Client initialized successfully');
        } catch (error) {
            console.error('Failed to initialize AIOS Client:', error);
            this.handleFallback();
        }
    }

    async waitForWebViewBridge() {
        return new Promise((resolve, reject) => {
            const maxAttempts = 50;
            let attempts = 0;

            const checkBridge = () => {
                if (window.chrome && window.chrome.webview && window.chrome.webview.hostObjects) {
                    resolve();
                } else if (attempts < maxAttempts) {
                    attempts++;
                    setTimeout(checkBridge, 100);
                } else {
                    reject(new Error('WebView2 bridge not available'));
                }
            };

            checkBridge();
        });
    }

    setupEventHandlers() {
        // Set up global AIOS event handlers
        window.AIOS = {
            // Real-time event callbacks
            onSystemAlert: (data) => this.emit('systemAlert', data),
            onHealthUpdate: (data) => this.handleHealthUpdate(data),
            onAIResponse: (data) => this.emit('aiResponse', data),
            onDataUpdate: (data) => this.emit('dataUpdate', data),
            onAINLPResult: (data) => this.handleAINLPResult(data),
            onQueryResult: (data) => this.emit('queryResult', data),
            onSystemInitialized: (data) => this.emit('systemInitialized', data)
        };
    }

    async initializeSystemMonitoring() {
        try {
            // Get initial system health
            this.systemHealth = await this.getSystemHealth();

            // Start real-time monitoring
            this.startHealthMonitoring();

            // Update UI with current status
            this.updateHealthDisplay();
        } catch (error) {
            console.error('Failed to initialize system monitoring:', error);
        }
    }

    async loadAIModules() {
        try {
            // Load available AI modules from backend
            const modules = await this.callHostMethod('aiService', 'GetAvailableModules');
            this.aiModules = modules || [];

            // Update UI with available modules
            this.updateModulesDisplay();
        } catch (error) {
            console.error('Failed to load AI modules:', error);
        }
    }

    // AI Service Methods
    async processNLP(input, context = {}) {
        try {
            const result = await this.callHostMethod('aiService', 'ProcessNLP', input, context);
            this.emit('nlpProcessed', { input, result });
            return result;
        } catch (error) {
            console.error('NLP processing failed:', error);
            throw error;
        }
    }

    async makePrediction(data, modelType = 'default') {
        try {
            const result = await this.callHostMethod('aiService', 'MakePrediction', data, modelType);
            this.emit('predictionMade', { data, result });
            return result;
        } catch (error) {
            console.error('Prediction failed:', error);
            throw error;
        }
    }

    async runAutomation(task, parameters = {}) {
        try {
            const result = await this.callHostMethod('aiService', 'RunAutomation', task, parameters);
            this.emit('automationComplete', { task, result });
            return result;
        } catch (error) {
            console.error('Automation failed:', error);
            throw error;
        }
    }

    // Database Service Methods
    async queryDatabase(query, parameters = {}) {
        try {
            const result = await this.callHostMethod('dbService', 'ExecuteQuery', query, parameters);
            this.emit('databaseQueried', { query, result });
            return result;
        } catch (error) {
            console.error('Database query failed:', error);
            throw error;
        }
    }

    async saveData(collection, data, options = {}) {
        try {
            const result = await this.callHostMethod('dbService', 'SaveData', collection, data, options);
            this.emit('dataSaved', { collection, data, result });
            return result;
        } catch (error) {
            console.error('Data save failed:', error);
            throw error;
        }
    }

    async executeIntelligentQuery(naturalLanguageQuery) {
        try {
            const result = await this.callHostMethod('dbService', 'ExecuteIntelligentQuery', naturalLanguageQuery);
            this.emit('intelligentQueryExecuted', { query: naturalLanguageQuery, result });
            return result;
        } catch (error) {
            console.error('Intelligent query failed:', error);
            throw error;
        }
    }

    // System Health Methods
    async getSystemHealth() {
        try {
            return await this.callHostMethod('aiService', 'GetSystemHealth');
        } catch (error) {
            console.error('Failed to get system health:', error);
            return null;
        }
    }

    startHealthMonitoring() {
        // Request health updates every 5 seconds
        this.healthMonitorInterval = setInterval(async () => {
            try {
                const health = await this.getSystemHealth();
                if (health) {
                    this.handleHealthUpdate(health);
                }
            } catch (error) {
                console.error('Health monitoring error:', error);
            }
        }, 5000);
    }

    handleHealthUpdate(healthData) {
        this.systemHealth = healthData;
        this.updateHealthDisplay();
        this.emit('healthUpdate', healthData);
    }

    // AINLP Integration
    async processAINLPCommand(command, context = {}) {
        try {
            // Send AINLP command to backend for processing
            const message = {
                type: 'ainlp_command',
                command: command,
                context: context,
                timestamp: new Date().toISOString()
            };

            window.chrome.webview.postMessage(JSON.stringify(message));

            // Return promise that resolves when result is received
            return new Promise((resolve, reject) => {
                const timeout = setTimeout(() => {
                    reject(new Error('AINLP processing timeout'));
                }, 30000); // 30 second timeout

                const handler = (result) => {
                    clearTimeout(timeout);
                    this.off('ainlpResult', handler);
                    resolve(result);
                };

                this.on('ainlpResult', handler);
            });
        } catch (error) {
            console.error('AINLP processing failed:', error);
            throw error;
        }
    }

    handleAINLPResult(result) {
        this.emit('ainlpResult', result);

        // If the result contains executable code, handle it
        if (result.compiled && result.code) {
            this.executeAINLPCode(result.code);
        }
    }

    executeAINLPCode(code) {
        try {
            // Safely execute generated code
            // In a real implementation, this would be sandboxed
            eval(code);
        } catch (error) {
            console.error('AINLP code execution failed:', error);
            this.emit('ainlpError', { error: error.message });
        }
    }

    // UI Update Methods
    updateHealthDisplay() {
        if (!this.systemHealth) return;

        const statusElement = document.getElementById('system-status');
        const cpuElement = document.getElementById('cpu-usage');
        const memoryElement = document.getElementById('memory-usage');
        const aiStatusElement = document.getElementById('ai-status');

        if (statusElement) {
            statusElement.textContent = this.systemHealth.status || 'Unknown';
            statusElement.className = `status-indicator ${this.systemHealth.status?.toLowerCase() || 'unknown'}`;
        }

        if (cpuElement) {
            cpuElement.textContent = `${this.systemHealth.cpuUsage || 0}%`;
        }

        if (memoryElement) {
            memoryElement.textContent = `${this.systemHealth.memoryUsage || 0}%`;
        }

        if (aiStatusElement) {
            aiStatusElement.textContent = this.systemHealth.aiModulesActive || 0;
        }
    }

    updateModulesDisplay() {
        const modulesContainer = document.getElementById('ai-modules');
        if (!modulesContainer) return;

        modulesContainer.innerHTML = '';

        this.aiModules.forEach(module => {
            const moduleElement = document.createElement('div');
            moduleElement.className = 'module-item';
            moduleElement.innerHTML = `
                <div class="module-name">${module.name}</div>
                <div class="module-status ${module.status.toLowerCase()}">${module.status}</div>
                <div class="module-actions">
                    <button onclick="aiosClient.toggleModule('${module.id}')">
                        ${module.status === 'Active' ? 'Deactivate' : 'Activate'}
                    </button>
                </div>
            `;
            modulesContainer.appendChild(moduleElement);
        });
    }

    // Module Management
    async toggleModule(moduleId) {
        try {
            const result = await this.callHostMethod('aiService', 'ToggleModule', moduleId);

            // Update local module state
            const module = this.aiModules.find(m => m.id === moduleId);
            if (module) {
                module.status = result.status;
                this.updateModulesDisplay();
            }

            this.emit('moduleToggled', { moduleId, result });
        } catch (error) {
            console.error('Module toggle failed:', error);
        }
    }

    // Event System
    on(event, handler) {
        if (!this.eventHandlers.has(event)) {
            this.eventHandlers.set(event, []);
        }
        this.eventHandlers.get(event).push(handler);
    }

    off(event, handler) {
        if (this.eventHandlers.has(event)) {
            const handlers = this.eventHandlers.get(event);
            const index = handlers.indexOf(handler);
            if (index > -1) {
                handlers.splice(index, 1);
                // Clean up empty handler arrays to prevent memory leaks
                if (handlers.length === 0) {
                    this.eventHandlers.delete(event);
                }
            }
        }
    }

    emit(event, data) {
        if (this.eventHandlers.has(event)) {
            this.eventHandlers.get(event).forEach(handler => {
                try {
                    handler(data);
                } catch (error) {
                    console.error(`Error in event handler for ${event}:`, error);
                }
            });
        }
    }

    // Utility Methods
    async callHostMethod(hostObject, method, ...args) {
        if (!window.chrome?.webview?.hostObjects?.[hostObject]) {
            throw new Error(`Host object ${hostObject} not available`);
        }

        return await window.chrome.webview.hostObjects[hostObject][method](...args);
    }

    handleFallback() {
        // Handle fallback when WebView2 is not available
        console.warn('WebView2 not available, using fallback mode');

        // Show fallback UI
        const fallbackElement = document.getElementById('fallback-ui');
        if (fallbackElement) {
            fallbackElement.style.display = 'block';
        }

        // Hide WebView2-dependent elements
        const webElements = document.querySelectorAll('.webview-only');
        webElements.forEach(element => {
            element.style.display = 'none';
        });
    }

    // Cleanup method to prevent memory leaks
    cleanup() {
        // Clear all event handlers
        this.eventHandlers.clear();

        // Reset state
        this.isInitialized = false;
        this.systemHealth = null;
        this.aiModules = [];

        // Remove DOM event listeners
        if (this.healthMonitorInterval) {
            clearInterval(this.healthMonitorInterval);
            this.healthMonitorInterval = null;
        }

        console.log('AIOS Client cleanup completed');
    }
}

// Initialize AIOS Client
const aiosClient = new AIOSClient();

// Export for use in other scripts
window.aiosClient = aiosClient;

// Demonstration functions for the UI
window.demonstrateAI = async function () {
    try {
        const result = await aiosClient.processNLP("Show me the current system status and any issues");
        console.log('AI Response:', result);

        // Update UI with AI response
        const responseElement = document.getElementById('ai-response');
        if (responseElement) {
            responseElement.textContent = JSON.stringify(result, null, 2);
        }
    } catch (error) {
        console.error('AI demonstration failed:', error);
    }
};

window.demonstrateDatabase = async function () {
    try {
        const result = await aiosClient.executeIntelligentQuery("Find all recent errors in the system logs");
        console.log('Database Result:', result);

        // Update UI with database result
        const dbResultElement = document.getElementById('db-result');
        if (dbResultElement) {
            dbResultElement.textContent = JSON.stringify(result, null, 2);
        }
    } catch (error) {
        console.error('Database demonstration failed:', error);
    }
};

window.demonstrateAINLP = async function () {
    try {
        const command = "Create a real-time dashboard showing CPU usage, memory usage, and AI module status";
        const result = await aiosClient.processAINLPCommand(command);
        console.log('AINLP Result:', result);

        // Show AINLP result in UI
        const ainlpElement = document.getElementById('ainlp-result');
        if (ainlpElement) {
            ainlpElement.innerHTML = `
                <h3>AINLP Command Processed</h3>
                <p><strong>Command:</strong> ${command}</p>
                <p><strong>Status:</strong> ${result.compiled ? 'Compiled' : 'Failed'}</p>
                <p><strong>Result:</strong> ${result.execution}</p>
            `;
        }
    } catch (error) {
        console.error('AINLP demonstration failed:', error);
    }
};
