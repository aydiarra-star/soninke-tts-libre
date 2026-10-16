#!/usr/bin/env python3
"""Run a local ASR experiment on one user-provided audio file.

This script does not upload the audio for inference. Hugging Face may be contacted
to authenticate and download the gated model weights. The output is experimental.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import soundfile as sf
import torch
from transformers import pipeline

DEFAULT_MODEL = "sil-ai/wav2vec2-bloom-speech-snk"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Transcrire localement un fichier audio avec un modèle ASR Soninké."
    )
    parser.add_argument("--audio", required=True, help="Chemin vers un fichier audio local.")
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"ID Hugging Face (défaut : {DEFAULT_MODEL}).")
    parser.add_argument("--output", help="Chemin JSON de sortie. Sans cette option, écrit dans le terminal.")
    args = parser.parse_args()

    audio_path = Path(args.audio).expanduser().resolve()
    if not audio_path.is_file():
        parser.error(f"Fichier audio introuvable : {audio_path}")

    audio, sample_rate = sf.read(audio_path, dtype="float32", always_2d=True)
    if audio.size == 0:
        parser.error("Le fichier audio est vide.")
    mono = np.mean(audio, axis=1, dtype=np.float32)

    device = 0 if torch.cuda.is_available() else -1
    recognizer = pipeline(
        task="automatic-speech-recognition",
        model=args.model,
        device=device,
    )
    prediction = recognizer({"raw": mono, "sampling_rate": int(sample_rate)})

    report = {
        "task": "experimental_asr",
        "model": args.model,
        "audio_file_name": audio_path.name,
        "sample_rate_hz": int(sample_rate),
        "channels_in_source": int(audio.shape[1]),
        "device": "cuda" if device == 0 else "cpu",
        "transcript": str(prediction.get("text", "")).strip(),
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "warning": (
            "Résultat expérimental non validé. Comparer à une transcription de référence "
            "relue par un locuteur compétent. Ne pas interpréter ce résultat comme une preuve "
            "de qualité générale du modèle."
        ),
    }
    rendered = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        output_path = Path(args.output).expanduser()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(rendered + "\n", encoding="utf-8")
        print(f"Rapport écrit dans : {output_path}")
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
