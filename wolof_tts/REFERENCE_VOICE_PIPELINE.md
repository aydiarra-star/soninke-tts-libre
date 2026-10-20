# Référence vocale Wolof — garde-fous et état de préparation

## Référence privée

Le fichier de bibliothèque `wolof-reference-private.base64.txt` est une référence privée Ogg Opus d'environ 6,26 s. Il ne doit pas être copié dans Git, un artefact public, le site, les logs CI ou un manifeste public.

Pour GitHub Actions, la valeur base64 doit être fournie séparément comme secret `WOLOF_REFERENCE_AUDIO_B64`. Le workflow ne doit jamais afficher cette variable. Un secret configuré signifie seulement que la référence est disponible au runner, pas que le moteur sait la cloner.

## Exigence non négociable : la voix de l'utilisateur uniquement

Aucune voix de substitution n'est acceptable pour les mots audio Wolof. Le moteur doit être conditionné par l'enregistrement de référence de l'utilisateur et produire une preuve de son utilisation. Ne pas générer ni publier un lot si le moteur ne prend pas en charge cette référence : marquer les entrées `blocked-no-reference-engine` et arrêter le lot.

Les audios Soninké précédemment produits peuvent être évalués comme ressources complémentaires uniquement si leur identité vocale est vérifiée. Ne pas supposer qu'un audio Soninké est la voix source simplement parce qu'il existe ou qu'une prononciation a été validée. Une validation linguistique confirme le contenu/prononciation, pas à elle seule l'identité du locuteur.

La preuve de concept doit être écoutée et validée avant toute production à grande échelle. Les entrées générées ne sont conformes que si la référence a réellement été utilisée et que l'identité vocale a été contrôlée.

## État technique

Le générateur actuel `wolof_tts/generate_lexicon_batch.py` sélectionne `CONCREE/Adia_TTS`. Le manifeste des lots existants ne contient ni empreinte de la référence utilisée, ni statut de vérification d'identité vocale. Les WAV sont donc des candidats techniques, **pas des audios certifiés comme étant la voix de l'utilisateur**.

Il faut choisir explicitement un moteur réellement conditionné par une référence vocale avant de générer les 767 entrées. Valider d'abord une petite preuve de concept (chargement de la référence, génération, comparaison/écoute), puis lancer les lots. Ne pas présenter Adia_TTS comme du clonage vocal sans preuve.

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
