#!/usr/bin/env python3
"""Download Kaikki's French-Wiktionary Wolof data into a separate review-only file.

This intentionally does not merge candidates into the app dictionary. It preserves
source provenance and labels every translation as unverified until reviewed.
"""
import argparse
import json
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

SOURCE_URL = "https://kaikki.org/frwiktionary/Wolof/kaikki.org-dictionary-Wolof.jsonl"
SOURCE_PAGE = "https://kaikki.org/frwiktionary/Wolof/index.html"
LICENSE_NOTE = "Wiktionary-derived data; retain attribution and comply with applicable CC BY-SA/GFDL terms."


def get_french_glosses(record):
    glosses = []
    for sense in record.get("senses", []) or []:
        if not isinstance(sense, dict):
            continue
        values = sense.get("glosses") or []
        if isinstance(values, str):
            values = [values]
        for value in values:
            text = str(value).strip()
            if text and text not in glosses:
                glosses.append(text)
        # Some post-processed records expose a single gloss field.
        single = sense.get("gloss")
        if isinstance(single, str) and single.strip() and single.strip() not in glosses:
            glosses.append(single.strip())
    return glosses


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("data/kaikki-wolof-candidates.json"))
    parser.add_argument("--input-jsonl", type=Path, help="Use an existing JSONL file instead of downloading.")
    args = parser.parse_args()

    if args.input_jsonl:
        lines = args.input_jsonl.read_text(encoding="utf-8").splitlines()
    else:
        request = urllib.request.Request(SOURCE_URL, headers={"User-Agent": "WolofLexiconAudit/1.0 (open-source research)"})
        with urllib.request.urlopen(request, timeout=60) as response:
            raw = response.read().decode("utf-8")
        lines = raw.splitlines()

    candidates = []
    seen = set()
    pos_counts = Counter()
    ignored_non_wolof = 0
    malformed = 0
    for line_number, line in enumerate(lines, 1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            malformed += 1
            continue
        lang_code = str(record.get("lang_code") or record.get("language_code") or "").lower()
        # Fail closed: this source is the French Wiktionary Wolof dictionary.
        # Ignore records that explicitly identify another language.
        if lang_code and lang_code not in {"wo", "wol"}:
            ignored_non_wolof += 1
            continue
        word = str(record.get("word") or "").strip()
        if not word:
            continue
        pos = str(record.get("pos") or "unspecified").strip()
        glosses = get_french_glosses(record)
        if not glosses:
            glosses = [""]
        for gloss in glosses:
            key = (word.casefold(), pos.casefold(), gloss.casefold())
            if key in seen:
                continue
            seen.add(key)
            pos_counts[pos] += 1
            candidates.append({
                "wolof": word,
                "french": gloss,
                "partOfSpeech": pos,
                "source": SOURCE_PAGE,
                "sourceDataset": SOURCE_URL,
                "sourceRecordLine": line_number,
                "licenseNote": LICENSE_NOTE,
                "translationStatus": "unverified-candidate",
                "pronunciationStatus": "unverified",
                "audioUrl": "",
                "audioStatus": "missing",
                "humanReviewRequired": True,
            })

    candidates.sort(key=lambda row: (row["wolof"].casefold(), row["partOfSpeech"], row["french"].casefold()))
    result = {
        "schemaVersion": 1,
        "dataset": "Kaikki / Wiktionnaire français — Wolof",
        "source": SOURCE_PAGE,
        "downloadUrl": SOURCE_URL,
        "extractedAtUtc": datetime.now(timezone.utc).isoformat(),
        "licenseNote": LICENSE_NOTE,
        "candidateCount": len(candidates),
        "uniqueWolofSpellings": len({row["wolof"].casefold() for row in candidates}),
        "partOfSpeechCounts": dict(pos_counts.most_common()),
        "ignoredExplicitlyNonWolofRecords": ignored_non_wolof,
        "malformedJsonLines": malformed,
        "policy": "Review-only candidates. Do not merge automatically into the production dictionary; translations and pronunciations are not user-validated.",
        "entries": candidates,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k != "entries"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
