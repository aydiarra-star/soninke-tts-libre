# Premier essai TTS soninké sans quota de démo

Ce guide contourne le blocage rencontré sur le Space Hugging Face : on utilise le notebook officiel OmniVoice dans Google Colab plutôt que de dépendre du quota ZeroGPU du Space. **Colab peut lui aussi ne pas attribuer de GPU gratuit** ; ce chemin est un essai à coût zéro si les ressources gratuites sont disponibles, pas une garantie de calcul gratuit.

## Liens officiels

- [Ouvrir le notebook OmniVoice dans Google Colab](https://colab.research.google.com/github/k2-fsa/OmniVoice/blob/master/docs/OmniVoice.ipynb)
- [Dépôt OmniVoice et installation officielle](https://github.com/k2-fsa/OmniVoice)
- [Fiche du modèle et licences](https://huggingface.co/k2-fsa/OmniVoice)
- [Liste officielle des langues](https://github.com/k2-fsa/OmniVoice/blob/master/docs/languages.md)

La liste des langues indique Soninke (`snk`). Cela justifie un essai, mais ne prouve pas que la prononciation soninké soit bonne. La fiche indique une licence non commerciale pour les poids pré-entraînés : ne pas employer ces poids dans une offre commerciale ni les redistribuer sans autorisation compatible.

## Procédure depuis un téléphone

1. Ouvrir le notebook Colab dans Safari ou Chrome et se connecter à Google si demandé.
2. Dans le menu **Environnement d'exécution**, choisir **Modifier le type d'exécution**, puis GPU si l'option gratuite est proposée. Si aucun GPU n'est disponible, arrêter là et noter le message ; ne souscrire à aucun forfait.
3. Exécuter les cellules d'installation puis de chargement du modèle du notebook officiel. Le téléchargement est volumineux et peut prendre du temps.
4. Dans la section de génération automatique (« Auto Voice »), remplacer uniquement le texte de démonstration par **une phrase soninké dont la formulation a été validée**. Pour notre première vérification, utiliser `Daga goli.`. Ne lui ajouter aucune traduction.
5. Si l'interface propose explicitement un choix de langue, sélectionner **Soninke / Soninké (`snk`)**. Si aucun choix de langue n'est visible et que le notebook n'expose pas ce paramètre, ne pas supposer que le modèle a bien utilisé le soninké : consigner cette limite.
6. Exécuter la cellule de génération. Le notebook officiel enregistre normalement l'audio sous forme de fichier WAV et l'affiche pour écoute. Télécharger le fichier WAV réel avec l'outil de téléchargement de Colab si la génération réussit.
7. Écouter l'audio et noter séparément : clarté, exactitude de la prononciation, naturel de la voix. La validation déjà donnée par le référent pour la phrase `Daga goli.` valide la phrase/prononciation selon son appréciation ; elle ne prouve pas à elle seule que cet éventuel nouvel audio est correct.
8. Conserver le fichier audio et noter la date, le nom/version du modèle, les réglages, le message de résultat et la source. Ne pas déposer un enregistrement privé dans le dépôt public sans consentement explicite.

## Si la génération échoue

- **GPU indisponible / quota épuisé** : arrêter sans payer ; noter l'erreur exacte et réessayer ultérieurement ou sur un ordinateur déjà disponible.
- **Mémoire insuffisante ou téléchargement interrompu** : ne pas déclarer le test réussi. Noter la cellule qui échoue.
- **Pas de sélecteur Soninke ou `snk`** : ne pas interpréter un audio produit comme une validation du soninké avant d'avoir confirmé le paramètre de langue.
- **Audio créé mais prononciation douteuse** : garder l'échantillon comme échec/essai, pas comme voix validée.

## Ce que ce guide ne promet pas

- Il ne garantit ni GPU gratuit ni génération réussie.
- Il ne remplace pas l'écoute d'un fichier audio réel.
- Il n'intègre pas encore OmniVoice dans l'application Soninké TTS Libre.
- Il ne change pas les trois phrases historiques du projet : `Daga yige`, `Li tao`, `Daga goli`.
