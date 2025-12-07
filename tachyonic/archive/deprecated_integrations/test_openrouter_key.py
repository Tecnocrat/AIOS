"""Quick test of OpenRouter API key"""
import requests
import os

# Load API key from Windows User PATH environment variable
api_key = os.getenv('DEEPSEEK_API_KEY')

# Validation
if not api_key:
    raise ValueError(
        "DEEPSEEK_API_KEY not found in environment variables.\n"
        "Please set it in Windows User Environment Variables:\n"
        "  1. Press Win+X → System → Advanced → Environment Variables\n"
        "  2. Under 'User variables', click 'New...'\n"
        "  3. Variable name: DEEPSEEK_API_KEY\n"
        "  4. Variable value: your-regenerated-key\n"
        "  5. Click OK and restart terminal/VS Code"
    )

print("Testing OpenRouter API key...")
print(f"Key loaded from environment: {api_key[:15]}...{api_key[-10:]}")

# Test with a simple request
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

test_data = {
    "model": "deepseek/deepseek-chat",
    "messages": [
        {"role": "user", "content": "Say hello"}
    ],
    "max_tokens": 10
}

try:
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=test_data,
        timeout=10
    )
    
    print(f"\nStatus Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        print("\n✅ API KEY IS VALID!")
    elif response.status_code == 401:
        print("\n❌ API KEY IS INVALID OR EXPIRED")
        print("\nTo get a new key:")
        print("1. Go to: https://openrouter.ai/keys")
        print("2. Log in with your account")
        print("3. Create a new API key")
        print("4. Update vscode-extension\\.env with new key")
    else:
        print(f"\n⚠️ Unexpected response: {response.status_code}")
        
except Exception as e:
    print(f"\n❌ Error testing API key: {e}")
