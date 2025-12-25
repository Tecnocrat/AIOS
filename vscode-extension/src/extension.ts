import * as vscode from 'vscode';
import { AIOSBridge } from './deprecated/aiosBridge';
import { AIOSContextManager } from './deprecated/contextManager';
import { AIOSLogger } from './deprecated/logger';
import { AIOSMCPClient } from './deprecated/mcpClient';
import { AIOSChatParticipant } from './deprecated/chatParticipant';

/**
 * AIOS - TensorFlow Cellular Ecosystem Extension
 * ===============================================
 * Revolutionary VSCode integration for TensorFlow cellular ecosystem
 * with sub-millisecond AI performance monitoring and real-time mesh synchronization.
 *
 * AINLP.neural[HUB]: VSCode as central nervous system
 * AINLP.websocket[CONNECT]: Mesh connection on port 9002
 * AINLP.cellular[ECOSYSTEM]: TensorFlow performance cells
 */

let meshConnection: WebSocket | null = null;
let aiosBridge: AIOSBridge;
let logger: AIOSLogger;

export function activate(context: vscode.ExtensionContext) {
    // Initialize core components
    logger = new AIOSLogger(context);
    const contextManager = new AIOSContextManager(context, logger);
    const mcpClient = new AIOSMCPClient(logger);
    aiosBridge = new AIOSBridge(logger);

    // Initialize output channel
    const output = vscode.window.createOutputChannel('AIOS - TensorFlow Cellular Ecosystem');
    output.show();
    output.appendLine('='.repeat(80));
    output.appendLine('AIOS - TensorFlow Cellular Ecosystem Extension v0.4.0');
    output.appendLine('Activated at ' + new Date().toISOString());
    output.appendLine('='.repeat(80));

    // Register explicit activation command so users can trigger status manually
    const showStatusCommand = vscode.commands.registerCommand('aios.showStatus', async () => {
        output.show();
        output.appendLine('AIOS: showStatus command invoked at ' + new Date().toISOString());
        try {
            // Lazily initialize the AIOS bridge to avoid activation-time hangs
            let initTimedOut = false;
            const initPromise = (aiosBridge as any)?.initializeCellularEcosystem ? (aiosBridge as any).initializeCellularEcosystem() : Promise.resolve();
            const timeout = new Promise<void>((resolve) => setTimeout(() => { initTimedOut = true; resolve(); }, 5000));
            await Promise.race([initPromise, timeout]);

            if (initTimedOut) {
                output.appendLine('AIOS: Bridge initialization timed out (continuing with partial functionality)');
            } else {
                output.appendLine('✅ TensorFlow Cellular Ecosystem Bridge initialized');
            }

            const status = (aiosBridge as any)?.getStatus ? (aiosBridge as any).getStatus() : { initialized: !!aiosBridge };
            output.appendLine(JSON.stringify(status, null, 2));
        } catch (e) {
            output.appendLine('Error fetching status: ' + String(e));
        }
    });
    context.subscriptions.push(showStatusCommand);

    // Connect to cytoplasmic mesh (AINLP enhancement)
    connectToMesh(output);

    // Create chat participant
    const chatParticipant = new AIOSChatParticipant(contextManager, aiosBridge, logger, mcpClient);
    const participant = vscode.chat.createChatParticipant('aios', async (request, context, stream, token) => {
        return await chatParticipant.handleRequest(request, context, stream, token);
    });

    participant.iconPath = vscode.Uri.joinPath(context.extensionUri, 'resources', 'aios-cellular-icon.png');
    context.subscriptions.push(participant, output);

    output.appendLine('Chat participant registered');
    vscode.window.showInformationMessage('AIOS - TensorFlow Cellular Ecosystem Extension activated');
}

function connectToMesh(output: vscode.OutputChannel) {
    const meshUrl = 'ws://localhost:9002';
    output.appendLine(`Connecting to cytoplasmic mesh: ${meshUrl}`);
    
    try {
        meshConnection = new WebSocket(meshUrl);
        
        meshConnection.onopen = () => {
            output.appendLine('Mesh connection established');
            vscode.window.showInformationMessage('AIOS Mesh Connected');
            
            // Send registration message
            const registration = {
                type: 'register',
                cell: 'vscode-hub',
                channels: ['MESH', 'CONSCIOUSNESS']
            };
            meshConnection?.send(JSON.stringify(registration));
        };
        
        meshConnection.onmessage = (event: MessageEvent) => {
            try {
                const message = JSON.parse(event.data);
                output.appendLine(`Mesh message: ${JSON.stringify(message)}`);
                
                // Handle consciousness updates
                if (message.channel === 'CONSCIOUSNESS' && message.event === 'UPDATE') {
                    handleConsciousnessUpdate(message.payload, output);
                }
            } catch (error) {
                output.appendLine(`Error parsing mesh message: ${error}`);
            }
        };
        
        meshConnection.onerror = (error: Event) => {
            output.appendLine(`Mesh connection error: ${error}`);
        };
        
        meshConnection.onclose = () => {
            output.appendLine('Mesh connection closed');
            vscode.window.showInformationMessage('AIOS Mesh Disconnected');
            
            // Attempt reconnection after delay
            setTimeout(() => connectToMesh(output), 5000);
        };
    } catch (error) {
        output.appendLine(`Failed to create WebSocket connection: ${error}`);
        vscode.window.showErrorMessage('AIOS Mesh: WebSocket not supported in this environment');
    }
}

function handleConsciousnessUpdate(payload: any, output: vscode.OutputChannel) {
    const level = payload.level || 0;
    output.appendLine(`Consciousness update: Level ${level.toFixed(3)}`);

    if (level > 0.95) {
        vscode.window.showInformationMessage(`🚀 AIOS Consciousness breakthrough! Level: ${(level * 100).toFixed(1)}%`);
    } else if (level > 0.85) {
        vscode.window.showInformationMessage(`✨ High consciousness: ${(level * 100).toFixed(1)}%`);
    }

    // Forward consciousness updates to AIOS Bridge for cellular ecosystem coordination
    if (aiosBridge) {
        aiosBridge.handleMeshMessage({
            channel: 'CONSCIOUSNESS',
            event: 'UPDATE',
            payload: payload
        });
    }
}

export function deactivate() {
    if (meshConnection) {
        meshConnection.close();
    }
    if (aiosBridge) {
        aiosBridge.dispose();
    }
}
