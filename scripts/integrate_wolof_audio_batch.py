#!/usr/bin/env python3
"""Integrate one generated Wolof audio batch without claiming linguistic validation."""
from __future__ import annotations

import argparse
import json
import os
import shutil
import tempfile
import zipfile
from pathlib import Path


def norm(value: str) -> str:
    return " ".join(value.casefold().strip().split())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact-dir", type=Path, required=True)
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    args = parser.parse_args()
    root = args.repo_root.resolve()
    artifact_dir = args.artifact_dir.resolve()
    outer_zip = artifact_dir / "wolof-lexicon-audio-batch.zip"
    if not outer_zip.is_file():
        raise SystemExit(f"Missing workflow artifact archive: {outer_zip}")

    with tempfile.TemporaryDirectory() as temp:
        batch_dir = Path(temp)
        # The workflow artifact download action already unpacks the outer artifact;
        # this remaining ZIP contains the WAVs and their manifests.
        with zipfile.ZipFile(outer_zip) as batch:
            batch.extractall(batch_dir)
            manifest_path = batch_dir / "manifest.json"
            if not manifest_path.is_file():
                raise SystemExit("Audio manifest is missing")
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            records = manifest.get("entries", [])
            if not records:
                raise SystemExit("Audio manifest contains no entries")

            dictionary_path = root / "data/wolof-fr-dictionary.json"
            dictionary = json.loads(dictionary_path.read_text(encoding="utf-8"))
            entries = dictionary.get("entries", [])
            index = {}
            for entry in entries:
                word = str((entry.get("wolof") or {}).get("word") or "")
                if word:
                    index.setdefault(norm(word), []).append(entry)

            audio_dir = root / "audio/wolof"
            audio_dir.mkdir(parents=True, exist_ok=True)
            imported = []
            added_candidates = 0
            for record in records:
                filename = Path(record.get("file", "")).name
                source_wav = batch_dir / filename
                if not filename.endswith(".wav") or not source_wav.is_file():
                    raise SystemExit(f"Missing or invalid WAV in batch: {filename}")
                target = audio_dir / filename
                shutil.copy2(source_wav, target)
                word = str(record.get("wolof") or "").strip()
                if not word:
                    raise SystemExit(f"Missing Wolof headword in manifest entry {filename}")
                matches = index.get(norm(word), [])
                if matches:
                    targets = matches
                else:
                    entry_id = "wolof-audio-candidate-" + str(record.get("id") or filename.rsplit(".", 1)[0])
                    candidate = {
                        "id": entry_id,
                        "soninke": {"word": "", "definition": "", "example": "", "audio_url": ""},
                        "wolof": {"word": word, "definition": "", "example": "", "audio_url": "audio/wolof/" + filename},
                        "fr": {"word": str(record.get("french") or ""), "definition": "", "example": "", "audio_url": ""},
                        "en": {"word": "", "definition": "", "example": "", "audio_url": ""},
                        "sourceExamples": [],
                        "category": "other",
                        "source": str(record.get("source") or "https://kaikki.org/frwiktionary/Wolof/index.html"),
                        "sourceName": str(record.get("source_name") or "Kaikki / Wiktionnaire français"),
                        "license": "Données dérivées de Wiktionnaire : conserver l’attribution et respecter les licences applicables CC BY-SA/GFDL.",
                        "status": "draft",
                        "origin": "external-dictionary-candidate",
                        "pronunciationStatus": "unverified",
                        "translationStatus": "unverified-candidate",
                        "audioStatus": "generated-unvalidated",
                        "audioManifest": "data/wolof-audio-manifest.json",
                    }
                    entries.append(candidate)
                    index.setdefault(norm(word), []).append(candidate)
                    targets = [candidate]
                    added_candidates += 1

                for entry in targets:
                    wolof = entry.setdefault("wolof", {})
                    wolof["audio_url"] = "audio/wolof/" + filename
                    entry["audioStatus"] = "generated-unvalidated"
                    entry["audioManifest"] = "data/wolof-audio-manifest.json"
                    # Never upgrade a pronunciation or translation validation status here.
                    if entry.get("pronunciationStatus") != "validated":
                        entry["pronunciationStatus"] = "unverified"
                    if entry.get("status") not in ("validated",):
                        entry["status"] = "draft"
                imported.append({
                    **record,
                    "file": "audio/wolof/" + filename,
                    "audio_url": "audio/wolof/" + filename,
                    "human_pronunciation_validation": "pending",
                    "translation_validation": "pending" if not matches else record.get("source_translation_status", "unverified"),
                })

            dictionary["entries"] = entries
            dictionary["entryCount"] = len(entries)
            dictionary["audioBatchNote"] = "Les fichiers Wolof générés automatiquement restent des candidats : écouter et valider humainement chaque prononciation avant de la déclarer correcte."
            dictionary_path.write_text(json.dumps(dictionary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            manifest_out_path = root / "data/wolof-audio-manifest.json"
            previous_manifest = {}
            if manifest_out_path.is_file():
                previous_manifest = json.loads(manifest_out_path.read_text(encoding="utf-8"))
            previous_entries = previous_manifest.get("entries", [])
            merged_by_id = {}
            for item in previous_entries:
                if isinstance(item, dict) and item.get("id"):
                    merged_by_id[item["id"]] = item
            for item in imported:
                merged_by_id[item["id"]] = item
            current_run = os.environ.get("AUDIO_RUN_ID", "unknown")
            prior_sources = previous_manifest.get("batchSources", [])
            if not isinstance(prior_sources, list):
                prior_sources = []
            if previous_manifest.get("batchSource"):
                prior_sources.append(previous_manifest["batchSource"])
            current_source = "GitHub Actions artifact run " + current_run
            all_sources = list(dict.fromkeys([*prior_sources, current_source]))
            manifest_out_path.write_text(
                json.dumps({
                    "schemaVersion": 1,
                    "batchSource": current_source,
                    "batchSources": all_sources,
                    "model": manifest.get("model", previous_manifest.get("model", "CONCREE/Adia_TTS")),
                    "technicalValidation": "passed by generator; WAV archive rechecked; publication checks pending",
                    "humanPronunciationValidation": "pending",
                    "translationValidation": "pending for external candidates",
                    "entries": list(merged_by_id.values()),
                }, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            print(f"Integrated {len(imported)} WAVs; added {added_candidates} review-only candidates.")
            print("No entry was marked as linguistically validated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
