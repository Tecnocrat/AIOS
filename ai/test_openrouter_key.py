"""Quick test of OpenRouter API key"""
import requests
import os

# Your current API key from .env
api_key = "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"

print("Testing OpenRouter API key...")
print(f"Key: {api_key[:15]}...{api_key[-10:]}")

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
