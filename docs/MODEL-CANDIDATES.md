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

### Candidat prioritaire à tester — k2-fsa/OmniVoice

- Dépôt du modèle : https://huggingface.co/k2-fsa/OmniVoice
- Code source et liste des langues : https://github.com/k2-fsa/OmniVoice/blob/master/docs/languages.md
- Type : synthèse vocale multilingue (TTS).
- La liste officielle indique explicitement **Soninke**, code ISO 639-3 `snk`, avec 10,04 heures de données d'entraînement répertoriées. Cela en fait un candidat réellement pertinent, contrairement à une simple supposition à partir d'un modèle multilingue.
- Licence du code : Apache-2.0. **Licence des poids pré-entraînés : CC-BY-NC (non commerciale)** selon la fiche officielle du modèle ; ne pas intégrer dans un service commercial sans autorisation/licence compatible. La licence des poids ne doit pas être confondue avec celle du code.
- Taille du dépôt de modèle : environ 3,27 Go (poids `model.safetensors` : environ 2,45 Go). L'inférence peut dépasser les ressources d'un téléphone et nécessiter un ordinateur ou GPU.
- Démo officielle : https://huggingface.co/spaces/k2-fsa/OmniVoice . La page du modèle indique qu'aucun fournisseur d'inférence hébergé n'est actuellement configuré pour appeler le modèle directement via l'API d'Inference Providers ; la démo Space est donc la piste à tester séparément et peut être soumise à une limite de quota.
- Le modèle prend en charge une génération avec voix automatique ou avec audio de référence. Toute voix de référence doit être utilisée avec consentement explicite. La qualité sur des clips soninké courts reste à vérifier.
- L'essai précédent effectué pour ce projet n'a pas produit d'audio à cause d'une limite de quota. La prise en charge déclarée de `snk` est prometteuse, mais la prononciation, l'intelligibilité et le coût réel d'exécution restent **non validés** ici.

**Décision :** OmniVoice devient le premier candidat TTS soninké à retester. Ne pas annoncer que le TTS fonctionne avant d'avoir généré un fichier audio, vérifié le fichier, puis obtenu l'avis d'un locuteur compétent. L'absence de quota gratuit disponible reste un blocage opérationnel possible.

### Autre piste

- JollofLab décrit ses travaux vocaux/TTS comme « forthcoming » (à venir) dans son état public consulté ; ce n'est pas actuellement une intégration prête à l'emploi pour ce dépôt. Source : https://www.jolloflab.org/

Prochaine démarche :
1. Ouvrir la démo officielle https://huggingface.co/spaces/k2-fsa/OmniVoice et vérifier si elle est réveillée et si le sélecteur de langue propose Soninke/Sonké.
2. Utiliser uniquement une phrase soninké validée par un locuteur. Les trois phrases historiques restent intactes ; ne pas leur inventer de traduction.
3. Si l'interface est disponible, lancer une génération courte en sélectionnant explicitement Soninke, puis sauvegarder le fichier audio réel. Noter les paramètres et toute erreur/limite de quota.
4. Faire écouter l'audio à un locuteur compétent avant de considérer le candidat acceptable. Si la démo est indisponible ou en quota nul, noter le blocage plutôt que de prétendre que le test a réussi.

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
- OmniVoice — liste officielle des langues : https://github.com/k2-fsa/OmniVoice/blob/master/docs/languages.md
- OmniVoice — modèle : https://huggingface.co/k2-fsa/OmniVoice
- OmniVoice — problème de génération de clips courts : https://github.com/k2-fsa/OmniVoice/issues/118
- JollofLab : https://www.jolloflab.org/
- SIL AI Soninke ASR : https://huggingface.co/sil-ai/wav2vec2-bloom-speech-snk
- CONCREE Adia TTS : https://huggingface.co/CONCREE/Adia_TTS
- SpeechT5 Wolof : https://huggingface.co/HullJi/speecht5_tts-wolof
