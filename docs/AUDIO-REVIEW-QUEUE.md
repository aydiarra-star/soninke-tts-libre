# File de revue audio — Xam Xam Xara

Cette file suit les candidats audio sans confondre génération technique, exactitude de la traduction et validation de prononciation.

## Règles de revue

- Ne jamais marquer une prononciation comme validée sur la seule base du contrôle WAV.
- Écouter le fichier réel et vérifier que le mot entendu correspond à la graphie wolof.
- Faire confirmer la graphie, le sens français et la prononciation par un locuteur compétent.
- Si un point est incertain, conserver le statut « à vérifier » et une note explicite.
- Ne pas remplacer un WAV existant sans comparer son SHA-256 et documenter la raison.
- Conserver la provenance de chaque entrée et les licences des sources.
- Pour le Soninké, ne produire aucun audio fictif : n’ajouter un fichier que si un moteur a effectivement généré le WAV et que l’artefact a été contrôlé.

## Lot Wolof déjà intégré — 10 candidats

Tous les éléments ci-dessous sont à revoir. Leur présence dans le site ne signifie pas que la prononciation ou la traduction sont validées.

| Graphie | Traduction candidate du manifeste | Prononciation humaine | Traduction |
|---|---|---|---|
| abal | Prêter. | À écouter / valider | À vérifier |
| adarees | Adresse. | À écouter / valider | À vérifier |
| Addis-Abeba | Addis-Abeba (capitale de l’Éthiopie). | À écouter / valider | À vérifier |
| adduna | Monde. | À écouter / valider | À vérifier |
| afeer | L’affaire. | À écouter / valider | À vérifier |
| Almaañ | Allemagne (pays européen). | À écouter / valider | À vérifier |
| almet | Allumette. | À écouter / valider | À vérifier |
| alxames | jeudi | À écouter / valider | Source documentaire présente ; confirmation humaine attendue |
| am | avoir | À écouter / valider | Source documentaire présente ; confirmation humaine attendue |
| amam | Richesse. | À écouter / valider | À vérifier |

Manifeste source : `data/wolof-audio-manifest.json`. Les fichiers sont référencés sous `audio/wolof/`. Consulter les URLs de provenance et les empreintes SHA-256 dans le manifeste avant toute correction.

## Protocole du prochain lot Wolof

1. Sélectionner au plus 10 entrées inédites au premier passage.
2. Écarter les doublons exacts ; préserver les variantes orthographiques comme variantes, sans les fusionner automatiquement.
3. Exiger une source traçable et une traduction candidate clairement séparée du statut de validation.
4. Générer les WAV dans un lot isolé, puis contrôler la lecture, la durée, le nombre de canaux, la fréquence, l'encodage et les empreintes.
5. Vérifier que les fichiers référencés existent et que les lecteurs du site les chargent depuis l'URL publiée.
6. Ouvrir une PR avec manifeste et rapport de contrôle. Ne pas fusionner en cas d'échec ou de provenance manquante.

## Enrichissement Soninké

- Inventaire de référence actuel : 577 entrées, 576 WAV ; l'absence de `snk-00308` reste explicite.
- Réutiliser les audios existants sans les modifier.
- Les nouvelles générations restent bloquées jusqu'à l'obtention d'un vrai artefact audio et à la vérification des licences du moteur et de ses poids.
- Garder distincts : disponibilité audio, contrôle technique, validation de transcription, validation de prononciation et validation de traduction.

## Critères de sortie d'un lot

- [ ] Aucun identifiant ni chemin audio dupliqué.
- [ ] Aucun fichier existant écrasé silencieusement.
- [ ] Manifeste JSON/CSV et empreintes SHA-256 cohérents.
- [ ] Tous les fichiers annoncés disponibles existent réellement.
- [ ] Contrôles statiques et workflow réussis.
- [ ] Validation humaine toujours explicite, jamais déduite du succès CI.
- [ ] Vérification Safari/iPhone suivie séparément des tests automatisés.
