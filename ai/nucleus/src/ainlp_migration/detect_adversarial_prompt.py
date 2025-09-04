"""
AINLP adversarial prompt pattern detector for meta-prompts,
dual-response logic, and obfuscation.
"""
import re
from collections import namedtuple

DetectionResult = namedtuple("DetectionResult", ["is_adversarial", "reason"])

# Patterns for meta-prompts, dual-response, and obfuscation
META_PROMPT_PATTERNS = [
    r"dual[-_ ]?response",  # explicit dual response
    r"unrestricted answer",  # requests for unrestricted output
    r"refusal|disclaimer",  # explicit refusal/disclaimer
    r"godmode|liberated answer",  # jailbreak/godmode
    r"minimum word count|not less than \\d+ words",  # word count enforcement
    r"opposite(ly)? to the refusal",  # explicit inversion
    r"insert the following divider",  # divider insertion
    r"act(ivate)? !godmode",  # godmode activation
    r"prompt(ing)? engineering|meta[-_ ]?prompt",  # meta-prompting
    r"adversarial prompt",  # adversarial intent
    r"jailbreak",  # jailbreak keyword
]

OBFUSCATION_HINTS = [
    r"[Ａ-Ｚａ-ｚ０-９]+",  # full-width unicode
    r"[𝒜-𝒵𝒶-𝓏𝟢-𝟫]+",  # math script unicode
    r"[🇦-🇿]+",  # regional indicator symbols
    r"[ -ᚿ]+",  # runic block
    r"[⠁-⠿]+",  # braille patterns
    r"[ⓐ-ⓩⓐ-ⓩ]+",  # enclosed alphanumerics
]


def detect_adversarial_prompt(text):
    reasons = []
    for pat in META_PROMPT_PATTERNS:
        if re.search(pat, text, re.IGNORECASE):
            reasons.append(f"Matched meta-prompt pattern: {pat}")
    for obf in OBFUSCATION_HINTS:
        if re.search(obf, text):
            reasons.append(f"Obfuscation detected: {obf}")
    is_adv = bool(reasons)
    return DetectionResult(is_adversarial=is_adv, reason="; ".join(reasons))
