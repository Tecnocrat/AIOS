import * as vscode from 'vscode';
import { AIOSLogger } from './logger';

export interface ContextMessage {
    id: string;
    timestamp: number;
    role: 'user' | 'assistant' | 'system';
    content: string;
    metadata?: {
        workspaceContext?: WorkspaceContext;
        aiResponse?: AIOSResponse;
    };
}

export interface WorkspaceContext {
    workspaceFolders: string[];
    activeFile?: string;
    openFiles: string[];
    gitBranch?: string;
    projectType?: string;
}

export interface AIOSResponse {
    text: string;
    actions?: string[];
    context?: any;
    confidence?: number;
}

export interface ConversationState {
    id: string;
    messages: ContextMessage[];
    workspaceContext: WorkspaceContext;
    lastActivity: number;
    iterationCount: number;
    metadata: {
        version: string;
        aiosVersion: string;
    };
}

export class AIOSContextManager {
    private context: vscode.ExtensionContext;
    private logger: AIOSLogger;
    private currentConversation: ConversationState | null = null;
    private maxHistorySize: number;
    private persistAcrossRestarts: boolean;

    constructor(context: vscode.ExtensionContext, logger: AIOSLogger) {
        this.context = context;
        this.logger = logger;

        // Load configuration
        const config = vscode.workspace.getConfiguration('aios.context');
        this.maxHistorySize = config.get('maxHistorySize', 1000);
        this.persistAcrossRestarts = config.get('persistAcrossRestarts', true);

        // Listen for configuration changes
        vscode.workspace.onDidChangeConfiguration((e: vscode.ConfigurationChangeEvent) => {
            if (e.affectsConfiguration('aios.context')) {
                this.updateConfiguration();
            }
        });

        // Initialize conversation
        this.initializeConversation();
    }

    private updateConfiguration(): void {
        const config = vscode.workspace.getConfiguration('aios.context');
        this.maxHistorySize = config.get('maxHistorySize', 1000);
        this.persistAcrossRestarts = config.get('persistAcrossRestarts', true);

        this.logger.debug('Context configuration updated', {
            maxHistorySize: this.maxHistorySize,
            persistAcrossRestarts: this.persistAcrossRestarts
        });
    }

    private initializeConversation(): void {
        this.currentConversation = {
            id: this.generateConversationId(),
            messages: [],
            workspaceContext: this.getCurrentWorkspaceContext(),
            lastActivity: Date.now(),
            iterationCount: 0,
            metadata: {
                version: '1.0',
                aiosVersion: '0.4.0'
            }
        };
    }

    private generateConversationId(): string {
        return `aios-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    }

    private getCurrentWorkspaceContext(): WorkspaceContext {
        const workspaceFolders = vscode.workspace.workspaceFolders?.map(folder => folder.uri.fsPath) || [];
        const activeFile = vscode.window.activeTextEditor?.document.uri.fsPath;
        const openFiles = vscode.workspace.textDocuments.map(doc => doc.uri.fsPath);

        return {
            workspaceFolders,
            activeFile,
            openFiles,
            // TODO: Add git branch detection
            // TODO: Add project type detection
        };
    }

    public addMessage(role: 'user' | 'assistant' | 'system', content: string, metadata?: any): void {
        if (!this.currentConversation) {
            this.initializeConversation();
        }

        const message: ContextMessage = {
            id: `msg-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
            timestamp: Date.now(),
            role,
            content,
            metadata: {
                workspaceContext: this.getCurrentWorkspaceContext(),
                ...metadata
            }
        };

        this.currentConversation!.messages.push(message);
        this.currentConversation!.lastActivity = Date.now();
        this.currentConversation!.iterationCount++;

        // Trim messages if exceeding max size
        if (this.currentConversation!.messages.length > this.maxHistorySize) {
            const removeCount = this.currentConversation!.messages.length - this.maxHistorySize;
            this.currentConversation!.messages.splice(0, removeCount);
            this.logger.debug(`Trimmed ${removeCount} old messages from context`);
        }

        this.logger.debug('Added message to context', {
            role,
            messageId: message.id,
            totalMessages: this.currentConversation!.messages.length
        });
    }

    public getMessages(): ContextMessage[] {
        return this.currentConversation?.messages || [];
    }

    public getConversationState(): ConversationState | null {
        return this.currentConversation;
    }

    public async saveContext(): Promise<void> {
        if (!this.persistAcrossRestarts || !this.currentConversation) {
            this.logger.debug('Context persistence disabled or no conversation to save');
            return;
        }

        try {
            const stateKey = 'aios.conversationState';
            await this.context.globalState.update(stateKey, this.currentConversation);

            this.logger.info('Context saved successfully', {
                messageCount: this.currentConversation.messages.length,
                conversationId: this.currentConversation.id
            });
        } catch (error) {
            this.logger.error('Failed to save context:', error);
            throw error;
        }
    }

    public async loadContext(): Promise<void> {
        if (!this.persistAcrossRestarts) {
            this.logger.debug('Context persistence disabled');
            return;
        }

        try {
            const stateKey = 'aios.conversationState';
            const savedState = this.context.globalState.get<ConversationState>(stateKey);

            if (savedState) {
                // Validate and restore state
                this.currentConversation = {
                    ...savedState,
                    workspaceContext: this.getCurrentWorkspaceContext(), // Update with current workspace
                    lastActivity: Date.now()
                };

                this.logger.info('Context loaded successfully', {
                    messageCount: this.currentConversation.messages.length,
                    conversationId: this.currentConversation.id,
                    iterationCount: this.currentConversation.iterationCount
                });
            } else {
                this.logger.debug('No saved context found, initializing new conversation');
                this.initializeConversation();
            }
        } catch (error) {
            this.logger.error('Failed to load context:', error);
            this.initializeConversation(); // Fallback to new conversation
        }
    }

    public resetContext(): void {
        this.logger.info('Resetting conversation context');
        this.initializeConversation();

        // Clear saved state
        if (this.persistAcrossRestarts) {
            Promise.resolve(this.context.globalState.update('aios.conversationState', undefined))
                .then(() => {
                    this.logger.debug('Saved context cleared successfully');
                })
                .catch((err: any) => {
                    this.logger.error('Failed to clear saved context:', err);
                });
        }
    }

    public getContextStats(): { messageCount: number; iterationCount: number; lastActivity: Date } {
        if (!this.currentConversation) {
            return { messageCount: 0, iterationCount: 0, lastActivity: new Date() };
        }

        return {
            messageCount: this.currentConversation.messages.length,
            iterationCount: this.currentConversation.iterationCount,
            lastActivity: new Date(this.currentConversation.lastActivity)
        };
    }
}
