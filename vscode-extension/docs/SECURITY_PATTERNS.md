# AIOS Security Patterns
# ======================
#
# CRITICAL SECURITY IMPLEMENTATION
# ================================
#
# This document outlines the mandatory security patterns enforced in AIOS agent mode.
# These patterns ensure that sensitive information is NEVER displayed in VSCode Copilot chat.
#
# ## 🔒 Core Security Principles
#
# ### 1. NEVER SHOW SECRETS IN CHAT
# - API keys, tokens, passwords, certificates
# - Vault unseal keys, root tokens
# - Private keys, SSL certificates
# - Any sensitive configuration data
#
# ### 2. EPHEMERAL TERMINAL CLI OPERATIONS
# - All secret manipulation happens in secure terminal sessions
# - Terminals are transient (disappear after use)
# - Commands are executed securely without exposing sensitive data
#
# ### 3. RESPONSE SANITIZATION
# - All AI responses are scanned for potential secrets
# - Detected secrets are automatically redacted
# - Security violations are logged without exposing content
#
# ## 🛡️ Implementation Details
#
# ### Security Module (`securityModule.ts`)
# - `containsSecretOperation()`: Detects secret-related requests
# - `sanitizeResponse()`: Removes secrets from chat responses
# - `executeSecretOperation()`: Runs secure operations via terminal
# - `validateResponse()`: Comprehensive security validation
#
# ### Integration Points
# - **Chat Participant**: Pre-processes all messages for security
# - **AIOS Bridge**: Sanitizes all AI-generated responses
# - **Terminal Operations**: Ephemeral CLI for secret manipulation
#
# ## 🚨 Security Operations
#
# ### Vault Operations
# ```bash
# # Initialize (secure terminal)
# docker exec aios-vault vault operator init -format=json > vault_init.json
#
# # Unseal (secure terminal)
# for key in $(jq -r ".unseal_keys_b64[]" vault_init.json | head -3); do
#   docker exec aios-vault vault operator unseal $key
# done
# ```
#
# ### API Key Management
# ```bash
# # Set key (secure terminal)
# read -s -p "Enter API key: " key && export API_KEY="$key"
#
# # Validate (secure terminal)
# [ -n "$API_KEY" ] && echo "API key configured" || echo "Not configured"
# ```
#
# ## 📊 Security Monitoring
#
# ### Violation Detection
# - Pattern-based secret detection
# - Automatic redaction and logging
# - Security event tracking
#
# ### Audit Logging
# - Operation types and timestamps
- Resource identifiers (no sensitive content)
- Success/failure status
- Security violation counts
#
# ## 🔧 Developer Guidelines
#
# ### When Adding New Features
# 1. Check if feature involves sensitive data
# 2. Use `securityModule.containsSecretOperation()` for detection
# 3. Implement terminal-based operations for secrets
# 4. Add response sanitization for all outputs
#
# ### Testing Security
# 1. Test with known secret patterns
# 2. Verify terminal operations work correctly
# 3. Confirm chat responses are sanitized
# 4. Check audit logs for proper tracking
#
# ## 🚫 Prohibited Patterns
#
# ### NEVER DO THIS:
# ```typescript
// BAD: Exposing secrets in chat
stream.markdown(`Your API key is: ${apiKey}`);
stream.markdown(`Vault token: hvs.xxxxx`);
```
#
# ### ALWAYS DO THIS:
# ```typescript
# // GOOD: Secure terminal operations
# const operation = securityModule.generateApiKeyOperation('set', 'openai');
# await securityModule.executeSecretOperation(operation);
# stream.markdown('✅ API key configured securely via terminal');
# ```
#
# ## 🔄 Migration Notes
#
# ### From Previous Versions
# - All secret-displaying code must be refactored
# - Chat logs containing secrets should be sanitized
- Terminal operations replace direct secret handling
#
# ### Breaking Changes
# - Responses containing secrets will be automatically redacted
# - Secret operations now require terminal confirmation
# - Enhanced logging for security compliance
#
# ## 📞 Support
#
# For security-related issues or questions:
# 1. Check this document first
# 2. Review security module implementation
# 3. Contact security team for guidance
#
# **REMEMBER**: Security is not optional. These patterns are MANDATORY for all AIOS agent interactions.