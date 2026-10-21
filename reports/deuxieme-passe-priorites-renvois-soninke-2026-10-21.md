# Deuxième passe de contrôle des renvois soninké — priorités de vérification

Date : 2026-10-21  
Branche : `data/lexique-soninke-fr-v1`

## But

Cette note transforme l'audit des 28 lignes sans correspondance exacte en file de travail ordonnée. Elle s'appuie sur les champs `texte_complet_renvoi` des trois CSV de fiches-cibles. Les cibles citées ci-dessous sont celles que le texte source imprime après « See main entry: ». Ce constat textuel ne valide ni l'analyse morphologique ni la relation sémantique.

## Priorité 1 — Renvois directs à traiter comme variantes candidates

Ces entrées indiquent explicitement une autre forme comme entrée principale. Il faut d'abord vérifier la forme cible dans le dictionnaire source et conserver la forme de départ comme renvoi/provenance si le rattachement est confirmé.

| Forme source | Cible indiquée | Paragraphe source | Vérification |
|---|---|---:|---|
| `baramaneene` | `faramaneene` | 237 | Vérifier initiale b/f et prononciation; ne pas normaliser automatiquement. |
| `ciga` | `tiga` | 811 | Confirmer la relation c/t. |
| `cigakorome` | `tigakorome` | 812 | Vérifier séparément la forme composée. |
| `cigamaxafo` | `tigamaxafo` | 813 | Vérifier séparément la forme composée. |
| `cigate` | `tigate` | 814 | Confirmer la relation c/t. |
| `ciye` | `tiye` | 823 | Confirmer la variante et la catégorie grammaticale. |
| `consolinde` | `sonsolondi` | 826 | Écart orthographique plus large : contrôler la source, ne pas déduire une équivalence. |
| `consolindi` | `sonsolondi` | 827 | Garder cette forme distincte de `consolinde` jusqu'à vérification. |
| `cuballe` | `suballe` | 832 | Confirmer la relation c/s. |
| `cunsu` | `sunsu` | 835 | Confirmer la relation c/s. |
| `cuuba` | `juuba` | 838 | Confirmer la relation c/j et la prononciation. |

## Priorité 2 — Renvois composés ou morphologiques

Ne pas réduire ces cibles à un seul composant. Les marqueurs comme `n4`, `-ndi1`, `-bali` et `-aaxu` doivent être interprétés dans leur système de notation d'origine.

| Forme source | Cible textuelle complète | Glose du renvoi | Paragraphe(s) |
|---|---|---|---|
| `faabanbaanaaxu` | `-aaxu, baane, baane, faaba2` | rivalité, opposition | 45 |
| `faqilanbali` | `-bali, haqile, n4` | impatient | 135 |
| `ɲamanbali` | `-bali, n4, n4, ɲama1` | éternel, inépuisable | 136 |
| `batikanxoore` | `bati, kaa, n4, xoore` | temple à Jérusalem | 264 |
| `battaranlenme` | `battara, n4, renme` | vaurien | 273, 275 |
| `battaransere` | `battara, n4, sere1` | vaurien | 274 |
| `allanbatte1` | `Alla, batu2` | adoration de Dieu | 284 |
| `baxandoroke` | `baxa1, doroke, n4` | robe indigo | 298 |
| `fatanbinne` | `binne, fate1, n4` | africain, peau noire | 442 |
| `boroxonjilinka` | `boroxonjile, kaa, n4` | fourmilière | 616, 617 |
| `nuxudunbure` | `bure, -dun, -dun, nuxu` | désagréable, hypocrite, mauvais | 709 |
| `buudinlenme` | `buudi, n4, renme, n4` | pièce d'argent | 767, 768 |
| `consonlindaana` | `-aana, -ndi1, sonsolo` | sondeur, espion | 829 |

## Contrôle des répétitions

Les 28 lignes de travail se répartissent en 24 formes sources distinctes. Les répétitions sont conservées car elles renvoient à des paragraphes/occurrences différents, notamment :

- `batikanxoore` : paragraphe 264 répété dans les fiches de travail;
- `battaranlenme` : paragraphes 273 et 275;
- `boroxonjilinka` : paragraphes 616 et 617;
- `buudinlenme` : paragraphes 767 et 768.

Avant toute modification future, vérifier si une répétition vient du document source ou du découpage de la fiche. Ne pas dédupliquer les occurrences sans conserver leur provenance.

## Ordre de travail recommandé

1. Vérifier les 11 renvois directs de la priorité 1 dans le document source, puis consigner « confirmé », « variante probable » ou « incertain » avec preuve.
2. Examiner ensuite les 13 formes composées/morphologiques, en consultant les entrées de chaque composant et leur glose complète.
3. Garder séparés les homographes numérotés et les formes proches tant que le sens n'est pas comparé.
4. Pour chaque décision, enregistrer le texte justificatif et l'identité de la personne qui valide.
5. N'importer aucune correction dans `data/lexique-soninke-fr-base.csv` avant validation linguistique explicite.

## État de production

La base de production reste hors périmètre de cette note : aucune entrée n'a été ajoutée, supprimée, fusionnée ou normalisée. Les cibles restent des propositions issues du texte source, pas des validations linguistiques.
