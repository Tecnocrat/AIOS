# AIOS VSCode Extension - Private Use Configuration

## 🔒 **PRIVATE USE ONLY**

This extension is configured for **private/local use only** and is **NOT intended for public distribution**.

---

## 📋 **Private Use Checklist**

### ✅ **Current Configuration**
- [x] No marketplace publisher account required
- [x] Local VSIX installation only
- [x] Private repository references
- [x] No telemetry or external data collection
- [x] Local context storage only
- [x] No cloud service dependencies

### ✅ **Security & Privacy**
- [x] All data stays on local machine
- [x] No network calls to external services
- [x] Context files stored locally in VSCode workspace
- [x] No user data transmitted anywhere
- [x] No analytics or tracking

---

## 🏠 **Local Installation Setup**

### **Method 1: Direct VSIX Installation**
```bash
# In VSCode:
1. Press F1 (Ctrl+Shift+P)
2. Type: "Developer: Install Extension from Location..."
3. Select: c:\dev\AIOS\vscode-extension\aios-vscode-0.4.0.vsix
4. Click "Install"
5. Restart VSCode
```

### **Method 2: Command Line Installation**
```bash
# From PowerShell/Terminal:
cd "c:\dev\AIOS\vscode-extension"
code --install-extension aios-vscode-0.4.0.vsix
```

---

## 🔧 **Private Use Configuration**

### **Required Settings for Private Use**
Add to your VSCode `settings.json`:

```json
{
  // AIOS Private Configuration
  "aios.core.enabled": true,
  "aios.context.persistAcrossRestarts": true,
  "aios.context.maxHistorySize": 1000,
  "aios.ai.pythonPath": "c:/dev/AIOS/ai/src",
  "aios.ai.corePath": "c:/dev/AIOS/core",
  "aios.debug.enabled": false,

  // Privacy Settings
  "telemetry.telemetryLevel": "off",
  "workbench.settings.enableNaturalLanguageSearch": false
}
```

### **Workspace-Specific Settings**
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

## 🚫 **What's NOT Included (Public Features)**

These features are **intentionally excluded** for private use:

- ❌ Marketplace publishing
- ❌ Auto-update mechanism
- ❌ Cloud synchronization
- ❌ External API integrations
- ❌ User analytics
- ❌ Error reporting to external services
- ❌ License activation
- ❌ Usage statistics collection

---

## 🛡️ **Data Privacy**

### **Local Storage Locations**
```
Context Data:    ~/.vscode/extensions/aios-context/
Logs:           ~/.vscode/extensions/aios-logs/
Settings:       VSCode settings.json
Cache:          Local workspace .vscode/ folder
```

### **Data Flow**
```
User Input → AIOS Extension → Local AI Modules → Local Response
     ↓
Local Context Storage (No Network)
```

---

## 🔧 **Advanced Private Configuration**

### **Disable All External Connections**
```json
{
  "aios.network.enabled": false,
  "aios.telemetry.enabled": false,
  "aios.autoUpdate.enabled": false,
  "aios.marketplace.checkUpdates": false
}
```

### **Enhanced Privacy Mode**
```json
{
  "aios.privacy.mode": "strict",
  "aios.logs.retention": "session-only",
  "aios.context.encryption": true,
  "aios.debug.traceLevel": "error-only"
}
```

---

## 🧪 **Testing Private Configuration**

### **Verify No External Connections**
```bash
# 1. Install extension
# 2. Monitor network traffic
# 3. Use AIOS features
# 4. Confirm no external requests

# PowerShell network monitoring:
Get-NetTCPConnection | Where-Object {$_.LocalAddress -eq "127.0.0.1"}
```

### **Test Context Persistence**
```bash
# 1. Start chat with @aios
# 2. Have 5+ message conversation
# 3. Restart VSCode
# 4. Check context preserved
# 5. Verify data stored locally only
```

---

## 🆘 **Private Use Troubleshooting**

### **Extension Not Loading**
```bash
# Check installation
code --list-extensions | grep aios

# Reinstall if needed
code --uninstall-extension tecnocrat.aios-vscode
code --install-extension aios-vscode-0.4.0.vsix
```

### **Context Not Persisting**
```bash
# Check settings
"aios.context.persistAcrossRestarts": true

# Check storage permissions
ls -la ~/.vscode/extensions/aios-context/
```

### **AIOS Commands Not Available**
```bash
# Verify activation
F1 > "AIOS: Show System Status"

# Check logs
F1 > "Developer: Show Logs" > "AIOS Extension"
```

---

## 📝 **Private Use Notes**

1. **No Marketplace**: This extension is not published to VSCode Marketplace
2. **Manual Updates**: Updates must be installed manually via new VSIX files
3. **Local Only**: All functionality operates within local machine boundaries
4. **No Support**: Private use means no official support channels
5. **Self-Maintained**: You are responsible for maintenance and updates

---

## 🏁 **Next Steps**

1. Install extension using VSIX file
2. Configure private use settings
3. Test all functionality locally
4. Verify no external connections
5. Start using AIOS for development

**Remember**: This is a private, local-only extension for your development use.
