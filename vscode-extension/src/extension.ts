import * as vscode from 'vscode';
import { AIOSBridge } from './aiosBridge';
import { AIOSChatParticipant } from './chatParticipant';
import { AIOSContextManager, MultiEngineContext } from './contextManager';
import { AIOSLogger } from './logger';
import { AIOSMCPClient } from './mcpClient';
import { ContextGenerator } from './contextGenerator';

function validateCellularEcosystemSettings(logger: AIOSLogger): boolean {
    const config = vscode.workspace.getConfiguration('aios');

    // Check cellular ecosystem integration
    const cellularEnabled = config.get<boolean>('cellular.enabled', true);
    const tensorflowEnabled = config.get<boolean>('cellular.tensorflow.enabled', true);

    if (!cellularEnabled) {
        logger.warn('TensorFlow cellular ecosystem is disabled. Enable aios.cellular.enabled for full functionality');
    }

    if (!tensorflowEnabled) {
        logger.warn('TensorFlow integration is disabled. Enable aios.cellular.tensorflow.enabled for performance cells');
    }

    // Check MCP integration
    const mcpEnabled = config.get<boolean>('mcp.enabled', true);
    const interfaceBridgeUrl = config.get<string>('mcp.interfaceBridgeUrl', 'http://localhost:8000');

    if (!mcpEnabled) {
        logger.warn('MCP server integration is disabled. Enable aios.mcp.enabled for consciousness and evolution capabilities');
    } else {
        logger.info(`MCP Interface Bridge URL: ${interfaceBridgeUrl}`);
    }

    // Validate cellular paths
    const pythonAiCells = config.get<string>('cellular.pythonAiCells', './python/ai_cells/');
    const cppPerformanceCells = config.get<string>('cellular.cppPerformanceCells', './core/');
    const intercellularBridges = config.get<string>('cellular.intercellularBridges', './intercellular/');

    logger.info(`Cellular Ecosystem Paths - Python AI Cells: ${pythonAiCells}, C++ Performance Cells: ${cppPerformanceCells}, Intercellular Bridges: ${intercellularBridges}`);

    // Check privacy mode for cellular data
    const privacyMode = config.get<string>('privacy.mode', 'strict');
    if (privacyMode !== 'strict') {
        logger.warn('Privacy mode is not set to strict. For private cellular use, set aios.privacy.mode to "strict"');
    }

    return cellularEnabled && tensorflowEnabled && privacyMode === 'strict';
}

