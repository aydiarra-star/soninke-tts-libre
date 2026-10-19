#!/usr/bin/env python3
"""Generate one bounded batch of Wolof lexicon audios with ADIA_TTS.

Every imported word is a candidate until a competent speaker validates it.
This script never uses or uploads the user's private voice recording.
"""
import csv
import os
import re
import unicodedata
from pathlib import Path

import soundfile as sf
import torch
from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer

MODEL_ID = "CONCREE/Adia_TTS"
VOICE_DESCRIPTION = "A clear and educational Wolof voice, with a flow adapted to language learning"
ROOT = Path(__file__).resolve().parents[1]
LEXICON = ROOT / "data/wolof/lexicon.csv"
OUT = Path("wolof-adia-samples")


def slug(value: str) -> str:
    ascii_text = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", ascii_text.lower()).strip("-") or "mot"


def main() -> None:
    offset = max(0, int(os.environ.get("WOLOF_OFFSET", "0")))
    batch_size = min(25, max(1, int(os.environ.get("WOLOF_BATCH_SIZE", "10"))))
    if not LEXICON.exists():
        raise SystemExit(f"Lexicon missing: {LEXICON}. Run scripts/import_kaikki_wolof.py first.")
    with LEXICON.open(encoding="utf-8", newline="") as f:
        entries = list(csv.DictReader(f))
    batch = entries[offset:offset + batch_size]
    if not batch:
        raise SystemExit(f"No entries at offset {offset}; lexicon has {len(entries)} entries.")
    OUT.mkdir(parents=True, exist_ok=True)
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    print(f"Loading {MODEL_ID} on {device}; batch {offset}:{offset + len(batch)} / {len(entries)}")
    model = ParlerTTSForConditionalGeneration.from_pretrained(MODEL_ID).to(device)
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    model.eval()
    description_ids = tokenizer(VOICE_DESCRIPTION, return_tensors="pt").input_ids.to(device)
    output_rows = []

    for index, entry in enumerate(batch, start=offset):
        word = entry["wolof"].strip()
        filename = f"{index:05d}_{slug(word)}.wav"
        print(f"Generating {index + 1}/{len(entries)}: {word}")
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
        if not torch.isfinite(torch.from_numpy(samples)).all().item() or float(abs(samples).max()) == 0:
            raise RuntimeError(f"Invalid or silent output for {word}")
        target = OUT / filename
        sample_rate = int(model.config.sampling_rate)
        sf.write(target, samples, sample_rate, subtype="PCM_16")
        info = sf.info(target)
        if info.channels != 1 or info.samplerate != sample_rate or info.duration <= 0:
            raise RuntimeError(f"Audio validation failed for {filename}")
        output_rows.append({
            "lexicon_index": index,
            "id": entry.get("id", ""),
            "wolof": word,
            "francais": entry.get("francais", ""),
            "part_of_speech": entry.get("part_of_speech", ""),
            "audio_file": filename,
            "model": MODEL_ID,
            "sample_rate_hz": info.samplerate,
            "channels": info.channels,
            "duration_seconds": round(info.duration, 3),
            "voice_type": "synthetic_model_voice_not_user_clone",
            "linguistic_status": entry.get("linguistic_status", "not_native_validated"),
            "translation_status": entry.get("translation_status", "review_required"),
            "audio_status": "technical_checks_passed_pronunciation_unvalidated",
            "source": entry.get("source", ""),
            "source_url": entry.get("source_url", ""),
        })
        print(f"Saved {filename}: {info.duration:.2f}s, {info.samplerate} Hz, mono")

    manifest = OUT / "manifest.csv"
    with manifest.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(output_rows[0].keys()))
        writer.writeheader()
        writer.writerows(output_rows)
    (OUT / "README.txt").write_text(
        "Wolof lexicon audio batch generated with ADIA_TTS.\n"
        "Audio is synthetic model voice, NOT a clone of the user's voice.\n"
        "Technical audio checks do not validate Wolof pronunciation or French meaning.\n"
        "Imported dictionary translations and pronunciations require review by a competent Wolof speaker.\n"
        "Model: CONCREE/Adia_TTS. Source data: French Wiktionary via Kaikki/Wiktextract.\n"
        f"Batch offset={offset}; batch size={len(batch)}; lexicon entries={len(entries)}.\n",
        encoding="utf-8",
    )
    print(f"Batch complete: {len(output_rows)} audio files, manifest={manifest}")


if __name__ == "__main__":
    main()
