"""
Test adversarial prompt ingestion and detection using GROK-MEGA.mkd patterns.
"""


import sys
import os
import pytest
from pathlib import Path


@pytest.fixture(autouse=True, scope="session")
def add_src_to_path():
    parent_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..')
    )
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)


GROK_MEGA_PATH = (
    Path(__file__).parents[2] /
    ".github" / "experimentals" / "GROK-MEGA-STUB.mkd"
)


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
    from src.ainlp_migration import detect_adversarial_prompt
    result = detect_adversarial_prompt(prompt_text)
    assert result.is_adversarial, (
        f"Prompt not detected as adversarial: {prompt_text[:80]}..."
    )
