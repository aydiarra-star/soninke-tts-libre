# Plan de constitution des dictionnaires multilingues

## Objectif

Créer un lexique pédagogique utile, consultable hors ligne après chargement, qui relie le soninké, le wolof, le français et l’anglais. Le modèle doit permettre d’ajouter le pulaar, le bambara, le sérère et d’autres langues sans changer le format principal.

## État réel au 19 octobre 2026

- **Soninké** : le dépôt contient 577 entrées du lexique du projet et un manifeste de 576 WAV disponibles. L’entrée `snk-00308` reste sans WAV. La validation linguistique attestée par le référent du projet est conservée séparément de la disponibilité technique du fichier.
- **Wolof** : un instantané automatisé de 750 fiches de sens français–wolof est importé depuis 26 pages alphabétiques de Jàngileen, avec URL source par fiche. L’extraction a identifié 709 têtes d’entrée françaises, dont 707 avec au moins une traduction exploitable et 2 sans traduction exploitable. Le site affiche 911 mots wolof ; ce chiffre n’est pas directement comparable aux têtes d’entrée françaises ou aux fiches de sens. La couverture doit être réconciliée avec le modèle du dictionnaire avant de déclarer l’import complet.
- **Français et anglais** : ils servent de langues-pivots dans le modèle. Les définitions, formes grammaticales, exemples et audio seront renseignés depuis des sources ouvertes ou rédigés comme contenu original puis revus.
- **Parcours** : une première structure A0–A2 est disponible dans `data/learning-curriculum.json`. La page propose des raccourcis par catégorie ; elle ne prétend pas encore fournir toutes les leçons.

## Sources et décisions de licence

