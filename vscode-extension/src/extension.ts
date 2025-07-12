import * as vscode from 'vscode';
import { AIOSBridge } from './aiosBridge';
import { AIOSChatParticipant } from './chatParticipant';
import { AIOSContextManager } from './contextManager';
import { AIOSLogger } from './logger';

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
    logger.info('AIOS TensorFlow Cellular Ecosystem Extension activating...');

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

        // Initialize Cellular Context Manager
        const contextManager = new AIOSContextManager(context, logger);

        // Initialize Cellular Chat Participant
        const chatParticipant = new AIOSChatParticipant(contextManager, aiosBridge, logger);

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
            })
        ];

        // Add all disposables to context
        context.subscriptions.push(participant, ...commands);

        // Initialize TensorFlow Cellular Ecosystem connection
        aiosBridge.initializeCellularEcosystem().then(() => {
            logger.info('TensorFlow Cellular Ecosystem Bridge initialized successfully');

            // Load persisted cellular context if available
            contextManager.loadContext().then(() => {
                logger.info('Cellular context loaded from persistence');
            }).catch(err => {
                logger.warn('Failed to load persisted context:', err);
            });

        }).catch(err => {
            logger.error('Failed to initialize AIOS Bridge:', err);
            vscode.window.showErrorMessage('AIOS: Failed to connect to AI modules. Some features may be limited.');
        });

        logger.info('AIOS Extension activated successfully');

    } catch (error) {
        logger.error('Failed to activate AIOS Extension:', error);
        vscode.window.showErrorMessage(`AIOS: Activation failed - ${error}`);
    }
}

export function deactivate() {
    // Extension cleanup will be handled by VSCode disposing subscriptions
}
