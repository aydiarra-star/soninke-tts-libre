# Évaluation du lecteur vocal wolof

## Candidats identifiés

### 1. ADIA_TTS — candidat prioritaire pour un premier essai léger

- Modèle : https://huggingface.co/CONCREE/Adia_TTS
- Échantillons audio et démonstration : https://huggingface.co/spaces/CONCREE/Adia_TTS
- Licence indiquée sur la fiche du modèle : Apache-2.0 ; conserver l’attribution à CONCREE et examiner les fichiers/licences des dépendances avant distribution.
- Fiche du modèle : environ 40 heures de données wolof, 24 kHz, modèle annoncé à environ 1,88 Go et RAM recommandée autour de 3,9 Go.
- Limite documentée : jusqu’à 200 caractères par génération sans segmentation ; les nombres, dates et longues phrases peuvent être moins fiables.
- La fiche consultée ne montrait pas de fournisseur d’inférence hébergé. Ne pas promettre une API gratuite permanente.

### 2. Oolel Voices — deuxième candidat à écouter, plus récent

- Démonstration interactive : https://huggingface.co/spaces/soynade-research/Oolel-Voices
- Fiche du modèle : https://huggingface.co/soynade-research/Oolel-Voices
- Le projet annonce une synthèse dédiée au wolof et au mélange wolof-français, avec contrôle expressif et voix de référence facultative.
- Licence affichée sur le dépôt du modèle : AGPL-3.0. Cela impose une analyse de licence avant intégration dans un service web ; ne pas supposer que les obligations conviennent automatiquement au produit.
- Les fichiers du dépôt représentent plusieurs gigaoctets (environ 8,5 Go indiqués pour le dépôt). Le modèle est donc plus lourd à exécuter dans un environnement gratuit limité.
- L’API Soynade est payante à l’usage : la page de tarification consultée indique 0,22 USD pour 1 000 caractères. La démo interactive est une piste d’écoute, mais ni sa gratuité permanente ni sa disponibilité ne sont garanties.

### 3. Kiriku Wolof TTS — piste de comparaison

- Modèle : https://huggingface.co/AIHubSN/Kiriku-Wolof-TTS
- L’accès aux fichiers demande d’accepter des conditions ; examiner la licence et les conditions d’accès avant usage.

### 4. GalsenAI xTTS-v2-wolof — piste de comparaison conditionnelle

- Modèle : https://huggingface.co/galsenai/xTTS-v2-wolof
- Vérifier particulièrement les restrictions d’utilisation : le dépôt de déploiement xTTS consulté signale une restriction non commerciale. Ne pas choisir ce candidat pour un produit commercial sans clarification écrite des droits.

## Objectif de la première étape

Obtenir un petit lot d’audios réels et évaluer la qualité, sans toucher à la branche principale ni publier une nouvelle voix comme validée.

1. Écouter d’abord les échantillons disponibles d’ADIA_TTS et la démonstration Oolel Voices, si elles sont accessibles.
2. Générer ensuite 10 à 20 WAV avec ADIA_TTS dans un environnement gratuit à durée limitée (par exemple Google Colab ou Kaggle, selon disponibilité réelle du service et du quota).
3. Sélectionner les entrées wolof déjà présentes dans les données du projet, en conservant leur graphie exacte et leur source. Le notebook génère un premier lot de 10 mots pour vérifier la chaîne technique ; ce lot n’est pas un corpus linguistiquement validé.
4. Conserver pour chaque audio le texte exact, le modèle/version, la date, les paramètres, le fichier audio et le statut de validation.
5. Vérifier l’écoute avec un locuteur wolof compétent : prononciation, rythme, diacritiques, intelligibilité et éventuelles omissions.
6. Ne pas intégrer les WAV dans la page publique tant que la prononciation, la provenance et les droits de redistribution des fichiers n’ont pas été vérifiés.

## Architecture recommandée pour le lecteur

La page GitHub Pages actuelle est statique : elle ne peut pas charger raisonnablement un modèle de près de 2 Go ou davantage dans le navigateur. Ne pas télécharger le modèle à chaque ouverture et ne pas exposer de clé API dans le JavaScript client.

Ordre recommandé :

1. **Prototype hors ligne contrôlé** : générer quelques fichiers WAV, les écouter et les faire valider.
2. **Lecteur web** : afficher un bouton « Écouter » seulement pour les entrées disposant d’un audio réellement disponible et d’un statut explicite. Prévoir une indication claire « audio en préparation » pour les autres.
3. **Petit catalogue d’audios** : envisager des WAV statiques pour les mots/phrases de leçons les plus utiles, si la taille, les droits et le budget de stockage sont acceptables.
4. **Génération à la demande** : seulement après étude d’un hébergement gratuit réellement stable, de la latence, des quotas et de la confidentialité. Une session Colab n’est pas une API de production permanente.

Ne pas utiliser automatiquement la voix française du navigateur pour lire du wolof : elle risque de mal prononcer les graphies wolof. Le fallback doit être explicite, sans présenter une voix incorrecte comme wolof.

## Conditions avant validation

- [ ] Au moins 10 WAV réellement générés, pas seulement un notebook qui s’exécute.
- [ ] Fichiers audio lisibles, durée non nulle, fréquence d’échantillonnage documentée.
- [ ] Texte source et audio associés sans décalage.
- [ ] Écoute humaine et statut de validation conservés.
- [ ] Licence du modèle, dépendances, données d’entraînement et conditions de redistribution documentées.
- [ ] Test mobile du lecteur sur Safari/iPhone et Android.
- [ ] Aucune modification de `main` ni publication de la page avant validation explicite.

## État

**À l’étude — non validé.** Aucun audio ADIA_TTS ou Oolel Voices n’a encore été généré ou contrôlé dans le cadre de ce dépôt. La présence d’un modèle ou d’une démo ne constitue pas une preuve de qualité phonétique pour les leçons.
