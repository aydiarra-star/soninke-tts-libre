# Pistes de rapprochement des renvois — revue humaine

Date : 2026-10-21  
Branche : `data/lexique-soninke-fr-v1`

## Méthode
J'ai comparé les composants extraits des cibles de renvoi aux 305 lemmes de la base, en conservant les chiffres finaux. Pour les composants absents par correspondance exacte, j'ai généré deux types de pistes non conclusives : (1) retirer les chiffres finaux uniquement pour voir si une forme de base apparaît; (2) relever quelques formes de base à distance orthographique de 1 caractère. Ces pistes ne sont **pas** des équivalences linguistiques et ne doivent jamais entraîner un rattachement automatique.

## Exemples à contrôler

| Lemme source | Cible originale | Piste automatique | Contrôle requis |
|---|---|---|---|
| baabondi | baabo1, -ndi3 | baabo si l'indice numérique est une homonymie éditoriale | Vérifier dans la source si baabo1 est distinct de baabo |
| baanaaxu | baana2, baana2 | baana si l'indice numérique n'est pas distinctif | Vérifier l'entrée numérotée et conserver le double renvoi original |
| baawo2 | baabo2 | baabo si l'indice numérique n'est pas distinctif | Comparer la source, la note et le ton; ne pas remplacer baabo2 par baabo sans validation |
| baawo3 | baabo3 | baabo si l'indice numérique n'est pas distinctif | Garder distinct le sens « première pluie de l'année » tant que la référence n'est pas confirmée |
| bafi | boyi1 | boyi si l'indice numérique n'est pas distinctif | Contrôler l'entrée numérotée et le sens verbal |
| bafaade | boyaade | biyaade (forme proche, distance 1) | Simple piste orthographique; confirmer dans le dictionnaire |
| balandi | bala, -ndi3 | bara (forme proche, distance 1) | Similarité de chaîne insuffisante pour un rattachement |
| baabe | baananbe | aucune piste de distance 1 retenue | Recherche linguistique manuelle requise |

## Résultat et limites
- La comparaison exacte initiale a recensé 236 segments de renvoi.
- 185 segments comportent au moins un composant de cible non trouvé exactement ou une cible non extraite.
- Les suggestions de chaîne ne permettent pas de déterminer si deux formes sont des variantes, des homonymes ou des formes morphologiquement liées.
- Les marqueurs tels que `-ndi3`, `-lenme`, `-aaxu`, ainsi que les notations comme `n4`, doivent être interprétés comme notation lexicographique et non comme mots autonomes.
- Les répétitions de la source sont conservées; elles peuvent correspondre à des paragraphes dupliqués ou à des entrées distinctes.

## Décision de production
Aucune des pistes ci-dessus n'est validée automatiquement. La base `data/lexique-soninke-fr-base.csv` reste inchangée à 305 entrées. Le prochain contrôle devra vérifier chaque proposition dans la source complète, puis faire confirmer les rattachements linguistiques avant import.
