# OpenRouter API Key Troubleshooting Guide

## Current Status

✅ OpenRouter service is operational (342 models available)
❌ Your API key returns "401 User not found"

## Most Common Causes

### 1. Account Verification Required
- OpenRouter may require email verification
- Check your email for verification link
- Visit: https://openrouter.ai/account

### 2. Billing/Payment Method
- Even for free tier, a payment method might be required
- Visit: https://openrouter.ai/settings/credits
- Add a payment method (won't be charged unless you exceed free credits)

### 3. Rate Limiting / Account Suspended
- Too many failed requests can temporarily suspend account
- Wait 15-30 minutes before trying again
- Check: https://openrouter.ai/settings

### 4. Using Wrong Account
- You might have multiple OpenRouter accounts
- Verify you're logged into the correct one
- Check email used for signup

## Immediate Solutions

### Option A: Use Different Authentication Method

If you have credits on OpenRouter, try the alternative header format:

```powershell
# Test with X-API-Key header instead of Bearer
$headers = @{
    "X-API-Key" = $env:OPENROUTER_API_KEY
    "Content-Type" = "application/json"
}
$body = @{
    model = "qwen/qwen3-coder:free"
    messages = @(@{
        role = "user"
        content = "test"
    })
} | ConvertTo-Json

Invoke-RestMethod -Uri "https://openrouter.ai/api/v1/chat/completions" -Method POST -Headers $headers -Body $body
```

### Option B: Create Fresh Account

1. Logout of OpenRouter completely
2. Clear browser cookies
3. Visit https://openrouter.ai/auth?sign_up=true
4. Use different email if available
5. Complete verification immediately
6. Add payment method (for free tier access)
7. Generate new API key
8. Test with: `python test_openrouter_key.py`

### Option C: Alternative Model Providers

While OpenRouter issues are resolved, use alternatives:

**1. Ollama (Already working)**
- Tier 1: Context preparation ✅
- Can also do Tier 2 code generation
- Free, local, no API keys

**2. Direct DeepSeek API**
```powershell
$env:DEEPSEEK_API_KEY = "your-key"
# Get key from: https://platform.deepseek.com/api_keys
# Cost: $0.0000003/1M tokens
```

**3. Direct Anthropic Claude**
```powershell
$env:ANTHROPIC_API_KEY = "your-key"
# Get key from: https://console.anthropic.com/settings/keys
# Free tier: $5 credit
```

**4. Hugging Face Inference API**
```powershell
$env:HF_TOKEN = "your-token"
# Get from: https://huggingface.co/settings/tokens
# Free tier available
```

## Next Steps for AIOS

### Immediate: Use Ollama for All Tiers

Since Ollama is working, we can:
1. Use `gemma3:1b` for Tier 1 (context) ✅ Already working
2. Use `qwen3-coder:7b` for Tier 2 (generation) - Download: `ollama pull qwen3-coder`
3. Use `deepseek-chat` for Tier 3 (validation) - Download: `ollama pull deepseek-chat`

**Run this to set up all-Ollama pipeline:**
```powershell
ollama pull qwen3-coder
ollama pull deepseek-chat
```

### Long-term: Fix OpenRouter Access

1. Complete account verification
2. Add payment method
3. Wait for any suspension to clear
4. Re-run setup script

## Testing Commands

```powershell
# Test Ollama is ready
ollama list

# Test OpenRouter key (when fixed)
python test_openrouter_key.py

# Run E501 fixes with current setup
python agentic_e501_fixer.py --fix c:\AIOS\ai\tools\test_file.py
```

## Support

If issues persist after 24 hours:
- Contact OpenRouter support: https://openrouter.ai/docs#errors
- Check status page: https://status.openrouter.ai
- Discord: https://discord.gg/openrouter
