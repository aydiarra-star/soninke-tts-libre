# Fiche de validation linguistique — lot prioritaire Soninké

La fiche conserve les 71 segments de la source correspondant aux 50 étiquettes de lemmes candidates. Le référent linguistique a confirmé les traductions, définitions et informations du lot le 21 octobre 2026, puis 42 lemmes canoniques ont été intégrés à la base.

## Fichiers

- Fiche complétée : `reports/fiche-validation-referent-soninke.csv`
- Lot prioritaire : `reports/lot-validation-prioritaire-soninke.csv`
- Base : `data/lexique-soninke-fr-base.csv`

## Règles appliquées

1. Les 50 étiquettes de la source sont regroupées en 42 lemmes canoniques dans la base, en retirant les suffixes numériques servant à indexer des homonymes.
2. Chaque lemme canonique n'apparaît qu'une fois dans la base principale.
3. Les sens multiples sont regroupés dans le champ français, les variantes sont signalées dans le champ source et les 71 textes complets restent dans la fiche.
4. Les champs de validation sont renseignés avec le statut confirmé et la date de validation communiquée.
5. Les exemples et la provenance de la source restent disponibles dans `texte_source_complet`; ils ne sont pas remplacés par les gloses automatiques.

## Dépôt

Dépôt : `aydiarra-star/xamxam-xara`  
Branche : `data/lexique-soninke-fr-v1`