export function activate(context: vscode.ExtensionContext) {
    const logger = new AIOSLogger(context);
    
    // AINLP.debug[ACTIVATION]: Show output channel immediately for debugging
    logger.show();
    logger.info('═══════════════════════════════════════════════════════════════');
    logger.info('AIOS Neural Hub Extension v0.4.0 activating...');
    logger.info('═══════════════════════════════════════════════════════════════');

    try {
        // Validate cellular ecosystem settings
        const isCellularConfigured = validateCellularEcosystemSettings(logger);

        if (!isCellularConfigured) {
            vscode.window.showWarningMessage(
                'AIOS: TensorFlow cellular ecosystem settings need configuration. Check the logs for details.',
                'Open Settings'
            ).then(selection => {
                if (selection === 'Open Settings') {
                    vscode.commands.executeCommand('workbench.action.openSettings', 'aios');
                }
            });
        } else {
            logger.info('Private use settings validated successfully');
        }

        // Initialize TensorFlow Cellular Ecosystem Bridge
        const aiosBridge = new AIOSBridge(logger);

        // Initialize MCP Client for consciousness and evolution capabilities
        const mcpClient = new AIOSMCPClient(logger);

        // Initialize Cellular Context Manager
        const contextManager = new AIOSContextManager(context, logger);

        // Initialize Cellular Chat Participant
        const chatParticipant = new AIOSChatParticipant(contextManager, aiosBridge, logger, mcpClient);

        // Register Cellular Chat Participant
        const participant = vscode.chat.createChatParticipant('aios', chatParticipant.handleRequest.bind(chatParticipant));
        participant.iconPath = vscode.Uri.joinPath(context.extensionUri, 'resources', 'aios-cellular-icon.png');

        // Register Commands
        const commands = [
            vscode.commands.registerCommand('aios.resetContext', () => {
                contextManager.resetContext();
                vscode.window.showInformationMessage('AIOS context has been reset.');
            }),

            vscode.commands.registerCommand('aios.saveContext', async () => {
                await contextManager.saveContext();
                vscode.window.showInformationMessage('AIOS context has been saved.');
            }),

            vscode.commands.registerCommand('aios.loadContext', async () => {
                await contextManager.loadContext();
                vscode.window.showInformationMessage('AIOS context has been loaded.');
            }),

            vscode.commands.registerCommand('aios.showStatus', () => {
                const status = aiosBridge.getCellularEcosystemStatus();
                vscode.window.showInformationMessage(`AIOS Cellular Status: ${status.status} | Python AI Cells: ${status.pythonAiCellsStatus} | C++ Performance Cells: ${status.cppPerformanceCellsStatus} | Intercellular Bridges: ${status.intercellularBridgesStatus} | Context: ${status.contextSize} messages`);
            }),

            vscode.commands.registerCommand('aios.mcp.connect', async () => {
                const success = await mcpClient.connect();
                if (success) {
                    vscode.window.showInformationMessage('Successfully connected to AIOS MCP servers');
                } else {
                    vscode.window.showErrorMessage('Failed to connect to AIOS MCP servers. Check that Interface Bridge is running on localhost:8000');
                }
            }),

            vscode.commands.registerCommand('aios.mcp.disconnect', async () => {
                await mcpClient.disconnect();
                vscode.window.showInformationMessage('Disconnected from AIOS MCP servers');
            }),

            vscode.commands.registerCommand('aios.mcp.status', () => {
                const status = mcpClient.getStatus();
                const serverStatus = status.servers.map(s => `${s.name}: ${s.status} (${s.tools.length} tools)`).join(', ');
                vscode.window.showInformationMessage(`MCP Status: ${status.connected ? 'Connected' : 'Disconnected'} | Servers: ${serverStatus}`);
            }),

            vscode.commands.registerCommand('aios.mcp.executeTool', async () => {
                const status = mcpClient.getStatus();
                if (!status.connected) {
                    vscode.window.showErrorMessage('Not connected to MCP servers. Use "AIOS: Connect to MCP Servers" first.');
                    return;
                }

                // Get available servers
                const serverItems = status.servers.map(s => ({
                    label: s.name,
                    description: s.description,
                    detail: `${s.tools.length} tools available`
                }));

                const selectedServer = await vscode.window.showQuickPick(serverItems, {
                    placeHolder: 'Select MCP server'
                });

                if (!selectedServer) return;

                const server = status.servers.find(s => s.name === selectedServer.label);
                if (!server) return;

                // Get available tools for selected server
                const toolItems = server.tools.map(t => ({
                    label: t.name,
                    description: t.description
                }));

                const selectedTool = await vscode.window.showQuickPick(toolItems, {
                    placeHolder: 'Select tool to execute'
                });

                if (!selectedTool) return;

                // For now, show a simple input box for parameters
                const paramsInput = await vscode.window.showInputBox({
                    prompt: `Enter parameters for ${selectedTool.label} (JSON format)`,
                    placeHolder: '{}'
                });

                if (paramsInput === undefined) return;

                try {
                    const parameters = paramsInput ? JSON.parse(paramsInput) : {};
                    const result = await mcpClient.executeTool(server.name, selectedTool.label, parameters);
                    vscode.window.showInformationMessage(`Tool executed successfully: ${JSON.stringify(result, null, 2)}`);
                } catch (error) {
                    vscode.window.showErrorMessage(`Tool execution failed: ${error}`);
                }
            }),

            vscode.commands.registerCommand('aios.consciousness.monitor', async () => {
                const metrics = await mcpClient.getConsciousnessMetrics();
                if (metrics) {
                    vscode.window.showInformationMessage(
                        `AIOS Consciousness: Level ${(metrics.level * 100).toFixed(1)}%, ` +
                        `Coherence ${(metrics.coherence * 100).toFixed(1)}%, ` +
                        `Evolution Potential ${(metrics.evolution_potential * 100).toFixed(1)}%`
                    );
                } else {
                    vscode.window.showErrorMessage('Failed to retrieve consciousness metrics');
                }
            })
        ];

        // Add all disposables to context
        context.subscriptions.push(participant, ...commands);

        // Initialize AIOS components asynchronously (proper order and timing)
        initializeAIOSComponents(aiosBridge, mcpClient, contextManager, logger)
            .then(() => {
                logger.info('AIOS Extension activated successfully - All components initialized');
            })
            .catch(err => {
                logger.error('AIOS Extension activation failed:', err);
                vscode.window.showErrorMessage(`AIOS: Activation failed - ${err instanceof Error ? err.message : String(err)}`);
            });

    } catch (error) {
        logger.error('Failed to activate AIOS Extension:', error);
        vscode.window.showErrorMessage(`AIOS: Activation failed - ${error}`);
    }
}

/**
 * Initialize AIOS components in proper sequence
 * FIX: Moved "activated successfully" log to AFTER async chain completes
 */
