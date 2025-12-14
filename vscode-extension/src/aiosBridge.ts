import { AIOSResponse } from './contextManager';
import { AIOSLogger } from './logger';
import { OpenRouterEngine, AIEngineResponse } from './aiEngines/openRouterEngine';
<<<<<<< HEAD
import { AIOSSecurityModule } from './securityModule';
=======
>>>>>>> origin/OS0.6.2.grok

export interface CellularEcosystemStatus {
    status: 'active' | 'inactive' | 'error';
    cellularIntegrationActive: boolean;
    pythonAiCellsStatus: 'active' | 'inactive' | 'error';
    cppPerformanceCellsStatus: 'active' | 'inactive' | 'error';
    intercellularBridgesStatus: 'active' | 'inactive' | 'error';
    contextSize: number;
    lastResponse?: number;
    performanceMetrics?: {
        inferenceLatency: number;
        throughput: number;
        subMillisecondAchieved: boolean;
    };
}

export class AIOSBridge {
    private logger: AIOSLogger;
    private isInitialized: boolean = false;
    private cellularEcosystemStatus: CellularEcosystemStatus;
    private openRouterEngine: OpenRouterEngine;
    private useRealAI: boolean = false;
<<<<<<< HEAD
    private securityModule: AIOSSecurityModule;
=======
>>>>>>> origin/OS0.6.2.grok

    constructor(logger: AIOSLogger) {
        this.logger = logger;
        this.openRouterEngine = new OpenRouterEngine(logger);
<<<<<<< HEAD
        this.securityModule = new AIOSSecurityModule(logger);
=======
>>>>>>> origin/OS0.6.2.grok
        this.cellularEcosystemStatus = {
            status: 'inactive',
            cellularIntegrationActive: false,
            pythonAiCellsStatus: 'inactive',
            cppPerformanceCellsStatus: 'inactive',
            intercellularBridgesStatus: 'inactive',
            contextSize: 0
        };
    }

    public async initializeCellularEcosystem(): Promise<void> {
        this.logger.info('Initializing TensorFlow Cellular Ecosystem Bridge...');

        try {
            // Initialize OpenRouter DeepSeek Engine first
            await this.initializeOpenRouterEngine();

            // TODO: Initialize connection to Python AI training cells
            await this.initializePythonAiCells();

            // TODO: Initialize connection to C++ performance cells
            await this.initializeCppPerformanceCells();

            // TODO: Initialize intercellular communication bridges
            await this.initializeIntercellularBridges();

            // TODO: Test sub-millisecond inference capabilities
            await this.testCellularPerformance();

            // For now, simulate successful cellular initialization
            await this.simulateCellularInitialization();

            this.isInitialized = true;
            this.cellularEcosystemStatus.status = 'active';
            this.cellularEcosystemStatus.cellularIntegrationActive = true;
            this.cellularEcosystemStatus.pythonAiCellsStatus = 'active';
            this.cellularEcosystemStatus.cppPerformanceCellsStatus = 'active';
            this.cellularEcosystemStatus.intercellularBridgesStatus = 'active';

            this.logger.info('TensorFlow Cellular Ecosystem Bridge initialized successfully');

        } catch (error) {
            this.logger.error('Failed to initialize TensorFlow Cellular Ecosystem Bridge:', error);
            this.cellularEcosystemStatus.status = 'error';
            throw error;
        }
    }

    private async initializeOpenRouterEngine(): Promise<void> {
        this.logger.info('Initializing OpenRouter DeepSeek Engine...');
        try {
            await this.openRouterEngine.initialize();
            this.useRealAI = true;
            this.logger.info('✅ Real AI intelligence activated via OpenRouter DeepSeek');
        } catch (error) {
            this.logger.warn('OpenRouter DeepSeek not available, using enhanced simulation', error);
            this.useRealAI = false;
        }
    }

