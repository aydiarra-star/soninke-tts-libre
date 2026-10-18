# Premier essai TTS soninké sans quota de démo

Ce guide contourne le blocage rencontré sur le Space Hugging Face : on utilise le notebook officiel OmniVoice dans Google Colab plutôt que de dépendre du quota ZeroGPU du Space. **Colab peut lui aussi ne pas attribuer de GPU gratuit** ; ce chemin est un essai à coût zéro si les ressources gratuites sont disponibles, pas une garantie de calcul gratuit.

## Liens officiels

- [Ouvrir le notebook OmniVoice dans Google Colab](https://colab.research.google.com/github/k2-fsa/OmniVoice/blob/master/docs/OmniVoice.ipynb)
- [Dépôt OmniVoice et installation officielle](https://github.com/k2-fsa/OmniVoice)
- [Fiche du modèle et licences](https://huggingface.co/k2-fsa/OmniVoice)
- [Liste officielle des langues](https://github.com/k2-fsa/OmniVoice/blob/master/docs/languages.md)
- [Code officiel de l'API de génération](https://github.com/k2-fsa/OmniVoice/blob/master/omnivoice/models/omnivoice.py)

La liste des langues et le code officiel confirment que le nom `soninke` est accepté et associé au code `snk`. Cela justifie un essai, mais ne prouve pas que la prononciation soninké soit bonne. La fiche indique une licence non commerciale pour les poids pré-entraînés : ne pas employer ces poids dans une offre commerciale ni les redistribuer sans autorisation compatible.


## Notebook personnalisé prêt à lancer

Le dépôt contient maintenant un notebook dédié qui installe OmniVoice, vérifie la présence d’un GPU, charge le modèle officiel, génère les trois phrases historiques (`Daga yige`, `Li tao`, `Daga goli`), enregistre les WAV et prépare une archive ZIP à télécharger :

- [Voir le notebook dans GitHub](../notebooks/OmniVoice-Soninke-TTS.ipynb)
- [Ouvrir directement dans Google Colab](https://colab.research.google.com/github/aydiarra-star/soninke-tts-libre/blob/feat/soninke-tts-lab-prototype/notebooks/OmniVoice-Soninke-TTS.ipynb)

Le notebook s’arrête volontairement si aucun GPU n’est disponible, afin d’éviter un calcul CPU potentiellement très long. Il ne souscrit à aucun forfait, ne publie pas les audios sur GitHub et marque chaque nouvelle génération comme « validation humaine en attente ».

## Procédure depuis un téléphone

1. Ouvrir le notebook Colab dans Safari ou Chrome et se connecter à Google si demandé.
2. Dans le menu **Environnement d'exécution**, choisir **Modifier le type d'exécution**, puis GPU si l'option gratuite est proposée. Si aucun GPU n'est disponible, arrêter là et noter le message ; ne souscrire à aucun forfait.
3. Exécuter les cellules d'installation puis de chargement du modèle du notebook officiel. Le téléchargement est volumineux et peut prendre du temps.
4. Aller à la section **Python API** du notebook, après la cellule qui charge `model` et `soundfile as sf`. Ajouter une nouvelle cellule de code avec exactement ceci :

   ```python
   from IPython.display import Audio, display

   audio = model.generate(
       text="Daga goli.",
       language="soninke",
   )
   sf.write("soninke_daga_goli.wav", audio[0], model.sampling_rate)
   display(Audio(audio[0], rate=model.sampling_rate))
   ```

   Cette cellule transmet explicitement la langue `soninke` au moteur et enregistre un vrai fichier WAV. Ne pas ajouter de traduction ni modifier la phrase.

5. Exécuter la cellule. Si elle réussit, écouter le résultat dans le notebook et télécharger `soninke_daga_goli.wav` depuis l'espace de fichiers de Colab.
6. Évaluer séparément la clarté, l'exactitude de la prononciation et le naturel de la voix. La validation déjà donnée par le référent pour la phrase `Daga goli.` ne prouve pas à elle seule que ce nouvel audio est correct.
7. Conserver le fichier audio et noter la date, le nom/version du modèle, les réglages, le message de résultat et la source. Ne pas déposer un enregistrement privé dans le dépôt public sans consentement explicite.

## Si la génération échoue

- **GPU indisponible / quota épuisé** : arrêter sans payer ; noter l'erreur exacte et réessayer ultérieurement ou sur un ordinateur déjà disponible.
- **Mémoire insuffisante ou téléchargement interrompu** : ne pas déclarer le test réussi. Noter la cellule qui échoue.
- **Erreur indiquant que la langue est inconnue** : ne pas retirer le paramètre de langue en silence ; relever l'erreur et vérifier la version du modèle et sa liste de langues.
- **Audio créé mais prononciation douteuse** : garder l'échantillon comme essai non validé, pas comme voix validée.

## Ce que ce guide ne promet pas

- Il ne garantit ni GPU gratuit ni génération réussie.
- Il ne remplace pas l'écoute d'un fichier audio réel.
- Il n'intègre pas encore OmniVoice dans l'application Soninké TTS Libre.
- Il ne change pas les trois phrases historiques du projet : `Daga yige`, `Li tao`, `Daga goli`.
