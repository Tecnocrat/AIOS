import { AIOSLogger } from '../logger';

export interface OpenRouterConfig {
    apiKey: string;
    baseUrl: string;
    model: string;
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

export class OpenRouterEngine {
    private config: OpenRouterConfig;
    private logger: AIOSLogger;
    private isInitialized: boolean = false;

    constructor(logger: AIOSLogger) {
        this.logger = logger;
        
        // Load configuration from environment variables
        const apiKey = process.env.OPENROUTER_API_KEY || 
                      process.env.AIOS_OPENROUTER_API_KEY || 
                      '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';
        
        this.config = {
            apiKey: apiKey,
            baseUrl: 'https://openrouter.ai/api/v1/chat/completions',
            model: process.env.OPENROUTER_MODEL || 'deepseek/deepseek-chat',
            maxTokens: parseInt(process.env.OPENROUTER_MAX_TOKENS || '2048'),
            temperature: parseFloat(process.env.OPENROUTER_TEMPERATURE || '0.7')
        };
    }

    public async initialize(): Promise<void> {
        this.logger.info('Initializing OpenRouter DeepSeek Engine...');

        try {
            // Validate API key
            if (!this.config.apiKey || this.config.apiKey === '') {
                throw new Error('OpenRouter API key not configured');
            }

            // Log configuration (without exposing full API key)
            this.logger.debug('OpenRouter Configuration', {
                model: this.config.model,
                maxTokens: this.config.maxTokens,
                temperature: this.config.temperature,
                hasApiKey: !!this.config.apiKey,
                apiKeyPrefix: this.config.apiKey.substring(0, 8) + '...'
            });

            // Test connection with simple health check
            await this.testConnection();
            
            this.isInitialized = true;
            this.logger.info('✅ OpenRouter DeepSeek Engine initialized successfully');

        } catch (error) {
            this.logger.error('❌ Failed to initialize OpenRouter DeepSeek Engine:', error);
            throw error;
        }
    }

