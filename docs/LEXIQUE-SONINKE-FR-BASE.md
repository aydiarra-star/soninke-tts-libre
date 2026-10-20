# Base lexicale Soninké–français

## Fichier

`data/lexique-soninke-fr-base.csv`

- Format : CSV UTF-8 avec séparateur point-virgule.
- Colonnes : `id`, `soninke`, `francais`, `categorie`, `source`, `statut`.
- Provenance : liste fournie par le référent linguistique du projet.
- Les graphies et traductions sont conservées telles que fournies dans cette première extraction.
- Le statut `fourni_par_referent` signifie « fourni par le référent », et non une vérification indépendante ou une validation phonétique de chaque entrée.

## Périmètre de cette première livraison

Cette première livraison structure les verbes de base et les éléments grammaticaux suivants :
- pronoms personnels des séries longue et diminutive ;
- marqueurs temporels et aspectuels ;
- négation, particules et expression impérative.

Elle ne contient pas encore toutes les formes dérivées fournies dans la liste source (noms d'action, gérondifs et variantes). Elles devront être ajoutées dans un fichier ou une extension distincte, sans écraser les formes de base.

## Règles de traitement

1. Ne pas remplacer automatiquement les caractères `ŋ`, apostrophes, traits d'union, espaces ou graphies originales.
2. Ne pas déduire une prononciation à partir de la traduction française.
3. Ne pas associer d'audio sur la seule base d'une ressemblance de nom de fichier.
4. Conserver les variantes comme entrées distinctes lorsqu'elles sont fournies comme variantes.
5. Séparer les statuts de provenance lexicale, de validation linguistique et de validation audio.
6. Ne pas utiliser ces mots isolés comme s'ils constituaient à eux seuls un corpus de phrases suffisant pour entraîner une synthèse vocale.

## Étape suivante

Ajouter les noms d'action et gérondifs en conservant les liens avec leur forme de base, puis rapprocher les entrées des manifestes audio existants. Les fichiers WAV et leurs validations ne doivent pas être modifiés par cette étape lexicale.
