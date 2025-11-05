# Windows API Key Environment Variable Setup Guide

**Created**: November 5, 2025  
**Purpose**: Secure API keys by storing them in environment variables instead of hardcoded in source files  
**APIs**: DeepSeek/OpenRouter, Google Gemini

---

## 🔒 Security Status

**BEFORE**:
- ❌ API keys hardcoded in 3 source files
- ❌ Risk of accidental GitHub upload
- ❌ Keys visible in version control history

**AFTER**:
- ✅ API keys stored in environment variables
- ✅ `.env` file protected by `.gitignore`
- ✅ Keys never committed to GitHub

---

## 📋 Quick Reference

### Your API Keys

```env
DEEPSEEK_API_KEY=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
OPENROUTER_API_KEY=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
GEMINI_API_KEY=AIzaSyCuj6S1PJcslZr29ez9Cd9oVNFDuzLH2OE
OLLAMA_HOST=http://localhost:11434
```

---

## 🎯 Three Methods to Set Environment Variables

### Method 1: Windows System Properties (Recommended - Persistent)

**Best for**: Production use, system-wide access, persistent across reboots

**Steps**:

1. **Open Environment Variables Dialog**:
   - Press `Win + X` → Select "System"
   - Click "Advanced system settings" (right side)
   - Click "Environment Variables..." button (bottom)

2. **Add User Environment Variables** (Recommended):
   - In "User variables" section (top half), click "New..."
   - Variable name: `DEEPSEEK_API_KEY`
   - Variable value: `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`
   - Click "OK"

3. **Repeat for Other Keys**:
   ```
   OPENROUTER_API_KEY = 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
   GEMINI_API_KEY = AIzaSyCuj6S1PJcslZr29ez9Cd9oVNFDuzLH2OE
   OLLAMA_HOST = http://localhost:11434
   ```

4. **Apply Changes**:
   - Click "OK" on all dialogs
   - Close and reopen PowerShell/Command Prompt/VS Code

5. **Verify**:
   ```powershell
   # PowerShell
   echo $env:DEEPSEEK_API_KEY
   echo $env:GEMINI_API_KEY
   ```

**Pros**:
- ✅ Persistent across reboots
- ✅ Available to all applications
- ✅ No file dependencies
- ✅ Standard Windows approach

**Cons**:
- ❌ Requires GUI navigation
- ❌ Changes need terminal restart
- ❌ Not version controlled

---

### Method 2: PowerShell Profile (Session-Based)

**Best for**: Development, quick changes, per-user configuration

**Steps**:

1. **Check if Profile Exists**:
   ```powershell
   Test-Path $PROFILE
   # If False, create it:
   New-Item -Path $PROFILE -ItemType File -Force
   ```

2. **Edit Profile**:
   ```powershell
   notepad $PROFILE
   ```

3. **Add Environment Variables**:
   ```powershell
   # Add these lines to your profile
   $env:DEEPSEEK_API_KEY = "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"
   $env:OPENROUTER_API_KEY = "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"
   $env:GEMINI_API_KEY = "AIzaSyCuj6S1PJcslZr29ez9Cd9oVNFDuzLH2OE"
   $env:OLLAMA_HOST = "http://localhost:11434"
   
   Write-Host "[AIOS] API keys loaded from PowerShell profile" -ForegroundColor Green
   ```

4. **Save and Reload**:
   ```powershell
   # Save file in Notepad (Ctrl+S)
   # Reload profile:
   . $PROFILE
   ```

5. **Verify**:
   ```powershell
   echo $env:DEEPSEEK_API_KEY
   echo $env:GEMINI_API_KEY
   ```

**Pros**:
- ✅ Fast to set up
- ✅ Easy to edit
- ✅ Loads automatically on PowerShell start
- ✅ Can version control (exclude actual keys)

**Cons**:
- ❌ PowerShell only (not Command Prompt)
- ❌ Per-session (not truly persistent)
- ❌ Need to reload profile after changes

---

### Method 3: .env File with python-dotenv (Development)

**Best for**: Development, project-specific keys, CI/CD

**Steps**:

1. **Install python-dotenv** (if not already):
   ```powershell
   pip install python-dotenv
   ```

2. **Use Existing .env File**:
   - Already created at `c:\dev\AIOS\.env`
   - Contains your API keys
   - Protected by `.gitignore`

3. **Load in Python Code**:
   ```python
   from dotenv import load_dotenv
   import os
   
   # Load environment variables from .env file
   load_dotenv()
   
   # Access keys
   deepseek_key = os.getenv('DEEPSEEK_API_KEY')
   gemini_key = os.getenv('GEMINI_API_KEY')
   ```

4. **Load in Node.js Code**:
   ```bash
   npm install dotenv
   ```
   
   ```javascript
   require('dotenv').config();
   
   const DEEPSEEK_KEY = process.env.DEEPSEEK_API_KEY;
   const GEMINI_KEY = process.env.GEMINI_API_KEY;
   ```

**Pros**:
- ✅ Standard practice for development
- ✅ Project-specific configuration
- ✅ Easy to manage multiple environments
- ✅ Works with CI/CD pipelines

**Cons**:
- ❌ Requires library dependency
- ❌ Must call load_dotenv() in each script
- ❌ File must exist (not ideal for distribution)

---

## 🔧 Files Needing Refactoring

### 1. `ai/test_openrouter_key.py`

