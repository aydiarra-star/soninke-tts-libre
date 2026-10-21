# Fiche de validation linguistique — lot 2 Soninké

La fiche reprend les 120 segments source couvrant 50 lemmes candidats distincts. Elle est destinée au référent linguistique. Aucun de ces nouveaux candidats n'est importé dans la base avant validation.

## Colonnes à compléter
- `validation_referent` : `CONFIRMÉ`, `À CORRIGER`, `À REJETER` ou `À DISCUTER`.
- `lemme_corrige` : graphie validée si elle diffère de la proposition.
- `traduction_fr_confirmee` : traduction française validée, en distinguant les sens multiples.
- `sens_variantes_exemples_a_conserver` : variantes, exemples, sens, formes sous-jacentes.
- `commentaires_referent`, `validateur`, `date_validation` : notes et provenance de la validation.

## Règles
1. Ne pas importer une entrée avant validation.
2. Un seul enregistrement par lemme canonique dans la base; conserver les sens multiples sous cet enregistrement.
3. Les variantes et les textes sources complets sont conservés.
4. Si deux homonymes doivent être distingués malgré une graphie identique, préciser ce choix dans les commentaires avant l'import.
5. Les renvois explicites vers une entrée principale ont été exclus de ce lot.

Dépôt : `aydiarra-star/xamxam-xara`  
Branche : `data/lexique-soninke-fr-v1`
