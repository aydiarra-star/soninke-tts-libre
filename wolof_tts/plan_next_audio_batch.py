#!/usr/bin/env python3
"""Build a review-only, reproducible Wolof audio batch plan without generating audio.

This planner downloads the currently published Kaikki JSONL via the existing importer,
combines it with the canonical dictionary in memory, excludes known previous batch
headwords, and writes a hash-addressed plan. It never modifies the dictionary or WAVs.
The output records that a source snapshot is time-specific and must be reviewed.
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
    "agsil ak jàmm ci sa kër", "aksidaa", "alarba", "albaani", "alemaanñ", "all",
}

def norm(value):
    return re.sub(r"\s+", " ", str(value or "").strip()).casefold()

def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("wolof-next-audio-batch-plan.json"))
    parser.add_argument("--batch-size", type=int, default=10)
    parser.add_argument("--start-offset", type=int, default=0,
                        help="Offset into the filtered, sorted candidates (not a generator index).")
    args = parser.parse_args()
    if not 1 <= args.batch_size <= 20 or args.start_offset < 0:
        raise SystemExit("batch-size must be 1..20 and start-offset must be >= 0")

    lexicon_bytes = LEXICON.read_bytes()
    lexicon = json.loads(lexicon_bytes.decode("utf-8"))
    with tempfile.TemporaryDirectory(prefix="wolof-plan-") as tmp:
        candidate_path = Path(tmp) / "kaikki-wolof-candidates.json"
        subprocess.run([sys.executable, str(IMPORTER), "--output", str(candidate_path)],
                       cwd=ROOT, check=True)
        candidate_bytes = candidate_path.read_bytes()
        candidate_payload = json.loads(candidate_bytes.decode("utf-8"))

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
        # Preserve the canonical dictionary entry when a normalized headword collides.
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

    known = {norm(w) for w in KNOWN_AUDIO_HEADWORDS}
    candidates = [row for key, row in merged.items() if key not in known]
    candidates.sort(key=lambda row: (norm(row["wolof"]), row["french"].casefold(), row.get("source", "")))
    selected = candidates[args.start_offset:args.start_offset + args.batch_size]
    plan = {
        "schema_version": 1,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "purpose": "review-only candidate plan; no audio generated and no canonical data modified",
        "source": {"kaikki_page": KAIKKI_PAGE, "kaikki_jsonl": KAIKKI_URL,
                   "kaikki_license_note": LICENSE_NOTE},
        "source_hashes": {"canonical_lexicon_sha256": sha256_bytes(lexicon_bytes),
                          "kaikki_candidates_json_sha256": sha256_bytes(candidate_bytes)},
        "candidate_count_before_exclusions": len(merged),
        "excluded_known_audio_headwords": sorted(known),
        "remaining_candidate_count": len(candidates),
        "start_offset": args.start_offset,
        "selected_count": len(selected),
        "selected": selected,
        "important": [
            "This is a time-specific snapshot of a live upstream dataset, not a permanent vocabulary census.",
            "Review the translations and licenses before publication.",
            "A planned word is not proof that an audio file exists.",
            "All pronunciation validation remains pending until a human listens to the actual WAV.",
        ],
    }
    output = args.output if args.output.is_absolute() else ROOT / args.output
    output.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output.relative_to(ROOT) if output.is_relative_to(ROOT) else output),
        "candidate_count_before_exclusions": len(merged),
        "excluded_known_headwords": len(known),
        "remaining_candidate_count": len(candidates),
        "selected_count": len(selected),
        "candidate_hash": plan["source_hashes"]["kaikki_candidates_json_sha256"],
        "selected_headwords": [row["wolof"] for row in selected],
        "audio_generated": False,
    }, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
