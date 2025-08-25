"""
Test adversarial prompt ingestion and detection using GROK-MEGA.mkd patterns.
"""
import pytest
from pathlib import Path

# Placeholder: Replace with actual AINLP adversarial prompt detection logic
from ai.src.ainlp_migration import detect_adversarial_prompt

GROK_MEGA_PATH = Path(__file__).parents[2] / ".github" / "experimentals" / "GROK-MEGA.mkd"

def load_grok_mega_samples():
    with open(GROK_MEGA_PATH, encoding="utf-8") as f:
        content = f.read()
    # Simple split: each '###' header marks a new adversarial prompt block
    samples = [s.strip() for s in content.split('###') if s.strip()]
    return samples

@pytest.mark.parametrize("prompt_text", load_grok_mega_samples())
def test_grok_mega_adversarial_detection(prompt_text):
    """
    Ensure AINLP adversarial prompt detector flags GROK-MEGA patterns.
    """
    result = detect_adversarial_prompt(prompt_text)
    assert result.is_adversarial, f"Prompt not detected as adversarial: {prompt_text[:80]}..."
