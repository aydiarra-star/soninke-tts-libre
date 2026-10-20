"""Publish the existing Soninke WAV bundle from Google Colab to a review PR."""
from pathlib import Path
from datetime import datetime, timezone
import base64, csv, getpass, io, json, os, shutil, subprocess, tempfile, wave, zipfile
import requests

REPO = "aydiarra-star/xamxam-xara"
ARCHIVE_DEFAULT = Path("/content/drive/MyDrive/SONINKE_TTS_LIBRE/soninke_audio_export.zip")

def run(args, **kwargs):
    print("+", " ".join(str(x) for x in args[:4]), "...")
    return subprocess.run(args, check=True, **kwargs)

def main():
    # Ne demande pas l'accès à Google Drive si l'archive est déjà disponible.
    archive = ARCHIVE_DEFAULT
    drive_root = Path("/content/drive/MyDrive")
    if not archive.is_file():
        try:
            from google.colab import drive
            drive.mount("/content/drive")
        except Exception as exc:
            print("Montage Google Drive indisponible; passage au sélecteur de fichier:", type(exc).__name__)
        candidates = list(drive_root.rglob("soninke_audio_export.zip")) if drive_root.is_dir() else []
        if candidates:
            archive = candidates[0]
        else:
            print("Archive absente de Google Drive. Sélectionne l'archive ZIP existante depuis l'appareil.")
            from google.colab import files
            uploaded = files.upload()
            matches = [name for name in uploaded if name.lower().endswith(".zip") and "soninke" in name.lower()]
            if len(matches) != 1:
                raise FileNotFoundError("Téléverse un seul ZIP contenant l'export audio Soninké.")
            archive = Path("/content") / matches[0]
    if not archive.is_file():
        raise FileNotFoundError("Archive ZIP introuvable: " + str(archive))
    print("Archive:", archive, "bytes:", archive.stat().st_size)

    with zipfile.ZipFile(archive) as zf:
        bad = zf.testzip()
        if bad:
            raise RuntimeError("Archive endommagee: " + bad)
        rows = list(csv.DictReader(io.StringIO(zf.read("manifest.csv").decode("utf-8-sig"))))
        if len(rows) != 577:
            raise RuntimeError("Le manifeste doit contenir 577 entrees, trouve: " + str(len(rows)))
        if not rows:
            raise RuntimeError("Manifeste audio vide.")
        required = {"id"}
        if not required.issubset(rows[0].keys()):
            raise RuntimeError("Colonne id absente du manifeste audio.")
        text_columns = ("text", "word", "soninke", "phrase")
        if not any(column in rows[0] for column in text_columns):
            raise RuntimeError("Colonne de transcription absente (text/word/soninke/phrase).")
        names = set(zf.namelist())
        temp = Path("/content/soninke-audio-publish")
        if temp.exists():
            shutil.rmtree(temp)
        (temp / "audio").mkdir(parents=True)
        copied = []
        for row in rows:
            aid = row["id"]
            member = "audio/" + aid + ".wav"
            if member in names:
                target = temp / "audio" / (aid + ".wav")
                target.write_bytes(zf.read(member))
                with wave.open(str(target), "rb") as wav:
                    if wav.getnframes() <= 0:
                        raise RuntimeError("WAV vide: " + aid)
                copied.append(aid)

    ids = [r["id"] for r in rows]
    if len(ids) != len(set(ids)):
        raise RuntimeError("Identifiants dupliques dans le manifeste.")
    missing = sorted(set(ids) - set(copied))
    print("Manifeste:", len(rows), "| WAV distincts:", len(copied), "| sans WAV:", missing)
    if len(copied) < 500 or len(missing) > 10:
        raise RuntimeError("Controle qualite refuse la publication.")

    token = getpass.getpass("Jeton GitHub temporaire masque: ").strip()
    if not token:
        raise RuntimeError("Jeton vide.")
    repo_dir = Path("/content/soninke-tts-libre")
    if repo_dir.exists():
        shutil.rmtree(repo_dir)
    run(["git", "clone", "--depth", "1", "https://github.com/" + REPO + ".git", str(repo_dir)])
    branch = "audio/integrate-lexicon-wav-" + datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    run(["git", "-C", str(repo_dir), "checkout", "-b", branch])

    target_audio = repo_dir / "audio"
    target_audio.mkdir(exist_ok=True)
    for wav_file in (temp / "audio").glob("snk-*.wav"):
        shutil.copy2(wav_file, target_audio / wav_file.name)

    entries = []
    for row in rows:
        aid = row["id"]
        available = (target_audio / (aid + ".wav")).is_file()
        word = next((row.get(column, "").strip() for column in ("text", "word", "soninke", "phrase") if row.get(column, "").strip()), "")
        if not word:
            raise RuntimeError("Transcription vide pour " + aid)
        duration_value = row.get("duration_seconds") or row.get("duration") or row.get("duration_s")
        entries.append({
            "id": aid, "word": word,
            "audioPath": "audio/" + aid + ".wav" if available else None,
            "audioAvailable": available,
            "durationSeconds": float(duration_value) if duration_value else None,
            "technicalStatus": row.get("technical_status") or "unknown",
            "source": row.get("source", ""), "license": row.get("license", ""),
            "attribution": row.get("attribution", "")
        })
    data_dir = repo_dir / "data"
    data_dir.mkdir(exist_ok=True)
    (data_dir / "audio-manifest.json").write_text(json.dumps({
        "schemaVersion": 1, "createdAt": datetime.now(timezone.utc).isoformat(),
        "sourceArchive": "soninke_audio_export.zip", "entryCount": len(entries),
        "audioCount": sum(1 for e in entries if e["audioAvailable"]),
        "missingAudioIds": [e["id"] for e in entries if not e["audioAvailable"]],
        "entries": entries
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    js_path = repo_dir / "lexique.js"
    js = js_path.read_text(encoding="utf-8")
    old_card = '      card.append(el("h2", "corpus-soninke", entry.word));\n'
    new_card = '''      card.append(el("h2", "corpus-soninke", entry.word));
      const audioInfo = audioById.get(entry.id);
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
    if old_card not in js:
        raise RuntimeError("Point d’insertion du lecteur introuvable dans lexique.js; aucune modification approximative.")
    js = js.replace(old_card, new_card, 1)
    old_load = '''  fetch(DATA_URL)
    .then(response => { if (!response.ok) throw new Error("HTTP " + response.status); return response.text(); })
    .then(text => {
      entries = text.split(/\\r?\\n/).filter(line => line.trim()).map(line => JSON.parse(line));
      if (!entries.length) throw new Error("lexique vide");
      render();
    })
    .catch(() => {
      count.textContent = "Lexique indisponible";
      message.textContent = "Impossible de charger le lexique. Vérifiez que la page est ouverte depuis le site publié.";
    });
'''
    new_load = '''  let audioById = new Map();
  Promise.all([
    fetch(DATA_URL).then(response => { if (!response.ok) throw new Error("Lexique HTTP " + response.status); return response.text(); }),
    fetch("data/audio-manifest.json").then(response => { if (!response.ok) throw new Error("Manifeste audio HTTP " + response.status); return response.json(); })
  ])
    .then(([text, audioData]) => {
      entries = text.split(/\\r?\\n/).filter(line => line.trim()).map(line => JSON.parse(line));
      if (!entries.length) throw new Error("lexique vide");
      audioById = new Map((audioData.entries || []).map(item => [item.id, item]));
      render();
    })
    .catch(error => {
      count.textContent = "Lexique indisponible";
      message.textContent = "Impossible de charger le lexique et son manifeste audio. " + error.message;
    });
'''
    if old_load not in js:
        raise RuntimeError("Bloc de chargement introuvable dans lexique.js; aucune modification approximative.")
    js_path.write_text(js.replace(old_load, new_load, 1), encoding="utf-8")

    docs = repo_dir / "docs" / "AUDIO-BUNDLE-INTEGRATION.md"
    docs.parent.mkdir(exist_ok=True)
    docs.write_text(
        "# Intégration du lot audio du lexique\n\n"
        "Les fichiers sont servis sous audio/snk-NNNNN.wav et le mapping ID/terme/disponibilité est publié dans data/audio-manifest.json. La page lexique affiche un lecteur HTML5 pour chaque entrée qui dispose d’un WAV. Une entrée sans fichier reste visible avec un message explicite.\n\n"
        "## Contrôles de ce lot\n\n"
        "- Entrées du manifeste: " + str(len(rows)) + "\n"
        "- Fichiers WAV copiés et décodés: " + str(len(copied)) + "\n"
        "- Identifiants sans WAV: " + (", ".join(missing) if missing else "aucun") + "\n"
        "- Le doublon Copie de snk-00001.wav est ignoré.\n"
        "- Sources, licences et attributions conservées dans le manifeste audio.\n\n"
        "La validation linguistique reste distincte de la disponibilité technique. Aucun audio n’est fabriqué pour combler une absence.\n",
        encoding="utf-8"
    )
    if len(list(target_audio.glob("snk-*.wav"))) != len(copied):
        raise RuntimeError("Le nombre de WAV préparés ne correspond pas au contrôle.")
    run(["git", "-C", str(repo_dir), "config", "user.name", "Soninke TTS Libre automation"])
    run(["git", "-C", str(repo_dir), "config", "user.email", "soninke-tts-automation@users.noreply.github.com"])
    run(["git", "-C", str(repo_dir), "add", "audio", "data/audio-manifest.json", "lexique.js", "docs/AUDIO-BUNDLE-INTEGRATION.md"])
    run(["git", "-C", str(repo_dir), "commit", "-m", "feat(audio): integrate lexicon WAV players and manifest"])
    auth = base64.b64encode(("x-access-token:" + token).encode()).decode()
    env = os.environ.copy()
    env["GIT_CONFIG_COUNT"] = "1"
    env["GIT_CONFIG_KEY_0"] = "http.https://github.com/.extraheader"
    env["GIT_CONFIG_VALUE_0"] = "AUTHORIZATION: basic " + auth
    run(["git", "-C", str(repo_dir), "push", "origin", branch], env=env)
    headers = {"Authorization": "Bearer " + token, "Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
    body = {
        "title": "feat(audio): intégrer les audios du lexique soninké",
        "head": branch, "base": "main",
        "body": "## Objectif\nRendre les WAV existants accessibles depuis le lexique.\n\n## Changements\n- WAV sous audio/ sans doublon.\n- Manifeste audio avec mapping ID/fichier, provenance et licence.\n- Lecteur HTML5 pour chaque fiche avec audio.\n- Message explicite pour les entrées sans fichier.\n\n## Contrôles\n- 577 entrées du manifeste; " + str(len(copied)) + " WAV distincts.\n- Entrées sans WAV: " + (", ".join(missing) if missing else "aucune") + ".\n- Aucune fusion automatique dans main.\n\nÀ vérifier par CI et sur Safari iPhone avant fusion."
    }
    response = requests.post("https://api.github.com/repos/" + REPO + "/pulls", headers=headers, json=body, timeout=30)
    if response.status_code != 201:
        raise RuntimeError("Push effectué mais PR non confirmée: HTTP " + str(response.status_code) + " " + response.text[:400])
    print("PR créée:", response.json().get("html_url"))
    print("Branche:", branch)
    print("La PR n’est pas fusionnée automatiquement.")
    token = None

if __name__ == "__main__":
    main()
