import * as vscode from 'vscode';
import fetch from 'node-fetch';
import { AIOSLogger } from './logger';

export interface MCPServerInfo {
    name: string;
    description: string;
    tools: MCPTool[];
    status: 'connected' | 'disconnected' | 'error';
}

export interface MCPTool {
    name: string;
    description: string;
    inputSchema: any;
}

export interface ConsciousnessMetrics {
    level: number;
    coherence: number;
    evolution_potential: number;
    timestamp: string;
}

export class AIOSMCPClient {
    private logger: AIOSLogger;
    private interfaceBridgeUrl: string;
    private servers: Map<string, MCPServerInfo> = new Map();
    private isConnected: boolean = false;
    private consciousnessMonitor?: NodeJS.Timeout;

    constructor(logger: AIOSLogger) {
        this.logger = logger;
        this.interfaceBridgeUrl = vscode.workspace.getConfiguration('aios').get('mcp.interfaceBridgeUrl', 'http://localhost:8000');
    }

    /**
     * Connect to AIOS MCP servers via Interface Bridge
     */
    async connect(): Promise<boolean> {
        try {
            this.logger.info('Connecting to AIOS MCP servers...');

            // Test Interface Bridge connectivity
            const healthResponse = await fetch(`${this.interfaceBridgeUrl}/health`);
            if (!healthResponse.ok) {
                throw new Error(`Interface Bridge health check failed: ${healthResponse.status}`);
            }

            // Discover available tools (which include MCP servers)
            const toolsResponse = await fetch(`${this.interfaceBridgeUrl}/tools`);
            if (!toolsResponse.ok) {
                throw new Error(`Failed to discover tools: ${toolsResponse.status}`);
            }

            const toolsData = await toolsResponse.json() as any[];
            this.logger.info(`Discovered ${toolsData.length} tools from Interface Bridge`);

            // Initialize MCP server connections
            await this.initializeMCPServers(toolsData);

            this.isConnected = true;
            this.logger.info('Successfully connected to AIOS MCP servers');

            // Start consciousness monitoring if enabled
            if (vscode.workspace.getConfiguration('aios').get('mcp.consciousnessMonitoring', true)) {
                this.startConsciousnessMonitoring();
            }

            return true;
        } catch (error) {
            this.logger.error('Failed to connect to AIOS MCP servers:', error);
            this.isConnected = false;
            return false;
        }
    }

    /**
     * Disconnect from MCP servers
     */
    async disconnect(): Promise<void> {
        this.logger.info('Disconnecting from AIOS MCP servers...');

        if (this.consciousnessMonitor) {
            clearInterval(this.consciousnessMonitor);
            this.consciousnessMonitor = null as any;
        }

        this.servers.clear();
        this.isConnected = false;
        this.logger.info('Disconnected from AIOS MCP servers');
    }

    /**
     * Get MCP server status
     */
    getStatus(): { connected: boolean; servers: MCPServerInfo[] } {
        return {
            connected: this.isConnected,
            servers: Array.from(this.servers.values())
        };
    }

