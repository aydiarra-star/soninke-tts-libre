# Guide — génération TTS soninké en lot

## Notebook

Ouvrir le notebook dans Google Colab :
https://colab.research.google.com/github/aydiarra-star/soninke-tts-libre/blob/feat/soninke-batch-dictionary-tts/notebooks/OmniVoice-Soninke-Batch-TTS.ipynb

Notebook source : [OmniVoice-Soninke-Batch-TTS.ipynb](../notebooks/OmniVoice-Soninke-Batch-TTS.ipynb)

## Ce que l'automatisation fait

- Monte Google Drive et enregistre durablement les WAV, le manifeste et une playlist.
- Reprend les fichiers déjà générés après une interruption au lieu de les recréer.
- Lit une liste CSV, une ligne par mot ou expression.
- Produit un WAV par ligne avec le modèle OmniVoice et la référence vocale.
- Enregistre les erreurs et quelques contrôles techniques (présence, durée, amplitude).
- Prépare un manifeste à annoter et une archive de sauvegarde.

## Première utilisation

1. Ouvrir le notebook dans Colab et sélectionner un GPU gratuit s'il est disponible. Ne rien acheter.
2. Exécuter les cellules dans l'ordre.
3. Lorsqu'il le demande, téléverser depuis l'iPhone les deux enregistrements originaux nommés exactement `Daga goli.wav` et `Li taxu.wav`, ou un fichier `reference_soninke.wav` existant.
4. Le notebook crée `MyDrive/SONINKE_TTS_LIBRE` dans Google Drive. C'est là que les résultats persistent après la fermeture de Colab.
5. La première liste `wordlist.csv` est créée à partir de `data/soninke-batch-template.csv`. Pour ajouter des entrées, modifier ce CSV dans Drive en gardant les colonnes `id,text,source,license`, avec un identifiant unique par ligne.
6. Relancer la cellule de génération autant de fois que nécessaire. Les WAV présents sont réutilisés ; les erreurs restent visibles.
7. Télécharger l'archive ZIP de sauvegarde et vérifier son contenu.

## Dictionnaire : règle impérative

Le notebook récupère automatiquement le lexique grammatical, les objets/compléments et les mots présents dans les corpus de `snk_engine`, à la révision épinglée dans le notebook. Le fichier `LICENSE-DATA` confirme la licence CC BY 4.0 pour `data/` et `corpus/`, avec attribution à noah-medra (ORCID 0009-0003-6018-9802). La liste obtenue est une base lexicale sourcée, **pas un dictionnaire exhaustif de tout le soninké**. Les tokens extraits de phrases perdent leur contexte ; ils doivent être vérifiés. La variété de référence ne représente pas nécessairement toutes les variétés. La source Asawan reste recensée dans `docs/LEXICAL-RESOURCES.md`, mais son contenu n'est pas copié tant que ses droits ne sont pas établis.

## Ce que l'automatisation ne peut pas déclarer

La réussite technique ne prouve pas qu'un mot est orthographié correctement ni que l'audio est correctement prononcé. Il n'existe pas encore, dans ce dépôt, de vérificateur indépendant et suffisamment validé pour certifier automatiquement la prononciation soninké de chaque mot. Le référent linguistique peut écouter le fichier `review_playlist.wav` en une seule lecture, en suivant l'ordre du manifeste, et inscrire les décisions/corrections dans `manifest.csv`. Un éventuel moteur STT ne peut fournir qu'un indice tant que sa précision en soninké n'a pas été évaluée.

## Confidentialité et licence

- Les audios sont enregistrés dans Google Drive, pas dans GitHub.
- Ne pas téléverser des voix privées dans le dépôt public sans autorisation explicite.
- Les poids pré-entraînés OmniVoice sont indiqués comme soumis à des restrictions non commerciales dans la documentation du projet. Ne pas les utiliser pour un service commercial sans autorisation compatible.
- Le notebook utilise les ressources GPU gratuites si disponibles ; aucune disponibilité n'est garantie.
