/**
 * AIOS Copilot Engine
 * ====================
 * AINLP.upgrade[MICROSOFT_AI]: Uses VSCode's Language Model API (vscode.lm)
 * 
 * This engine leverages GitHub Copilot's models directly through VSCode's
 * built-in Language Model API - no external API keys required!
 * 
 * Requirements:
 * - GitHub Copilot subscription (included in user's $10/month plan)
 * - VSCode 1.90+ (Language Model API)
 * 
 * Benefits:
 * - No external API costs
 * - Uses existing Copilot subscription
 * - Privacy: Data stays within Microsoft ecosystem
 * - Reliability: Microsoft-backed infrastructure
 */

import * as vscode from 'vscode';
import { AIOSLogger } from '../logger';

export interface CopilotEngineConfig {
    modelFamily: string;
    vendor: string;
    maxTokens: number;
    temperature: number;
}

export interface AIEngineResponse {
    text: string;
    confidence: number;
    model: string;
    usage?: {
        promptTokens: number;
        completionTokens: number;
        totalTokens: number;
    };
    metadata: {
        processingTime: number;
        engine: string;
        realConnection: boolean;
        timestamp: number;
    };
}

export class CopilotEngine {
    private config: CopilotEngineConfig;
    private logger: AIOSLogger;
    private isInitialized: boolean = false;
    private cachedModel: vscode.LanguageModelChat | null = null;

    constructor(logger: AIOSLogger) {
        this.logger = logger;
        
        this.config = {
            vendor: 'copilot',
            modelFamily: 'gpt-4o',  // Copilot's default model family
            maxTokens: 4096,
            temperature: 0.7
        };
    }

    public async initialize(): Promise<void> {
        this.logger.info('Initializing Microsoft Copilot Engine via vscode.lm API...');

        try {
            // Select available Copilot model
            const models = await vscode.lm.selectChatModels({
                vendor: this.config.vendor,
                family: this.config.modelFamily
            });

            if (models.length === 0) {
                // Try without family filter - get any Copilot model
                const anyModels = await vscode.lm.selectChatModels({
                    vendor: this.config.vendor
                });

                if (anyModels.length === 0) {
                    this.logger.warn('No Copilot models available - ensure GitHub Copilot is installed and authenticated');
                    this.isInitialized = false;
                    return;
                }

                this.cachedModel = anyModels[0]!;
            } else {
                this.cachedModel = models[0]!;
            }

            this.logger.info(`✅ Microsoft Copilot Engine initialized: ${this.cachedModel.name} (${this.cachedModel.family})`);
            this.isInitialized = true;

        } catch (error) {
            if (error instanceof vscode.LanguageModelError) {
                this.logger.warn(`Copilot access issue: ${error.message} (code: ${error.code})`);
                if (error.code === 'NoPermissions') {
                    this.logger.info('User consent required - will prompt on first use');
                }
            } else {
                this.logger.error('Failed to initialize Copilot Engine:', error);
            }
            this.isInitialized = false;
        }
    }

