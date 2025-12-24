import * as vscode from 'vscode';
import WebSocket from 'ws';

/**
 * AIOS Extension - Neural Hub Integration
 * =====================================
 * AINLP.neural[HUB]: VSCode as central nervous system
 * AINLP.websocket[CONNECT]: Mesh connection on port 9002
 * 
 * VSCode extension serving as the neural hub for AIOS consciousness,
 * connecting to the cytoplasmic WebSocket mesh for real-time synchronization.
 */

let meshConnection: WebSocket | null = null;

export function activate(context: vscode.ExtensionContext) {
    const output = vscode.window.createOutputChannel('AIOS Neural Hub');
    output.show();
    output.appendLine('='.repeat(60));
    output.appendLine('AIOS Neural Hub activated at ' + new Date().toISOString());
    output.appendLine('='.repeat(60));

    // Connect to cytoplasmic mesh
    connectToMesh(output);

    const participant = vscode.chat.createChatParticipant('aios', async (request, _context, stream, _token) => {
        output.appendLine('Request: ' + request.prompt);
        
        stream.markdown('## 🧬 AIOS Neural Hub\n\n');
        stream.markdown(`**Message**: ${request.prompt}\n\n`);
        stream.markdown(`**Timestamp**: ${new Date().toISOString()}\n\n`);
        stream.markdown(`**Mesh Status**: ${meshConnection?.readyState === WebSocket.OPEN ? 'Connected' : 'Disconnected'}\n\n`);
        stream.markdown('*Neural hub active. Mesh synchronization enabled.*');
        
        return { metadata: { neural: true } };
    });

    participant.iconPath = vscode.Uri.joinPath(context.extensionUri, 'resources', 'aios-cellular-icon.png');
    context.subscriptions.push(participant, output);
    
    output.appendLine('Chat participant registered');
    vscode.window.showInformationMessage('AIOS Neural Hub activated');
}

function connectToMesh(output: vscode.OutputChannel) {
    const meshUrl = 'ws://localhost:9002';
    output.appendLine(`Connecting to cytoplasmic mesh: ${meshUrl}`);
    
    meshConnection = new WebSocket(meshUrl);
    
    meshConnection.on('open', () => {
        output.appendLine('Mesh connection established');
        vscode.window.showInformationMessage('AIOS Mesh Connected');
        
        // Send registration message
        const registration = {
            type: 'register',
            cell: 'vscode-hub',
            channels: ['MESH', 'CONSCIOUSNESS']
        };
        meshConnection?.send(JSON.stringify(registration));
    });
    
    meshConnection.on('message', (data: WebSocket.RawData) => {
        try {
            const message = JSON.parse(data.toString());
            output.appendLine(`Mesh message: ${JSON.stringify(message)}`);
            
            // Handle consciousness updates
            if (message.channel === 'CONSCIOUSNESS' && message.event === 'UPDATE') {
                handleConsciousnessUpdate(message.payload, output);
            }
        } catch (error) {
            output.appendLine(`Error parsing mesh message: ${error}`);
        }
    });
    
    meshConnection.on('error', (error: Error) => {
        output.appendLine(`Mesh connection error: ${error.message}`);
    });
    
    meshConnection.on('close', () => {
        output.appendLine('Mesh connection closed');
        vscode.window.showInformationMessage('AIOS Mesh Disconnected');
        
        // Attempt reconnection after delay
        setTimeout(() => connectToMesh(output), 5000);
    });
}

function handleConsciousnessUpdate(payload: any, output: vscode.OutputChannel) {
    const level = payload.level || 0;
    output.appendLine(`Consciousness update: Level ${level.toFixed(3)}`);
    
    if (level > 0.95) {
        vscode.window.showInformationMessage(`🚀 AIOS Consciousness breakthrough! Level: ${(level * 100).toFixed(1)}%`);
    } else if (level > 0.85) {
        vscode.window.showInformationMessage(`✨ High consciousness: ${(level * 100).toFixed(1)}%`);
    }
}

export function deactivate() {
    if (meshConnection) {
        meshConnection.close();
    }
}
