# Soninké TTS Libre

Laboratoire open source pour faire progresser la synthèse vocale du soninké, avec une priorité : **ne jamais déclarer une voix fonctionnelle sans audio réellement généré et validé par un locuteur compétent**.

## Prototype actuel

La première version est une interface web statique, utilisable sur téléphone :

- conserve les trois phrases de test fournies exactement : `Daga yige`, `Li tao`, `Daga goli` ;
- permet d’importer et d’écouter un audio existant pour chaque phrase ;
- permet de noter la prononciation « correcte » ou « à corriger » et d’ajouter des remarques ;
- enregistre les annotations dans le navigateur ;
- exporte les métadonnées en JSON ou CSV.

**La synthèse TTS n’est pas encore intégrée.** Le prototype n’invente ni audio ni traduction. Les fichiers audio importés restent sur l’appareil et ne sont pas inclus dans les exports.

## Accès au site

Le workflow GitHub Actions de publication a terminé avec succès sur le commit `21ae5642e3e1b98b1e5ce26d65716608fae2c426`. Cela confirme le déploiement, mais pas encore un test visuel et fonctionnel complet dans Safari sur téléphone.

- Accueil : https://aydiarra-star.github.io/soninke-tts-libre/
- Corpus : https://aydiarra-star.github.io/soninke-tts-libre/corpus.html
- [État du déploiement GitHub Actions](https://github.com/aydiarra-star/soninke-tts-libre/actions/runs/38982991503)
- [Guide de publication et de dépannage](docs/DEPLOYMENT-GITHUB-PAGES.md)

## Espace d’apprentissage multilingue — en développement

Une branche de travail prépare un espace mobile-first pour apprendre **soninké, wolof, français et anglais** :

- [Ouvrir le prototype source](apprendre.html) (la branche doit être publiée pour être consultable comme page web) ;
- [PR #15 — application multilingue](https://github.com/aydiarra-star/soninke-tts-libre/pull/15) ;
- [Instantané du dictionnaire Wolof–Français — 750 fiches sourcées](data/wolof-fr-dictionary.json) ;
- [Catalogue des dictionnaires et licences](data/language-sources.json) ;
- [Plan d’import des dictionnaires](docs/LANGUAGE-DATA-IMPORT-PLAN.md) ;
- [Parcours pédagogique A0–A2](data/learning-curriculum.json).

Le dépôt conserve les 577 entrées soninké et le lot audio proposé dans la PR #14. Le prototype multilingue comprend un instantané de 750 fiches français–wolof issues de 26 pages alphabétiques du dictionnaire Jàngileen, avec une URL source par fiche. Le site indique 911 mots wolof ; les deux compteurs ne sont pas directement comparables, et l’import n’est pas déclaré complet. Les exemples dont la langue ne peut pas être attribuée avec certitude restent signalés comme à vérifier. Aucune traduction soninké ou anglaise n’est inventée pour remplir les champs manquants.

## Ressources de langue

- [Inventaire des dictionnaires, corpus et licences](docs/LEXICAL-RESOURCES.md)
- [Petit échantillon Soninké–français avec attribution](data/soninke-samples.jsonl)
- [Ouvrir la page de recherche et validation du corpus](corpus.html)

La page du corpus permet de rechercher les exemples par soninké ou français, filtrer les validations, enregistrer le résultat et exporter les annotations JSON. Les validations restent locales au navigateur. La page charge le fichier JSONL via HTTP(S) : elle doit être consultée depuis GitHub Pages ou un serveur web, pas nécessairement par ouverture directe du fichier HTML.

L’échantillon provient de `snk_engine`, données sous CC BY 4.0, attribuées à noah-medra. Les phrases sont sourcées mais **n’ont pas encore été revérifiées indépendamment par l’équipe de ce dépôt**. Elles ne sont pas des audios et ne valident pas un moteur TTS. La variété décrite par la source est celle de son locuteur de référence ; elle ne représente pas nécessairement toutes les variétés du soninké. Voir le document de ressources avant toute extension du corpus.

## Utilisation

1. Ouvrir la page du laboratoire via le lien HTTPS ci-dessus.
2. Pour chaque phrase, importer un échantillon audio réellement disponible.
3. Écouter l’échantillon et demander une validation à une personne compétente en soninké.
4. Enregistrer le statut et les remarques, puis exporter JSON ou CSV pour sauvegarder les annotations.

Les annotations sont locales au navigateur et ne se synchronisent pas entre appareils. Les audios sélectionnés devront être réimportés après rechargement.

## État technique et licences

Lire :
- [État des moteurs et preuves disponibles](docs/ENGINE-STATUS.md)
- [Données et validation humaine](docs/DATA-AND-VALIDATION.md)
- [Plan technique STT/TTS et critères d’acceptation](docs/PLAN-STT-TTS.md)
- [Checklist de test manuel sur téléphone](docs/TESTING-CHECKLIST.md)
- [Inventaire des candidats STT/TTS](docs/MODEL-CANDIDATES.md)
- [Notebook OmniVoice personnalisé — génération des trois phrases soninké](notebooks/OmniVoice-Soninke-TTS.ipynb) (ouvrir dans [Google Colab](https://colab.research.google.com/github/aydiarra-star/soninke-tts-libre/blob/feat/soninke-tts-lab-prototype/notebooks/OmniVoice-Soninke-TTS.ipynb))
- [NOUVEAU — Notebook de génération en lot avec reprise et sauvegarde Google Drive](notebooks/OmniVoice-Soninke-Batch-TTS.ipynb) (ouvrir dans [Google Colab](https://colab.research.google.com/github/aydiarra-star/soninke-tts-libre/blob/feat/soninke-batch-dictionary-tts/notebooks/OmniVoice-Soninke-Batch-TTS.ipynb))
- [Guide de génération en lot et validation](docs/BATCH-TTS-GUIDE.md)
- [Modèle CSV de départ](data/soninke-batch-template.csv)
- [Guide du premier essai TTS soninké sur Colab](docs/TTS-QUICKSTART.md)
- [Guide d'enregistrement vocal et consentement](docs/RECORDING-GUIDE.md)
- [Guide du premier essai STT local](docs/STT-QUICKSTART.md)
- [Évaluer le STT avec WER/CER](docs/STT-EVALUATION.md)
- [Inventaire des ressources linguistiques](docs/LEXICAL-RESOURCES.md)
- [Guide de publication GitHub Pages](docs/DEPLOYMENT-GITHUB-PAGES.md)

OmniVoice a été essayé avec la langue Soninke, mais la démo a échoué sur une limite de quota avant de générer un audio. Le moteur n’est donc pas validé. Son code et ses poids ont des conditions de licence différentes ; les poids signalés non commerciaux ne conviennent pas automatiquement à un produit redistribuable ou commercial.

Le code original de ce dépôt est sous MIT. Cette licence **ne couvre pas** les données vocales, les enregistrements de locuteurs, les modèles externes ni leurs poids. Les données réutilisées gardent leurs licences et attributions propres.

## Suite prévue

1. Vérifier l’interface et le format des annotations.
2. Faire relire les exemples de corpus par le référent linguistique, notamment la variété et l’orthographe.
3. Tester un moteur candidat en produisant un vrai audio pour les trois phrases.
4. Faire valider les échantillons par des locuteurs compétents.
5. N’intégrer un moteur qu’après vérification de la qualité, des droits et de la reproductibilité.

## Contribuer

Toute contribution de données vocales doit préciser la provenance, les autorisations, la licence, la transcription vérifiée et les conditions de redistribution. Ne publiez pas de données personnelles ou d’enregistrements sans consentement explicite.
