# Publication du prototype sur GitHub Pages

## État actuel

Le dépôt contient un site HTML/CSS/JavaScript statique. La présence du code ne signifie pas que le site est déjà publié. L’URL publique attendue, une fois la publication activée, est :

- Accueil : https://aydiarra-star.github.io/soninke-tts-libre/
- Corpus : https://aydiarra-star.github.io/soninke-tts-libre/corpus.html

## Configuration initiale (à faire une seule fois)

1. Ouvrir https://github.com/aydiarra-star/soninke-tts-libre/settings/pages en étant connecté au compte propriétaire.
2. Dans **Build and deployment**, choisir **Source: GitHub Actions**.
3. Enregistrer si GitHub présente un bouton de confirmation.
4. Ouvrir l’onglet **Actions**, sélectionner **Publier le prototype sur GitHub Pages**, puis **Run workflow** sur la branche voulue lorsque cette branche contient le workflow.
5. Attendre la fin du travail **build** puis **deploy**. Le lien public est également indiqué dans l’environnement **github-pages** du run réussi.

## Déploiements suivants

Après fusion approuvée vers `main`, chaque push sur `main` déclenche le workflow de publication. Le workflow peut aussi être lancé manuellement depuis l’onglet Actions.

## Dépannage

- **404 / page inaccessible** : vérifier que GitHub Pages est configuré sur **GitHub Actions**, que le workflow s’est terminé avec succès et que l’URL correspond exactement au nom du dépôt.
- **Workflow absent** : GitHub Actions n’affiche généralement que les workflows présents sur la branche sélectionnée. Vérifier la branche qui contient `.github/workflows/pages.yml`.
- **Page d’accueil visible mais corpus en erreur** : ouvrir `/soninke-tts-libre/corpus.html` depuis le site publié, pas comme fichier local `file://`. La page du corpus charge `data/soninke-samples.jsonl` via HTTP(S).
- **Données locales** : les annotations du prototype sont stockées dans le navigateur et ne sont pas synchronisées entre appareils.

## Limites fonctionnelles

La publication ne rend pas la synthèse vocale opérationnelle. Aucun moteur TTS soninké n’est validé dans le projet ; les fonctions présentes servent à tester des audios existants et à collecter des validations humaines.
