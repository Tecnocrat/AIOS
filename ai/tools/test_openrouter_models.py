#!/usr/bin/env python3
"""
OpenRouter Model Explorer - Find best alternatives to Gemini

Tests:
1. Gemini availability via OpenRouter
2. Coding-specialized models (Claude, GPT-4, DeepSeek)
3. Cost/performance analysis
"""

import httpx
import os
import json
from typing import List, Dict, Any


def fetch_openrouter_models() -> List[Dict[str, Any]]:
    """Fetch all available models from OpenRouter."""
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("ERROR: OPENROUTER_API_KEY not set")
        return []
    
    try:
        resp = httpx.get(
            "https://openrouter.ai/api/v1/models",
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=10
        )
        resp.raise_for_status()
        return resp.json()["data"]
    except Exception as e:
        print(f"ERROR fetching models: {e}")
        return []


def analyze_gemini_availability(models: List[Dict]) -> None:
    """Check if Gemini models available via OpenRouter."""
    gemini_models = [m for m in models if "gemini" in m["id"].lower()]
    
    print("=" * 80)
    print(f"GEMINI MODELS VIA OPENROUTER: {len(gemini_models)} found")
    print("=" * 80)
    
    if not gemini_models:
        print("  ❌ No Gemini models available via OpenRouter")
        print("     (Likely Google doesn't allow third-party routing)")
        return
    
    for model in gemini_models[:10]:
        ctx = model.get("context_length", 0)
        price = model.get("pricing", {}).get("prompt", "N/A")
        print(f"  ✅ {model['id'][:50]:50} | {ctx:>7} ctx | ${price}/1M")


def analyze_coding_models(models: List[Dict]) -> None:
    """Find best coding-specialized models."""
    coding_keywords = ["claude", "gpt-4", "deepseek", "qwen", "codestral", "llama"]
    coding_models = [
        m for m in models 
        if any(kw in m["id"].lower() for kw in coding_keywords)
        and m.get("context_length", 0) >= 8000  # Minimum for code tasks
    ]
    
    # Sort by context length (descending), then price (ascending)
    coding_models.sort(
        key=lambda x: (
            x.get("context_length", 0),
            -float(x.get("pricing", {}).get("prompt", "999"))
        ),
        reverse=True
    )
    
    print("\n" + "=" * 80)
    print(f"TOP CODING MODELS (8K+ context): {len(coding_models)} available")
    print("=" * 80)
    print(f"{'Model ID':<50} | {'Context':>7} | {'$/1M prompt':>12}")
    print("-" * 80)
    
    for model in coding_models[:15]:
        model_id = model["id"][:48]
        ctx = model.get("context_length", 0)
        price = model.get("pricing", {}).get("prompt", "N/A")
        print(f"{model_id:<50} | {ctx:>7} | ${str(price):>11}")


def analyze_free_models(models: List[Dict]) -> None:
    """Find free/cheap models for testing."""
    free_models = [
        m for m in models
        if float(m.get("pricing", {}).get("prompt", "999")) == 0.0
        or "free" in m["id"].lower()
    ]
    
    print("\n" + "=" * 80)
    print(f"FREE MODELS: {len(free_models)} available")
    print("=" * 80)
    
    for model in free_models[:10]:
        ctx = model.get("context_length", 0)
        print(f"  {model['id'][:60]:60} | {ctx:>7} ctx")


def recommend_tier2_tier3_models(models: List[Dict]) -> None:
    """Recommend models for Tier 2 (generation) and Tier 3 (validation)."""
    print("\n" + "=" * 80)
    print("RECOMMENDED MODEL STRATEGY FOR HIERARCHICAL PIPELINE")
    print("=" * 80)
    
    print("\n🎯 TIER 2 (Code Generation) - Balance speed + quality:")
    tier2_candidates = [
        m for m in models
        if any(kw in m["id"].lower() for kw in ["claude-3-5-haiku", "gpt-4o-mini", "deepseek-chat", "qwen"])
        and m.get("context_length", 0) >= 32000
    ]
    tier2_candidates.sort(key=lambda x: float(x.get("pricing", {}).get("prompt", "999")))
    
    for i, model in enumerate(tier2_candidates[:5], 1):
        price = model.get("pricing", {}).get("prompt", "N/A")
        ctx = model.get("context_length", 0)
        print(f"  {i}. {model['id'][:45]:45} | ${price}/1M | {ctx} ctx")
    
    print("\n🔍 TIER 3 (Quality Validation) - Prefer accuracy:")
    tier3_candidates = [
        m for m in models
        if any(kw in m["id"].lower() for kw in ["claude-3-5-sonnet", "gpt-4o", "deepseek-chat"])
        and m.get("context_length", 0) >= 32000
    ]
    tier3_candidates.sort(key=lambda x: -x.get("context_length", 0))
    
    for i, model in enumerate(tier3_candidates[:5], 1):
        price = model.get("pricing", {}).get("prompt", "N/A")
        ctx = model.get("context_length", 0)
        print(f"  {i}. {model['id'][:45]:45} | ${price}/1M | {ctx} ctx")


def main():
    print("\n🔍 OpenRouter Model Analysis for AIOS Multi-Agent Communication\n")
    
    models = fetch_openrouter_models()
    if not models:
        return
    
    print(f"Total models available: {len(models)}\n")
    
    analyze_gemini_availability(models)
    analyze_coding_models(models)
    analyze_free_models(models)
    recommend_tier2_tier3_models(models)
    
    print("\n" + "=" * 80)
    print("✅ OpenRouter provides unified interface for 200+ models")
    print("✅ No daily quotas - pay per use (typical: $0.10-$3.00 per 1M tokens)")
    print("✅ Can replace Gemini entirely with Claude/GPT-4/DeepSeek")
    print("=" * 80)


if __name__ == "__main__":
    main()
