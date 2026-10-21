# Fiche de validation linguistique — lot prioritaire Soninké

Cette fiche facilite la validation par le référent linguistique des 50 lemmes candidats du premier lot. Elle reprend les 71 segments de la source afin de ne perdre aucun sens, variante, exemple ou indication de provenance.

## Fichier à remplir

`fiche-validation-referent-soninke.csv`

## Colonnes à compléter

- `validation_referent` : inscrire `CONFIRMÉ`, `À CORRIGER`, `À REJETER` ou `À DISCUTER`.
- `lemme_corrige` : renseigner la graphie validée si elle diffère de la graphie proposée.
- `traduction_fr_confirmee` : donner une traduction française validée. Pour plusieurs sens, les distinguer clairement.
- `sens_variantes_exemples_a_conserver` : noter les sens, variantes, exemples et formes sous-jacentes à préserver.
- `commentaires_referent` : ajouter les explications utiles, les incertitudes ou le contexte dialectal.
- `validateur` et `date_validation` : indiquer qui a validé et quand.

## Règles importantes

1. **Ne pas importer automatiquement** une entrée simplement parce qu'elle apparaît dans cette fiche.
2. Un même lemme ne doit apparaître qu'une seule fois dans le lexique principal. Les différents sens et exemples doivent être conservés sous cette entrée, pas dupliqués en plusieurs lemmes.
3. Garder les variantes explicitement identifiées par la source; ne pas fusionner deux formes différentes sans validation linguistique.
4. Si la graphie ou le sens est incertain, choisir `À DISCUTER` plutôt que deviner.
5. Les 71 lignes représentent des segments/occurrences de la source pour 50 lemmes candidats distincts; elles ne signifient pas qu'il faut créer 71 entrées.
6. La glose automatique peut être tronquée ou imparfaite. Toujours consulter `texte_source_complet` et conserver la provenance.
7. Les champs de validation sont laissés vides intentionnellement : aucune nouvelle entrée n'est marquée comme validée par anticipation.

## Branche et destination

Dépôt : `aydiarra-star/xamxam-xara`  
Branche : `data/lexique-soninke-fr-v1`  
Fiche CSV : `reports/fiche-validation-referent-soninke.csv`
