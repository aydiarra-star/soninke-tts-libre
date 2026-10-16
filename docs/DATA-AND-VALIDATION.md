# Données et validation humaine

## Phrases initiales

Ces chaînes doivent rester exactement telles que fournies, sans normalisation automatique :

1. `Daga yige`
2. `Li tao`
3. `Daga goli`

Aucune traduction française n’est fournie. Ne pas en inventer.

## Statuts de validation

- `not_evaluated` : aucun jugement humain consigné.
- `correct` : un validateur compétent juge la prononciation correcte.
- `needs_correction` : le validateur identifie un problème ; ajouter une note utile.

Le statut est une annotation humaine, pas une métrique automatique de qualité. Lorsque c’est possible, documenter le dialecte/variété, le nom ou identifiant choisi par le locuteur, la date, le contexte et le nom du validateur avec son consentement. Ne pas publier de données personnelles sans accord.

## Format exporté

Le prototype exporte les métadonnées en JSON ou CSV. Les fichiers audio ne sont pas téléversés et ne sont pas incorporés aux exports. Le nom du fichier local est une référence indicative seulement : conserver l’audio séparément et établir un manifeste avant tout partage.

Pour constituer un corpus redistribuable, obtenir et archiver :
- consentement explicite du locuteur pour l’enregistrement, le traitement et les usages prévus ;
- licence de redistribution claire pour chaque audio et transcription ;
- provenance et identifiant stables pour chaque enregistrement ;
- validation de la transcription et de la prononciation ;
- procédure de retrait/correction et protection des informations personnelles.

## Limites de cette première version

- Pas de génération TTS.
- Pas d’envoi de fichiers vers un serveur.
- Les annotations sont enregistrées dans le stockage local du navigateur ; elles ne se synchronisent pas entre appareils.
- Les fichiers audio importés ne sont pas persistés après rechargement de la page ; les sélectionner de nouveau pour les écouter.
- L’export est une sauvegarde des métadonnées, pas un dataset audio complet.
