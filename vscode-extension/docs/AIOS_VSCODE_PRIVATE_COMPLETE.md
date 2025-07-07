# AIOS VSCode Extension - Complete Private Use Guide

## 🔒 **PRIVATE USE ONLY - CRITICAL SETUP**

This extension is **exclusively for private/local use** and solves the critical chat iteration reset problem in AI-assisted VSCode development.

---

## 🚨 **Problem Solved**

**Before**: VSCode restarts → AI chat context lost → Development continuity broken
**After**: VSCode restarts → AI chat context preserved → Seamless development experience

---

## 🎯 **Quick Start (1 Minute)**

### **Step 1: Install Extension**
```powershell
# Option A: PowerShell Automated Setup
cd "c:\dev\AIOS\vscode-extension"
.\setup-private.ps1 -All

# Option B: Manual Installation
# 1. Open VSCode
# 2. Press F1 → "Developer: Install Extension from Location..."
# 3. Select: c:\dev\AIOS\vscode-extension\aios-vscode-0.4.0.vsix
# 4. Restart VSCode
```

### **Step 2: Verify Installation**
```powershell
# Check extension is installed
code --list-extensions | grep aios

# Test AIOS commands
# F1 → Type "AIOS" → Should see AIOS commands
```

### **Step 3: Test Context Persistence**
```powershell
# 1. Open VSCode chat (Ctrl+Shift+P → "Chat: Open Chat")
# 2. Type: @aios Hello, remember this conversation
# 3. Have 5+ message conversation
# 4. Restart VSCode
# 5. ✅ Context should be preserved
```

---

## 🔧 **Private Use Configuration**

### **Automated Configuration**
```powershell
# Complete private setup
cd "c:\dev\AIOS\vscode-extension"
.\setup-private.ps1 -All

# Individual steps
.\setup-private.ps1 -Install      # Install extension
.\setup-private.ps1 -Configure    # Configure settings
.\setup-private.ps1 -Test         # Test configuration
```

### **Manual Configuration**
Add to your VSCode `settings.json`:
```json
{
  "aios.core.enabled": true,
  "aios.context.persistAcrossRestarts": true,
  "aios.context.maxHistorySize": 1000,
  "aios.ai.pythonPath": "c:/dev/AIOS/ai/src",
  "aios.ai.corePath": "c:/dev/AIOS/core",
  "aios.debug.enabled": false,
  "aios.privacy.mode": "strict",
  "aios.network.enabled": false,
  "aios.telemetry.enabled": false,
  "aios.autoUpdate.enabled": false,
  "aios.marketplace.checkUpdates": false,
  "aios.logs.retention": "session-only",
  "aios.context.encryption": true,
  "aios.debug.traceLevel": "error-only",
  "telemetry.telemetryLevel": "off"
}
```

---

## 🚀 **Usage Examples**

### **Basic Chat with Context Preservation**
```
User: @aios Help me understand the AIOS project structure
AIOS: [Analyzes workspace and provides detailed explanation]

User: What about the C++ core?
AIOS: [Continues with context about previous discussion]

# Restart VSCode
User: Continue our discussion about the C++ core
AIOS: [Remembers previous conversation and continues]
```

### **AIOS Commands**
```
@aios /status      # Show system status
@aios /reset       # Reset conversation context
@aios /save        # Save current context
@aios /load        # Load saved context
@aios /help        # Show available commands
```

### **Development Workflow**
```
# 1. Start development session
@aios Review this TypeScript code for improvements

# 2. Continue working
@aios Now explain how this connects to the Python modules

# 3. Restart VSCode (context preserved)
@aios Based on our previous discussion, what's next?
```

---

## 🔐 **Privacy & Security**

### **What's Private**
- ✅ All data stays on local machine
- ✅ No network calls to external services
- ✅ Context stored locally only
- ✅ No telemetry or analytics
- ✅ No cloud synchronization
- ✅ No external API calls

### **Data Storage Locations**
```
Context:     ~/.vscode/extensions/aios-context/
Logs:        ~/.vscode/extensions/aios-logs/
Settings:    VSCode settings.json
Cache:       Local workspace .vscode/ folder
```

