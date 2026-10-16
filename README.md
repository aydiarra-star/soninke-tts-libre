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

## Ressources de langue

- [Inventaire des dictionnaires, corpus et licences](docs/LEXICAL-RESOURCES.md)
- [Petit échantillon Soninké–français avec attribution](data/soninke-samples.jsonl)
- [Ouvrir la page de recherche et validation du corpus](corpus.html)

La page du corpus permet de rechercher les exemples par soninké ou français, filtrer les validations, enregistrer le résultat et exporter les annotations JSON. Les validations restent locales au navigateur. La page charge le fichier JSONL via HTTP(S) : elle doit être consultée depuis GitHub Pages ou un serveur web, pas nécessairement par ouverture directe du fichier HTML.

L’échantillon provient de `snk_engine`, données sous CC BY 4.0, attribuées à noah-medra. Les phrases sont sourcées mais **n’ont pas encore été revérifiées indépendamment par l’équipe de ce dépôt**. Elles ne sont pas des audios et ne valident pas un moteur TTS. La variété décrite par la source est celle de son locuteur de référence ; elle ne représente pas nécessairement toutes les variétés du soninké. Voir le document de ressources avant toute extension du corpus.

## Utilisation

1. Ouvrir `index.html` dans un navigateur, ou activer GitHub Pages pour publier cette interface statique.
2. Pour chaque phrase, importer un échantillon audio réellement disponible.
3. Écouter l’échantillon et demander une validation à une personne compétente en soninké.
4. Enregistrer le statut et les remarques, puis exporter JSON ou CSV pour sauvegarder les annotations.

Les annotations sont locales au navigateur et ne se synchronisent pas entre appareils. Les audios sélectionnés devront être réimportés après rechargement.

## État technique et licences

Lire :
- [État des moteurs et preuves disponibles](docs/ENGINE-STATUS.md)
- [Données et validation humaine](docs/DATA-AND-VALIDATION.md)
- [Inventaire des ressources linguistiques](docs/LEXICAL-RESOURCES.md)

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
