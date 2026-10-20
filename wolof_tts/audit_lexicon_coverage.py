#!/usr/bin/env python3
"""Read-only coverage audit for the Wolof–French lexicon.

Never edits the source dictionary or marks a pronunciation as validated.
"""
import argparse
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LEXICON = ROOT / "data" / "wolof-fr-dictionary.json"


def clean(value):
    return re.sub(r"\s+", " ", str(value or "")).strip()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--lexicon", type=Path, default=DEFAULT_LEXICON)
    parser.add_argument("--report", type=Path, default=Path("wolof-lexicon-audit.json"))
    args = parser.parse_args()

    payload = json.loads(args.lexicon.read_text(encoding="utf-8"))
    entries = payload.get("entries", [])
    if not isinstance(entries, list):
        raise SystemExit("Invalid lexicon: 'entries' must be a list")

    source_counts = Counter()
    status_counts = Counter()
    unique_words = {}
    missing_wolof = missing_fr = missing_audio = 0
    variant_candidates = 0
    report_entries = []

    for row in entries:
        if not isinstance(row, dict):
            continue
        wolof = clean((row.get("wolof") or {}).get("word"))
        french = clean((row.get("fr") or {}).get("word"))
        audio = clean((row.get("wolof") or {}).get("audio_url"))
        if not wolof:
            missing_wolof += 1
            continue
        if not french:
            missing_fr += 1
        if not audio:
            missing_audio += 1
        source_counts[clean(row.get("sourceName") or row.get("source") or "source inconnue")] += 1
        status_counts[clean(row.get("pronunciationStatus") or "non renseigné")] += 1
        if "/" in wolof:
            variant_candidates += 1
        key = wolof.casefold()
        unique_words.setdefault(key, {"wolof": wolof, "french": french, "source": clean(row.get("source"))})
        report_entries.append({
            "id": clean(row.get("id")),
            "wolof": wolof,
            "french": french,
            "audio_url": audio,
            "source": clean(row.get("source")),
            "pronunciation_status": clean(row.get("pronunciationStatus") or "unverified"),
            "translation_status": clean(row.get("translationStatus") or "unspecified"),
        })

    report = {
        "schemaVersion": 1,
        "auditType": "read-only-coverage-audit",
        "sourceFile": str(args.lexicon),
        "sourceEntryCount": len(entries),
        "validWolofEntryCount": len(report_entries),
        "uniqueWolofSpellingsCaseInsensitive": len(unique_words),
        "missingWolofCount": missing_wolof,
        "missingFrenchTranslationCount": missing_fr,
        "missingAudioReferenceCount": missing_audio,
        "slashSeparatedVariantCandidates": variant_candidates,
        "sourceCounts": dict(source_counts.most_common()),
        "pronunciationStatusCounts": dict(status_counts.most_common()),
        "entries": report_entries,
        "notes": [
            "Audio URL presence is not proof that the file is accessible, licensed, or linguistically correct.",
            "TTS technical success is not pronunciation validation.",
            "No source data was modified by this audit."
        ]
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k != "entries"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