    public async processMessage(
        message: string, 
        context?: any, 
        systemPrompt?: string
    ): Promise<AIEngineResponse> {
        if (!this.isInitialized) {
            throw new Error('OpenRouter Engine not initialized');
        }

        this.logger.debug('Processing message through DeepSeek via OpenRouter', {
            messageLength: message.length,
            hasContext: !!context,
            hasSystemPrompt: !!systemPrompt
        });

        const startTime = Date.now();

        try {
            // Prepare AIOS-aware system prompt
            const aiosSystemPrompt = this.buildAIOSSystemPrompt(systemPrompt, context);

            // Build message array for OpenAI-compatible API
            const messages = [
                { role: 'system', content: aiosSystemPrompt },
                { role: 'user', content: message }
            ];

            // Add conversation history if available
            if (context?.conversationHistory) {
                const historyMessages = context.conversationHistory
                    .slice(-6) // Last 6 messages for context
                    .map((msg: any) => ({
                        role: msg.role,
                        content: msg.content
                    }));
                messages.splice(1, 0, ...historyMessages);
            }

            // Make API request to OpenRouter
            const response = await fetch(this.config.baseUrl, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${this.config.apiKey}`,
                    'Content-Type': 'application/json',
                    'HTTP-Referer': 'https://aios.dev', // Optional: for analytics
                    'X-Title': 'AIOS Development Platform'
                },
                body: JSON.stringify({
                    model: this.config.model,
                    messages: messages,
                    max_tokens: this.config.maxTokens,
                    temperature: this.config.temperature,
                    stream: false
                })
            });

            if (!response.ok) {
                const errorData = await response.text();
                throw new Error(`OpenRouter API error ${response.status}: ${errorData}`);
            }

            const apiResponse = await response.json();
            const processingTime = Date.now() - startTime;

            // Extract response data
            const aiText = apiResponse.choices?.[0]?.message?.content || 'No response generated';
            const usage = apiResponse.usage;

            // Calculate confidence based on response quality
            const confidence = this.calculateConfidence(aiText, usage);

            this.logger.info('✅ DeepSeek processing completed', {
                processingTime,
                responseLength: aiText.length,
                confidence,
                tokensUsed: usage?.total_tokens
            });

            return {
                text: aiText,
                confidence: confidence,
                model: this.config.model,
                usage: usage,
                metadata: {
                    processingTime,
                    engine: 'deepseek-openrouter',
                    realConnection: true,
                    timestamp: Date.now()
                }
            };

        } catch (error) {
            const processingTime = Date.now() - startTime;
            const errorMessage = error instanceof Error ? error.message : 'Unknown error';
            
            this.logger.error('❌ DeepSeek processing failed:', error);
            
            throw new Error(`DeepSeek processing failed: ${errorMessage}`);
        }
    }

    private buildAIOSSystemPrompt(customPrompt?: string, context?: any): string {
        const basePrompt = `You are AIOS (Artificial Intelligence Operative System), an advanced AI assistant specialized in multi-language development platform architecture.

## AIOS Context & Capabilities
- **Architecture**: Multi-language AI platform (Python, C++, C#, TypeScript)
- **Components**: AI Intelligence Layer, Core Engine, Interface Layer, Runtime Intelligence, Tachyonic Archive
- **Version**: OS0.6.1.claude
- **Development Philosophy**: Professional standards, biological computing principles, consciousness crystal framework

## Core Expertise Areas
🧠 **AI Intelligence Layer**: Python modules, TensorFlow integration, machine learning
⚡ **Core Engine**: C++ components, performance optimization, sub-millisecond processing
🖥️ **Interface Layer**: C# WPF, XAML, WebView2 hybrid interfaces
🧮 **Runtime Intelligence**: System monitoring, health checks, performance analysis
🌌 **Tachyonic Archive**: Knowledge crystals, consciousness framework, spatial metadata

## Professional Standards
- **Environment**: Windows PowerShell only (NO Linux bash commands)
- **File Operations**: Check .aios_spatial_metadata.json before creating/modifying files
- **Documentation**: Follow AINLP governance - consolidate rather than proliferate
- **Code Quality**: No decorative elements, practical metrics, professional standards
- **Architecture**: Respect consciousness levels and biological computing principles

## Response Guidelines
- Provide intelligent, context-aware responses
- Include actionable suggestions when appropriate
- Reference specific AIOS components when relevant
- Maintain professional technical communication
- Suggest concrete implementation approaches`;

        if (customPrompt) {
            return `${basePrompt}\n\n## Additional Context\n${customPrompt}`;
        }

        return basePrompt;
    }

    private calculateConfidence(text: string, usage?: any): number {
        let confidence = 0.7; // Base confidence

        // Increase confidence for longer, more detailed responses
        if (text.length > 500) confidence += 0.1;
        if (text.length > 1000) confidence += 0.1;

        // Increase confidence for technical content
        const technicalKeywords = ['python', 'c++', 'c#', 'typescript', 'aios', 'architecture', 'implementation'];
        const technicalMatches = technicalKeywords.filter(keyword => 
            text.toLowerCase().includes(keyword)
        ).length;
        confidence += Math.min(technicalMatches * 0.02, 0.1);

        // Factor in token usage efficiency
        if (usage?.total_tokens && usage.total_tokens < 1000) {
            confidence += 0.05; // Bonus for concise responses
        }

        return Math.min(confidence, 0.95); // Cap at 95%
    }

    private async testConnection(): Promise<void> {
        const testMessage = 'Hello, this is a connection test.';
        
        try {
            const response = await fetch(this.config.baseUrl, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${this.config.apiKey}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    model: this.config.model,
                    messages: [{ role: 'user', content: testMessage }],
                    max_tokens: 50,
                    temperature: 0.1
                })
            });

            if (!response.ok) {
                throw new Error(`Connection test failed: ${response.status}`);
            }

            this.logger.debug('OpenRouter connection test successful');

        } catch (error) {
            throw new Error(`OpenRouter connection test failed: ${error}`);
        }
    }

    public getStatus(): any {
        return {
            initialized: this.isInitialized,
            model: this.config.model,
            hasApiKey: !!this.config.apiKey,
            baseUrl: this.config.baseUrl
        };
    }

    public updateConfig(newConfig: Partial<OpenRouterConfig>): void {
        this.config = { ...this.config, ...newConfig };
        this.logger.debug('OpenRouter configuration updated');
    }
}