# Guide d'enregistrement vocal — pilote soninké

Ce guide prépare des données propres et autorisées. Il ne constitue pas une garantie juridique ; les conditions de consentement et de diffusion doivent être adaptées au contexte du projet avant toute publication.

## Avant d'enregistrer

1. Choisir la variété de soninké que le pilote veut documenter et la noter explicitement. Ne pas mélanger plusieurs variétés sans les étiqueter.
2. Faire relire chaque texte par une personne compétente avant la séance. Ne pas demander au locuteur d'enregistrer une phrase dont le sens ou l'orthographe n'est pas confirmé.
3. Expliquer l'objectif : recherche et développement d'outils de reconnaissance et/ou synthèse vocale, qui pourra écouter les fichiers, où ils seront conservés, et si une diffusion publique ou un entraînement de modèles est prévu.
4. Obtenir un accord explicite avant de commencer. La personne doit pouvoir refuser une phrase, interrompre la séance ou demander le retrait selon les conditions convenues.
5. Ne jamais enregistrer une conversation privée ou une personne tierce à son insu.

## Enregistrer avec un téléphone

- Choisir une pièce calme, avec peu d'écho ; couper télévision, musique et notifications.
- Poser le téléphone sur un support stable, à environ 15–25 cm de la bouche, sans couvrir le microphone.
- Garder la même position et le même volume de voix pour toute une série.
- Parler naturellement, sans exagérer l'articulation et sans accélérer.
- Laisser environ une seconde de silence avant et après chaque phrase.
- Enregistrer une phrase par fichier quand c'est possible. Ne pas couper le début ou la fin des sons.
- Utiliser WAV non compressé si l'application le permet. Sinon, conserver le fichier original et noter son format ; ne pas convertir l'unique copie.
- Éviter les filtres, la réduction de bruit agressive, la musique et les effets de voix.
- Écouter quelques fichiers au casque après la séance et refaire immédiatement les prises avec bruit, saturation, coupure ou erreur.

## Transcription et nommage

Un nom de fichier ne doit pas contenir le nom réel, le téléphone, l'adresse ou d'autres données personnelles du locuteur.

Exemple de nommage :
`snk-varieteA-spk001-utt0001.wav`

Utiliser un identifiant pseudonyme pour le locuteur et un identifiant stable pour chaque phrase. La transcription doit correspondre à ce qui a été dit, y compris les mots omis ou repris. Si une prise est corrigée, garder l'original et enregistrer la version corrigée séparément.

Le manifeste doit inclure :
- identifiant de l'énoncé ;
- chemin local relatif vers l'audio ;
- transcription originale et, si nécessaire, version normalisée séparée ;
- langue et variété déclarées ;
- identifiant pseudonyme du locuteur ;
- date ou lot de séance, si le locuteur l'accepte ;
- statut de validation de la transcription ;
- statut de consentement et licence réellement accordée ;
- notes de qualité audio.

Ne pas inscrire « consentement obtenu » ou une licence si cela n'a pas été explicitement accepté et documenté.

## Proposition de texte de consentement à faire valider

> Je comprends que ma voix et les textes associés seront enregistrés pour le projet Soninké TTS Libre. Avant d'accepter, on m'a expliqué les usages prévus, les personnes qui pourront accéder aux fichiers, les modalités de conservation, la possibilité éventuelle de publier les données et les limites du retrait après diffusion. Je peux poser des questions, refuser certaines phrases et arrêter la séance. Je choisis séparément les usages auxquels je consens ci-dessous.

Cases à renseigner séparément, sans présumer d'un accord :
- [ ] Enregistrement de ma voix pour l'évaluation interne du projet.
- [ ] Utilisation de mes enregistrements pour entraîner ou ajuster des modèles STT/TTS.
- [ ] Partage des enregistrements et transcriptions avec les personnes contribuant au projet.
- [ ] Publication publique des enregistrements et transcriptions sous une licence qui m'a été expliquée.
- [ ] Utilisation commerciale éventuelle, après explication des conditions correspondantes.

Si une personne ne consent qu'à certains usages, respecter uniquement ceux-là. Ne pas publier une signature, un nom complet ou un contact dans le dépôt public. Les conditions de retrait, de conservation et les droits applicables doivent être expliqués clairement avant de collecter les fichiers.

## Séparation des jeux de données

- Garder un dossier privé pour les originaux et les informations de consentement.
- Ne publier dans Git que les fichiers explicitement autorisés à être diffusés et de taille adaptée.
- Pour l'évaluation STT, conserver un jeu de test séparé, avec des phrases jamais utilisées pour l'entraînement. Si plusieurs locuteurs sont disponibles, séparer les locuteurs entre entraînement et test.
- Pour le TTS mono-locuteur, vérifier la qualité et la variété des phrases ; ne pas prétendre que quelques minutes représentent toutes les voix ou variétés soninké.
- Sauvegarder les originaux en lieu sûr et limiter l'accès aux personnes autorisées.

## Contrôle qualité minimal

Pour chaque fichier, vérifier :
- [ ] fichier lisible et complet ;
- [ ] une seule phrase attendue ;
- [ ] pas de voix tierce identifiable ;
- [ ] bruit ou saturation acceptable ;
- [ ] transcription vérifiée ;
- [ ] variété documentée ;
- [ ] autorisations correspondant à l'usage prévu ;
- [ ] fichier lié au manifeste sans donnée personnelle inutile.

Aucun fichier ne doit être considéré comme prêt pour l'entraînement avant la vérification de ces points.
