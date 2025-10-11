# Gemini API Setup Guide

## 🌟 Why Gemini?

Gemini provides access to Google's powerful AI models, including:
- **gemini-pro**: Advanced reasoning and code generation
- **High rate limits**: Much more generous than other free options
- **Fast responses**: Low latency
- **Free tier**: Generous free quota for development

## 📋 Setup Steps

### 1. Get Your API Key

1. Visit: https://aistudio.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your API key

### 2. Install Required Package

```powershell
pip install google-generativeai
```

### 3. Set Environment Variable

**Option A: Set for current PowerShell session**
```powershell
$env:GEMINI_API_KEY = "your-api-key-here"
```

**Option B: Set permanently (Windows)**
```powershell
[System.Environment]::SetEnvironmentVariable('GEMINI_API_KEY', 'your-api-key-here', 'User')
```

**Option C: Create .env file** (recommended for development)
```
# Create .env file in C:\dev\AIOS\
GEMINI_API_KEY=your-api-key-here
```

### 4. Test Your Setup

```powershell
python -c "import os; import google.generativeai as genai; genai.configure(api_key=os.environ['GEMINI_API_KEY']); model = genai.GenerativeModel('gemini-pro'); response = model.generate_content('Say hello'); print('✅ Gemini works!', response.text)"
```

## 🔧 Integration with AIOS

The Gemini bridge is now integrated into the library code generation loop:

```python
from integrations.gemini_bridge.gemini_evolution_bridge import GeminiEvolutionBridge

# Initialize
bridge = GeminiEvolutionBridge()

# Generate code
code = await bridge.generate_code(
    prompt="Create a Python function that...",
    temperature=0.7,
    max_tokens=2000
)
```

## 🚀 Usage with Library Generation

Once set up, Gemini will be automatically used by the library code generation loop:

```python
loop = LibraryCodeGenerationLoop(
    use_ollama=True,   # Will use Ollama if available
    use_gemini=True    # Will use Gemini if available
)

results = await loop.run_complete_cycle(
    library_name='aios_core',
    task_description='Create a consciousness-driven data processor',
    generation_size=3
)
```

## 🔍 Verification

Check if Gemini is available:
```powershell
python -c "import os; print('✅ API Key set' if os.environ.get('GEMINI_API_KEY') else '❌ No API key'); import google.generativeai; print('✅ Package installed')"
```

## 🎯 Next Steps

1. Install Ollama for dual-agent setup (optional but recommended)
2. Test with `python test_library_generation.py`
3. Check generated code in `evolution_lab/library_generations/`

## 📚 Resources

- [Gemini API Documentation](https://ai.google.dev/docs)
- [Get API Key](https://aistudio.google.com/app/apikey)
- [Python SDK](https://github.com/google/generative-ai-python)
