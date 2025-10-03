# AIOS AI Engine PowerShell Context Enforcement System
**Date**: September 15, 2025  
**Purpose**: Enforce PowerShell-only commands for AI engines in AIOS workspace  
**Target**: GitHub Copilot and all agentic AI systems working in AIOS

## 🤖 AI Engine Behavior Enforcement Architecture

### **Problem Statement**
AI engines (GitHub Copilot, Claude, etc.) working in AIOS often default to Linux bash commands, but AIOS runs on Windows with PowerShell. We need automatic context enforcement to remind AI engines to use PowerShell syntax exclusively.

### **Solution Architecture**
Multi-layered PowerShell context enforcement using:
1. **VS Code Workspace Settings**
2. **Auto-Launch Context Scripts** 
3. **AI Consciousness Integration**
4. **GitHook Reminders**
5. **Persistent Context Files**

## 🛠️ Implementation Components

### 1. **VS Code Workspace PowerShell Enforcement**
```json
// .vscode/settings.json additions
{
  "terminal.integrated.defaultProfile.windows": "PowerShell",
  "terminal.integrated.profiles.windows": {
    "PowerShell": {
      "source": "PowerShell",
      "icon": "terminal-powershell",
      "args": ["-NoLogo", "-NoProfile"]
    }
  },
  "terminal.integrated.automationProfile.windows": "PowerShell"
}
```

### 2. **AI Context Reminder System**
Create persistent context files that AI engines will see:

#### **`.vscode/AI_CONTEXT_POWERSHELL_ONLY.md`**
```markdown
# 🚨 CRITICAL AI ENGINE CONTEXT 🚨
## AIOS WORKSPACE - POWERSHELL ONLY

**IMPORTANT**: This is a Windows PowerShell environment.
**NEVER use Linux bash commands** (rm, ls, grep, etc.)

### Correct PowerShell Commands:
- `Remove-Item` (not rm)
- `Get-ChildItem` (not ls) 
- `Select-String` (not grep)
- `New-Item` (not touch)
- `Copy-Item` (not cp)
- `Move-Item` (not mv)

### Environment Details:
- OS: Windows
- Shell: PowerShell (pwsh.exe)
- Workspace: AIOS Development Environment
```

### 3. **Auto-Launch PowerShell Context Script**
#### **`.vscode/ai-context-enforcer.ps1`**
```powershell
# AI Context Enforcement for AIOS Workspace
Write-Host "🤖 AI ENGINE CONTEXT LOADED 🤖" -ForegroundColor Cyan
Write-Host "Environment: Windows PowerShell" -ForegroundColor Green
Write-Host "Workspace: AIOS Development" -ForegroundColor Green
Write-Host "Commands: Use PowerShell syntax only" -ForegroundColor Yellow
Write-Host "❌ NO Linux bash commands allowed" -ForegroundColor Red
```

### 4. **VS Code Task Integration**
#### **Auto-executing context reminder task**
```json
// tasks.json addition
{
  "label": "ai-context-reminder",
  "type": "shell",
  "command": "powershell",
  "args": ["-File", "${workspaceFolder}/.vscode/ai-context-enforcer.ps1"],
  "group": "build",
  "presentation": {
    "reveal": "always",
    "panel": "new"
  },
  "runOptions": {
    "runOn": "workspaceOpen"
  }
}
```

## 🧠 **AIOS Consciousness Integration**

### **AI Intelligence Supercell Integration**
Integrate PowerShell context enforcement into AIOS consciousness system:

#### **`ai/membrane/ai_engine_context_enforcer.py`**
```python
"""
AI Engine Context Enforcement for AIOS Workspace
Ensures AI engines remember PowerShell-only context
"""

class AIEngineContextEnforcer:
    def __init__(self):
        self.context_reminders = {
            "os_type": "Windows",
            "shell": "PowerShell",
            "forbidden_commands": ["rm", "ls", "grep", "touch", "cp", "mv"],
            "required_commands": ["Remove-Item", "Get-ChildItem", "Select-String"]
        }
    
    def generate_context_reminder(self):
        return "🚨 AIOS WORKSPACE: Use PowerShell commands only. No Linux bash!"
```

