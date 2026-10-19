#!/usr/bin/env python3
"""Build a reviewable Wolof–French lexicon from the French Wiktionary extract.

Imported translations are candidates, not native-speaker validated entries.
The user's three validated entries always take precedence.
"""
import csv
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/wolof/source/kaikki-frwiktionary-wolof.jsonl"
SEED = ROOT / "data/wolof/lexicon_seed.csv"
OUTPUT = ROOT / "data/wolof/lexicon.csv"
FIELDS = [
    "id", "wolof", "francais", "part_of_speech", "definition_fr",
    "source", "source_url", "source_license", "linguistic_status",
    "translation_status", "audio_file", "audio_status",
]


def slug(value: str) -> str:
    ascii_text = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", ascii_text.lower()).strip("-") or "mot"


def read_seed():
    with SEED.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def main():
    if not SOURCE.exists():
        raise SystemExit(f"Source missing: {SOURCE}")
    rows = read_seed()
    seen = {r["wolof"].strip().casefold() for r in rows}
    imported = 0
    with SOURCE.open(encoding="utf-8") as f:
        for line in f:
            try:
                item = json.loads(line)
            except json.JSONDecodeError:
                continue
            word = str(item.get("word", "")).strip()
            if not word or word.casefold() in seen:
                continue
            pos = str(item.get("pos", "")).strip()
            senses = item.get("senses") or []
            glosses = []
            for sense in senses:
                for gloss in (sense.get("glosses") or sense.get("raw_glosses") or []):
                    gloss = re.sub(r"\s+", " ", str(gloss)).strip()
                    if gloss and gloss not in glosses:
                        glosses.append(gloss)
            if not glosses:
                continue
            french = " ; ".join(glosses[:3])
            entry_id = "wiktionary-" + slug(word)
            rows.append({
                "id": entry_id,
                "wolof": word,
                "francais": french,
                "part_of_speech": pos,
                "definition_fr": french,
                "source": "Wiktionnaire français via Kaikki/Wiktextract",
                "source_url": "https://kaikki.org/frwiktionary/Wolof/index.html",
                "source_license": "Wiktionary data: CC BY-SA; verify upstream terms and attribution",
                "linguistic_status": "imported_not_native_validated",
                "translation_status": "candidate_translation_review_required",
                "audio_file": f"audio/{slug(word)}.wav",
                "audio_status": "pending",
            })
            seen.add(word.casefold())
            imported += 1
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Lexicon built: {len(rows)} entries ({imported} imported candidates, 3 seed entries).")
    print(f"Output: {OUTPUT}")


if __name__ == "__main__":
    main()
