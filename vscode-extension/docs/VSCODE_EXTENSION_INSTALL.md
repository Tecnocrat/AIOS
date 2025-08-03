# AIOS VSCode Extension - Quick Installation Guide

## 🚨 **Critical Problem Solved**

**Chat Iteration Reset Issue**: VSCode extension restarts cause complete AI chat context loss, breaking development continuity.

**Solution**: AIOS VSCode Extension with persistent context management.

---

## ⚡ **1-Minute Installation**

### **Step 1: Install Extension**
```bash
# Method 1: From VSIX file (Recommended)
1. Open VSCode
2. Press F1 (or Ctrl+Shift+P)
3. Type: "Developer: Install Extension from Location..."
4. Navigate to: c:\dev\AIOS\vscode-extension\aios-vscode-0.4.0.vsix
5. Click "Install"
6. Restart VSCode when prompted
```

### **Step 2: Verify Installation**
```bash
# Check extension is active
1. Press F1
2. Type: "AIOS"
3. You should see AIOS commands available
```

### **Step 3: First Use**
```bash
# Open any chat in VSCode
1. Press Ctrl+Shift+P
2. Type: "Chat: Open Chat"
3. In chat, type: @aios Hello
4. You should get an AIOS response with context preservation info
```

---

## 🧪 **Test Context Persistence**

### **Before AIOS Extension**
```
1. Start chat with AI assistant
2. Have conversation with 5+ messages
3. Restart VSCode
4. ❌ Context is lost, conversation resets
```

### **After AIOS Extension**
```
1. Start chat with @aios
2. Have conversation with 5+ messages
3. Restart VSCode
4. ✅ Context preserved, conversation continues
```

---

## 🎯 **Usage Examples**

### **Basic Chat**
```
@aios Help me understand this AIOS project structure

# Response: AIOS analyzes the workspace context and provides
# detailed explanation with preserved conversation history
```

### **Context Commands**
```
@aios /status       # Show AIOS system status
@aios /reset        # Reset conversation context
@aios /save         # Save current context
@aios /help         # Show all available commands
```

### **Development Assistance**
```
@aios Explain how the C++ core communicates with Python AI modules

# Response: AIOS provides multi-language analysis with
# context of previous discussions about the architecture
```

---

## 🔧 **Configuration**

### **Settings**
Access via: `File > Preferences > Settings > Extensions > AIOS`

```json
{
  "aios.context.persistAcrossRestarts": true,    // Enable context persistence
  "aios.context.maxHistorySize": 1000,          // Max messages to keep
  "aios.debug.enabled": false                   // Enable debug logging
}
```

### **Debug Mode**
```json
{
  "aios.debug.enabled": true
}
```

Then check: `View > Output > AIOS` for detailed logs

---

## 🚨 **Troubleshooting**

### **Extension Not Working**
```bash
# Check installation
1. Go to Extensions (Ctrl+Shift+X)
2. Search for "AIOS"
3. Verify it's enabled

# Check VSCode version
Requires VSCode 1.95.0 or higher
```

### **Context Not Persisting**
```bash
# Check settings
"aios.context.persistAcrossRestarts": true

# Test manually
@aios /save    # Save context
@aios /load    # Load context
```

### **AIOS Connection Issues**
```bash
# Check system status
@aios /status

# Expected response should show:
# - Status: active
# - AI Modules: Active
# - Context Messages: [number]
```

---

## ✅ **Success Verification**

### **Test Checklist**
- [ ] Extension installs without errors
- [ ] `@aios` command responds in chat
- [ ] `/status` shows active system
- [ ] Context persists after VSCode restart
- [ ] Debug logs available in Output panel

### **Expected Benefits**
- ✅ **No Context Loss**: Conversations continue across restarts
- ✅ **Professional Integration**: Native VSCode chat experience
- ✅ **AIOS AI Power**: Multi-language AI coordination
- ✅ **Smart Context**: Automatic optimization and management

---

## 🎉 **Next Steps**

1. **Use AIOS for Development**: Try @aios for code analysis, generation, and architecture questions
2. **Explore Commands**: Use @aios /help to see all available features
3. **Configure Settings**: Customize context size and persistence options
4. **Provide Feedback**: Test extensively and report any issues

---

## 📞 **Support**

**Issues**: Check AIOS Output panel (`View > Output > AIOS`)
**Commands**: `@aios /help` for full command list
**Status**: `@aios /status` for system health
**Reset**: `@aios /reset` if context becomes corrupted

---

**AIOS VSCode Extension** - Your AI development companion with memory that never forgets.
