#!/usr/bin/env python3
"""Build a review-only Wolof batch plan with stable ordering and cross-batch deduplication.

Use --input-candidates to pin a previously downloaded Kaikki JSON snapshot. Without it,
the importer downloads the current upstream dataset and the plan is explicitly time-specific.
No audio is generated and canonical lexical data is never modified.
"""
import argparse
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEXICON = ROOT / "data" / "wolof-fr-dictionary.json"
IMPORTER = ROOT / "wolof_tts" / "import_kaikki_candidates.py"
KAIKKI_URL = "https://kaikki.org/frwiktionary/Wolof/kaikki.org-dictionary-Wolof.jsonl"
KAIKKI_PAGE = "https://kaikki.org/frwiktionary/Wolof/index.html"
LICENSE_NOTE = "Wiktionary-derived data; retain attribution and comply with applicable CC BY-SA/GFDL terms."
KNOWN_AUDIO_HEADWORDS = {
    "aada", "aay", "aaye", "ab", "abb", "ag", "ak", "alal", "alkaati", "altine",
    "agsil ak jàmm ci sa kër", "aksidaa", "alarba", "albaani", "alemaañ", "all",
}
VALIDATED_REFERENCES = {"jërëjëf", "kër", "ñëw"}


def norm(value):
    return re.sub(r"\s+", " ", str(value or "").strip()).casefold()


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def load_json(path):
    raw = path.read_bytes()
    return json.loads(raw.decode("utf-8")), raw


def manifest_words(path):
    """Read generator manifests and simple manifest lists; fail closed on unknown shapes."""
    payload, raw = load_json(path)
    rows = payload if isinstance(payload, list) else payload.get("entries")
    if not isinstance(rows, list):
        raise SystemExit(f"Unsupported previous manifest format: {path}")
    words = set()
    for row in rows:
        if not isinstance(row, dict):
            continue
        word = row.get("wolof") or row.get("word")
        if word and norm(word):
            words.add(norm(word))
    return words, sha256_bytes(raw)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("wolof-next-audio-batch-plan.json"))
    parser.add_argument("--batch-size", type=int, default=10)
    parser.add_argument("--start-offset", type=int, default=0,
                        help="Offset into filtered, sorted candidates (not a generator index).")
    parser.add_argument("--input-candidates", type=Path,
                        help="Pinned JSON candidate snapshot from import_kaikki_candidates.py.")
    parser.add_argument("--previous-manifest", type=Path, action="append", default=[],
                        help="Prior generated manifest JSON; repeat for every available batch.")
    args = parser.parse_args()
    if not 1 <= args.batch_size <= 20 or args.start_offset < 0:
        raise SystemExit("batch-size must be 1..20 and start-offset must be >= 0")

    lexicon, lexicon_bytes = load_json(LEXICON)
    if not args.input_candidates:
        raise SystemExit(
            "Refusing non-reproducible planning: provide --input-candidates with a saved, "
            "versioned Kaikki candidate JSON snapshot. No live download fallback is allowed."
        )
    candidate_path = args.input_candidates if args.input_candidates.is_absolute() else ROOT / args.input_candidates
    candidate_payload, candidate_bytes = load_json(candidate_path)
    candidate_mode = "pinned-input-snapshot"

    previous_words = {norm(w) for w in KNOWN_AUDIO_HEADWORDS}
    manifest_hashes = []
    for manifest_path in args.previous_manifest:
        path = manifest_path if manifest_path.is_absolute() else ROOT / manifest_path
        words, digest = manifest_words(path)
        previous_words.update(words)
        manifest_hashes.append({"path": str(path), "sha256": digest, "unique_headwords": len(words)})

    merged = {}
    for entry in lexicon.get("entries", []):
        word = str((entry.get("wolof") or {}).get("word") or "").strip()
        french = str((entry.get("fr") or {}).get("word") or "").strip()
        if not word or not french:
            continue
        variants = [v.strip() for v in re.split(r"\s*/\s*", word) if v.strip()]
        for variant_no, variant in enumerate(variants, 1):
            key = norm(variant)
            merged.setdefault(key, {
                "wolof": variant, "french": french, "source": entry.get("source", ""),
                "source_name": entry.get("sourceName", lexicon.get("source", "Jàngileen")),
                "source_translation_status": entry.get("translationStatus", "source-documented"),
                "variant_index": variant_no, "license_note": "Verify Jàngileen terms before redistribution.",
                "human_pronunciation_validation": "pending",
            })
    for row in candidate_payload.get("entries", []):
        word, french = str(row.get("wolof") or "").strip(), str(row.get("french") or "").strip()
        if not word or not french:
            continue
        key = norm(word)
        merged.setdefault(key, {
            "wolof": word, "french": french, "source": row.get("source", KAIKKI_PAGE),
            "source_dataset": row.get("sourceDataset", KAIKKI_URL),
            "source_record_line": row.get("sourceRecordLine"),
            "source_name": row.get("dataset", "Kaikki / Wiktionnaire français"),
            "source_translation_status": row.get("translationStatus", "unverified-candidate"),
            "part_of_speech": row.get("partOfSpeech", "unspecified"),
            "license_note": row.get("licenseNote", LICENSE_NOTE),
            "human_pronunciation_validation": "pending",
        })

    candidates = [row for key, row in merged.items()
                  if key not in previous_words and key not in VALIDATED_REFERENCES]
    candidates.sort(key=lambda row: (norm(row["wolof"]), row["french"].casefold(), row.get("source", "")))
    selected = candidates[args.start_offset:args.start_offset + args.batch_size]
    plan = {
        "schema_version": 2,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "purpose": "review-only candidate plan; no audio generated and no canonical data modified",
        "source": {"kaikki_page": KAIKKI_PAGE, "kaikki_jsonl": KAIKKI_URL,
                   "kaikki_license_note": LICENSE_NOTE, "candidate_mode": candidate_mode},
        "source_hashes": {"canonical_lexicon_sha256": sha256_bytes(lexicon_bytes),
                          "kaikki_candidates_json_sha256": sha256_bytes(candidate_bytes)},
        "previous_manifest_hashes": manifest_hashes,
        "excluded_previous_headword_count": len(previous_words),
        "excluded_validated_reference_headwords": sorted(VALIDATED_REFERENCES),
        "candidate_count_before_exclusions": len(merged),
        "remaining_candidate_count": len(candidates),
        "start_offset": args.start_offset,
        "selected_count": len(selected),
        "selected": selected,
        "important": [
            "Use --input-candidates with a saved candidate JSON to reproduce the same lexical source snapshot.",
            "Supply every available prior audio manifest with repeated --previous-manifest arguments to prevent cross-batch repeats.",
            "Only the manifests supplied to this run can be checked; absent or expired artifacts cannot be inferred.",
            "Review translations and licences before publication.",
            "A planned word is not proof that an audio file exists.",
            "All generated pronunciation validation remains pending until a human listens to the actual WAV.",
        ],
    }
    output = args.output if args.output.is_absolute() else ROOT / args.output
    output.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output.relative_to(ROOT) if output.is_relative_to(ROOT) else output),
        "candidate_mode": candidate_mode,
        "candidate_count_before_exclusions": len(merged),
        "excluded_previous_headwords": len(previous_words),
        "remaining_candidate_count": len(candidates),
        "selected_count": len(selected),
        "candidate_hash": plan["source_hashes"]["kaikki_candidates_json_sha256"],
        "selected_headwords": [row["wolof"] for row in selected],
        "audio_generated": False,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
