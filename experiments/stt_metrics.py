"""Dependency-free text normalization and error metrics for STT evaluation."""
from __future__ import annotations

import unicodedata


def normalize_text(text: str) -> str:
    """Normalize Unicode to NFC, case-fold and collapse whitespace; preserve accents."""
    return " ".join(unicodedata.normalize("NFC", text).casefold().split())


def edit_distance(reference: list[str] | str, hypothesis: list[str] | str) -> int:
    """Levenshtein distance with O(min(n, m)) memory."""
    if len(reference) < len(hypothesis):
        reference, hypothesis = hypothesis, reference
    previous = list(range(len(hypothesis) + 1))
    for i, ref_item in enumerate(reference, start=1):
        current = [i]
        for j, hyp_item in enumerate(hypothesis, start=1):
            current.append(min(
                current[-1] + 1,
                previous[j] + 1,
                previous[j - 1] + (ref_item != hyp_item),
            ))
        previous = current
    return previous[-1]


def word_error_counts(reference: str, hypothesis: str) -> tuple[int, int]:
    ref_words = normalize_text(reference).split()
    hyp_words = normalize_text(hypothesis).split()
    if not ref_words:
        raise ValueError("La transcription de référence ne peut pas être vide.")
    return edit_distance(ref_words, hyp_words), len(ref_words)


def character_error_counts(reference: str, hypothesis: str) -> tuple[int, int]:
    ref_text = normalize_text(reference)
    hyp_text = normalize_text(hypothesis)
    if not ref_text:
        raise ValueError("La transcription de référence ne peut pas être vide.")
    return edit_distance(ref_text, hyp_text), len(ref_text)
