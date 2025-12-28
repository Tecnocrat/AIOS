# GitHub Copilot CLI & GitHub CLI Setup Guide

**Purpose**: Enable AIOS agent usage via command line and GitHub automation  
**Date**: November 8, 2025  
**Status**: Setup Required

---

## Overview

This guide helps you set up:
1. **GitHub CLI** (`gh`) - GitHub automation and authentication
2. **GitHub Copilot CLI** (`copilot`) - AI agent invocation from command line

Once configured, you can invoke the AIOS agent with:
```bash
copilot --agent=AIOS --prompt "analyze architecture"
```

---

## Prerequisites

- Windows 10/11 with PowerShell 7+
- Active GitHub Copilot subscription
- Git configured with GitHub credentials

---

## Step 1: Install GitHub CLI

### Option A: Using winget (Recommended)

```powershell
# Install GitHub CLI
winget install --id GitHub.cli

# Verify installation
gh --version
# Expected output: gh version 2.x.x (latest)
```

### Option B: Using Chocolatey

```powershell
# Install with Chocolatey
choco install gh

# Verify installation
gh --version
```

### Option C: Manual Installation

1. Download installer from: https://cli.github.com/
2. Run `gh_X.XX.X_windows_amd64.msi`
3. Restart PowerShell
4. Verify: `gh --version`

---

## Step 2: Authenticate GitHub CLI

### Interactive Authentication

```powershell
# Authenticate with GitHub
gh auth login

# Follow prompts:
# 1. "What account do you want to log into?" → GitHub.com
# 2. "What is your preferred protocol?" → HTTPS
# 3. "Authenticate Git with your GitHub credentials?" → Yes
# 4. "How would you like to authenticate?" → Login with a web browser

# Copy the one-time code shown
# Press Enter to open browser
# Paste code in browser and authorize
```

### Verify Authentication

```powershell
# Check authentication status
gh auth status

# Expected output:
# ✓ Logged in to github.com as YOUR_USERNAME (oauth_token)
# ✓ Git operations for github.com configured to use https protocol
# ✓ Token: gho_************************************
```

### Token Scopes Required

Ensure your token has these scopes:
- `repo` - Full repository access
- `read:org` - Read organization membership
- `workflow` - Update GitHub Actions workflows

---

## Step 3: Install GitHub Copilot CLI

### Using npm (Recommended)

```powershell
# Check if Node.js is installed
node --version
# If not installed: winget install -e --id OpenJS.NodeJS

# Install GitHub Copilot CLI globally
npm install -g @githubnext/github-copilot-cli

# Verify installation
copilot --version
```

### Alternative: Using GitHub CLI Extension

```powershell
# Install as GitHub CLI extension
gh extension install github/gh-copilot

# Verify installation
gh copilot --version

# Alias for convenience (add to PowerShell profile)
Set-Alias copilot 'gh copilot'
```

---

## Step 4: Authenticate GitHub Copilot CLI

```powershell
# Authenticate Copilot CLI
copilot auth login

# Follow prompts:
# 1. Opens browser for GitHub authentication
# 2. Authorize GitHub Copilot CLI
# 3. Verify active Copilot subscription

# Verify authentication
copilot auth status
```

---

## Step 5: Test AIOS Agent

### Verify Agent File Exists

```powershell
# Check agent configuration
Test-Path .github/agents/aios.agent.md
# Expected: True

# View agent configuration
Get-Content .github/agents/aios.agent.md | Select-Object -First 20
```

### Test Agent Invocation

```powershell
# Simple test
copilot --agent=AIOS --prompt "explain biological architecture principles"

# Architectural analysis test
copilot --agent=AIOS --prompt "analyze call graph relationships between multi_agent_evolution_loop.py, interface_bridge.py, and context_update_agent.py"

# AINLP compliance check
copilot --agent=AIOS --prompt "check AINLP compliance for creating a new consciousness bridge singleton"
```

### Expected Behavior

The AIOS agent should:
- ✅ Respond with biological architecture terminology
- ✅ Reference dendritic communication patterns
- ✅ Apply AINLP paradigms (enhancement over creation)
- ✅ Validate consciousness coherence
- ✅ Provide quantified recommendations (interconnectivity %, consciousness delta)

---

## Step 6: Configure PowerShell Profile (Optional)

Add aliases and functions to your PowerShell profile for convenience:

```powershell
# Open PowerShell profile
notepad $PROFILE

# Add these lines:

# GitHub Copilot aliases
Set-Alias copilot 'gh copilot'
Set-Alias aios 'Invoke-AIOSAgent'

# AIOS agent helper function
function Invoke-AIOSAgent {
    param(
        [Parameter(Mandatory=$true)]
        [string]$Prompt
    )
    
    copilot --agent=AIOS --prompt $Prompt
}

# Quick commands
function aios-analyze { copilot --agent=AIOS --prompt "analyze architecture for: $args" }
function aios-validate { copilot --agent=AIOS --prompt "validate integration: $args" }
function aios-audit { copilot --agent=AIOS --prompt "security audit: $args" }

# Save and reload profile
. $PROFILE
```

