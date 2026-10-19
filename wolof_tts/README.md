# Wolof TTS batch audio prototype

This isolated work branch uses the open-weight CONCREE/Adia_TTS model (Apache-2.0 model card) to generate three WAVs from the user's linguistically validated entries:

- Jërëjëf — Merci
- Kër — Maison
- Ñëw — Venir

The batch script reopens each saved WAV and checks PCM encoding, sample rate, mono channel count, duration, non-silence, finite samples, and SHA-256. It exports a ZIP plus JSON/CSV manifests.

Important: passing technical checks does not establish correct Wolof pronunciation. human_pronunciation_validation remains pending until a competent Wolof speaker listens to the actual outputs. This model synthesizes a model voice; it does not clone the user's voice.

The GitHub Actions workflow is isolated to feat/wolof-tts-audio-batch; it does not write audio or code to main. Outputs are uploaded as a temporary workflow artifact, not committed to the repository. Model download and CPU inference may take several minutes; the run may fail if dependencies or runner memory change.

CPU runner note: the workflow reinstalls matching CPU-only torch/torchaudio wheels after Parler-TTS dependencies to avoid a CUDA runtime dependency on GitHub's CPU runner.