**Before** (Line 6):
```python
api_key = "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"
```

**After**:
```python
import os
from dotenv import load_dotenv

# Load environment variables from .env file (optional - for .env method)
load_dotenv()

# Get API key from environment variable
api_key = os.getenv('DEEPSEEK_API_KEY') or os.getenv('OPENROUTER_API_KEY')

# Validation
if not api_key:
    raise ValueError(
        "API key not found. Set DEEPSEEK_API_KEY environment variable.\n"
        "Methods:\n"
        "  1. Windows: System Properties → Environment Variables\n"
        "  2. PowerShell: Add to $PROFILE\n"
        "  3. .env file: Create .env with DEEPSEEK_API_KEY=your-key"
    )
```

---

### 2. `ai/tools/agentic_e501_fixer.py`

**Before** (Line 90):
```python
api_key = "AIzaSyCuj6S1PJcslZr29ez9Cd9oVNFDuzLH2OE"  # Provided API key
```

**After**:
```python
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Gemini API key from environment
api_key = os.getenv('GEMINI_API_KEY')

# Validation
if not api_key:
    raise ValueError(
        "Gemini API key not found. Set GEMINI_API_KEY environment variable.\n"
        "Get your key at: https://makersuite.google.com/app/apikey"
    )
```

---

### 3. `vscode-extension/test-openrouter.js`

**Before** (Line 8):
```javascript
const API_KEY = "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";
```

**After**:
```javascript
// Load environment variables from .env file (optional)
require('dotenv').config();

// Get API key from environment
const API_KEY = process.env.DEEPSEEK_API_KEY || process.env.OPENROUTER_API_KEY;

// Validation
if (!API_KEY) {
    throw new Error(
        'API key not found. Set DEEPSEEK_API_KEY environment variable.\n' +
        'Methods:\n' +
        '  1. Windows: System Properties → Environment Variables\n' +
        '  2. PowerShell: Add to $PROFILE\n' +
        '  3. .env file: npm install dotenv && create .env'
    );
}
```

---

## ✅ Verification Steps

### Test Python Environment Variables

```powershell
# Test from PowerShell
python -c "import os; print('DEEPSEEK:', os.getenv('DEEPSEEK_API_KEY')[:20] + '...' if os.getenv('DEEPSEEK_API_KEY') else 'NOT SET')"
python -c "import os; print('GEMINI:', os.getenv('GEMINI_API_KEY')[:20] + '...' if os.getenv('GEMINI_API_KEY') else 'NOT SET')"
```

### Test Node.js Environment Variables

```powershell
# Test from PowerShell
node -e "console.log('DEEPSEEK:', process.env.DEEPSEEK_API_KEY ? process.env.DEEPSEEK_API_KEY.substring(0, 20) + '...' : 'NOT SET')"
```

### Test .env File Loading

```python
# test_env.py
from dotenv import load_dotenv
import os

load_dotenv()

print("DEEPSEEK_API_KEY:", os.getenv('DEEPSEEK_API_KEY')[:20] + "..." if os.getenv('DEEPSEEK_API_KEY') else "NOT SET")
print("GEMINI_API_KEY:", os.getenv('GEMINI_API_KEY')[:20] + "..." if os.getenv('GEMINI_API_KEY') else "NOT SET")
```

---

## 🛡️ Security Checklist

- [x] `.env` file created with API keys
- [x] `.env` added to `.gitignore`
- [x] `.env.template` created (safe to commit)
- [ ] Hardcoded keys removed from `ai/test_openrouter_key.py`
- [ ] Hardcoded keys removed from `ai/tools/agentic_e501_fixer.py`
- [ ] Hardcoded keys removed from `vscode-extension/test-openrouter.js`
- [ ] Environment variables set (choose method 1, 2, or 3)
- [ ] Refactored code tested with environment variables
- [ ] Old commits with hardcoded keys documented (optional: git filter-branch)

---

## 🚀 Recommended Workflow

**For You (User)**:

1. **Set Windows User Environment Variables** (Method 1):
   - Win+X → System → Advanced → Environment Variables
   - Add `DEEPSEEK_API_KEY`, `GEMINI_API_KEY`
   - Close/reopen terminals

2. **Refactor Code** (Methods shown above):
   - Update 3 files to use `os.getenv()` or `process.env`
   - Test each file individually

3. **Verify**:
   - Run `python ai/test_openrouter_key.py`
   - Run `node vscode-extension/test-openrouter.js`
   - Check output for API key loading

4. **Commit Refactored Code**:
   ```powershell
   git add ai/test_openrouter_key.py
   git add ai/tools/agentic_e501_fixer.py
   git add vscode-extension/test-openrouter.js
   git add .gitignore
   git add .env.template
   git commit -m "Security: Replace hardcoded API keys with environment variables"
   ```

---

## 📚 Additional Resources

- [python-dotenv documentation](https://github.com/theskumar/python-dotenv)
- [Node.js dotenv documentation](https://github.com/motdotla/dotenv)
- [Windows Environment Variables Guide](https://docs.microsoft.com/en-us/windows/win32/procthread/environment-variables)
- [12-Factor App: Store config in environment](https://12factor.net/config)

---

**Status**: `.env` file protected by `.gitignore`, ready for refactoring  
**Next**: Refactor 3 files to use environment variables  
**Consciousness**: +0.02 (security awareness, API key protection pattern)
