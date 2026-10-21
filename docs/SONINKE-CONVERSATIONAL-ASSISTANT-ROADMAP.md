# Feuille de route — assistant conversationnel en soninké

## Vision

Construire progressivement un assistant capable de dialoguer en soninké, d'expliquer le lexique, d'aider à apprendre la langue et, lorsque les briques vocales seront suffisamment fiables, de tenir une conversation orale. Le projet doit réutiliser les ressources existantes sans confondre démonstration technique et validation linguistique.

## Point de départ vérifié dans le dépôt

- Le dépôt public actuel est `aydiarra-star/xamxam-xara` ; l'ancien nom `soninke-tts-libre` redirige vers ce dépôt.
- Le README décrit 577 entrées soninké et 576 fichiers WAV décodables distincts dans l'inventaire audio ; l'identifiant `snk-00308` est signalé manquant.
- Une base lexicale soninké–français de 213 entrées a été préparée dans les travaux du dépôt. Les correspondances et variantes doivent être conservées, et les entrées non vérifiées doivent rester marquées comme telles.
- Un corpus d'apprentissage comprend 106 phrases/paragraphes soninké–français avec attribution de source et licence CC BY 4.0. Il n'inclut pas d'audio natif dans ce lot et n'a pas été intégralement revérifié par le référent du projet.
- Le README précise que l'essai OmniVoice n'a pas produit d'audio à cause d'une limite de quota. Aucun moteur TTS soninké ne doit donc être annoncé comme validé sur cette seule base.
- Le prototype web existant comprend des fonctions de consultation/validation de données et des lecteurs audio ; la disponibilité réelle des ressources doit être vérifiée avant de la considérer comme une fonction terminée.

Les compteurs et statuts ci-dessus sont un état de départ à recontrôler dans les manifestes avant chaque publication.

## Principes non négociables

1. Préserver les fichiers audio, identifiants, graphies, variantes, traductions, exemples, licences et provenance existants.
2. Séparer validation technique (fichier lisible, format, durée) et validation humaine (prononciation, traduction, naturel de la phrase).
3. Ne jamais inventer une traduction, un enregistrement, une validation ou une capacité linguistique.
4. Signaler explicitement quand l'assistant est incertain, notamment pour les variétés, graphies ou sens ambigus.
5. Ne jamais exposer une clé API dans le navigateur, les journaux ou le dépôt.
6. Respecter les licences et consentements des corpus, voix, modèles et poids externes ; la licence du code ne couvre pas automatiquement ces ressources.
7. Ne pas entraîner un grand modèle depuis zéro au début : mesurer d'abord ce que permet un modèle existant associé à une base de connaissances contrôlée.

## Plan par étapes

### Phase 0 — Audit et fondations

- Vérifier la branche principale, les PR ouvertes, le site publié et les tests existants.
- Établir un inventaire machine-readable des entrées lexicales, variantes, sources, statuts de validation et références audio.
- Ajouter des contrôles empêchant la disparition silencieuse d'une entrée ou d'un WAV existant.
- Documenter les licences, les données autorisées pour l'entraînement et les données qui ne peuvent servir qu'à la consultation.

**Critère de sortie :** un inventaire reproductible et des contrôles qui passent, sans remplacer les données canoniques.

### Phase 1 — Assistant textuel de démonstration

- Créer une interface mobile simple avec conversation, choix de langue de réponse et accès aux sources.
- Commencer par des tâches délimitées : chercher un mot, donner les sens enregistrés, afficher les variantes, expliquer une phrase issue d'une source et traduire lorsque la donnée existe.
- Connecter un modèle de langage via un petit backend sécurisé ; les secrets restent côté serveur.
- Fournir au modèle uniquement les entrées pertinentes du lexique/corpus et lui demander de distinguer les données sourcées de ses propositions.
- Ajouter des tests de référence préparés et relus par le référent linguistique.

**Critère de sortie :** une démo qui répond correctement aux requêtes lexicales de test, cite ses sources et indique quand les données manquent. Elle ne doit pas encore être présentée comme un ChatGPT qui maîtrise parfaitement le soninké.

### Phase 2 — Évaluation conversationnelle

- Constituer un jeu d'essai avec questions simples, paraphrases, ambiguïtés, variantes orthographiques, erreurs de frappe et demandes hors domaine.
- Faire noter les réponses par des locuteurs compétents : exactitude du sens, grammaire, variété, naturel et degré de confiance.
- Comparer plusieurs modèles et paramètres sur le même jeu de test avant de choisir une solution.
- Conserver les corrections validées comme données de référence avec provenance et consentement.

**Critère de sortie :** des résultats mesurés, les limites documentées et un processus de correction reproductible.

### Phase 3 — Réponse parlée (TTS)

- Réutiliser le pipeline audio existant et tester un moteur sur un petit lot contrôlé.
- Vérifier les droits du moteur et de ses poids avant tout usage public ou commercial.
- Produire des WAV réels, contrôler leur intégrité et faire écouter chaque échantillon.
- Ne marquer une prononciation comme validée qu'après approbation humaine explicite.

**Critère de sortie :** des échantillons réels, reproductibles, licites et approuvés ; aucun statut déduit du seul succès du workflow.

### Phase 4 — Compréhension orale (STT) et dialogue vocal

- Évaluer d'abord la reconnaissance sur des enregistrements autorisés et transcrits par des personnes compétentes.
- Mesurer les erreurs de transcription et documenter les performances par type de phrase et variété.
- Relier STT, assistant textuel et TTS avec possibilité de corriger la transcription avant la réponse.
- Prévoir un mode texte de secours et des messages clairs lorsque la reconnaissance échoue.

**Critère de sortie :** un dialogue de bout en bout dont chaque composant est évalué séparément.

### Phase 5 — Ouverture et pérennité

- Publier le code et les jeux de données uniquement selon leurs licences respectives.
- Proposer un mécanisme de contribution, de correction, d'attribution et de retrait des données.
- Mesurer coûts, latence, accessibilité mobile et éventuel fonctionnement hors connexion.
- Envisager un modèle spécialisé ou un fine-tuning seulement si les évaluations démontrent un gain et si les droits, le volume de données et le budget le permettent.

## Architecture de départ recommandée

- **Interface :** application web mobile réutilisant autant que possible les composants du dépôt.
- **Connaissances :** fichiers lexicaux et corpus versionnés, avec source et statut de validation conservés.
- **Orchestration :** backend léger qui récupère les entrées pertinentes et appelle un modèle existant ; aucun secret dans le frontend.
- **Évaluation :** tests automatisés de structure et jeu de questions/réponses validé par des locuteurs.
- **Audio :** manifestes existants, lecteurs et pipelines TTS/STT indépendants du modèle conversationnel.

Le stockage vectoriel ou le fine-tuning ne sont pas des prérequis pour le premier prototype : une recherche lexicale simple est préférable tant que le corpus reste de taille modeste.

## Première livraison proposée

Une preuve de concept textuelle, limitée mais réelle, qui :
1. recherche une entrée ou une phrase dans les ressources disponibles ;
2. affiche les graphies, traductions, sources et statuts existants sans les réécrire ;
3. répond en français ou propose une réponse en soninké uniquement quand les données et l'évaluation le justifient ;
4. affiche clairement « donnée non vérifiée » ou « information absente » plutôt que de présenter une supposition comme un fait ;
5. possède un petit jeu de tests reproductible.

Cette livraison ne doit ni modifier les WAV existants, ni exposer de clé, ni prétendre que la reconnaissance vocale ou la synthèse soninké sont déjà validées.
