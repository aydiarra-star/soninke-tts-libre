# Fiches de cibles des renvois — rapprochement avec la revue source

Date : 2026-10-21  
Branche : `data/lexique-soninke-fr-v1`

## Livrables
Trois tableaux CSV détaillent les cibles de renvoi et, lorsque la cible correspond exactement à un lemme de la revue source, reprennent la glose, la variante, le texte source, le statut et la décision provisoire de la fiche candidate.

- [Partie 1 — fiches de cibles](fiches-cibles-renvois-soninke-partie-1-2026-10-21.csv)
- [Partie 2 — fiches de cibles](fiches-cibles-renvois-soninke-partie-2-2026-10-21.csv)
- [Partie 3 — fiches de cibles](fiches-cibles-renvois-soninke-partie-3-2026-10-21.csv)

## Résultats
- 236 segments de renvoi source ont été comparés.
- Le tableau détaillé contient 195 lignes de travail.
- 167 lignes associent un composant cible à une fiche de la revue source par correspondance exacte du lemme.
- 28 lignes correspondent à des composants pour lesquels aucun candidat exact n'a été retrouvé dans la revue disponible.

Ces nombres décrivent des lignes de travail, et non des lemmes uniques ou des décisions linguistiques définitives. Certains renvois comportent plusieurs composants, et les répétitions de la source peuvent subsister.

## Correction de qualité
Lors d'une vérification ultérieure, j'ai repéré que le libellé de statut généré dans certaines lignes pouvait laisser entendre qu'une cible était déjà validée. Les trois CSV ont été corrigés : les correspondances exactes avec la revue portent maintenant le libellé **« CIBLE EXACTE DANS REVUE SOURCE — NON VALIDÉE »**. Cette mention décrit uniquement la correspondance textuelle; elle ne change pas le statut d'origine de la fiche candidate et ne constitue pas une validation linguistique.

## Comment utiliser les fiches
1. Vérifier le texte complet du renvoi et celui de la fiche candidate.
2. Comparer la glose et les exemples, pas seulement l'orthographe.
3. Préserver les chiffres finaux, les variantes et les marqueurs morphologiques.
4. Ne pas importer une cible sur la seule base d'une correspondance de chaîne.
5. Soumettre les cas ambigus à la validation linguistique.

## État de la base
La base de production n'a pas été modifiée et reste à 305 entrées. Les statuts d'origine du fichier de revue source sont conservés.
