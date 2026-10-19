#!/usr/bin/env python3
"""Generate three Wolof baseline samples with ADIA_TTS (synthetic voice only).

This deliberately does not use, upload, or require the user's private voice
recording. Outputs are technical test artifacts and need human listening.
"""
import csv
import json
from pathlib import Path

import soundfile as sf
import torch
from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer

MODEL_ID = "CONCREE/Adia_TTS"
WORDS = [
    ("Jërëjëf", "Merci", "Jerejef.wav"),
    ("Kër", "Maison", "Ker.wav"),
    ("Ñëw", "Venir", "Ngew.wav"),
]
VOICE_DESCRIPTION = (
    "A clear and educational voice, with a flow adapted to learning"
)


def main() -> None:
    out = Path("wolof-adia-samples")
    out.mkdir(parents=True, exist_ok=True)
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    print(f"Loading {MODEL_ID} on {device}; this may take several minutes.")
    model = ParlerTTSForConditionalGeneration.from_pretrained(MODEL_ID).to(device)
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    model.eval()

    description_ids = tokenizer(
        VOICE_DESCRIPTION, return_tensors="pt"
    ).input_ids.to(device)
    rows = []

    for index, (word, french, filename) in enumerate(WORDS, start=1):
        print(f"Generating {index}/{len(WORDS)}: {word}")
        prompt_ids = tokenizer(word, return_tensors="pt").input_ids.to(device)
        with torch.inference_mode():
            audio = model.generate(
                input_ids=description_ids,
                prompt_input_ids=prompt_ids,
                do_sample=False,
                max_new_tokens=400,
            )
        samples = audio.detach().cpu().float().numpy().squeeze()
        if samples.ndim != 1 or samples.size == 0:
            raise RuntimeError(f"Unexpected audio shape for {word}: {samples.shape}")
        if not torch.isfinite(torch.from_numpy(samples)).all().item():
            raise RuntimeError(f"Non-finite audio samples for {word}")
        if float(abs(samples).max()) == 0.0:
            raise RuntimeError(f"Silent output for {word}")
        target = out / filename
        sample_rate = int(model.config.sampling_rate)
        sf.write(target, samples, sample_rate, subtype="PCM_16")
        info = sf.info(target)
        if info.channels != 1 or info.samplerate != sample_rate or info.duration <= 0:
            raise RuntimeError(f"Audio validation failed for {filename}")
        rows.append({
            "wolof": word,
            "francais": french,
            "audio_file": filename,
            "model": MODEL_ID,
            "sample_rate_hz": info.samplerate,
            "channels": info.channels,
            "duration_seconds": round(info.duration, 3),
            "voice_type": "synthetic_model_voice_not_user_clone",
            "validation_status": "unvalidated_requires_human_listening",
        })
        print(
            f"Saved {filename}: {info.duration:.2f}s, "
            f"{info.samplerate} Hz, mono"
        )

    with (out / "manifest.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    (out / "README.txt").write_text(
        "ADIA_TTS Wolof baseline samples.\n"
        "Synthetic model voice only; this is NOT a clone of the user's voice.\n"
        "Technical checks passed only; pronunciation and naturalness remain unvalidated.\n"
        "Model: CONCREE/Adia_TTS (Apache-2.0; credit the original authors).\n",
        encoding="utf-8",
    )
    print(json.dumps({"output_directory": str(out), "samples": len(rows)}))


if __name__ == "__main__":
    main()
