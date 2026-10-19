# Registre des sources lexicales et audio Wolof

Ce registre sert à élargir progressivement le dictionnaire Wolof–français et à attribuer un audio à chaque entrée retenue. Il distingue explicitement la disponibilité d'une ressource, le droit de la réutiliser et la validation linguistique.

## Règles non négociables

- Une ligne lexicale doit garder sa source exacte, sa graphie originale et sa traduction française.
- Ne pas fusionner automatiquement des homonymes, variantes régionales, formes fléchies ou sens différents.
- Un modèle TTS peut produire un WAV, mais cela ne valide ni la prononciation ni la traduction.
- Ne pas importer une ressource dans le dictionnaire distribué tant que ses conditions de réutilisation ne sont pas claires.
- Les corpus de phrases ne sont pas des dictionnaires : ils servent à trouver des candidats après extraction/alignement et contrôle, pas à convertir aveuglément chaque phrase en entrée lexicale.
- Garder les trois références validées par le référent humain : Jërëjëf — Merci ; Kër — Maison ; Ñëw — Venir.

## Sources recensées

| Source | Contenu signalé | Licence / réutilisation | Décision |
|---|---|---|---|
| Jàngileen, dictionnaire français–wolof | Source déjà importée dans `data/wolof-fr-dictionary.json` ; le fichier local indique 750 entrées structurées et 594 formes distinctes après dédoublonnage et séparation des variantes lors de l'analyse du 2026-10-19 | La page « À propos » du site indique que les données du dictionnaire (mots, traductions et exemples) peuvent être redistribuées et modifiées. Reconfirmer les conditions et attribuer la source dans les exports | Source lexicale de départ ; entrées candidates, pas validation automatique |
| Kaikki / Wiktionnaire français | Source lexicale machine-readable mentionnée dans le plan antérieur ; ne pas compter comme intégrée tant que l'import et la licence ne sont pas audités dans le dépôt | Vérifier les licences propres aux données et aux contributions de Wiktionnaire avant réutilisation | À importer et comparer, en gardant l'origine par entrée |
| GalsenAI — Wolof TTS | 40 010 extraits audio et textes associés, corpus de deux locuteurs natifs ; page GalsenAI indique CC BY 4.0 | CC BY 4.0 : attribution requise ; vérifier les fichiers et la carte du jeu de données avant toute redistribution | Ressource prioritaire pour étudier une voix native et un alignement texte/audio. Ce corpus ne fournit pas nécessairement un audio isolé par mot |
| GalsenAI — Anta Women TTS | Environ 19 947 extraits, voix féminine nettoyée, selon la fiche GalsenAI | CC BY 4.0 selon la fiche du catalogue ; confirmer les conditions de la fiche Hugging Face | Option pour un audio de référence de locutrice native ; ne pas prétendre qu'il contient chaque mot du lexique |
| GalsenAI — French-Wolof Translation | 17 777 paires de phrases selon le catalogue GalsenAI | Licence non précisée dans le catalogue : ne pas intégrer ni redistribuer avant clarification | Source potentielle de candidats uniquement après clarification des droits |
| GalsenAI — Centralized Wolof-French Translation Data | 98 345 paires de phrases selon le catalogue GalsenAI, avec traçabilité de provenance annoncée | Licence non précisée dans le catalogue : ne pas intégrer ni redistribuer avant clarification | À examiner pour repérer des candidats et comparer les traductions ; aucune ingestion automatique |
| GalsenAI — Wolof Corpus | 52 706 phrases textuelles selon le catalogue | Licence non précisée dans le catalogue | Ne pas redistribuer sans clarification ; utile comme piste de couverture lexicale si autorisé |
| FLORES-200 | Jeu multilingue d'évaluation, incluant le wolof et le français | CC BY-SA 4.0 selon le catalogue GalsenAI | Phrases d'évaluation, pas un dictionnaire exhaustif ; usage limité et attribution requise |

## Liens de référence

- Jàngileen : https://jangileen.kalam-alami.net/dictionary
- Conditions Jàngileen : https://jangileen.kalam-alami.net/special/apropos
- Catalogue GalsenAI Wolof : https://galsen.ai/datasets/langue/wolof/
- Dataset TTS Wolof (CC BY 4.0) : https://huggingface.co/datasets/galsenai/wolof_tts
- Dataset Anta Women TTS : https://huggingface.co/datasets/galsenai/anta_women_tts
- Corpus de traduction français–wolof : https://huggingface.co/datasets/galsenai/french-wolof-translation
- Traductions centralisées : https://huggingface.co/datasets/galsenai/centralized_wolof_french_translation_data
- Corpus textuel wolof : https://huggingface.co/datasets/galsenai/wolof_corpus
- FLORES-200 : https://huggingface.co/datasets/facebook/flores

## Prochaine méthode d'enrichissement

1. Importer les sources lexicales autorisées et normaliser uniquement les espaces Unicode/variantes techniques, sans effacer les diacritiques wolof.
2. Dédoublonner avec une clé normalisée tout en conservant toutes les variantes et toutes les sources.
3. Repérer les entrées dont les traductions divergent et les marquer `needs-review`.
4. Générer les WAV par lots de taille limitée et conserver un manifeste complet.
5. Valider automatiquement le format et le contenu technique des WAV, puis demander une écoute humaine pour la prononciation.
6. Publier les lots uniquement avec les notices d'attribution et les statuts de validation exacts.

## Objectif de couverture

« Tous les mots wolof » n'a pas de liste finie universelle : la langue évolue, les formes dérivées et conjuguées sont nombreuses, et les variantes dialectales ou orthographiques existent. Le but opérationnel est donc un lexique cumulatif, extensible, sourcé, avec suivi du nombre de formes uniques, des variantes, des traductions à revoir et des audios techniquement générés/validés. Ne jamais afficher une couverture exhaustive tant qu'elle n'est pas démontrable.
