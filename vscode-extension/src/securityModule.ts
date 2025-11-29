import * as vscode from 'vscode';
import { AIOSLogger } from './logger';

/**
 * AIOS Security Module
 * ====================
 *
 * Enforces secure handling of sensitive information in VSCode Copilot chat.
 * NEVER displays secrets in chat responses - uses ephemeral terminal CLI instead.
 *
 * Security Patterns:
 * - Secret Detection: Identifies potential secret content
 * - Terminal Operations: Manipulates secrets via secure CLI commands
 * - Response Sanitization: Removes sensitive data from chat output
 * - Audit Logging: Tracks secret operations without exposing content
 */

export interface SecretOperation {
    type: 'create' | 'update' | 'delete' | 'validate' | 'rotate';
    resource: string;
    description: string;
    terminalCommand: string;
    successPattern?: string;
    errorPattern?: string;
}

export class AIOSSecurityModule {
    private logger: AIOSLogger;
    private terminal?: vscode.Terminal;

    constructor(logger: AIOSLogger) {
        this.logger = logger;
    }

    /**
     * Detects if a message involves sensitive operations
     */
    public containsSecretOperation(message: string): boolean {
        const secretKeywords = [
            'secret', 'token', 'key', 'password', 'credential',
            'vault', 'unseal', 'encrypt', 'decrypt', 'auth',
            'api_key', 'access_token', 'refresh_token',
            'private_key', 'certificate', 'ssl', 'tls'
        ];

        const lowerMessage = message.toLowerCase();
        return secretKeywords.some(keyword => lowerMessage.includes(keyword));
    }

