#!/usr/bin/env python3
"""Fail-closed Wolof TTS using a supplied voice reference with k2-fsa/OmniVoice.

No built-in/automatic speaker fallback is permitted. A generated sample is not
certified as the user's voice until the user has listened and confirmed it.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEXICON = ROOT / "data" / "wolof-fr-dictionary.json"
AUDIO_MANIFEST = ROOT / "data" / "wolof-audio-manifest.json"
MODEL_ID = "k2-fsa/OmniVoice"
# OmniVoice examples write generated samples at 24 kHz. Some package versions
# do not expose model.sampling_rate, so use the documented rate when absent.
DEFAULT_SAMPLE_RATE = 24000
VALIDATED_SEEDS = {"jërëjëf": "Merci", "kër": "Maison", "ñëw": "Venir"}


def norm(value: str) -> str:
    return re.sub(r"\s+", " ", unicodedata.normalize("NFC", value.strip())).casefold()


def prepare_reference(args: argparse.Namespace, tempdir: Path) -> Path:
    source = args.reference_audio
    if source:
        source_path = Path(source).expanduser().resolve()
        if not source_path.is_file():
            raise SystemExit("Référence vocale introuvable.")
    else:
        encoded = os.environ.get("WOLOF_REFERENCE_AUDIO_B64", "")
        if not encoded:
            raise SystemExit(
                "BLOQUÉ : fournir --reference-audio ou le secret "
                "WOLOF_REFERENCE_AUDIO_B64. Aucune voix de substitution ne sera utilisée."
            )
        try:
            raw = base64.b64decode("".join(encoded.split()), validate=True)
        except Exception as exc:
            raise SystemExit("BLOQUÉ : le secret de référence n'est pas un base64 valide.") from exc
        if len(raw) < 1024:
            raise SystemExit("BLOQUÉ : la référence vocale semble vide ou trop courte.")
        source_path = tempdir / "private-reference-source.ogg"
        source_path.write_bytes(raw)

    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise SystemExit("BLOQUÉ : ffmpeg est requis pour convertir la référence en WAV mono.")
    wav_path = tempdir / "private-reference-mono-24k.wav"
    proc = subprocess.run(
        [ffmpeg, "-nostdin", "-hide_banner", "-loglevel", "error", "-y",
         "-i", str(source_path), "-vn", "-ac", "1", "-ar", "24000",
         "-c:a", "pcm_s16le", str(wav_path)],
        capture_output=True, text=True,
    )
    if proc.returncode != 0 or not wav_path.is_file() or wav_path.stat().st_size < 1024:
        raise SystemExit("BLOQUÉ : impossible de décoder la référence vocale en WAV.")
    try:
        import soundfile as sf
        info = sf.info(str(wav_path))
    except Exception as exc:
        raise SystemExit("BLOQUÉ : impossible de contrôler la référence audio.") from exc
    duration = info.frames / info.samplerate if info.samplerate else 0
    if info.channels != 1 or info.samplerate != 24000 or not (3 <= duration <= 10):
        raise SystemExit("BLOQUÉ : la référence doit être mono, 24 kHz et durer entre 3 et 10 secondes.")
    return wav_path


def translation_needs_review(status: object) -> bool:
    value = str(status or "").strip().casefold()
    return any(marker in value for marker in (
        "candidate", "pending", "uncertain", "review", "unverified", "needs-review"
    ))


def select_entries(
    start: int,
    size: int,
    lexicon_payload: dict | None = None,
    manifest_payload: dict | None = None,
) -> list[dict]:
    payload = lexicon_payload
    if payload is None:
        payload = json.loads(LEXICON.read_text(encoding="utf-8"))
    manifest = manifest_payload
    if manifest is None:
        manifest = json.loads(AUDIO_MANIFEST.read_text(encoding="utf-8")) if AUDIO_MANIFEST.is_file() else {"entries": []}

    flagged_audio_words = set()
    for audio_entry in manifest.get("entries", []):
        word = str(audio_entry.get("wolof") or "").strip()
        if not word:
            continue
        statuses = (
            audio_entry.get("translation_validation"),
            audio_entry.get("source_translation_status"),
        )
        if any(translation_needs_review(status) for status in statuses):
            flagged_audio_words.add(norm(word))

    rows = []
    for index, entry in enumerate(payload.get("entries", [])):
        word = str((entry.get("wolof") or {}).get("word") or "").strip()
        french = str((entry.get("fr") or {}).get("word") or "").strip()
        status = (
            entry.get("translationStatus")
            or entry.get("translation_validation")
            or entry.get("source_translation_status")
            or "source-documented"
        )
        if not word or not french or translation_needs_review(status):
            continue
        if norm(word) in flagged_audio_words:
            continue
        rows.append({
            "entry_id": str(entry.get("id") or f"dictionary-row-{index:05d}"),
            "dictionary_index": index,
            "wolof": word,
            "french": french,
            "translation_status": str(status),
        })

    # Keep every dictionary entry, including repeated Wolof headwords with
    # different French senses: the requirement is one audio per entry.
    rows.sort(key=lambda row: (norm(row["wolof"]), row["french"].casefold(), row["entry_id"]))
    return rows[start:start + size]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference-audio", help="Chemin local privé vers l'enregistrement de référence.")
    parser.add_argument("--poc-text", default="Jërëjëf", help="Texte d'un seul test de voix.")
    parser.add_argument("--batch", action="store_true", help="Générer un petit lot du dictionnaire.")
    parser.add_argument("--start-index", type=int, default=0)
    parser.add_argument("--batch-size", type=int, default=1)
    parser.add_argument("--voice-identity-approved", action="store_true",
                        help="À utiliser seulement après écoute et confirmation explicite du test par l'utilisateur.")
    parser.add_argument("--output-dir", type=Path, default=Path("wolof_reference_voice_outputs"))
    args = parser.parse_args()

    if args.batch_size < 1 or args.batch_size > 10 or args.start_index < 0:
        raise SystemExit("BLOQUÉ : batch-size doit être compris entre 1 et 10 et start-index >= 0.")
    if args.batch and not args.voice_identity_approved:
        raise SystemExit(
            "BLOQUÉ : les lots du dictionnaire restent désactivés jusqu'à la validation humaine "
            "du test de référence vocale. Utiliser d'abord --poc-text."
        )
    if args.batch and args.poc_text != "Jërëjëf":
        raise SystemExit("BLOQUÉ : --poc-text ne s'applique pas au mode lot.")
    if not args.batch and args.batch_size != 1:
        raise SystemExit("BLOQUÉ : un test de référence ne génère qu'un seul WAV.")
    if not LEXICON.is_file():
        raise SystemExit(f"Dictionnaire introuvable : {LEXICON}")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="wolof-reference-") as tmp:
        tempdir = Path(tmp)
        reference = prepare_reference(args, tempdir)
        reference_sha256 = hashlib.sha256(reference.read_bytes()).hexdigest()
        try:
            import numpy as np
            import soundfile as sf
            import torch
            from omnivoice import OmniVoice
        except Exception as exc:
            raise SystemExit(
                "BLOQUÉ : dépendances OmniVoice manquantes. Aucun moteur de remplacement ne sera chargé."
            ) from exc

        device = "cuda:0" if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else "cpu")
        model = OmniVoice.from_pretrained(
            MODEL_ID, device_map=device,
            dtype=torch.float16 if device.startswith("cuda") else torch.float32,
        )
        sample_rate = int(getattr(model, "sampling_rate", DEFAULT_SAMPLE_RATE) or DEFAULT_SAMPLE_RATE)
        if sample_rate <= 0:
            raise SystemExit("BLOQUÉ : le moteur n'a pas fourni une fréquence d'échantillonnage valide.")
        if args.batch:
            selected = select_entries(args.start_index, args.batch_size)
            if not selected:
                raise SystemExit("Aucune entrée admissible dans cette plage du dictionnaire.")
        else:
            selected = [{"entry_id": "proof-of-concept", "dictionary_index": -1,
                         "wolof": args.poc_text, "french": VALIDATED_SEEDS.get(norm(args.poc_text), ""),
                         "translation_status": "user-validated-reference" if norm(args.poc_text) in VALIDATED_SEEDS else "needs-review"}]

        records = []
        for offset, item in enumerate(selected, start=args.start_index if args.batch else 0):
            safe_id = f"{offset:05d}-" + re.sub(r"[^a-z0-9]+", "-", norm(item["wolof"])).strip("-")[:40]
            output_path = args.output_dir / f"{safe_id}.wav"
            kwargs = {"text": item["wolof"], "ref_audio": str(reference), "language_id": "wo"}
            reference_transcript = os.environ.get("WOLOF_REFERENCE_TRANSCRIPT", "").strip()
            if reference_transcript:
                kwargs["ref_text"] = reference_transcript
            with torch.inference_mode():
                audio = model.generate(**kwargs)
            samples = audio[0] if isinstance(audio, (list, tuple)) else audio
            if hasattr(samples, "detach"):
                samples = samples.detach().cpu().numpy()
            samples = np.asarray(samples).squeeze()
            if samples.ndim != 1 or samples.size == 0 or not np.isfinite(samples).all():
                raise SystemExit(f"BLOQUÉ : audio invalide pour {item['wolof']!r}.")
            sf.write(str(output_path), samples, sample_rate, subtype="PCM_16")
            with sf.SoundFile(output_path) as wav:
                check = wav.read(dtype="float32")
                rate, channels, subtype = wav.samplerate, wav.channels, wav.subtype
                duration = len(check) / rate
            peak = float(np.max(np.abs(check))) if check.size else 0.0
            if rate != sample_rate or channels != 1 or not (0.15 <= duration <= 15) or peak <= 0.0001 or not np.isfinite(check).all():
                output_path.unlink(missing_ok=True)
                raise SystemExit(f"BLOQUÉ : contrôle technique échoué pour {item['wolof']!r}.")
            records.append({
                "id": safe_id, "entry_id": item["entry_id"], "dictionary_index": item["dictionary_index"],
                "wolof": item["wolof"], "french": item["french"],
                "file": output_path.name, "model": MODEL_ID, "language_id": "wo",
                "sample_rate_hz": rate, "channels": channels, "subtype": subtype,
                "duration_seconds": round(duration, 3), "peak_amplitude": round(peak, 6),
                "sha256": hashlib.sha256(output_path.read_bytes()).hexdigest(),
                "reference_audio_sha256": reference_sha256,
                "voice_engine": MODEL_ID, "generation_status": "generated",
                "technical_validation": "passed", "voice_identity_validation": "pending",
                "pronunciation_validation": "pending",
                "translation_validation": item["translation_status"],
                "generated_at_utc": datetime.now(timezone.utc).isoformat(),
            })
        manifest = {
            "model": MODEL_ID, "language_id": "wo", "reference_audio_sha256": reference_sha256,
            "voice_identity_validation": "pending-user-listening-confirmation",
            "batch_mode": args.batch, "entries": records,
        }
        (args.output_dir / "manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print(f"Génération technique terminée : {len(records)} WAV. Identité vocale : EN ATTENTE.")
        print(f"Manifeste : {args.output_dir / 'manifest.json'}")
        print("La référence privée n'a pas été copiée dans le manifeste; seule son empreinte est conservée.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