    public async processMessage(
        message: string,
        context?: any,
        systemPrompt?: string,
        token?: vscode.CancellationToken
    ): Promise<AIEngineResponse> {
        const startTime = Date.now();

        // Ensure we have a model
        if (!this.cachedModel) {
            await this.initialize();
        }

        if (!this.cachedModel) {
            return this.createFallbackResponse(message, startTime);
        }

        try {
            // Build messages array
            const messages: vscode.LanguageModelChatMessage[] = [];

            // Add system prompt
            const aiosSystemPrompt = this.buildAIOSSystemPrompt(systemPrompt);
            messages.push(vscode.LanguageModelChatMessage.User(aiosSystemPrompt));

            // Add conversation history if available
            if (context?.conversationHistory) {
                const history = context.conversationHistory.slice(-6);
                for (const msg of history) {
                    if (msg.role === 'user') {
                        messages.push(vscode.LanguageModelChatMessage.User(msg.content));
                    } else if (msg.role === 'assistant') {
                        messages.push(vscode.LanguageModelChatMessage.Assistant(msg.content));
                    }
                }
            }

            // Add current message
            messages.push(vscode.LanguageModelChatMessage.User(message));

            this.logger.debug('Sending request to Copilot', {
                messageCount: messages.length,
                model: this.cachedModel.name
            });

            // Make request
            const response = await this.cachedModel.sendRequest(
                messages,
                {
                    justification: 'AIOS Extension processing user chat request'
                },
                token || new vscode.CancellationTokenSource().token
            );

            // Collect response text
            let responseText = '';
            for await (const part of response.text) {
                responseText += part;
            }

            const processingTime = Date.now() - startTime;

            this.logger.info('✅ Copilot response received', {
                processingTime,
                responseLength: responseText.length,
                model: this.cachedModel.name
            });

            return {
                text: responseText,
                confidence: 0.95,  // High confidence from Copilot
                model: this.cachedModel.name,
                metadata: {
                    processingTime,
                    engine: 'microsoft-copilot',
                    realConnection: true,
                    timestamp: Date.now()
                }
            };

        } catch (error) {
            if (error instanceof vscode.LanguageModelError) {
                this.logger.warn(`Copilot request failed: ${error.message} (${error.code})`);
                
                // Handle specific error codes
                if (error.code === 'NoPermissions') {
                    return {
                        text: '⚠️ **Copilot Access Required**\n\nPlease grant AIOS permission to use GitHub Copilot. A consent dialog should appear.',
                        confidence: 0,
                        model: 'none',
                        metadata: {
                            processingTime: Date.now() - startTime,
                            engine: 'microsoft-copilot-no-permission',
                            realConnection: false,
                            timestamp: Date.now()
                        }
                    };
                }

                if (error.code === 'Blocked') {
                    return {
                        text: '⚠️ **Rate Limited**\n\nCopilot request was blocked (quota exceeded). Please try again in a moment.',
                        confidence: 0,
                        model: 'none',
                        metadata: {
                            processingTime: Date.now() - startTime,
                            engine: 'microsoft-copilot-blocked',
                            realConnection: false,
                            timestamp: Date.now()
                        }
                    };
                }
            }

            this.logger.error('Copilot processing failed:', error);
            return this.createFallbackResponse(message, startTime);
        }
    }

    private createFallbackResponse(message: string, startTime: number): AIEngineResponse {
        return {
            text: `**AIOS Copilot Engine Unavailable**\n\nCopilot integration requires:\n\n` +
                  `1. **GitHub Copilot** installed and signed in\n` +
                  `2. **VSCode 1.90+** for Language Model API\n` +
                  `3. Grant permission when prompted\n\n` +
                  `Your message: "${message.substring(0, 100)}..."\n\n` +
                  `*Using local processing mode.*`,
            confidence: 0,
            model: 'none',
            metadata: {
                processingTime: Date.now() - startTime,
                engine: 'copilot-unavailable',
                realConnection: false,
                timestamp: Date.now()
            }
        };
    }

    private buildAIOSSystemPrompt(customPrompt?: string): string {
        const basePrompt = `You are AIOS (Artificial Intelligence Operative System), an advanced AI assistant integrated into VSCode via the AIOS extension.

## AIOS Context & Capabilities
- **Architecture**: Multi-language AI platform (Python, C++, C#, TypeScript)
- **Components**: AI Intelligence Layer, Core Engine, Interface Layer, Runtime Intelligence, Tachyonic Archive
- **Version**: Current (loaded from .aios_context.json at runtime)
- **Philosophy**: Professional standards, biological computing principles, consciousness crystal framework

## Core Expertise Areas
🧠 **AI Intelligence Layer**: Python modules, TensorFlow integration, machine learning
⚡ **Core Engine**: C++ components, performance optimization
🖥️ **Interface Layer**: C# WPF, XAML, WebView2 hybrid interfaces
🧮 **Runtime Intelligence**: System monitoring, health checks
🌌 **Tachyonic Archive**: Knowledge crystals, consciousness framework

## Professional Standards
- **Environment**: Windows PowerShell only (NO Linux bash commands)
- **Documentation**: Follow AINLP governance - consolidate rather than proliferate
- **Code Quality**: No decorative elements, practical metrics, professional standards

## Response Guidelines
- Provide intelligent, context-aware responses
- Reference specific AIOS components when relevant
- Maintain professional technical communication`;

        if (customPrompt) {
            return `${basePrompt}\n\n## Additional Context\n${customPrompt}`;
        }

        return basePrompt;
    }

    public isReady(): boolean {
        return this.isInitialized && this.cachedModel !== null;
    }

    public getModelInfo(): { name: string; family: string; vendor: string } | null {
        if (!this.cachedModel) {
            return null;
        }
        return {
            name: this.cachedModel.name,
            family: this.cachedModel.family,
            vendor: this.cachedModel.vendor
        };
    }
}
