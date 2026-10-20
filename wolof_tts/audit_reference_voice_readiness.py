#!/usr/bin/env python3
"""Audit Wolof audio readiness without exposing or decoding the private reference audio.

This is an audit only: it never generates audio, changes dictionary entries, or prints
secret environment variables. The reference recording must remain in a GitHub Actions
secret named WOLOF_REFERENCE_AUDIO_B64, never in the repository.
"""
import argparse
import json
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def norm(value):
    return re.sub(r"\s+", " ", str(value or "").strip()).casefold()


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dictionary", type=Path, default=ROOT / "data/wolof-fr-dictionary.json")
    parser.add_argument("--manifest", type=Path, default=ROOT / "data/wolof-audio-manifest.json")
    parser.add_argument("--expected-target-count", type=int, default=767)
    parser.add_argument("--output", type=Path, help="Optional JSON report destination")
    args = parser.parse_args()

    dictionary = read_json(args.dictionary)
    manifest = read_json(args.manifest) if args.manifest.exists() else {"entries": []}
    source_entries = dictionary.get("entries", [])
    eligible = []
    missing_french = []
    for entry in source_entries:
        wolof = norm((entry.get("wolof") or {}).get("word"))
        french = str((entry.get("fr") or {}).get("word") or "").strip()
        if not wolof:
            continue
        if not french:
            missing_french.append({"id": entry.get("id", ""), "wolof": wolof})
        eligible.append((wolof, french, entry.get("translationStatus", "source-documented")))

    unique_forms = {row[0] for row in eligible}
    audio_entries = manifest.get("entries", [])
    audio_words = {norm(row.get("wolof")) for row in audio_entries if norm(row.get("wolof"))}
    missing_audio = sorted(unique_forms - audio_words)
    no_reference_model = [
        row for row in audio_entries
        if not row.get("reference_audio_sha256")
        or row.get("voice_identity_validation", "pending") != "verified"
    ]
    uncertain_translations = [
        row for row in audio_entries
        if row.get("translation_validation") in {"unverified-candidate", "needs-review", "uncertain", "missing"}
        or not str(row.get("french") or "").strip()
    ]

    report = {
        "schemaVersion": 1,
        "auditOnly": True,
        "targetDistinctWolofForms": args.expected_target_count,
        "dictionaryEntryCount": len(source_entries),
        "dictionaryDistinctWolofForms": len(unique_forms),
        "targetCountMatches": len(unique_forms) == args.expected_target_count,
        "dictionaryEntriesMissingFrench": len(missing_french),
        "missingFrenchExamples": missing_french[:50],
        "audioManifestEntryCount": len(audio_entries),
        "distinctDictionaryFormsWithoutAudio": len(missing_audio),
        "missingAudioExamples": missing_audio[:50],
        "audioEntriesWithoutVerifiedReferenceVoice": len(no_reference_model),
        "uncertainOrMissingFrenchInAudioManifest": len(uncertain_translations),
        "referenceSecretConfigured": bool(os.environ.get("WOLOF_REFERENCE_AUDIO_B64")),
        "currentManifestModels": sorted({str(row.get("model", "unknown")) for row in audio_entries}),
        "voiceIdentityPolicy": "unverified unless voice_identity_validation=verified with evidence",
        "notes": [
            "A technically valid WAV is not proof of the user's voice.",
            "The current Adia_TTS manifest does not record reference-audio conditioning.",
            "A configured secret alone does not prove the chosen engine supports voice cloning.",
            "Never write the base64 secret, decoded recording, or a private audio URL into repository files or logs."
        ]
    }
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