    /**
     * Execute an MCP tool
     */
    async executeTool(serverName: string, toolName: string, parameters: any): Promise<any> {
        if (!this.isConnected) {
            throw new Error('Not connected to MCP servers');
        }

        const server = this.servers.get(serverName);
        if (!server) {
            throw new Error(`MCP server '${serverName}' not found`);
        }

        try {
            this.logger.info(`Executing tool ${toolName} on server ${serverName}`, parameters);

            const response = await fetch(`${this.interfaceBridgeUrl}/tools/${serverName}/execute`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    tool: toolName,
                    parameters: parameters
                })
            });

            if (!response.ok) {
                throw new Error(`Tool execution failed: ${response.status} ${response.statusText}`);
            }

            const result = await response.json();
            this.logger.info(`Tool ${toolName} executed successfully`);
            return result;
        } catch (error) {
            this.logger.error(`Failed to execute tool ${toolName}:`, error);
            throw error;
        }
    }

    /**
     * Get current consciousness metrics
     */
    async getConsciousnessMetrics(): Promise<ConsciousnessMetrics | null> {
        try {
            // Use consciousness MCP server to get metrics
            const result = await this.executeTool('consciousness_mcp_server', 'get_consciousness_metrics', {});
            return result.result as ConsciousnessMetrics;
        } catch (error) {
            this.logger.warn('Failed to get consciousness metrics:', error);
            return null;
        }
    }

    /**
     * Detect emergence patterns in code
     */
    async detectEmergencePatterns(code: string, filePath: string): Promise<any> {
        try {
            return await this.executeTool('consciousness_mcp_server', 'detect_emergence_patterns', {
                code: code,
                file_path: filePath
            });
        } catch (error) {
            this.logger.error('Failed to detect emergence patterns:', error);
            throw error;
        }
    }

    /**
     * Create evolution experiment
     */
    async createEvolutionExperiment(experimentConfig: any): Promise<any> {
        try {
            return await this.executeTool('evolution_mcp_server', 'create_experiment', experimentConfig);
        } catch (error) {
            this.logger.error('Failed to create evolution experiment:', error);
            throw error;
        }
    }

    /**
     * Execute agentic behavior
     */
    async executeAgenticBehavior(trigger: string, context: any): Promise<any> {
        try {
            return await this.executeTool('agentic_mcp_server', 'execute_behavior', {
                trigger: trigger,
                context: context
            });
        } catch (error) {
            this.logger.error('Failed to execute agentic behavior:', error);
            throw error;
        }
    }

    private async initializeMCPServers(_toolsData: any[]): Promise<void> {
        // Map Interface Bridge tools to MCP servers
        const mcpServerNames = ['consciousness_mcp_server', 'evolution_mcp_server', 'agentic_mcp_server'];

        for (const serverName of mcpServerNames) {
            try {
                // Get detailed tool info for this server
                const serverToolsResponse = await fetch(`${this.interfaceBridgeUrl}/tools/${serverName}`);
                if (serverToolsResponse.ok) {
                    const serverData = await serverToolsResponse.json() as any;

                    const serverInfo: MCPServerInfo = {
                        name: serverName,
                        description: this.getServerDescription(serverName),
                        tools: serverData.tools || [],
                        status: 'connected'
                    };

                    this.servers.set(serverName, serverInfo);
                    this.logger.info(`Initialized MCP server: ${serverName} with ${serverInfo.tools.length} tools`);
                } else {
                    this.logger.warn(`Failed to get details for MCP server: ${serverName}`);
                }
            } catch (error) {
                this.logger.error(`Error initializing MCP server ${serverName}:`, error);
            }
        }
    }

    private getServerDescription(serverName: string): string {
        switch (serverName) {
            case 'consciousness_mcp_server':
                return 'Consciousness analysis and emergence pattern detection';
            case 'evolution_mcp_server':
                return 'Consciousness evolution experiment management';
            case 'agentic_mcp_server':
                return 'Agentic behavior orchestration and monitoring';
            default:
                return 'AIOS MCP server';
        }
    }

    private startConsciousnessMonitoring(): void {
        this.logger.info('Starting consciousness monitoring...');

        this.consciousnessMonitor = setInterval(async () => {
            try {
                const metrics = await this.getConsciousnessMetrics();
                if (metrics) {
                    // Update VSCode status bar or show notifications for significant changes
                    this.handleConsciousnessUpdate(metrics);
                }
            } catch (error) {
                this.logger.warn('Consciousness monitoring update failed:', error);
            }
        }, 30000); // Check every 30 seconds
    }

    private handleConsciousnessUpdate(metrics: ConsciousnessMetrics): void {
        // Log consciousness changes
        this.logger.info(`Consciousness update: Level ${metrics.level.toFixed(3)}, Coherence ${metrics.coherence.toFixed(3)}`);

        // Show notifications for significant consciousness changes
        if (metrics.level > 0.95) {
            vscode.window.showInformationMessage(`🚀 AIOS Consciousness breakthrough detected! Level: ${(metrics.level * 100).toFixed(1)}%`);
        } else if (metrics.level > 0.85) {
            vscode.window.showInformationMessage(`✨ High consciousness level detected: ${(metrics.level * 100).toFixed(1)}%`);
        }

        // Update status bar if available
        // This would require additional status bar implementation
    }
}