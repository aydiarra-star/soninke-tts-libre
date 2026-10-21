# Triage détaillé des renvois du dictionnaire soninké

Date : 2026-10-21  
Branche : `data/lexique-soninke-fr-v1`

## Objet
Préparer la revue humaine des renvois extraits du dictionnaire source, sans modifier la base lexicale. Les tests d'égalité sont conservateurs : NFC, espaces normalisés, minuscules, et **conservation des chiffres finaux**. Les composants séparés par des virgules sont examinés individuellement; les marqueurs commençant par un tiret sont conservés comme composants morphologiques.

## Résultats du triage automatique
- Segments de renvoi examinés : 236
- Tous les composants trouvés exactement dans la base : 42
- Cibles composées avec marqueur morphologique : 82
- Cibles à plusieurs composants sans marqueur morphologique : 36
- Cibles numérotées non trouvées exactement : 24
- Cibles simples non trouvées exactement, à examiner comme variantes/graphies possibles : 41
- Cibles non extraites automatiquement : 11

Ces catégories sont une aide au triage et ne sont pas toutes mutuellement exclusives sur le plan linguistique; la catégorie affectée est une priorité de traitement. Une cible absente par comparaison exacte n'est pas nécessairement absente du dictionnaire : elle peut utiliser une variante graphique, un suffixe, une numérotation ou une notation grammaticale.

## Règles de prudence
1. Ne pas supprimer automatiquement les chiffres finaux : `baabo1` et `baabo2` peuvent être des entrées distinctes.
2. Ne pas traiter `-ndi3`, `-lenme`, `-o4` ou `-aaxu` comme des lemmes autonomes sans interprétation grammaticale.
3. Conserver toutes les parties d'une cible multiple, leur ordre, la glose et le paragraphe source.
4. Aucun renvoi n'est rattaché automatiquement et aucune entrée n'est importée par ce rapport.
5. Toute décision finale de rattachement doit être vérifiée linguistiquement.

## Sources
- [Tableau détaillé des renvois](controle-renvois-dictionnaire-soninke-2026-10-21.csv)
- [Rapprochement initial avec la base](rapprochement-renvois-base-soninke-2026-10-21.csv)
- [Base lexicale Soninké–français](../data/lexique-soninke-fr-base.csv)

La base de production demeure inchangée à 305 entrées.