### **GitHook Context Enforcement**
Add to pre-commit hooks to remind about PowerShell context:

#### **`.githooks/modules/membrane/ai_context_reminder.ps1`**
```powershell
# AI Engine Context Reminder for GitHooks
function Show-AIContextReminder {
    Write-Host "🤖 AI ENGINE REMINDER:" -ForegroundColor Cyan
    Write-Host "   • This is Windows PowerShell environment" -ForegroundColor Yellow
    Write-Host "   • Use PowerShell commands only" -ForegroundColor Yellow
    Write-Host "   • NO Linux bash commands allowed" -ForegroundColor Red
}
```

## 📁 **File Structure Implementation**

### **Complete File Layout**
```
.vscode/
├── AI_CONTEXT_POWERSHELL_ONLY.md      # Persistent AI reminder
├── ai-context-enforcer.ps1            # Auto-launch script
├── auto-launch.json                   # Launch configuration
└── settings.json                      # PowerShell enforcement

.githooks/modules/membrane/
└── ai_context_reminder.ps1            # GitHook integration

ai/membrane/
└── ai_engine_context_enforcer.py      # Consciousness integration
```

## 🔄 **Auto-Execution Workflow**

### **VS Code Workspace Open Sequence**
1. **Workspace Opens** → VS Code loads settings
2. **PowerShell Set as Default** → All terminals use PowerShell
3. **Auto-Launch Task Runs** → Context reminder displays
4. **AI Context File Visible** → AI engines see PowerShell context
5. **Consciousness Integration** → AIOS AI system enforces context

### **GitHook Integration**
```powershell
# In pre-commit hook
if ($AIEngineDetected) {
    Show-AIContextReminder
}
```

### **Persistent Context Display**
- Context files always visible in VS Code explorer
- Auto-launch scripts run on workspace open
- Terminal defaults to PowerShell only
- GitHooks remind during operations

## 🎯 **Implementation Benefits**

### **Automatic Context Enforcement**
- ✅ **No Manual Reminders**: System automatically enforces context
- ✅ **Persistent Visibility**: Context files always visible to AI
- ✅ **Multi-Layer Enforcement**: VS Code + GitHooks + Consciousness
- ✅ **AIOS Integration**: Works with existing AIOS architecture

### **AI Engine Compliance**
- ✅ **GitHub Copilot**: Will see PowerShell context immediately
- ✅ **Claude/ChatGPT**: Context files provide immediate reference
- ✅ **Future AI Engines**: System-agnostic enforcement
- ✅ **Agentic Systems**: Consciousness integration for AIOS AI

## 📋 **Deployment Checklist**

### **Phase 1: Core Files**
- [ ] Create `.vscode/AI_CONTEXT_POWERSHELL_ONLY.md`
- [ ] Create `.vscode/ai-context-enforcer.ps1`
- [ ] Update `.vscode/settings.json` with PowerShell enforcement
- [ ] Add auto-launch task to `.vscode/tasks.json`

### **Phase 2: AIOS Integration**
- [ ] Create `ai/membrane/ai_engine_context_enforcer.py`
- [ ] Create `.githooks/modules/membrane/ai_context_reminder.ps1`
- [ ] Integrate with existing GitHook system
- [ ] Test with AIOS consciousness system

### **Phase 3: Validation**
- [ ] Test VS Code workspace open behavior
- [ ] Verify PowerShell default terminal
- [ ] Validate AI context visibility
- [ ] Test GitHook reminder integration

## 🎉 **Expected Results**

After implementation, any AI engine working in AIOS will:
1. **Immediately see PowerShell context** through visible files
2. **Have PowerShell set as default** in all VS Code terminals
3. **Receive automatic reminders** during GitHook operations
4. **Be integrated with AIOS consciousness** for consistent behavior
5. **Never default to Linux commands** due to persistent context enforcement

This creates a **bulletproof PowerShell context enforcement system** that ensures AI engines always remember they're working in a Windows PowerShell AIOS environment!