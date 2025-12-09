# GitHub Models API Setup Guide

**AINLP.dendritic[VOID→GitHub{models,PAT,Microsoft_Cloud_AI}]**

## Overview

GitHub Models provides **FREE** access to industry-leading AI models through your existing GitHub subscription. This leverages Microsoft Cloud AI infrastructure that you're already paying for!

## Available Models

| Model | Provider | Best For |
|-------|----------|----------|
| `openai/gpt-4o` | OpenAI | Main reasoning, creative tasks |
| `openai/gpt-4o-mini` | OpenAI | Fast verification, concise output |
| `openai/gpt-4.1` | OpenAI | Latest capabilities |
| `meta-llama/llama-3.1-*` | Meta | Open weights, privacy |
| `mistral/mistral-large-2` | Mistral | Low latency, code |

## Step 1: Create Personal Access Token (PAT)

1. Go to **https://github.com/settings/tokens**
2. Click **"Generate new token (classic)"**
3. Give it a name: `AIOS-VOID-Bridge`
4. Select scopes:
   - ✅ **`models`** - Required for GitHub Models API
   - ✅ `repo` (optional - for Actions integration)
5. Click **Generate token**
6. **Copy the token immediately** (you won't see it again!)

## Step 2: Set Environment Variable

### Windows (PowerShell)

```powershell
# Temporary (current session)
$env:GITHUB_TOKEN = "ghp_your_token_here"

# Permanent (user level)
[Environment]::SetEnvironmentVariable("GITHUB_TOKEN", "ghp_your_token_here", "User")
```

### Linux/macOS

```bash
# Add to ~/.bashrc or ~/.zshrc
export GITHUB_TOKEN="ghp_your_token_here"
```

### VS Code Settings

Add to your workspace `.env` file:
```
GITHUB_TOKEN=ghp_your_token_here
```

## Step 3: Verify Setup

```powershell
cd c:\dev\aios-win\aios-core\ai\tools
python -c "
from void_bridge import VOIDBridge
b = VOIDBridge()
print('GitHub token set:', bool(b._github_token))
print('Token length:', len(b._github_token) if b._github_token else 0)
"
```

## Step 4: Test API Call

```powershell
python -c "
from void_bridge import VOIDBridge
b = VOIDBridge()
result = b._github_generate('Say hello in 5 words', 'openai/gpt-4o-mini')
print('Response:', result)
"
```

## Using in VOID Bridge

### Tri-Agent Cascade (Default)

```bash
python void_bridge.py --url "https://example.com/article" --crystallize --tri-agent
```

This uses:
- 🔷 **OLLAMA** (Harmonizer) - Local preprocessing
- 🟡 **GEMINI** (Creator) - Main extraction
- 🔵 **GITHUB** (Verifier) - Quality verification

### Multi-Version Distillation

```bash
python void_bridge.py --url "https://example.com" --crystallize --multi-version 3
```

Generates 3 independent crystallizations using different models, then synthesizes the best elements.

## Rate Limits

GitHub Models has generous rate limits for development:
- Free tier: Suitable for development and experimentation
- Enterprise: Higher limits available

## Troubleshooting

### "GitHub Models generation failed"

1. Check token is set: `echo $env:GITHUB_TOKEN`
2. Verify token has `models` scope
3. Test with curl:

```powershell
curl -L -X POST `
  -H "Accept: application/vnd.github+json" `
  -H "Authorization: Bearer $env:GITHUB_TOKEN" `
  -H "X-GitHub-Api-Version: 2022-11-28" `
  -H "Content-Type: application/json" `
  https://models.github.ai/inference/chat/completions `
  -d '{"model":"openai/gpt-4o-mini","messages":[{"role":"user","content":"Hello"}]}'
```

### Token Expired

GitHub classic PATs don't expire by default, but fine-grained tokens do. Check token expiration at https://github.com/settings/tokens

## Integration Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    VOID BRIDGE v2.0                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐    │
│  │   OLLAMA     │   │   GEMINI     │   │   GITHUB     │    │
│  │  Harmonizer  │ → │   Creator    │ → │   Verifier   │    │
│  │    (Local)   │   │   (Cloud)    │   │  (MS Cloud)  │    │
│  └──────────────┘   └──────────────┘   └──────────────┘    │
│         ↓                  ↓                  ↓              │
│  Entry coherence    Main reasoning     Quality check        │
│  Noise filtering    Extraction         Verification         │
│  Structure detect   Crystallization    Gap analysis         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Related Documentation

- [VOID Pattern](../AINLP/patterns/VOID_PATTERN.md)
- [DEV_PATH.md](../../DEV_PATH.md)
- [GitHub Models Docs](https://docs.github.com/en/github-models)
