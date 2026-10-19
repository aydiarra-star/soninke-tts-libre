# Essai vocal wolof ADIA_TTS sans Colab

## Pourquoi cette voie
Cette voie produit une voix synthétique préentraînée en wolof avec `CONCREE/Adia_TTS`. Elle ne clone PAS la voix du propriétaire et n'utilise aucun enregistrement personnel. Elle permet de vérifier le pipeline audio sans compte Colab, secret GitHub ou service d'inférence payant.

## Génération
Le workflow GitHub Actions `Wolof — échantillons de base ADIA_TTS` utilise un runner Ubuntu CPU et génère :
- `Jerejef.wav` pour « Jërëjëf » ;
- `Ker.wav` pour « Kër » ;
- `Ngew.wav` pour « Ñëw » ;
- `manifest.csv` avec les métadonnées et l'état de validation ;
- `README.txt` rappelant les limites.

Les fichiers sont publiés sous l'artefact temporaire `wolof-adia-baseline-samples`, conservé 7 jours. Le modèle fait environ 1,88 Go et demande environ 3,9 Go de RAM selon sa fiche de modèle ; le téléchargement initial peut prendre du temps. Le runner CPU gratuit peut être soumis aux quotas et limites du dépôt.

## Validation obligatoire
Les contrôles automatisés vérifient que les WAV sont non vides, mono, lisibles, au taux d'échantillonnage annoncé et sans valeurs invalides. Ils ne prouvent ni la prononciation wolof correcte ni le naturel de la voix. Le propriétaire doit écouter et valider chaque fichier avant intégration.

## Licence et attribution
La fiche de modèle indique Apache-2.0 et demande de créditer CONCREE / les auteurs d'origine. Référence : https://huggingface.co/CONCREE/Adia_TTS

## Séparation du clonage vocal
La voie Oolel-Voices / OmniVoice avec référence privée reste séparée. Ne jamais committer l'enregistrement ni sa chaîne Base64. Aucune sortie synthétique ADIA_TTS ne doit être présentée comme le clone de la voix du propriétaire.

## Garde-fous
- Tout le travail reste sur `feat/wolof-tts-reader-evaluation`.
- Ne pas fusionner cette PR dans `main` et ne pas déployer avant validation explicite.
- Ne pas lancer de génération à grande échelle avant écoute et validation des trois tests.
