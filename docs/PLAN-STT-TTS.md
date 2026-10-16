# Plan technique STT/TTS — Soninké TTS Libre

## Objectif

Construire une chaîne expérimentale reproductible pour le soninké, en commençant par une variété linguistique explicitement identifiée. Ne jamais présenter un moteur comme fonctionnel sans audio ou transcription réellement produit(e), mesures documentées et vérification par des locuteurs compétents.

## Principes non négociables

- Préserver les trois phrases initiales exactement : `Daga yige`, `Li tao`, `Daga goli`. Aucune traduction ne doit être inventée.
- Garder séparés les exemples issus de sources externes et les phrases vérifiées par le projet.
- Enregistrer la variété/dialecte, l'orthographe utilisée, la provenance et la licence de chaque élément.
- Obtenir le consentement explicite des locuteurs pour l'enregistrement, le traitement IA et les usages prévus.
- Ne pas envoyer d'enregistrements personnels à un service tiers sans consentement et information appropriés.
- Vérifier séparément les licences du code, des poids de modèles et des données.
- Budget initial : outils gratuits, enregistrement au téléphone dans un environnement calme, essais courts. Aucun achat ni service payant sans accord explicite.

## Phase 0 — Qualifier les données

1. Faire relire les cinq exemples de `data/soninke-samples.jsonl` par au moins un locuteur compétent.
2. Pour chaque exemple, noter : validé / à corriger / variété inconnue, commentaire, date et identifiant du validateur (sans publier son identité sans accord).
3. Ne pas utiliser les exemples non validés comme vérité terrain pour calculer les performances.
4. Définir une convention d'orthographe avec le référent linguistique. Conserver la transcription originale et toute forme normalisée dans des champs séparés.
5. Préparer une fiche de consentement simple indiquant finalités, accès, durée de conservation, possibilité de retrait et licence de partage envisagée.

**Sortie attendue :** un petit ensemble de phrases dont le texte et la variété ont été relus, avec provenance et droits documentés.

## Phase 1 — Collecter un corpus pilote

- Commencer par 50 à 100 phrases variées et vérifiées, enregistrées par consentement explicite. C'est un pilote de faisabilité, pas une taille suffisante garantie pour un modèle de production.
- Enregistrer en WAV mono si possible, à fréquence d'échantillonnage native du téléphone ; éviter musique, bruit, réverbération et compression excessive.
- Garder des phrases courtes et naturelles, sans couper les consonnes au début ou à la fin.
- Garder un identifiant stable et un fichier audio distinct par phrase.
- Conserver les fichiers maîtres hors du dépôt Git tant que les droits et la stratégie de stockage ne sont pas confirmés.
- Faire relire les transcriptions par une seconde personne lorsque possible.
- Séparer les données d'entraînement et de test par locuteur si plusieurs locuteurs participent, afin d'éviter qu'une même voix figure dans les deux ensembles.

### Manifeste de données recommandé

Prévoir un CSV ou JSONL avec au minimum :

- `utterance_id`
- `audio_path` (chemin relatif, pas de lien privé)
- `transcript_original`
- `transcript_normalized` (facultatif, règle documentée)
- `language` (ex. `snk`, si le code est approprié au corpus)
- `variety`
- `speaker_id` (pseudonyme, pas le nom réel)
- `recording_consent`
- `license`
- `source`
- `transcript_review_status`
- `split` (`train`, `validation`, `test`)

Ne jamais marquer un consentement ou une licence comme acquis sans preuve réelle.

## Phase 2 — Évaluer le STT (audio vers texte)

1. Constituer un jeu de test de phrases inédites, transcrites et relues par un locuteur compétent.
2. Établir d'abord une référence manuelle et un protocole d'orthographe.
3. Tester un modèle multilingue existant sur ces audios sans réentraînement, si un environnement gratuit et autorisé est disponible.
4. Enregistrer modèle/version, paramètres, date, résultat brut, transcription de référence et erreurs observées.
5. Mesurer le taux d'erreur de caractères (CER) et, si la segmentation des mots est stable, le taux d'erreur de mots (WER). Ces scores ne remplacent pas l'évaluation humaine.
6. Si les résultats sont faibles, analyser les erreurs avant d'envisager un fine-tuning. Le fine-tuning demande des données licenciées, des ressources de calcul et une procédure reproductible.

**Critère d'acceptation pilote :** une transcription est produite par un modèle réel, les résultats sont comparés à des références vérifiées, les erreurs et limites sont publiées sans prétendre à une prise en charge générale du soninké.

## Phase 3 — Évaluer le TTS (texte vers audio)

1. Faire un inventaire des modèles candidats et vérifier langue, méthode d'entraînement, licence du code, licence des poids et restrictions commerciales.
2. Ne pas supposer que XTTS-v2, Piper ou Bark prennent en charge le soninké simplement parce qu'ils sont open source.
3. Tester d'abord l'inférence existante si le modèle déclare une prise en charge pertinente. Documenter précisément tout échec technique ou limite de quota.
4. N'envisager un entraînement ou fine-tuning qu'après validation des transcriptions, du consentement, des licences et du format audio.
5. Produire des fichiers audio réels pour un ensemble fixe de phrases de test.
6. Faire écouter les résultats à des locuteurs compétents et noter intelligibilité, prononciation, prosodie et erreurs. Ne pas utiliser seulement une note automatique.

**Critère d'acceptation pilote :** au moins un fichier audio réellement généré, reproductible avec le modèle et les paramètres documentés, puis évalué par un locuteur compétent. Cela ne suffit pas à déclarer le système prêt pour la production.

## Phase 4 — Reproductibilité et publication

Avant d'intégrer un modèle dans l'application, publier :
- instructions exactes de reproduction ;
- versions des dépendances et modèle ;
- provenance et licence des données ;
- résultats et exemples d'échec ;
- limites de variété, de prononciation et d'usage ;
- procédure de correction ou retrait de données.

Ne pas publier de voix, de transcriptions privées ou de données d'identification sans autorisation.

## État actuel

- Le laboratoire web permet des annotations manuelles et l'import local d'audios.
- Le corpus d'exemples est sourcé mais doit encore être relu indépendamment.
- Aucun TTS n'a encore produit un audio vérifié dans ce projet.
- Aucun STT n'a encore été évalué sur un jeu de test soninké validé.
- Ce document est un plan de travail, pas une preuve de fonctionnement.
