#!/usr/bin/env python3
"""Test OpenRouter API key configuration"""

import os
import httpx

def test_openrouter_key():
    """Validate OpenRouter API key setup."""
    
    # Check environment variable
    key = os.environ.get("OPENROUTER_API_KEY")
    
    print("=" * 70)
    print("OpenRouter API Key Validation")
    print("=" * 70)
    
    if not key:
        print("❌ ERROR: OPENROUTER_API_KEY environment variable not set")
        print("\nTo set it:")
        print("  PowerShell: $env:OPENROUTER_API_KEY = 'your-key-here'")
        print("  Bash: export OPENROUTER_API_KEY='your-key-here'")
        return False
    
    print(f"✅ Environment variable set")
    print(f"   Length: {len(key)} characters")
    print(f"   Prefix: {key[:15]}...")
    print(f"   Format: {'✅ Valid' if key.startswith('sk-or-v1-') else '❌ Invalid (should start with sk-or-v1-)'}")
    
    # Test with auth endpoint
    print("\nTesting authentication...")
    try:
        resp = httpx.get(
            "https://openrouter.ai/api/v1/auth/key",
            headers={"Authorization": f"Bearer {key}"},
            timeout=10
        )
        
        print(f"Status Code: {resp.status_code}")
        
        if resp.status_code == 200:
            data = resp.json()
            print("✅ API key is VALID")
            print(f"   Label: {data.get('data', {}).get('label', 'N/A')}")
            print(f"   Limit: ${data.get('data', {}).get('limit', 'N/A')}")
            print(f"   Usage: ${data.get('data', {}).get('usage', 'N/A')}")
            return True
        elif resp.status_code == 401:
            print("❌ API key is INVALID or REVOKED")
            print(f"   Response: {resp.text}")
            print("\n🔧 Solution:")
            print("   1. Go to: https://openrouter.ai/settings/keys")
            print("   2. Generate a new API key")
            print("   3. Copy the key")
            print("   4. In PowerShell: $env:OPENROUTER_API_KEY = 'your-new-key'")
            print("   5. Verify it persists: echo $env:OPENROUTER_API_KEY")
            return False
        else:
            print(f"⚠️ Unexpected status: {resp.status_code}")
            print(f"   Response: {resp.text}")
            return False
            
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

if __name__ == "__main__":
    success = test_openrouter_key()
    exit(0 if success else 1)