| Source | Usage retenu | Condition |
| --- | --- | --- |
| [snk_engine](https://github.com/oscarmedra/snk_engine) | Données et règles soninké, avec révision épinglée | Conserver l’attribution CC BY 4.0 et les notes sur les variantes |
| [Asawan](https://www.asawan.org/fr/lexique_soninke) | Référence lexicale et lien utilisateur | Pas d’import massif tant que la licence de la base lexicale n’est pas confirmée |
| [Jàngileen](https://jangileen.kalam-alami.net/special/apropos) | Dictionnaire wolof-français | La page légale indique que les données du dictionnaire peuvent être redistribuées et modifiées ; conserver source et date d’extraction |
| [Baatukaay](https://github.com/alphajoop/baatukaay) | Référence complémentaire | La licence MIT du dépôt ne suffit pas à prouver automatiquement les droits de toutes les données lexicales |
| [Kaikki/Wiktionary Wolof](https://kaikki.org/frwiktionary/Wolof/index.html) | Source structurée de mots, sens et catégories | Respecter l’attribution et la licence applicable aux données Wiktionary |
| [Wiktionary anglais](https://en.wiktionary.org/) et [Wiktionary français](https://fr.wiktionary.org/) | Définitions, formes et catégories en complément | Attribution et partage à l’identique quand la licence l’exige |

Le dictionnaire Jàngileen affichait 911 mots wolof au moment de la recherche. L’importateur récupère 750 fiches de sens à partir des 26 pages alphabétiques et conserve l’URL de chaque fiche. Le rapport distingue 709 têtes d’entrée françaises, 707 avec traduction exploitable et 2 sans traduction. Les exemples sont conservés dans leur forme brute lorsqu’on ne peut pas attribuer leur langue avec certitude, car les libellés d’exemples ne sont pas cohérents sur toutes les entrées.

## Champs obligatoires par entrée

- identifiant stable et langue du mot principal ;
- mot, sens/définition, catégorie grammaticale et variantes orthographiques documentées ;
- traductions indépendantes dans les autres langues, laissées vides si non établies ;
- exemple de phrase et traduction de l’exemple, uniquement si la source les fournit ou si un rédacteur les a créés ;
- audio URL, source du fichier, licence et statut de validation de la prononciation ;
- source et attribution pour chaque traduction, avec date d’import ;
- statuts séparés : fiche, traduction, prononciation, audio technique ;
- note dialectale ou régionale si elle est documentée.

## Pipeline d’import recommandé

1. Récupérer uniquement une source dont les droits de réutilisation sont documentés.
2. Sauvegarder la version/source d’origine, la date d’extraction et l’attribution.
3. Normaliser les champs sans effacer les graphies ni les variantes.
4. Dédupliquer avec un identifiant de source, sans fusionner automatiquement deux sens différents.
5. Vérifier les traductions par paires (wolof-français, soninké-français, anglais-français) et ne pas générer automatiquement les traductions manquantes.
6. Garder les entrées en brouillon tant que le statut de révision n’est pas explicite.
7. Générer un rapport de couverture par langue, catégorie grammaticale, exemples et audio.
8. Exécuter les validations statiques, puis vérifier manuellement l’affichage et l’audio sur iPhone et ordinateur.

## Fonctionnalités pédagogiques à construire à partir des données

- recherche dans toutes les langues et dans les définitions ;
- cartes de vocabulaire et révision espacée ;
- quiz de reconnaissance, traduction et écoute, uniquement quand la réponse est sourcée ;
- exemples en contexte, grammaire progressive et variantes ;
- audio natif communautaire, transcription et lecture répétée ;
- progression locale et export, sans compte obligatoire au départ ;
- contributions communautaires avec source, consentement audio et revue avant publication.

## Limites à ne pas masquer

Une page de dictionnaire externe n’est pas un corpus audio. Une voix de synthèse du navigateur n’est pas un enregistrement natif. Une traduction d’une seule source n’est pas automatiquement validée par la communauté. L’application doit afficher ces différences au lieu de promettre une couverture ou une qualité inexistante.


## Corpus de phrases soninké intégré
106 phrases et paragraphes soninké–français ont été importés depuis cinq fichiers `corpus/valide/` du dépôt `snk_engine`, à une révision épinglée, sous CC BY 4.0 avec attribution. L’application conserve la graphie d’origine, la source et le niveau. La mention « validé dans la source » ne signifie pas que ce dépôt a revérifié indépendamment chaque phrase. Les phrases n’ont pas d’audio natif associé dans ce lot ; l’application ne prétend pas en disposer.


## Références soninké supplémentaires examinées
- **Ousmane Moussa Diagana, *Dictionnaire soninké-français (Mauritanie)*, Karthala, 2011** : référence publiée signalée avec plus de 5 800 entrées. À utiliser pour l’étude et la comparaison linguistique ; aucune copie massive sans autorisation.
- **Ch. Monteil / V. Monteil, *Vocabulaire soninké I–II* (1966)** : référence historique annoncée à plus de 7 000 mots, principalement du soninké occidental avec une transcription historique. Ne pas fusionner directement avec les graphies actuelles ; vérifier les droits et documenter les variantes.
- **ASJP Soninke wordlists** : listes comparatives sous CC BY 4.0 ; candidate pour une annexe comparative, pas pour remplacer le lexique principal.
- **Mayoiga/Soninke-dataset (Hugging Face)** : environ 1 310 lignes soninké–français provenant notamment de textes Calaméo, mais la licence du dataset et les droits sur les textes sous-jacents n’étaient pas clairement indiqués dans la fiche examinée. Aucune importation avant clarification.

Ces ressources sont enregistrées dans `data/language-sources.json`. La présence d’un lien ou d’un nombre d’entrées dans le catalogue ne signifie pas que les données ont été intégrées ni que leur licence autorise la copie.


## Ressource anglais–français en examen
[Panlexia](https://github.com/barumau/panlexia) relie des mots à des concepts communs et propose des listes anglais/français. Le dépôt indique CC BY 4.0 pour son contenu, mais réutilise aussi Concepticon (CC BY 4.0), NorthEuraLex (CC BY-SA 4.0), WOLD (CC BY 3.0 Allemagne) et d’autres sources. Il ne faut donc pas importer ses fichiers eng/fra comme si chaque ligne avait une licence uniforme : la provenance et les droits de chaque source amont doivent être conservés. Pour l’instant, Panlexia reste une référence de recherche, pas une importation dans le lexique utilisateur.


## Rapport de couverture de l’import wolof
L’importateur conserve maintenant le nombre de têtes d’entrée source, celles qui ont au moins une traduction exploitable, et une liste sourcée des têtes d’entrée sans traduction exploitable. Le contrôle CI exige que ces compteurs concordent avant de considérer l’instantané comme importé. Cette liste permet de compléter la couverture sans inventer les traductions absentes.


### Instantané Jàngileen actuellement versionné
L’instantané versionné contient 750 fiches de sens sourcées, regroupées autour de 709 têtes d’entrée françaises : 707 têtes ont au moins une traduction wolof exploitable et 2 sont explicitement listées sans traduction exploitable. Ces chiffres décrivent l’extraction, pas la totalité du dictionnaire. Le compteur public de 911 mots wolof est une mesure distincte et n’est pas présenté comme équivalent au nombre de têtes françaises ni au nombre de fiches de sens.