    /**
     * Sanitizes response text to remove any potential secrets
     */
    public sanitizeResponse(text: string): string {
        // Remove potential secrets using regex patterns
        const secretPatterns = [
            /(["']?)(secret|token|key|password)["']?\s*[:=]\s*["']([^"'\s]+)["']/gi,
            /(api_key|access_token|refresh_token|private_key)["']?\s*[:=]\s*["']([^"'\s]+)["']/gi,
            /(vault.*token|unseal.*key)["']?\s*[:=]\s*["']([^"'\s]+)["']/gi,
            /hvs\.[A-Za-z0-9_-]+/gi, // HashiCorp Vault tokens
            /sk-[A-Za-z0-9_-]+/gi, // OpenAI API keys
            /[A-Za-z0-9_-]{20,}/g // Generic long alphanumeric strings (potential keys)
        ];

        let sanitized = text;
        secretPatterns.forEach(pattern => {
            sanitized = sanitized.replace(pattern, (match, ...groups) => {
                // Log the detection without exposing the secret
                this.logger.warn('Potential secret detected and redacted in response', {
                    pattern: pattern.source,
                    length: match.length
                });
                return '[REDACTED_SECRET]';
            });
        });

        return sanitized;
    }

    /**
     * Executes secret operations via ephemeral terminal
     */
    public async executeSecretOperation(operation: SecretOperation): Promise<boolean> {
        try {
            // Create ephemeral terminal for secret operations
            this.terminal = vscode.window.createTerminal({
                name: 'AIOS Security Terminal',
                isTransient: true, // Ephemeral - disappears after use
                hideFromUser: false // Show to user but mark as secure
            });

            this.logger.info('Executing secure operation via terminal', {
                type: operation.type,
                resource: operation.resource,
                description: operation.description
            });

            // Execute the command
            this.terminal.sendText(operation.terminalCommand);
            this.terminal.sendText('echo "AIOS Security Operation Complete"');

            // Wait for operation to complete (basic implementation)
            await new Promise(resolve => setTimeout(resolve, 2000));

            // Clean up terminal
            this.terminal.dispose();
            this.terminal = undefined;

            this.logger.info('Secure operation completed successfully');
            return true;

        } catch (error) {
            this.logger.error('Failed to execute secure operation', error);
            if (this.terminal) {
                this.terminal.dispose();
                this.terminal = undefined;
            }
            return false;
        }
    }

    /**
     * Generates secure operation for common secret tasks
     */
    public generateVaultOperation(operation: string, context?: any): SecretOperation | null {
        const lowerOp = operation.toLowerCase();

        if (lowerOp.includes('init') || lowerOp.includes('initialize')) {
            return {
                type: 'create',
                resource: 'vault',
                description: 'Initialize HashiCorp Vault with secure key generation',
                terminalCommand: 'docker exec aios-vault vault operator init -format=json > vault_init.json && echo "Vault initialized. Keys saved to vault_init.json (KEEP SECURE)"'
            };
        }

        if (lowerOp.includes('unseal')) {
            return {
                type: 'update',
                resource: 'vault',
                description: 'Unseal HashiCorp Vault using stored keys',
                terminalCommand: 'if [ -f vault_init.json ]; then for key in $(jq -r ".unseal_keys_b64[]" vault_init.json | head -3); do docker exec aios-vault vault operator unseal $key; done && echo "Vault unsealed successfully"; else echo "vault_init.json not found. Run vault init first."; fi'
            };
        }

        if (lowerOp.includes('status') || lowerOp.includes('health')) {
            return {
                type: 'validate',
                resource: 'vault',
                description: 'Check HashiCorp Vault status and health',
                terminalCommand: 'docker exec aios-vault vault status --format=json || echo "Vault container not running"'
            };
        }

        return null;
    }

    /**
     * Generates secure operation for API key management
     */
    public generateApiKeyOperation(operation: string, service?: string): SecretOperation | null {
        const lowerOp = operation.toLowerCase();

        if (lowerOp.includes('set') || lowerOp.includes('configure') || lowerOp.includes('add')) {
            const envVar = service ? `${service.toUpperCase()}_API_KEY` : 'API_KEY';
            return {
                type: 'create',
                resource: 'api_key',
                description: `Securely set ${service || 'API'} key via environment`,
                terminalCommand: `read -s -p "Enter ${service || 'API'} key: " key && echo && export ${envVar}="$key" && echo "${envVar} configured securely"`
            };
        }

        if (lowerOp.includes('validate') || lowerOp.includes('test') || lowerOp.includes('check')) {
            const envVar = service ? `${service.toUpperCase()}_API_KEY` : 'API_KEY';
            return {
                type: 'validate',
                resource: 'api_key',
                description: `Validate ${service || 'API'} key configuration`,
                terminalCommand: `if [ -n "$${envVar}" ]; then echo "${envVar} is configured (length: $(echo "$${envVar}" | wc -c) chars)"; else echo "${envVar} not configured"; fi`
            };
        }

        return null;
    }

    /**
     * Processes a message and returns secure response
     */
    public async processSecureMessage(message: string): Promise<string> {
        if (!this.containsSecretOperation(message)) {
            return ''; // Not a security operation
        }

        this.logger.info('Processing secure operation request', {
            messageLength: message.length,
            containsSecrets: true
        });

        // Try vault operations first
        let operation = this.generateVaultOperation(message);
        if (operation) {
            const success = await this.executeSecretOperation(operation);
            return success
                ? `✅ **Secure Operation Completed**\n\n${operation.description}\n\n*Operation executed via secure terminal. Check terminal output for details.*`
                : `❌ **Secure Operation Failed**\n\n${operation.description}\n\n*Check terminal for error details.*`;
        }

        // Try API key operations
        const apiMatch = message.match(/(openai|anthropic|openrouter|github|azure)/i);
        operation = this.generateApiKeyOperation(message, apiMatch ? apiMatch[1] : undefined);
        if (operation) {
            const success = await this.executeSecretOperation(operation);
            return success
                ? `✅ **API Key Operation Completed**\n\n${operation.description}\n\n*Key configured securely via terminal. Never displayed in chat.*`
                : `❌ **API Key Operation Failed**\n\n${operation.description}\n\n*Check terminal for error details.*`;
        }

        // Generic secure operation
        return `🔒 **Security Operation Detected**\n\nYour request involves sensitive operations. For security, this must be handled via terminal CLI.\n\n**Available Secure Operations:**\n• Vault initialization/unsealing\n• API key configuration\n• Certificate management\n\n*Use specific commands like "initialize vault" or "set OpenAI key" for guided secure operations.*`;
    }

    /**
     * Validates that a response doesn't contain secrets before display
     */
    public validateResponse(response: string): { isValid: boolean; sanitizedResponse: string; violations: string[] } {
        const violations: string[] = [];
        let sanitizedResponse = response;

        // Check for common secret patterns
        const patterns = [
            { name: 'Vault Token', regex: /hvs\.[A-Za-z0-9_-]+/gi },
            { name: 'OpenAI Key', regex: /sk-[A-Za-z0-9_-]+/gi },
            { name: 'Generic API Key', regex: /[A-Za-z0-9_-]{32,}/g },
            { name: 'Password Pattern', regex: /password["']?\s*[:=]\s*["'][^"'\s]+["']/gi },
            { name: 'Secret Pattern', regex: /secret["']?\s*[:=]\s*["'][^"'\s]+["']/gi }
        ];

        patterns.forEach(pattern => {
            const matches = response.match(pattern.regex);
            if (matches) {
                violations.push(`${pattern.name}: ${matches.length} instances detected`);
                sanitizedResponse = sanitizedResponse.replace(pattern.regex, '[REDACTED_SECRET]');
            }
        });

        return {
            isValid: violations.length === 0,
            sanitizedResponse,
            violations
        };
    }
}