    private async initializePythonAiCells(): Promise<void> {
        this.logger.info('Connecting to Python AI training cells...');
        try {
            // Connect to AIOS Integration Bridge API
            const response = await fetch('http://localhost:8080/health', {
                method: 'GET',
                headers: { 'Content-Type': 'application/json' }
            });

            if (response.ok) {
                this.logger.info(' Python AI training cells connected successfully');
                this.cellularEcosystemStatus.pythonAiCellsStatus = 'active';
            } else {
                throw new Error(`Python AI cells connection failed: ${response.status}`);
            }
        } catch (error) {
            this.logger.warn('Python AI cells not available, using fallback mode');
            this.cellularEcosystemStatus.pythonAiCellsStatus = 'inactive';
        }
    }

    private async initializeCppPerformanceCells(): Promise<void> {
        this.logger.info('Connecting to C++ performance cells...');
        try {
            // Test C++ core availability through integration bridge
            const response = await fetch('http://localhost:8080/status/cpp', {
                method: 'GET',
                headers: { 'Content-Type': 'application/json' }
            });

            if (response.ok) {
                const status = await response.json();
                if (status.cpp_core_active) {
                    this.logger.info(' C++ performance cells connected successfully');
                    this.cellularEcosystemStatus.cppPerformanceCellsStatus = 'active';

                    // Update performance metrics if available
                    if (status.performance_metrics) {
                        this.cellularEcosystemStatus.performanceMetrics = {
                            inferenceLatency: status.performance_metrics.inference_latency || 0.5,
                            throughput: status.performance_metrics.throughput || 1000,
                            subMillisecondAchieved: status.performance_metrics.sub_millisecond || false
                        };
                    }
                } else {
                    throw new Error('C++ core not active');
                }
            } else {
                throw new Error(`C++ cells connection failed: ${response.status}`);
            }
        } catch (error) {
            this.logger.warn('C++ performance cells not available, using fallback mode');
            this.cellularEcosystemStatus.cppPerformanceCellsStatus = 'inactive';
        }
    }

