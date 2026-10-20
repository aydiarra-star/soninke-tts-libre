#!/usr/bin/env python3
"""Audit Wolof dictionary/audio coverage without modifying source data.

Headword coverage and per-dictionary-entry coverage are reported separately.
A headword match is not enough when one word has several dictionary senses.
"""
from __future__ import annotations

import argparse
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LEXICON = ROOT / "data" / "wolof-fr-dictionary.json"
DEFAULT_MANIFEST = ROOT / "data" / "wolof-audio-manifest.json"


def norm(value: object) -> str:
    text = unicodedata.normalize("NFC", str(value or "")).strip()
    return re.sub(r"\s+", " ", text).casefold()


def build_report(lexicon: dict, manifest: dict) -> dict:
    entries = lexicon.get("entries", [])
    audio_entries = manifest.get("entries", [])
    dictionary_by_word = {}
    dictionary_by_id = {}
    missing_french_entries = []
    for index, row in enumerate(entries):
        word = norm((row.get("wolof") or {}).get("word"))
        french = str((row.get("fr") or {}).get("word") or "").strip()
        entry_id = str(row.get("id") or f"dictionary-row-{index:05d}")
        if not word:
            continue
        dictionary_by_id[entry_id] = {"id": entry_id, "word": word, "has_french": bool(french)}
        dictionary_by_word.setdefault(word, {
            "word": str((row.get("wolof") or {}).get("word") or "").strip(),
            "has_french": False,
        })
        if french:
            dictionary_by_word[word]["has_french"] = True
        else:
            missing_french_entries.append({"id": entry_id, "wolof": word})

    audio_by_word = {}
    audio_by_entry_id = {}
    audio_rows_without_entry_id = []
    for index, row in enumerate(audio_entries):
        word = norm(row.get("wolof"))
        if word:
            audio_by_word.setdefault(word, []).append(row)
        entry_id = str(row.get("entry_id") or "").strip()
        if entry_id:
            audio_by_entry_id.setdefault(entry_id, []).append(row)
        else:
            audio_rows_without_entry_id.append(str(row.get("id") or f"manifest-row-{index:05d}"))

    dictionary_words = set(dictionary_by_word)
    matched_audio = dictionary_words & set(audio_by_word)
    verified_voice_words = set()
    pending_voice_words = set()
    for word in matched_audio:
        for row in audio_by_word[word]:
            if row.get("voice_identity_validation") == "verified" and row.get("reference_audio_sha256"):
                verified_voice_words.add(word)
            else:
                pending_voice_words.add(word)

    dictionary_ids = set(dictionary_by_id)
    matched_entry_ids = dictionary_ids & set(audio_by_entry_id)
    verified_entry_ids = set()
    pending_entry_ids = set()
    for entry_id in matched_entry_ids:
        for row in audio_by_entry_id[entry_id]:
            if row.get("voice_identity_validation") == "verified" and row.get("reference_audio_sha256"):
                verified_entry_ids.add(entry_id)
            else:
                pending_entry_ids.add(entry_id)

    candidate_translation = sorted({
        norm(row.get("wolof")) for row in audio_entries
        if norm(row.get("wolof")) and any(
            marker in str(row.get(field) or "").casefold()
            for field in ("translation_validation", "source_translation_status")
            for marker in ("candidate", "pending", "uncertain", "review", "unverified")
        )
    })
    missing_french_forms = sorted(
        word for word, record in dictionary_by_word.items() if not record["has_french"]
    )
    missing_entry_ids = sorted(dictionary_ids - matched_entry_ids)
    return {
        "schema_version": 2,
        "dictionary_entry_rows": len(entries),
        "dictionary_entries_with_wolof_and_id": len(dictionary_by_id),
        "dictionary_entries_missing_french_translation": len(missing_french_entries),
        "dictionary_entries_missing_french_examples": missing_french_entries[:50],
        "dictionary_unique_wolof_forms": len(dictionary_words),
        "dictionary_forms_with_french_translation": sum(1 for row in dictionary_by_word.values() if row["has_french"]),
        "dictionary_forms_missing_french_translation": missing_french_forms,
        "audio_manifest_rows": len(audio_entries),
        "unique_audio_headwords": len(audio_by_word),
        "dictionary_forms_with_audio_manifest": len(matched_audio),
        "dictionary_forms_without_audio_manifest": len(dictionary_words - set(audio_by_word)),
        "dictionary_forms_with_verified_reference_voice": len(verified_voice_words),
        "dictionary_forms_with_voice_identity_pending_or_unverified": len(pending_voice_words),
        "dictionary_entries_with_audio_by_entry_id": len(matched_entry_ids),
        "dictionary_entries_without_audio_by_entry_id": len(missing_entry_ids),
        "dictionary_entries_without_audio_by_entry_id_examples": missing_entry_ids[:50],
        "dictionary_entries_with_verified_reference_voice": len(verified_entry_ids),
        "dictionary_entries_with_voice_identity_pending_or_unverified": len(pending_entry_ids),
        "audio_manifest_rows_without_dictionary_entry_id": len(audio_rows_without_entry_id),
        "audio_manifest_rows_without_dictionary_entry_id_examples": audio_rows_without_entry_id[:50],
        "audio_headwords_not_in_dictionary": sorted(set(audio_by_word) - dictionary_words),
        "audio_headwords_with_translation_review_flags": candidate_translation,
        "audio_models": sorted({str(row.get("model") or row.get("voice_engine") or "unknown") for row in audio_entries}),
        "note": "Headword coverage is not per-entry coverage. A dictionary entry counts as having audio only when manifest.entry_id matches dictionary.id. Voice identity counts as verified only when that matched entry has voice_identity_validation='verified' and reference_audio_sha256. This audit does not listen to audio or certify pronunciation.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lexicon", type=Path, default=DEFAULT_LEXICON)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--output", type=Path, help="Optional path for a JSON report; source files are never changed.")
    args = parser.parse_args()
    try:
        lexicon = json.loads(args.lexicon.read_text(encoding="utf-8"))
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Audit impossible : {exc}") from exc
    report = build_report(lexicon, manifest)
    rendered = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
