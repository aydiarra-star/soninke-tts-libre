#!/usr/bin/env python3
"""Validate the existing Soninke WAV archive and stage it for a review PR."""
from __future__ import annotations
import csv, io, json, re, shutil, sys, tempfile, wave, zipfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
import gdown

ROOT = Path.cwd()
TEXT_COLUMNS = ("text", "word", "soninke", "phrase")
EXPECTED_ENTRIES = 577
EXPECTED_AUDIO = 576

def fail(message):
    raise SystemExit("ERREUR: " + message)

def download_archive(file_id, confirmed, destination):
    if confirmed.lower() not in {"true", "yes", "oui"}:
        fail("Confirme que le ZIP est partagé Toute personne disposant du lien - Lecteur.")
    if not re.fullmatch(r"[A-Za-z0-9_-]{10,}", file_id):
        fail("Identifiant Google Drive invalide. Fournis uniquement l'ID du fichier.")
    output = destination / "soninke_audio_export.zip"
    result = gdown.download(id=file_id, output=str(output), quiet=False, fuzzy=True)
    if not result or not output.is_file() or output.stat().st_size < 1000:
        fail("Téléchargement impossible. Vérifie le partage du ZIP et son ID.")
    print("ZIP téléchargé:", output.stat().st_size, "octets")
    return output

def validate_archive(archive, staged_audio):
    with zipfile.ZipFile(archive) as zf:
        bad = zf.testzip()
        if bad:
            fail("Archive ZIP endommagée: " + bad)
        manifests = [n for n in zf.namelist() if PurePosixPath(n).name.lower() == "manifest.csv"]
        if len(manifests) != 1:
            fail("Un seul manifest.csv attendu; trouvé: " + str(len(manifests)))
        rows = list(csv.DictReader(io.StringIO(zf.read(manifests[0]).decode("utf-8-sig"))))
        if len(rows) != EXPECTED_ENTRIES:
            fail("577 entrées attendues; trouvé: " + str(len(rows)))
        if not rows or "id" not in rows[0] or not any(c in rows[0] for c in TEXT_COLUMNS):
            fail("Colonnes id et transcription (text/word/soninke/phrase) requises.")
        ids = [r.get("id", "").strip() for r in rows]
        if any(not x for x in ids) or len(ids) != len(set(ids)):
            fail("Identifiants vides ou dupliqués.")
        by_basename = {}
        for name in zf.namelist():
            by_basename.setdefault(PurePosixPath(name).name, []).append(name)
        staged_audio.mkdir(parents=True, exist_ok=True)
        copied = []
        for aid in ids:
            candidates = [n for n in by_basename.get(aid + ".wav", [])
                          if not PurePosixPath(n).name.lower().startswith("copie de ")]
            exact = [n for n in candidates if n == "audio/" + aid + ".wav"]
            chosen = exact[0] if exact else (candidates[0] if len(candidates) == 1 else None)
            if not chosen:
                continue
            target = staged_audio / (aid + ".wav")
            target.write_bytes(zf.read(chosen))
            try:
                with wave.open(str(target), "rb") as wav:
                    if wav.getnframes() <= 0 or wav.getframerate() <= 0 or wav.getnchannels() <= 0:
                        fail("WAV vide ou invalide: " + aid)
            except (wave.Error, EOFError) as exc:
                fail("WAV illisible " + aid + ": " + str(exc))
            copied.append(aid)
    missing = sorted(set(ids) - set(copied))
    print("Manifeste:", len(rows), "| WAV distincts valides:", len(copied), "| sans WAV:", missing)
    if len(copied) != EXPECTED_AUDIO or missing != ["snk-00308"]:
        fail("Le lot ne correspond pas au contrôle attendu; aucun changement ne sera proposé.")
    return rows, missing

