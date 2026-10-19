# Langues en partage — évolution de Soninké TTS Libre

## Vision
Faire de Soninké TTS Libre une application ouverte, simple d’accès et incontournable pour les amoureux des langues et l’apprentissage au Sénégal et en Afrique.

## Langues au lancement
Soninké, wolof, français et anglais. Le format est extensible pour le pulaar, le bambara, le sérère et d’autres langues.

## Principes
- Préserver le lexique soninké et les WAV existants.
- Distinguer disponibilité technique, validation de prononciation, validation de traduction et provenance.
- Ne pas inventer de traduction ni d’audio natif. La synthèse vocale du navigateur est indiquée comme telle.
- Garder une première version légère : HTML/CSS/JavaScript, pas de compte obligatoire ni de service payant nécessaire pour explorer.
- Autoriser ajout local et export JSON/CSV. Les contributions du prototype ne sont pas publiées automatiquement.

## Fichiers
- `apprendre.html` : interface d’apprentissage adaptée au mobile.
- `apprendre.css` : styles responsives.
- `apprendre.js` : recherche, filtres, lecture audio, synthèse vocale navigateur pour français/anglais, ajout local et exports.
- `data/trilingual-lexicon.json` : registre des langues et schéma extensible.

## Suite
1. Vérifier les contrôles CI et le chargement des ressources.
2. Tester la lecture réelle sur Safari iPhone et navigateur de bureau.
3. Ajouter un premier lexique wolof documenté avec sources fiables.
4. Préparer un flux de contribution simple pour les audios et corrections communautaires.
5. Intégrer via PR sans réinitialiser ni écraser le travail existant.

## Ressources linguistiques repérées
- Asawan, lexique Soninké-Français-Anglais : https://www.asawan.org/fr/lexique_soninke
- Asawan, guides de lecture/écriture : https://www.asawan.org/fr/apprendre-sonink%C3%A9-ajami
- Soninké structuré et corpus : https://oscarmedra.github.io/snk_engine/ (données annoncées CC BY 4.0 ; conserver l’attribution fournie par la source)
- Jàngileen : https://jangileen.kalam-alami.net/special/apropos (le site indique que les données du dictionnaire peuvent être réutilisées et redistribuées ; vérifier les mentions propres à chaque ressource)
- Baatukaay : https://github.com/alphajoop/baatukaay (dépôt annoncé sous licence MIT ; vérifier séparément la licence des données lexicales avant extraction)
- Kaikki / Wiktionary Wolof : https://kaikki.org/frwiktionary/Wolof/index.html (données extraites de Wiktionary ; conserver l’attribution et la licence applicable)

Ces liens sont ajoutés à l’interface comme références externes. Aucun dictionnaire propriétaire ou corpus tiers n’est copié dans le dépôt sans vérification de licence. La prochaine étape de recherche est d’établir une fiche de provenance par source, de confirmer les droits des données lexicales, puis d’importer seulement les corpus autorisés avec leurs champs de citation.


## Parcours d’apprentissage
La page propose maintenant des entrées guidées par niveau : salutations, vie quotidienne, famille, déplacement, grammaire, puis écoute et révision. Les boutons appliquent les filtres correspondants au lexique ; ils ne prétendent pas encore représenter un cours complet. Le programme pédagogique est décrit dans `data/learning-curriculum.json` afin de construire les leçons à partir d’entrées documentées et de contenus validés.

## Vérification automatique
Le workflow de validation contrôle désormais la syntaxe de `apprendre.js`, la structure des JSON, les quatre langues de lancement, les futures langues, les 577 entrées et la présence des 576 fichiers WAV déclarés disponibles. Ces tests statiques ne remplacent pas une vérification manuelle sur iPhone ni une écoute de tous les fichiers.


## Ajouter une langue sans refaire l’interface
Ajouter la langue à `languages` dans `data/trilingual-lexicon.json` avec un code stable, un nom et éventuellement `speechLocale`; déplacer son code depuis `futureLanguages` vers `languages`. Les sélecteurs de langue, les champs de contribution et les colonnes d’export sont construits à partir de cette liste. Pour chaque nouvelle entrée, ajouter les champs de cette langue et conserver les sources/statuts. Une locale de synthèse n’active un bouton que si une voix correspondante est réellement installée dans le navigateur.


## Exercices
La page propose deux modes de quiz : vocabulaire dans les langues choisies, quand les deux formes existent, et phrases soninké–français tirées du corpus sourcé. Le score est limité à la session courante ; aucun progrès durable ni synchronisation entre appareils n’est revendiqué à ce stade. Les réponses sont comparées après normalisation Unicode et casse, sans supprimer les diacritiques linguistiquement importants.


## Contributions communautaires
L’ajout local dans la page ne publie rien sur le dépôt. Pour proposer une entrée au lexique commun, le formulaire GitHub `.github/ISSUE_TEMPLATE/language_contribution.yml` collecte la langue, le mot, les traductions, la source, le contexte et les autorisations de partage. Les audios peuvent être joints à l’issue après sa création. Les propositions restent à examiner avant toute intégration ; le consentement du locuteur et la licence du fichier audio doivent être explicites.


## Révisions locales
Chaque fiche peut être ajoutée à une liste « Mes révisions », conservée dans le navigateur avec `localStorage`. Le filtre permet de retrouver les mots choisis à la prochaine visite sur le même navigateur. Cette liste n’est ni synchronisée entre appareils ni envoyée au serveur.
