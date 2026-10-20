# Wolof–French lexicon automation checkpoint — 2026-10-20

## Scope and safety

- Working branch: `feat/wolof-lexicon-audio-batches`.
- Keep all lexical candidates and generated WAVs review-only until human review.
- Do not merge or close PRs; do not write to `main`.
- Never overwrite existing dictionary rows or audio. Keep source URLs, dataset attribution, license notes, source translation status, technical validation, and human pronunciation validation separate.

## Verified GitHub Actions state

- Audio run: https://github.com/aydiarra-star/soninke-tts-libre/actions/runs/39302188446
- Latest job ID: `118260294259`, conclusion: `success`.
- Audio artifact: https://github.com/aydiarra-star/soninke-tts-libre/actions/runs/39302188446/artifacts/12215499007
- Artifact ID: `12215499007`; SHA-256: `68e8a08fe1dc6f11309f5ef78917b150f70c72987eddea8d761d6a32611b74f7`; expiry: 2026-11-02.
- Log confirms candidate count 1,316, selected range 10:20, and ten technically verified WAVs: `ag`, `agsil ak jàmm ci sa kër`, `ak`, `aksidaa`, `alal`, `alarba`, `Albaani`, `Alemaañ`, `alkaati`, `all`.
- Audio artifact uploads are temporary (14-day retention); they are not committed to the canonical dictionary.
- Kaikki audit run: https://github.com/aydiarra-star/soninke-tts-libre/actions/runs/39302087424
- Audit artifact: https://github.com/aydiarra-star/soninke-tts-libre/actions/runs/39302087424/artifacts/12210589358

## Critical reproducibility issue

The workflow imports Kaikki live on every run and then sorts the combined candidate set before selecting a numeric slice. Earlier runs used a different candidate set (reported as 617 rows); the current run used 1,316. Numeric indices are therefore not guaranteed to refer to the same words across runs. The successful 10:20 artifact overlaps earlier audio for four headwords (`ag`, `ak`, `alal`, `alkaati`). Do not assume index 20 is safe until the candidate snapshot/order is pinned.

## Required next technical steps

1. Pin a versioned Kaikki input snapshot or store a hash-addressed candidate manifest; keep the original source URL, retrieval timestamp, license note, and source record line.
2. Build a stable batch plan from normalized headwords, preserving spelling variants as explicit separate entries where appropriate. Deduplicate on a reviewed lexical identity, not just the display string.
3. Compare the proposed next batch against every available prior manifest/artifact before inference; skip already-generated identities without deleting any artifact.
4. Include the candidate-set hash, source snapshot hash, model ID, audio SHA-256, and human pronunciation state in every manifest.
5. Continue in small batches only after the candidate plan is stable. Keep `human_pronunciation_validation: pending` for generated audio.
6. Retain a source/license manifest for both Jàngileen and Kaikki/Wiktionnaire; never auto-promote candidate translations into the canonical dictionary.

## Known limitation

The available GitHub connector in this execution can inspect runs, jobs, logs, artifacts, and branch files, but exposes no workflow-dispatch operation. A new audio run cannot be safely started manually through this connector. A commit that triggers the existing workflow would currently default to start index 10 and risk repeating the same slice; do not use that workaround.

## Validation status

- Audio artifact: ten WAVs technically checked by the workflow; no claim of linguistically correct pronunciation.
- Human pronunciation: pending for all generated entries.
- Canonical dictionary: unchanged by this checkpoint.
- `main`: unchanged.
- PR: no merge or closure performed.
