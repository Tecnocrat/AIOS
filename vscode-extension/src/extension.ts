import * as vscode from 'vscode';
import { AIOSBridge } from './aiosBridge';
import { AIOSChatParticipant } from './chatParticipant';
import { AIOSContextManager } from './contextManager';
import { AIOSLogger } from './logger';

function validatePrivateUseSettings(logger: AIOSLogger): boolean {
    const config = vscode.workspace.getConfiguration('aios');

    // Check privacy mode
    const privacyMode = config.get<string>('privacy.mode', 'strict');
    if (privacyMode !== 'strict') {
        logger.warn('Privacy mode is not set to strict. For private use, set aios.privacy.mode to "strict"');
    }

    // Check network setting
    const networkEnabled = config.get<boolean>('network.enabled', false);
    if (networkEnabled) {
        logger.warn('Network connections are enabled. For private use, set aios.network.enabled to false');
    }

    // Check telemetry setting
    const telemetryEnabled = config.get<boolean>('telemetry.enabled', false);
    if (telemetryEnabled) {
        logger.warn('Telemetry is enabled. For private use, set aios.telemetry.enabled to false');
    }

    // Check auto-update setting
    const autoUpdateEnabled = config.get<boolean>('autoUpdate.enabled', false);
    if (autoUpdateEnabled) {
        logger.warn('Auto-update is enabled. For private use, set aios.autoUpdate.enabled to false');
    }

    return privacyMode === 'strict' && !networkEnabled && !telemetryEnabled && !autoUpdateEnabled;
}

export function activate(context: vscode.ExtensionContext) {
    const logger = new AIOSLogger(context);
    logger.info('AIOS Extension activating...');

    try {
        // Validate private use settings
        const isPrivatelyConfigured = validatePrivateUseSettings(logger);

        if (!isPrivatelyConfigured) {
            vscode.window.showWarningMessage(
                'AIOS: Some settings are not configured for private use. Check the logs for details.',
                'Open Settings'
            ).then(selection => {
                if (selection === 'Open Settings') {
                    vscode.commands.executeCommand('workbench.action.openSettings', 'aios');
                }
            });
        } else {
            logger.info('Private use settings validated successfully');
        }

        // Initialize AIOS Bridge
        const aiosBridge = new AIOSBridge(logger);

        // Initialize Context Manager
        const contextManager = new AIOSContextManager(context, logger);

        // Initialize Chat Participant
        const chatParticipant = new AIOSChatParticipant(contextManager, aiosBridge, logger);

        // Register Chat Participant
        const participant = vscode.chat.createChatParticipant('aios', chatParticipant.handleRequest.bind(chatParticipant));
        participant.iconPath = vscode.Uri.joinPath(context.extensionUri, 'resources', 'aios-icon.png');

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
                const status = aiosBridge.getSystemStatus();
                vscode.window.showInformationMessage(`AIOS Status: ${status.status} | AI Modules: ${status.aiModulesActive} | Context: ${status.contextSize} messages`);
            })
        ];

        // Add all disposables to context
        context.subscriptions.push(participant, ...commands);

        // Initialize AIOS connection
        aiosBridge.initialize().then(() => {
            logger.info('AIOS Bridge initialized successfully');

            // Load persisted context if available
            contextManager.loadContext().then(() => {
                logger.info('Context loaded from persistence');
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