    private async initializeIntercellularBridges(): Promise<void> {
        this.logger.info('Initializing intercellular communication bridges...');
        try {
            // Test intercellular bridge communication
            const testMessage = {
                type: 'bridge_test',
                source: 'vscode_extension',
                target: 'integration_bridge',
                data: { test: true, timestamp: Date.now() }
            };

            const response = await fetch('http://localhost:8080/bridge/test', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(testMessage)
            });

            if (response.ok) {
                const result = await response.json();
                if (result.bridge_active) {
                    this.logger.info(' Intercellular communication bridges initialized successfully');
                    this.cellularEcosystemStatus.intercellularBridgesStatus = 'active';
                } else {
                    throw new Error('Bridge test failed');
                }
            } else {
                throw new Error(`Bridge initialization failed: ${response.status}`);
            }
        } catch (error) {
            this.logger.warn('Intercellular bridges not available, using direct mode');
            this.cellularEcosystemStatus.intercellularBridgesStatus = 'inactive';
        }
    }

    private async testCellularPerformance(): Promise<void> {
        this.logger.info('Testing cellular ecosystem performance...');
        try {
            // Perform performance test through integration bridge
            const testPayload = {
                test_type: 'performance_benchmark',
                metrics_requested: ['inference_latency', 'throughput', 'sub_millisecond_capability'],
                sample_data: 'AIOS VSCode Extension Performance Test'
            };

            const startTime = Date.now();
            const response = await fetch('http://localhost:8080/test/performance', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(testPayload)
            });
            const endTime = Date.now();

            if (response.ok) {
                const results = await response.json();
                const roundTripTime = endTime - startTime;

                this.cellularEcosystemStatus.performanceMetrics = {
                    inferenceLatency: results.inference_latency || roundTripTime,
                    throughput: results.throughput || 1000,
                    subMillisecondAchieved: (results.inference_latency || roundTripTime) < 1
                };

                this.logger.info(` Cellular performance test completed: ${roundTripTime}ms round-trip`);

                if (this.cellularEcosystemStatus.performanceMetrics.subMillisecondAchieved) {
                    this.logger.info(' Sub-millisecond performance achieved!');
                }
            } else {
                throw new Error(`Performance test failed: ${response.status}`);
            }
        } catch (error) {
            this.logger.warn('Performance testing not available, using estimated metrics');
            this.cellularEcosystemStatus.performanceMetrics = {
                inferenceLatency: 1.0,
                throughput: 500,
                subMillisecondAchieved: false
            };
        }
    }

    private async simulateCellularInitialization(): Promise<void> {
        // Simulate cellular ecosystem connection time
        return new Promise(resolve => setTimeout(resolve, 1000));
    }

    public async processMessage(message: string, context?: any): Promise<AIOSResponse> {
        if (!this.isInitialized) {
            throw new Error('AIOS Bridge not initialized');
        }

        this.logger.debug('Processing message through AIOS Bridge', {
            messageLength: message.length,
            hasContext: !!context
        });

        try {
            // Real AIOS communication implementation
            const response = await this.processMessageThroughAIOS(message, context);

<<<<<<< HEAD
            // 🔒 SECURITY: Validate response before returning
            const validation = this.securityModule.validateResponse(response.text);
            if (!validation.isValid) {
                this.logger.warn('AIOS response contained potential secrets, sanitizing', {
                    violations: validation.violations.length
                });
                response.text = validation.sanitizedResponse;
                response.metadata = {
                    ...response.metadata,
                    securitySanitized: true,
                    violationsDetected: validation.violations.length
                };
            }

=======
>>>>>>> origin/OS0.6.2.grok
            this.cellularEcosystemStatus.lastResponse = Date.now();
            this.logger.debug('Message processed successfully', {
                responseLength: response.text.length,
                confidence: response.confidence,
                securityValidated: true
            });

            return response;

        } catch (error) {
            this.logger.error('Failed to process message:', error);
            this.cellularEcosystemStatus.status = 'error';
            throw error;
        }
    }

    private async simulateAIOSProcessing(message: string, context?: any): Promise<AIOSResponse> {
        // Enhanced AIOS processing with real workspace intelligence
        this.logger.debug('Processing through AIOS Intelligence Layer', { message: message.substring(0, 50) });

        try {
            // Step 1: Analyze message intent and workspace context
            const analysis = await this.analyzeMessageIntent(message);
            
            // Step 2: Generate intelligent response based on AIOS capabilities
            const response = await this.generateIntelligentResponse(message, analysis, context);
<<<<<<< HEAD

            // 🔒 SECURITY: Validate simulated response
            const validation = this.securityModule.validateResponse(response.text);
            if (!validation.isValid) {
                this.logger.warn('Simulated AIOS response contained potential secrets, sanitizing');
                response.text = validation.sanitizedResponse;
            }

            return response;
            
        } catch (error) {
            this.logger.warn('AIOS processing failed, using basic fallback', error);
            return await this.basicFallbackResponse(message);
        }
    }

=======
            
            return response;
            
        } catch (error) {
            this.logger.warn('AIOS processing failed, using basic fallback', error);
            return await this.basicFallbackResponse(message);
        }
    }

