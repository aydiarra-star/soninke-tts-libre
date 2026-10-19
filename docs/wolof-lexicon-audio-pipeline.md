# Dictionnaire wolof–français et audios associés

## Objectif
Construire progressivement un lexique structuré dans lequel chaque entrée dispose d'une forme wolof, d'une traduction française, d'attributs linguistiques, d'une provenance et d'un emplacement audio stable.

Il n'existe pas de liste finie contenant « tous les mots wolof ». Le premier lot de départ exploite le dictionnaire machine-readable extrait du Wiktionnaire français par Kaikki/Wiktextract. La page source indique environ 1 111 formes distinctes dans sa version consultée. Ce nombre est un point de départ, pas une mesure exhaustive du vocabulaire wolof.

## Données
- `data/wolof/lexicon_seed.csv` : trois entrées confirmées par le référent linguistique du projet : **Jërëjëf → Merci**, **Kër → Maison**, **Ñëw → Venir**.
- `data/wolof/lexicon.csv` : lexique généré par l'importeur. Les entrées importées sont explicitement marquées comme candidates à vérifier.
- `scripts/import_kaikki_wolof.py` : lit le JSONL source et conserve les mots disposant d'au moins une glose.
- `scripts/generate_wolof_adia_samples.py` : produit un lot borné de fichiers WAV et un manifeste CSV contenant le mot, sa traduction, les attributs, le modèle et l'état de validation.

## Attributs de chaque entrée
Identifiant stable, graphie wolof, traduction française/candidats de sens, catégorie grammaticale, définition, source, URL de provenance, licence/provenance, état de validation linguistique, état de validation de la traduction, chemin audio et état audio.

## Génération audio par lots
Le workflow GitHub Actions « Wolof — génération audio du lexique ADIA_TTS » récupère le dictionnaire et génère un lot par exécution. Les paramètres manuels sont :
- `offset` : index de départ (0 au début) ;
- `batch_size` : nombre de mots du lot, limité à 25 ; commencer par 10 pour vérifier durée, mémoire et qualité.

Le workflow utilise `transformers==4.46.1`, la version requise par la dépendance `parler-tts` installée. Les fichiers générés sont conservés dans un artefact temporaire de 14 jours. Il faut télécharger et archiver les lots validés pour éviter de perdre les artefacts temporaires.

## Limites de qualité
- Une glose du Wiktionnaire n'est pas nécessairement une traduction simple, unique ou validée par un locuteur natif.
- Les variantes et formes fléchies peuvent apparaître séparément.
- Une génération WAV réussie ne garantit pas que le modèle prononce correctement chaque mot wolof.
- Les mots importés portent `imported_not_native_validated` et `candidate_translation_review_required`. Ne pas effacer ces marqueurs automatiquement.
- Les trois entrées du fichier seed ont été validées par le référent du projet ; cela ne valide pas automatiquement les audios synthétiques.

## Sources et licence
- Kaikki, dictionnaire wolof extrait du Wiktionnaire français : https://kaikki.org/frwiktionary/Wolof/index.html
- Données Wiktionnaire : vérifier et respecter les conditions d'attribution/partage à l'identique applicables aux données réutilisées. Les sorties de ce pipeline gardent une URL de provenance et un champ de licence à vérifier.
- Modèle ADIA_TTS : https://huggingface.co/CONCREE/Adia_TTS

## Protection et branches
Aucun enregistrement vocal personnel n'est utilisé par ce workflow. Les fichiers personnels et les données Base64 ne doivent jamais être ajoutés au dépôt public. Tout reste sur `feat/wolof-tts-reader-evaluation` ; aucune fusion vers `main` ni aucun déploiement sans accord explicite.
