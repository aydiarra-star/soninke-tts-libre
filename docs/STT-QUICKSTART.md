# Premier essai STT local (Soninké)

Ce protocole est destiné à tester un candidat existant sur un audio que vous êtes autorisé à utiliser. Il ne fournit pas de garantie de transcription et ne remplace pas une évaluation linguistique.

## Prérequis

- Un fichier audio de test obtenu avec le consentement approprié.
- Un compte Hugging Face.
- Avoir consulté puis accepté personnellement les conditions d'accès du modèle : https://huggingface.co/sil-ai/wav2vec2-bloom-speech-snk
- Un environnement Python avec suffisamment de mémoire et d'espace disque. Le téléchargement des poids peut être volumineux ; le CPU peut être lent.

**Important :** la fiche du modèle indique une licence SIL International AI & NLP RAIL-M non commerciale et des conditions d'accès qui peuvent partager l'adresse e-mail et le nom d'utilisateur avec les auteurs. Lisez les conditions avant d'accepter. N'utilisez pas ce candidat dans un service commercial sans autorisation compatible.

## Exécution

Dans un environnement Python (par exemple un notebook Colab que vous contrôlez), installez les dépendances :

```bash
pip install torch transformers soundfile numpy
```

Authentifiez-vous auprès de Hugging Face en suivant la méthode officielle et après avoir accepté l'accès au modèle :

```bash
hf auth login
```

Dans un terminal où le dépôt est disponible :

```bash
python experiments/stt_transcribe.py --audio /chemin/vers/test.wav --output results/transcription.json
```

Le script :
- lit un fichier audio local ;
- utilise le candidat `sil-ai/wav2vec2-bloom-speech-snk` par défaut ;
- exécute l'inférence dans l'environnement local (CPU ou GPU détecté) ;
- écrit la transcription et les métadonnées dans un JSON.

L'audio n'est pas envoyé à un service d'inférence distant par ce script. Hugging Face peut être contacté pour l'authentification et le téléchargement du modèle. Ne placez jamais un jeton d'accès dans le dépôt.

## Comment juger le résultat

1. Faire transcrire le même audio indépendamment par une personne compétente en soninké.
2. Comparer la sortie exacte au texte de référence, avec une convention orthographique explicitée.
3. Noter les mots omis, substitutions, répétitions, noms propres et différences de variété.
4. Tester plusieurs phrases inédites avant de calculer WER/CER.
5. Garder le résultat dans un rapport expérimental ; ne pas l'ajouter au corpus de référence comme texte correct sans relecture.

Le script n'a pas encore été exécuté sur un audio soninké dans ce dépôt. Le modèle est un candidat, pas une fonctionnalité intégrée ou validée.
