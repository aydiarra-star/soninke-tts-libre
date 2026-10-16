# Checklist de test manuel — téléphone

Ce contrôle complète la CI. Il doit être réalisé dans un vrai navigateur, idéalement sur iPhone Safari, après que la page soit accessible via HTTPS. Ne pas cocher une étape qui n'a pas été exécutée.

## A. Page d'accueil

- [ ] Ouvrir la page du laboratoire.
- [ ] Vérifier que les trois phrases restent exactement : `Daga yige`, `Li tao`, `Daga goli`.
- [ ] Pour chaque phrase, choisir un vrai fichier audio local fourni avec l'autorisation du locuteur.
- [ ] Vérifier que le bouton d'écoute lit le fichier sélectionné.
- [ ] Choisir « correcte », puis « à corriger » et vérifier que le statut affiché suit le choix.
- [ ] Ajouter une remarque, recharger la page et vérifier que les annotations restent disponibles.
- [ ] Exporter JSON puis CSV ; ouvrir les fichiers et confirmer que les trois phrases et leurs statuts sont présents.
- [ ] Vérifier que les fichiers audio ne sont pas inclus dans les exports et que le texte de l'interface l'explique.

## B. Page de recherche du corpus

- [ ] Depuis l'accueil, ouvrir « Rechercher dans le corpus ».
- [ ] Vérifier que les cinq exemples sont chargés et que leurs sources/licences sont visibles.
- [ ] Rechercher un mot soninké puis un mot français ; vérifier que les résultats changent.
- [ ] Changer le filtre de validation et vérifier que les résultats suivent le filtre.
- [ ] Ajouter une note et modifier le statut d'un exemple ; recharger la page et vérifier la persistance locale.
- [ ] Exporter les annotations JSON et vérifier qu'il s'agit d'annotations, pas de fichiers audio.
- [ ] Vérifier que les notes restent sur cet appareil et ne sont pas présentées comme synchronisées.
- [ ] Tester la page sans réseau ou avec le chargement JSONL bloqué : un message d'erreur compréhensible doit apparaître.

## C. Rapport à consigner

- Date et navigateur :
- Appareil :
- URL exacte testée :
- Résultat A (réussi / échoué / non testé) :
- Résultat B (réussi / échoué / non testé) :
- Problèmes observés et étapes pour les reproduire :
- Identifiant du testeur (facultatif, sans publier de données personnelles) :

## Important

Cette checklist ne valide ni la qualité de la prononciation ni un moteur TTS. Les exemples du corpus doivent être relus par une personne compétente en soninké. Ne pas téléverser ou publier un enregistrement sans consentement et droits documentés.
