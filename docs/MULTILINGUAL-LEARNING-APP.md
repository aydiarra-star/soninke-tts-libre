# Langues en partage — évolution de Soninké TTS Libre

## Vision
Faire de Soninké TTS Libre une application ouverte, simple d’accès et incontournable pour les amoureux des langues et l’apprentissage au Sénégal et en Afrique.

## Langues au lancement
Soninké, wolof, français et anglais. Le format est extensible pour le pulaar, le bambara, le sérère et d’autres langues.

## Principes
- Préserver le lexique soninké et les WAV existants.
- Distinguer disponibilité technique, validation de prononciation, validation de traduction et provenance.
- Ne pas inventer de traduction ni d’audio natif. La synthèse vocale du navigateur est indiquée comme telle.
- Garder une première version légère : HTML/CSS/JavaScript, pas de compte obligatoire ni de service payant nécessaire pour explorer.
- Autoriser ajout local et export JSON/CSV. Les contributions du prototype ne sont pas publiées automatiquement.

## Fichiers
- `apprendre.html` : interface d’apprentissage adaptée au mobile.
- `apprendre.css` : styles responsives.
- `apprendre.js` : recherche, filtres, lecture audio, synthèse vocale navigateur pour français/anglais, ajout local et exports.
- `data/trilingual-lexicon.json` : registre des langues et schéma extensible.

## Suite
1. Vérifier les contrôles CI et le chargement des ressources.
2. Tester la lecture réelle sur Safari iPhone et navigateur de bureau.
3. Ajouter un premier lexique wolof documenté avec sources fiables.
4. Préparer un flux de contribution simple pour les audios et corrections communautaires.
5. Intégrer via PR sans réinitialiser ni écraser le travail existant.