import * as vscode from 'vscode';

/**
 * AIOS Extension - Minimal Working Core
 * =====================================
 * AINLP.context[DEPRECATED]: Full integration deprecated 2025-12-17
 * 
 * This is the minimal proven-working chat participant.
 * Complex integrations (AIOSBridge, MCPClient, ContextManager) 
 * are preserved in ./deprecated/ but not loaded.
 */

export function activate(context: vscode.ExtensionContext) {
    const output = vscode.window.createOutputChannel('AIOS');
    output.show();
    output.appendLine('='.repeat(60));
    output.appendLine('AIOS Extension activated at ' + new Date().toISOString());
    output.appendLine('='.repeat(60));

    const participant = vscode.chat.createChatParticipant('aios', async (request, _context, stream, _token) => {
        output.appendLine('Request: ' + request.prompt);
        
        stream.markdown('## 🧬 AIOS Neural Hub\n\n');
        stream.markdown(`**Message**: ${request.prompt}\n\n`);
        stream.markdown(`**Timestamp**: ${new Date().toISOString()}\n\n`);
        stream.markdown('*Minimal core active. Full integration deprecated.*');
        
        return { metadata: { minimal: true } };
    });

    participant.iconPath = vscode.Uri.joinPath(context.extensionUri, 'resources', 'aios-cellular-icon.png');
    context.subscriptions.push(participant, output);
    
    output.appendLine('Chat participant registered');
    vscode.window.showInformationMessage('AIOS Extension activated');
}

export function deactivate() {}
