# Référence vocale Wolof — garde-fous et état de préparation

## Référence privée

Le fichier de bibliothèque `wolof-reference-private.base64.txt` est une référence privée Ogg Opus d'environ 6,26 s. Il ne doit pas être copié dans Git, un artefact public, le site, les logs CI ou un manifeste public.

Pour un workflow GitHub Actions, la valeur base64 doit être fournie séparément comme secret de dépôt `WOLOF_REFERENCE_AUDIO_B64`. Le workflow ne doit jamais afficher cette variable. Un secret configuré signifie seulement que la référence est disponible au runner, pas que le moteur sait la cloner.

## État technique vérifié dans le code actuel

Le générateur `wolof_tts/generate_lexicon_batch.py` sélectionne `CONCREE/Adia_TTS`. Le manifeste des lots existants ne contient ni empreinte de la référence utilisée, ni statut de vérification d'identité vocale. Les WAV sont donc des candidats techniques, **pas des audios certifiés comme étant la voix de l'utilisateur**.

Le pipeline doit choisir explicitement un moteur réellement conditionné par une référence vocale avant de lancer la génération des 767 entrées. Il faut valider une petite preuve de concept (référence chargée, génération réussie, comparaison/écoute de la voix), puis seulement ouvrir la génération par lots. Ne pas faire passer Adia_TTS pour du clonage vocal.

## Statuts requis par entrée

- `generation_status`: `pending`, `generated`, `failed`, `blocked-no-reference-engine`.
- `technical_validation`: `pending`, `passed`, `failed`.
- `voice_identity_validation`: `pending`, `verified`, `rejected`.
- `translation_validation`: `source-documented`, `unverified-candidate`, `needs-review`, `validated`.
- `reference_audio_sha256` et `voice_engine` seulement si une référence a effectivement été utilisée.

Une entrée sans traduction française ne doit pas être supprimée silencieusement du plan : elle doit rester visible avec `translation_validation=needs-review` et être bloquée de la génération destinée aux apprenants jusqu'à correction. Une traduction candidate incertaine reste signalée même si elle est non vide.

## Audit

Exécuter :

```bash
python wolof_tts/audit_reference_voice_readiness.py --output wolof-reference-voice-readiness.json
```

Le rapport est un audit en lecture seule. Il compte les formes distinctes, les entrées sans français, les formes sans audio, les audios dont l'identité vocale n'est pas vérifiée et les traductions à contrôler. Il ne lit ni n'affiche la valeur du secret.
