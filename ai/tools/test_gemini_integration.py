#!/usr/bin/env python3
"""
AIOS Gemini Integration Test

Tests all available Gemini integration paths:
1. Google AI Studio (GEMINI_API_KEY)
2. Vertex AI (gcloud auth)
3. Local fallback (Ollama mistral)

Run: python ai/tools/test_gemini_integration.py
"""

import asyncio
import os
import sys
from pathlib import Path

# Add tools to path
sys.path.insert(0, str(Path(__file__).parent))


def test_ai_studio():
    """Test Google AI Studio API."""
    print("\n[1] Testing Google AI Studio...")

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("    [SKIP] GEMINI_API_KEY not set")
        print("    Get key: https://aistudio.google.com/apikey")
        return False

    try:
        import httpx

        url = (
            "https://generativelanguage.googleapis.com/v1beta"
            f"/models/gemini-2.0-flash:generateContent?key={api_key}"
        )

        payload = {
            "contents": [{"parts": [{"text": 'Respond with: {"status": "ok"}'}]}],
            "generationConfig": {"temperature": 0, "maxOutputTokens": 50},
        }

        with httpx.Client(timeout=30) as client:
            response = client.post(url, json=payload)

            if response.status_code == 200:
                print("    [OK] Google AI Studio connected")
                data = response.json()
                text = data["candidates"][0]["content"]["parts"][0]["text"]
                print(f"    Response: {text[:50]}")
                return True
            else:
                print(f"    [FAIL] Status {response.status_code}")
                print(f"    {response.text[:100]}")
                return False

    except Exception as e:
        print(f"    [FAIL] {e}")
        return False


def test_vertex_ai():
    """Test Vertex AI."""
    print("\n[2] Testing Vertex AI...")

    try:
        import vertexai
        from vertexai.generative_models import GenerativeModel

        project = os.getenv("GOOGLE_CLOUD_PROJECT", "gen-lang-client-0072186287")
        region = os.getenv("GOOGLE_CLOUD_REGION", "us-central1")

        print(f"    Project: {project}")
        print(f"    Region:  {region}")

        vertexai.init(project=project, location=region)
        model = GenerativeModel("gemini-1.5-flash-002")

        response = model.generate_content(
            'Respond with: {"status": "ok"}',
            generation_config={"temperature": 0, "max_output_tokens": 50},
        )

        print("    [OK] Vertex AI connected")
        print(f"    Response: {response.text[:50]}")
        return True

    except ImportError:
        print("    [SKIP] google-cloud-aiplatform not installed")
        print("    Install: pip install google-cloud-aiplatform")
        return False
    except Exception as e:
        print(f"    [FAIL] {e}")
        return False


def test_ollama_fallback():
    """Test local Ollama fallback."""
    print("\n[3] Testing Ollama Fallback (Mistral)...")

    try:
        import httpx

        with httpx.Client(timeout=30) as client:
            response = client.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "mistral:7b-instruct",
                    "prompt": 'Respond with: {"status": "ok"}',
                    "stream": False,
                    "options": {"temperature": 0, "num_predict": 50},
                },
            )

            if response.status_code == 200:
                data = response.json()
                text = data.get("response", "")
                print("    [OK] Ollama Mistral connected")
                print(f"    Response: {text[:50]}")
                return True
            else:
                print(f"    [FAIL] Status {response.status_code}")
                return False

    except Exception as e:
        print(f"    [FAIL] {e}")
        return False


def test_gemma_scout():
    """Test Gemma scout agent."""
    print("\n[4] Testing Gemma Scout (1B)...")

    try:
        import httpx

        with httpx.Client(timeout=15) as client:
            response = client.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "gemma3:1b",
                    "prompt": "Classify: E501 (line too long). One word.",
                    "stream": False,
                    "options": {"temperature": 0.1, "num_predict": 10},
                },
            )

            if response.status_code == 200:
                data = response.json()
                text = data.get("response", "").strip()
                print("    [OK] Gemma Scout connected")
                print(f"    Classification: {text[:30]}")
                return True
            else:
                print(f"    [FAIL] Status {response.status_code}")
                return False

    except Exception as e:
        print(f"    [FAIL] {e}")
        return False


def main():
    """Run all integration tests."""
    print("=" * 60)
    print("AIOS Gemini Integration Test")
    print("=" * 60)
    print(f"Project: gen-lang-client-0072186287")
    print(f"Firebase: aios-28728220")

    results = {
        "ai_studio": test_ai_studio(),
        "vertex_ai": test_vertex_ai(),
        "ollama_mistral": test_ollama_fallback(),
        "ollama_gemma": test_gemma_scout(),
    }

    print("\n" + "=" * 60)
    print("Summary:")
    print("=" * 60)

    working = []
    for name, ok in results.items():
        status = "[OK]" if ok else "[--]"
        print(f"  {status} {name}")
        if ok:
            working.append(name)

    print()
    if "ai_studio" in working or "vertex_ai" in working:
        print("[READY] Gemini Oracle available")
        print("        Triangular system can operate with cloud validation")
    elif "ollama_mistral" in working:
        print("[PARTIAL] Local-only mode")
        print("          Mistral worker available, no cloud validation")
    else:
        print("[ERROR] No working agents found")

    print()
    print("Next Steps:")
    if "ai_studio" not in working and "vertex_ai" not in working:
        print("  1. Set GEMINI_API_KEY from https://aistudio.google.com/apikey")
        print("  2. Or install Vertex AI: pip install google-cloud-aiplatform")
        print("  3. Then authenticate: gcloud auth application-default login")

    return 0 if any(results.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