def build_manifest(rows, missing, audio_dir):
    entries = []
    for row in rows:
        aid = row["id"].strip()
        word = next((row.get(c, "").strip() for c in TEXT_COLUMNS if row.get(c, "").strip()), "")
        if not word:
            fail("Transcription vide pour " + aid)
        duration_value = row.get("duration_seconds") or row.get("duration") or row.get("duration_s")
        try:
            duration = float(duration_value) if duration_value else None
        except ValueError:
            duration = None
        available = (audio_dir / (aid + ".wav")).is_file()
        entries.append({
            "id": aid, "word": word,
            "audioPath": "audio/" + aid + ".wav" if available else None,
            "audioAvailable": available, "durationSeconds": duration,
            "technicalStatus": row.get("technical_status") or "unknown",
            "source": row.get("source", ""), "license": row.get("license", ""),
            "attribution": row.get("attribution", "")
        })
    data_dir = ROOT / "data"
    data_dir.mkdir(exist_ok=True)
    (data_dir / "audio-manifest.json").write_text(json.dumps({
        "schemaVersion": 1, "createdAt": datetime.now(timezone.utc).isoformat(),
        "sourceArchive": "soninke_audio_export.zip", "entryCount": len(entries),
        "audioCount": sum(1 for e in entries if e["audioAvailable"]),
        "missingAudioIds": missing, "entries": entries
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def update_lexique():
    path = ROOT / "lexique.js"
    js = path.read_text(encoding="utf-8")
    if "audioById" not in js:
        anchor = '      card.append(el("h2", "corpus-soninke", entry.word));\n'
        if anchor not in js:
            fail("Point d'insertion du lecteur introuvable dans lexique.js.")
        player = '''      const audioInfo = audioById.get(entry.id);
      if (audioInfo && audioInfo.audioAvailable && audioInfo.audioPath) {
        const audio = el("audio", "lexicon-audio-player");
        audio.controls = true;
        audio.preload = "none";
        audio.src = audioInfo.audioPath;
        audio.setAttribute("aria-label", "Écouter la prononciation de " + entry.word);
        card.append(audio);
        card.append(el("p", "corpus-field-label", "Audio disponible" + (audioInfo.durationSeconds ? " · " + audioInfo.durationSeconds.toFixed(2).replace(".", ",") + " s" : "")));
      } else {
        card.append(el("p", "corpus-caveat", "Audio indisponible pour cette entrée ; aucun fichier n’a été inventé."));
      }
'''
        js = js.replace(anchor, anchor + player, 1)
        anchor_entries = "  let entries = [];\n"
        if anchor_entries not in js:
            fail("Déclaration entries introuvable dans lexique.js.")
        js = js.replace(anchor_entries, anchor_entries + "  let audioById = new Map();\n", 1)
    pattern = re.compile(
        r'  fetch\(DATA_URL\)\n'
        r'    \.then\(response => \{ if \(!response\.ok\) throw new Error\("HTTP " \+ response\.status\); return response\.text\(\); \}\)\n'
        r'    \.then\(text => \{\n'
        r'      entries = text\.split\(/\\\\r\?\\\\n/\)\.filter\(line => line\.trim\(\)\)\.map\(line => JSON\.parse\(line\)\);\n'
        r'      if \(!entries\.length\) throw new Error\("lexique vide"\);\n'
        r'      render\(\);\n'
        r'    \}\)\n'
        r'    \.catch\(\(\) => \{\n'
        r'      count\.textContent = "Lexique indisponible";\n'
        r'      message\.textContent = "Impossible de charger le lexique\. Vérifiez que la page est ouverte depuis le site publié\.";\n'
        r'    \}\);'
    )
    replacement = '''  Promise.all([
    fetch(DATA_URL).then(response => { if (!response.ok) throw new Error("Lexique HTTP " + response.status); return response.text(); }),
    fetch("data/audio-manifest.json").then(response => { if (!response.ok) throw new Error("Manifeste audio HTTP " + response.status); return response.json(); })
  ])
    .then(([text, audioData]) => {
      entries = text.split(/\\\\r?\\\\n/).filter(line => line.trim()).map(line => JSON.parse(line));
      if (!entries.length) throw new Error("lexique vide");
      audioById = new Map((audioData.entries || []).map(item => [item.id, item]));
      render();
    })
    .catch(error => {
      count.textContent = "Lexique indisponible";
      message.textContent = "Impossible de charger le lexique et son manifeste audio. " + error.message;
    });'''
    if pattern.search(js):
        js = pattern.sub(lambda _: replacement, js, count=1)
    elif 'fetch("data/audio-manifest.json")' not in js:
        fail("Bloc de chargement introuvable; arrêt sans modification approximative.")
    path.write_text(js, encoding="utf-8")

def main():
    if len(sys.argv) != 3:
        fail("Usage: publish_audio_bundle_actions.py GOOGLE_DRIVE_FILE_ID PUBLIC_LINK_CONFIRMED")
    with tempfile.TemporaryDirectory(prefix="soninke-audio-") as tmp:
        tmp = Path(tmp)
        archive = download_archive(sys.argv[1].strip(), sys.argv[2].strip(), tmp)
        staged = tmp / "audio"
        rows, missing = validate_archive(archive, staged)
        destination = ROOT / "audio"
        if destination.exists():
            shutil.rmtree(destination)
        shutil.copytree(staged, destination)
        build_manifest(rows, missing, destination)
        update_lexique()
        docs = ROOT / "docs" / "AUDIO-BUNDLE-INTEGRATION.md"
        docs.parent.mkdir(exist_ok=True)
        docs.write_text(
            "# Intégration du lot audio du lexique\n\n"
            "Les WAV disponibles sont servis sous audio/ et référencés dans data/audio-manifest.json. "
            "La page lexique affiche un lecteur HTML5 pour chaque entrée avec WAV. "
            "Une entrée sans fichier reste visible avec un message explicite.\n\n"
            "## Contrôles du lot\n\n"
            "- Entrées du manifeste: " + str(len(rows)) + "\n"
            "- WAV distincts valides: " + str(len(list(destination.glob("snk-*.wav")))) + "\n"
            "- Identifiants sans WAV: " + ", ".join(missing) + "\n"
            "- Le doublon exact Copie de snk-00001.wav est ignoré.\n"
            "- Aucun audio n'est fabriqué pour combler une absence.\n\n"
            "La validation linguistique reste distincte de la disponibilité technique.\n",
            encoding="utf-8"
        )
    print("Préparation terminée; le workflow créera une Pull Request séparée, sans push direct vers main.")

if __name__ == "__main__":
    main()
