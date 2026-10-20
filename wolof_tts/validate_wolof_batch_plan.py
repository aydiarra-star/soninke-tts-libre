#!/usr/bin/env python3
"""Validate a Wolof batch plan against pinned inputs without importing TTS libraries."""
import hashlib
import importlib.util
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEXICON = ROOT / "data" / "wolof-fr-dictionary.json"
CANDIDATES = ROOT / "data" / "kaikki-wolof-candidates.json"
HISTORICAL = ROOT / "wolof_tts" / "manifests" / "historical-audio-headwords.json"
SEEDS = {"jërëjëf", "kër", "ñëw"}


def norm(value):
    return re.sub(r"\\s+", " ", str(value or "").strip()).casefold()


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_planner():
    spec = importlib.util.spec_from_file_location("wolof_plan_module", ROOT / "wolof_tts" / "plan_next_audio_batch.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _merged_sources():
    lexicon = json.loads(LEXICON.read_text(encoding="utf-8"))
    candidate_payload = json.loads(CANDIDATES.read_text(encoding="utf-8"))
    merged = {}
    for entry in lexicon.get("entries", []):
        word = str((entry.get("wolof") or {}).get("word") or "").strip()
        french = str((entry.get("fr") or {}).get("word") or "").strip()
        if not word or not french:
            continue
        for variant_no, variant in enumerate([v.strip() for v in re.split(r"\\s*/\\s*", word) if v.strip()], 1):
            merged.setdefault(norm(variant), {
                "wolof": variant, "french": french, "source": entry.get("source", ""),
                "source_name": entry.get("sourceName", lexicon.get("source", "Jàngileen")),
                "source_translation_status": entry.get("translationStatus", "source-documented"),
                "variant_index": variant_no,
            })
    for row in candidate_payload.get("entries", []):
        word, french = str(row.get("wolof") or "").strip(), str(row.get("french") or "").strip()
        if not word or not french:
            continue
        merged.setdefault(norm(word), {
            "wolof": word, "french": french, "source": row.get("source", "https://kaikki.org/frwiktionary/Wolof/index.html"),
            "source_dataset": row.get("sourceDataset", "https://kaikki.org/frwiktionary/Wolof/kaikki.org-dictionary-Wolof.jsonl"),
            "source_record_line": row.get("sourceRecordLine"),
            "source_name": row.get("dataset", "Kaikki / Wiktionnaire français"),
            "source_translation_status": row.get("translationStatus", "unverified-candidate"),
            "part_of_speech": row.get("partOfSpeech", "unspecified"),
            "license_note": row.get("licenseNote", "Wiktionary-derived data; retain attribution and comply with applicable CC BY-SA/GFDL terms."),
            "human_pronunciation_validation": "pending",
        })
    return merged


def validate_plan(plan_path, root=ROOT):
    plan_path = Path(plan_path)
    if not plan_path.is_absolute():
        plan_path = Path.cwd() / plan_path
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    expected_hashes = {
        "canonical_lexicon_sha256": sha256(LEXICON),
        "kaikki_candidates_json_sha256": sha256(CANDIDATES),
    }
    actual_hashes = plan.get("source_hashes") or {}
    for key, expected in expected_hashes.items():
        if actual_hashes.get(key) != expected:
            raise ValueError(f"Plan rejected: {key} does not match the pinned file.")
    selected = plan.get("selected")
    if not isinstance(selected, list) or not 1 <= len(selected) <= 20:
        raise ValueError("Plan rejected: selected must contain 1..20 entries.")
    if plan.get("selected_count") != len(selected):
        raise ValueError("Plan rejected: selected_count does not match selected list length.")

    planner = _load_planner()
    historical = json.loads(HISTORICAL.read_text(encoding="utf-8"))
    excluded = {planner.norm(w) for w in planner.KNOWN_AUDIO_HEADWORDS}
    excluded.update(planner.norm(row.get("wolof")) for row in historical.get("entries", []))
    excluded.update(SEEDS)
    merged = _merged_sources()
    seen = set()
    for row in selected:
        if not isinstance(row, dict):
            raise ValueError("Plan rejected: every selected entry must be an object.")
        word = str(row.get("wolof") or "").strip()
        key = norm(word)
        french = str(row.get("french") or "").strip()
        if not key or not french:
            raise ValueError(f"Plan rejected: missing headword or French translation: {row!r}")
        if key in seen:
            raise ValueError(f"Plan rejected: duplicate normalized headword {word!r}.")
        if key in excluded:
            raise ValueError(f"Plan rejected: headword is in historical audio or validated references: {word!r}.")
        source_row = merged.get(key)
        if source_row is None:
            raise ValueError(f"Plan rejected: selected headword is absent from pinned source inputs: {word!r}.")
        for field in ("wolof", "french", "source", "source_name", "source_translation_status", "variant_index"):
            if row.get(field) != source_row.get(field):
                raise ValueError(f"Plan rejected: {field} for {word!r} differs from merged pinned sources.")
        seen.add(key)
    return {
        "valid": True,
        "selected_count": len(selected),
        "selected_headwords": [row["wolof"] for row in selected],
        "source_hashes": expected_hashes,
        "historical_headwords_excluded": len(excluded),
        "audio_generated": False,
        "tts_model_loaded": False,
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path)
    args = parser.parse_args()
    print(json.dumps(validate_plan(args.plan), ensure_ascii=False, indent=2))
