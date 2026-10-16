# Publication du prototype sur GitHub Pages

## État actuel vérifié

Le dépôt contient un site HTML/CSS/JavaScript statique. Le workflow GitHub Actions **pages build and deployment** a terminé avec succès sur le commit `21ae5642e3e1b98b1e5ce26d65716608fae2c426` :

- Exécution : https://github.com/aydiarra-star/soninke-tts-libre/actions/runs/38982991503
- Accueil : https://aydiarra-star.github.io/soninke-tts-libre/
- Corpus : https://aydiarra-star.github.io/soninke-tts-libre/corpus.html

La réussite du workflow confirme la construction et le déploiement par GitHub Actions, mais ne prouve pas à elle seule que les pages s'affichent correctement dans Safari sur téléphone. Le test visuel et fonctionnel sur appareil reste à effectuer.

## Configuration initiale (si le site est inaccessible)

1. Ouvrir https://github.com/aydiarra-star/soninke-tts-libre/settings/pages en étant connecté au compte propriétaire.
2. Dans **Build and deployment**, choisir **Source: GitHub Actions**.
3. Enregistrer si GitHub présente un bouton de confirmation.
4. Ouvrir l'onglet **Actions** et vérifier l'exécution la plus récente de **pages build and deployment**.
5. Attendre la fin des tâches **build** et **deploy**. Le lien public est également indiqué dans l'environnement **github-pages** d'une exécution réussie.

## Déploiements suivants

Le workflow `.github/workflows/pages.yml` est configuré pour les pushes vers `main` et peut être lancé manuellement avec `workflow_dispatch`. La branche prototype n'est pas automatiquement déployée à chaque push ; ne pas supposer qu'un nouveau commit est en ligne sans vérifier l'exécution de déploiement correspondante.

## Dépannage

- **404 / page inaccessible** : vérifier que GitHub Pages est configuré sur **GitHub Actions**, que le workflow s'est terminé avec succès et que l'URL correspond exactement au nom du dépôt.
- **Workflow absent** : GitHub Actions n'affiche généralement que les workflows présents sur la branche sélectionnée. Vérifier la branche qui contient `.github/workflows/pages.yml`.
- **Page d'accueil visible mais corpus en erreur** : ouvrir `/soninke-tts-libre/corpus.html` depuis le site publié, pas comme fichier local `file://`. La page du corpus charge `data/soninke-samples.jsonl` via HTTP(S).
- **Données locales** : les annotations du prototype sont stockées dans le navigateur et ne sont pas synchronisées entre appareils.
- **Page blanche ou chargement infini** : noter l'URL exacte et le navigateur, puis vérifier la console réseau/JavaScript si possible. Ne pas déclarer le test réussi sans avoir essayé les interactions.

## Limites fonctionnelles

La publication ne rend pas la synthèse vocale opérationnelle. Aucun moteur TTS soninké n'est validé dans le projet ; les fonctions présentes servent à tester des audios existants et à collecter des validations humaines.