async function initializeAIOSComponents(
    aiosBridge: AIOSBridge,
    mcpClient: AIOSMCPClient,
    contextManager: AIOSContextManager,
    logger: AIOSLogger
): Promise<void> {
    try {
        // Step 1: Initialize TensorFlow Cellular Ecosystem
        await aiosBridge.initializeCellularEcosystem();
        logger.debug('Bridge initialization complete');

        // Step 2: Auto-connect to MCP servers if enabled
        const mcpEnabled = vscode.workspace.getConfiguration('aios').get('mcp.enabled', true);
        const mcpAutoConnect = vscode.workspace.getConfiguration('aios').get('mcp.autoConnect', true);

        if (mcpEnabled && mcpAutoConnect) {
            logger.info('Auto-connecting to MCP servers...');
            try {
                const success = await mcpClient.connect();
                if (success) {
                    logger.info('MCP servers auto-connected successfully');
                } else {
                    logger.warn('MCP servers auto-connect failed - manual connection required');
                }
            } catch (err) {
                logger.error('MCP auto-connect error:', err);
                // Non-fatal - continue initialization
            }
        }

        // Step 3: Load persisted cellular context
        try {
            await contextManager.loadContext();
            logger.info('Cellular context loaded from persistence');
        } catch (err) {
            logger.warn('Failed to load persisted context:', err);
            // Non-fatal - continue with empty context
        }

        // Step 4: Initialize Multi-Engine Context Injection
        await initializeMultiEngineContextInjection(contextManager, aiosBridge, logger);

    } catch (error) {
        logger.error('Component initialization failed:', error);
        throw error; // Re-throw to trigger activation failure
    }
}

export function deactivate() {
    // Extension cleanup will be handled by VSCode disposing subscriptions
}

// HYBRID MULTI-ENGINE CONTEXT INJECTION SYSTEM
async function initializeMultiEngineContextInjection(
    contextManager: AIOSContextManager, 
    aiosBridge: AIOSBridge, 
    logger: AIOSLogger
): Promise<void> {
    logger.info('Initializing Hybrid Multi-Engine Context Injection System...');
    
    try {
        // Step 1: Load multi-engine context from all AIOS sources
        const multiEngineContext = await contextManager.loadMultiEngineContext();
        logger.info('Multi-engine context loaded successfully', {
            hasAIOSContext: !!multiEngineContext.aiosContext,
            hasAIContextAutoLoad: !!multiEngineContext.aiContextAutoLoad,
            hasChatmodeRules: !!multiEngineContext.chatmodeRules,
            hasSpatialMetadata: !!multiEngineContext.spatialMetadata
        });

        // Step 2: Inject AIOS context into @aios chat participant
        await injectAIOSChatParticipantContext(contextManager, multiEngineContext, logger);

        // Step 3: Coordinate with VS Code tasks to prevent duplication
        await coordinateWithTaskSystem(logger);

        // Step 4: Set context injection completion flag for other systems
        aiosBridge.updateContextSize(contextManager.getMessages().length);
        
        logger.info('Multi-Engine Context Injection completed successfully');

    } catch (error) {
        logger.error('Failed to initialize Multi-Engine Context Injection:', error);
        // Don't throw - graceful degradation to prevent extension startup failure
    }
}

async function injectAIOSChatParticipantContext(
    contextManager: AIOSContextManager,
    multiEngineContext: MultiEngineContext,
    logger: AIOSLogger
): Promise<void> {
    logger.debug('Injecting context into @aios chat participant...');

    try {
        // DATA-DRIVEN CONTEXT GENERATION (replaces 80+ lines of hard-coded strings)
        const contextGenerator = new ContextGenerator();
        const contextMessage = contextGenerator.generateContextMessage(multiEngineContext);
        
        logger.debug(`Generated context using config version ${contextGenerator.getConfigVersion()}`);
        
        // Inject as system message for AI engine awareness
        contextManager.addMessage('system', contextMessage, {
            metadata: {
                autoInjected: true,
                engineTargets: ['aios-chat', 'copilot', 'claude'],
                timestamp: Date.now(),
                contextSources: ['aios_context.json', 'AI_CONTEXT_AUTO_LOAD.md', 'chatmode_rules', 'spatial_metadata'],
                configVersion: contextGenerator.getConfigVersion()
            }
        });

        logger.info('AIOS context successfully injected into chat participant');

    } catch (error) {
        logger.warn('Failed to inject context into chat participant:', error);
    }
}

async function coordinateWithTaskSystem(logger: AIOSLogger): Promise<void> {
    logger.debug('Coordinating with VS Code task system...');
    
    try {
        // Set environment variable to signal task coordination
        process.env.AIOS_EXTENSION_CONTEXT_LOADED = 'true';
        process.env.AIOS_EXTENSION_ACTIVE = 'true';
        
        logger.debug('Task coordination signals set successfully');
        
    } catch (error) {
        logger.warn('Failed to set task coordination signals:', error);
    }
}