### **Security Validation**
```powershell
# Check no external connections
Get-NetTCPConnection | Where-Object {$_.State -eq "Established"}

# Verify private settings
code --list-extensions | grep aios
```

---

## 🛠️ **Advanced Features**

### **Context Management**
```
F1 → "AIOS: Save Context"     # Manual save
F1 → "AIOS: Load Context"     # Manual load
F1 → "AIOS: Reset Context"    # Clear all context
F1 → "AIOS: Show Status"      # System status
```

### **Multi-Language AI Integration**
```
@aios Explain how the C++ core communicates with Python AI modules
@aios Show me the data flow between TypeScript UI and C++ backend
@aios Help me optimize the Python AI processing pipeline
```

### **Workspace-Specific Configuration**
Create `.vscode/settings.json` in your project:
```json
{
  "aios.core.enabled": true,
  "aios.context.persistAcrossRestarts": true,
  "aios.ai.pythonPath": "./ai/src",
  "aios.ai.corePath": "./core",
  "aios.debug.enabled": true
}
```

---

## 🧪 **Testing & Validation**

### **Test Context Persistence**
```powershell
# 1. Start chat session
@aios Remember: We're working on the AIOS project

# 2. Add context
@aios The main goal is to solve chat iteration reset

# 3. Continue conversation
@aios We've implemented persistent context management

# 4. Restart VSCode
@aios What were we discussing about the AIOS project?
# Expected: Should remember the conversation
```

### **Test Private Configuration**
```powershell
# Run configuration test
cd "c:\dev\AIOS\vscode-extension"
.\setup-private.ps1 -Test

# Check network isolation
# No external connections should be made
```

---

## 🆘 **Troubleshooting**

### **Extension Not Loading**
```powershell
# Reinstall extension
code --uninstall-extension tecnocrat.aios-vscode
code --install-extension aios-vscode-0.4.0.vsix

# Check activation
F1 → "Developer: Show Running Extensions"
```

### **Context Not Persisting**
```powershell
# Check settings
"aios.context.persistAcrossRestarts": true

# Verify storage
ls "$env:USERPROFILE\.vscode\extensions\aios-context"
```

### **AIOS Commands Missing**
```powershell
# Check extension status
F1 → "AIOS: Show System Status"

# View logs
F1 → "Developer: Show Logs" → "AIOS Extension"
```

### **Settings Not Applied**
```powershell
# Open settings
F1 → "Preferences: Open Settings (JSON)"

# Verify AIOS settings are present
# Look for "aios.privacy.mode": "strict"
```

---

## 📋 **Maintenance**

### **Updates**
```powershell
# Manual update process (no auto-update)
1. Download new VSIX file
2. Uninstall old version
3. Install new version
4. Reconfigure settings
```

### **Backup Context**
```powershell
# Manual backup
F1 → "AIOS: Save Context"
# Copy: ~/.vscode/extensions/aios-context/
```

### **Clean Installation**
```powershell
# Complete clean install
code --uninstall-extension tecnocrat.aios-vscode
Remove-Item "$env:USERPROFILE\.vscode\extensions\aios-*" -Recurse -Force
cd "c:\dev\AIOS\vscode-extension"
.\setup-private.ps1 -All
```

---

## 🏁 **Success Checklist**

- [ ] Extension installed from VSIX
- [ ] Private settings configured
- [ ] Context persistence working
- [ ] No external connections
- [ ] AIOS commands available
- [ ] Chat integration working
- [ ] Settings validation passed
- [ ] Logs showing private mode

---

## 📞 **Support**

**Remember**: This is a private extension for personal use only.

- Check logs: F1 → "Developer: Show Logs" → "AIOS Extension"
- Review settings: F1 → "Preferences: Open Settings" → Search "aios"
- Test configuration: `.\setup-private.ps1 -Test`

**Extension Location**: `c:\dev\AIOS\vscode-extension\aios-vscode-0.4.0.vsix`

---

## 🎉 **You're Ready!**

Your AIOS VSCode extension is now configured for private use with persistent context. The critical chat iteration reset problem is solved!

**Next Steps**:
1. Start coding with @aios
2. Experience seamless context preservation
3. Enjoy uninterrupted AI-assisted development
