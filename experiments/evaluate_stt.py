#!/usr/bin/env python3
"""Evaluate local ASR predictions against a reviewed CSV reference manifest."""
from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import soundfile as sf
import torch
from transformers import pipeline

from stt_metrics import character_error_counts, word_error_counts

DEFAULT_MODEL = "sil-ai/wav2vec2-bloom-speech-snk"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Évaluer un modèle STT sur un manifeste CSV avec transcriptions vérifiées."
    )
    parser.add_argument("--manifest", required=True, help="CSV avec audio_path et transcript_reference.")
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"ID Hugging Face (défaut : {DEFAULT_MODEL}).")
    parser.add_argument("--output", default="results/stt-evaluation.json", help="Rapport JSON de sortie.")
    args = parser.parse_args()

    manifest = Path(args.manifest).expanduser().resolve()
    if not manifest.is_file():
        parser.error(f"Manifeste introuvable : {manifest}")

    with manifest.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        parser.error("Le manifeste CSV ne contient aucune ligne.")
    required = {"audio_path", "transcript_reference"}
    missing = required - set(rows[0].keys())
    if missing:
        parser.error("Colonnes obligatoires manquantes : " + ", ".join(sorted(missing)))

    prepared = []
    for index, row in enumerate(rows, start=1):
        reference = (row.get("transcript_reference") or "").strip()
        audio_value = (row.get("audio_path") or "").strip()
        if not reference or not audio_value:
            parser.error(f"Ligne {index} : audio_path et transcript_reference doivent être remplis.")
        audio_path = (manifest.parent / audio_value).resolve()
        if not audio_path.is_file():
            parser.error(f"Ligne {index} : fichier audio introuvable : {audio_value}")
        prepared.append((row.get("utterance_id") or f"utt-{index:04d}", audio_path, reference))

    device = 0 if torch.cuda.is_available() else -1
    recognizer = pipeline("automatic-speech-recognition", model=args.model, device=device)
    results = []
    total_word_errors = total_reference_words = 0
    total_char_errors = total_reference_chars = 0

    for utterance_id, audio_path, reference in prepared:
        audio, sample_rate = sf.read(audio_path, dtype="float32", always_2d=True)
        if audio.size == 0:
            parser.error(f"Audio vide : {audio_path.name}")
        mono = np.mean(audio, axis=1, dtype=np.float32)
        prediction = recognizer({"raw": mono, "sampling_rate": int(sample_rate)})
        hypothesis = str(prediction.get("text", "")).strip()
        word_errors, reference_words = word_error_counts(reference, hypothesis)
        char_errors, reference_chars = character_error_counts(reference, hypothesis)
        total_word_errors += word_errors
        total_reference_words += reference_words
        total_char_errors += char_errors
        total_reference_chars += reference_chars
        results.append({
            "utterance_id": utterance_id,
            "audio_file_name": audio_path.name,
            "reference": reference,
            "hypothesis": hypothesis,
            "word_errors": word_errors,
            "reference_word_count": reference_words,
            "wer": word_errors / reference_words,
            "character_errors": char_errors,
            "reference_character_count": reference_chars,
            "cer": char_errors / reference_chars,
        })

    report = {
        "task": "experimental_stt_evaluation",
        "model": args.model,
        "device": "cuda" if device == 0 else "cpu",
        "manifest_name": manifest.name,
        "sample_count": len(results),
        "aggregate_wer": total_word_errors / total_reference_words if total_reference_words else None,
        "aggregate_cer": total_char_errors / total_reference_chars if total_reference_chars else None,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "warning": (
            "Les références doivent avoir été relues par une personne compétente. "
            "Les scores ne valent que pour ce corpus et sa convention orthographique. "
            "Le script exécute l'inférence localement ; l'authentification et le téléchargement "
            "du modèle peuvent contacter Hugging Face."
        ),
        "items": results,
    }
    output_path = Path(args.output).expanduser()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Rapport écrit : {output_path}")
    print(f"Énoncés : {len(results)} | WER : {report['aggregate_wer']:.4f} | CER : {report['aggregate_cer']:.4f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
