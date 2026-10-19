# Génération privée de trois échantillons vocaux wolof

## Objectif
Tester Oolel-Voices avec la référence vocale autorisée, pour les trois mots de contrôle :
- Jërëjëf — Merci
- Kër — Maison
- Ñëw — Venir

## Confidentialité
- Ne jamais committer le fichier audio source ou sa chaîne Base64 dans le dépôt.
- Configurer la chaîne Base64 comme secret GitHub Actions nommé `WOLOF_REFERENCE_AUDIO_B64`.
- Le workflow ne doit pas imprimer la valeur du secret.
- Les WAV sont rassemblés puis chiffrés avant d'être stockés comme artefact temporaire.
- La clé de chiffrement de l'archive est dérivée du secret de référence. Pour la récupérer côté opérateur, utiliser la même valeur Base64 du secret.
- Les WAV restent non validés jusqu'à écoute par le propriétaire de la voix.

## Configurer le secret
1. Préparer la chaîne Base64 de la référence audio compressée, sans retour à la ligne.
2. Dans GitHub, ouvrir Settings → Secrets and variables → Actions → New repository secret.
3. Nom : `WOLOF_REFERENCE_AUDIO_B64`.
4. Valeur : coller la chaîne Base64 complète.
5. Ouvrir Actions → « Wolof — échantillons privés avec référence vocale » → Run workflow.
6. Vérifier que l'artefact est nommé `wolof-voice-reference-samples-encrypted`.

La valeur Base64 est une donnée biométrique personnelle : ne pas la placer dans un issue, une PR, un commentaire ou un fichier suivi par Git.

## Déchiffrement de l'archive
Le workflow chiffre `wolof-voice-reference-samples.zip` avec OpenSSL AES-256-CBC, PBKDF2, 200 000 itérations. La phrase de passe est le SHA-256 hexadécimal de la valeur exacte de `WOLOF_REFERENCE_AUDIO_B64`.

Sous un environnement disposant d'OpenSSL :
```sh
export WOLOF_REFERENCE_AUDIO_B64='COLLER_LA_VALEUR_DU_SECRET'
export WOLOF_ARTIFACT_ENCRYPTION_KEY="$(printf '%s' "$WOLOF_REFERENCE_AUDIO_B64" | sha256sum | cut -d ' ' -f1)"
openssl enc -d -aes-256-cbc -pbkdf2 -iter 200000 \
  -in wolof-voice-reference-samples.zip.enc \
  -out wolof-voice-reference-samples.zip \
  -pass env:WOLOF_ARTIFACT_ENCRYPTION_KEY
```

## Statut
Cette procédure ne constitue pas une validation linguistique. Contrôler les WAV et les faire écouter au propriétaire avant toute génération à grande échelle. Ne jamais fusionner cette PR dans `main` avant validation explicite.
