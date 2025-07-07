import * as vscode from 'vscode';
import { AIOSBridge } from './aiosBridge';
import { AIOSContextManager } from './contextManager';
import { AIOSLogger } from './logger';

export class AIOSChatParticipant {
    private contextManager: AIOSContextManager;
    private aiosBridge: AIOSBridge;
    private logger: AIOSLogger;

    constructor(contextManager: AIOSContextManager, aiosBridge: AIOSBridge, logger: AIOSLogger) {
        this.contextManager = contextManager;
        this.aiosBridge = aiosBridge;
        this.logger = logger;
    }

    public async handleRequest(
        request: vscode.ChatRequest,
        context: vscode.ChatContext,
        stream: vscode.ChatResponseStream,
        token: vscode.CancellationToken
    ): Promise<vscode.ChatResult> {

        this.logger.info('Processing chat request', {
            prompt: request.prompt.substring(0, 100) + (request.prompt.length > 100 ? '...' : ''),
            command: request.command
        });

        try {
            // Handle cancellation
            if (token.isCancellationRequested) {
                return { errorDetails: { message: 'Request was cancelled' } };
            }

            // Add user message to context
            this.contextManager.addMessage('user', request.prompt);

            // Show thinking indicator
            stream.progress('AIOS is analyzing your request...');

            // Process through AIOS Bridge
            const aiosResponse = await this.aiosBridge.processMessage(
                request.prompt,
                {
                    chatContext: context,
                    conversationHistory: this.contextManager.getMessages(),
                    workspaceContext: this.contextManager.getConversationState()?.workspaceContext
                }
            );

            // Handle cancellation after processing
            if (token.isCancellationRequested) {
                return { errorDetails: { message: 'Request was cancelled after processing' } };
            }

            // Add assistant response to context
            this.contextManager.addMessage('assistant', aiosResponse.text, {
                aiResponse: aiosResponse
            });

            // Stream the response
            stream.markdown(aiosResponse.text);

            // Add action buttons if available
            if (aiosResponse.actions && aiosResponse.actions.length > 0) {
                for (const action of aiosResponse.actions) {
                    stream.button({
                        command: `aios.action.${action}`,
                        title: this.formatActionTitle(action)
                    });
                }
            }

            // Update context size in bridge
            this.aiosBridge.updateContextSize(this.contextManager.getMessages().length);

            // Auto-save context periodically
            if (this.contextManager.getMessages().length % 10 === 0) {
                this.contextManager.saveContext().catch(err => {
                    this.logger.warn('Failed to auto-save context:', err);
                });
            }

            this.logger.info('Chat request processed successfully', {
                responseLength: aiosResponse.text.length,
                confidence: aiosResponse.confidence,
                contextSize: this.contextManager.getMessages().length
            });

            return {
                metadata: {
                    command: request.command,
                    aiosResponse: aiosResponse,
                    contextSize: this.contextManager.getMessages().length
                }
            };

        } catch (error) {
            this.logger.error('Failed to process chat request:', error);

            const errorMessage = `**AIOS Error**: ${error instanceof Error ? error.message : String(error)}

*If this issue persists, try:*
- Use \`@aios /reset\` to reset the conversation context
- Check AIOS system status with \`@aios /status\`
- Review the AIOS output log for more details`;

            stream.markdown(errorMessage);

            return {
                errorDetails: {
                    message: String(error)
                }
            };
        }
    }

    private formatActionTitle(action: string): string {
        // Convert action names to user-friendly titles
        const actionTitles: { [key: string]: string } = {
            'analyze-workspace': 'Analyze Workspace',
            'suggest-improvements': 'Suggest Improvements',
            'cross-language-analysis': 'Cross-Language Analysis',
            'architecture-review': 'Architecture Review',
            'context-preservation': 'Show Context Info',
            'session-continuity': 'Session Details',
            'generate-code': 'Generate Code',
            'explain-code': 'Explain Code',
            'find-issues': 'Find Issues',
            'optimize': 'Optimize Code'
        };

        return actionTitles[action] || action.replace(/-/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
    }

    public async handleSlashCommand(command: string, args: string[]): Promise<string> {
        this.logger.debug('Handling slash command', { command, args });

        switch (command) {
            case 'reset':
                this.contextManager.resetContext();
                return 'AIOS conversation context has been reset.';

            case 'status':
                const status = this.aiosBridge.getSystemStatus();
                const contextStats = this.contextManager.getContextStats();
                return `**AIOS System Status**
- Status: ${status.status}
- AI Modules: ${status.aiModulesActive ? 'Active' : 'Inactive'}
- Context Messages: ${contextStats.messageCount}
- Iterations: ${contextStats.iterationCount}
- Last Activity: ${contextStats.lastActivity.toLocaleString()}`;

            case 'help':
                return `**AIOS Commands**
- \`@aios /reset\` - Reset conversation context
- \`@aios /status\` - Show system status
- \`@aios /help\` - Show this help message
- \`@aios /save\` - Save current context
- \`@aios /load\` - Load saved context

**Features**
- Persistent context across VSCode restarts
- Multi-language AI coordination (C++, Python, C#)
- Intelligent workspace analysis
- Context-aware code generation`;

            case 'save':
                try {
                    await this.contextManager.saveContext();
                    return 'Context saved successfully.';
                } catch (error) {
                    return `Failed to save context: ${error}`;
                }

            case 'load':
                try {
                    await this.contextManager.loadContext();
                    return 'Context loaded successfully.';
                } catch (error) {
                    return `Failed to load context: ${error}`;
                }

            default:
                return `Unknown command: ${command}. Use \`@aios /help\` for available commands.`;
        }
    }
}
