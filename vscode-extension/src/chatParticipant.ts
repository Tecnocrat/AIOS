import * as vscode from 'vscode';
import { AIOSBridge } from './aiosBridge';
import { AIOSContextManager } from './contextManager';
import { AIOSLogger } from './logger';
import { AIOSMCPClient } from './mcpClient';
import { AIOSSecurityModule } from './securityModule';

export class AIOSChatParticipant {
    private contextManager: AIOSContextManager;
    private aiosBridge: AIOSBridge;
    private logger: AIOSLogger;
    private mcpClient: AIOSMCPClient;
    private securityModule: AIOSSecurityModule;

    constructor(contextManager: AIOSContextManager, aiosBridge: AIOSBridge, logger: AIOSLogger, mcpClient: AIOSMCPClient) {
        this.contextManager = contextManager;
        this.aiosBridge = aiosBridge;
        this.logger = logger;
        this.mcpClient = mcpClient;
        this.securityModule = new AIOSSecurityModule(logger);
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

            // Check for MCP commands
            const mcpCommands = await this.handleMCPCommands(request.prompt, stream);
            if (mcpCommands) {
                return mcpCommands;
            }

            // 🔒 SECURITY FIRST: Check for secret operations and handle securely
            const secureResponse = await this.securityModule.processSecureMessage(request.prompt);
            if (secureResponse) {
                stream.markdown(secureResponse);
                this.logger.info('Secure operation handled via terminal', {
                    prompt: request.prompt.substring(0, 50) + '...'
                });
                return { metadata: { secureOperation: true } };
            }

            // Process through AIOS Bridge
            const aiosResponse = await this.aiosBridge.processMessage(
                request.prompt,
                {
                    chatContext: context,
                    conversationHistory: this.contextManager.getMessages(),
                    workspaceContext: this.contextManager.getConversationState()?.workspaceContext
                }
            );

            // 🔒 SECURITY: Validate and sanitize AIOS response before display
            const validation = this.securityModule.validateResponse(aiosResponse.text);
            if (!validation.isValid) {
                this.logger.warn('AIOS response contained potential secrets, sanitizing', {
                    violations: validation.violations.length
                });
                aiosResponse.text = validation.sanitizedResponse;
                stream.markdown('⚠️ **Response Sanitized**: Potential sensitive content was detected and removed.\n\n');
            }

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
            // Legacy actions
            'analyze-workspace': 'Analyze Workspace',
            'suggest-improvements': 'Suggest Improvements',
            'cross-language-analysis': 'Cross-Language Analysis',
            'architecture-review': 'Architecture Review',
            'context-preservation': 'Show Context Info',
            'session-continuity': 'Session Details',
            'generate-code': 'Generate Code',
            'explain-code': 'Explain Code',
            'find-issues': 'Find Issues',
            'optimize': 'Optimize Code',
            
            // Enhanced intelligent actions
            'run-system-health': '🔍 Run System Health Check',
            'run-tests': '🧪 Execute Test Suite',
            'build-project': '🔨 Build Project',
            'analyze-architecture': '🏗️ Analyze Architecture',
            'check-dependencies': '📦 Check Dependencies',
            'review-code-quality': '📊 Review Code Quality',
            'provide-guidance': '📚 Provide Guidance',
            'show-examples': '💡 Show Examples',
            'explain-architecture': '🏛️ Explain Architecture',
            'create-python-module': '🐍 Create Python Module',
            'create-cpp-component': '⚡ Create C++ Component',
            'create-csharp-class': '🔷 Create C# Class',
            'general-assistance': '🤝 General Assistance',
            'workspace-overview': '📋 Workspace Overview',
            'development-guide': '📖 Development Guide',
            'basic-assistance': '⚙️ Basic Assistance'
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
- \`@aios /security\` - Show security status and operations
- \`@aios /security-test\` - Test security sanitization
- \`@aios /help\` - Show this help message
- \`@aios /save\` - Save current context
- \`@aios /load\` - Load saved context

**Features**
- Persistent context across VSCode restarts
- Multi-language AI coordination (C++, Python, C#)
- Intelligent workspace analysis
- Context-aware code generation
- 🔒 **Mandatory Security**: Secrets never shown in chat`;

            case 'save':
                try {
                    await this.contextManager.saveContext();
                    return 'Context saved successfully.';
                } catch (error) {
                    return `Failed to save context: ${error}`;
                }

            case 'security':
                return `**🔒 AIOS Security Status**
- Security Module: Active
- Secret Detection: Enabled
- Terminal Operations: Ephemeral CLI
- Response Sanitization: Automatic
- Audit Logging: Enabled

**Security Operations Available:**
• \`vault init\` - Initialize HashiCorp Vault securely
• \`vault unseal\` - Unseal vault with stored keys
• \`vault status\` - Check vault health
• \`set [service] key\` - Configure API keys (OpenAI, Anthropic, etc.)
• \`validate [service] key\` - Check key configuration

*All operations use secure terminal CLI. Secrets are never displayed in chat.*`;

            case 'security-test':
                // Test security patterns
                const testResponse = `Test response with potential secrets:
- API Key: sk-test12345678901234567890123456789012
- Vault Token: hvs.CAES1234567890abcdef
- Password: mySecretPass123

This should be automatically sanitized.`;
                const sanitized = this.securityModule.sanitizeResponse(testResponse);
                return `**Security Test Results:**
Original length: ${testResponse.length}
Sanitized length: ${sanitized.length}
Sanitization applied: ${testResponse !== sanitized}

Sanitized output:
${sanitized}`;

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

    private async handleMCPCommands(prompt: string, stream: vscode.ChatResponseStream): Promise<vscode.ChatResult | null> {
        const lowerPrompt = prompt.toLowerCase().trim();

        // MCP Status command
        if (lowerPrompt === '/mcp-status' || lowerPrompt === 'mcp status') {
            const status = this.mcpClient.getStatus();
            const serverStatus = status.servers.map(s =>
                `• ${s.name}: ${s.status} (${s.tools.length} tools)`
            ).join('\n');

            stream.markdown(`**AIOS MCP Server Status**\n\n**Connection**: ${status.connected ? '✅ Connected' : '❌ Disconnected'}\n\n**Servers**:\n${serverStatus}`);
            return { metadata: { command: 'mcp-status' } };
        }

        // Consciousness monitoring command
        if (lowerPrompt === '/consciousness' || lowerPrompt === 'consciousness monitor') {
            stream.progress('Retrieving consciousness metrics...');
            const metrics = await this.mcpClient.getConsciousnessMetrics();

            if (metrics) {
                stream.markdown(`**AIOS Consciousness Metrics**\n\n• **Level**: ${(metrics.level * 100).toFixed(1)}%\n• **Coherence**: ${(metrics.coherence * 100).toFixed(1)}%\n• **Evolution Potential**: ${(metrics.evolution_potential * 100).toFixed(1)}%\n• **Timestamp**: ${metrics.timestamp}`);
            } else {
                stream.markdown('❌ Failed to retrieve consciousness metrics. Ensure MCP servers are connected.');
            }
            return { metadata: { command: 'consciousness-monitor' } };
        }

        // Emergence detection command
        if (lowerPrompt.startsWith('/detect-emergence') || lowerPrompt.startsWith('detect emergence')) {
            const activeEditor = vscode.window.activeTextEditor;
            if (!activeEditor) {
                stream.markdown('❌ No active editor found. Please open a file to analyze.');
                return { metadata: { command: 'detect-emergence' } };
            }

            stream.progress('Analyzing code for emergence patterns...');
            const code = activeEditor.document.getText();
            const filePath = activeEditor.document.uri.fsPath;

            try {
                const result = await this.mcpClient.detectEmergencePatterns(code, filePath);
                stream.markdown(`**Emergence Pattern Analysis**\n\n${JSON.stringify(result, null, 2)}`);
            } catch (error) {
                stream.markdown(`❌ Emergence detection failed: ${error}`);
            }
            return { metadata: { command: 'detect-emergence' } };
        }

        // Evolution experiment command
        if (lowerPrompt.startsWith('/create-experiment') || lowerPrompt.startsWith('create evolution experiment')) {
            const config = { type: 'consciousness_evolution', auto_start: true };
            stream.progress('Creating evolution experiment...');

            try {
                const result = await this.mcpClient.createEvolutionExperiment(config);
                stream.markdown(`**Evolution Experiment Created**\n\n${JSON.stringify(result, null, 2)}`);
            } catch (error) {
                stream.markdown(`❌ Experiment creation failed: ${error}`);
            }
            return { metadata: { command: 'create-experiment' } };
        }

        return null; // Not an MCP command
    }
}
