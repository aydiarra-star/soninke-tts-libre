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

## Ressources linguistiques repérées
- Asawan, lexique Soninké-Français-Anglais : https://www.asawan.org/fr/lexique_soninke
- Asawan, guides de lecture/écriture : https://www.asawan.org/fr/apprendre-sonink%C3%A9-ajami
- Soninké structuré et corpus : https://oscarmedra.github.io/snk_engine/ (données annoncées CC BY 4.0 ; conserver l’attribution fournie par la source)
- Jàngileen : https://jangileen.kalam-alami.net/special/apropos (le site indique que les données du dictionnaire peuvent être réutilisées et redistribuées ; vérifier les mentions propres à chaque ressource)
- Baatukaay : https://github.com/alphajoop/baatukaay (dépôt annoncé sous licence MIT ; vérifier séparément la licence des données lexicales avant extraction)
- Kaikki / Wiktionary Wolof : https://kaikki.org/frwiktionary/Wolof/index.html (données extraites de Wiktionary ; conserver l’attribution et la licence applicable)

Ces liens sont ajoutés à l’interface comme références externes. Aucun dictionnaire propriétaire ou corpus tiers n’est copié dans le dépôt sans vérification de licence. La prochaine étape de recherche est d’établir une fiche de provenance par source, de confirmer les droits des données lexicales, puis d’importer seulement les corpus autorisés avec leurs champs de citation.
