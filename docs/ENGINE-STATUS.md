# État des moteurs de synthèse vocale

Dernière vérification du projet : 2026-10-16.

## Résultat confirmé

- Le démonstrateur OmniVoice a été ouvert et réglé sur la langue Soninke (`snk`).
- La génération a échoué avant de produire un audio, avec une erreur de quota ZeroGPU (« 0s left »).
- **Aucun échantillon Soninké issu d’OmniVoice n’a donc été obtenu ou écouté.** La qualité de prononciation reste inconnue.
- OmniVoice est une piste expérimentale, pas un moteur intégré ou validé pour ce projet.

Liens à examiner :
- Dépôt : https://github.com/k2-fsa/OmniVoice
- Modèle : https://huggingface.co/k2-fsa/OmniVoice
- Démonstrateur : https://huggingface.co/spaces/k2-fsa/OmniVoice

## Licence : point de vigilance

Le code du projet OmniVoice est annoncé sous Apache-2.0, tandis que les poids préentraînés sont indiqués sous une licence non commerciale liée aux données d’entraînement. Vérifier les fichiers de licence et la fiche du modèle au moment de toute intégration. Ne pas redistribuer ces poids ni bâtir une offre commerciale sur eux sans autorisation/licence compatible.

## Décision actuelle

1. Ne pas afficher de bouton « Générer l’audio » qui simulerait une génération.
2. Utiliser ce laboratoire pour écouter des audios réellement disponibles et consigner les validations humaines.
3. Rechercher un moteur, des données et des dépendances dont les licences permettent explicitement l’usage et la redistribution visés.
4. Avant d’entraîner un modèle, auditer chaque corpus, les droits des enregistrements, le consentement des locuteurs et la qualité des transcriptions.

## Pistes à auditer, sans les considérer comme validées

- https://github.com/oscarmedra/snk_engine — examiner code, données, qualité et licences.
- https://www.asawan.org/fr/lexique_soninke — ressource lexicale, pas un moteur TTS.
- https://lgidf.cnrs.fr/soninke — ressource linguistique, pas une preuve de modèle TTS disponible.
- [SIL AI — wav2vec2-bloom-speech-snk](https://huggingface.co/sil-ai/wav2vec2-bloom-speech-snk) — candidat prioritaire pour un premier essai STT, pas un moteur TTS. La fiche annonce un WER de 28,88 % et un CER de 5,76 % sur son évaluation Bloom Speech Soninke ; ce sont des résultats déclarés par le modèle sur son propre jeu d'évaluation, pas une garantie sur nos enregistrements. Le dépôt est soumis à une licence SIL International AI & NLP RAIL-M non commerciale et exige l'acceptation de conditions qui partagent le nom d'utilisateur et l'adresse e-mail avec les auteurs. Aucun fournisseur d'inférence n'est actuellement indiqué comme disponible sur sa fiche. Il faut donc vérifier l'accès, la licence et le coût de calcul avant l'essai ; ne pas l'intégrer automatiquement dans une offre commerciale.

## Critères avant intégration

- Génération d’un vrai fichier audio reproductible.
- Écoute et validation par un locuteur compétent en soninké.
- Licence compatible documentée pour le code, les poids, les données et chaque dépendance.
- Pas de traduction ou de sens attribué aux phrases de test sans validation.


## Journal d’évaluation audio — 2026-10-17

Ce journal distingue la qualité sonore perçue de l’exactitude linguistique. Un échantillon ne valide pas à lui seul le moteur qui l’a produit.

| Référence | Phrase test | Clarté sonore | Prononciation soninké | Naturel de la voix | Source/moteur |
|---|---|---|---|---|---|
| 001 | `Daga yigé` (forme saisie lors de l’évaluation) | **Validée par le référent : « claire et limpide »** | À confirmer séparément | À évaluer | Non documentée dans le journal ; ne pas attribuer l’audio à OmniVoice sans preuve |
| 002 | `Li tao.` | En attente d’écoute | En attente de validation | En attente d’écoute | À renseigner après génération/import |
| 003 | `Daga goli.` | Non évaluée sur un fichier joint ici | **Prononciation soninké validée explicitement par le référent le 2026-10-17** | Non évalué sur un fichier joint ici | Aucun fichier audio joint à cette conversation ; moteur/source non documentés |

### Protocole pour les prochains échantillons

1. Le 2026-10-17, le référent linguistique a explicitement confirmé qu’il valide la prononciation soninké de `Daga goli.`, même sans pouvoir joindre le fichier audio ici. Consigner cette validation humaine ; ne pas prétendre que le fichier, sa clarté sonore ou le naturel de la voix ont été vérifiés indépendamment dans cette conversation.
2. Obtenir et écouter un fichier audio réel pour `Li tao.`, puis pour `Daga goli.`.
3. Noter séparément clarté, prononciation et naturel ; inscrire la source ou le moteur uniquement si elle est connue.
4. Demander au référent linguistique de confirmer la prononciation. Ne pas déduire le sens des phrases ni modifier leur orthographe sans sa validation.
5. Conserver l’audio original et ses métadonnées ensemble. Le présent journal ne contient pas les fichiers audio et ne prétend pas qu’ils sont archivés dans GitHub.