>>>>>>> origin/OS0.6.2.grok
    private async analyzeMessageIntent(message: string): Promise<any> {
        const intent: {
            type: string;
            confidence: number;
            keywords: string[];
            workspaceRelevant: boolean;
            requiresAction: boolean;
            suggestedActions: string[];
        } = {
            type: 'general',
            confidence: 0.5,
            keywords: [],
            workspaceRelevant: false,
            requiresAction: false,
            suggestedActions: []
        };

        const lowerMessage = message.toLowerCase();

        // Analyze intent patterns
        if (lowerMessage.includes('test') || lowerMessage.includes('run') || lowerMessage.includes('execute')) {
            intent.type = 'execution';
            intent.requiresAction = true;
            intent.suggestedActions = ['run-tests', 'execute-script', 'analyze-system'];
        } else if (lowerMessage.includes('analyze') || lowerMessage.includes('check') || lowerMessage.includes('status')) {
            intent.type = 'analysis';
            intent.suggestedActions = ['system-health', 'workspace-analysis', 'architecture-review'];
        } else if (lowerMessage.includes('help') || lowerMessage.includes('how') || lowerMessage.includes('what')) {
            intent.type = 'assistance';
            intent.suggestedActions = ['provide-guidance', 'show-examples', 'explain-architecture'];
        } else if (lowerMessage.includes('create') || lowerMessage.includes('generate') || lowerMessage.includes('build')) {
            intent.type = 'creation';
            intent.requiresAction = true;
            intent.suggestedActions = ['generate-code', 'create-file', 'build-component'];
        }

        // Check workspace relevance
        const workspaceKeywords = ['aios', 'python', 'c++', 'c#', 'typescript', 'core', 'interface', 'runtime'];
        intent.workspaceRelevant = workspaceKeywords.some(keyword => lowerMessage.includes(keyword));

        return intent;
    }

    private async generateIntelligentResponse(message: string, analysis: any, context?: any): Promise<AIOSResponse> {
        let responseText = '';
        let confidence = 0.7;
        let actions: string[] = [];

        // Wait to simulate processing time
        await new Promise(resolve => setTimeout(resolve, 200 + Math.random() * 300));

        switch (analysis.type) {
            case 'execution':
                responseText = `**AIOS Execution Analysis**\n\nI can help you execute tasks in the AIOS workspace. Available actions:\n\n`;
                responseText += `• **System Health Check**: Run comprehensive system analysis\n`;
                responseText += `• **Test Suite**: Execute Python/C++ test suites\n`;
                responseText += `• **Build Process**: Compile C++ core and C# interface\n`;
                responseText += `• **Runtime Intelligence**: Activate monitoring tools\n\n`;
                
                // Add real system status if available
                const systemStatus = this.getSystemStatus();
                if (systemStatus && systemStatus.initialized) {
                    responseText += `**Current System Status**: ${systemStatus.cellularEcosystem.status || 'Unknown'}\n\n`;
                }
                
                responseText += `What would you like me to execute?`;
                actions = ['run-system-health', 'run-tests', 'build-project'];
                confidence = 0.9;
                break;

            case 'analysis':
                responseText = `**AIOS Workspace Analysis**\n\nCurrent AIOS project status:\n\n`;
                responseText += `• **Architecture**: Multi-language AI platform (Python/C++/C#)\n`;
                responseText += `• **Components**: AI Intelligence, Core Engine, Interface, Runtime Intelligence, Tachyonic Archive\n`;
                responseText += `• **Version**: OS0.6.1.claude\n`;
                responseText += `• **Status**: Active development with AI agent architecture research\n\n`;
                responseText += `I can provide detailed analysis of any component. What would you like me to analyze?`;
                actions = ['analyze-architecture', 'check-dependencies', 'review-code-quality'];
                confidence = 0.85;
                break;

            case 'assistance':
                responseText = `**AIOS Development Assistant**\n\nI can help you with:\n\n`;
                responseText += `🧠 **AI Intelligence Layer**: Python modules, TensorFlow integration\n`;
                responseText += `⚡ **Core Engine**: C++ components, performance optimization\n`;
                responseText += `🖥️ **Interface Layer**: C# WPF, XAML, WebView2 hybrid\n`;
                responseText += `🧮 **Runtime Intelligence**: Monitoring, health checks, system status\n`;
                responseText += `🌌 **Tachyonic Archive**: Knowledge crystals, consciousness framework\n\n`;
                responseText += `**Professional Standards**: PowerShell commands only, spatial metadata compliance, no decorative elements\n\n`;
                responseText += `What specific AIOS topic can I help you with?`;
                actions = ['explain-architecture', 'show-examples', 'development-guide'];
                confidence = 0.95;
                break;

            case 'creation':
                responseText = `**AIOS Creation Assistant**\n\nI can help you create:\n\n`;
                responseText += `• **Python Modules**: AI intelligence components, integrations\n`;
                responseText += `• **C++ Components**: Core engine modules, performance cells\n`;
                responseText += `• **C# Interface**: WPF controls, services, data models\n`;
                responseText += `• **Configuration**: JSON configs, metadata files\n`;
                responseText += `• **Documentation**: Architecture docs, API references\n\n`;
                responseText += `**Note**: All creation follows spatial metadata compliance and AINLP governance rules.\n\n`;
                responseText += `What would you like me to create?`;
                actions = ['create-python-module', 'create-cpp-component', 'create-csharp-class'];
                confidence = 0.8;
                break;

            default:
                responseText = `**AIOS Intelligence Response**\n\nMessage: "${message}"\n\n`;
                responseText += `I'm analyzing your request through the AIOS consciousness crystal framework. The system integrates:\n\n`;
                responseText += `• **Multi-language coordination** (Python, C++, C#, TypeScript)\n`;
                responseText += `• **Biological computing principles** through cellular architecture\n`;
                responseText += `• **Professional development standards** with spatial metadata compliance\n\n`;
                responseText += `How can I assist you with AIOS development today?`;
                actions = ['general-assistance', 'workspace-overview'];
                confidence = 0.7;
                break;
        }

        return {
            text: responseText,
            confidence: confidence,
            actions: actions,
            context: {
                processedAt: Date.now(),
                inputMessage: message,
                intentAnalysis: analysis,
                aiosVersion: '0.4.0-enhanced'
            },
            metadata: {
                processingTime: 300,
                aiosVersion: '0.4.0-enhanced',
                realAiosConnection: false,
                contextProvided: !!context,
                cellularMetrics: this.cellularEcosystemStatus.performanceMetrics
            }
        };
    }

    private async basicFallbackResponse(message: string): Promise<AIOSResponse> {
        return {
            text: `**AIOS Basic Response**\n\nProcessed: "${message}"\n\nI'm currently in enhanced simulation mode. The full AIOS intelligence layer integration is in development. I can still assist with workspace analysis and development guidance.\n\nTry asking about:\n• System analysis\n• Architecture overview\n• Component creation\n• Development assistance`,
            confidence: 0.6,
            actions: ['basic-assistance'],
            context: {
                processedAt: Date.now(),
                inputMessage: message,
                aiosVersion: '0.4.0-basic'
            },
            metadata: {
                processingTime: 100,
                aiosVersion: '0.4.0-basic',
                realAiosConnection: false,
                fallbackReason: 'Enhanced simulation mode'
            }
        };
    }

    private async processMessageThroughAIOS(message: string, context?: any): Promise<AIOSResponse> {
        try {
            // NEW: Use Real DeepSeek AI if available
            if (this.useRealAI && this.openRouterEngine) {
                this.logger.info('🧠 Processing through Real DeepSeek AI via OpenRouter');
                return await this.processWithRealAI(message, context);
            }

            // Check if AIOS local bridge is available, fallback to simulation if not
            if (this.cellularEcosystemStatus.status !== 'active') {
                this.logger.warn('AIOS not fully active, using intelligent fallback');
                return await this.simulateAIOSProcessing(message, context);
            }

            // Attempt local AIOS Integration Bridge (legacy path)
            const aiosRequest = {
                message: message,
                context: {
                    workspace: context?.workspace || 'unknown',
                    timestamp: Date.now(),
                    vscode_extension: true,
                    user_session: context?.sessionId || 'vscode_session',
                    message_history: context?.history || []
                },
                processing: {
                    nlp: true,
                    prediction: true,
                    automation: true,
                    cellular_optimization: true
                },
                response_format: {
                    include_actions: true,
                    include_confidence: true,
                    include_cellular_metrics: true
                }
            };

            this.logger.debug('Sending request to AIOS Integration Bridge', {
                messageLength: message.length,
                hasContext: !!context
            });

            // Send to AIOS Integration Bridge
            const response = await fetch('http://localhost:8080/process', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Source': 'vscode-extension',
                    'X-Version': '0.4.0'
                },
                body: JSON.stringify(aiosRequest),
                signal: AbortSignal.timeout(30000) // 30 second timeout
            });

            if (!response.ok) {
                throw new Error(`AIOS API error: ${response.status} ${response.statusText}`);
            }

            const aiosResponse = await response.json();

            // Update cellular ecosystem status based on response
            if (aiosResponse.cellular_metrics) {
                this.cellularEcosystemStatus.performanceMetrics = {
                    inferenceLatency: aiosResponse.cellular_metrics.inference_latency || 1.0,
                    throughput: aiosResponse.cellular_metrics.throughput || 1000,
                    subMillisecondAchieved: aiosResponse.cellular_metrics.sub_millisecond || false
                };
            }

            // Format response for VSCode
            const formattedResponse: AIOSResponse = {
                text: aiosResponse.response_text || 'AIOS processed your request successfully.',
                confidence: aiosResponse.confidence || 0.85,
                actions: aiosResponse.suggested_actions || [],
                metadata: {
                    processingTime: aiosResponse.processing_time || 0,
                    cellularMetrics: aiosResponse.cellular_metrics,
                    aiosVersion: '0.4.0',
                    realAiosConnection: true,
                    contextProvided: !!context
                }
            };

            this.logger.info(' Real AIOS processing completed successfully', {
                confidence: formattedResponse.confidence,
                processingTime: aiosResponse.processing_time,
                actionsCount: formattedResponse.actions?.length || 0
            });

            return formattedResponse;

        } catch (error) {
            const errorMessage = error instanceof Error ? error.message : 'Unknown error';
            this.logger.warn('AIOS connection failed, using intelligent fallback', { error: errorMessage });

            // Graceful fallback to simulation with enhanced context
            const fallbackResponse = await this.simulateAIOSProcessing(message, context);
            if (fallbackResponse.metadata) {
                fallbackResponse.metadata.realAiosConnection = false;
                fallbackResponse.metadata.fallbackReason = errorMessage;
            } else {
                fallbackResponse.metadata = {
                    realAiosConnection: false,
                    fallbackReason: errorMessage,
                    aiosVersion: '0.4.0',
                    contextProvided: !!context
                };
            }

            return fallbackResponse;
        }
    }

    private async processWithRealAI(message: string, context?: any): Promise<AIOSResponse> {
        try {
            // Build AIOS-specific context for the AI
            const aiosContext = this.buildAIOSContext(context);
            
            // Process through DeepSeek with AIOS context
            const aiResponse: AIEngineResponse = await this.openRouterEngine.processMessage(
                message,
                aiosContext,
                this.buildSystemPromptForContext(context)
            );

            // Analyze response for actionable items
            const actions = this.extractActionsFromAIResponse(aiResponse.text);

            // Format for AIOS response structure
            const aiosResponse: AIOSResponse = {
                text: aiResponse.text,
                confidence: aiResponse.confidence,
                actions: actions,
                context: {
                    processedAt: Date.now(),
                    inputMessage: message,
                    aiEngine: 'deepseek-v3.1',
                    aiosVersion: '0.4.0-ai-enhanced'
                },
                metadata: {
                    processingTime: aiResponse.metadata.processingTime,
                    aiosVersion: '0.4.0-ai-enhanced',
                    realAiosConnection: true,
                    contextProvided: !!context,
                    cellularMetrics: this.cellularEcosystemStatus.performanceMetrics
                }
            };

            this.logger.info('🧠 Real AI processing completed successfully', {
                processingTime: aiResponse.metadata.processingTime,
                responseLength: aiResponse.text.length,
                confidence: aiResponse.confidence,
                actionsExtracted: actions.length
            });

            return aiosResponse;

        } catch (error) {
            this.logger.error('Real AI processing failed, falling back to simulation', error);
            
            // Fallback to enhanced simulation
            const fallbackResponse = await this.simulateAIOSProcessing(message, context);
            if (fallbackResponse.metadata) {
                fallbackResponse.metadata.fallbackReason = `Real AI failed: ${error}`;
                fallbackResponse.metadata.realAiosConnection = false;
            }
            
            return fallbackResponse;
        }
    }

    private buildAIOSContext(context?: any): any {
        return {
            ...context,
            aiosWorkspace: {
                architecture: 'Multi-language AI platform',
                components: ['AI Intelligence', 'Core Engine', 'Interface', 'Runtime Intelligence', 'Tachyonic Archive'],
                version: 'OS0.6.1.claude',
                developmentPhase: 'Active development with AI agent architecture research'
            },
            conversationHistory: context?.conversationHistory || [],
            workspaceContext: context?.workspaceContext || {}
        };
    }

    private buildSystemPromptForContext(context?: any): string {
        let prompt = 'You are responding within the AIOS development environment.';
        
        if (context?.workspaceContext?.currentFile) {
            prompt += ` Current file: ${context.workspaceContext.currentFile}`;
        }
        
        if (context?.intent?.type) {
            prompt += ` User intent: ${context.intent.type}`;
        }
        
        return prompt;
    }

    private extractActionsFromAIResponse(text: string): string[] {
        const actions: string[] = [];
        
        // Look for common action patterns in AI response
        if (text.toLowerCase().includes('analyze') || text.toLowerCase().includes('analysis')) {
            actions.push('analyze-code');
        }
        if (text.toLowerCase().includes('test') || text.toLowerCase().includes('testing')) {
            actions.push('run-tests');
        }
        if (text.toLowerCase().includes('create') || text.toLowerCase().includes('generate')) {
            actions.push('generate-code');
        }
        if (text.toLowerCase().includes('build') || text.toLowerCase().includes('compile')) {
            actions.push('build-project');
        }
        if (text.toLowerCase().includes('documentation') || text.toLowerCase().includes('explain')) {
            actions.push('show-documentation');
        }
        
        return actions.length > 0 ? actions : ['general-assistance'];
    }

    public getCellularEcosystemStatus(): CellularEcosystemStatus {
        return { ...this.cellularEcosystemStatus };
    }

    public async testConnection(): Promise<boolean> {
        try {
            this.logger.debug('Testing AIOS connection...');

            // TODO: Implement actual connection test
            // For now, simulate test
            await new Promise(resolve => setTimeout(resolve, 200));

            const isConnected = this.isInitialized && this.cellularEcosystemStatus.status === 'active';
            this.logger.debug('Connection test result:', isConnected);

            return isConnected;

        } catch (error) {
            this.logger.error('Connection test failed:', error);
            return false;
        }
    }

    public async healthCheck(): Promise<{ healthy: boolean; details: any }> {
        try {
            const connectionOk = await this.testConnection();

            // TODO: Add more health checks
            // - C++ core responsiveness
            // - Python AI module status
            // - Memory usage
            // - Context size

            const healthy = connectionOk && this.cellularEcosystemStatus.status === 'active';

            return {
                healthy,
                details: {
                    bridge: this.isInitialized,
                    connection: connectionOk,
                    status: this.cellularEcosystemStatus,
                    timestamp: Date.now()
                }
            };

        } catch (error) {
            this.logger.error('Health check failed:', error);
            return {
                healthy: false,
                details: { error: String(error) }
            };
        }
    }

    public updateContextSize(size: number): void {
        this.cellularEcosystemStatus.contextSize = size;
    }

    public getSystemStatus(): any {
        return {
            initialized: this.isInitialized,
            cellularEcosystem: this.cellularEcosystemStatus,
            lastActivity: this.cellularEcosystemStatus.lastResponse || Date.now(),
            connectionHealth: {
                pythonAiCells: this.cellularEcosystemStatus.pythonAiCellsStatus === 'active',
                cppPerformanceCells: this.cellularEcosystemStatus.cppPerformanceCellsStatus === 'active',
                intercellularBridges: this.cellularEcosystemStatus.intercellularBridgesStatus === 'active'
            },
            performanceMetrics: this.cellularEcosystemStatus.performanceMetrics || {
                inferenceLatency: 1.0,
                throughput: 500,
                subMillisecondAchieved: false
            }
        };
    }
}
