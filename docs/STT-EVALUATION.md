# Évaluer le STT sur un petit corpus vérifié

Cette procédure compare les prédictions du modèle à une référence humaine. Elle ne fonctionne correctement que si les transcriptions de référence ont été relues par une personne compétente en soninké et si la convention orthographique est définie.

## 1. Préparer le manifeste

Créer un fichier CSV local avec ces colonnes :

```csv
utterance_id,audio_path,transcript_reference
utt-0001,audio/utt-0001.wav,"COLLER ICI LA TRANSCRIPTION VALIDÉE"
```

La valeur illustrative entre crochets doit être remplacée par une vraie transcription validée. Ne jamais utiliser un texte supposé comme référence. Les chemins audio sont relatifs au fichier CSV.

Garder les audios, transcriptions privées et consentements hors du dépôt public, sauf autorisation explicite de publication.

## 2. Préparer l'environnement

Après avoir lu et accepté les conditions d'accès du modèle candidat :
https://huggingface.co/sil-ai/wav2vec2-bloom-speech-snk

Installer les dépendances dans l'environnement Python :

```bash
pip install torch transformers soundfile numpy
hf auth login
```

## 3. Lancer l'évaluation

Depuis la racine du dépôt :

```bash
python experiments/evaluate_stt.py --manifest /chemin/vers/manifest.csv --output results/stt-evaluation.json
```

Le modèle est chargé une seule fois puis chaque fichier est transcrit localement. Le script produit un rapport JSON avec les références, prédictions, erreurs et scores agrégés WER/CER.

- WER = erreurs de mots / nombre de mots de référence.
- CER = erreurs de caractères / nombre de caractères de référence.
- Les scores peuvent dépasser 1 lorsque les insertions sont nombreuses.
- La normalisation ignore la casse et les espaces multiples, mais conserve les accents et les signes diacritiques.
- Ne comparez des scores que si la convention orthographique et la préparation des données sont comparables.

## Limites

Le modèle nécessite un accès accepté sur Hugging Face et peut demander des ressources de calcul et du stockage. Ce script n'envoie pas les audios à un service d'inférence distant, mais l'authentification et le téléchargement du modèle contactent Hugging Face. Les performances annoncées par la fiche du modèle ne sont pas des résultats de ce projet.

Ce script et les tests de métriques sont ajoutés au dépôt, mais aucune évaluation sur des audios soninké réels n'a encore été exécutée.
