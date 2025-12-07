#!/usr/bin/env python3
"""
GitHub Models API Setup for AIOS - Free GPT-4o Access

GitHub provides free API access to OpenAI models via GitHub Models:
- GPT-4o, GPT-4o-mini (OpenAI)
- Llama 3.1 405B, 70B (Meta)
- Phi-3 (Microsoft)
- Mistral Large (Mistral AI)

Rate limits: 15 requests/min, 150 requests/hour (generous for AIOS)
Cost: $0 (included with GitHub account)

Setup:
1. Visit: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Name: "AIOS GitHub Models API"
4. Scopes: Check "repo" (or just "public_repo")
5. Generate and copy token
6. Run: $env:GITHUB_TOKEN = "ghp_your_token_here"
"""

import os
import requests
from typing import List, Dict, Any


def test_github_token() -> bool:
    """Test if GitHub token has API access."""
    token = os.environ.get("GITHUB_TOKEN")

    if not token:
        print("❌ GITHUB_TOKEN not set")
        print("\n📋 Setup instructions:")
        print("   1. Visit: https://github.com/settings/tokens")
        print("   2. Generate new token (classic)")
        print("   3. Scopes: 'repo' or 'public_repo'")
        print("   4. In PowerShell: $env:GITHUB_TOKEN = 'ghp_...'")
        print("   5. Re-run this script")
        return False

    print(f"✅ GITHUB_TOKEN found ({len(token)} chars)")
    print(f"   Prefix: {token[:10]}...")

    # Test API access
    try:
        response = requests.get(
            "https://models.inference.ai.azure.com/models",
            headers={"Authorization": f"Bearer {token}"},
            timeout=10,
        )

        if response.status_code == 200:
            models = response.json()
            print(f"\n✅ GitHub Models API accessible!")
            print(f"   Available models: {len(models)}")
            return True
        elif response.status_code == 401:
            print("\n❌ Token invalid or insufficient permissions")
            print("   Regenerate token with 'repo' scope")
            return False
        else:
            print(f"\n⚠️  Unexpected status: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False

    except Exception as e:
        print(f"\n❌ API test failed: {e}")
        return False


def list_available_models() -> List[Dict[str, Any]]:
    """List all available GitHub Models."""
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        return []

    try:
        response = requests.get(
            "https://models.inference.ai.azure.com/models",
            headers={"Authorization": f"Bearer {token}"},
            timeout=10,
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching models: {e}")
        return []


def test_gpt4o_chat() -> bool:
    """Test GPT-4o chat completion."""
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        return False

    print("\n🧪 Testing GPT-4o chat completion...")

    try:
        response = requests.post(
            "https://models.inference.ai.azure.com/chat/completions",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
            json={
                "model": "gpt-4o",
                "messages": [
                    {"role": "user", "content": "Say 'GitHub Models works!' in 3 words"}
                ],
                "max_tokens": 20,
            },
            timeout=30,
        )
        response.raise_for_status()

        data = response.json()
        content = data["choices"][0]["message"]["content"]

        print(f"✅ GPT-4o response: {content}")
        return True

    except Exception as e:
        print(f"❌ GPT-4o test failed: {e}")
        return False


def main():
    print("=" * 70)
    print("🚀 GitHub Models API Setup for AIOS")
    print("=" * 70)
    print()

    # Test token
    if not test_github_token():
        return

    # List models
    print("\n📊 Fetching available models...")
    models = list_available_models()

    if models:
        print(f"\n✅ {len(models)} models available:")

        # Categorize by provider
        openai_models = [m for m in models if "gpt" in m.get("name", "").lower()]
        meta_models = [m for m in models if "llama" in m.get("name", "").lower()]
        microsoft_models = [m for m in models if "phi" in m.get("name", "").lower()]

        if openai_models:
            print("\n  🤖 OpenAI Models:")
            for m in openai_models[:5]:
                print(f"     - {m.get('name', m.get('id', 'unknown'))}")

        if meta_models:
            print("\n  🦙 Meta Models:")
            for m in meta_models[:5]:
                print(f"     - {m.get('name', m.get('id', 'unknown'))}")

        if microsoft_models:
            print("\n  🔷 Microsoft Models:")
            for m in microsoft_models[:3]:
                print(f"     - {m.get('name', m.get('id', 'unknown'))}")

    # Test GPT-4o
    if test_gpt4o_chat():
        print("\n" + "=" * 70)
        print("✅ GitHub Models API ready for AIOS!")
        print("=" * 70)
        print("\n📋 Next steps:")
        print("   1. Run: python unified_github_models_handler.py")
        print("   2. Test hierarchical pipeline with GitHub Models")
        print("   3. Fix E501 violations using GPT-4o")
        print("\n💰 Cost: $0 (free tier)")
        print("⏱️  Rate limit: 15 req/min, 150 req/hour")


if __name__ == "__main__":
    main()
