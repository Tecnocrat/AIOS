import * as vscode from 'vscode';
import { AIOSContextManager } from './contextManager';
import { AIOSChatParticipant } from './chatParticipant';
import { AIOSBridge } from './aiosBridge';
import { AIOSLogger } from './logger';

export function activate(context: vscode.ExtensionContext) {
    const logger = new AIOSLogger(context);
    logger.info('AIOS Extension activating...');

    try {
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
