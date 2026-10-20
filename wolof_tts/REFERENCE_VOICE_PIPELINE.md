# Référence vocale Wolof — garde-fous et état de préparation

## Référence privée

Le fichier de bibliothèque `wolof-reference-private.base64.txt` est une référence privée Ogg Opus d'environ 6,26 s. Il ne doit pas être copié dans Git, un artefact public, le site, les logs CI ou un manifeste public.

Pour GitHub Actions, la valeur base64 doit être fournie séparément comme secret `WOLOF_REFERENCE_AUDIO_B64`. Le workflow ne doit jamais afficher cette variable. Un secret configuré signifie seulement que la référence est disponible au runner, pas que le moteur sait la cloner.

## Exigence non négociable : la voix de l'utilisateur uniquement

Aucune voix de substitution n'est acceptable pour les mots audio Wolof. Le moteur doit être conditionné par l'enregistrement de référence de l'utilisateur et produire une preuve de son utilisation. Ne pas générer ni publier un lot si le moteur ne prend pas en charge cette référence : marquer les entrées `blocked-no-reference-engine` et arrêter le lot.

Les audios Soninké précédemment produits peuvent être évalués comme ressources complémentaires uniquement si leur identité vocale est vérifiée. Ne pas supposer qu'un audio Soninké est la voix source simplement parce qu'il existe ou qu'une prononciation a été validée. Une validation linguistique confirme le contenu/prononciation, pas à elle seule l'identité du locuteur.

La preuve de concept doit être écoutée et validée avant toute production à grande échelle. Les entrées générées ne sont conformes que si la référence a réellement été utilisée et que l'identité vocale a été contrôlée.

## État technique et moteur de référence

Le générateur historique `wolof_tts/generate_lexicon_batch.py` sélectionne `CONCREE/Adia_TTS` sans lui passer la référence. Ses WAV restent des candidats techniques, **pas des audios certifiés comme étant la voix de l'utilisateur**.

Une nouvelle voie isolée est ajoutée dans `wolof_tts/generate_reference_voice_batch.py`, fondée sur `k2-fsa/OmniVoice` (licence Apache-2.0). Sa documentation amont décrit le clonage zéro-shot avec `ref_audio` et liste le wolof parmi les 646 langues (ID de langue `wo`). Cela justifie un test contrôlé, mais ne prouve ni la qualité du wolof produit ni l'identité vocale du résultat. Références : [dépôt OmniVoice](https://github.com/k2-fsa/OmniVoice) et [table des langues](https://huggingface.co/spaces/phinam112/OmniVoice-Studio/blob/main/docs/languages.md).

### Preuve de concept — un seul mot

Installer dans un environnement Python adapté : `pip install omnivoice soundfile` (PyTorch doit être installé selon le matériel) et rendre `ffmpeg` disponible. Puis fournir le fichier privé localement avec `--reference-audio`, ou définir le secret d'environnement `WOLOF_REFERENCE_AUDIO_B64` sans l'afficher dans les logs.

```bash
python wolof_tts/generate_reference_voice_batch.py \\
  --reference-audio /chemin/prive/reference.ogg \\
  --poc-text 'Jërëjëf' \\
  --output-dir wolof_reference_voice_outputs
```

Si le texte exact de la référence est connu et validé, il peut être fourni via `WOLOF_REFERENCE_TRANSCRIPT`. Sinon, OmniVoice peut tenter sa transcription automatique ; elle doit être considérée comme incertaine tant qu'elle n'est pas vérifiée. Le script convertit la référence en WAV mono 24 kHz, vérifie sa durée (3–10 s), transmet explicitement `ref_audio` et `language_id='wo'`, et arrête le traitement si une dépendance ou la référence manque. Il n'a aucun fallback vers une voix prédéfinie.

Le manifeste garde l'empreinte de la référence effectivement transmise, mais **ne déclare jamais l'identité vocale comme vérifiée**. L'utilisateur doit écouter le WAV et confirmer la ressemblance avant d'autoriser le mode lot. Après cette confirmation uniquement, un lot limité peut être lancé avec `--batch --voice-identity-approved`; la taille est limitée à 10 par exécution. Les traductions marquées incertaines sont exclues du lot.

Cette nouvelle voie n'a pas encore été exécutée dans un environnement doté des dépendances/modèle, et aucun WAV de test n'a été produit ou validé à ce stade.

## Statuts par entrée

- `generation_status`: `pending`, `generated`, `failed`, `blocked-no-reference-engine`.
- `technical_validation`: `pending`, `passed`, `failed`.
- `voice_identity_validation`: `pending`, `verified`, `rejected`.
- `translation_validation`: `source-documented`, `unverified-candidate`, `needs-review`, `validated`.
- `reference_audio_sha256` et `voice_engine` seulement si la référence a effectivement été utilisée.

Une entrée sans traduction française ne doit pas disparaître silencieusement du plan : elle doit rester visible avec `translation_validation=needs-review` et être bloquée de la génération destinée aux apprenants jusqu'à correction. Une traduction candidate incertaine reste signalée même si elle n'est pas vide.

## Audit en lecture seule

```bash
python wolof_tts/audit_reference_voice_readiness.py --output wolof-reference-voice-readiness.json
```

Le rapport compte les formes distinctes, les entrées sans français, les formes sans audio, les audios dont l'identité vocale n'est pas vérifiée et les traductions à contrôler. Il ne lit ni n'affiche la valeur du secret.
