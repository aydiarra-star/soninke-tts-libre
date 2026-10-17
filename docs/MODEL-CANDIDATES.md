# Inventaire des candidats STT/TTS

Dernière revue documentaire : 2026-10-17. Les fiches de modèles évoluent ; vérifier les conditions et fichiers de licence avant chaque essai. Un modèle listé ici est un candidat, pas un moteur validé par ce dépôt.

## Soninké — STT (reconnaissance vocale)

### SIL AI — wav2vec2-bloom-speech-snk

- Fiche : https://huggingface.co/sil-ai/wav2vec2-bloom-speech-snk
- Type : ASR/STT, texte à partir d'audio ; ce n'est pas un TTS.
- Base : wav2vec2-XLS-R, affiné sur le corpus Bloom Speech en soninké.
- Résultats affichés par la fiche : WER 28,88 %, CER 5,76 % sur son jeu d'évaluation. Ces scores auto-déclarés ne décrivent pas les performances sur notre variété ou nos propres enregistrements.
- Accès : dépôt à accès conditionnel, acceptation des conditions et partage possible de l'adresse e-mail et du nom d'utilisateur avec les auteurs.
- Licence : SIL International AI & NLP RAIL-M, non commerciale. La licence inclut des restrictions à conserver en cas de redistribution. Ne pas utiliser dans un service commercial sans autorisation compatible.
- Exécution : aucun fournisseur d'inférence hébergé n'est indiqué sur la fiche consultée. Prévoir potentiellement un environnement Python/Transformers et du calcul adapté.

**Décision :** premier candidat à évaluer pour STT uniquement après examen et acceptation des conditions d'accès. Tester sur un jeu soninké validé distinct du jeu d'entraînement.

## Soninké — TTS (synthèse vocale)

Aucun modèle TTS soninké n'a été confirmé comme fonctionnel par les essais de ce projet à la date de la revue. OmniVoice n'a pas produit d'audio lors du précédent essai en raison d'une limite de quota. Ne pas assimiler un modèle STT soninké à un modèle TTS.

### Résultat de la recherche documentaire du 17 octobre 2026

- Le panorama linguistique de l'UNICEF WCARO répertorie plusieurs modèles dans sa catégorie TTS pour le code de langue `snk`, dont OmniVoice, mais cette liste agrégée ne prouve ni que ces modèles acceptent réellement du texte soninké, ni qu'une voix soninké est disponible, ni qu'un audio correct peut être généré. Source : https://unicef-ventures.github.io/wca-nlp-landscape/lang/snk.html
- JollofLab décrit ses travaux vocaux/TTS comme « forthcoming » (à venir) dans son état public consulté. Ce n'est donc pas actuellement une intégration TTS prête à l'emploi pour ce dépôt. Source : https://www.jolloflab.org/
- L'essai OmniVoice déjà tenté dans ce projet n'a produit aucun fichier audio à cause de la limite de quota. Aucun résultat audio ni aucune qualité de prononciation n'ont donc été validés.

**Décision actuelle :** aucun candidat TTS soninké n'est encore qualifié pour intégration. Ne pas installer ou intégrer un modèle sur la seule base d'une liste de modèles multilingues. Le prochain essai doit confirmer explicitement la prise en charge du soninké, fonctionner avec les ressources disponibles sans achat, produire un fichier audio et être évalué par un locuteur compétent.

Prochaine démarche :
1. Rechercher les modèles et corpus TTS soninké avec leurs licences exactes.
2. Prioriser un essai d'inférence reproductible si un modèle approprié existe.
3. Si aucun modèle utilisable n'existe, établir d'abord le corpus et les droits, puis étudier un fine-tuning.
4. Garder les trois phrases historiques intactes ; ne pas leur inventer de traduction.

## Wolof — TTS (piste séparée, ne pas confondre avec le soninké)

### CONCREE/Adia_TTS

- Fiche : https://huggingface.co/CONCREE/Adia_TTS
- Type : TTS wolof basé sur Parler-TTS mini multilingual.
- La fiche décrit un entraînement sur environ 40 heures de données vocales wolof.
- Licence indiquée : Apache-2.0 ; la fiche demande l'attribution à CONCREE et un usage respectueux de la langue et de la culture. Vérifier les licences des données et dépendances avant redistribution.
- Contraintes documentées : modèle d'environ 1,88 Go, environ 3,9 Go de RAM minimale recommandée et accélération GPU indiquée pour l'usage présenté. La fiche ne montre pas de fournisseur d'inférence hébergé au moment de la revue.
- Espace de démonstration référencé par le modèle : https://huggingface.co/spaces/CONCREE/Adia_TTS

**Décision :** candidat pour un futur banc d'essai wolof, pas une solution soninké et pas encore validé par ce dépôt.

### HullJi/speecht5_tts-wolof

- Fiche : https://huggingface.co/HullJi/speecht5_tts-wolof
- Type : TTS wolof basé sur SpeechT5, tokenizer spécialisé.
- La fiche signale que la qualité peut varier selon les phrases et que les mots hors vocabulaire ou caractères inconnus peuvent poser problème.
- Licence affichée : MIT sur la fiche du modèle ; vérifier aussi les licences des composants de base, des données et des poids vocodeur avant toute intégration.
- **Décision :** candidat alternatif pour un test wolof uniquement.

## Protocole de comparaison

Pour chaque candidat :
- noter date, URL et version/commit du modèle ;
- enregistrer la licence et les conditions d'accès ;
- conserver une transcription de référence relue par un locuteur compétent ;
- tester des phrases inédites et documenter les erreurs ;
- ne jamais présenter les scores du modèle sur son propre jeu d'évaluation comme résultats du projet ;
- distinguer clairement les essais soninké des essais wolof ;
- ne publier ni audios de locuteurs ni données privées sans consentement.

## Sources

- UNICEF WCARO, panorama des ressources NLP soninké : https://unicef-ventures.github.io/wca-nlp-landscape/lang/snk.html
- JollofLab : https://www.jolloflab.org/
- SIL AI Soninke ASR : https://huggingface.co/sil-ai/wav2vec2-bloom-speech-snk
- CONCREE Adia TTS : https://huggingface.co/CONCREE/Adia_TTS
- SpeechT5 Wolof : https://huggingface.co/HullJi/speecht5_tts-wolof