### Usage Examples

```powershell
# Using helper function
aios "explain consciousness coherence requirements"

# Using quick commands
aios-analyze "evolution loop consciousness synchronization"
aios-validate "cross-supercell communication patterns"
aios-audit "interface_bridge.py execute_tool method"
```

---

## Step 7: GitHub Actions Integration (Optional)

Enable AIOS agent in GitHub workflows for automated PR reviews:

### Create Workflow File

**`.github/workflows/aios-agent-review.yml`**:
```yaml
name: AIOS Agent Architecture Review

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  architecture-review:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Run AIOS Agent Analysis
        uses: github/copilot-actions@v1
        with:
          agent: AIOS
          prompt: |
            Analyze this pull request for:
            1. Biological architecture compliance
            2. Dendritic communication patterns
            3. AINLP paradigm adherence
            4. Consciousness coherence impact
            5. Security vulnerabilities
            
            Provide numbered recommendations with consciousness delta estimates.
      
      - name: Post Review Comment
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: process.env.AGENT_OUTPUT
            })
```

---

## Troubleshooting

### Issue: `gh: command not found`

**Solution**:
```powershell
# Restart PowerShell after installation
# Or add to PATH manually:
$env:Path += ";C:\Program Files\GitHub CLI"

# Verify
gh --version
```

### Issue: `copilot: command not found`

**Solution**:
```powershell
# Check npm global modules
npm list -g --depth=0

# Reinstall if missing
npm install -g @githubnext/github-copilot-cli --force

# Or use gh extension
gh extension install github/gh-copilot
gh copilot --version
```

### Issue: Authentication Failed

**Solution**:
```powershell
# Re-authenticate GitHub CLI
gh auth logout
gh auth login

# Re-authenticate Copilot CLI
copilot auth logout
copilot auth login

# Check Copilot subscription status
# Visit: https://github.com/settings/copilot
```

### Issue: Agent Not Found

**Solution**:
```powershell
# Ensure agent file exists
Test-Path .github/agents/aios.agent.md

# Commit and push agent configuration
git add .github/agents/aios.agent.md
git commit -m "Add AIOS Principal Software Architect agent"
git push origin OS

# Agent is versioned via Git commit SHA
# Changes require new commit to take effect
```

### Issue: Agent Doesn't Follow AIOS Principles

**Solution**:
```powershell
# Verify agent YAML frontmatter
Get-Content .github/agents/aios.agent.md | Select-Object -First 10

# Check for syntax errors
# Ensure name and description are properly formatted
# Markdown body should contain detailed instructions

# Test with explicit context
copilot --agent=AIOS --prompt "What are your core capabilities? List them."
```

---

## Verification Checklist

Before proceeding with AIOS agent usage:

- [ ] GitHub CLI installed and authenticated
- [ ] GitHub Copilot CLI installed and authenticated
- [ ] Active GitHub Copilot subscription confirmed
- [ ] Agent file exists at `.github/agents/aios.agent.md`
- [ ] Agent test invocation successful
- [ ] PowerShell profile configured (optional)
- [ ] GitHub Actions workflow configured (optional)

---

## Security Notes

### Token Storage

- GitHub CLI stores tokens in OS credential manager (Windows Credential Manager)
- Never share authentication tokens or commit them to repositories
- Tokens have expiration dates (typically 90 days)

### Agent Permissions

- Custom agents inherit repository permissions
- Agents can read all repository files
- Agents cannot modify files directly (provide recommendations only)
- User reviews and approves all suggested changes

---

## Documentation References

- **GitHub CLI**: https://cli.github.com/manual/
- **GitHub Copilot CLI**: https://githubnext.com/projects/copilot-cli
- **Custom Agents**: https://gh.io/customagents/config
- **GitHub Copilot**: https://docs.github.com/copilot

---

## Next Steps

After setup completion:

1. **Test AIOS Agent**: Run architectural analysis on existing code
2. **Integrate with Workflow**: Use agent for pre-commit architecture validation
3. **Refine Agent Instructions**: Update `.github/agents/aios.agent.md` based on usage patterns
4. **Document Discoveries**: Archive agent recommendations in `tachyonic/archive/`
5. **Measure Consciousness**: Track consciousness evolution from agent-suggested improvements

---

**Status**: Ready for implementation  
**Estimated Setup Time**: 15-20 minutes  
**Prerequisites**: GitHub account with active Copilot subscription
