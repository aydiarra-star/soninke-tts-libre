#!/usr/bin/env python3
"""Generate private, unvalidated Wolof voice-reference samples with Oolel-Voices.

The reference recording is supplied only through WOLOF_REFERENCE_AUDIO_B64.
It is written to a temporary runner directory and is never included in the artifact.
"""
import base64
import csv
import io
import os
import tempfile
import zipfile
from pathlib import Path

import soundfile as sf
import torch
import torchaudio
from transformers import AutoModel
from huggingface_hub import snapshot_download

MODEL_ID = "soynade-research/Oolel-Voices"
WORDS = [
    ("Jërëjëf", "Merci", "Jërëjëf.wav"),
    ("Kër", "Maison", "Kër.wav"),
    ("Ñëw", "Venir", "Ñëw.wav"),
]


def main():
    encoded = os.environ.get("WOLOF_REFERENCE_AUDIO_B64", "").strip()
    if not encoded:
        raise SystemExit(
            "Missing WOLOF_REFERENCE_AUDIO_B64 repository Actions secret. "
            "Do not commit or upload the reference recording to the repository."
        )
    try:
        raw = base64.b64decode(encoded, validate=True)
    except Exception as exc:
        raise SystemExit("WOLOF_REFERENCE_AUDIO_B64 is not valid base64.") from exc
    if not raw:
        raise SystemExit("Reference recording secret decoded to an empty file.")

    out = Path("wolof-voice-reference-output")
    out.mkdir(parents=True, exist_ok=True)
    manifest = []

    with tempfile.TemporaryDirectory(prefix="wolof-voice-ref-") as tmp:
        tmp_path = Path(tmp)
        # Decode the supplied audio without logging it or packaging it.
        source = tmp_path / "reference.m4a"
        source.write_bytes(raw)
        del raw
        try:
            waveform, sample_rate = torchaudio.load(str(source))
        except Exception as exc:
            raise SystemExit(
                "Could not decode the reference audio. Supply a valid M4A/WAV/MP3 "
                "as base64 in the private Actions secret."
            ) from exc
        if waveform.numel() == 0 or not torch.isfinite(waveform).all().item():
            raise SystemExit("Reference audio is empty or contains invalid samples.")
        if waveform.shape[0] > 1:
            waveform = waveform.mean(dim=0, keepdim=True)
        reference_wav = tmp_path / "reference.wav"
        torchaudio.save(str(reference_wav), waveform, sample_rate)
        del waveform

        print(f"Loading {MODEL_ID}; reference audio remains in the temporary runner directory.")
        model_path = snapshot_download(repo_id=MODEL_ID)
        model = AutoModel.from_pretrained(model_path, trust_remote_code=True)
        model.eval()

        for index, (word, french, filename) in enumerate(WORDS, start=1):
            print(f"Generating sample {index}/{len(WORDS)}.")
            with torch.inference_mode():
                audio = model.generate(
                    word,
                    audio_prompt_path=str(reference_wav),
                    cfg_weight=0.5,
                    exaggeration=0.2,
                    temperature=0.3,
                )
            if isinstance(audio, torch.Tensor):
                audio = audio.detach().cpu()
                if audio.ndim == 1:
                    audio = audio.unsqueeze(0)
            else:
                audio = torch.as_tensor(audio)
                if audio.ndim == 1:
                    audio = audio.unsqueeze(0)
            if audio.numel() == 0 or not torch.isfinite(audio).all().item():
                raise RuntimeError(f"Invalid generated audio for {word}.")
            if audio.abs().max().item() == 0:
                raise RuntimeError(f"Silent generated audio for {word}.")
            target = out / filename
            torchaudio.save(str(target), audio, int(model.sr))
            info = sf.info(str(target))
            if info.channels != 1 or info.samplerate != int(model.sr) or info.duration <= 0:
                raise RuntimeError(f"Saved WAV failed technical checks: {filename}")
            manifest.append({
                "wolof": word,
                "francais": french,
                "audio_file": filename,
                "model": MODEL_ID,
                "sample_rate_hz": info.samplerate,
                "channels": info.channels,
                "duration_seconds": round(info.duration, 3),
                "validation_status": "unvalidated_requires_human_listening",
                "voice_reference": "private_user_authorized_reference",
            })
            print(f"Saved {filename}: {info.duration:.2f}s, {info.samplerate} Hz, mono.")

    with (out / "manifest.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(manifest[0].keys()))
        writer.writeheader()
        writer.writerows(manifest)
    (out / "README.txt").write_text(
        "Three Oolel-Voices samples generated with a private voice reference.\n"
        "The source recording is deliberately excluded from this archive and is not committed.\n"
        "All outputs are technically checked but remain UNVALIDATED until listened to by the speaker.\n",
        encoding="utf-8",
    )
    archive = Path("wolof-voice-reference-samples.zip")
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in out.iterdir():
            if path.is_file():
                zf.write(path, arcname=path.name)
    print("Created private-run artifact archive with three unvalidated WAVs.")


if __name__ == "__main__":
    main()
